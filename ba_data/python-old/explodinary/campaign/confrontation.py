from __future__ import annotations
from typing import Any, Sequence

import ba
from collections.abc import Callable
from explodinary.actor.bsespazbot import (
    OverseerBot,
    OverseerClone,
    BrawlerBot,
    BomberBotProShielded,
    ChargerBotProShielded,
    TriggerBotPro,
    BrawlerBotPro,
    NoirBot,
)

from explodinary.campaign import (
    BSECampaignActivity,
    Wave,
    Spawn,
    Point,
)
from explodinary.custom.particle import bseVFX
from explodinary.actor import bsespawner
from explodinary.actor.bsespazbot import SpazBotSet
from explodinary.lib.boss import BossHealthbar
from bastd.gameutils import SharedObjects
from explodinary.lib.unlock import UnlockPopup
from explodinary.campaign import Player

from explodinary.lib import dialogue, skipvote
import random

class ConfrontationGame(BSECampaignActivity):
    """ Last BSE Campaign Level! """

    name = 'Eyes Of The Abyss'

    def __init__(self, settings: dict):

        # Set our map and if we get our defs from the json file.
        settings['map'] = 'Confrontation'
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

        # Dis the last one I promise
        self._has_cutscene = True
        self._end_game_after_waves: bool = False
        self._black_screen: ba.Node | None = None
        self._default_tints: dict | None = None
        # Overseer Boss
        self.overseer_boss: ba.Actor | None = None
        self.overseer_ff: ba.Node | None = None
        self.overseer_ff_bl: list = []
        self._overseer_clone_summon_trail: ba.Timer | None = None

        self.want_end_stage_3: bool = False

        self.can_end_stage_3: bool = False
        self.can_end_stage_3_t: ba.Timer | None = None
        
        self.want_end_stage_4: bool = False

        self.can_end_stage_4: bool = False
        self.can_end_stage_4_t: ba.Timer | None = None

        self._set_ff_mats()
        
        # Musica!
        self._music = ba.MusicType.PRE_ABYSS
        
    def _alternate_end(self):
        """ Alternate end if we don't end our game after waves. """
        self.overseer_boss.node.is_area_of_interest = True
        # We don't want players picking up powerups anymore
        # (and tnt would be an inconvenience at this point)
        self._disable_powerup_tnt()
        # Start the meteor shower after some seconds of showing Overseer.
        ba.setmusic(ba.MusicType.ABYSS)
        # Boss routine with their respective times.
        d = {
            'meteor': 18,
            'clone': 12,
        }
        ba.timer(1.5,
                 ba.Call(self.boss_meteor_shower,
                         d['meteor'],
                         ba.Call(self.boss_clone_stage,
                                 d['clone'],
                                 self.boss_clone_end_check,
                         )
                 )
        )
        
        # Respawn playa :3
        self._do_all_respawn()

    def animate_thunder(self):
        """ Animates the screen's outer vignette, simulating lightning """

        def animate():
            gn = self.globalsnode
            ba.animate_array(gn, 'vignette_outer', 3, {
                0: gn.vignette_outer,
                0.005: (1,1,1),
                0.08: gn.vignette_outer,
                0.1: (0.9,0.9,0.9),
                0.2: gn.vignette_outer,
                }
            )

        ba.playsound(ba.getsound("overseerEffectThunder"))
        ba.timer(1.5, animate)

    def overseer_thunder(self,
                         itr: int = 4):
        if not self.overseer_boss.node.exists(): return
        self.overseer_boss.node.handlemessage('celebrate', 222)
        
        thunderpos = [p + (1.05 if i == 1 else 0) for i,p in enumerate(self.overseer_boss.node.position)]
        ba.timer(0.05, lambda: bseVFX('thunderbolt', thunderpos, (0,2,0)))
        ba.emitfx(position=thunderpos,
                  velocity=(0,5,0),
                  count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                  scale=0.5,
                  spread=0.7,
                  chunk_type='spark')
        ploki = ba.newnode(
            'light',
            attrs={
                'position': self.overseer_boss.node.position,
                'volume_intensity_scale': 0.1,
                'intensity':0.25,
                'color': (0.9,0.9,1.2),
                'radius': 0.2,
            },
        )
        ba.animate(ploki, 'radius', {
            0: ploki.radius,
            0.09: 0.35,
            0.19: 0.09,
            0.26: 0.12,
            0.4: 0,
        })
        # Deletion
        ba.timer(0.6, ploki.delete)


        if itr > 0:
            ba.timer(0.38, ba.Call(self.overseer_thunder, itr-1))

    def _disable_powerup_tnt(self):
        """ Disables powerup drops and TNT respawning """
        self._powerup_drop_timer = None
        self._tnt_drop_timer = None

    def on_begin(self) -> None:

        # Save some general variables.
        player_count = len(self.players)
        self._excluded_powerups = []
        args: dict = {
            'first_spawn_type': ['fly_punch', 'dash'],
            'goal_time': '4m20s',
            'tnt': True,

            'showScoreboard': False,
        }
        self._track_damage = 'nodamage'

        # Our main list of waves and events.
        self._waves = [
            Wave(
                entries=[
                    Spawn(BomberBotProShielded, Point.RIGHT),
                    Spawn(BomberBotProShielded, Point.RIGHT_UPPER),
                    Spawn(BomberBotProShielded, Point.RIGHT_UPPER_MORE),
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
                    Spawn(NoirBot, Point.BOTTOM),
                    Spawn(NoirBot, Point.TOP),
                    Spawn(TriggerBotPro, Point.BOTTOM_HALF_RIGHT),
                    Spawn(TriggerBotPro, Point.BOTTOM_HALF_LEFT)
                    if player_count > 1
                    else None,
                    Spawn(NoirBot, Point.BOTTOM_RIGHT),
                    Spawn(NoirBot, Point.BOTTOM_LEFT)
                    if player_count > 2
                    else None,
                    Spawn(TriggerBotPro, Point.TOP_RIGHT),
                    Spawn(TriggerBotPro, Point.TOP_LEFT)
                    if player_count > 3
                    else None,
                ]
            ),
            Wave(
                entries=[
                    Spawn(ChargerBotProShielded, Point.RIGHT),
                    Spawn(BrawlerBotPro, Point.TOP_HALF_LEFT),
                    Spawn(BrawlerBotPro, Point.TOP),
                    Spawn(BrawlerBotPro, Point.TOP_HALF_RIGHT),
                    Spawn(ChargerBotProShielded, Point.LEFT)
                    if player_count > 1
                    else None,
                    Spawn(ChargerBotProShielded, Point.TOP_RIGHT),
                    Spawn(ChargerBotProShielded, Point.TOP_LEFT)
                    if player_count > 2
                    else None,
                    Spawn(BrawlerBotPro, Point.RIGHT_UPPER),
                    Spawn(BrawlerBotPro, Point.LEFT_UPPER)
                    if player_count > 3
                    else None,
                ]
            ),
        ]
        # Let our main class set up powerups, start waves and such.
        super().on_begin(args)

        self._popuped = False
        
        # Update damage evasion badge goal information
        dmgtsh = str(self._damage_threshold + 110)
        self._badge_text('nodamage',
                         desc=ba.Lstr(resource='explodinary.campaignBadge.nodmg.desc', subs=[('${DMG}', dmgtsh)]),
                         short_desc=ba.Lstr(resource='explodinary.campaignBadge.nodmg.s_desc', subs=[('${DMG}', dmgtsh)]),
                         )

        # Cutting scenes again!
        gln = self._globalsnode
        self._default_tints = {
            'tint': gln.tint,
            'amb': gln.ambient_color,
            'v_in': gln.vignette_inner,
            'v_out': gln.vignette_outer,
        }
        
        self._do_intro_cutscene()
        self.overseer_boss: ba.Actor = self.overseer_summon()
        self.overseer_boss.impact_scale = 0
        ba.timer(1.0, self.overseer_hold_pos)

    def _is_overseer_alive(self):
        """ Checks if Overseer exists """
        try:
            return self.overseer_boss.node.exists()
        except:
            return self.overseer_boss

    def _set_ff_mats(self):
        """ Sets Overseer's fling forcefield materials """
        self._shared = shared = SharedObjects.get()
        self._overseer_ff_mat = ba.Material()
        self._overseer_ff_mat.add_actions(
            conditions=('they_have_material', shared.object_material),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                (
                    'call',
                    'at_connect',
                    ba.Call(self.overseer_fling_player, True),
                ),
                (
                    'call',
                    'at_disconnect',
                    ba.Call(self.overseer_fling_player, False), # BSE-TODO: Pretty sure this isn't necessary.. heck, ill leave it for later
                ),
            ),
        )

    def boss_meteor_shower(self,
                           duration: float,
                           end_call: Callable = None):
        """ Summons a meteor shower for the given time """
        from bastd.actor.bomb import Bomb
        # This is wild: What if we made the meteor shower predictable?
        random.seed('overseerse')
        bounds = self.map.get_def_bound_box('map_bounds')
        newbounds = [bounds[0]+3, bounds[1], bounds[2]+7,
                     bounds[3]-3, bounds[4], bounds[5]-1]
        bounds = newbounds

        # Pool of bombs that can drop
        bombpool = (
                    ['normal']
                    )

        def bomba():
            """ Summons a bomb """
            type = random.choice(bombpool)

            pos = (
                random.uniform(bounds[0], bounds[3],)*0.9,
                random.uniform(bounds[4], bounds[4],),
                random.uniform(bounds[2], bounds[5],)*0.9,
                   )

            vel = (
                (-5.0 + random.random() * 15.0) * -( ( pos[0] - ( bounds[0] + bounds[3] ) / 2 ) / 4 ),
                random.uniform(-3.066, -4.12),
                (-5.0 + random.random() * 15.0) * -( ( pos[2] - ( bounds[2] + bounds[5] ) / 2 ) / 4 ),
            )

            Bomb(position=pos, velocity=vel, bomb_type=type).autoretain()

        def _not():
            """ Ends the event and calls if included """
            self._bomba_timer = False
            if end_call:
                ba.timer(2, end_call)

        def mainrout():
            """ Sets the timers for our bombs """
            bpes = 1/12
            self._bomba_timer = ba.Timer(bpes, bomba, repeat=True)
            self._bomba_shutdown_timer = ba.Timer(duration, _not)

        # Thunder FX
        self.animate_thunder()
        # Overseer animation
        ba.timer(1.5, lambda: self.overseer_thunder(int((1/0.38)*duration)))
        # Main routine
        ba.timer(1.5, mainrout)

    def boss_clone_stage(self,
                         duration: float,
                         end_call: Callable = None):
        """ Brings Overseer down to summon some clones """
        spawn_delay = 1
        position = (-1.0, 2.4, -7.125)

        self.overseer_badoink()

        bsespawner.BSESpawner(
            pt=position,
            spawn_time=spawn_delay,
            send_spawn_message=False,
            spawn_callback=ba.Call(self.overseer_boss_3rd_stage, position),
        )

        mp = 0.87 + (0.13 * len(self.players))
        stime = {
            'lazy':     1 / mp,
            'lazyd':    2 / mp,
            'norm':     2.75 / mp,
        }

        def start():
            self._clone_timer_lazy = ba.Timer(stime['lazy'],
                                              ba.Call(self.overseer_clone_routsummon,
                                                      delay = stime['lazyd'],
                                                      lazy = True,
                                                      ),
                                              repeat=True)

            self._clone_timer_norm = ba.Timer(stime['norm'],
                                              ba.Call(self.overseer_clone_routsummon),
                                              repeat=True)
            
        def stop():
            self._clone_timer_lazy = self._clone_timer_norm = None
            if end_call:
                ba.timer(2, end_call)

        start()
        ba.timer(duration, stop)

    def boss_clone_end_check(self,
                             itr: int = 8,
                             conf: bool = False):
        """ Checks if all Overseer clones are dead """
        if itr < 1:
            self.boss_balls()
            return

        # We want to end this stage
        self.want_end_stage_3 = True
        conf = True

        lbots = self._bots.get_living_bots()
        if self.can_end_stage_3:
            for x in lbots:
                if type(x) is OverseerGoon:
                    conf = False
        else:
            conf = False

        if conf:
            itr -= 1
            time = 0.33
        else:
            itr = 8
            time = 1

        ba.timer(time, lambda: self.boss_clone_end_check(itr, conf))
        
    def boss_balls(self):
        self.overseer_badoink()
        if self.overseer_ff:
                self.overseer_ff.delete()
        ba.playsound(ba.getsound('overseerLaugh'), volume=5)

        # Modify the range for the x, y, and z coordinates as needed
        X_RANGE = (-8, -6)  # Example: spawn balls between x = -8 and x = -6
        Y_RANGE = (5, 9)    # Example: spawn balls between y = 5 and y = 9
        Z_RANGE = (-8, 2)   # Example: spawn balls between z = -8 and z = 2
        
        def _summon_first_balls():  
            for _ in range(6):
                x = random.uniform(X_RANGE[0], X_RANGE[1])
                y = random.uniform(Y_RANGE[0], Y_RANGE[1])
                z = random.uniform(Z_RANGE[0], Z_RANGE[1])
                BigBall((x, y, z), (0, 0, 0)).autoretain()
        
        def _summon_second_balls():
            for _ in range(6):
                x = random.uniform(X_RANGE[0], X_RANGE[1])
                y = random.uniform(Y_RANGE[0], Y_RANGE[1])
                z = random.uniform(Z_RANGE[0], Z_RANGE[1])
                BigBall((x, y, z), (0, 0, 0)).autoretain()
        
        def _summon_third_balls():
            for _ in range(6):
                x = random.uniform(X_RANGE[0], X_RANGE[1])
                y = random.uniform(Y_RANGE[0], Y_RANGE[1])
                z = random.uniform(Z_RANGE[0], Z_RANGE[1])
                BigBall((x, y, z), (0, 0, 0)).autoretain()

        def _end_balls():
            self._boss_battle()
            # self._start_powerup_drops()
            forcetype = 'health'
            self._tnt_drop_timer = None
        
        _summon_first_balls()
        ba.timer(4, _summon_second_balls)
        ba.timer(8, _summon_third_balls)
        
        ba.timer(10, _end_balls)
    
    def _boss_behavior(self, position):
        """ Respawns Overseer for our final battle """
        self.overseer_boss = self.overseer_summon(position, True)
        
        self.overseer_boss.impact_scale = 0.85
        self.overseer_boss.node.is_area_of_interest = True
        self.overseer_boss._ai = True
        hp = 3775 + (225 * len(self.players))
        self.overseer_boss.hitpoints = self.overseer_boss.hitpoints_max = hp
        
        BossHealthbar(self.overseer_boss,
                      name="Overseer",
                      position=(0, -80),
                      attach="topCenter",
                      color=(0.62,0.87,1),
                      coloralt=(0.5,0.77,1),
                      deathtrigger=ba.Call(self.victory),
                      )

        # Particles
        ba.emitfx(position=position,
                  velocity=(0, 0, 0),
                  count=12,
                  scale=2.15,
                  spread=1.5,
                  chunk_type='spark')

        # More stuff!
        self.overseer_ai_doobie()
    
    def victory(self):
        self._timer_win() # Timer check!! Yippie!
        self.show_zoom_message(
            ba.Lstr(resource='victoryText'), scale=1.0, duration=4.0
        )
        self.celebrate(20.0)
        base_delay = 5.0
        self._award_completion_achievements()
        ba.timer(base_delay, ba.WeakCall(self._award_completion_bonus))
        base_delay += 0.85
        ba.playsound(self._winsound)

        ba.cameraflash()
        ba.setmusic(ba.MusicType.VICTORY)

        self._do_all_respawn()

        self._game_over = self._won = True

        # Can't just pass delay to do_end because our extra bonuses
        # haven't been added yet (once we call do_end the score
        # gets locked in).
        ba.timer(base_delay, ba.WeakCall(self.do_end, 'victory'))
        
    def _boss_battle(self):
        """ Brings Overseer down... to take YOU down! """
        spawn_delay = 1
        position = (-1.0, 2.4, -7.125)
        
        self.overseer_badoink()

        bsespawner.BSESpawner(
            pt=position,
            spawn_time=spawn_delay,
            send_spawn_message=False,
            spawn_callback=ba.Call(self._boss_behavior, position),
        )
        
        self._do_all_respawn()
        
        for player in self.players:
            player.actor.equip_boxing_gloves()
            player.actor.handlemessage(ba.PowerupMessage('health', None, False))
        
    def overseer_summon(self,
                        pos: tuple = (-1, 6.6, -9.8),
                        particle: bool = False) -> ba.Actor:
        """ Oh sheit, it's Overseer! """
        spaz: ba.Actor | None = None

        spaz = OverseerBoss().autoretain()
        spaz.node.is_area_of_interest = False

        hp = 4500 + (600 * len(self.players))
        spaz.hitpoints = spaz.hitpoints_max = hp

        ba.playsound(ba.getsound('spawn'), position=pos)
        spaz.node.handlemessage('flash')
        spaz.handlemessage(ba.StandMessage(pos, 0))
        if particle: bseVFX('gone_puff', spaz.node.position, spaz.node.velocity)

        #SpazBotSet.add_bot(self._bots, spaz)
        return spaz
    
    def overseer_ai_doobie(self): SpazBotSet.add_bot(self._bots, self.overseer_boss)

    def overseer_hold_pos(self):
        """ Teleports Overseer to the location he's in the moment this function is called """
        self._seer_stand = ba.Timer(0.05, ba.Call(self.overseer_stand, self.overseer_boss.node.position), repeat=True)
    def overseer_release_all(self):
        self._seer_stand = None
        self._overseer_health_timer = None
    def overseer_stand(self, pos):
        try:
            o,p,s = (self.overseer_boss, self.overseer_boss.node.position, pos)
            for i,x in enumerate(p):
                if p[i] < s[i]-0.25 or p[i] > s[i]+0.25:
                    o.handlemessage(ba.StandMessage((s[0], s[1]-1, s[2])))
        except: return None

    def overseer_badoink(self):
        """ Overseer DIES. """
        try:
            bseVFX('gone_puff', self.overseer_boss.node.position, self.overseer_boss.node.velocity)
            self.overseer_boss.node.handlemessage(ba.DieMessage(how=ba.DeathType.GENERIC))
            self.overseer_boss.node.delete()
            self.overseer_release_all()
        except: pass

    def overseer_boss_3rd_stage(self, position):
        """ Respawns overseer for our 3rd stage """
        self.overseer_boss = self.overseer_summon(position, True)
        
        self.overseer_boss.impact_scale = 1.25
        self.overseer_boss.node.is_area_of_interest = True
        self.overseer_boss._ai = True

        # Particles
        ba.emitfx(position=position,
                  velocity=(0, 0, 0),
                  count=12,
                  scale=2.15,
                  spread=1.5,
                  chunk_type='spark')
        
        # Set temp. properties so he doesn't sprint right into our player.
        self.overseer_boss.charge_speed_min = 0.25
        self.overseer_boss.charge_speed_max = 0.25
        self.overseer_boss.run = False

        # More stuff!
        self.overseer_ai_doobie()
        self.overseer_set_hp_clock()
        
        self.overseer_ff = ba.newnode(
            'region',
            attrs={
                'position': (-12.0, 2.25, -3.3),
                'scale': (1.5, 1.5, 1.5),
                'type': 'sphere',
                'materials': [self._overseer_ff_mat, self._shared.region_material],
            },
        )
        self.overseer_boss.node.connectattr('torso_position', self.overseer_ff, 'position')

    def _ces3_check(self): self.can_end_stage_3 = True

    def overseer_clone_summon(self,
                              the):
        """ Summons a Overseer clone """
        # Don't spawn if we already want to end this stage
        self.can_end_stage_3 = False
        if type(the) is tuple:
            # If it has a coordinate format, consider it a direct position.
            pos = the
        else:
            # We assume its a point instead.
            pos = self.map.defs.points[the.value]

        def clone():
            spaz = OverseerGoon().autoretain()

            ba.playsound(ba.getsound('overseerEffectCloneSpawn'), position=pos)
            spaz.node.handlemessage('flash')
            spaz.handlemessage(ba.StandMessage(pos, 0))

            SpazBotSet.add_bot(self._bots, spaz)

        bsespawner.BSESpawner(
            pt=pos,
            spawn_time=1.5,
            send_spawn_message=False,
            spawn_callback=clone,
        )

        self.can_end_stage_3_t = ba.Timer(3, self._ces3_check)

    def overseer_clone_routsummon(self, delay = 0.001, lazy: bool = False):
        """ Call routine for clone summoning """
        if lazy:
            pos = random.choice([p for p in self.players if p.exists()]).actor.node.position
        else:
            pool = [
                Point.RIGHT,
                Point.RIGHT_UPPER,
                Point.RIGHT_UPPER_MORE,
                Point.LEFT,
                Point.LEFT_UPPER,
                Point.LEFT_UPPER_MORE,
                Point.TOP,
                Point.TOP_HALF_RIGHT,
                Point.BOTTOM,
                Point.BOTTOM_HALF_RIGHT,
                Point.BOTTOM_HALF_LEFT,
                Point.BOTTOM_RIGHT,
                Point.BOTTOM_LEFT,
                Point.TOP_RIGHT,
                Point.TOP_LEFT,
                Point.RIGHT_UPPER,
                Point.LEFT_UPPER,
                Point.TOP_HALF_LEFT,
                Point.TOP_HALF_RIGHT,
            ]
            pos = random.choice(pool)

        ba.timer(delay, ba.Call(self.overseer_clone_summon, pos))


    def overseer_set_hp_clock(self): self._overseer_health_timer = ba.Timer(0.05, self.overseer_hp_cap, repeat=True)
    
            
    def overseer_hp_cap(self):
        if not self._is_overseer_alive(): return
        if not self.overseer_boss.hitpoints == self.overseer_boss.hitpoints_max:
            self.overseer_boss.hitpoints = self.overseer_boss.hitpoints_max
            self.overseer_boss.node.hurt = 0

    def overseer_shield(self, pmo: tuple = (0,0,0)):
        if not self._is_overseer_alive(): return
        # Shield
        opos = self.overseer_boss.node.position
        plok = ba.newnode(
                'shield',
                owner=self.overseer_boss.node,
                attrs={
                    'color': (0.4, 0.4, 1.2),
                    'radius': 2.25,
                    },
            )
        self.overseer_boss.node.connectattr('position_center', plok, 'position')
        # Shield color decoloring
        ba.animate_array(plok, 'color', 3, {
            0: plok.color,
            0.3: (0,0,0),
        })
        # Shield tinifying
        ba.animate(plok, 'radius', {
            0: plok.radius,
            0.3: 0,
        })
        # Deletion
        ba.timer(0.3, plok.delete)

        # Light
        ploki = ba.newnode(
            'light',
            attrs={
                'position': opos,
                'volume_intensity_scale': 0.1,
                'intensity':0.9,
                'color': (0.4, 0.4, 1.1),
                'radius': 0.66,
            },
        )
        ba.animate(ploki, 'radius', {
            0: ploki.radius,
            0.3: 0,
        })
        # Deletion
        ba.timer(0.3, ploki.delete)

        # FX
        # Particles
        ba.emitfx(position=opos,
                  velocity=(pmo[0], pmo[1], pmo[2]),
                  count=12,
                  scale=2.15,
                  spread=1.5,
                  chunk_type='spark')
        # Visual distortion
        ba.emitfx(
            position=opos,
            emit_type='distortion',
            spread=1.66,
        )
        # evel = (velocity[0], max(-1.0, velocity[1]), velocity[2])
        # explosion = ba.newnode(
        #     'explosion',
        #     attrs={
        #         'position': opos,
        #         'velocity': (0,0,0),
        #         'radius': 1.8,
        #         'big': True,
        #         'color': (0,0,0),
        #     },
        # )
        # ba.timer(1.0, explosion.delete)

    def overseer_fling_player(self, collide: bool):
        """ Flings a player if he gets too close to Overseer """
        if not collide: return
        collision = ba.getcollision()
        try:
            they = collision.opposingnode.getdelegate(ba.Actor, None)
            if they in self.overseer_ff_bl: return
            try:
                they._ai
                return
            except: pass
            opos = self.overseer_boss.node.position
            ppos = they.node.position
        except: return None

        # Add them to our blacklist for half a second to prevent pushing them more than once.
        self.overseer_ff_bl.append(they)
        ba.timer(0.025, ba.Call(self.overseer_ff_bl.remove, they))

        ff = [p-opos[i] + (0.22 if i == 1 else 0) for i,p in enumerate(ppos)]

        self.overseer_thunder(0)
        self.overseer_shield(ff)
        ba.playsound(ba.getsound('shieldHit'), position=self.overseer_boss.node.position)

        for x in range(4):
            they.node.handlemessage('impulse', they.node.position[0], they.node.position[1], they.node.position[2],
                                    0, 0, 0,
                                    12*11, 0,
                                    0, 0,
                                    ff[0]*0.2, ff[1]*4, ff[2]*0.2)

            they.node.handlemessage('impulse', they.node.position[0], they.node.position[1], they.node.position[2],
                                    0, 0, 0,
                                    12*31, 0,
                                    0, 0,
                                    ff[0]*2.6, ff[1]*0.5, ff[2]*2.6)
    
    def _do_intro_cutscene(self):
        """ Does our level intro. """
        # Skip if we've already seen this cutscene / are in speedrun mode / have "skip cutscenes" enabled
        if self.has_done_cutscene('cft'):
            self._intro_cutscene_end(True)
            return

        # Disable player controls
        self._handle_controllers(False)
        # Hide stuff!
        self._inv_flashbang()

        # Extra funcs
        def hwait()  : dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}05"), time=1.0, idle=1.0, fade=0.4, scale=0.44, offset=(85, 85), end_call=None).start()
        def _end():
            _skip_vote.end()
            self._reveal_screen()
            self._intro_cutscene_end()

        # Dialogue routine
        dkey = "explodinary.campaignDialogue.confrontation."
        player_speakers = [dialogue.get_player_speaker(p) for p in self.players]; helpy_speaker = dialogue.SpeakerLib().helpy

        _skip_vote = skipvote.SkipVoteModule(skiptext=ba.Lstr(resource='explodinary.skipCutscene'), on_vote_end=self.reset)

        plural = len(self.players) > 1
        named_players = [
            self.players[0].getname(),
            self.players[1].getname() if len(self.players) > 1 else '',
            "".join([p+(', ' if not i+1 == len(self.players[2:]) else '') for i,p in enumerate(self.players[2:])]) if len(self.players) > 2 else '', 
            '' if len(self.players) < 2 else 'a' if len(self.players) < 3 else 'b'
        ]

        _dialogue_manager = dialogue.DialogueManager(finish_call = _end)
        _dialogue_manager.add_message([
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}00"),                                             time=4.2, idle=1.5, fade=0.0, end_call=None),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}01"),                            time=2.1, idle=1.4, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}02"),                                             time=2.9, idle=1.5, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}03"),                                             time=3.1, idle=1.5, fade=0.0, end_call=ba.Call(ba.timer, 2.1, hwait)),
            dialogue.DialogueMessage(random.choice(player_speakers), text=ba.Lstr(resource=f"{dkey}04{'a' if plural else ''}"),     time=3.4, idle=1.1, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}06{'a' if plural else ''}"),                      time=3.4, idle=1.7, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}07{'a' if plural else ''}"),                      time=3.1, idle=1.5, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}08{named_players[3]}", subs=[
                ('${NAME}', named_players[0]),
                ('${NAME2}', named_players[1]),
                ('${NAMES}', named_players[2]),
                ]),                                                                                                                 time=2.3, idle=1.4, fade=0.0, end_call=None),
            dialogue.DialogueMessage(helpy_speaker, text=ba.Lstr(resource=f"{dkey}09"),                                             time=0.4, idle=1.5, fade=1.0, end_call=None),
        ])
        
        ba.timer(0.5, _dialogue_manager.start)
            
    def _inv_flashbang(self):
        """ Covers the screen with a black image """
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

    def _end_wrapup(self):
        # Show once per session only.
        cd = ba.getsession().customdata
        if not cd.get('tip_abyss', False):
            cd['tip_abyss'] = True
            self.tips = [
                ba.GameTip(
                        'Use Cloud Cuffs to shoot your enemies or trigger chain reactions quickly.\n'
                        'Use Dash-O-Matic to dash forward a few times and gain speed.',
                        icon=ba.gettexture('abyssTip'),
                        sound=ba.getsound('ding'),
                )
            ]
        self._args['showScoreboard'] = True
        self._show_scoreboard_info()
        ba.timer(3, ba.WeakCall(self._start_time_bonus_timer))
        ba.timer(0.8, self._show_tip)
        ba.timer(0.2, self._render_badges)

    def _badge_define(self):
        """ Defines our badges. """
        k = 'explodinary.campaignBadge.cft.'
        # Speedrun
        self._badge_append(
            'timetrial',
            ba.Lstr(resource=f'{k}n00'),
            ba.Lstr(resource=f'{k}d00'),
            '',
            'badgeSpeed',
        )
        # No damage
        self._badge_append(
            'nodamage',
            ba.Lstr(resource=f'{k}n01'),
            ba.Lstr(resource=f'{k}d01'),
            '',
            'badgeHP',
            True,
        )
        # Don't get hit
        self._badge_append(
            'nohit',
            ba.Lstr(resource=f'{k}n02'),
            ba.Lstr(resource=f'{k}d02'),
            '',
            'badgeFlawless',
        )

    def end_game(self) -> None:
        super().end_game()
        ba.playsound(ba.getsound('overseerLaughDefeat'), volume=2)

    def _update_waves(self) -> None:
        super()._update_waves()
        unlockedOversilly = ba.app.config.get("BSE: Oversilly Oversillier", False)

        force_popup = False # debug
        if self._won and (not unlockedOversilly or force_popup) and not self._popuped:
            UnlockPopup()
            self._popuped = True
            ba.app.config['BSE: Oversilly Oversillier'] = True
            ba.app.config.commit()

