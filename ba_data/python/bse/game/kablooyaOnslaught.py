"""Provides Onslaught Co-op game."""

# Yes this is a long one..
# pylint: disable=too-many-lines

# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from enum import Enum, unique
from dataclasses import dataclass
from typing import TYPE_CHECKING

from bastd.game.onslaught import OnslaughtGame

import ba
from bastd.actor.bomb import TNTSpawner
from bastd.actor.scoreboard import Scoreboard
from bastd.actor.spazbot import (
    SpazBotDiedMessage,
    SpazBotSet,
    ChargerBot,
    StickyBot,
    StickyBotPro,
    BomberBot,
    BrawlerBot,
    TriggerBot,
    TriggerBotPro,
    ExplodeyBot,
    ExplodeyBotShielded,
    BouncyBot,
    WaiterBot,
    WaiterBotPro,
    WaiterBotProShielded,
    FrostyBot,
    BrawlerBotProShielded,
    ChargerBotProShielded,
    BomberBotPro,
    TriggerBotProShielded,
    BrawlerBotPro,
    BomberBotProShielded,
    SantaBot,
    SantaBotPro,
    MicBot,
    MicBotPro,
    SplashBot,
    SoldatBot,
    NoirBot,
    MellyBot,
    ExplodeyBotNoTimeLimit,
    ToxicBot,
)

if TYPE_CHECKING:
    from typing import Any, Sequence
    from bastd.actor.spazbot import SpazBot


@dataclass
class Wave:
    """A wave of enemies."""

    entries: list[Spawn | Spacing | Delay | None]
    base_angle: float = 0.0


@dataclass
class Spawn:
    """A bot spawn event in a wave."""

    bottype: type[SpazBot] | str
    point: Point | None = None
    spacing: float = 5.0


@dataclass
class Spacing:
    """Empty space in a wave."""

    spacing: float = 5.0


@dataclass
class Delay:
    """A delay between events in a wave."""

    duration: float


class Preset(Enum):
    """Game presets we support."""

    ENDLESS = "endless"
    KABLOOYA = "kablooya"


@unique
class Point(Enum):
    """Points on the map we can spawn at."""

    LEFT_UPPER_MORE = "bot_spawn_left_upper_more"
    LEFT_UPPER = "bot_spawn_left_upper"
    TURRET_TOP_RIGHT = "bot_spawn_turret_top_right"
    RIGHT_UPPER = "bot_spawn_right_upper"
    TURRET_TOP_MIDDLE_LEFT = "bot_spawn_turret_top_middle_left"
    TURRET_TOP_MIDDLE_RIGHT = "bot_spawn_turret_top_middle_right"
    TURRET_TOP_LEFT = "bot_spawn_turret_top_left"
    TOP_RIGHT = "bot_spawn_top_right"
    TOP_LEFT = "bot_spawn_top_left"
    TOP = "bot_spawn_top"
    BOTTOM = "bot_spawn_bottom"
    LEFT = "bot_spawn_left"
    RIGHT = "bot_spawn_right"
    RIGHT_UPPER_MORE = "bot_spawn_right_upper_more"
    RIGHT_LOWER = "bot_spawn_right_lower"
    RIGHT_LOWER_MORE = "bot_spawn_right_lower_more"
    BOTTOM_RIGHT = "bot_spawn_bottom_right"
    BOTTOM_LEFT = "bot_spawn_bottom_left"
    TURRET_BOTTOM_RIGHT = "bot_spawn_turret_bottom_right"
    TURRET_BOTTOM_LEFT = "bot_spawn_turret_bottom_left"
    LEFT_LOWER = "bot_spawn_left_lower"
    LEFT_LOWER_MORE = "bot_spawn_left_lower_more"
    TURRET_TOP_MIDDLE = "bot_spawn_turret_top_middle"
    BOTTOM_HALF_RIGHT = "bot_spawn_bottom_half_right"
    BOTTOM_HALF_LEFT = "bot_spawn_bottom_half_left"
    TOP_HALF_RIGHT = "bot_spawn_top_half_right"
    TOP_HALF_LEFT = "bot_spawn_top_half_left"


class Player(ba.Player["Team"]):
    """Our player type for this game."""

    def __init__(self) -> None:
        self.has_been_hurt = False
        self.respawn_wave = 0


class Team(ba.Team[Player]):
    """Our team type for this game."""


