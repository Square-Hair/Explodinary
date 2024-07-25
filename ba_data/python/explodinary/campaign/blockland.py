from __future__ import annotations
from typing import Any

import ba
from explodinary.actor.bsespazbot import (
    ChargerBot,
    StickyBot,
    ExplodeyBotNoTimeLimit,
    BouncyBot,
    BrawlerBotProShielded,
    ChargerBotProShielded,
    TriggerBotProShielded,
    TriggerBotPro,
    ExplodeyBot,
    MicBot,
    SplashBot,
    SoldatBot,
)

from explodinary.campaign import (
    BSECampaignActivity,
    Player,
    Wave,
    Spawn,
    Point,
    Player,
)

from bastd.actor.playerspaz import PlayerSpazVitalMessage, PlayerSpazVitaminMessage
from explodinary.lib import dialogue, skipvote
import random

class BlocklandGame(BSECampaignActivity):
    """ Seventh BSE Campaign Level. """

    name = 'Blockland'

    def __init__(self, settings: dict):

        # Set our map and if we get our defs from the json file.
        settings['map'] = 'Blockland'
        settings['json'] = False

        super().__init__(settings)


    def _map_defs(self) -> dict:
        """ Map defs in case we opt-out of getting defs from our json file. """
        return {
            'spawn_center':     (-6, 2, -2),
            'tntspawnpos':      (-0.11, 3.0, 1.9),
            'powerup_center':   (0, 4, -2.3),
            'powerup_spread':   (5.82, 2.9),
        }


    def on_transition_in(self) -> None:
        super().on_transition_in()

        # Yeah :)
        self._has_cutscene = True

        # MUSIC!
        self._music = ba.setmusic(ba.MusicType.BLOCKLAND)


    def on_begin(self) -> None:

        # Save some general variables.
        player_count = len(self.players)
        self._excluded_powerups = ['fly_punch', 'dash']
        args: dict = {
            'first_spawn_type': ['vital_bombs'],
            'tnt': True,
            'goal_time': '2m15s',
        }

        # Our main list of waves and events.
        self._waves = [
            Wave(
                entries=[
                    Spawn(BrawlerBotProShielded, Point.TOP),
                    Spawn(BrawlerBotProShielded, Point.TOP_HALF_LEFT),
                    Spawn(BrawlerBotProShielded, Point.TOP_LEFT),
                    Spawn(ChargerBot, Point.LEFT_LOWER),
                    Spawn(ChargerBot, Point.BOTTOM_LEFT),
                    Spawn(ChargerBot, Point.LEFT_LOWER_MORE)
                    if player_count > 2
                    else None,
                    Spawn(BrawlerBotProShielded, Point.TOP_HALF_RIGHT),
                ]
            ),
            Wave(
                entries=[
                    Spawn(TriggerBotPro, Point.BOTTOM_RIGHT),
                    Spawn(TriggerBotPro, Point.BOTTOM_LEFT),
                    Spawn(TriggerBotPro, Point.LEFT_UPPER),
                    Spawn(ExplodeyBot, Point.RIGHT_UPPER),
                    Spawn(ExplodeyBot, Point.TOP)
                    if player_count > 1
                    else None,
                    Spawn(TriggerBotPro, Point.BOTTOM_HALF_LEFT),
                    Spawn(ExplodeyBot, Point.BOTTOM_HALF_RIGHT)
                    if player_count > 2
                    else None,
                    Spawn(TriggerBotProShielded, Point.LEFT_LOWER),
                    Spawn(ExplodeyBotNoTimeLimit, Point.TOP_HALF_LEFT),
                    Spawn(TriggerBotProShielded, Point.RIGHT_LOWER)
                    if player_count > 3
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(SplashBot, Point.LEFT_UPPER_MORE),
                    Spawn(SoldatBot, Point.LEFT_UPPER),
                    Spawn(SplashBot, Point.LEFT),
                    Spawn(SplashBot, Point.RIGHT_UPPER_MORE),
                    Spawn(SoldatBot, Point.RIGHT_UPPER),
                    Spawn(SplashBot, Point.RIGHT),
                    Spawn(BouncyBot, Point.BOTTOM_HALF_LEFT),
                    Spawn(BouncyBot, Point.BOTTOM_HALF_RIGHT)
                    if player_count > 1
                    else None,
                    Spawn(BouncyBot, Point.TOP_RIGHT)
                    if player_count > 2
                    else None,
                    Spawn(BouncyBot, Point.TOP_HALF_LEFT),
                    Spawn(BouncyBot, Point.TOP_HALF_RIGHT),
                    Spawn(BouncyBot, Point.TOP_LEFT)
                    if player_count > 3
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(StickyBot, Point.RIGHT),
                    Spawn(StickyBot, Point.LEFT),
                    Spawn(StickyBot, Point.TOP),
                    Spawn(StickyBot, Point.BOTTOM),
                    Spawn(StickyBot, Point.LEFT_LOWER),
                    Spawn(StickyBot, Point.RIGHT_LOWER)
                    if player_count > 1
                    else None,
                    Spawn(StickyBot, Point.TOP_LEFT),
                    Spawn(StickyBot, Point.TOP_RIGHT)
                    if player_count > 2
                    else None,
                    Spawn(StickyBot, Point.TOP_HALF_LEFT),
                    Spawn(StickyBot, Point.TOP_HALF_RIGHT)
                    if player_count > 3
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(ChargerBotProShielded, Point.RIGHT_UPPER),
                    Spawn(ChargerBotProShielded, Point.LEFT_UPPER),
                    Spawn(MicBot, Point.BOTTOM),
                    Spawn(MicBot, Point.TOP),
                    Spawn(SplashBot, Point.TOP_HALF_LEFT),
                    Spawn(SplashBot, Point.TOP_HALF_RIGHT)
                    if player_count > 1
                    else None,
                    Spawn(ChargerBotProShielded, Point.BOTTOM_HALF_LEFT),
                    Spawn(ChargerBotProShielded, Point.BOTTOM_HALF_RIGHT)
                    if player_count > 2
                    else None,
                    Spawn(MicBot, Point.BOTTOM_LEFT),
                    Spawn(SplashBot, Point.BOTTOM_RIGHT)
                    if player_count > 3
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(SplashBot, Point.RIGHT),
                    Spawn(SplashBot, Point.LEFT),
                    Spawn(BrawlerBotProShielded, Point.RIGHT_UPPER),
                    Spawn(BrawlerBotProShielded, Point.LEFT_UPPER),
                    Spawn(BrawlerBotProShielded, Point.TOP)
                    if player_count > 1
                    else None,
                    Spawn(BrawlerBotProShielded, Point.TOP_HALF_RIGHT)
                    if player_count > 2
                    else None,
                    Spawn(SplashBot, Point.LEFT_LOWER),
                    Spawn(BrawlerBotProShielded, Point.TOP_HALF_LEFT),
                    Spawn(SplashBot, Point.RIGHT_LOWER)
                    if player_count > 3
                    else None,
                ]
            ),
        ]
        
        # Let our main class set up powerups, start waves and such.
        super().on_begin(args)

        # Extra badge goal variables
        vtg = self._vitalizations_goal = 2+int(1.75*player_count)
        self._vitalizations: int = 0
        self._vitamizations: int = 0

        self._badge_text('vitalize',
                         desc=ba.Lstr(resource='explodinary.campaignBadge.bl.d01', subs=[('${COUNT}', str(vtg))]),
                         )
        
        self.spawn_helpy((-11.2, 4.8, -1.15))
        self._do_intro_cutscene()

    def _do_intro_cutscene(self):
        """ Does our level intro. """
        # Skip if we've already seen this cutscene / are in speedrun mode / have "skip cutscenes" enabled
        if self.has_done_cutscene('bl'):
            self._intro_cutscene_end(True)
            return
        
        # Extra functions
        def _dumb_spawn()   : ba.timer(0.4, self._dumb_bot_spawn)
        def _powerups()     : ba.timer(1.6, ba.WeakCall(self._start_spawning_stuff, 0, 1.5, 0, False))
        def _end():
            _skip_vote.end()
            self._intro_cutscene_end()
        
        # Disable player controls
        self._handle_controllers(False)

        # Extra funcs
        def oh()    : dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}03"), time=0.4, idle=1.0, fade=0.6, scale=0.44, offset=(85, 85), end_call=None).start()

        # Dialogue routine
        dkey = "explodinary.campaignDialogue.blockland."
        player_speakers = [dialogue.get_player_speaker(p) for p in self.players]; helpy_speaker = dialogue.SpeakerLib().helpy
        
        _skip_vote = skipvote.SkipVoteModule(skiptext=ba.Lstr(resource='explodinary.skipCutscene'), on_vote_end=self.reset)
        
        plural = len(self.players) > 1
        
        _dialogue_manager = dialogue.DialogueManager(finish_call = _end)
        _dialogue_manager.add_message([
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}00"),                                             time=0.4, idle=1.1, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}01{'a' if plural else ''}"),     time=2.2, idle=1.2, fade=0.0, end_call=None),
            ('call', ba.Call(ba.timer, 0.8, oh)),
            ('call', ba.Call(ba.timer, 1.4, self._dumb_bot_spawn)),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}02"),                                             time=0.2, idle=2.0, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}04"),                                             time=1.2, idle=1.4, fade=0.6, end_call=None),
            ('wait', 1.4),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}05"),                                             time=2.1, idle=1.4, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}06"),                            time=1.5, idle=1.2, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}07"),                                             time=0.3, idle=1.5, fade=0.0, end_call=ba.Call(self._start_spawning_stuff, 1.4, 5.4, 1, False)),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}08"),                            time=1.3, idle=1.4, fade=0.6, end_call=None),
        ])
        
        ba.timer(0.5, _dialogue_manager.start)
        
    def _end_wrapup(self):
        # Show once per session only.
        cd = ba.getsession().customdata
        if not cd.get('tip_bl', False):
            cd['tip_bl'] = True
            self.tips = [
                ba.GameTip(
                    'Use Vital Bombs to heal yourself or your\n'
                    'allies, and to boost your punching speed!',
                    icon=ba.gettexture('powerupVitalBombs'),
                    sound=ba.getsound('vitalBlast'),
                )
            ]
        ba.timer(3, ba.WeakCall(self._start_time_bonus_timer))
        ba.timer(0.8, self._show_tip)
        ba.timer(0.2, self._render_badges)

    def _do_end_cutscene(self, outcome: str):
        """ Does our end level cutscene. """
        self._cutscene_helpy.node.is_area_of_interest = True

        if self.has_done_cutscene('blf', False):
            super().do_end(outcome)
            return
        
        # Dialogue routine
        dkey = "explodinary.campaignDialogue.blockland."
        player_speakers = [dialogue.get_player_speaker(p) for p in self.players]; helpy_speaker = dialogue.SpeakerLib().helpy
        
        # Extra funcs
        def _end():
            #_skip_vote.end()
            self.alt_do_end(outcome)    
        
        plural = len(self.players) > 1
        
        _skip_vote = skipvote.SkipVoteModule(skiptext=ba.Lstr(resource='explodinary.skipCutscene'), on_vote_end=_end)
        _dialogue_manager = dialogue.DialogueManager(finish_call = _end)
        
        _dialogue_manager.add_message([
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e00"),                                            time=0.4, idle=1.3, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}e01{'a' if plural else ''}"),    time=2.4, idle=1.8, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e02"),                                            time=0.3, idle=1.3, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e03"),                                            time=6.7, idle=1.7, fade=1.2, end_call=None),
        ])
        
        _dialogue_manager.start()
        
    def do_end(self, outcome: str, delay: float = 0) -> None:
        if self._won:
            self._do_end_cutscene(outcome)
        else: super().do_end(outcome, delay)

    def spawn_player(self, player: Player) -> ba.Actor:
        import random
        # We keep track of who got hurt each wave for score purposes.
        player.has_been_hurt = False
        pos = (
            self._spawn_center[0] + random.uniform(-0.5, 0.5),
            self._spawn_center[1],
            self._spawn_center[2] + random.uniform(-0.5, 0.5),
        )
        spaz = self.spawn_player_spaz(player, position=pos)
        spaz.add_dropped_bomb_callback(self._handle_player_dropped_bomb)
        return spaz

    def _badge_define(self):
        """ Defines our badges. """
        k = 'explodinary.campaignBadge.bl.'
        # Speedrun
        self._badge_append(
            'timetrial',
            ba.Lstr(resource=f'{k}n00'),
            ba.Lstr(resource=f'{k}d00'),
            '',
            'badgeSpeed',
        )
        # Use vital bombs
        self._badge_append(
            'vitalize',
            ba.Lstr(resource=f'{k}n01'),
            ba.Lstr(resource=f'{k}d01'),
            '',
            'badgeVital',
        )
        # Take vitamins
        self._badge_append(
            'vitaminize',
            ba.Lstr(resource=f'{k}n02'),
            ba.Lstr(resource=f'{k}d02'),
            '',
            'badgeVitamin',
        )

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, PlayerSpazVitalMessage):
            super().handlemessage(msg)  # Augment standard behavior.
            self.handle_player_vitalize()
        elif isinstance(msg, PlayerSpazVitaminMessage):
            super().handlemessage(msg)  # Augment standard behavior.
            self.handle_player_vitamin()
        else:
            return super().handlemessage(msg) # Return standard behavior.

    def handle_player_vitalize(self):
        """ Handles vitalization badge progression. """
        self._vitalizations += 1
        if self._vitalizations == self._vitalizations_goal:
            self._badge_update('vitalize', True)

    def handle_player_vitamin(self):
        """ Handles vitamin badge progression. """
        self._vitamizations += 1
        if self._vitamizations == 3:
            self._badge_update('vitaminize', True)