class OverseerBoss(OverseerBot):
    """ Class for our Overseer boss """
    def __init__(self) -> None:
        super().__init__()
        ba.timer(0.1, self.record_pos)

    def record_pos(self): self.initpos = self.node.position

    def ai(self, enable: bool = True):
        self._ai = enable

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.OutOfBoundsMessage):
            self.node.handlemessage(ba.StandMessage(self.initpos))
            return
        else:
            super().handlemessage(msg)

class OverseerGoon(OverseerClone):
    """ Class for our Overseer clones """
    def __init__(self) -> None:
        super().__init__()

    def _vanish(self) -> None:
        if self.node.exists():
            bseVFX('gone_puff', self.node.position, self.node.velocity)
            ba.playsound(ba.getsound('overseerEffectClonePoof'), 1.25, position=self.node.position)
            self.node.delete()

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.HitMessage):
            super().handlemessage(msg)
            self.handlemessage(ba.DieMessage())
        elif isinstance(msg, ba.DieMessage):
            super().handlemessage(msg)
            ba.timer(random.uniform(0.15,2), self._vanish)
        else:
            super().handlemessage(msg)

class BigBall(ba.Actor):
    """ Ball actor summoned by the Overseer. """
    def __init__(self,
                 position: Sequence[float] = (0.0, 1.0, 0.0),
                 velocity: Sequence[float] = (0.0, 0.0, 0.0)):
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
                'velocity':         velocity,
                'model':            ba.getmodel('bigRock'),
                'light_model':      ba.getmodel('bigRock'),
                'body':             'sphere',
                'body_scale':       1.5,
                'model_scale':      2.65,
                'shadow_size':      0.1,
                'color_texture':    ba.gettexture('bigRockColor'),
                'reflection':       'soft',
                'reflection_scale': [0.12],
                'materials':        [shared.footing_material, collide_mat, clip_mat],
                'gravity_scale':    0.89,
                'density':          2.5,
            })
        ba.animate(self.node, 'model_scale', {0: 0, 0.65: self.node.model_scale})
        self.rock_light = ba.newnode('light',
                          owner=self.node,
                          attrs={'position':self.node.position,
                                  'radius':0.4,
                                  'intensity':0.5,
                                  'color': (0, 0, 1),
                                  'volume_intensity_scale': 1.0}) 
        self.node.connectattr('position',self.rock_light,'position')
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
                if type(them) is OverseerBoss: pass
                else:
                    tnode.handlemessage('impulse', tnode.position[0], tnode.position[1], tnode.position[2],
                                                0, 0, 0,
                                                300, 1000, 0, 0,
                                                self.node.velocity[0]*1.15, abs(self.node.velocity[1])*2, self.node.velocity[2]*1.15)
                    try:
                        them.last_attacked_type = ('bigball', 'bigball')
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