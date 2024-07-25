from explodinary.chaos import ChaosEvent, append_chaos_event
from explodinary.chaos import shared

from bastd.actor.spazappearance import Appearance
from explodinary.custom.particle import bseVFX
from bastd.actor.bomb import get_bomb_types, Blast

from explodinary.game.pathwayPandemonium import PathwayPandemoniumGame

import ba
from bastd.actor.spaz import Spaz
import random

class SoKPiggies(ChaosEvent):
    name = 'Piggies!'
    icon = 'chaosPiggies'

    def event(self):
        transmutes = [
            ba.app.spaz_appearances.get('Mel'),
            ba.app.spaz_appearances.get('Melly'),
            ba.app.spaz_appearances.get('Melvin'),
        ]
        
        for spaz in self._get_everyone():
            if not spaz.node.exists(): continue
            transmute_choice = random.choice(transmutes)
            self.transmute(spaz, transmute_choice)
            
    def transmute(self, spaz: Spaz, transmute: Appearance):
        ''' Turn 'em into piggos! '''
        # Transform our Spaz
        shared.transform_spaz_appearance(spaz, transmute)
        
        # Give 'em Triples and Stickies
        spaz.node.handlemessage(ba.PowerupMessage(poweruptype='sticky_bombs', showtooltip=False))
        spaz.node.handlemessage(ba.PowerupMessage(poweruptype='triple_bombs', showtooltip=False))
            
append_chaos_event(SoKPiggies)

class SoKJumpymania(ChaosEvent):
    name = 'Jumpymania'
    icon = 'chaosJumpymania'
    
    def event(self):
        self.duration = duration = self._get_config()['time'] * 0.85
        self.fit = fetch_iterations = 24
        self.clock = duration / fetch_iterations
            
        self.fetch_victims()
            
        return duration

    def hop(self,
            spaz: Spaz,
            pool: list = [],
            first: bool = True):
        ''' Makes the spaz jump. '''
        if not spaz.node.exists(): return
        
        # Skip the first iteration
        if not first:
            spaz.node.jump_pressed = True
            spaz.node.jump_pressed = False
            spaz.node.handlemessage('celebrate', 300)
        
        if len(pool) < 1:
            spaz._chaos_hoppin = False
            return
        
        delay = pool.pop(0)
        
        # Re-queue
        ba.timer(delay, ba.Call(self.hop, spaz, pool, False))
        
    def fetch_victims(self,
                      itr: int = 0):
        ''' Finds victims and makes them hop.
            Useful for those fellas respawning :) '''
        for entity in self._get_everyone():
            try:
                if entity._chaos_hoppin:
                    continue
                else: entity._chaos_hoppin = True
            except:
                entity._chaos_hoppin = True
            
            mitr = self.fit
            
            time = self.duration - (self.duration * (itr / mitr))
            jumps = random.randint(int(mitr/3.428), mitr); jumps = max(1, int(jumps - (jumps * (itr / mitr))))
            
            timepool = shared.distribute(time, jumps)
            ttime = timepool.pop(0)
            
            ba.timer(ttime, ba.Call(self.hop, entity, timepool, True))
            
        if not itr >= self.fit: 
            ba.timer(self.clock, ba.Call(self.fetch_victims, itr+1))
        
append_chaos_event(SoKJumpymania)

class SoKPuppets(ChaosEvent):
    name = 'Puppets?!'
    icon = 'chaosPuppets'
    blacklist = [
        ba.CoopSession
    ]
    
    def event(self):
        duration = max(3, self._get_config()['time'] * 0.44)
        self.fit = fetch_iterations = 2+int(duration)
        self.clock = duration / fetch_iterations
            
        self.fetch_victims(-1)
            
        return duration

    def min_max(self) -> int: return random.choice([-1,1])

    def fetch_victims(self,
                      itr: int = 0):
        ''' Finds victims and flings them. '''
        for entity in self._get_everyone():
            if not entity.node.exists(): return
            spaz = entity; mm = self.min_max
            spaz.node.handlemessage('impulse',
                                    spaz.node.position[0], spaz.node.position[1], spaz.node.position[2],
                                    120, 0, 120,
                                    150, 0.4, 0, 0,
                                    mm(), 1, mm())
            
        if not itr >= self.fit: 
            ba.timer(self.clock, ba.Call(self.fetch_victims, itr+1))
        
