import bascenev1 as bs
import random

from typing import Any

from bascenev1lib.gameutils import SharedObjects

rseed:int = 0
if rseed: random.seed(rseed)

class Particle(bs.Actor):
    def __init__(self,
                 args: dict):
        super().__init__()
        shared = SharedObjects.get()

        self.attrs = a = args

        m = bs.Material()
        m.add_actions(('modify_part_collision', 'collide', False))
        m.add_actions(('modify_part_collision', 'damping', a['damping']))
        m.add_actions(('modify_part_collision', 'stiffness', a['stiffness']))
        m.add_actions(
            conditions=('they_have_material', shared.footing_material),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'friction', a['friction']),
            ),
        )

        self.node = bs.newnode(
            'prop',
            delegate=self,
            attrs={
                'position'          : a['position'],
                'velocity'          : a['velocity'],
                'mesh'              : a['mesh'],
                'light_mesh'        : a['light_mesh'],
                'body'              : a['body'],
                'body_scale'        : a['body_scale'],
                'mesh_scale'        : a['mesh_scale'],
                'shadow_size'       : a['shadow_size'],
                'color_texture'     : a['color_texture'],
                #'color'            : a['color'],
                'reflection'        : a['reflection'],
                'reflection_scale'  : [a['reflection_scale']],
                'gravity_scale'     : a['gravity_scale'],
                'materials'         : [m],
            },
        )

        bs.animate(self.node, 'mesh_scale', {
            0:0,
            a['in']:a['mesh_scale'],
        })

        bs.timer(a['time']+a['in'], self._fade_out)

    def _fade_out(self):
        if self.node:
            bs.animate(self.node, 'mesh_scale', {
                0:self.node.mesh_scale,
                self.attrs['fade']:0,
            })
            bs.timer(self.attrs['fade'], bs.Call(self.handlemessage, bs.DieMessage()))

    def _die(self):
        """ Dye """
        if self.node: self.node.delete()
            
    def handlemessage(self, msg: Any) -> Any:
        """ Handles bunch'a stuff """
        if isinstance(msg, bs.DieMessage):
            self._die()
        else:
            super().handlemessage(msg)

