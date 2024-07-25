from __future__ import annotations

import ba
from explodinary.actor.bsespazbot import (
    ChargerBot,
    BomberBot,
    BrawlerBot,
    ExplodeyBot,
    ExplodeyBotShielded,
    FrostyBot,
    FrostyBotPro,
    FrostyBotProShielded,
    BrawlerBotProShielded,
    BrawlerBotPro,
    BomberBotProShielded,
    NoirBot,
    SpazBotDiedMessage,
    ToxicBot,
    GolemBot,
)

from explodinary.campaign import (
    BSECampaignActivity,
    Wave,
    Spawn,
    Delay,
)

import math, random
from explodinary.custom.particle import bseVFX
from explodinary.actor.bsespazbot import SpazBotSet
from explodinary.actor import bsespawner
from explodinary.lib.boss import BossHealthbar

from explodinary.lib import dialogue, skipvote

class MountChillGame(BSECampaignActivity):
    """ Fourth BSE Campaign Level. """

    name = 'Mount Chill'

    def __init__(self, settings: dict):

        # Set our map and if we get our defs from the json file.
        settings['map'] = 'Mount Chill'
        settings['json'] = False
        
        self._boss_wave: int = 8

        super().__init__(settings)


    def _map_defs(self) -> dict:
        """ Map defs in case we opt-out of getting defs from our json file. """
        return {
            'spawn_center':     (1, 3, -2),
            'tntspawnpos':      (0.59646, 3.5, -5.45602),
            'powerup_center':   (0, 4, -1),
            'powerup_spread':   (3, 2),
        }


    def on_transition_in(self) -> None:
        super().on_transition_in()

        # Cutscene!
        self._has_cutscene = True

        self._black_screen: ba.Node | None = None
        self._default_tints: dict | None = None
        
        # Music
        self._music = ba.MusicType.MOUNT_CHILL

    def on_begin(self) -> None:

        # Save some general variables.
        player_count = len(self.players)
        self._excluded_powerups = ['clouder_bombs', 'flutter_mines', 'vital_bombs', 'fly_punch', 'dash']
        args: dict = {
            'first_spawn_type': ['steampunk_bombs'],
            'tnt': True,
            'goal_time': '3m25s',
            'radial_spawn_y': 2.75,
        }

        # Our main list of waves and events.
        self._waves = [
            Wave(
                base_angle=-120,
                entries=[
                    Spawn(FrostyBot, spacing=22),
                    Spawn(FrostyBot, spacing=22),
                    Spawn(BrawlerBotPro if player_count > 1 else BrawlerBot, spacing=180),
                    Spawn(BrawlerBotPro, spacing=40)
                    if player_count > 1
                    else None,
                    Spawn(FrostyBot, spacing=55)
                    if player_count > 2
                    else None,
                    Spawn(BrawlerBotPro, spacing=60)
                    if player_count > 2
                    else None,
                    Spawn(BrawlerBotPro, spacing=60)
                    if player_count > 3
                    else None,
                ],
            ),
            Wave(
                base_angle=-180,
                entries=[
                    Spawn(BrawlerBot, spacing=20),
                    Spawn(ChargerBot, spacing=80),
                    Spawn(BrawlerBot, spacing=20),
                    Spawn(ChargerBot, spacing=80),
                    Spawn(BrawlerBot, spacing=20)
                    if player_count > 2
                    else None,
                    Spawn(ChargerBot, spacing=80)
                    if player_count > 2
                    else None,
                    Spawn(FrostyBotPro if player_count > 1 else FrostyBot, spacing=50),
                    Spawn(FrostyBotPro if player_count > 2 else FrostyBot, spacing=15),
                    Spawn(FrostyBotProShielded, spacing=15)
                    if player_count > 3
                    else None,
                ],
            ),
            Wave(
                base_angle=55,
                entries=[
                    Spawn(ExplodeyBot, spacing=77),
                    Delay(2),
                    Spawn(ExplodeyBot, spacing=77),
                    Delay(1.5),
                    Spawn(ExplodeyBotShielded if player_count > 1 else ExplodeyBot, spacing=77),
                    Delay(1.25),
                    Spawn(ExplodeyBotShielded if player_count > 2 else ExplodeyBot, spacing=77),
                    Delay(1),
                    Spawn(ExplodeyBotShielded if player_count > 3 else ExplodeyBot, spacing=77)
                    if player_count > 1
                    else None,
                ],
            ),
            Wave(
                base_angle=12,
                entries=[
                    Spawn(BomberBotProShielded, spacing=66),
                    Spawn(ToxicBot, spacing=66),
                    Delay(1.2),
                    Spawn(FrostyBotPro, spacing=66),
                    Spawn(FrostyBotPro, spacing=66)
                    if player_count > 1
                    else None,
                    Spawn(BomberBotProShielded, spacing=50)
                    if player_count > 3
                    else None,
                ],
            ),
            Wave(
                base_angle=180,
                entries=[
                    Spawn(BrawlerBotPro, spacing=66),
                    Spawn(BomberBot, spacing=30),
                    Delay(2),
            
                    Spawn(BrawlerBotProShielded if player_count > 2 else BrawlerBotPro, spacing=66),
                    Spawn(BomberBot, spacing=30),
                    Delay(2)
                    if player_count > 2
                    else None,
            
                    Spawn(BrawlerBotProShielded if player_count > 3 else BrawlerBotPro, spacing=66)
                    if player_count > 2
                    else None,
                    Spawn(BomberBot, spacing=30)
                    if player_count > 2
                    else None,
                ]
            ),
            Wave(
                base_angle=20,
                entries=[
                    Spawn(ChargerBot, spacing=122),
                    Spawn(ChargerBot, spacing=122),
                    Spawn(ChargerBot, spacing=55),
                    Spawn(NoirBot, spacing=55),
                    Spawn(NoirBot, spacing=55),
                    Spawn(NoirBot, spacing=55)
                    if player_count > 1
                    else None,
                    Spawn(NoirBot, spacing=55)
                    if player_count > 2
                    else None,
                    Spawn(NoirBot, spacing=55)
                    if player_count > 3
                    else None,
                ],
            ),
            Wave(
                base_angle=-55,
                entries=[
                    Spawn(FrostyBotPro, spacing=15),
                    Spawn(FrostyBotPro, spacing=30),
                    Spawn(FrostyBotProShielded if player_count > 1 else FrostyBotPro, spacing=45),
                    Spawn(FrostyBotProShielded if player_count > 2 else FrostyBotPro, spacing=60),
                    Spawn(FrostyBotProShielded if player_count > 3 else FrostyBotPro, spacing=75)
                    if player_count > 1
                    else None,
                    Spawn(FrostyBotPro, spacing=90)
                    if player_count > 2
                    else None,
                    Spawn(FrostyBotPro, spacing=105)
                    if player_count > 3
                    else None,
                ],
            ),
            Wave(
                base_angle=0,
                entries=[
                    #Replaced by summon_boss
                    #Spawn(GolemBot, spacing=0),
                    Delay(2.5),
                    Spawn(FrostyBot, spacing=124),
                    Spawn(FrostyBot, spacing=124),
                    Spawn(FrostyBot, spacing=124)
                    if player_count > 2
                    else None,
                    Spawn(FrostyBot, spacing=124)
                    if player_count > 3
                    else None,
                ],
            ),
        ]

        # Let our main class set up powerups, start waves and such.
        super().on_begin(args)

        # Some extra snowy variables.
        self._snow_timer: ba.Timer | None = ba.Timer(0.12, self.do_snow, repeat=True)
        self._blizzard_sound: ba.Node | None = ba.newnode(
                type='sound',
                attrs={
                    'sound': ba.getsound('blizzardAmbience'),
                    'positional': False,
                    'music': True,
                    'volume': 0,
                    'loop': True,
                },
            )
        
        # Particles
        c = self.map.get_def_bound_box('map_bounds')
        self._stage_ceiling = [(c[0],c[4]-2,c[2]),(c[3],c[4]-2,c[5])]

        # Badge variables
        self._steam_bomb_kills: int = 0
        self._snowball_kill: bool = False

        # Cutscene variables
        gln = self._globalsnode
        self._default_tints = {
            'tint': gln.tint,
            'ambient_color': gln.ambient_color,
            'vignette_inner': gln.vignette_inner,
            'vignette_outer': gln.vignette_outer,
        }
        self._do_intro_cutscene()

    def _do_intro_cutscene(self):
        """ Does our level intro. """
        # Skip if we've already seen this cutscene / are in speedrun mode / have "skip cutscenes" enabled
        if self.has_done_cutscene('mc'):
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
        
        # Helpy routine
        self.spawn_helpy((-2.2, 2.2, -2.8))
        self.helpy_move(1, 0.1, True)
        ba.timer(1.1, lambda: self.helpy_move(-0.21, 0, False))
        ba.timer(1.7, lambda: self.helpy_move(-0.1, 0, jump = True))
        ba.timer(2.2, lambda: self.helpy_move(0, 0, jump = True))
        ba.timer(2.8, lambda: self.helpy_move(0, 0, jump = True))
        ba.timer(3.5, lambda: self.helpy_move(-0.05, 0, jump = True))
        ba.timer(4.1, lambda: self.helpy_move(0, 0, jump = True))

        # Teleport our players to set spots for this cutscene.
        pls = self.players
        try:
            pls[0].actor.node.handlemessage(ba.StandMessage((-4.0-1.5,  2.2,  -3.1), 90))
            pls[1].actor.node.handlemessage(ba.StandMessage((-5.2-1.5,  2.2,  -2.4), 90))
            pls[2].actor.node.handlemessage(ba.StandMessage((-5.5-1.5,  2.2,  -1.5), 90))
            pls[3].actor.node.handlemessage(ba.StandMessage((-6.3-1.5,  2.2,  -4.2), 90))
        except: pass
        for i, player in enumerate(self.players):
            from bastd.actor.spaz import Spaz
            player.actor.on_move_left_right(0.4 + (0.075 * i))

        # Extra functions
        def cantcatchup()   :
            ba.timer(2.1, self.do_faint_clock)
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}01"),   time=2.1, idle=0.15, fade=2.0, scale=0.44, offset=(85, 85), end_call=None).start()
        def notgreattohear():
            self._dumb_bot_spawn(0.22)
            ba.timer(1.7, dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}06"),   time=1.4, idle=1.2, fade=0.6, scale=0.44, offset=(85, 85), end_call=None).start)
        
        # Dialogue routine
        dkey = "explodinary.campaignDialogue.mount_chill."
        player_speakers = [dialogue.get_player_speaker(p) for p in self.players]; helpy_speaker = dialogue.SpeakerLib().helpy
        
        _skip_vote = skipvote.SkipVoteModule(skiptext=ba.Lstr(resource='explodinary.skipCutscene'), on_vote_end=self.reset)
        
        plural = len(self.players) > 1
        _dialogue_manager = dialogue.DialogueManager(finish_call = _end)
        _dialogue_manager.add_message([
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}00"),                                         time=1.4, idle=3.0, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}02{'a' if plural else ''}"),                  time=2.5, idle=1.2, fade=0.6, end_call=self.turn_to_day),
            ('wait', 3.6),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}03{'a' if plural else ''}"),                  time=1.8, idle=1.2, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}04"),                        time=1.5, idle=1.4, fade=0.0, end_call=notgreattohear),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}05"),                                         time=1.3, idle=3.2, fade=0.0, end_call=ba.Call(self._start_spawning_stuff, 4.25, 8.25, 5, False)),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}07"),                                         time=4.2, idle=1.2, fade=0.6, end_call=self.badoink_helpy),
        ])
        
        self._set_night()
        ba.timer(0.5, _dialogue_manager.start)
        ba.timer(1.3, cantcatchup)

    def _golem_dialogue(self):
        """ Dialogue that shows up when golem spawns. """
        # Extra functions
        def no()    : dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}g02"), time=0.4, idle=1.4, fade=0.6, scale=0.44, offset=(85, 85), end_call=None).start()

        # Dialogue routine
        dkey = "explodinary.campaignDialogue.mount_chill."
        player_speakers = [dialogue.get_player_speaker(p) for p in self.players]; helpy_speaker = dialogue.SpeakerLib().helpy
        
        _dialogue_manager = dialogue.DialogueManager(finish_call = None)
        _dialogue_manager.add_message([
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}g00"),   time=1.2, idle=1.4, fade=0.0, end_call=ba.Call(ba.timer, 2.6, no)),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}g01"),                    time=2.5, idle=1.5, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}g03"),                    time=1.9, idle=1.2, fade=0.6, end_call=None),
        ])
        
        _dialogue_manager.start() 
        
    def _do_end_cutscene(self, outcome: str):
        """ Does our end level cutscene. """
        self.spawn_helpy((-0.5, 2.2, -3.1), True)
        self._cutscene_helpy.node.is_area_of_interest = True

        if self.has_done_cutscene('mcf', False):
            super().do_end(outcome)
            return
        
        # Dialogue routine
        dkey = "explodinary.campaignDialogue.mount_chill."
        player_speakers = [dialogue.get_player_speaker(p) for p in self.players]; helpy_speaker = dialogue.SpeakerLib().helpy
        
        # Extra funcs
        def _end():
            #_skip_vote.end()
            self.alt_do_end(outcome)
            
        def yoink_helpy():
            """ Moves helpy to throw himself off the mountain. """
            self._cutscene_helpy.on_run(1.5)
            self._cutscene_helpy.on_move_left_right(2.5)
            self._cutscene_helpy.on_move_up_down(-0.2)
            
            ba.timer(2.1, self._cutscene_helpy.on_jump_press)
        
        _skip_vote = skipvote.SkipVoteModule(skiptext=ba.Lstr(resource='explodinary.skipCutscene'), on_vote_end=_end)
        _dialogue_manager = dialogue.DialogueManager(finish_call = _end)
        
        _dialogue_manager.add_message([
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}e00"),   time=1.8, idle=1.2, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e01"),                    time=2.1, idle=1.3, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}e02"),   time=0.4, idle=0.2, fade=0.0, end_call=ba.Call(ba.timer, 1.2, yoink_helpy)),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}e03"),                    time=1.4, idle=1.6, fade=0.6, end_call=None),
        ])
        
        _dialogue_manager.start()

    def do_end(self, outcome: str, delay: float = 0) -> None:
        if self._won:
            self._do_end_cutscene(outcome)
        else: super().do_end(outcome, delay)

    def _end_wrapup(self):
        # Show once per session only.
        cd = ba.getsession().customdata
        if not cd.get('tip_mc', False):
            cd['tip_mc'] = True
            self.tips = [
                ba.GameTip(
                    'Steam Bombs have 4 seconds fuse, but the blast radius\n'
                    'is much bigger. Be patient to gain advantage!',
                    icon=ba.gettexture('powerupSteampunk'),
                    sound=ba.getsound('ding'),
                )
            ]
        self._dumbify(True)
        ba.timer(3, ba.WeakCall(self._start_time_bonus_timer))
        ba.timer(0.8, self._show_tip)
        ba.timer(0.2, self._render_badges)


    def turn_to_day(self):
        """ Turns the level into daytime. """
        self._fade_black()
        ba.timer(1.25, self._restore_tint)
        ba.timer(1.25, self.faster_snow)
        ba.timer(1.5, self.displace_players)
        ba.timer(1.5, lambda: self._cutscene_helpy.node.handlemessage(ba.StandMessage((1, 2.2, -3.1), 86)))
        ba.timer(3, self._fade_in)
        ba.timer(4.6, self.un_faint)

    def do_faint_clock(self):
        self.faint_clock = ba.Timer(0.05, self.all_faint, repeat=True)

    def un_faint(self): self.faint_clock = None

    def all_faint(self):
        for i, player in enumerate(self.players):
            if not player.actor: return
            player.actor.on_move_left_right(0)
            ba.timer(0.25 * (i*1.45), ba.Call(player.actor.node.handlemessage, 'knockout', 3 * 1000))

    def displace_players(self, factor = 3.25, rf = 1.25, facing = None):
        """ Offsets all players' X axis position """
        for i, player in enumerate(self.players):
            if not player.actor: return

            pos = player.actor.node.position
            npos = (pos[0]+random.uniform(-rf,rf)+factor,
                    pos[1]-0.5,
                    pos[2]+random.uniform(-rf,rf))

            if not facing:
                facing = random.uniform(-360, 360)

            player.actor.node.handlemessage(ba.StandMessage(npos, facing))

    def _set_night(self):
        """ Set our level to night """
        ba.animate_array(self._globalsnode, 'tint', 3, {
            0: (0.25,0.25,0.52),
            1: (0.25,0.25,0.52),
        })
        ba.animate_array(self._globalsnode, 'vignette_outer', 3, {
            0: (0.3,0.44,0.8), 
            1: (0.3,0.44,0.8),
        })

    def _restore_tint(self):
        """ Restores all tint values to their respective default value. """
        for x in ['tint','ambient_color','vignette_inner','vignette_outer']:
            ba.animate_array(self._globalsnode, x, 3, {
                0: self._globalsnode.__getattribute__(x), 
                1: self._default_tints[x],
            })

    def _fade_black(self):
        """ Covers our screen in darkness """
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
            1.5: 1,
        })

    def _fade_in(self):
        try:
            ba.animate(self._black_screen, 'opacity', {
                0: 1,
                1.5: 0,
            })
        except KeyError:
            ba.raise_exception("Should call after fade_black!")

    def faster_snow(self):
        self._snow_timer = ba.Timer(0.01, self.do_snow, repeat=True)

    def do_snow(self):
        bseVFX('snowflake',
               ([random.uniform(self._stage_ceiling[0][i], self._stage_ceiling[1][i]) for i in range(3)]),
               (0.2,-3,-0.2))
        
    def turn_blizzard(self):
        self._snow_timer = ba.Timer(0.01, self.do_blizzard, repeat=True)
        ba.animate(self._blizzard_sound, 'volume', {
            0:0,
            4.5:1.25 * 3,
        })

    def do_blizzard(self):
         bseVFX('blizzard',
               ([random.uniform(self._stage_ceiling[0][i], self._stage_ceiling[1][i]) for i in range(3)]),
               (5.25,-3.77,-1.25))

    def summon_boss(self) -> ba.Actor:

        pos = (1,2.75,-2.5) 
        ambiance = True

        spaz: ba.Actor | None = None

        def modify_ambiance():
            gn = self.globalsnode

            ba.animate_array(gn, 'vignette_outer', 3, {
                0:gn.vignette_outer,
                4.5:(1.15,1.15,1.4),
            })

            ba.animate_array(gn, 'tint', 3, {
                0:gn.tint,
                4.5:(0.8,0.8,1.1),
            })

            self.turn_blizzard()

        def golem():
            spaz = BossGolem().autoretain()

            hp = 1375 + (225 * len(self.players))
            spaz.hitpoints = spaz.hitpoints_max = hp

            ba.playsound(ba.getsound('spawn'), position=pos)
            spaz.node.handlemessage('flash')
            spaz.handlemessage(ba.StandMessage(pos, 0))

            SpazBotSet.add_bot(self._bots, spaz)
            BossHealthbar(spaz,
                          name="Snow Golem",
                          position=(0, -80),
                          attach="topCenter",
                          color=(0.62,0.87,1),
                          coloralt=(0.5,0.77,1),
                          deathtrigger=self._nuke_all_enemies,
                          )
            
            ba.timer(1.2, self._golem_dialogue)

        if ambiance: modify_ambiance()  
        bsespawner.BSESpawner(
            pt=pos,
            spawn_time=3.0,
            send_spawn_message=False,
            spawn_callback=golem,
        )

        return spaz

    def _nuke_all_enemies(self) -> None:
        self._nuke_timer = ba.Timer(0.05, self._nae_nae, repeat=True)

    def _nae_nae(self) -> None:
        self._bots._update()
        for bot in self._bots._bot_lists:
            try: bot[0].handlemessage(ba.DieMessage(how=ba.DeathType.OUT_OF_BOUNDS))
            except: pass

    def _start_next_wave(self) -> None:
        self._nuke_timer = None
        super()._start_next_wave()

        if self._wavenum == self._boss_wave:
            self.summon_boss()
            
            def music_change():
                ba.setmusic(ba.MusicType.GOLEM)
                
            ba.timer(3, music_change)

    def _badge_define(self):
        """ Defines our badges. """
        k = 'explodinary.campaignBadge.mc.'
        # Speedrun
        self._badge_append(
            'timetrial',
            ba.Lstr(resource=f'{k}n00'),
            ba.Lstr(resource=f'{k}d00'),
            '',
            'badgeSpeed',
        )
        # Steampunk bomb kills
        self._badge_append(
            'steampunkkills',
            ba.Lstr(resource=f'{k}n01'),
            ba.Lstr(resource=f'{k}d01'),
            '',
            'badgeSteam',
        )
        # Snowball kill
        self._badge_append(
            'snowballkill',
            ba.Lstr(resource=f'{k}n02'),
            ba.Lstr(resource=f'{k}d02'),
            '',
            'badgeSnoboi'
        )

    def _handle_kill_achievements(self, msg: SpazBotDiedMessage) -> None:
        """ Handles steam bomb / snowbal badge goals. """
        # Some basic variables
        dmg = msg.spazbot.last_attacked_type
        has_killer = msg.killerplayer

        if has_killer and dmg == ('explosion', 'steampunk'):
            # Track and requite!
            self._steam_bomb_kills += 1
            if self._steam_bomb_kills == 2:
                self._badge_update('steampunkkills', True)

        elif dmg == ('snowball', 'snowball'):
            badge = 'snowballkill'
            # Confirm we did in fact just do that (but just in case we havent.)
            if not self._badge_status(badge):
                self._badge_update(badge, True)


