from __future__ import annotations
from typing import Any

import ba
from explodinary.actor.bsespazbot import (
    BomberBot,
    ChargerBot,
    BrawlerBot,
    TriggerBot,
    BouncyBot,
    BrawlerBotPro,
    BomberBotPro,
)

from explodinary.campaign import (
    BSECampaignActivity,
    Wave,
    Spawn,
    Point,
)

from explodinary.lib import dialogue, skipvote
import random

from explodinary.actor.bsespazbot import SpazBotAttackedMessage

class GrottoGame(BSECampaignActivity):
    """ Third BSE Campaign Level. """

    name = 'Beyond The Grotto'

    def __init__(self, settings: dict):

        # Set our map and if we get our defs from the json file.
        settings['map'] = 'Grotto'
        settings['json'] = False

        super().__init__(settings)


    def _map_defs(self) -> dict:
        """ Map defs in case we opt-out of getting defs from our json file. """
        return {
            'spawn_center':     (-12, 6, -3),
            'tntspawnpos':      (0.0, 3.0, 2.1),
            'powerup_center':   (0, 4, -1),
            'powerup_spread':   (3, 2),
        }


    def on_transition_in(self) -> None:
        super().on_transition_in()
        
        # Cutscene confirmed.
        self._has_cutscene = True

        if self.has_done_cutscene('btg', False):
            self._spawn_center = (-1.15, 0.9, -2.7)
            
        self._music = ba.MusicType.GROTTO

    def on_begin(self) -> None:

        # Save some general variables.
        player_count = len(self.players)
        self._excluded_powerups = ['steampunk_bombs', 'toxic_bombs', 'vital_bombs', 'present', 'clouder_bombs', 'flutter_mines', 'fly_punch', 'dash']
        args: dict = {
            'first_spawn_type': ['lite_mines'],
            'tnt': False,
            'goal_time': '2m00s',
        }
        self._track_damage = 'nodamage'

        # Our main list of waves and events.
        self._waves = [
            Wave(
                entries=[
                    Spawn(ChargerBot, Point.TOP_HALF_RIGHT),
                    Spawn(ChargerBot, Point.TOP_HALF_LEFT),
                    Spawn(BrawlerBot, Point.TOP)
                    if player_count > 2
                    else None,
                    Spawn(BrawlerBot, Point.TOP_RIGHT),
                ]
            ),
            Wave(
                entries=[
                    Spawn(BomberBot, Point.BOTTOM),
                    Spawn(ChargerBot, Point.TOP),
                    Spawn(BomberBotPro, Point.BOTTOM_HALF_RIGHT),
                    Spawn(BomberBotPro, Point.BOTTOM_HALF_LEFT)
                    if player_count > 1
                    else None,
                    Spawn(BomberBot, Point.BOTTOM_RIGHT),
                    Spawn(BomberBot, Point.BOTTOM_LEFT)
                    if player_count > 2
                    else None,
                    Spawn(ChargerBot, Point.TOP_RIGHT)
                    if player_count > 3
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(BrawlerBotPro, Point.RIGHT),
                    Spawn(TriggerBot, Point.TOP_HALF_LEFT),
                    Spawn(BrawlerBotPro, Point.TOP),
                    Spawn(TriggerBot, Point.TOP_HALF_RIGHT),
                    Spawn(BrawlerBotPro, Point.LEFT)
                    if player_count > 1
                    else None,
                    Spawn(BrawlerBot, Point.TOP_RIGHT),
                    Spawn(BrawlerBot, Point.TOP_LEFT)
                    if player_count > 2
                    else None,
                    Spawn(TriggerBot, Point.RIGHT_UPPER)
                    if player_count > 3
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(BomberBot, Point.RIGHT),
                    Spawn(BomberBot, Point.LEFT),
                    Spawn(BouncyBot, Point.TOP)
                    if player_count > 1
                    else None,
                    Spawn(BomberBot, Point.TOP_LEFT),
                    Spawn(BomberBot, Point.TOP_RIGHT)
                    if player_count > 2
                    else None,
                    Spawn(BouncyBot, Point.TOP_HALF_LEFT)
                    if player_count > 3
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(ChargerBot, Point.RIGHT_UPPER),
                    Spawn(ChargerBot, Point.LEFT_UPPER),
                    Spawn(BrawlerBot, Point.TOP)
                    if player_count > 1
                    else None,
                    Spawn(BrawlerBotPro, Point.BOTTOM_HALF_LEFT),
                    Spawn(BrawlerBotPro, Point.BOTTOM_HALF_RIGHT)
                    if player_count > 2
                    else None,
                    Spawn(ChargerBot, Point.BOTTOM_LEFT)
                    if player_count > 3
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(ChargerBot, Point.RIGHT),
                    Spawn(ChargerBot, Point.LEFT),
                    Spawn(TriggerBot, Point.RIGHT_UPPER)
                    if player_count > 1
                    else None,
                    Spawn(TriggerBot, Point.TOP_HALF_RIGHT),
                    Spawn(TriggerBot, Point.TOP_HALF_LEFT)
                    if player_count > 2
                    else None,
                    Spawn(ChargerBot, Point.LEFT_LOWER)
                    if player_count > 3
                    else None,
                ]
            ),
        ]

        # Let our main class set up powerups, start waves and such.
        super().on_begin(args)

        # Badge goals variables
        self._litemine_enemy_hits: int = 0

        # Update damage evasion badge goal information
        self._damage_threshold = dmg = 500
        self._damage_threshold:int = int(((dmg*1.05)*player_count) + (dmg*0.2))
        
        dmgtsh = str(self._damage_threshold)
        self._badge_text('nodamage',
                         desc=ba.Lstr(resource='explodinary.campaignBadge.nodmg.desc', subs=[('${DMG}', dmgtsh)]),
                         short_desc=ba.Lstr(resource='explodinary.campaignBadge.nodmg.s_desc', subs=[('${DMG}', dmgtsh)]),
                         )
        
        # Helpy Spawn
        self.spawn_helpy((-10.8, 5.6, -3.8))
        ba.timer(1, self.hold_pos_helpy)
        
        self._do_intro_cutscene()

    def _do_intro_cutscene(self):
        """ Does our intro cutscene. """
        # Replace spawnpoint immediately!
        self._spawn_center = (-1.15, 0.9, -2.7)
        # Skip if we've already seen this cutscene / are in speedrun mode / have "skip cutscenes" enabled
        if self.has_done_cutscene('btg'):
            self._intro_cutscene_end(True)
            return
        
        # Disable player controls
        self._handle_controllers(False)
        
        # Extra functions
        def yeet():
            self.players_iscl(0)
            for i, player in enumerate([p for p in self.players if p.actor]):
                ba.timer(0.22 * i, ba.Call(
                    player.actor.node.handlemessage, 'impulse', player.actor.node.position[0], player.actor.node.position[1], player.actor.node.position[2],
                                    0, 0, 0,
                                    120*15, 1,
                                    0, 0,
                                    35, 12, 0
                    )
                )
                ba.timer((0.22 * i) + 0.1, ba.Call(
                    player.actor.node.handlemessage, 'impulse', player.actor.node.position[0], player.actor.node.position[1], player.actor.node.position[2],
                                    0, 0, 0,
                                    120*15, 1,
                                    0, 0,
                                    40, 2, 0
                    )
                )
        def _dumb_spawn()   : ba.timer(0.4, self._dumb_bot_spawn)
        def _post_fall()    :
            for player in (p for p in self.players if p.is_alive()):
                player.has_been_hurt = False
            self.players_iscl(1.0)
            def focus():
                self._bots._update()
                for bot in self._bots._bot_lists:
                    try     : bot[0].node.is_area_of_interest = True
                    except  : continue
            def unfocus():
                self._bots._update()
                for bot in self._bots._bot_lists:
                    try     : bot[0].node.is_area_of_interest = False
                    except  : continue
                self.theyclock = None
                
            self._dumb_bot_spawn()
            self.theyclock = ba.Timer(0.1, focus, repeat=True)
            ba.timer(7.5, unfocus)
        def _powerups()     : ba.timer(1.6, ba.WeakCall(self._start_spawning_stuff, 0, 1.2, 0, False))
        def a_little_help_here(): dialogue.DialogueMessage(the_shouters[1], text=ba.Lstr(resource=f"{dkey}05{'' if len(self.players) < 2 else 'a'}"), time=1.0, idle=1.5, fade=0.3, scale=0.44, offset=(85, 85), end_call=None).start()
        def _end():
            _skip_vote.end()
            self._intro_cutscene_end()

        # Dialogue routine
        dkey = "explodinary.campaignDialogue.beyond_the_grotto."
        player_speakers = [dialogue.get_player_speaker(p) for p in self.players]; helpy_speaker = dialogue.SpeakerLib().helpy
        
        the_dualers     = len(player_speakers) > 1
        the_shouters    = random.sample(player_speakers, 2) if the_dualers else [random.choice(player_speakers)]
        the_idlers      = 2.2 if the_dualers else 1.65
        the_callers     = ba.Call(ba.timer, 1.44, a_little_help_here) if the_dualers else None
        
        _skip_vote = skipvote.SkipVoteModule(skiptext=ba.Lstr(resource='explodinary.skipCutscene'), on_vote_end=self.reset)
        
        _dialogue_manager = dialogue.DialogueManager(finish_call = _end)
        _dialogue_manager.add_message([
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}00"),    time=1.75, idle=1.5, fade=0.0, end_call=ba.Call(ba.timer, 3.8, yeet)),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}01"),                     time=3.25, idle=1.3, fade=0.2, end_call=None),
            ('wait', 1.2),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}02"),    time=0.6, idle=1.1, fade=0.0, end_call=_post_fall),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}03"),                     time=1.6, idle=1.2, fade=0.0, end_call=the_callers),
            dialogue.DialogueMessage(the_shouters[0], text=ba.Lstr(resource=f"{dkey}04"),                   time=1.7, idle=the_idlers, fade=0.0, end_call=_powerups),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}06"),                     time=1.9, idle=1.2, fade=0.9, end_call=None),
        ])
        
        ba.timer(1.75, _dialogue_manager.start)
    
    def players_iscl(self, impact_scale: float = 1.0):
        """ Resets players' impact scale """
        for player in (p for p in self.players if p.actor):
            player.actor.impact_scale = impact_scale

    def _intro_cutscene_end(self, instant=False):
        """ Remove our players' god mode when finishing our cutscene. """
        self.players_iscl()
        return super()._intro_cutscene_end(instant)
    
    def _end_wrapup(self):
        # Show once per session only.
        cd = ba.getsession().customdata
        if not cd.get('tip_btg', False):
            cd['tip_btg'] = True
            self.tips = [
                ba.GameTip(
                    'Use Lite Mines to quickly make your enemies unconscious.\n'
                    'Works on enemies with shields too!',
                    icon=ba.gettexture('powerupSkyMines'),
                    sound=ba.getsound('ding'),
                )
            ]
        self._dumbify(True)
        ba.timer(3, ba.WeakCall(self._start_time_bonus_timer))
        ba.timer(0.8, self._show_tip)
        ba.timer(0.2, self._render_badges)

    def _do_end_cutscene(self, outcome: str):
        """ Does our end level cutscene. """
        if self.has_done_cutscene('btgf', False):
            super().do_end(outcome)
            return
        
        dkey = "explodinary.campaignDialogue.beyond_the_grotto."
        
        def _end():
            #_skip_vote.end()
            self.alt_do_end(outcome)
        
        player_speakers = [dialogue.get_player_speaker(p) for p in self.players]; helpy_speaker = dialogue.SpeakerLib().helpy
        
        _skip_vote = skipvote.SkipVoteModule(skiptext=ba.Lstr(resource='explodinary.skipCutscene'), on_vote_end=_end)
        
        _dialogue_manager = dialogue.DialogueManager(finish_call = _end)
        _dialogue_manager.add_message([
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}e00"),    time=1.8, idle=1.2, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e01"),                     time=0.3, idle=0.8, fade=0.6, end_call=None),
        ])
        
        _dialogue_manager.start()

    def do_end(self, outcome: str, delay: float = 0) -> None:
        if self._won:
            self._do_end_cutscene(outcome)
        else: super().do_end(outcome, delay)

    def _badge_define(self):
        """ Defines our badges. """
        k = 'explodinary.campaignBadge.btg.'
        # Speedrun
        self._badge_append(
            'timetrial',
            ba.Lstr(resource=f'{k}n00'),
            ba.Lstr(resource=f'{k}d00'),
            '',
            'badgeSpeed',
        )
        # Litemine kills
        self._badge_append(
            'liteminekills',
            ba.Lstr(resource=f'{k}n01'),
            ba.Lstr(resource=f'{k}d01'),
            '',
            'badgeLiteMine',
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

    def handlemessage(self, msg: Any) -> Any:
        """ Handling of messages for badges! """
        if isinstance(msg, SpazBotAttackedMessage):
            # Check whenever an enemy gets hurt with a lite-mine
            if msg.subtype == 'lite':
                # Increase and reward!
                self._litemine_enemy_hits += 1
                if self._litemine_enemy_hits == 3:
                    self._badge_update('liteminekills', True)

        else: return super().handlemessage(msg)