class KablooyaOnslaughtGame(OnslaughtGame):
    """Co-op game where players try to survive attacking waves of enemies."""

    name = "Kablooya Onslaught"
    description = "Make it through!"

    tips: list[str | ba.GameTip] = [
        "insert useful tip here",
        "Try not to die. Very useful, huh?",
        "Use Flutter Bombs to send your enemies flying.",
        "Lite-Mines are a perfect way to keep more bots away from you.",
        "Steam Bombs are perfect for groups.",
        "Try to get group of bots near TNT - multikill guaranteed!",
    ]

    # Show messages when players die since it matters here.
    announce_player_deaths = True

    def __init__(self, settings: dict):

        self._preset = Preset(settings.get("preset", "kablooya"))
        if self._preset is Preset.KABLOOYA:
            settings["map"] = "Kablooya"
        elif self._preset is Preset.ENDLESS:
            settings["map"] = "Endless Kablooya"
        else:
            raise Exception("Put an eggroll with it.")

        ba.CoopGameActivity.__init__(self, settings)

        self._new_wave_sound = ba.getsound("scoreHit01")
        self._winsound = ba.getsound("score")
        self._cashregistersound = ba.getsound("cashRegister")
        self._a_player_has_been_hurt = False
        self._player_has_dropped_bomb = False

        # FIXME: should use standard map defs.
        self._spawn_center = (0, 3, -5)
        self._tntspawnpos = (0.0, 3.0, -5.0)
        self._powerup_center = (0, 5, -3.6)
        self._powerup_spread = (6.0, 4.0)
        self._scoreboard: Scoreboard | None = None
        self._game_over = False
        self._wavenum = 0
        self._can_end_wave = True
        self._score = 0
        self._time_bonus = 0
        self._spawn_info_text: ba.NodeActor | None = None
        self._dingsound = ba.getsound("dingSmall")
        self._dingsoundhigh = ba.getsound("dingSmallHigh")
        self._have_tnt = False
        self._excluded_powerups: list[str] | None = None
        self._waves: list[Wave] = []
        self._tntspawner: TNTSpawner | None = None
        self._bots: SpazBotSet | None = None
        self._powerup_drop_timer: ba.Timer | None = None
        self._time_bonus_timer: ba.Timer | None = None
        self._time_bonus_text: ba.NodeActor | None = None
        self._flawless_bonus: int | None = None
        self._wave_text: ba.NodeActor | None = None
        self._wave_update_timer: ba.Timer | None = None
        self._throw_off_kills = 0
        self._land_mine_kills = 0
        self._tnt_kills = 0

        if self._preset in [Preset.ENDLESS]:
            ba.getsession().max_players = 5

    def on_transition_in(self) -> None:
        super().on_transition_in()

        if self._preset is Preset.KABLOOYA:
            self.tips.append(
                "You really think you can beat it? Well. Maybe you can.."
            )
        self._spawn_info_text = ba.NodeActor(
            ba.newnode(
                "text",
                attrs={
                    "position": (15, -130),
                    "h_attach": "left",
                    "v_attach": "top",
                    "scale": 0.55,
                    "color": (0.3, 0.8, 0.3, 1.0),
                    "text": "",
                },
            )
        )
        ba.setmusic(ba.MusicType.KABLOOYA)

        self._scoreboard = Scoreboard(
            label=ba.Lstr(resource="scoreText"), score_split=0.5
        )

    def on_begin(self) -> None:
        ba.CoopGameActivity.on_begin(self)
        player_count = len(self.players)

        if self._preset in {Preset.KABLOOYA}:
            self._have_tnt = True
            self._waves = [
                Wave(
                    base_angle=-80,
                    entries=[
                        (
                            Spawn(ExplodeyBot, spacing=15)
                            if player_count > 3
                            else None
                        ),
                        Spawn(SoldatBot, spacing=37),
                        Spawn(SplashBot, spacing=80),
                        Spawn(BrawlerBot, spacing=100),
                        (
                            Spawn(NoirBot, spacing=110)
                            if self._preset is Preset.KABLOOYA
                            else None
                        ),
                        (
                            Spawn(BomberBot, spacing=6)
                            if player_count > 1
                            else None
                        ),
                        Spawn(SplashBot, spacing=7),
                        (
                            Spawn(BrawlerBotPro, spacing=35)
                            if player_count > 2
                            else None
                        ),
                    ],
                ),
                Wave(
                    base_angle=180,
                    entries=[
                        (
                            Spawn(BouncyBot, spacing=6)
                            if player_count > 3
                            else None
                        ),
                        (
                            Spawn(MicBot, spacing=6)
                            if self._preset is Preset.KABLOOYA
                            else None
                        ),
                        Spawn(MicBot, spacing=6),
                        Spawn(WaiterBot, spacing=45),
                        (
                            Spawn(ChargerBot, spacing=45)
                            if player_count > 1
                            else None
                        ),
                        Spawn(BrawlerBotPro, spacing=6),
                        (
                            Spawn(BrawlerBotPro, spacing=6)
                            if self._preset is Preset.KABLOOYA
                            else None
                        ),
                        (
                            Spawn(BrawlerBot, spacing=6)
                            if player_count > 2
                            else None
                        ),
                    ],
                ),
                Wave(
                    base_angle=0,
                    entries=[
                        Spawn(ChargerBotProShielded, spacing=30),
                        Spawn(TriggerBotPro, spacing=30),
                        Spawn(TriggerBotPro, spacing=30),
                        (
                            Spawn(TriggerBot, spacing=30)
                            if self._preset is Preset.KABLOOYA
                            else None
                        ),
                        (
                            Spawn(TriggerBot, spacing=30)
                            if player_count > 1
                            else None
                        ),
                        (
                            Spawn(TriggerBotPro, spacing=30)
                            if player_count > 3
                            else None
                        ),
                        Spawn(ChargerBotProShielded, spacing=30),
                    ],
                ),
                Wave(
                    base_angle=150,
                    entries=[
                        Spawn(StickyBotPro, spacing=70),
                        Spawn(WaiterBotPro, spacing=50),
                        (
                            Spawn(MellyBot, spacing=80)
                            if self._preset is Preset.KABLOOYA
                            else None
                        ),
                        Spawn(WaiterBotPro, spacing=70),
                        Spawn(StickyBotPro, spacing=50),
                        (
                            Spawn(MellyBot, spacing=120)
                            if player_count > 1
                            else None
                        ),
                        (
                            Spawn(MellyBot, spacing=70)
                            if player_count > 3
                            else None
                        ),
                        Spawn(StickyBotPro, spacing=80),
                        Spawn(WaiterBotPro, spacing=70),
                    ],
                ),
                Wave(
                    base_angle=0,
                    entries=[
                        Spawn(ChargerBot, spacing=72),
                        Spawn(BrawlerBotPro, spacing=72),
                        (
                            Spawn(SplashBot, spacing=72)
                            if self._preset is Preset.KABLOOYA
                            else None
                        ),
                        Spawn(SplashBot, spacing=72),
                        Spawn(SantaBot, spacing=72),
                        (
                            Spawn(NoirBot, spacing=36)
                            if player_count > 2
                            else None
                        ),
                    ],
                ),
                Wave(
                    base_angle=30,
                    entries=[
                        Spawn(BrawlerBotProShielded, spacing=50),
                        Spawn(BrawlerBotProShielded, spacing=50),
                        (
                            Spawn(BomberBotProShielded, spacing=50)
                            if self._preset is Preset.KABLOOYA
                            else None
                        ),
                        (
                            Spawn(BomberBotProShielded, spacing=50)
                            if player_count > 1
                            else None
                        ),
                        (
                            Spawn(BrawlerBotProShielded, spacing=50)
                            if player_count > 2
                            else None
                        ),
                    ],
                ),
                Wave(
                    base_angle=80,
                    entries=[
                        Spawn(BomberBotProShielded, spacing=50),
                        Spawn(StickyBotPro, spacing=50),
                        (
                            Spawn(BomberBotPro, spacing=50)
                            if self._preset is Preset.KABLOOYA
                            else None
                        ),
                        (
                            Spawn(BomberBotProShielded, spacing=50)
                            if player_count > 1
                            else None
                        ),
                        (
                            Spawn(StickyBotPro, spacing=50)
                            if player_count > 2
                            else None
                        ),
                    ],
                ),
                Wave(
                    base_angle=40,
                    entries=[
                        Spawn(BrawlerBotPro, spacing=50),
                        Spawn(MicBotPro, spacing=50),
                        (
                            Spawn(BomberBotPro, spacing=50)
                            if self._preset is Preset.KABLOOYA
                            else None
                        ),
                        (
                            Spawn(ChargerBotProShielded, spacing=50)
                            if player_count > 1
                            else None
                        ),
                        (
                            Spawn(ChargerBotProShielded, spacing=50)
                            if player_count > 2
                            else None
                        ),
                        Spawn(BrawlerBotProShielded, spacing=50),
                    ],
                ),
                Wave(
                    base_angle=130,
                    entries=[
                        Spawn(TriggerBot, spacing=50),
                        Spawn(TriggerBotProShielded, spacing=50),
                        (
                            Spawn(TriggerBot, spacing=50)
                            if self._preset is Preset.KABLOOYA
                            else None
                        ),
                        (
                            Spawn(TriggerBotProShielded, spacing=50)
                            if player_count > 1
                            else None
                        ),
                        (
                            Spawn(TriggerBot, spacing=50)
                            if player_count > 2
                            else None
                        ),
                        Spawn(TriggerBotProShielded, spacing=50),
                    ],
                ),
                Wave(
                    base_angle=170,
                    entries=[
                        Spawn(ChargerBotProShielded, spacing=50),
                        Spawn(TriggerBotProShielded, spacing=50),
                        (
                            Spawn(ChargerBotProShielded, spacing=50)
                            if self._preset is Preset.KABLOOYA
                            else None
                        ),
                        (
                            Spawn(TriggerBotProShielded, spacing=50)
                            if player_count > 1
                            else None
                        ),
                        (
                            Spawn(TriggerBotProShielded, spacing=50)
                            if player_count > 2
                            else None
                        ),
                        Spawn(ChargerBotProShielded, spacing=50),
                    ],
                ),
                Wave(
                    base_angle=15,
                    entries=[
                        Spawn(NoirBot, spacing=50),
                        Spawn(SoldatBot, spacing=50),
                        (
                            Spawn(SplashBot, spacing=50)
                            if self._preset is Preset.KABLOOYA
                            else None
                        ),
                        (
                            Spawn(SoldatBot, spacing=50)
                            if player_count > 1
                            else None
                        ),
                        (
                            Spawn(SplashBot, spacing=50)
                            if player_count > 2
                            else None
                        ),
                        Spawn(SoldatBot, spacing=50),
                        Spawn(SplashBot, spacing=50),
                    ],
                ),
                Wave(
                    base_angle=150,
                    entries=[
                        Spawn(SantaBotPro, spacing=50),
                        Spawn(WaiterBotProShielded, spacing=50),
                        (
                            Spawn(ChargerBotProShielded, spacing=50)
                            if self._preset is Preset.KABLOOYA
                            else None
                        ),
                        (
                            Spawn(TriggerBotProShielded, spacing=50)
                            if player_count > 1
                            else None
                        ),
                        (
                            Spawn(BomberBotProShielded, spacing=50)
                            if player_count > 2
                            else None
                        ),
                        Spawn(SantaBotPro, spacing=50),
                    ],
                ),
            ]

        # We generate these on the fly in endless.
        elif self._preset in {Preset.ENDLESS}:
            self._have_tnt = True
            self._excluded_powerups = []
            self._waves = []

        else:
            raise RuntimeError(f"Invalid preset: {self._preset}")

        # FIXME: Should migrate to use setup_standard_powerup_drops().
        # Spit out a few powerups and start dropping more shortly.
        self._drop_powerups(
            standard_points=True,
            poweruptype=(
                "shield" if self._preset in [Preset.KABLOOYA] else None
            ),
        )
        ba.timer(4.0, self._start_powerup_drops)

        # Our TNT spawner (if applicable).
        if self._have_tnt:
            self._tntspawner = TNTSpawner(position=self._tntspawnpos)

        self.setup_low_life_warning_sound()
        self._update_scores()
        self._bots = SpazBotSet()
        ba.timer(4.0, self._start_updating_waves)

    def _award_completion_achievements(self) -> None:
        return "unused"

    def _bot_levels_for_wave(self) -> list[list[type[SpazBot]]]:
        level = self._wavenum
        bot_types = [
            BomberBot,
            BrawlerBot,
            TriggerBot,
            ChargerBot,
            BomberBotPro,
            BrawlerBotPro,
            TriggerBotPro,
            BomberBotProShielded,
            BouncyBot,
            ChargerBotProShielded,
            StickyBot,
            StickyBotPro,
            WaiterBot,
            WaiterBotPro,
            WaiterBotProShielded,
            BrawlerBotProShielded,
            TriggerBotProShielded,
            MicBot,
            SantaBot,
            SplashBot,
            MellyBot,
            FrostyBot,
            SoldatBot,
        ]
        if level > 5:
            bot_types += [
                ExplodeyBot,
                WaiterBot,
                WaiterBotPro,
                TriggerBotProShielded,
                BrawlerBotProShielded,
                ChargerBotProShielded,
                SantaBot,
                MicBot,
                SplashBot,
                ToxicBot,
            ]
        if level > 7:
            bot_types += [
                ExplodeyBot,
                ExplodeyBotShielded,
                WaiterBotPro,
                TriggerBotProShielded,
                BrawlerBotProShielded,
                ChargerBotProShielded,
                StickyBotPro,
                MicBotPro,
                BomberBotProShielded,
            ]
        if level > 10:
            bot_types += [
                TriggerBotProShielded,
                WaiterBotProShielded,
                BouncyBot,
                FrostyBot,
                TriggerBotProShielded,
                TriggerBotProShielded,
                TriggerBotProShielded,
                SantaBotPro,
                MellyBot,
                SplashBot,
            ]
        if level > 13:
            bot_types += [
                TriggerBotProShielded,
                TriggerBotProShielded,
                TriggerBotProShielded,
                TriggerBotProShielded,
                StickyBotPro,
                StickyBotPro,
                ExplodeyBotNoTimeLimit,
            ]
        bot_levels = [
            [b for b in bot_types if b.points_mult == 1],
            [b for b in bot_types if b.points_mult == 2],
            [b for b in bot_types if b.points_mult == 3],
            [b for b in bot_types if b.points_mult == 4],
        ]

        # Make sure all lists have something in them
        if not all(bot_levels):
            raise RuntimeError("Got empty bot level")
        return bot_levels

    def _handle_kill_achievements(self, msg: SpazBotDiedMessage) -> None:
        return "unused"

    def end_game(self) -> None:
        super().end_game()
        ba.setmusic(ba.MusicType.DEFEAT_KABLOOYA)

    # There needs to be a bit of code redundancy if we don't want to break things...
    def _update_waves(self) -> None:
        assert self._bots is not None
        if (
            self._can_end_wave
            and not self._bots.have_living_bots()
            and not self._game_over
        ):
            self._can_end_wave = False
            self._time_bonus_timer = None
            self._time_bonus_text = None
            if self._preset in {Preset.ENDLESS}:
                won = False
            else:
                won = self._wavenum == len(self._waves)

            base_delay = 4.0 if won else 0.0

            # Reward time bonus.
            if self._time_bonus > 0:
                ba.timer(0, lambda: ba.playsound(self._cashregistersound))
                ba.timer(
                    base_delay,
                    ba.WeakCall(self._award_time_bonus, self._time_bonus),
                )
                base_delay += 1.0

            # Reward flawless bonus.
            if self._wavenum > 0:
                have_flawless = False
                for player in self.players:
                    if player.is_alive() and not player.has_been_hurt:
                        have_flawless = True
                        ba.timer(
                            base_delay,
                            ba.WeakCall(self._award_flawless_bonus, player),
                        )
                    player.has_been_hurt = False  # reset
                if have_flawless:
                    base_delay += 1.0

            if won:
                self.show_zoom_message(
                    ba.Lstr(resource="victoryText"), scale=1.0, duration=4.0
                )
                self.celebrate(20.0)
                self._award_completion_achievements()
                ba.timer(base_delay, ba.WeakCall(self._award_completion_bonus))
                base_delay += 0.85
                ba.playsound(self._winsound)
                ba.cameraflash()
                ba.setmusic(ba.MusicType.VICTORY)
                self._game_over = True

                # Can't just pass delay to do_end because our extra bonuses
                # haven't been added yet (once we call do_end the score
                # gets locked in).
                ba.timer(base_delay, ba.WeakCall(self.do_end, "victory"))
                return

            self._wavenum += 1

            # Short celebration after waves.
            if self._wavenum > 1:
                self.celebrate(0.5)
            ba.timer(base_delay, ba.WeakCall(self._start_next_wave))

    def _start_next_wave(self) -> None:
        if self._game_over:
            return

        self._respawn_players_for_wave()
        if self._preset in {Preset.ENDLESS}:
            wave = self._generate_random_wave()
        else:
            wave = self._waves[self._wavenum - 1]

        self._setup_wave_spawns(wave)
        self._update_wave_ui_and_bonuses()
        ba.timer(0.4, ba.Call(ba.playsound, self._new_wave_sound))

    def _update_endless_wave_text(self) -> None:
        wttxt = ba.Lstr(
            value="${A} ${B}",
            subs=[
                ("${A}", ba.Lstr(resource="waveText")),
                (
                    "${B}",
                    str(self._wavenum)
                    + (
                        ""
                        if self._preset in [Preset.ENDLESS]
                        else ("/" + str(len(self._waves)))
                    ),
                ),
            ],
        )
        self._wave_text.node.text = wttxt

    def _update_wave_ui_and_bonuses(self) -> None:
        super()._update_wave_ui_and_bonuses()
        self._update_endless_wave_text()


class EndlessKablooyaOnslaughtGame(KablooyaOnslaughtGame):
    name = "Endless Kablooya Onslaught"
    description = "Kablooya Onslaught, but endless!"