class BossGolem(GolemBot):
    """ Extra class for boss functions. """
    hardmode = False
    _ai = True

    def __init__(self):
        super().__init__()
        self._punch_power_scale = 2.9
        
        self._snowguy_max_time = smt = 16.25 - (0.25 * len(self._a().players))
        self._snowguy_timer = ba.Timer(smt, self.snowguy_operand)

        self._place_snoboi_here: list[tuple, float] | None = None

        self._snowball_timer = (ba.Timer(4, self.snowball_attack) if not self.hardmode else
                                ba.Timer(2, self.hardmode_snowball_attack, repeat=True))
        
    def update_ai(self):
        if not self._ai: return
        super().update_ai()

    def _a(self) -> MountChillGame: return ba.getactivity()

    def hpmx(self) -> float: return (self.hitpoints / self.hitpoints_max)

    def conscious(self) -> bool: return (self.node.exists() and self.is_alive() and not self.node.knockout > 0)

    def snowball_attack(self, time = 0.3, distance = None):
        """ Summons a snowball entity that pushes all entities it comes in contact with """
        if not self.node.exists() or self._a()._game_over: return
        if not distance: distance = max(4, 11.5 * self.hpmx())

        attack = True
        bdist, bplyr = [0, None]
        plist = self._a().players.copy()

        for pl in plist:
            if not pl.actor.is_alive(): continue
            mp, pp = [self.node.position, pl.node.position]
            dist = math.sqrt((mp[0] - pp[0])**2 + (mp[1] - pp[1])**2)

            if dist < distance:
                attack = False

            elif dist > bdist:
                bdist = dist
                bplyr = pl.node

        if attack:
            self._ai = False
            self.node.move_left_right = 0
            self.node.move_up_down = 0
            ba.timer(time, ba.Call(self.snobal_yoink, distance))
        else:
            self._snowball_timer = ba.Timer(max(0.88, 5.67 * self.hpmx()), self.snowball_attack)

    def snobal_yoink(self, distance = 0, normal = True):
        if self.conscious() and not self._a()._game_over:
            p, pf = [self.node.position_center, self.node.position_forward]
            angle = math.atan2(pf[2] - p[2], pf[0] - p[0])
            vl = (-math.cos(angle)*2, 0, -math.sin(angle)*2)
            vls = (-math.cos(angle)*5, 0, -math.sin(angle)*5)
            
            self.on_punch_press()
            self.on_punch_release()

            ba.timer(0.03, ba.Call(self._summon_snowball, pf, vl, vls))

        if normal:
            self._ai = True
            roll = random.random()
            if roll > self.hpmx():
                self._snowball_timer = ba.Timer(0.66, ba.Call(self.snowball_attack, 0.25, distance+(roll*0.5)))
            else:
                self._snowball_timer = ba.Timer(max(0.88, 5.67 * self.hpmx()), self.snowball_attack)


    def hardmode_snowball_attack(self): self.snobal_yoink()

    def _summon_snowball(self, pos, vel, svel):
        if self.conscious(): Snowball(pos, vel, svel).autoretain()

    def snowguy_summon(self):
        """ Animates snowmen to assist them in battle """
        
        angle = random.uniform(0,360)

        self._a()._can_end_wave = False

        angle_radians = angle / 57.2957795
        xval = math.sin(angle_radians) * 1.06
        zval = math.cos(angle_radians) * 1.06
        point = (xval / 0.125, 2.75, (zval / 0.2) - 3.7)

        self._place_snoboi_here = [point, angle]

        bsespawner.BSESpawner(
            pt=point,
            spawn_time=1.22,
            send_spawn_message=False,
            spawn_callback=self._snoboi,
        )

    def _snoboi(self):
        """ snoboi """
        pos, angle = self._place_snoboi_here
        m = self.hpmx()

        minion = FrostMinion if m > 0.5 else FrostMinionPro

        spaz = minion().autoretain()
        spaz.node.is_area_of_interest = False

        ba.playsound(ba.getsound('spawn'), 1.2, pos)

        spaz.handlemessage(ba.StandMessage(pos, angle))
        bseVFX('snowpuff', ([x - (0.5 if i == 1 else 0) for i,x in enumerate(pos)]), (0,2.1,0))

        SpazBotSet.add_bot(self._a()._bots, spaz)

        self._a()._can_end_wave = True

    def snowguy_operand(self):  
        """ Internal stuff before our snowguy_summon """
        if not self.node.exists(): return
        m = self.hpmx()
        smt = self._snowguy_max_time

        self.snowguy_summon()

        self._snowguy_timer = ba.Timer(max(smt*0.44, smt*m), self.snowguy_operand)