class bseVFX:
    def __init__(self,
                 mode:str,
                 position:tuple[float,float,float],
                 velocity:tuple[float,float,float],
                 ):
        """ The backbone of all custom BSE particles. """
        self.pos = position
        self._mode = mode
        p = bs.app.config.get("BSE: Custom Particles", 'Max')

        # Don't show particles if Custom Particles is disabled.
        if p == 'None': return

        # Check if we need to reduce particles
        hq = True if p == 'Max' else False

        if mode == 'vitalbomb':
            # Petals
            petalspeed = ([(x*0.22 if i != 1 else 2) for i,x in enumerate(velocity)])
            itr = 6 if hq else 2
            self._generate('particlePetal', 'vitalBomb',
                           position,
                           petalspeed,
                           'landMine',
                           iterations=itr, spread=2.9,
                           body_scale=0.77, mesh_scale=1.66, shadow_size=0.005,
                           friction=1.55, stiffness=3, gravity_scale=0.42,
                           lifespan=3, lifefade=2,
                           )
            
            # Sparks
            sparkpos = ([(p if i != 1 else p+0.45) for i,p in enumerate(position)])
            itr = random.randint(6,11) if hq else 3
            self._generate('particleFlower', 'null',
                           sparkpos,
                           ([(random.uniform(-0.4, 0.4) if i != 1 else 
                              random.uniform(-0.45, -0.9)) for i in range(3)]),
                           'sphere', color=(1,0.22,1.2),
                           iterations=itr, spread=2, gravity_scale=-0.44,
                           lifespan=0, lifefade=1.22,
                           )
            
            # Leafs
            itr = random.randint(6,8) if hq else 2
            self._generate('particleLeaf', 'theBeginningLevelColor',
                           position,
                           ([(v*0.1 + (random.randint(-1, 1) * random.uniform(0.1, 3))) for v in velocity]),
                           'landMine',
                           iterations=itr, spread=[1,5],
                           body_scale=0.77, mesh_scale=[0.7,1.1], shadow_size=0.005, reflection_scale=0.7,
                           friction=[0.8,1.55], stiffness=1.2, gravity_scale=0.42,
                           lifespan=1, lifefade=4,
                           )
            
        elif mode == 'snowflake':
            # If low quality, give us a chance to *not* spawn snowflakes
            if not hq and random.random() > 0.6: return
            itr = random.randint(1,2) if hq else 1
            self._generate('bomb', 'null',
                           position, velocity, 'sphere', color=(2,2,2),
                           iterations=itr, spread=1.2,
                           body_scale=0.1, mesh_scale=0.3, shadow_size=0.005,
                           friction=5, damping=5, stiffness=5, gravity_scale=0,
                           fadein=0.1, lifespan=0, lifefade=[1.22,3.22],
                           )
            
        elif mode in ['snowpuff', 'rocket']:
            rocket = mode == 'rocket'
            
            itr = int(max(1, (17 if hq else 4) * (0.25 if rocket else 1)))
            spr = 0.4 if rocket else 1.8
            
            self._generate('bomb', 'null',
                           position, velocity, 'sphere', color=(2,2,2),
                           iterations=itr, spread=spr,
                           body_scale=0.1, mesh_scale=[0.39,0.56], shadow_size=0.005,
                           friction=3, damping=2, stiffness=50, gravity_scale=0.67,
                           fadein=0.07, lifespan=0, lifefade=[1,1.5],
                           )
            
        elif mode == 'blizzard':
            # If low quality, give us a chance to *not* spawn snowflakes
            if not hq and random.random() > 0.8: return
            itr = random.randint(2,3) if hq else 1
            self._generate('bomb', 'null',
                           position, velocity, 'sphere', color=(2,2,2),
                           iterations=itr, spread=1.2,
                           body_scale=0.1, mesh_scale=0.4, shadow_size=0.005,
                           friction=5, damping=5, stiffness=5, gravity_scale=0.1,
                           fadein=0.15, lifespan=0, lifefade=[2,3.5],
                           )
            
        elif mode == 'puff':
            itr = 19 if hq else 4
            self._generate('bomb', 'null',
                           ([p+(random.uniform(-0.1, 0.1) if i != 1 else 
                              random.uniform(0.4, -0.5)) for i,p in enumerate(position)]),
                           ([(random.uniform(-0.1, 0.1) if i != 1 else 
                              random.uniform(-0.15, -0.9)) for i in range(3)]),
                           'sphere', color=(1,0.22,1.2),
                           iterations=itr, spread=1.22, gravity_scale=-0.44,
                           body_scale=0.1, mesh_scale=0.4, shadow_size=0.005, reflection_scale=0,
                           lifespan=0, lifefade=1.22,
                           )
            
        elif mode == 'gone_puff':
            itr = 14 if hq else 3
            self._generate('bomb', 'null',
                           ([p+(random.uniform(-0.1, 0.1) if i != 1 else 
                              random.uniform(0.4, -0.5)) for i,p in enumerate(position)]),
                           ([(random.uniform(-0.1, 0.1) if i != 1 else 
                              random.uniform(-0.15, -0.3)) for i in range(3)]),
                           'sphere', color=(1,0.22,1.2),
                           iterations=itr, spread=1.22, gravity_scale=-0.2,
                           body_scale=0.22, mesh_scale=0.4, shadow_size=0.005, reflection_scale=0,
                           lifespan=0, lifefade=0.94,
                           )
            
        elif mode == 'thunderbolt':
            itr = 7 if hq else 4
            self._generate('bomb', 'null',
                           position,
                           ([(random.uniform(-0.5, 0.5) if i != 1 else 
                              random.uniform(-0.15, -0.2)) for i in range(3)]),
                           'sphere', color=(1,0.22,1.2),
                           iterations=itr, spread=1.66, gravity_scale=-1.2,
                           body_scale=0.02, mesh_scale=0.12, shadow_size=0.005, reflection_scale=2,
                           lifespan=0.2, lifefade=0.33,
                           )
            
        elif mode == 'confetti':
            itr = 24 if hq else 8
            texlist = ([f'confetti{v}' for v in [ "Blue","Green","Red","Yellow" ]])
            self._generate('particleConfetti', texlist,
                           position, velocity, 'landMine',
                           iterations=itr, spread=1.8,
                           body_scale=0.3, mesh_scale=[0.77, 1], shadow_size=0.005,
                           friction=3, damping=2, stiffness=12, gravity_scale=0.3,
                           fadein=0.07, lifespan=3, lifefade=[1,1.5],
                           )
            
        else: raise Exception(f'Type not identified: "{mode}"')

    def _generate(self,
                  mesh: str | bs.Mesh,
                  texture: str | bs.Texture,
                  position: tuple | None            = None,
                  velocity: tuple | None            = None,
                  body: str                         = 'box',
                  color: tuple                      = (1,1,1),
                  body_scale: float | list          = 1,
                  mesh_scale: float | list          = 1,
                  shadow_size: float | list         = 1,
                  reflection: str                   = 'soft',
                  reflection_scale: float | list    = 1.5,
                  gravity_scale: float | list       = 1,
                  iterations: int                   = 1,
                  spread: float | list              = 0,
                  friction: float | list            = 1,
                  damping: float | list             = 0,
                  stiffness: float | list           = 0, 
                  fadein: float | list              = 0,
                  lifespan: float | list            = 5,
                  lifefade: float | list            = 1,
                 ):
        """ Generates a custom prop that will function as particles. """
        real: dict = {
            'body_scale': body_scale,
            'mesh_scale': mesh_scale,
            'shadow_size': shadow_size,
            'reflection_scale': reflection_scale,
            'gravity_scale': gravity_scale,
            'spread': spread,
            'friction': friction,
            'damping': damping,
            'stiffness': stiffness,
            'fadein': fadein,
            'lifespan': lifespan,
            'lifefade': lifefade 
        }

        rd = [
            body_scale,
            mesh_scale,
            shadow_size,
            reflection_scale,
            gravity_scale,
            spread,
            friction,
            damping,
            stiffness,
            fadein,
            lifespan,
            lifefade 
        ]

        def randomize_randomizables():
            for i,k in enumerate(real.keys()):
                v = real[k]; og = rd[i]
                # Transform our valus to floats if they're a tuple or list
                if type(og) in [tuple, list]:
                    if len(og) > 1:
                        fv = random.uniform(og[0], og[1])
                    else:
                        fv = og[0]
                else:
                    fv = og
                real[k] = fv

        p = position if position else self.pos
        v = velocity if velocity else (0,0,0)

        for i in range(iterations):
            randomize_randomizables()
            # Tweak position and velocity using our spread value
            position = ([x + (random.uniform(-real['spread']/3, real['spread']/3) if real['spread'] else 0) for x in p])
            velocity = ([random.uniform(-real['spread']/1.25, real['spread']/1.25) + (x * random.uniform(1, real['spread'])) for x in v])
            
            # Choose a random mesh and texture if a list is assigned to them
            amesh = random.choice(mesh) if type(mesh) is list else mesh
            atexture = random.choice(texture) if type(texture) is list else texture
            
            # Get mesh / texture if the values are strings instead of their respective type
            if type(amesh) is str:     amesh = bs.getmesh(amesh)
            if type(atexture) is str:   atexture = bs.gettexture(atexture)

            prop = Particle({
                'position':         position,
                'velocity':         velocity,
                'mesh':            amesh,
                'light_mesh':      amesh,
                'body':             body,
                'body_scale':       real['body_scale'],
                'mesh_scale':      real['mesh_scale'],
                'shadow_size':      real['shadow_size'],
                'color_texture':    atexture,
                'color':            color,
                'reflection':       reflection,
                'reflection_scale': real['reflection_scale'],
                'gravity_scale':    real['gravity_scale'],

                'friction':         real['friction'],
                'damping':          real['damping'],
                'stiffness':        real['stiffness'],

                'in':               real['fadein'],
                'time':             real['lifespan'],
                'fade':             real['lifefade'],
            })