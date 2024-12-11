# Released under the MIT License. See LICENSE for details.
#
"""Defines the runaround co-op game."""

# We wear the cone of shame.
# pylint: disable=too-many-lines

# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

import random
from typing import TYPE_CHECKING

import ba
from bastd.actor.bomb import TNTSpawner, JumpPadSpawner
from bastd.actor.scoreboard import Scoreboard
from bastd.actor.respawnicon import RespawnIcon
from bastd.gameutils import SharedObjects
from bastd.actor.spazbot import (
    SpazBotSet,
    SpazBotDiedMessage,
    SpazBot,
    BomberBot,
    BrawlerBot,
    TriggerBot,
    TriggerBotPro,
    BomberBotProShielded,
    TriggerBotProShielded,
    ChargerBot,
    ChargerBotProShielded,
    StickyBot,
    ExplodeyBot,
    BrawlerBotProShielded,
    BomberBotPro,
    BrawlerBotPro,
    SplashBot,
    FrostyBot,
    SoldatBot,
    MicBot,
    WaiterBot,
    NoirBot,
    MellyBot,
    ExplodeyBotNoTimeLimit,
    ToxicBot,
)

from explodinary.lib.unlock import UnlockPopup

if TYPE_CHECKING:
    from typing import Any, Sequence

from bastd.game.runaround import (
    RunaroundGame,
    Player,
    Wave,
    Spacing,
    Spawn,
    Point,
    Preset,
)


