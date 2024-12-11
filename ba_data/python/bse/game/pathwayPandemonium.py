"""Defines the runaround co-op game."""

# We wear the cone of shame.
# pylint: disable=too-many-lines

# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

import ba
from bastd.actor.popuptext import PopupText
from bastd.actor.bomb import TNTSpawner
from bastd.actor.scoreboard import Scoreboard
from bastd.actor.respawnicon import RespawnIcon
from bastd.actor.powerupbox import PowerupBox, PowerupBoxFactory
from bastd.gameutils import SharedObjects
from bastd.actor.spazbot import (
    SpazBotSet,
    SpazBot,
    SpazBotDiedMessage,
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

from explodinary.lib.text import show_bottom_zoom_message

if TYPE_CHECKING:
    from typing import Any, Sequence


class Preset(Enum):
    """Play presets."""

    ENDLESS = "endless"
    ENDLESS_TOURNAMENT = "endless_tournament"
    PRO = "pro"
    PRO_EASY = "pro_easy"
    UBER = "uber"
    UBER_EASY = "uber_easy"
    TOURNAMENT = "tournament"
    TOURNAMENT_UBER = "tournament_uber"


class Point(Enum):
    """Where we can spawn stuff and the corresponding map attr name."""

    BOTTOM_LEFT = "bot_spawn_bottom_left"
    BOTTOM_RIGHT = "bot_spawn_bottom_right"
    START = "bot_spawn_start"


@dataclass
class Spawn:
    """Defines a bot spawn event."""

    # noinspection PyUnresolvedReferences
    type: type[SpazBot]
    path: int = 0
    point: Point | None = None


@dataclass
class Spacing:
    """Defines spacing between spawns."""

    duration: float


@dataclass
class Wave:
    """Defines a wave of enemies."""

    entries: list[Spawn | Spacing | None]


class Player(ba.Player["Team"]):
    """Our player type for this game."""

    def __init__(self) -> None:
        self.respawn_timer: ba.Timer | None = None
        self.respawn_icon: RespawnIcon | None = None


class Team(ba.Team[Player]):
    """Our team type for this game."""


class PathwayPandemoniumGame(ba.CoopGameActivity[Player, Team]):
    """Game involving trying to bomb bots as they walk through the map."""

    name = "Pathway Pandemonium"
    description = "How many days do you think you'll last?"
    tips = [
        "Jump just as you're throwing to get bombs up to the highest levels.",
        "No, you can't get up on the ledge. You have to throw bombs.",
        "Whip back and forth to get more distance on your throws..",
    ]
    default_music = ba.MusicType.RESTYE

    # How fast our various bot types walk.
    _bot_speed_map: dict[type[SpazBot], float] = {
        BomberBot: 0.58,
        BomberBotPro: 0.58,
        BomberBotProShielded: 0.58,
        BrawlerBot: 0.67,
        BrawlerBotPro: 0.67,
        BrawlerBotProShielded: 0.67,
        TriggerBot: 0.83,
        TriggerBotPro: 0.88,
        TriggerBotProShielded: 0.88,
        ChargerBot: 0.88,
        ChargerBotProShielded: 1,
        ExplodeyBot: 1.1,
        StickyBot: 0.6,
        SplashBot: 0.8,
        WaiterBot: 0.7,
        SoldatBot: 0.55,
        FrostyBot: 0.75,
        MicBot: 0.45,
        MellyBot: 0.6,
        ToxicBot: 0.75,
        NoirBot: 0.65,
        ExplodeyBotNoTimeLimit: 0.8,
    }

    def __init__(self, settings: dict):
        settings["map"] = "Pathway Pandemonium"
        super().__init__(settings)
        shared = SharedObjects.get()
        self._preset = Preset(settings.get("preset", "pro"))

        self._player_death_sound = ba.getsound("playerDeath")
        self._special_point = ba.getsound("specialPoint")
        self._special_point2 = ba.getsound("specialPoint2")
        self._special_point3 = ba.getsound("specialPoint3")
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
        self._daynum = 1
        self._can_end_wave = True
        self._score = 0
        self._time_bonus = 0
        self._score_region: ba.Actor | None = None
        self._dingsound = ba.getsound("dingSmall")
        self._dingsoundhigh = ba.getsound("dingSmallHigh")
        self._exclude_powerups: list[str] | None = None
        self._have_tnt: bool | None = None
        self._waves: list[Wave] | None = None
        self._bots = SpazBotSet()
        self._tntspawner: TNTSpawner | None = None
        self._tntspawner2: TNTSpawner | None = None
        self._lives_bg: ba.NodeActor | None = None
        self._lives_hbtime: ba.Timer | None = None
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

        ba.getsession().max_players = 5  # Tada

    def on_transition_in(self) -> None:
        super().on_transition_in()

        self._scoreboard = Scoreboard(
            label=ba.Lstr(resource="scoreText"), score_split=0.5
        )
        self._score_region = ba.NodeActor(
            ba.newnode(
                "region",
                attrs={
                    "position": self.map.defs.boxes["score_region"][0:3],
                    "scale": self.map.defs.boxes["score_region"][6:9],
                    "type": "box",
                    "materials": [self._score_region_material],
                },
            )
        )

    def _day_update(self) -> None:
        self._daynum += 1

        if self._daynum == 2:
            ba.setmusic(ba.MusicType.RESTYE2)
        elif self._daynum == 3:
            ba.setmusic(ba.MusicType.RESTYE3)
        elif self._daynum == 4:
            ba.setmusic(ba.MusicType.RESTYE4)

        ba.timer(0.4, ba.Call(ba.playsound, self._new_wave_sound))
        textval = ba.Lstr(
            value="${A} ${B}",
            subs=[
                ("${A}", ba.Lstr(resource="explodinary.dayText")),
                ("${B}", str(self._daynum)),
            ],
        )
        self._day_text.node.text = textval
        show_bottom_zoom_message(
            ba.Lstr(
                value="${A} ${B}",
                subs=[
                    ("${A}", ba.Lstr(resource="explodinary.dayText")),
                    ("${B}", str(self._daynum)),
                ],
            ),
            scale=0.7,
            color=(0.2, 0.7, 1),
            duration=1.0,
            trail=True,
        )

    def on_begin(self) -> None:
        super().on_begin()
        player_count = len(self.players)

        self._day_timer = ba.Timer(
            200, self._day_update, repeat=True, suppress_format_warning=True
        )
        textval = ba.Lstr(
            value="${A} ${B}",
            subs=[
                ("${A}", ba.Lstr(resource="explodinary.dayText")),
                ("${B}", str(self._daynum)),
            ],
        )
        self._day_text = ba.NodeActor(
            ba.newnode(
                "text",
                attrs={
                    "v_attach": "top",
                    "h_attach": "center",
                    "h_align": "center",
                    "vr_depth": -10,
                    "color": (1, 1, 1, 1),
                    "shadow": 1.0,
                    "flatness": 1.0,
                    "position": (0, -40),
                    "scale": 1.3,
                    "text": textval,
                },
            )
        )
        ba.animate(self._day_text.node, "opacity", {3: 0, 7.0: 1.0})

        if self._preset in {Preset.ENDLESS, Preset.ENDLESS_TOURNAMENT}:
            self._exclude_powerups = []
            self._have_tnt = True

        # Spit out a few powerups and start dropping more shortly.
        self._drop_powerups(standard_points=True)
        ba.timer(4.0, self._start_powerup_drops)
        self.setup_low_life_warning_sound()
        self._update_scores()

        # Our TNT spawner (if applicable).
        if self._have_tnt:
            self._tntspawner = TNTSpawner(position=self._tntspawnpos)
            self._tntspawner2 = TNTSpawner(position=self._tntspawnpos2)

        # Make sure to stay out of the way of menu/party buttons in the corner.
        uiscale = ba.app.ui.uiscale
        l_offs = (
            -80
            if uiscale is ba.UIScale.SMALL
            else -40 if uiscale is ba.UIScale.MEDIUM else 0
        )

        self._lives_bg = ba.NodeActor(
            ba.newnode(
                "image",
                attrs={
                    "texture": self._heart_tex,
                    "model_opaque": self._heart_model_opaque,
                    "model_transparent": self._heart_model_transparent,
                    "attach": "topRight",
                    "scale": (90, 90),
                    "position": (-110 + l_offs, -50),
                    "color": (0.3, 0.5, 0.8),
                },
            )
        )
        # FIXME; should not set things based on vr mode.
        #  (won't look right to non-vr connected clients, etc)
        vrmode = ba.app.vr_mode
        self._lives_text = ba.NodeActor(
            ba.newnode(
                "text",
                attrs={
                    "v_attach": "top",
                    "h_attach": "right",
                    "h_align": "center",
                    "color": (1, 1, 1, 1) if vrmode else (0.8, 0.8, 0.8, 1.0),
                    "flatness": 1.0 if vrmode else 0.5,
                    "shadow": 1.0 if vrmode else 0.5,
                    "vr_depth": 10,
                    "position": (-113 + l_offs, -69),
                    "scale": 1.3,
                    "text": str(self._lives),
                },
            )
        )

        ba.timer(2.0, self._start_updating_waves)

    def _handle_reached_end(self) -> None:
        spaz = ba.getcollision().opposingnode.getdelegate(SpazBot, True)
        if not spaz.is_alive():
            return  # Ignore bodies flying in.

        self._flawless = False
        pos = spaz.node.position
        ba.playsound(self._bad_guy_score_sound, position=pos)
        light = ba.newnode(
            "light", attrs={"position": pos, "radius": 0.5, "color": (1, 0, 0)}
        )
        ba.animate(light, "intensity", {0.0: 0, 0.1: 1, 0.5: 0}, loop=False)
        ba.timer(1.0, light.delete)
        spaz.handlemessage(
            ba.DieMessage(immediate=True, how=ba.DeathType.REACHED_GOAL)
        )

        if self._lives > 0:
            self._lives -= 1
            if self._lives == 0:
                self._bots.stop_moving()
                self.continue_or_end_game()
            # Heartbeat behavior
            if self._lives < 4:
                hbtime = 0.39 + (0.21 * self._lives)
                self._lives_hbtime = ba.Timer(
                    hbtime, lambda: self.heart_dyin(True, hbtime), repeat=True
                )
                self.heart_dyin(True)
            else:
                self._lives_hbtime = None
                self.heart_dyin(False)

            assert self._lives_text is not None
            assert self._lives_text.node
            self._lives_text.node.text = str(self._lives)
            delay = 0.0

            def _safesetattr(node: ba.Node, attr: str, value: Any) -> None:
                if node:
                    setattr(node, attr, value)

            for _i in range(4):
                ba.timer(
                    delay,
                    ba.Call(
                        _safesetattr,
                        self._lives_text.node,
                        "color",
                        (1, 0, 0, 1.0),
                    ),
                )
                assert self._lives_bg is not None
                assert self._lives_bg.node
                ba.timer(
                    delay,
                    ba.Call(_safesetattr, self._lives_bg.node, "opacity", 0.5),
                )
                delay += 0.125
                ba.timer(
                    delay,
                    ba.Call(
                        _safesetattr,
                        self._lives_text.node,
                        "color",
                        (1.0, 1.0, 0.0, 1.0),
                    ),
                )
                ba.timer(
                    delay,
                    ba.Call(_safesetattr, self._lives_bg.node, "opacity", 1.0),
                )
                delay += 0.125
            ba.timer(
                delay,
                ba.Call(
                    _safesetattr,
                    self._lives_text.node,
                    "color",
                    (0.8, 0.8, 0.8, 1.0),
                ),
            )

    def on_continue(self) -> None:
        self._lives = 3
        assert self._lives_text is not None
        assert self._lives_text.node
        self._lives_text.node.text = str(self._lives)
        self._bots.start_moving()

    def spawn_player(self, player: Player) -> ba.Actor:
        pos = (
            self._spawn_center[0] + random.uniform(-1.5, 1.5),
            self._spawn_center[1],
            self._spawn_center[2] + random.uniform(-1.5, 1.5),
        )
        spaz = self.spawn_player_spaz(player, position=pos)

        # Add the material that causes us to hit the player-wall.
        spaz.pick_up_powerup_callback = self._on_player_picked_up_powerup
        return spaz

    def _on_player_picked_up_powerup(self, player: ba.Actor) -> None:
        del player  # Unused.
        self._player_has_picked_up_powerup = True

    def _drop_powerup(self, index: int, poweruptype: str | None = None) -> None:
        if poweruptype is None:
            poweruptype = PowerupBoxFactory.get().get_random_powerup_type(
                excludetypes=self._exclude_powerups
            )
        PowerupBox(
            position=self.map.powerup_spawn_points[index],
            poweruptype=poweruptype,
        ).autoretain()

    def _start_powerup_drops(self) -> None:
        ba.timer(3.0, self._drop_powerups, repeat=True)

    def _drop_powerups(
        self, standard_points: bool = False, force_first: str | None = None
    ) -> None:
        """Generic powerup drop."""

        # If its been a minute since our last wave finished emerging, stop
        # giving out land-mine powerups. (prevents players from waiting
        # around for them on purpose and filling the map up)
        if ba.time() - self._last_wave_end_time > 60.0:
            extra_excludes = ["land_mines", "lite_mines", "flutter_mines"]
        else:
            extra_excludes = []

        if standard_points:
            points = self.map.powerup_spawn_points
            for i in range(len(points)):
                ba.timer(
                    1.0 + i * 0.5,
                    ba.Call(
                        self._drop_powerup, i, force_first if i == 0 else None
                    ),
                )
        else:
            pos = (
                self._powerup_center[0]
                + random.uniform(
                    -1.0 * self._powerup_spread[0],
                    1.0 * self._powerup_spread[0],
                ),
                self._powerup_center[1],
                self._powerup_center[2]
                + random.uniform(
                    -self._powerup_spread[1], self._powerup_spread[1]
                ),
            )

            # drop one random one somewhere..
            assert self._exclude_powerups is not None
            PowerupBox(
                position=pos,
                poweruptype=PowerupBoxFactory.get().get_random_powerup_type(
                    excludetypes=self._exclude_powerups + extra_excludes
                ),
            ).autoretain()

    def end_game(self) -> None:
        ba.pushcall(ba.Call(self.do_end, "defeat"))
        ba.setmusic(ba.MusicType.RESTYEDEFEAT)
        ba.playsound(self._player_death_sound)
        assert self._bots is not None
        self._bots.final_celebrate()

    def do_end(self, outcome: str) -> None:
        """End the game now with the provided outcome."""

        if outcome == "defeat":
            delay = 2.0
            self.fade_to_red()
        else:
            delay = 0

        score: int | None
        if self._wavenum >= 2:
            score = self._score
            fail_message = None
        else:
            score = None
            fail_message = ba.Lstr(resource="reachWave2Text")

        self.end(
            delay=delay,
            results={
                "outcome": outcome,
                "score": score,
                "fail_message": fail_message,
                "playerinfos": self.initialplayerinfos,
            },
        )

    def _update_waves(self) -> None:
        # pylint: disable=too-many-branches

        # If we have no living bots, go to the next wave.
        if (
            self._can_end_wave
            and not self._bots.have_living_bots()
            and not self._game_over
            and self._lives > 0
        ):

            self._can_end_wave = False
            self._time_bonus_timer = None
            self._time_bonus_text = None

            if self._preset in {Preset.ENDLESS, Preset.ENDLESS_TOURNAMENT}:
                won = False
            else:
                assert self._waves is not None
                won = self._wavenum == len(self._waves)

            base_delay = 4.0 if won else 0

            # Reward flawless bonus.
            if self._wavenum > 0 and self._flawless:
                ba.timer(base_delay, self._award_flawless_bonus)
                base_delay += 1.0

            self._flawless = True  # reset

            if won:

                self.celebrate(10.0)
                ba.timer(base_delay, self._award_lives_bonus)
                base_delay += 1.0
                ba.timer(base_delay, self._award_completion_bonus)
                base_delay += 0.85
                ba.playsound(self._winsound)
                ba.cameraflash()
                ba.setmusic(ba.MusicType.VICTORY)
                self._game_over = True
                ba.timer(base_delay, ba.Call(self.do_end, "victory"))
                return

            self._wavenum += 1

            ba.timer(0, self._start_next_wave)

    def _award_completion_bonus(self) -> None:
        bonus = 200
        ba.playsound(self._cashregistersound)
        PopupText(
            ba.Lstr(
                value="+${A} ${B}",
                subs=[
                    ("${A}", str(bonus)),
                    ("${B}", ba.Lstr(resource="completionBonusText")),
                ],
            ),
            color=(0.7, 0.7, 1.0, 1),
            scale=1.6,
            position=(0, 1.5, -1),
        ).autoretain()
        self._score += bonus
        self._update_scores()

    def _award_lives_bonus(self) -> None:
        bonus = self._lives * 30
        self._score += bonus
        self._update_scores()

    def _award_flawless_bonus(self) -> None:
        assert self._flawless_bonus is not None
        self._score += self._flawless_bonus
        self._update_scores()

    def _start_time_bonus_timer(self) -> None:
        self._time_bonus_timer = ba.Timer(
            1.0, self._update_time_bonus, repeat=True
        )

    def _start_next_wave(self) -> None:
        # FIXME: Need to split this up.
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        t_sec = 0.0
        base_delay = 0.5
        delay = 0.0
        bot_types: list[Spawn | Spacing | None] = []
        level = self._daynum

        if self._preset in {Preset.ENDLESS, Preset.ENDLESS_TOURNAMENT}:
            level = self._daynum
            wave = self._wavenum
            target_points = (level + 1) * 8.0
            group_count = random.randint(1, 3)
            entries: list[Spawn | Spacing | None] = []
            spaz_types: list[tuple[type[SpazBot], float]] = []
            if level == 1:
                spaz_types += [(BomberBot, 4.0)]
                spaz_types += [(SoldatBot, 4.0)]
                spaz_types += [(TriggerBot, 6.0)]
                spaz_types += [(ChargerBot, 6.0)]
            if level == 2:
                spaz_types += [(TriggerBotPro, 7.5)]
                spaz_types += [(BomberBotProShielded, 5.0)]
            if level > 2:
                spaz_types += [(ChargerBotProShielded, 5.0)]
                spaz_types += [(TriggerBotProShielded, 7.5)]
            # Bot type, their effect on target points.
            defender_types: list[tuple[type[SpazBot], float]] = [
                (BomberBot, 0.9),
                (TriggerBot, 1),
                (SoldatBot, 0.7),
                (NoirBot, 0.9),
                (ChargerBot, 0.9),
            ]
            if wave >= 4:
                defender_types += [(BomberBot, 0.9)]
                defender_types += [(NoirBot, 0.9)]
                defender_types += [(ChargerBot, 0.9)]
                defender_types += [(TriggerBot, 1)]
            if wave >= 14:
                defender_types += [(StickyBot, 0.7)]
                defender_types += [(WaiterBot, 0.7)]
                defender_types += [(FrostyBot, 1.5)]
                defender_types += [(SplashBot, 0.7)]
                defender_types += [(MicBot, 0.7)]
                defender_types += [(ExplodeyBotNoTimeLimit, 0.7)]
            if wave >= 25:
                defender_types += [(ExplodeyBot, 0.7)]
                defender_types += [(ToxicBot, 0.7)]
            if wave >= 35:
                defender_types += [(ChargerBotProShielded, 0.7)] * (
                    1 + (level - 6) // 3
                )
                defender_types += [(BomberBotProShielded, 0.7)] * (
                    1 + (level - 6) // 3
                )
                defender_types += [(TriggerBotProShielded, 0.7)] * (
                    1 + (level - 6) // 3
                )
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
                    or (group == 1 and level == 1)
                    or (group == 2 and level > 1)
                ):
                    if random.random() < min(0.75, (wave - 4) * 0.11):
                        this_target_point_s, defender1 = _add_defender(
                            defender_type1, Point.BOTTOM_LEFT
                        )
                    if random.random() < min(0.75, (wave - 4) * 0.04):
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

        ba.timer(t_sec, self._start_time_bonus_timer)

        # Keep track of when this wave finishes emerging. We wanna stop
        # dropping land-mines powerups at some point (otherwise a crafty
        # player could fill the whole map with them)
        self._last_wave_end_time = ba.time() + t_sec
        totalwaves = str(len(self._waves)) if self._waves is not None else "??"

    def _on_bot_spawn(self, path: int, spaz: SpazBot) -> None:

        # Add our custom update callback and set some info for this bot.
        spaz_type = type(spaz)
        assert spaz is not None
        spaz.update_callback = self._update_bot

        # Tack some custom attrs onto the spaz.
        setattr(spaz, "r_walk_row", path)
        setattr(spaz, "r_walk_speed", self._get_bot_speed(spaz_type))

    def add_bot_at_point(
        self,
        point: Point,
        spaztype: type[SpazBot],
        path: int,
        spawn_time: float = 0.1,
    ) -> None:
        """Add the given type bot with the given delay (in seconds)."""

        # Don't add if the game has ended.
        if self._game_over:
            return
        pos = self.map.defs.points[point.value][:3]
        self._bots.spawn_bot(
            spaztype,
            pos=pos,
            spawn_time=spawn_time,
            on_spawn_call=ba.Call(self._on_bot_spawn, path),
        )

    def _update_time_bonus(self) -> None:
        self._time_bonus = int(self._time_bonus * 0.91)
        if self._time_bonus > 0 and self._time_bonus_text is not None:
            assert self._time_bonus_text.node
            assert self._time_bonus_mult
            self._time_bonus_text.node.text = ba.Lstr(
                value="${A}: ${B}",
                subs=[
                    ("${A}", ba.Lstr(resource="timeBonusText")),
                    (
                        "${B}",
                        str(int(self._time_bonus * self._time_bonus_mult)),
                    ),
                ],
            )
        else:
            self._time_bonus_text = None

    def _start_updating_waves(self) -> None:
        self._wave_update_timer = ba.Timer(2.0, self._update_waves, repeat=True)

    def _update_scores(self) -> None:
        score = self._score

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

        # Bots in row 1 attempt the high road..
        if ba.is_point_in_box(pos, boxes["b4"]):
            bot.node.move_up_down = speed
            bot.node.move_left_right = 0
            bot.node.run = 0.0
            return True

        # Row 1 and 2 bots attempt the middle road..
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
        if ba.is_point_in_box(pos, boxes["b5"]):
            bot.node.move_up_down = -speed
            bot.node.move_left_right = 0
            bot.node.run = 0.0
            return True
        if (
            ba.is_point_in_box(pos, boxes["b8"])
            and not ba.is_point_in_box(pos, boxes["b9"])
            and not ba.is_point_in_box(pos, boxes["b10"])
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
            respawn_time = 3.0 + len(self.initialplayerinfos) * 1.0
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

    def _get_bot_speed(self, bot_type: type[SpazBot]) -> float:
        speed = self._bot_speed_map.get(bot_type)
        level = self._daynum
        if level == 2:
            speed += 0.5

        if level == 3:
            speed += 0.3

        if level == 4:
            speed += 0.3

        if level == 5:
            speed += 0.2

        if speed is None:
            raise TypeError(
                "Invalid bot type to _get_bot_speed(): " + str(bot_type)
            )
        return speed

    def _set_can_end_wave(self) -> None:
        self._can_end_wave = True

    def heart_dyin(self, status: bool, time: float = 1.22) -> None:
        """Makes the UI heart beat at low health."""
        if not (self._lives_bg or self._lives_bg.node.exists()):
            return

        heart = self._lives_bg.node

        # Make the heart beat intensely!
        if status:
            ba.animate_array(
                heart,
                "scale",
                2,
                {
                    0: (90, 90),
                    time * 0.1: (105, 105),
                    time * 0.21: (88, 88),
                    time * 0.42: (90, 90),
                    time * 0.52: (105, 105),
                    time * 0.63: (88, 88),
                    time: (90, 90),
                },
            )

        # Neutralize heartbeat (Done did when dead.)
        else:
            ba.animate_array(
                heart,
                "scale",
                2,
                {
                    0: heart.scale,
                    time: (90, 90),
                },
            )
