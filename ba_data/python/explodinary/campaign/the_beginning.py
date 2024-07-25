from __future__ import annotations

import ba
from explodinary.actor.bsespazbot import (
    BomberBot,
    BrawlerBot,
    BrawlerBotLite,
    SpazBotDiedMessage,
    TriggerBot,
)

from explodinary.campaign import (
    BSECampaignActivity,
    Wave,
    Spawn,
)

from explodinary.lib import dialogue, skipvote
import random

class TheBeginningGame(BSECampaignActivity):
    """ First BSE Campaign Level. """

    name = 'The Beginning'

    def __init__(self, settings: dict):

        # Set our map and if we get our defs from the json file.
        settings['map'] = 'The Beginning'
        settings['json'] = False
        self._wavenum = 0
        super().__init__(settings)


    def _map_defs(self) -> dict:
        """ Map defs in case we opt-out of getting defs from our json file. """
        return {
            'spawn_center':     (-8, 5, -3.5),
            'tntspawnpos':      (0.0, 1.0, -5.0),
            'powerup_center':   (-5, 7, 2),
            'powerup_spread':   (3.0, 5.0),
        }


    def on_transition_in(self) -> None:
        super().on_transition_in()

        # This level has a cutscene
        self._has_cutscene = True


    def on_begin(self) -> None:
        # Save some general variables.
        player_count = len(self.players)
        self._excluded_powerups = ['lite_mines', 'steampunk_bombs', 'toxic_bombs', 'vital_bombs', 'present', 'clouder_bombs', 'flutter_mines', 'fly_punch', 'dash']
        args: dict = {
            'first_spawn_type': ['cluster_bombs'],
            'tnt': True,
            'radial_spawn_y': 5.6,
            'goal_time' : '2m10s',
        }
        self._track_damage = 'nodamage'

        # Our main list of waves and events.
        self._waves = [
            Wave(
                base_angle=60,
                entries=[
                    Spawn(BrawlerBotLite, spacing=40)
                    if player_count > 3
                    else None,
                    Spawn(BrawlerBotLite, spacing=40),
                    Spawn(BomberBot, spacing=50),
                    Spawn(BrawlerBotLite, spacing=40),
                    Spawn(BomberBot, spacing=8)
                    if player_count > 1
                    else None,
                    Spawn(BrawlerBotLite, spacing=40),
                    Spawn(BrawlerBotLite, spacing=40)
                    if player_count > 2
                    else None,
                ],
            ),
            Wave(
                base_angle=45,
                entries=[
                    Spawn(BrawlerBot, spacing=6)
                    if player_count > 3
                    else None,
                    Spawn(BrawlerBot, spacing=6),
                    Spawn(BrawlerBot, spacing=6),
                    Spawn(BrawlerBot, spacing=45),
                    Spawn(BrawlerBot, spacing=45)
                    if player_count > 1
                    else None,
                    Spawn(BrawlerBot, spacing=6),
                    Spawn(BrawlerBot, spacing=6),
                    Spawn(BrawlerBot, spacing=6)
                    if player_count > 2
                    else None,
                ],
            ),
            Wave(
                base_angle=60,
                entries=[
                    Spawn(BrawlerBot, spacing=40),
                    Spawn(TriggerBot, spacing=40),
                    Spawn(TriggerBot, spacing=40),
                    Spawn(TriggerBot, spacing=40),
                    Spawn(TriggerBot, spacing=40)
                    if player_count > 1
                    else None,
                ],
            ),
            Wave(
                base_angle=60,
                entries=[
                    Spawn(BomberBot, spacing=6),
                    Spawn(BomberBot, spacing=6),
                    Spawn(BomberBot, spacing=45),
                    Spawn(BomberBot, spacing=45)
                    if player_count > 1
                    else None,
                    Spawn(BomberBot, spacing=6)
                    if player_count > 3
                    else None,
                ],
            ),
            Wave(
                base_angle=60,
                entries=[
                    Spawn(BrawlerBot, spacing=40),
                    Spawn(BomberBot, spacing=40),
                    Spawn(BrawlerBot, spacing=40),
                    Spawn(BrawlerBot, spacing=40),
                    Spawn(BrawlerBotLite, spacing=40),
                ],
            ),
            Wave(
                base_angle=15,
                entries=[
                    Spawn(BomberBot, spacing=6),
                    Spawn(BomberBot, spacing=6),
                    Spawn(BomberBot, spacing=6),
                    Spawn(TriggerBot, spacing=6)
                    if player_count > 1
                    else None,
                    Spawn(BrawlerBot, spacing=6)
                    if player_count > 2
                    else None,
                ],
            ),
        ]

        # Let our main class set up powerups, start waves and such.
        super().on_begin(args)

        # Badge goal variables
        self._combo_kill_timer: dict[ba.Timer] = {}
        self._combo_counter: dict = {}

        # Update damage evasion badge goal information
        dmgtsh = str(self._damage_threshold)
        self._badge_text('nodamage',
                         desc=ba.Lstr(resource='explodinary.campaignBadge.nodmg.desc', subs=[('${DMG}', dmgtsh)]),
                         short_desc=ba.Lstr(resource='explodinary.campaignBadge.nodmg.s_desc', subs=[('${DMG}', dmgtsh)]),
                         )
        
        # Helpy Spawn
        self.spawn_helpy((-12, 4.8, 2.3))
        self._do_intro_cutscene()

    def _do_intro_cutscene(self):
        """ Does our level intro. """
        # Skip if we've already seen this cutscene / are in speedrun mode / have "skip cutscenes" enabled
        if self.has_done_cutscene('tb'):
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

        # Dialogue routine
        dkey = "explodinary.campaignDialogue.the_beginning."
        player_speakers = [dialogue.get_player_speaker(p) for p in self.players]; helpy_speaker = dialogue.SpeakerLib().helpy
        
        _skip_vote = skipvote.SkipVoteModule(skiptext=ba.Lstr(resource='explodinary.skipCutscene'), on_vote_end=self.reset)
        
        _dialogue_manager = dialogue.DialogueManager(finish_call = _end)
        _dialogue_manager.add_message([
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}00"), time=2.5, idle=1.5, fade=0.0, end_call=_dumb_spawn),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}01"), time=3.25, idle=1.3, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}02"), time=3.0, idle=1.0, fade=0.0, end_call=_powerups),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}03"), time=4, idle=1.8, fade=0.75, end_call=None),
        ])
        
        ba.timer(1.75, _dialogue_manager.start)

    def _end_wrapup(self):
        """ Does a post-end intro tip / timer management. """
        # Show once per session only.
        cd = ba.getsession().customdata
        if not cd.get('tip_tb', False):
            cd['tip_tb'] = True
            self.tips = [
                ba.GameTip(
                    'Use Cluster Bombs to cover a large area\n'
                    'with clusters quickly.',
                    icon=ba.gettexture('powerupClusterBombs'),
                    sound=ba.getsound('ding'),
                )
            ]
        ba.timer(3, ba.WeakCall(self._start_time_bonus_timer))
        ba.timer(0.8, self._show_tip)
        ba.timer(0.2, self._render_badges)

    def _do_end_cutscene(self, outcome: str):
        """ Does our end level cutscene. """
        self._cutscene_helpy.node.is_area_of_interest = True

        if self.has_done_cutscene('tbf', False):
            super().do_end(outcome)
            return
        
        # Dialogue routine
        dkey = "explodinary.campaignDialogue.the_beginning."
        player_speakers = [dialogue.get_player_speaker(p) for p in self.players]; helpy_speaker = dialogue.SpeakerLib().helpy
        
        # Extra funcs
        def _end():
            #_skip_vote.end()
            self.alt_do_end(outcome)    
        
        # Player names used when P1 introduces themselves / everyone else to Helpy
        player_names    = [p.getname() for p in self.players]
        nump            = len(player_names)
        extra = ba.Lstr(resource    = f"{dkey}"
                        f"e09s{'0' if nump < 2 else '1' if nump == 2 else '2'}",
                        
                        subs        = [
                            ('${NAME2}', '' if nump < 2 else player_names[1] if nump == 2 else ''.join([pname + (",⛔⛔⛔⛔ " if i != len(player_names[1:-1]) -1 else "⛔⛔") for i,pname in enumerate(player_names[1:-1])])),
                            ('${NAME3}', '' if nump < 3 else player_names[-1])
                        ]
                        )
        
        _skip_vote = skipvote.SkipVoteModule(skiptext=ba.Lstr(resource='explodinary.skipCutscene'), on_vote_end=_end)
        _dialogue_manager = dialogue.DialogueManager(finish_call = _end)
        
        _dialogue_manager.add_message([
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e00"),                    time=2, idle=1, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}e01"),   time=3, idle=1, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e02"),                    time=1, idle=0.5, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}e03"),   time=1, idle=1, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e04"),                    time=5, idle=1, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}e05"),   time=1, idle=0, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e06"),                    time=4, idle=0.5, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}e07"),   time=1, idle=1, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e08"),                    time=4, idle=1, fade=0.0, end_call=None),
            dialogue.DialogueMessage(player_speakers[0], text=ba.Lstr(resource=f"{dkey}e09",
                                                                      subs=[
                                                                          ('${NAME1}', player_names[0]),
                                                                          ('${EXTRA}', extra),
                                                                          ]),                               time=1, idle=1, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker,text=ba.Lstr(resource=f"{dkey}e10{''if nump<3 else'a'}"),time=2, idle=1, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}e11"),   time=1, idle=0.7, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e12"),                    time=6, idle=2, fade=0.0, end_call=None),
        ])
        
        _dialogue_manager.start()

    def do_end(self, outcome: str, delay: float = 0) -> None:
        if self._won: self._do_end_cutscene(outcome)
        else: super().do_end(outcome, delay)

    def _badge_define(self):
        """ Defines our badges. """
        k = 'explodinary.campaignBadge.tb.'
        # Speedrun
        self._badge_append( 
            'timetrial',
            ba.Lstr(resource=f'{k}n00'),
            ba.Lstr(resource=f'{k}d00'),
            '',
            'badgeSpeed',
        )
        # Triple kill
        self._badge_append(
            'triplekill',
            ba.Lstr(resource=f'{k}n01'),
            ba.Lstr(resource=f'{k}d01'),
            '',
            'badgeKills',
        )
        # Damage evasion
        self._badge_append(
            'nodamage',
            ba.Lstr(resource=f'{k}n02'),
            ba.Lstr(resource=f'{k}d02'),
            '',
            'badgeHP',
            True,
        )

    def _handle_kill_achievements(self, msg: SpazBotDiedMessage) -> None:
        """ Handles our triple kill badge goal. """
        killer = msg.killerplayer
        if not killer: return

        # Add 1 kill to our local counter (or create one if it doesn't exist.)
        try: self._combo_counter[killer] += 1
        except KeyError: self._combo_counter[killer] = 1

        # Clean and create a timer so we can reset our kill count after a second.
        self._combo_kill_timer[killer] = None
        self._combo_kill_timer[killer] = ba.Timer(1.0, lambda: self._kill_combo(killer))

        # Instance badge name
        badge: str = 'triplekill'

        # Did we reach 3 kills and it's our first time?
        if self._combo_counter[killer] == 3 and not self._badge_status(badge):
            # We achieved a triple kill! Update our badge display
            self._badge_update(badge, True)

    def _kill_combo(self, killer:str) -> None:
        # Took too long! Reset our combo kill counter.
        self._combo_counter[killer] = 0