append_chaos_event(SoKPuppets)

class SoKGoblins(ChaosEvent):
    name = 'GOBLINS'
    icon = 'chaosGoblins'
    
    def event(self):
        duration = max(3, self._get_config()['time'] * 0.9)
        self.fit = fetch_iterations = int(16 * duration)
        self.clock = duration / fetch_iterations
            
        self.fetch_victims(-1)
            
        return duration

    def fetch_victims(self,
                      itr: int = 0):
        ''' Finds victims and goblifies them. '''
        for entity in self._get_everyone():
            if not entity.node.exists(): return
            spaz = entity
            spaz.node.handlemessage('impulse',
                                    spaz.node.position[0], spaz.node.position[1], spaz.node.position[2],
                                    0, 0, 0,
                                    -400, -400, 0, 0,
                                    0, 1, 0)
            
        if not itr >= self.fit: 
            ba.timer(self.clock, ba.Call(self.fetch_victims, itr+1))
            
append_chaos_event(SoKGoblins)

class SoKEveryoneTrips(ChaosEvent):
    name = 'Everyone Trips'
    icon = 'chaosEveryoneTrips'
    
    def event(self):
        self.duration = duration = self._get_config()['time'] * 0.9
        self.fit = fetch_iterations = 4 if self._is_coop else 8
        self.clock = duration / fetch_iterations
            
        self.fetch_victims()
            
        return duration

    def trip(self,
            spaz: Spaz,
            pool: list = []):
        ''' Makes the spaz trip. '''
        if not spaz.node.exists(): return
        
        knocktime = random.randint(60, 175)
        spaz.node.handlemessage('knockout', knocktime)
        
        if len(pool) < 1:
            spaz._chaos_trippin = False
            return
        
        delay = pool.pop(0)
        
        # Re-queue
        ba.timer(delay, ba.Call(self.trip, spaz, pool))
        
    def fetch_victims(self,
                      itr: int = 0):
        ''' Finds victims and makes them trip. '''
        for entity in self._get_everyone():
            try:
                if entity._chaos_trippin:
                    continue
                else: entity._chaos_trippin = True
            except:
                entity._chaos_trippin = True
            
            time = self.duration - (self.duration * (itr / self.fit)) * random.uniform(0.85, 1)
            trips = random.randint(min(int(time), 2), self.fit); trips = max(1, int(trips - (trips * (itr / self.fit))))
            
            timepool = shared.distribute(time, trips)
            ttime = timepool.pop(0)
            
            ba.timer(ttime, ba.Call(self.trip, entity, timepool))
            
        if not itr >= self.fit: 
            ba.timer(self.clock, ba.Call(self.fetch_victims, itr+1))
        
append_chaos_event(SoKEveryoneTrips)