class RouteRouletteGame(RunaroundGame):
    """Game involving trying to bomb bots as they walk through the map."""

    name = "Route Roulette"
    description = "Prevent enemies from reaching the exit."
    tips = [
        "Use Jump-Pads to reach the upper level.",
        "No, you can't get up on the ledge. You have to throw bombs.",
    ]
    default_music = ba.MusicType.ROULETTE

    # How fast our various bot types walk.
    _bot_speed_map: dict[type[SpazBot], float] = {
        BomberBot: 0.48,
        BomberBotPro: 0.48,
        BomberBotProShielded: 0.48,
        BrawlerBot: 0.57,
        BrawlerBotPro: 0.57,
        BrawlerBotProShielded: 0.57,
        TriggerBot: 0.73,
        TriggerBotPro: 0.78,
        TriggerBotProShielded: 0.78,
        ChargerBot: 0.78,
        ChargerBotProShielded: 0.15,
        ExplodeyBot: 1.0,
        StickyBot: 0.5,
        SplashBot: 0.7,
        WaiterBot: 0.6,
        SoldatBot: 0.45,
        FrostyBot: 0.65,
        MicBot: 0.35,
        MellyBot: 0.5,
        NoirBot: 0.55,
        ToxicBot: 0.65,
        ExplodeyBotNoTimeLimit: 0.7,
    }

    def __init__(self, settings: dict):
        settings["map"] = "Route Roulette"
        ba.CoopGameActivity.__init__(self, settings)
        shared = SharedObjects.get()
        self._preset = Preset(settings.get("preset", "endless"))

        self._player_death_sound = ba.getsound("playerDeath")
        self._new_wave_sound = ba.getsound("scoreHit01")
        self._winsound = ba.getsound("score")
        self._cashregistersound = ba.getsound("cashRegister")
        self._bad_guy_score_sound = ba.getsound("shieldDown")
        self._heart_tex = ba.gettexture("heart")
        self._heart_model_opaque = ba.getmodel("heartOpaque")
        self._heart_model_transparent = ba.getmodel("heartTransparent")

        self._a_player_has_been_killed = False
        self._spawn_center = self._map_type.defs.points["spawn1"][0:3]
        self._tntspawnpos = self._map_type.defs.points["tnt_loc"][0:3]
        self._tntspawnpos2 = self._map_type.defs.points["tnt_loc2"][0:3]
        self._jumppadspawnpos = self._map_type.defs.points["jump_loc"][0:3]
        self._jumppad2spawnpos = self._map_type.defs.points["jump_loc_s"][0:3]
        self._powerup_center = self._map_type.defs.boxes["powerup_region"][0:3]
        self._powerup_spread = (
            self._map_type.defs.boxes["powerup_region"][6] * 0.5,
            self._map_type.defs.boxes["powerup_region"][8] * 0.5,
        )

        self._score_region_material = ba.Material()
        self._score_region_material.add_actions(
            conditions=("they_have_material", shared.player_material),
            actions=(
                ("modify_part_collision", "collide", True),
                ("modify_part_collision", "physical", False),
                ("call", "at_connect", self._handle_reached_end),
            ),
        )

        self._last_wave_end_time = ba.time()
        self._player_has_picked_up_powerup = False
        self._scoreboard: Scoreboard | None = None
        self._game_over = False
        self._wavenum = 0
        self._can_end_wave = True
        self._score = 0
        self._time_bonus = 0
        self._score_region: ba.Actor | None = None
        self._dingsound = ba.getsound("dingSmall")
        self._dingsoundhigh = ba.getsound("dingSmallHigh")
        self._exclude_powerups: list[str] | None = None
        self._have_tnt: bool | None = None
        self._have_jumppad: bool | None = None
        self._waves: list[Wave] | None = None
        self._bots = SpazBotSet()
        self._tntspawner: TNTSpawner | None = None
        self._tntspawner2: TNTSpawner | None = None
        self._jumppadspawner: JumpPadSpawner | None = None
        self._lives_bg: ba.NodeActor | None = None
        self._start_lives = 10
        self._lives = self._start_lives
        self._lives_text: ba.NodeActor | None = None
        self._flawless = True
        self._time_bonus_timer: ba.Timer | None = None
        self._time_bonus_text: ba.NodeActor | None = None
        self._time_bonus_mult: float | None = None
        self._wave_text: ba.NodeActor | None = None
        self._flawless_bonus: int | None = None
        self._wave_update_timer: ba.Timer | None = None

        ba.getsession().max_players = 5

    def on_begin(self) -> None:
        super().on_begin()
        self._exclude_powerups = []
        self._have_tnt = True
        self._have_jumppad = True
        if self._have_tnt:
            self._tntspawner = TNTSpawner(position=self._tntspawnpos)
            self._tntspawner2 = TNTSpawner(position=self._tntspawnpos2)

        if self._have_jumppad:
            self._jumppadspawner = JumpPadSpawner(
                position=self._jumppadspawnpos
            )
            self._jumppadspawner2 = JumpPadSpawner(
                position=self._jumppad2spawnpos
            )
        self._lives_bg.node.color = (0, 0.7, 0.3)

    def _start_next_wave(self) -> None:
        # FIXME: Need to split this up.
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        self.show_zoom_message(
            ba.Lstr(
                value="${A} ${B}",
                subs=[
                    ("${A}", ba.Lstr(resource="waveText")),
                    ("${B}", str(self._wavenum)),
                ],
            ),
            scale=1.0,
            duration=1.0,
            trail=True,
        )
        ba.timer(0.4, ba.Call(ba.playsound, self._new_wave_sound))
        t_sec = 0.0
        base_delay = 0.5
        delay = 0.0
        bot_types: list[Spawn | Spacing | None] = []

        if self._preset in {Preset.ENDLESS, Preset.ENDLESS_TOURNAMENT}:
            level = self._wavenum
            target_points = (level + 1) * 8.0
            group_count = random.randint(1, 3)
            entries: list[Spawn | Spacing | None] = []
            spaz_types: list[tuple[type[SpazBot], float]] = []
            if level < 6:
                spaz_types += [(BomberBot, 5.0)]
                spaz_types += [(SoldatBot, 5.0)]
            if level < 10:
                spaz_types += [(BrawlerBot, 5.0)]
                spaz_types += [(NoirBot, 5.0)]
            if level < 15:
                spaz_types += [(TriggerBot, 6.0)]
            if level > 5:
                spaz_types += [(TriggerBotPro, 7.5)] * (1 + (level - 5) // 7)
            if level > 2:
                spaz_types += [(BomberBotProShielded, 8.0)] * (
                    1 + (level - 2) // 6
                )
            if level > 6:
                spaz_types += [(TriggerBotProShielded, 8.0)] * (
                    1 + (level - 6) // 5
                )
            if level > 1:
                spaz_types += [(ChargerBot, 5.0)] * (1 + (level - 1) // 4)
            if level > 5:
                spaz_types += [(ChargerBot, 7.5)] * (1 + (level - 7) // 3)

            # Bot type, their effect on target points.
            defender_types: list[tuple[type[SpazBot], float]] = [
                (BomberBot, 0.9),
                (BrawlerBot, 0.9),
                (TriggerBot, 0.85),
                (SoldatBot, 0.7),
                (NoirBot, 0.9),
            ]
            if level > 2:
                defender_types += [(ChargerBot, 0.75)]
            if level > 4:
                defender_types += [(StickyBot, 0.7)] * (1 + (level - 5) // 6)
                defender_types += [(WaiterBot, 0.7)] * (1 + (level - 5) // 6)
            if level > 6:
                defender_types += [(ExplodeyBot, 0.7)] * (1 + (level - 5) // 5)
                defender_types += [(ExplodeyBotNoTimeLimit, 0.7)] * (
                    1 + (level - 5) // 5
                )
                defender_types += [(MicBot, 0.7)] * (1 + (level - 5) // 5)
                defender_types += [(NoirBot, 0.7)] * (1 + (level - 5) // 5)
            if level > 8:
                defender_types += [(BrawlerBotProShielded, 0.65)] * (
                    1 + (level - 5) // 4
                )
                defender_types += [(FrostyBot, 0.65)] * (1 + (level - 5) // 4)
                defender_types += [(MellyBot, 0.7)] * (1 + (level - 5) // 6)
            if level > 10:
                defender_types += [(TriggerBotProShielded, 0.6)] * (
                    1 + (level - 6) // 3
                )
                defender_types += [(SplashBot, 0.65)] * (1 + (level - 5) // 4)
                defender_types += [(ToxicBot, 0.65)] * (1 + (level - 5) // 4)

            for group in range(group_count):
                this_target_point_s = target_points / group_count

                # Adding spacing makes things slightly harder.
                rval = random.random()
                if rval < 0.07:
                    spacing = 1.5
                    this_target_point_s *= 0.85
                elif rval < 0.15:
                    spacing = 1.0
                    this_target_point_s *= 0.9
                else:
                    spacing = 0.0

                path = random.randint(1, 3)

                # Don't allow hard paths on early levels.
                if level < 3:
                    if path == 1:
                        path = 3

                # Easy path.
                if path == 3:
                    pass

                # Harder path.
                elif path == 2:
                    this_target_point_s *= 0.8

                # Even harder path.
                elif path == 1:
                    this_target_point_s *= 0.7

                # Looping forward.
                elif path == 4:
                    this_target_point_s *= 0.7

                # Looping backward.
                elif path == 5:
                    this_target_point_s *= 0.7

                # Random.
                elif path == 6:
                    this_target_point_s *= 0.7

                def _add_defender(
                    defender_type: tuple[type[SpazBot], float], pnt: Point
                ) -> tuple[float, Spawn]:
                    # This is ok because we call it immediately.
                    # pylint: disable=cell-var-from-loop
                    return this_target_point_s * defender_type[1], Spawn(
                        defender_type[0], point=pnt
                    )

                # Add defenders.
                defender_type1 = defender_types[
                    random.randrange(len(defender_types))
                ]
                defender_type2 = defender_types[
                    random.randrange(len(defender_types))
                ]
                defender1 = defender2 = None
                if (
                    (group == 0)
                    or (group == 1 and level > 3)
                    or (group == 2 and level > 5)
                ):
                    if random.random() < min(0.75, (level - 1) * 0.11):
                        this_target_point_s, defender1 = _add_defender(
                            defender_type1, Point.BOTTOM_LEFT
                        )
                    if random.random() < min(0.75, (level - 1) * 0.04):
                        this_target_point_s, defender2 = _add_defender(
                            defender_type2, Point.BOTTOM_RIGHT
                        )

                spaz_type = spaz_types[random.randrange(len(spaz_types))]
                member_count = max(
                    1, int(round(this_target_point_s / spaz_type[1]))
                )
                for i, _member in enumerate(range(member_count)):
                    if path == 4:
                        this_path = i % 3  # Looping forward.
                    elif path == 5:
                        this_path = 3 - (i % 3)  # Looping backward.
                    elif path == 6:
                        this_path = random.randint(1, 3)  # Random.
                    else:
                        this_path = path
                    entries.append(Spawn(spaz_type[0], path=this_path))
                    if spacing != 0.0:
                        entries.append(Spacing(duration=spacing))

                if defender1 is not None:
                    entries.append(defender1)
                if defender2 is not None:
                    entries.append(defender2)

                # Some spacing between groups.
                rval = random.random()
                if rval < 0.1:
                    spacing = 5.0
                elif rval < 0.5:
                    spacing = 1.0
                else:
                    spacing = 1.0
                entries.append(Spacing(duration=spacing))

            wave = Wave(entries=entries)

        else:
            assert self._waves is not None
            wave = self._waves[self._wavenum - 1]

        bot_types += wave.entries
        self._time_bonus_mult = 1.0
        this_flawless_bonus = 0
        non_runner_spawn_time = 1.0

        for info in bot_types:
            if info is None:
                continue
            if isinstance(info, Spacing):
                t_sec += info.duration
                continue
            bot_type = info.type
            path = info.path
            self._time_bonus_mult += bot_type.points_mult * 0.02
            this_flawless_bonus += bot_type.points_mult * 5

            # If its got a position, use that.
            if info.point is not None:
                point = info.point
            else:
                point = Point.START

            # Space our our slower bots.
            delay = base_delay
            delay /= self._get_bot_speed(bot_type)
            t_sec += delay * 0.5
            tcall = ba.Call(
                self.add_bot_at_point,
                point,
                bot_type,
                path,
                0.1 if point is Point.START else non_runner_spawn_time,
            )
            ba.timer(t_sec, tcall)
            t_sec += delay * 0.5

        # We can end the wave after all the spawning happens.
        ba.timer(
            t_sec - delay * 0.5 + non_runner_spawn_time + 0.01,
            self._set_can_end_wave,
        )

        # Reset our time bonus.
        # In this game we use a constant time bonus so it erodes away in
        # roughly the same time (since the time limit a wave can take is
        # relatively constant) ..we then post-multiply a modifier to adjust
        # points.
        self._time_bonus = 150
        self._flawless_bonus = this_flawless_bonus
        assert self._time_bonus_mult is not None
        txtval = ba.Lstr(
            value="${A}: ${B}",
            subs=[
                ("${A}", ba.Lstr(resource="timeBonusText")),
                ("${B}", str(int(self._time_bonus * self._time_bonus_mult))),
            ],
        )
        self._time_bonus_text = ba.NodeActor(
            ba.newnode(
                "text",
                attrs={
                    "v_attach": "top",
                    "h_attach": "left",
                    "h_align": "left",
                    "color": (1, 1, 0.0, 1),
                    "shadow": 1.0,
                    "vr_depth": -30,
                    "flatness": 1.0,
                    "position": (18, -170),
                    "scale": 0.8,
                    "text": txtval,
                },
            )
        )

        ba.timer(t_sec, self._start_time_bonus_timer)

        # Keep track of when this wave finishes emerging. We wanna stop
        # dropping land-mines powerups at some point (otherwise a crafty
        # player could fill the whole map with them)
        self._last_wave_end_time = ba.time() + t_sec
        totalwaves = str(len(self._waves)) if self._waves is not None else "??"
        txtval = ba.Lstr(
            value="${A} ${B}",
            subs=[
                ("${A}", ba.Lstr(resource="waveText")),
                (
                    "${B}",
                    str(self._wavenum)
                    + (
                        ""
                        if self._preset
                        in {Preset.ENDLESS, Preset.ENDLESS_TOURNAMENT}
                        else f"/{totalwaves}"
                    ),
                ),
            ],
        )
        self._wave_text = ba.NodeActor(
            ba.newnode(
                "text",
                attrs={
                    "v_attach": "top",
                    "h_attach": "left",
                    "h_align": "left",
                    "shadow": 1.0,
                    "vr_depth": -10,
                    "color": (1, 1, 1, 1),
                    "flatness": 1.0,
                    "position": (53, -145),
                    "scale": 1,
                    "text": txtval,
                },
            )
        )

    def _update_scores(self) -> None:
        score = self._score
        unlockedAmigo = ba.app.config.get("BSE: Adios Amigo", False)
        force_popup = False  # debug
        if score >= 2000:
            if not ba.app.config.get("BSE: Adios Amigo", False):
                UnlockPopup()
                self._popuped = True
                ba.app.config["BSE: Adios Amigo"] = True
                ba.app.config.commit()

        assert self._scoreboard is not None
        self._scoreboard.set_team_value(self.teams[0], score, max_score=None)

    def _update_bot(self, bot: SpazBot) -> bool:
        # Yup; that's a lot of return statements right there.
        # pylint: disable=too-many-return-statements

        if not bool(bot):
            return True

        assert bot.node

        # FIXME: Do this in a type safe way.
        r_walk_speed: float = getattr(bot, "r_walk_speed")
        r_walk_row: int = getattr(bot, "r_walk_row")

        speed = r_walk_speed
        pos = bot.node.position
        boxes = self.map.defs.boxes

        if ba.is_point_in_box(pos, boxes["b1"]):
            bot.node.move_up_down = speed
            bot.node.move_left_right = 0
            bot.node.run = 0.0
            return True

        # All bots settle for the third row.
        if ba.is_point_in_box(pos, boxes["b7"]):
            bot.node.move_up_down = speed
            bot.node.move_left_right = 0
            bot.node.run = 0.0
            return True
        if ba.is_point_in_box(pos, boxes["b2"]):
            bot.node.move_up_down = -speed
            bot.node.move_left_right = 0
            bot.node.run = 0.0
            return True
        if ba.is_point_in_box(pos, boxes["b3"]):
            bot.node.move_up_down = -speed
            bot.node.move_left_right = 0
            bot.node.run = 0.0
            return True
        if ba.is_point_in_box(pos, boxes["b6"]):
            bot.node.move_up_down = speed
            bot.node.move_left_right = 0
            bot.node.run = 0.0
            return True
        if (
            ba.is_point_in_box(pos, boxes["b8"])
            and not ba.is_point_in_box(pos, boxes["b9"])
        ) or pos == (0.0, 0.0, 0.0):

            # Default to walking right if we're still in the walking area.
            bot.node.move_left_right = speed
            bot.node.move_up_down = 0
            bot.node.run = 0.0
            return True

        # Revert to normal bot behavior otherwise..
        return False

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.PlayerScoredMessage):
            self._score += msg.score
            self._update_scores()

        elif isinstance(msg, ba.PlayerDiedMessage):
            # Augment standard behavior.
            super().handlemessage(msg)

            self._a_player_has_been_killed = True

            # Respawn them shortly.
            player = msg.getplayer(Player)
            assert self.initialplayerinfos is not None
            respawn_time = 2.0 + len(self.initialplayerinfos) * 1.0
            player.respawn_timer = ba.Timer(
                respawn_time, ba.Call(self.spawn_player_if_exists, player)
            )
            player.respawn_icon = RespawnIcon(player, respawn_time)

        elif isinstance(msg, SpazBotDiedMessage):
            if msg.how is ba.DeathType.REACHED_GOAL:
                return None
            pts, importance = msg.spazbot.get_death_points(msg.how)
            if msg.killerplayer is not None:
                target: Sequence[float] | None
                try:
                    assert msg.spazbot is not None
                    assert msg.spazbot.node
                    target = msg.spazbot.node.position
                except Exception:
                    ba.print_exception()
                    target = None
                try:
                    if msg.killerplayer:
                        self.stats.player_scored(
                            msg.killerplayer,
                            pts,
                            target=target,
                            kill=True,
                            screenmessage=False,
                            importance=importance,
                        )
                        ba.playsound(
                            (
                                self._dingsound
                                if importance == 1
                                else self._dingsoundhigh
                            ),
                            volume=0.6,
                        )
                except Exception:
                    ba.print_exception("Error on SpazBotDiedMessage.")

            # Normally we pull scores from the score-set, but if there's no
            # player lets be explicit.
            else:
                self._score += pts
            self._update_scores()

        else:
            return super().handlemessage(msg)
        return None
