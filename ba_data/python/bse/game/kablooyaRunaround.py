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
    StickyBotPro,
    ToxicBot,
)

from bastd.game.runaround import RunaroundGame

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


class KablooyaRunaroundGame(RunaroundGame):
    """Game involving trying to bomb bots as they walk through the map."""

    name = "Kablooya Runaround"
    description = (
        "Prevent enemies from reaching the exit. And don't die. Really."
    )
    tips = [
        "See this green heart? When you die, it goes down. When it reaches zero... game over.",
    ]
    default_music = ba.MusicType.MARCHING

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
        ChargerBot: 1.0,
        ChargerBotProShielded: 1.0,
        ExplodeyBot: 1.0,
        StickyBot: 0.5,
        StickyBotPro: 0.5,
        SplashBot: 0.7,
        WaiterBot: 0.6,
        SoldatBot: 0.45,
        FrostyBot: 0.65,
        MicBot: 0.35,
        MellyBot: 0.5,
        ToxicBot: 0.65,
        NoirBot: 0.55,
        ExplodeyBotNoTimeLimit: 0.7,
    }

    def __init__(self, settings: dict):
        self._preset = Preset(settings.get("preset", "uber"))
        if self._preset is Preset.UBER:
            settings["map"] = "Tower S"
        elif self._preset is Preset.ENDLESS:
            settings["map"] = "Endless Tower S"
        else:
            raise Exception("Put an eggroll with it.")
        ba.CoopGameActivity.__init__(self, settings)
        shared = SharedObjects.get()

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
        self._waves: list[Wave] | None = None
        self._bots = SpazBotSet()
        self._tntspawner: TNTSpawner | None = None
        self._lives_bg: ba.NodeActor | None = None
        self._death_lives_bg: ba.NodeActor | None = None
        self._start_lives = 10
        self._death_start_lives = 5 if self._preset is Preset.UBER else 8
        self._death_start_lives2 = 10 if self._preset is Preset.UBER else 14
        self._death_start_lives3 = 12 if self._preset is Preset.UBER else 18
        self._death_start_lives4 = 16 if self._preset is Preset.UBER else 20
        self._lives = self._start_lives
        self._death_lives = self._death_start_lives
        self._lives_text: ba.NodeActor | None = None
        self._death_lives_text: ba.NodeActor | None = None
        self._flawless = True
        self._time_bonus_timer: ba.Timer | None = None
        self._time_bonus_text: ba.NodeActor | None = None
        self._time_bonus_mult: float | None = None
        self._wave_text: ba.NodeActor | None = None
        self._flawless_bonus: int | None = None
        self._wave_update_timer: ba.Timer | None = None

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

    def on_begin(self) -> None:
        ba.CoopGameActivity.on_begin(self)
        player_count = len(self.players)
        hard = self._preset not in {Preset.PRO_EASY, Preset.UBER_EASY}

        if player_count == 1:
            self._death_lives = self._death_start_lives
        elif player_count == 2:
            self._death_lives = self._death_start_lives2
        elif player_count == 3:
            self._death_lives = self._death_start_lives3
        elif player_count == 4:
            self._death_lives = self._death_start_lives4

            self._exclude_powerups = ["curse"]
            self._have_tnt = True
            self._waves = [
                Wave(
                    entries=[
                        Spawn(BomberBot, path=3 if hard else 2),
                        Spawn(BomberBot, path=2),
                        Spawn(BomberBot, path=2) if hard else None,
                        Spawn(BomberBot, path=2) if player_count > 1 else None,
                        Spawn(BomberBot, path=1) if hard else None,
                        Spawn(BomberBot, path=1) if player_count > 2 else None,
                        Spawn(BomberBot, path=1) if player_count > 3 else None,
                    ]
                ),
                Wave(
                    entries=[
                        Spawn(BomberBot, path=1) if hard else None,
                        Spawn(BomberBot, path=2) if hard else None,
                        Spawn(BomberBot, path=2),
                        Spawn(BomberBot, path=2),
                        Spawn(BomberBot, path=2) if player_count > 3 else None,
                        Spawn(BrawlerBot, path=3),
                        Spawn(BrawlerBot, path=3),
                        Spawn(BrawlerBot, path=3) if hard else None,
                        Spawn(BrawlerBot, path=3) if player_count > 1 else None,
                        Spawn(BrawlerBot, path=3) if player_count > 2 else None,
                    ]
                ),
                Wave(
                    entries=[
                        Spawn(ChargerBot, path=2) if hard else None,
                        Spawn(ChargerBot, path=2) if player_count > 2 else None,
                        Spawn(TriggerBot, path=2),
                        Spawn(TriggerBot, path=2) if player_count > 1 else None,
                        Spacing(duration=3.0),
                        Spawn(BomberBot, path=2) if hard else None,
                        Spawn(BomberBot, path=2) if hard else None,
                        Spawn(BomberBot, path=2),
                        Spawn(BomberBot, path=3) if hard else None,
                        Spawn(BomberBot, path=3),
                        Spawn(BomberBot, path=3),
                        Spawn(BomberBot, path=3) if player_count > 3 else None,
                    ]
                ),
                Wave(
                    entries=[
                        Spawn(TriggerBot, path=1) if hard else None,
                        Spacing(duration=1.0) if hard else None,
                        Spawn(TriggerBot, path=2),
                        Spacing(duration=1.0),
                        Spawn(TriggerBot, path=3),
                        Spacing(duration=1.0),
                        Spawn(TriggerBot, path=1) if hard else None,
                        Spacing(duration=1.0) if hard else None,
                        Spawn(TriggerBot, path=2),
                        Spacing(duration=1.0),
                        Spawn(TriggerBot, path=3),
                        Spacing(duration=1.0),
                        (
                            Spawn(TriggerBot, path=1)
                            if (player_count > 1 and hard)
                            else None
                        ),
                        Spacing(duration=1.0),
                        Spawn(TriggerBot, path=2) if player_count > 2 else None,
                        Spacing(duration=1.0),
                        Spawn(TriggerBot, path=3) if player_count > 3 else None,
                        Spacing(duration=1.0),
                    ]
                ),
                Wave(
                    entries=[
                        Spawn(
                            ChargerBotProShielded if hard else ChargerBot,
                            path=1,
                        ),
                        Spawn(BrawlerBot, path=2) if hard else None,
                        Spawn(BrawlerBot, path=2),
                        Spawn(BrawlerBot, path=2),
                        Spawn(BrawlerBot, path=3) if hard else None,
                        Spawn(BrawlerBot, path=3),
                        Spawn(BrawlerBot, path=3),
                        Spawn(BrawlerBot, path=3) if player_count > 1 else None,
                        Spawn(BrawlerBot, path=3) if player_count > 2 else None,
                        Spawn(BrawlerBot, path=3) if player_count > 3 else None,
                    ]
                ),
                Wave(
                    entries=[
                        Spawn(BomberBotProShielded, path=3),
                        Spacing(duration=1.5),
                        Spawn(BomberBotProShielded, path=2),
                        Spacing(duration=1.5),
                        Spawn(BomberBotProShielded, path=1) if hard else None,
                        Spacing(duration=1.0) if hard else None,
                        Spawn(BomberBotProShielded, path=3),
                        Spacing(duration=1.5),
                        Spawn(BomberBotProShielded, path=2),
                        Spacing(duration=1.5),
                        Spawn(BomberBotProShielded, path=1) if hard else None,
                        Spacing(duration=1.5) if hard else None,
                        (
                            Spawn(BomberBotProShielded, path=3)
                            if player_count > 1
                            else None
                        ),
                        Spacing(duration=1.5),
                        (
                            Spawn(BomberBotProShielded, path=2)
                            if player_count > 2
                            else None
                        ),
                        Spacing(duration=1.5),
                        (
                            Spawn(BomberBotProShielded, path=1)
                            if player_count > 3
                            else None
                        ),
                    ]
                ),
            ]
            # KABLOOYA PRESET
        if self._preset in {
            Preset.UBER_EASY,
            Preset.UBER,
            Preset.TOURNAMENT_UBER,
        }:
            self._exclude_powerups = []
            self._have_tnt = True
            self._waves = [
                Wave(
                    entries=[
                        Spawn(NoirBot, path=1) if hard else None,
                        Spawn(TriggerBot, path=2),
                        Spawn(TriggerBot, path=2),
                        Spawn(StickyBotPro, path=3),
                        Spawn(
                            BrawlerBotPro if hard else BrawlerBot,
                            point=Point.BOTTOM_LEFT,
                        ),
                        (
                            Spawn(
                                ExplodeyBotNoTimeLimit, point=Point.BOTTOM_RIGHT
                            )
                            if player_count > 2
                            else None
                        ),
                    ]
                ),
                Wave(
                    entries=[
                        Spawn(ChargerBot, path=2),
                        Spawn(ChargerBot, path=3),
                        Spawn(ChargerBot, path=1) if hard else None,
                        Spawn(ChargerBot, path=2),
                        Spawn(ChargerBot, path=3),
                        Spawn(ChargerBot, path=1) if player_count > 2 else None,
                    ]
                ),
                Wave(
                    entries=[
                        Spawn(BomberBotPro, path=1) if hard else None,
                        Spawn(BomberBotPro, path=2),
                        Spawn(BomberBotPro, path=2),
                        Spawn(BomberBotPro, path=3),
                        Spawn(BomberBotPro, path=3),
                        Spawn(StickyBot, point=Point.BOTTOM_RIGHT),
                        (
                            Spawn(
                                BrawlerBotProShielded, point=Point.BOTTOM_LEFT
                            )
                            if player_count > 2
                            else None
                        ),
                    ]
                ),
                Wave(
                    entries=[
                        Spawn(ChargerBotProShielded, path=1) if hard else None,
                        Spawn(ExplodeyBotNoTimeLimit, path=1 if hard else 2),
                        Spawn(StickyBotPro, path=1 if hard else 2),
                        Spawn(TriggerBotPro, path=1 if hard else 2),
                        Spawn(TriggerBotPro, path=1 if hard else 2),
                        Spawn(TriggerBotPro, path=1 if hard else 2),
                        (
                            Spawn(TriggerBotPro, path=1 if hard else 2)
                            if player_count > 1
                            else None
                        ),
                        (
                            Spawn(TriggerBotPro, path=1 if hard else 2)
                            if player_count > 3
                            else None
                        ),
                    ]
                ),
                Wave(
                    entries=[
                        Spawn(
                            NoirBot if hard else TriggerBotPro,
                            point=Point.BOTTOM_LEFT,
                        ),
                        (
                            Spawn(
                                BrawlerBotProShielded, point=Point.BOTTOM_RIGHT
                            )
                            if hard
                            else None
                        ),
                        (
                            Spawn(SoldatBot, point=Point.BOTTOM_RIGHT)
                            if player_count > 2
                            else None
                        ),
                        Spawn(SoldatBot, path=3),
                        Spawn(SoldatBot, path=3),
                        Spacing(duration=5.0),
                        Spawn(BrawlerBotPro, path=2),
                        Spawn(BrawlerBotPro, path=2),
                        Spacing(duration=5.0),
                        Spawn(ChargerBot, path=1) if hard else None,
                        Spawn(ChargerBot, path=1) if hard else None,
                    ]
                ),
                Wave(
                    entries=[
                        Spawn(NoirBot, path=2),
                        Spawn(NoirBot, path=2) if hard else None,
                        Spawn(StickyBot, point=Point.BOTTOM_RIGHT),
                        Spawn(ChargerBot, path=2),
                        Spawn(ChargerBotProShielded, path=2),
                        (
                            Spawn(WaiterBot, point=Point.BOTTOM_RIGHT)
                            if player_count > 2
                            else None
                        ),
                        Spawn(BomberBotProShielded, path=2),
                        Spawn(ExplodeyBot, point=Point.BOTTOM_LEFT),
                        Spawn(BomberBot, path=2),
                        Spawn(BomberBot, path=2) if player_count > 1 else None,
                        Spacing(duration=5.0),
                        Spawn(NoirBot, point=Point.BOTTOM_LEFT),
                        Spacing(duration=2.0),
                        Spawn(TriggerBot, point=Point.BOTTOM_RIGHT),
                    ]
                ),
                Wave(
                    entries=[
                        Spawn(
                            TriggerBotProShielded if hard else TriggerBotPro,
                            point=Point.BOTTOM_LEFT,
                        ),
                        (
                            Spawn(
                                TriggerBotProShielded, point=Point.BOTTOM_RIGHT
                            )
                            if hard
                            else None
                        ),
                        (
                            Spawn(
                                TriggerBotProShielded, point=Point.BOTTOM_RIGHT
                            )
                            if player_count > 2
                            else None
                        ),
                        Spawn(SoldatBot, path=3),
                        Spawn(ExplodeyBotNoTimeLimit, path=3),
                        Spacing(duration=5.0),
                        Spawn(BrawlerBotPro, path=2),
                        Spawn(BrawlerBotPro, path=2),
                        Spacing(duration=5.0),
                        Spawn(ChargerBot, path=1) if hard else None,
                        Spawn(TriggerBotProShielded, path=1) if hard else None,
                    ]
                ),
                Wave(
                    entries=[
                        Spawn(ChargerBotProShielded, path=2),
                        Spawn(ChargerBotProShielded, path=2) if hard else None,
                        Spawn(StickyBotPro, point=Point.BOTTOM_RIGHT),
                        Spawn(BomberBotProShielded, path=2),
                        Spawn(BomberBotProShielded, path=2),
                        (
                            Spawn(StickyBot, point=Point.BOTTOM_RIGHT)
                            if player_count > 2
                            else None
                        ),
                        Spawn(BomberBotProShielded, path=2),
                        Spawn(ExplodeyBotNoTimeLimit, point=Point.BOTTOM_LEFT),
                        Spawn(ChargerBot, path=2),
                        (
                            Spawn(TriggerBotProShielded, path=2)
                            if player_count > 1
                            else None
                        ),
                        Spacing(duration=5.0),
                        Spawn(StickyBot, point=Point.BOTTOM_LEFT),
                        Spacing(duration=2.0),
                        Spawn(ExplodeyBot, point=Point.BOTTOM_RIGHT),
                    ]
                ),
            ]
        elif self._preset in {Preset.ENDLESS, Preset.ENDLESS_TOURNAMENT}:
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
                    "color": (1, 0.2, 0.2),
                },
            )
        )
        self._death_lives_bg = ba.NodeActor(
            ba.newnode(
                "image",
                attrs={
                    "texture": self._heart_tex,
                    "model_opaque": self._heart_model_opaque,
                    "model_transparent": self._heart_model_transparent,
                    "attach": "topRight",
                    "scale": (70, 70),
                    "position": (-180 + l_offs, -60),
                    "color": (0, 0.85, 0.2),
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

        self._death_lives_text = ba.NodeActor(
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
                    "position": (-182 + l_offs, -75),
                    "scale": 1,
                    "text": str(self._death_lives),
                },
            )
        )

        ba.timer(2.0, self._start_updating_waves)

    def on_continue(self) -> None:
        self._death_lives = 3
        assert self._death_lives_text is not None
        assert self._death_lives_text.node
        self._death_lives_text.node.text = str(self._death_lives)
        super().on_continue()

    def end_game(self) -> None:
        super().end_game()
        ba.setmusic(ba.MusicType.DEFEAT_KABLOOYA)

    def _update_waves(self) -> None:
        # pylint: disable=too-many-branches

        # If we have no living bots, go to the next wave.
        if (
            self._can_end_wave
            and not self._bots.have_living_bots()
            and not self._game_over
            and self._lives > 0
            and self._death_lives > 0
        ):

            self._can_end_wave = False
            self._time_bonus_timer = None
            self._time_bonus_text = None

            if self._preset in {Preset.ENDLESS, Preset.ENDLESS_TOURNAMENT}:
                won = False
            else:
                assert self._waves is not None
                won = self._wavenum == len(self._waves)

            # Reward time bonus.
            base_delay = 4.0 if won else 0
            if self._time_bonus > 0:
                ba.timer(0, ba.Call(ba.playsound, self._cashregistersound))
                ba.timer(
                    base_delay,
                    ba.Call(self._award_time_bonus, self._time_bonus),
                )
                base_delay += 1.0

            # Reward flawless bonus.
            if self._wavenum > 0 and self._flawless:
                ba.timer(base_delay, self._award_flawless_bonus)
                base_delay += 1.0

            self._flawless = True  # reset

            if won:
                # Give remaining players some points and have them celebrate.
                self.show_zoom_message(
                    ba.Lstr(resource="victoryText"), scale=1.0, duration=4.0
                )

                self.celebrate(10.0)
                ba.timer(base_delay, self._award_lives_bonus)
                ba.timer(base_delay, self._award_death_lives_bonus)
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

            # Short celebration after waves.
            if self._wavenum > 1:
                self.celebrate(0.5)

            ba.timer(base_delay, self._start_next_wave)

    def _award_death_lives_bonus(self) -> None:
        bonus = self._lives * 30
        ba.playsound(self._cashregistersound)
        PopupText(
            ba.Lstr(
                value="+${A} ${B}",
                subs=[
                    ("${A}", str(bonus)),
                    ("${B}", ba.Lstr(resource="livesBonusText")),
                ],
            ),
            color=(0.7, 1.0, 0.3, 1),
            scale=1.3,
            position=(0, 1, -1),
        ).autoretain()
        self._score += bonus
        self._update_scores()

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
                defender_types += [(ToxicBot, 0.7)] * (1 + (level - 5) // 6)
                defender_types += [(SplashBot, 0.65)] * (1 + (level - 5) // 4)

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
                    "h_attach": "center",
                    "h_align": "center",
                    "color": (1, 1, 0.0, 1),
                    "shadow": 1.0,
                    "vr_depth": -30,
                    "flatness": 1.0,
                    "position": (0, -60),
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
                    "h_attach": "center",
                    "h_align": "center",
                    "vr_depth": -10,
                    "color": (1, 1, 1, 1),
                    "shadow": 1.0,
                    "flatness": 1.0,
                    "position": (0, -40),
                    "scale": 1.3,
                    "text": txtval,
                },
            )
        )

    def handlemessage(self, msg: Any) -> Any:
        # Augment standard behavior.
        super().handlemessage(msg)

        if isinstance(msg, ba.PlayerDiedMessage):
            # Substract one point from our death lives counter.
            if self._death_lives > 0:
                self._death_lives -= 1
            if self._death_lives == 0:
                self._bots.stop_moving()
                self.continue_or_end_game()
            assert self._death_lives_text is not None
            assert self._death_lives_text.node
            self._death_lives_text.node.text = str(self._death_lives)


class EndlessKablooyaRunaroundGame(KablooyaRunaroundGame):
    name = "Endless Kablooya Runaround"
    description = "Prevent enemies from reaching the exit for as long as you can.\nAnd don't die. Really."