class Snowball(ba.Actor):
    """ Snowball actor summoned by the boss golem. """
    def __init__(self,
                 position,
                 velocity,
                 startingv):
        super().__init__()
        from bastd.gameutils import SharedObjects
        shared = SharedObjects.get()

        self._velocity = velocity

        clip_mat = ba.Material()
        clip_mat.add_actions(
            conditions=(
                (
                    ('we_are_younger_than', 400),
                    'or',
                    ('they_are_younger_than', 400),
                ),
                'and',
                ('they_have_material', shared.object_material),
            ),
            actions=('modify_node_collision', 'collide', False),
        )
        
        collide_mat = ba.Material()
        collide_mat.add_actions(
            conditions=                (
                    ('we_are_older_than', 750),
                    'or',
                    ('they_are_older_than', 750),
                ),
            actions=(
                ('call', 'at_connect', self._hit),
            ),
        )

        self.node = ba.newnode(
            'prop',
            delegate=self,
            attrs={
                'position':         position,
                'velocity':         startingv,
                'model':            ba.getmodel('snowball'),
                'light_model':      ba.getmodel('snowball'),
                'body':             'sphere',
                'body_scale':       1.5,
                'model_scale':      2.65,
                'shadow_size':      0.1,
                'color_texture':    ba.gettexture('vrFillMound'),
                'reflection':       'soft',
                'reflection_scale': [0.12],
                'materials':        [shared.footing_material, collide_mat, clip_mat],
                'gravity_scale':    0.89,
                'density':          2.5,
            })
        ba.animate(self.node, 'model_scale', {0: 0, 0.65: self.node.model_scale})
        self._impulse_timer = ba.Timer(0.1, self._constant_speed, repeat=True)

    def _constant_speed(self):
        if not self.node.exists():
            self._impulse_timer = None
            return
        
        me = self.node
        vl = self._velocity
        self.node.handlemessage('impulse', me.position[0], me.position[1], me.position[2],
                                0, 0, 0,
                                150, 150, 0, 0,
                                vl[0], 0, vl[2])

    def _hit(self):
        from bastd.actor.spaz import Spaz
        collision = ba.getcollision()
        try:
            them = collision.opposingnode.getdelegate(ba.Actor, None)
            tnode = them.node
            
            try:
                if type(them) is BossGolem: pass
                else:
                    tnode.handlemessage('impulse', tnode.position[0], tnode.position[1], tnode.position[2],
                                                0, 0, 0,
                                                300, 1000, 0, 0,
                                                self.node.velocity[0]*1.15, abs(self.node.velocity[1])*2, self.node.velocity[2]*1.15)
                    try:
                        them.last_attacked_type = ('snowball', 'snowball')
                    except: pass
            except: pass

        except ba.NotFoundError:
            return

    def _handle_oob(self):
        self.handlemessage(ba.DieMessage())

    def _handle_die(self):
        assert self.node
        self.node.delete()

    def handlemessage(self, msg):
        if isinstance(msg, ba.OutOfBoundsMessage):
            self._handle_oob()
        elif isinstance(msg, ba.DieMessage):
            self._handle_die()
        else:
            super().handlemessage(msg)


class FrostMinion(FrostyBot): points_mult = 0
class FrostMinionPro(FrostyBotPro): points_mult = 0
class FrostMinionProest(FrostyBotProShielded): points_mult = 0
