from __future__ import annotations

import ba
from explodinary.actor.bsespazbot import (
    BomberBot,
    BrawlerBot,
    SpazBotDiedMessage,
    TriggerBot,
    BomberBotPro,
    BrawlerBotPro,
    BomberBotPro,
    MellyBot,
    ToxicBot,
)

from explodinary.campaign import (
    BSECampaignActivity,
    Wave,
    Spawn,
    Point,
)

from explodinary.lib import dialogue, skipvote
import random

from bastd.gameutils import SharedObjects

class MysteriousSwampGame(BSECampaignActivity):
    """ Second BSE Campaign Level. """

    name = 'Mysterious Swamp'

    def __init__(self, settings: dict):

        # Set our map and if we get our defs from the json file.
        settings['map'] = 'Mysterious Swamp'
        settings['json'] = False

        super().__init__(settings)


    def _map_defs(self) -> dict:
        """ Map defs in case we opt-out of getting defs from our json file. """
        return {
            'spawn_center':     (-4, 2.5, -3),
            'tntspawnpos':      (-6.36367, 3.54908, -4.63826),
            'powerup_center':   (0, 4, -3.65),
            'powerup_spread':   (4.1, 3.21),
        }


    def on_transition_in(self) -> None:
        super().on_transition_in()

        # This level has a cutscene!
        self._has_cutscene = True

        self._black_screen: ba.Node | None = None
        self._default_tints: dict | None = None
    
        # Ready some materials for our boat region.
        self._shared = shared = SharedObjects.get()

        self._boat_region = ba.Material()
        self._boat_region.add_actions(
            conditions=('they_have_material', shared.player_material),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                (
                    'call',
                    'at_connect',
                    ba.Call(self.boat_region, True),
                ),
                (
                    'call',
                    'at_disconnect',
                    ba.Call(self.boat_region, False),
                ),
            ),
        )
        
        # Level music
        self._music = ba.MusicType.SWAMP
        self._helpy_came = False # :flushed:


    def on_begin(self) -> None:

        # Save some general variables.
        player_count = len(self.players)
        self._excluded_powerups = ['steampunk_bombs', 'clouder_bombs', 'flutter_mines', 'vital_bombs', 'present', 'lite_mines', 'fly_punch', 'dash']
        args: dict = {
            'first_spawn_type': ['toxic_bombs'],
            'tnt': True,
            'goal_time': '1m40s',
            'showScoreboard': False,
        }

        # Our main list of waves and events.
        self._waves = [
            Wave(
                entries=[
                    Spawn(ToxicBot, Point.RIGHT_UPPER_MORE),
                    Spawn(ToxicBot, Point.RIGHT_UPPER)
                    if player_count > 2
                    else None,
                    Spawn(ToxicBot, Point.RIGHT_UPPER),
                ]
            ),
            Wave(
                entries=[
                    Spawn(BomberBot, Point.RIGHT_UPPER_MORE),
                    Spawn(BrawlerBot, Point.TOP),
                    Spawn(BrawlerBot, Point.RIGHT_LOWER),
                    Spawn(BrawlerBot, Point.TOP_HALF_RIGHT)
                    if player_count > 1
                    else None,
                    Spawn(BomberBotPro, Point.RIGHT_UPPER)
                    if player_count > 2
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(BomberBotPro, Point.RIGHT_UPPER),
                    Spawn(TriggerBot, Point.RIGHT),
                    Spawn(TriggerBot, Point.TOP)
                    if player_count > 1
                    else None,
                    Spawn(TriggerBot, Point.TOP_HALF_RIGHT)
                    if player_count > 2
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(MellyBot, Point.TOP),
                    Spawn(MellyBot, Point.TOP_HALF_RIGHT)
                    if player_count > 1
                    else None,
                    Spawn(BrawlerBot, Point.TOP_HALF_LEFT),
                    Spawn(BrawlerBot, Point.BOTTOM_LEFT)
                    if player_count > 2
                    else None,
                    Spawn(BrawlerBot, Point.TOP),
                    Spawn(MellyBot, Point.RIGHT_UPPER),
                ]
            ),
            Wave(
                entries=[
                    Spawn(TriggerBot, Point.RIGHT_UPPER),
                    Spawn(TriggerBot, Point.TOP_HALF_LEFT),
                    Spawn(ToxicBot, Point.BOTTOM),
                    Spawn(ToxicBot, Point.BOTTOM_HALF_RIGHT)
                    if player_count > 1
                    else None,
                    Spawn(TriggerBot, Point.BOTTOM_HALF_LEFT)
                    if player_count > 2
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(ToxicBot, Point.RIGHT_UPPER),
                    Spawn(BrawlerBotPro, Point.TOP_HALF_LEFT),
                    Spawn(BrawlerBotPro, Point.BOTTOM),
                    Spawn(BrawlerBotPro, Point.BOTTOM_HALF_LEFT)
                    if player_count > 1
                    else None,
                    Spawn(BrawlerBotPro, Point.BOTTOM_HALF_RIGHT)
                    if player_count > 2
                    else None,
                ]
            ),
        ]

        # Let our main class set up powerups, start waves and such.
        super().on_begin(args)

        # Create boat region for badge goal.
        boatzone = [self._boat_region, self._shared.region_material]
        ba.newnode(
            'region',
            attrs={
                'position': (-12.0, 2.25, -3.3),
                'scale': (1.5, 1.5, 1.5),
                'type': 'sphere',
                'materials': boatzone,
            },
        )

        gln = self._globalsnode
        self._default_tints = {
            'tint': gln.tint,
            'amb': gln.ambient_color,
            'v_in': gln.vignette_inner,
            'v_out': gln.vignette_outer,
        }

        self.spawn_helpy((-10.9, 1.6, -3.25))
        ba.timer(1, self.hold_pos_helpy)
        self._do_intro_cutscene()

        # Badge variables
        self._poisoned_kills: int = 0

    def _inv_flashbang(self):
        """ Covers our screen in darkness """
        # We do it this way so online clients get the memo too
        # (usually setting the value dry may have them skip the packet)
        ba.animate_array(self._globalsnode, 'vignette_inner', 3, {
            0: (0,0,0),
            1: (0,0,0),
        })
        ba.animate_array(self._globalsnode, 'vignette_outer', 3, {
            0: (0,0,0),
            1: (0,0,0),
        })
        self._black_screen = ba.newnode(
            'image',
            attrs={
                'fill_screen': True,
                'texture': ba.gettexture('white'),
                'tilt_translate': -0.3,
                'has_alpha_channel': False,
                'color': (0, 0, 0),
                'opacity': 0,
            }
        )
        ba.animate(self._black_screen, 'opacity', {
            0: 0,
            0.25: 1,
        })

    def _reveal_screen(self):
        """ Reveals the screen """
        try: 
            # If this fails, we somehow managed to run this function before _inv_flashbang?
            self._black_screen.opacity
        except AttributeError:
            ba.raise_exception('Need to run "self._inv_flashbang" first!')

        ba.animate(self._black_screen, 'opacity', {
            0: 1,
            1.25: 0,
        })
        # We do it this way so online clients get the memo too
        # (usually setting the value dry may have them skip the packet)
        ba.animate_array(self._globalsnode, 'vignette_inner', 3, {
            0: (0,0,0),
            0.15: self._default_tints['v_in'],
            1.15: self._default_tints['v_in'],
        })
        ba.animate_array(self._globalsnode, 'vignette_outer', 3, {
            0: (0,0,0),
            0.15: self._default_tints['v_out'],
            1.15: self._default_tints['v_out'],
        })

    def _do_intro_cutscene(self):
        """ Does our level intro. """
        # Skip if we've already seen this cutscene / are in speedrun mode / have "skip cutscenes" enabled
        if self.has_done_cutscene('ms'):
            self._intro_cutscene_end(True)
            return

        # Disable player controls
        self._handle_controllers(False)
        # Hide stuff!
        self._inv_flashbang()

        # Dialogue routine
        dkey = "explodinary.campaignDialogue.mysterious_swamp."
        player_speakers = [dialogue.get_player_speaker(p) for p in self.players]; helpy_speaker = dialogue.SpeakerLib().helpy
        
        # Extra variables
        self.swimsfx = ba.newnode(
            'sound', attrs={
                'sound' : ba.getsound('waterboardLoop'),
                'volume': 0.75,
                'loop'  : True,
                'positional': False
            }
        )
        self.theyclock: ba.Timer | None = None
        
        # Extra functions
        def arghh(): dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}05"), time=1.0, idle=1.1, fade=0.3, scale=0.44, offset=(85, 85), end_call=None).start()
        def balloonio(): dialogue.DialogueMessage(idea_guy, text=ba.Lstr(resource=f"{dkey}11"), time=4.65, idle=1.0, fade=1.5, scale=0.44, offset=(85, 85), end_call=None).start()
        def uncareful():
            ba.animate(self.swimsfx, 'volume', {
                0: 0.75,
                0.77: 2.1,
                1: 0
            })
            ba.timer(2.0, self.swimsfx.delete)
            ba.playsound(ba.getsound('helpyMessesUpTheBoatSound'), volume=1.2)
        def great(): dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}09"), time=1.0, idle=0, fade=0.75, scale=0.44, offset=(85, 85), end_call=all_faint).start()
        def reveal():
            self._reveal_screen()
            ba.timer(0.8, great)
        def all_faint():
            for i,player in enumerate(self.players):
                if not player.actor: return
                ba.timer(0.25 * (i*1.45), ba.Call(player.actor.node.handlemessage, 'knockout', 3 * 1000))
        def _powerups(): self._start_spawning_stuff(1.77,5.77,2.5,False)
        def _they():
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
        def _end():
            _skip_vote.end()
            self._intro_cutscene_end()

        _skip_vote = skipvote.SkipVoteModule(skiptext=ba.Lstr(resource='explodinary.skipCutscene'), on_vote_end=self.reset)

        _dialogue_manager = dialogue.DialogueManager(finish_call = _end)
        idea_guy = random.choice(player_speakers)
        _dialogue_manager.add_message([
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}00"),                     time=2.1, idle=1.25, fade=0.3, end_call=None),
            ('wait', 2.25),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}01"),    time=2.0, idle=1.65, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}02"),                     time=4.0, idle=1.2, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}03"),    time=0.2, idle=0.6, fade=0.0, end_call=ba.Call(ba.timer ,1.3, arghh)),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}04"),                     time=1.25, idle=2.2, fade=0.3, end_call=None),
            ('wait', 1.9),
            ('call', ba.Call(ba.timer, 0.77, uncareful)),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}06"),    time=4.8, idle=0.7, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}07"),                     time=2.0, idle=1.2, fade=0.3, end_call=reveal),
            ('wait', 0.76),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}08"),                     time=2.1, idle=0.5, fade=0.0, end_call=ba.Call(ba.timer ,2.15, balloonio)),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}10"),                     time=5.25, idle=1.25, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}12"),                     time=7.15, idle=1.25, fade=0.0, end_call=None),
            dialogue.DialogueMessage(idea_guy, text=ba.Lstr(resource=f"{dkey}13"),                          time=1.75, idle=1.1, fade=0.0, end_call=_they),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}14"),                     time=2.0, idle=1.5, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}15"),    time=2.5, idle=1.45, fade=0.0, end_call=_powerups),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}16"),                     time=4.12, idle=1.25, fade=0.75, end_call=None),
        ])
        
        ba.timer(0.5, _dialogue_manager.start)

    def _end_wrapup(self):
        # Show once per session only.
        cd = ba.getsession().customdata
        if not cd.get('tip_ms', False):
            cd['tip_ms'] = True
            self.tips = [
                ba.GameTip(
                        'Use Toxic Bombs to poison your enemies\n'
                        'and make them more vulnerable to damage.',
                        icon=ba.gettexture('powerupToxicBombs'),
                        sound=ba.getsound('toxicAcid'),
                )
            ]
        self._args['showScoreboard'] = True
        self._show_scoreboard_info()
        ba.timer(3, ba.WeakCall(self._start_time_bonus_timer))
        ba.timer(0.8, self._show_tip)
        ba.timer(0.2, self._render_badges)

    def _update_waves(self):
        """ We make our Helpy speak when in the winning sequence. """
        super()._update_waves()
        
        if self._won and not self._helpy_came:
            self._helpy_came = True
            ba.timer(1.2, self._helpy_come_here)
            
    def _helpy_come_here(self):
            self._cutscene_helpy.node.is_area_of_interest = True
            helpy_speaker = dialogue.SpeakerLib().helpy
            _dialogue_manager = dialogue.DialogueManager()
            _dialogue_manager.add_message( dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource="explodinary.campaignDialogue.mysterious_swamp.e00"), time=1.65, idle=1.2, fade=0.6, end_call=None), )
            _dialogue_manager.start()
        
    def do_end(self, outcome: str, delay: float = 0) -> None:
        super().do_end(outcome, delay)

    def _badge_define(self):
        """ Defines our badges. """
        k = 'explodinary.campaignBadge.ms.'
        # Speedrun
        self._badge_append(
            'timetrial',
            ba.Lstr(resource=f'{k}n00'),
            ba.Lstr(resource=f'{k}d00'),
            '',
            'badgeSpeed',
        )
        # Poison kills
        self._badge_append(
            'poisonkills',
            ba.Lstr(resource=f'{k}n01'),
            ba.Lstr(resource=f'{k}d01'),
            '',
            'badgeToxic',
        )
        # Boat Escape
        self._badge_append(
            'getintheboat',
            ba.Lstr(resource=f'{k}n02'),
            ba.Lstr(resource=f'{k}d02'),
            '',
            'badgeBoat',
        )

    def boat_region(self, collide: bool) -> None:
        """ Our boat region handler.
            Grants our boat badge if we collide at the end. """
        if self._won and collide and not self._badge_status('getintheboat'):
            self._badge_update('getintheboat', True)

    def _handle_kill_achievements(self, msg: SpazBotDiedMessage) -> None:
        """ Handles our poison kill badge goal. """
        has_killer = msg.killerplayer

        # Only accept kills performed by players
        if has_killer and msg.spazbot._is_toxic:
            # Counting and rewarding!
            self._poisoned_kills += 1
            if self._poisoned_kills == 3:
                self._badge_update('poisonkills', True)