class SoKRockets(ChaosEvent):
    name = 'ROCKETS!'
    icon = 'chaosRockets'
    blacklist = [
        ba.CoopSession
    ]
    
    def event(self):
        self.d = duration = int(self._get_config()['time'] / 2)
        self.rocket_timer = RocketTimer(duration)
        
        self.engine_sound = ba.newnode(
                type='sound',
                attrs={
                    'sound': ba.getsound('engineSound'),
                    'positional': False,
                    'music': False,
                    'volume': 0.44,
                    'loop': True,
                },
            )
        
        self.biden_blast: ba.Node | None = None
        
        ba.timer(1, self.clock_timer)
        
        return duration
        
    def engine_pt2(self):
        ba.animate(self.engine_sound, 'volume', {
            0:0.44,
            0.2:0.5,
            1.2:0,
        })
        
        self.biden_blast = ba.newnode(
                type='sound',
                attrs={
                    'sound': ba.getsound('engineNear'),
                    'positional': False,
                    'music': False,
                    'volume': 0.75,
                    'loop': False,
                },
            )
        
        ba.animate(self.biden_blast, 'volume', {
            0:0,
            0.4:0.75,
        })
        
        ba.timer(2, self.engine_sound.delete)
        ba.timer(2, self.biden_blast.delete)
        
    def clock_timer(self):
        ''' Displays a countdown in the middle of the screen. '''
        self.rocket_timer.do_countdown()
        
        if self.d < 1:
            ba.playsound(ba.getsound('raceBeep2'), volume=0.5)
            self.liftoff()
            return
        
        elif self.d < 2:
            ba.timer(0.4, self.engine_pt2)
        
        self.d -= 1
        ba.playsound(ba.getsound('raceBeep1'), volume=0.5)
        ba.timer(1, self.clock_timer)
        
    def liftoff(self):
        ''' Lifts everyone... off? '''
        for entity in self._get_everyone():
            ba.timer(random.uniform(0.15, 1.5), ba.Call(self.spaz_lift, entity))
            
        def dodel(): del(self.rocket_timer)
        # Delete rocket_timer as we don't need it anymore
        ba.timer(3, dodel)
        
    def spaz_lift(self,
                  spaz: Spaz,
                  lstr: int = 70):
        if not spaz.node.exists(): return
        if (not spaz.is_alive() and lstr > 94):
            Blast(spaz.node.position, (0,0,0), 1.5, 'normal', spaz.source_player)
            return
        spaz.node.handlemessage('impulse',
                                spaz.node.position[0], spaz.node.position[1], spaz.node.position[2],
                                1.3, 1.3, 1.3,
                                lstr, lstr * 0.88, 0, 0,
                                0, 1, 0)
        ba.emitfx(
        position=spaz.node.position,
        velocity=spaz.node.velocity,
        count=2,
        spread=0,
        emit_type='tendrils',
        tendril_type='smoke',
        )
        
        ba.emitfx(
        position=spaz.node.position,
        velocity=spaz.node.velocity,
        count=5,
        spread=0,
        emit_type='tendrils',
        tendril_type='thin_smoke',
        )
        
        bseVFX('rocket', spaz.node.position, (0,-1,0))
        
        ba.timer(0.1, ba.Call(self.spaz_lift, spaz, lstr + 5))
        
class RocketTimer:
    def __init__(self,
                 count: int):
        self.count = count
    
    def do_countdown(self):
        text = (
            str(self.count) if not self.count < 1 else
            ba.Lstr(resource='explodinary.chaosEventTexts.liftoffText')
        )
        node = (
            ba.newnode(
                'text',
                attrs={
                    'text': text,
                    'maxwidth': 300,
                    'position': (0, -100),
                    'vr_depth': 10,
                    'h_attach': 'center',
                    'h_align': 'center',
                    'v_attach': 'center',
                    'v_align': 'center',
                    'color': (0.8, 0.8, 1.2, 0.75),
                    'shadow': 1,
                    'flatness': 1,
                    'scale': 2,
                    'opacity': 1,
                    'big': True,
                },
            )
        )
        ba.animate(node, 'scale', {
            0: node.scale,
            5: node.scale * 4,
        })
        ba.animate(node, 'opacity', {
            0: 1,
            1.4: 0,
        })
        self.count -= 1
        
        ba.timer(5, node.delete)
        
append_chaos_event(SoKRockets)

class SoKRandomBomb(ChaosEvent):
    name = 'Random Bomb'
    icon = 'chaosRandomBomb'
    
    def event(self):
        self.bpool = get_bomb_types(
            include_bombs=True,
            include_tnt=False,
            include_land_mines=False,
            include_projectiles=False,
            include_non_bombs=False,
        )
        
        for entity in self._get_everyone():
            self.switch_bomb(entity)

    def switch_bomb(self,
                    spaz: Spaz):
        if not spaz.node.exists() or not spaz.is_alive(): return
        
        # Internal crap
        if spaz._bomb_wear_off_timer:
            spaz._bomb_wear_off()
            
        spaz.node.mini_billboard_2_texture = ba.gettexture('empty')
        spaz.node.mini_billboard_2_start_time = 0
        spaz.node.mini_billboard_2_end_time = 0
        spaz._bomb_wear_off_flash_timer = None
        spaz._bomb_wear_off_timer = None
        
        # Set
        spaz.bomb_type = random.choice(self.bpool)
        
