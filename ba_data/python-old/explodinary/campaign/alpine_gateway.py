from __future__ import annotations

import ba
from explodinary.actor.bsespazbot import (
    ChargerBot,
    SpazBotDiedMessage,
    StickyBot,
    BrawlerBot,
    TriggerBot,
    ExplodeyBot,
    WaiterBot,
    BrawlerBotProShielded,
    ChargerBotProShielded,
    TriggerBotProShielded,
    BrawlerBotPro,
    BomberBotProStaticShielded,
    BomberBotProStatic,
    MellyBot,
    NoirBot,
)

from explodinary.campaign import (
    BSECampaignActivity,
    Wave,
    Spawn,
    Point,
)
from bastd.actor.bomb import get_bomb_types

from explodinary.lib import dialogue, skipvote
import random

class AlpineGatewayGame(BSECampaignActivity):
    """ Fourth BSE Campaign Level. """

    name = 'Alpine Gateway'
    # If I got a dollar for each time I called this level "Alpine Getaway", I would have 15. -T 

    def __init__(self, settings: dict):

        # Set our map and if we get our defs from the json file.
        settings['map'] = 'Alpine Gateway'
        settings['json'] = False
        self._cutscene_helpy = None

        super().__init__(settings)


    def _map_defs(self) -> dict:
        """ Map defs in case we opt-out of getting defs from our json file. """
        return {
            'spawn_center':     (-1, 3, -2),
            'tntspawnpos':      (-7, 3.2, -8),
            'powerup_center':   (0, 4, -2),
            'powerup_spread':   (6, 3.12),
        }


    def on_transition_in(self) -> None:
        super().on_transition_in()

        # This level does in fact have a cutscene
        self._has_cutscene = True
        
        # Level music
        self._music = ba.MusicType.ALPINE

    def on_begin(self) -> None:

        # Save some general variables.
        player_count = len(self.players)
        self._excluded_powerups = ['steampunk_bombs', 'clouder_bombs', 'flutter_mines', 'vital_bombs', 'fly_punch', 'dash']
        args: dict = {
            'first_spawn_type': ['present'],
            'tnt': True,
            'goal_time': '2m10s',
        }

        # Our main list of waves and events.
        self._waves = [
            Wave(
                entries=[
                    Spawn(BrawlerBot, Point.RIGHT),
                    Spawn(BrawlerBot, Point.RIGHT_UPPER),
                    Spawn(BrawlerBot, Point.RIGHT_UPPER_MORE),
                    Spawn(BrawlerBot, Point.LEFT),
                    Spawn(BrawlerBot, Point.LEFT_UPPER),
                    Spawn(BrawlerBot, Point.LEFT_UPPER_MORE),
                    Spawn(BrawlerBot, Point.TOP)
                    if player_count > 2
                    else None,
                    Spawn(BrawlerBot, Point.TOP_HALF_RIGHT),
                ]
            ),
            Wave(
                entries=[
                    Spawn(BomberBotProStatic, Point.TURRET_TOP_MIDDLE_RIGHT),
                    Spawn(BrawlerBotPro, Point.TOP),
                    Spawn(BomberBotProStatic, Point.TURRET_TOP_MIDDLE_LEFT),
                    Spawn(BrawlerBot, Point.TOP_HALF_RIGHT)
                    if player_count > 1
                    else None,
                    Spawn(BrawlerBotPro, Point.RIGHT_UPPER)
                    if player_count > 2
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(ExplodeyBot, Point.RIGHT_UPPER),
                    Spawn(ChargerBot, Point.RIGHT),
                    Spawn(TriggerBotProShielded, Point.TOP),
                    Spawn(TriggerBotProShielded, Point.TOP_HALF_RIGHT)
                    if player_count > 1
                    else None,
                    Spawn(TriggerBotProShielded, Point.TOP_RIGHT)
                    if player_count > 2
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(WaiterBot, Point.TOP),
                    Spawn(StickyBot, Point.TOP_HALF_RIGHT),
                    Spawn(StickyBot, Point.TOP_RIGHT),
                    Spawn(MellyBot, Point.TURRET_TOP_MIDDLE_LEFT)
                    if player_count > 1
                    else None,
                    Spawn(StickyBot, Point.RIGHT_LOWER),
                    Spawn(WaiterBot, Point.RIGHT_UPPER_MORE),
                    Spawn(MellyBot, Point.TURRET_TOP_MIDDLE_RIGHT)
                    if player_count > 2
                    else None,
                    Spawn(WaiterBot, Point.RIGHT),
                    Spawn(StickyBot, Point.RIGHT_UPPER),
                    Spawn(MellyBot, Point.TURRET_TOP_MIDDLE)
                ]
            ),
            Wave(
                entries=[
                    Spawn(NoirBot, Point.RIGHT_UPPER),
                    Spawn(ExplodeyBot, Point.TOP_HALF_RIGHT),
                    Spawn(ChargerBotProShielded, Point.BOTTOM),
                    Spawn(ChargerBotProShielded, Point.BOTTOM_HALF_RIGHT)
                    if player_count > 1
                    else None,
                    Spawn(TriggerBot, Point.BOTTOM_HALF_LEFT)
                    if player_count > 2
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(BomberBotProStaticShielded, Point.TURRET_TOP_MIDDLE),
                    Spawn(BomberBotProStaticShielded, Point.TURRET_TOP_MIDDLE_LEFT),
                    Spawn(BrawlerBotPro, Point.RIGHT),
                    Spawn(ChargerBotProShielded, Point.BOTTOM),
                    Spawn(BrawlerBotPro, Point.LEFT)
                    if player_count > 1
                    else None,
                    Spawn(BrawlerBotProShielded, Point.BOTTOM_HALF_RIGHT),
                    Spawn(BomberBotProStaticShielded, Point.TURRET_TOP_MIDDLE_RIGHT)
                    if player_count > 2
                    else None,
                ]
            ),
        ]

        # Let our main class set up powerups, start waves and such.
        super().on_begin(args)

        # Badge goal variables
        self._kill_by_present: int = 0
        self._kill_by_tnt: int = 0

        self._do_intro_cutscene()

    def _do_intro_cutscene(self):
        """ Does our level intro. """
        # Skip if we've already seen this cutscene / are in speedrun mode / have "skip cutscenes" enabled
        if self.has_done_cutscene('ag'):
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
        # Spawn helpy in cutscene only.
        self.spawn_helpy((-0.1, 3.1, -1.9))

        # Extra functions
        def bloopbloop()    :
            ba.timer(3.7, self.badoink_helpy)
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}08"),                     time=3.7, idle=0.0, fade=1.2, scale=0.44, offset=(85, 85), end_call=ba.Call(ba.timer, 1.2, wehidinhere)).start()
        def wehidinhere()   : dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}10"),   time=1.6, idle=1.1, fade=0.6, scale=0.44, offset=(85, 85), end_call=None).start()

        # Dialogue routine
        dkey = "explodinary.campaignDialogue.alpine_gateway."
        player_speakers = [dialogue.get_player_speaker(p) for p in self.players]; helpy_speaker = dialogue.SpeakerLib().helpy
        
        _skip_vote = skipvote.SkipVoteModule(skiptext=ba.Lstr(resource='explodinary.skipCutscene'), on_vote_end=self.reset)
        
        _dialogue_manager = dialogue.DialogueManager(finish_call = _end)
        _dialogue_manager.add_message([
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}00"),                     time=1.7, idle=1.4, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}01"),    time=4.5, idle=1.3, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}02"),                     time=4.9, idle=1.5, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}03"),    time=3.1, idle=2.0, fade=0.0, end_call=ba.Call(self._dumb_bot_spawn, 1.9)),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}04"),                     time=0.6, idle=1.1, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}05"),    time=1.6, idle=1.3, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}06"),                     time=0.9, idle=1.2, fade=0.0, end_call=ba.Call(ba.timer, 0.6, bloopbloop)),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}07"),    time=1.8, idle=1.3, fade=0.0, end_call=ba.Call(self._start_spawning_stuff, 3.8, 7.8, 2.9, False)),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}09"),    time=3.6, idle=2.75, fade=0.6, end_call=None),
        ])
        
        ba.timer(0.5, _dialogue_manager.start)

    def _end_wrapup(self):
        # Show once per session only.
        cd = ba.getsession().customdata
        if not cd.get('tip_ag', False):
            cd['tip_ag'] = True
            self.tips = [
                ba.GameTip(
                    'Use Unwanted Present to quickly wipe out groups of enemies.',
                    icon=ba.gettexture('powerupPresent'),
                    sound=ba.getsound('confetti'),
                )
            ]
        self._dumbify(True)
        ba.timer(3, ba.WeakCall(self._start_time_bonus_timer))

        ba.timer(0.8, self._show_tip)
        ba.timer(0.2, self._render_badges)

    def _do_end_cutscene(self, outcome: str):
        """ Does our end level cutscene. """
        if self.has_done_cutscene('agf', False):
            super().do_end(outcome)
            return
        
        dkey = "explodinary.campaignDialogue.alpine_gateway."
        
        # Spawn helpy in cutscene only.
        self.spawn_helpy((6.9, 3.1, -1.9), True)
        
        def _end():
            #_skip_vote.end()
            self.alt_do_end(outcome)
        
        player_speakers = [dialogue.get_player_speaker(p) for p in self.players]; helpy_speaker = dialogue.SpeakerLib().helpy
        
        _skip_vote = skipvote.SkipVoteModule(skiptext=ba.Lstr(resource='explodinary.skipCutscene'), on_vote_end=_end)
        
        _dialogue_manager = dialogue.DialogueManager(finish_call = _end)
        _dialogue_manager.add_message([
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e00"),                    time=3.25, idle=1.5, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}e01"),   time=1.4, idle=1, fade=0.6, end_call=None),
        ])
        
        _dialogue_manager.start()
        
    def do_end(self, outcome: str, delay: float = 0) -> None:
        if self._won:
            self._do_end_cutscene(outcome)
        else: super().do_end(outcome, delay)

    def _badge_define(self):
        """ Defines our badges. """
        k = 'explodinary.campaignBadge.ag.'
        # Speedrun
        self._badge_append(
            'timetrial',
            ba.Lstr(resource=f'{k}n00'),
            ba.Lstr(resource=f'{k}d00'),
            '',
            'badgeSpeed',
        )
        # Present kills
        self._badge_append(
            'presentkills',
            ba.Lstr(resource=f'{k}n01'),
            ba.Lstr(resource=f'{k}d01'),
            '',
            'badgePresent',
        )
        # TNT kills
        self._badge_append(
            'tntkills',
            ba.Lstr(resource=f'{k}n02'),
            ba.Lstr(resource=f'{k}d02'),
            '',
            'badgeTNT',
        )

    def _handle_kill_achievements(self, msg: SpazBotDiedMessage) -> None:
        """ Handle TNT & Present kills for tasks. """
        # Set some basic variables
        last = msg.spazbot.last_attacked_type
        has_killer = msg.killerplayer
        # Return if a last hit type doesn't exist or there's no kiler
        if not last: return

        # Handle our present kills.
        if has_killer and last == ('explosion', 'present'):
            # Count and award!
            self._kill_by_present += 1
            if self._kill_by_present == 7:
                self._badge_update('presentkills', True)

        # Handle our TNT kills.
        elif last[0] == 'explosion' and last[1] in get_bomb_types(False, True, False, False, False):
            # Increase and recompense!
            self._kill_by_tnt += 1
            if self._kill_by_tnt == 1:
                self._badge_update('tntkills', True)