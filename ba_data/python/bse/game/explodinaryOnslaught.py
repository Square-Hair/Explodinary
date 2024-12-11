from __future__ import annotations

from typing import TYPE_CHECKING

import bascenev1 as bs
from bascenev1lib.actor.bomb import TNTSpawner
from bascenev1lib.actor.scoreboard import Scoreboard
from bascenev1lib.actor.spazbot import (
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
    MellyBot,
    NoirBot,
    ToxicBot,
)

if TYPE_CHECKING:
    from bascenev1lib.actor.spazbot import SpazBot

from bascenev1lib.game.onslaught import (
    OnslaughtGame,
    Wave,
    Preset,
)


class ExplodinaryOnslaughtGame(OnslaughtGame):
    """Co-op game where players try to survive attacking waves of enemies."""

    name = "Explodinary Infinite Onslaught"
    description = (
        "This level is infinite; Defeat enemies to increase your score."
    )

    tips: list[str | bs.GameTip] = [
        "Hold any button to run."
        "  (Trigger buttons work well if you have them)",
        "Try tricking enemies into killing eachother or running off cliffs.",
        "Try 'Cooking off' bombs for a second or two before throwing them.",
        "It's easier to win with a friend or two helping.",
        "If you stay in one place, you're toast. Run and dodge to survive..",
        "Practice using your momentum to throw bombs more accurately.",
        "Your punches do much more damage if you are running or spinning.",
        "Lite-Mines are a perfect way to keep more bots away from you.",
        "Steam Bombs are perfect for groups.",
        "Try to get group of bots near TNT - multikill guaranteed!",
    ]

    def __init__(self, settings: dict):

        self._preset = Preset(settings.get("preset", "training"))
        settings["map"] = "Onslaught Arena"

        bs.CoopGameActivity.__init__(self, settings)

        self._new_wave_sound = bs.getsound("scoreHit01")
        self._winsound = bs.getsound("score")
        self._cashregistersound = bs.getsound("cashRegister")
        self._a_player_has_been_hurt = False
        self._player_has_dropped_bomb = False

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
        self._spawn_info_text: bs.NodeActor | None = None
        self._dingsound = bs.getsound("dingSmall")
        self._dingsoundhigh = bs.getsound("dingSmallHigh")
        self._have_tnt = False
        self._excluded_powerups: list[str] | None = None
        self._waves: list[Wave] = []
        self._tntspawner: TNTSpawner | None = None
        self._bots: SpazBotSet | None = None
        self._powerup_drop_timer: bs.Timer | None = None
        self._time_bonus_timer: bs.Timer | None = None
        self._time_bonus_text: bs.NodeActor | None = None
        self._flawless_bonus: int | None = None
        self._wave_text: bs.NodeActor | None = None
        self._wave_update_timer: bs.Timer | None = None
        self._throw_off_kills = 0
        self._land_mine_kills = 0
        self._tnt_kills = 0

    def on_transition_in(self) -> None:
        super().on_transition_in()

    def on_begin(self) -> None:
        super().on_begin()
        self._excluded_powerups = []

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
            ExplodeyBot,
            ExplodeyBotShielded,
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
            SoldatBot,
            MellyBot,
            NoirBot,
            ToxicBot,
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
                SoldatBot,
                NoirBot,
                MellyBot,
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
                SoldatBot,
                ToxicBot,
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
                NoirBot,
            ]
        if level > 13:
            bot_types += [
                TriggerBotProShielded,
                TriggerBotProShielded,
                TriggerBotProShielded,
                TriggerBotProShielded,
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

    def _do_tnt(self):
        self._tntspawner = TNTSpawner(position=self._tntspawnpos)

    def end_game(self) -> None:
        super().end_game()
        bs.setmusic(bs.MusicType.DEFEAT)