append_chaos_event(SoKRandomBomb)

class SoKBloodbath(ChaosEvent):
    name = 'Bloodbath'
    icon = 'chaosRedScreen'
    
    blacklist = [
        PathwayPandemoniumGame,
    ]

    def event(self):
        if self._get_variable('vfx', False): return False
        self._set_variable('vfx', True)
        
        duration = self._get_config()['time'] * 1.75
        
        self.do_bloodbath(duration)
        ba.timer(duration, ba.Call(self._set_variable, 'vfx', False))
        
        return duration
                
    def do_bloodbath(self, duration):
        ''' Turns the screen red. '''
        g = self.activity.globalsnode
        
        duration = (max(0.3, duration))
        
        ba.animate_array(g, 'tint', 3, {
            0: g.tint,
            1.5: (1, 0, 0),
            duration - 1.5: (1, 0, 0),
            duration:  g.tint,
        })
        
append_chaos_event(SoKBloodbath)

class SoKSlipperySlip(ChaosEvent):
    name = 'Slippery Slip'
    icon = 'chaosSlipperySlip'
    
    def event(self):
        if self._get_variable('is_slippery', False): return False
        
        duration = self._get_config()['time'] * 1.85 

        self.map_parts: list = []
        self.defaults: dict = {}
        
        # Add map parts
        for segment in dir(self.activity.map):
            this = getattr(self.activity.map, segment)
            if type(this) is ba.Node: self.map_parts.append(this)
            
        self.do_freeze()
        ba.timer(duration, self.do_thaw)
        
        return duration

    def do_freeze(self):
        self._set_variable('is_slippery', True)

        ba.playsound(ba.getsound('freeze'))
        icemat = ba.Material()
        icemat.add_actions(actions=('modify_part_collision','friction',0.03))
        for part in self.map_parts:
            if part.exists():
                try: 
                    name = str(part.getname())
                    # Save previous values
                    self.defaults[name] = [part.materials,
                                           part.color,
                                           part.reflection,
                                           part.reflection_scale]

                    if part.materials: part.materials = [part.materials[0], icemat]
                    else: part.materials = [icemat]
                    part.color              = (0.4,0.4,1.6)
                    part.reflection         = 'soft'
                    part.reflection_scale   = [0.9]
                except: pass

    def do_thaw(self):
        self._set_variable('is_slippery', False)
        
        for part in self.map_parts:
            if part.exists():
                try:
                    name = str(part.getname())
                    # Restore previous values!
                    part.materials          = self.defaults[name][0]
                    part.color              = self.defaults[name][1]
                    part.reflection         = self.defaults[name][2]
                    part.reflection_scale   = self.defaults[name][3]
                except: pass
                
append_chaos_event(SoKSlipperySlip)

class SoKARAU(ChaosEvent):
    name = 'At risk and unsafe!'
    icon = 'chaosAtRisk'
    
    def event(self):
        if self._get_variable('arau', False): return False
        self._set_variable('arau', True)
        
        duration = self._get_config()['time'] * 1.5
        
        self.extraimp = 4
        
        self.fit = fetch_iterations = int(duration * 3)
        self.clock = duration / fetch_iterations
        
        self._origin = {}
            
        self.fetch_victims(-1)
        ba.timer(duration, self.unarau)
        
        return duration
    
    def unarau(self): self._set_variable('arau', False)

    def fetch_victims(self,
                      itr: int = 0):
        ''' Finds victims and nerfs them. '''
        overdue = itr >= self.fit
        
        entity: Spaz
        for entity in self._get_everyone():
            if not entity.node.exists(): return
            
            impact_origin = self._origin.setdefault(entity, entity.impact_scale)
            
            entity.impact_scale = (
                impact_origin + (
                    0 if overdue else
                    ( self.extraimp * ( ( self.fit - itr ) / self.fit ) ) 
                    )
            )
            
        if not overdue: 
            ba.timer(self.clock, ba.Call(self.fetch_victims, itr+1))
            
append_chaos_event(SoKARAU)