from __future__ import annotations

from typing import TYPE_CHECKING

import ba
from bastd.actor.bomb import TNTSpawner
from bastd.actor.scoreboard import Scoreboard
from bastd.actor.spazbot import (
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
    from typing import Any, Sequence
    from bastd.actor.spazbot import SpazBot

from bastd.game.onslaught import (
    OnslaughtGame,
    Wave,
    Preset,
)

class TimeyBombnutsGame(OnslaughtGame):
    """Co-op game where players try to survive attacking waves of enemies."""

    name = 'Timey Bombnuts'
    description = 'This level is timed, get the best score before the time runs out!'

    def __init__(self, settings: dict):

        self._preset = Preset(settings.get('preset', 'training'))
        settings['map'] = 'Tree'

        ba.CoopGameActivity.__init__(self, settings)

        self._new_wave_sound = ba.getsound('scoreHit01')
        self._winsound = ba.getsound('score')
        self._cashregistersound = ba.getsound('cashRegister')
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
        self._spawn_info_text: ba.NodeActor | None = None
        self._dingsound = ba.getsound('dingSmall')
        self._dingsoundhigh = ba.getsound('dingSmallHigh')
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

    def on_transition_in(self) -> None:
        super().on_transition_in()
        ba.setmusic(ba.MusicType.BOMBNUTS)
        
    def on_begin(self) -> None:
        super().on_begin()
        self._time_limit = (300)
        self.setup_standard_time_limit(self._time_limit)
        self._excluded_powerups = []
        
    def _do_tnt(self): self._tntspawner = TNTSpawner(position=self._tntspawnpos)

    def _start_next_wave(self) -> None:

        # This can happen if we beat a wave as we die.
        # We don't wanna respawn players and whatnot if this happens.
        if self._game_over:
            return

        self._respawn_players_for_wave()
        if self._preset in {Preset.ENDLESS, Preset.ENDLESS_TOURNAMENT}:
            wave = self._generate_random_wave()
        else:
            wave = self._waves[self._wavenum - 1]
        self._setup_wave_spawns(wave)
        self._update_wave_ui_and_bonuses()
        ba.timer(0.4, ba.Call(ba.playsound, self._new_wave_sound))
        
    def _update_wave_ui_and_bonuses(self) -> None:

        self.show_zoom_message(
            ba.Lstr(
                value='${A} ${B}',
                subs=[
                    ('${A}', ba.Lstr(resource='waveText')),
                    ('${B}', str(self._wavenum)),
                ],
            ),
            scale=1.0,
            duration=1.0,
            trail=True,
        )

        # Reset our time bonus.
        tbtcolor = (1, 1, 0, 1)
        tbttxt = ba.Lstr(
            value='${A}: ${B}',
            subs=[
                ('${A}', ba.Lstr(resource='timeBonusText')),
                ('${B}', str(self._time_bonus)),
            ],
        )
        self._time_bonus_text = ba.NodeActor(
            ba.newnode(
                'text',
                attrs={
                    'v_attach': 'top',
                    'h_attach': 'center',
                    'h_align': 'center',
                    'vr_depth': -30,
                    'color': tbtcolor,
                    'shadow': 1.0,
                    'flatness': 1.0,
                    'position': (15, -105),
                    'scale': 0.8,
                    'text': tbttxt,
                },
            )
        )

        ba.timer(5.0, ba.WeakCall(self._start_time_bonus_timer))
        wtcolor = (1, 1, 1, 1)
        wttxt = ba.Lstr(
            value='${A} ${B}',
            subs=[
                ('${A}', ba.Lstr(resource='waveText')),
                (
                    '${B}',
                    str(self._wavenum)
                    + (
                        ''
                        if self._preset
                        in [Preset.ENDLESS, Preset.ENDLESS_TOURNAMENT]
                        else ('/' + str(len(self._waves)))
                    ),
                ),
            ],
        )
        self._wave_text = ba.NodeActor(
            ba.newnode(
                'text',
                attrs={
                    'v_attach': 'top',
                    'h_attach': 'center',
                    'h_align': 'center',
                    'vr_depth': -10,
                    'color': wtcolor,
                    'shadow': 1.0,
                    'flatness': 1.0,
                    'position': (15, -85),
                    'scale': 1.3,
                    'text': wttxt,
                },
            )
        )

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
            raise RuntimeError('Got empty bot level')
        return bot_levels


    def end_game(self) -> None:
        super().end_game()
        ba.setmusic(ba.MusicType.DEFEAT)
