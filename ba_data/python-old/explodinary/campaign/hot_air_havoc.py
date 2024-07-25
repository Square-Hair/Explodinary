from __future__ import annotations

import ba
from explodinary.actor.bsespazbot import (
    ChargerBot,
    BrawlerBot,
    ExplodeyBotNoTimeLimit,
    BouncyBot,
    BrawlerBotProShielded,
    ChargerBotProShielded,
    ChargerBotPro,
    SpazBotDiedMessage,
    TriggerBotProShielded,
    TriggerBotPro,
    BrawlerBotPro,
    SoldatBot,
    MellyBot,
    NoirBot,
)

from explodinary.campaign import (
    BSECampaignActivity,
    Wave,
    Spawn,
    Point,
    Delay,
)

import random
from explodinary.lib import dialogue, skipvote
from bastd.gameutils import SharedObjects

from typing import Any

class HotAirHavocGame(BSECampaignActivity):
    """ Fifth BSE Campaign Level. """

    name = 'Hot Air Havoc'

    def __init__(self, settings: dict):

        # Set our map and if we get our defs from the json file.
        settings['map'] = 'Hot Air Havoc'
        settings['json'] = False

        super().__init__(settings)


    def _map_defs(self) -> dict:
        """ Map defs in case we opt-out of getting defs from our json file. """
        return {
            'spawn_center':     (-1, 2, -2),
            'tntspawnpos':      (0.0, 3.0, 2.1),
            'powerup_center':   (0, 4, -1),
            'powerup_spread':   (3, 2),
        }


    def on_transition_in(self) -> None:
        super().on_transition_in()
        customdata = ba.getsession().customdata

        # Cutting scenes since 1984
        self._has_cutscene = True
        
        # Music
        self._music = ba.MusicType.HOT_AIR

    def on_begin(self) -> None:

        # Save some general variables.
        player_count = len(self.players)
        self._excluded_powerups = ['vital_bombs', 'fly_punch', 'dash']
        args: dict = {
            'first_spawn_type': ['clouder_bombs', 'flutter_mines'],
            'tnt': False,
            'goal_time': '2m05s',
        }

        # Our main list of waves and events.
        self._waves = [
            Wave(
                entries=[
                    Spawn(SoldatBot, Point.RIGHT),
                    Spawn(SoldatBot, Point.RIGHT_UPPER),
                    Spawn(SoldatBot, Point.RIGHT_UPPER_MORE),
                    Spawn(BrawlerBot, Point.LEFT),
                    Spawn(BrawlerBot, Point.LEFT_UPPER),
                    Spawn(BrawlerBot, Point.LEFT_UPPER_MORE),
                    Spawn(ChargerBot, Point.TOP)
                    if player_count > 2
                    else None,
                    Spawn(BrawlerBot, Point.TOP_HALF_RIGHT),
                ]
            ),
            Wave(
                entries=[
                    Spawn(NoirBot, Point.BOTTOM),
                    Spawn(NoirBot, Point.TOP),
                    Spawn(ChargerBot, Point.BOTTOM_HALF_RIGHT),
                    Spawn(ChargerBot, Point.BOTTOM_HALF_LEFT)
                    if player_count > 1
                    else None,
                    Spawn(NoirBot, Point.BOTTOM_RIGHT)
                    if player_count > 2
                    else None,
                    Spawn(ChargerBot, Point.TOP_RIGHT),
                    Spawn(ChargerBot, Point.TOP_LEFT)
                    if player_count > 3
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(ExplodeyBotNoTimeLimit, Point.RIGHT),
                    Spawn(TriggerBotProShielded if player_count > 1 else TriggerBotPro, Point.TOP_HALF_LEFT),
                    Spawn(TriggerBotProShielded if player_count > 1 else TriggerBotPro, Point.TOP_HALF_RIGHT),
                    Spawn(ExplodeyBotNoTimeLimit, Point.LEFT)
                    if player_count > 1
                    else None,
                    Spawn(ExplodeyBotNoTimeLimit, Point.TOP_RIGHT),
                    Spawn(ExplodeyBotNoTimeLimit, Point.TOP_LEFT)
                    if player_count > 2
                    else None,
                    Spawn(TriggerBotProShielded if player_count > 2 else TriggerBotPro, Point.RIGHT_UPPER),
                    Spawn(TriggerBotProShielded if player_count > 2 else TriggerBotPro, Point.LEFT_UPPER)
                    if player_count > 3
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(BouncyBot, Point.RIGHT),
                    Spawn(BouncyBot, Point.LEFT),
                    Spawn(MellyBot, Point.TOP),
                    Spawn(MellyBot, Point.BOTTOM)
                    if player_count > 1
                    else None,
                    Spawn(MellyBot, Point.TOP_LEFT)
                    if player_count > 2
                    else None,
                    Spawn(BouncyBot, Point.TOP_HALF_LEFT),
                    Spawn(BouncyBot, Point.TOP_HALF_RIGHT)
                    if player_count > 3
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(SoldatBot, Point.RIGHT_UPPER),
                    Spawn(SoldatBot, Point.LEFT_UPPER),
                    Spawn(BrawlerBotProShielded, Point.BOTTOM),
                    Spawn(BrawlerBotProShielded, Point.TOP)
                    if player_count > 1
                    else None,
                    Spawn(BrawlerBotPro, Point.BOTTOM_HALF_LEFT)
                    if player_count > 2
                    else None,
                    Spawn(BrawlerBotProShielded, Point.BOTTOM_LEFT),
                    Spawn(BrawlerBotPro, Point.BOTTOM_HALF_RIGHT),
                    Spawn(BrawlerBotProShielded, Point.BOTTOM_RIGHT)
                    if player_count > 3
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(ChargerBotProShielded if player_count > 2 else ChargerBotPro, Point.RIGHT),
                    Spawn(ChargerBotProShielded if player_count > 2 else ChargerBotPro, Point.LEFT),
                    Spawn(BrawlerBotPro, Point.RIGHT_UPPER),
                    Spawn(BrawlerBotPro, Point.LEFT_UPPER),
                    Delay(1.75),
                    Spawn(SoldatBot, Point.TOP)
                    if player_count > 1
                    else None,
                    Spawn(SoldatBot, Point.TOP_HALF_RIGHT)
                    if player_count > 2
                    else None,
                    Delay(1.25),
                    Spawn(BrawlerBotPro, Point.LEFT_LOWER),
                    Spawn(SoldatBot, Point.TOP_HALF_LEFT),
                    Spawn(ChargerBotProShielded, Point.RIGHT_LOWER)
                    if player_count > 3
                    else None,
                ]
            ),
        ]

        # Let our main class set up powerups, start waves and such.
        super().on_begin(args)
        self._fling_kills: int = 0
        # 
        self._combo_kill_timer: dict[ba.Timer] = {}
        self._combo_counter: dict = {}
        self._double_kills: int = 0

        # Ctsc
        self._do_intro_cutscene()

    def _do_intro_cutscene(self):
        """ Does our level intro. """
        # Skip if we've already seen this cutscene / are in speedrun mode / have "skip cutscenes" enabled
        if self.has_done_cutscene('hah'):
            self._intro_cutscene_end(True)
            return
        
        # Extra functions
        def _powerups()     : ba.timer(1.6, ba.WeakCall(self._start_spawning_stuff, 0, 1.5, 0, False))
        def _end():
            _skip_vote.end()
            self._intro_cutscene_end()
            
        def helpygoner():
            """ Disappears our Helpy as if he just said something controversial. """
            self.helpy_move(-1, 0, True, True)
            ba.timer(0.4, self.badoink_helpy)
            
        # Spawn Helpy in this cutscene
        self.spawn_helpy((-2.2, 2.2, -2.8))
        
        # Disable player controls
        self._handle_controllers(False)

        # Dialogue routine
        dkey = "explodinary.campaignDialogue.hot_air_havoc."
        player_speakers = [dialogue.get_player_speaker(p) for p in self.players]; helpy_speaker = dialogue.SpeakerLib().helpy
        
        _skip_vote = skipvote.SkipVoteModule(skiptext=ba.Lstr(resource='explodinary.skipCutscene'), on_vote_end=self.reset)
        
        _dialogue_manager = dialogue.DialogueManager(finish_call = _end)
        _dialogue_manager.add_message([
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}00"),                     time=1.5, idle=1.4, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}01"),    time=1.9, idle=1.4, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}02"),                     time=1.5, idle=1.1, fade=0.0, end_call=_powerups),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}03"),    time=1.9, idle=1.4, fade=0.0, end_call=ba.Call(ba.timer, 1.7, helpygoner)),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}04"),                     time=2.2, idle=1.3, fade=0.3, end_call=None),
        ])
        
        ba.timer(1.9, self._dumb_bot_spawn)
        ba.timer(0.5, _dialogue_manager.start)
        
    def _end_wrapup(self):
        # Show once per session only.
        cd = ba.getsession().customdata
        if not cd.get('tip_hah', False):
            cd['tip_hah'] = True
            self.tips = [
                ba.GameTip(
                        'Flutter Bombs or Flutter Mines are capable of launching your enemies far, far away!\n'
                        'They do pitiful damage, though, so keep that in mind.',
                        icon=ba.gettexture('flutterTip'),
                        sound=ba.getsound('ding'),
                )
            ]
        self._dumbify(True)
        ba.timer(3, ba.WeakCall(self._start_time_bonus_timer))
        ba.timer(0.8, self._show_tip)
        ba.timer(0.2, self._render_badges)

    def _do_end_cutscene(self, outcome: str):
        """ Does our end level cutscene. """
        if self.has_done_cutscene('hahf', False):
            super().do_end(outcome)
            return
        
        # Dialogue routine
        dkey = "explodinary.campaignDialogue.hot_air_havoc."
        player_speakers = [dialogue.get_player_speaker(p) for p in self.players]; helpy_speaker = dialogue.SpeakerLib().helpy
        
        # Spawn our helpy boyo!
        self.spawn_helpy((3, 2, -3), True)
        self._cutscene_helpy.node.is_area_of_interest = True
        self.old_aoib = None
        
        # Extra funcs
        def _thrash_balloon():
            """ Replaces our healthy balloon with a thrashed one and focuses the camera on it. """
            try:
                self.old_aoib = ba.getactivity().globalsnode.area_of_interest_bounds
                ba.getactivity().globalsnode.area_of_interest_bounds = (0,20,21,0,22,12)
                
                self.map.balloon.model                  = ba.getmodel('balloonBroken') 
                self.map.balloon.color_texture          = ba.gettexture('balloonBrokenColor')
            except Exception as e: print(f'Could not thrash balloon!\nMotive is "{e}"')
        def _unfocus_balloon()  : ba.getactivity().globalsnode.area_of_interest_bounds = self.old_aoib
        
        def _end():
            #_skip_vote.end()
            self.alt_do_end(outcome)    
        
        plural = len(self.players) > 1
        
        _skip_vote = skipvote.SkipVoteModule(skiptext=ba.Lstr(resource='explodinary.skipCutscene'), on_vote_end=_end)
        _dialogue_manager = dialogue.DialogueManager(finish_call = _end)
        
        _dialogue_manager.add_message([
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e00"),                                            time=2.1, idle=1.4, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}e01{'a' if plural else ''}"),    time=0.3, idle=1.6, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e02"),                                            time=2.1, idle=1.2, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}e03"),                           time=1.9, idle=1.4, fade=0.0, end_call=_thrash_balloon),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e04"),                                            time=3.3, idle=2.1, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e05"),                                            time=2.3, idle=1.3, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}e06"),                           time=0.9, idle=1.2, fade=0.6, end_call=None),
        ])
        
        _dialogue_manager.start()
        
    def do_end(self, outcome: str, delay: float = 0) -> None:
        if self._won:
            self._do_end_cutscene(outcome)
        else: super().do_end(outcome, delay)

    def _badge_define(self):
        """ Defines our badges. """
        k = 'explodinary.campaignBadge.hah.'
        # Speedrun
        self._badge_append(
            'timetrial',
            ba.Lstr(resource=f'{k}n00'),
            ba.Lstr(resource=f'{k}d00'),
            '',
            'badgeSpeed',
        )
        # Quad kill
        self._badge_append(
            'threetwo',
            ba.Lstr(resource=f'{k}n01'),
            ba.Lstr(resource=f'{k}d01'),
            '',
            'badgeKills',
        )
        # Balloon kills
        self._badge_append(
            'offyougo',
            ba.Lstr(resource=f'{k}n02'),
            ba.Lstr(resource=f'{k}d02'),
            '',
            'badgeBalloon',
        )

    def _handle_kill_achievements(self, msg: SpazBotDiedMessage) -> None:
        """ Handles kill badge goals. """
        killer = msg.killerplayer
        if not killer: return

        # Check if our goofballs were killed by falling off the map
        if msg.how is ba.DeathType.FALL:
            # Sum and celebrate!
            self._fling_kills += 1
            if self._fling_kills == 3:
                self._badge_update('offyougo', True)

        # Quad-kill handling
        try: self._combo_counter[killer] += 1
        except KeyError: self._combo_counter[killer] = 1
        # Create a timer so we can reset our counter in case it takes us too long
        self._combo_kill_timer[killer] = None
        self._combo_kill_timer[killer] = ba.Timer(1.0, lambda: self._kill_combo(killer))
        # Woah, a double kill? Better keep track of that!
        if self._combo_counter[killer] == 2:
            self._double_kills += 1
            # We got 3 double kills at last! grant the badge if we havent!
            if self._double_kills == 3 and not self._badge_status('threetwo'):
                self._badge_update('threetwo', True)

    def _kill_combo(self, killer:str) -> None:
        # Took too long! Reset our combo kill counter.
        self._combo_counter[killer] = 0