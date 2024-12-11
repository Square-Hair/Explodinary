import ba, _ba
import random
from typing import Any

from explodinary.chaos import ChaosEvent, append_chaos_event
from explodinary.chaos import shared
from bastd.gameutils import SharedObjects

from bastd.actor.spazappearance import Appearance, get_appearances
from explodinary.actor.glue import Glue
from bastd.actor.bomb import Bomb, Blast
from explodinary.custom.particle import bseVFX
from bastd.actor.spaz import Spaz
from bastd.actor.zoomtext import ZoomText
from bastd.actor.flag import Flag
from bastd.actor.powerupbox import PowerupBox, PowerupBoxFactory, DEFAULT_POWERUP_INTERVAL

from bastd.game.hockey import Puck
from bastd.game.easteregghunt import Egg
from explodinary.game import kablooyaRunaround, explodinaryRunaround, pathwayPandemonium
from bastd.game import runaround

from datetime import datetime

class TempProPlayers(ChaosEvent):
    name = 'Pro Players'
    icon = 'chaosProPlayers'

    def event(self):
        transmutes = [
            ba.app.spaz_appearances.get('Agent Johnson'),
            ba.app.spaz_appearances.get('Taobao Mascot'),
            ba.app.spaz_appearances.get('B-9000'),
        ]

        for spaz in self._get_everyone():
            if not spaz.node.exists(): continue
            transmute_choice = random.choice(transmutes)
            self.transmute(spaz, transmute_choice)

    def transmute(self, spaz: Spaz, transmute: Appearance):
        """ Make 'em pro. """
        # Transformio
        shared.transform_spaz_appearance(spaz, transmute)

        # Give 'em pro powerups!
        spaz.node.handlemessage(ba.PowerupMessage(poweruptype='impact_bombs', showtooltip=False))
        spaz.node.handlemessage(ba.PowerupMessage(poweruptype='shield', showtooltip=False))
        spaz.node.handlemessage(ba.PowerupMessage(poweruptype='punch', showtooltip=False))

append_chaos_event(TempProPlayers)

class TempHelloThere(ChaosEvent):
    name = 'Hello there!'
    icon = 'chaosHelloThere'

    def event(self):
        sfxpool = [f'HelloThere{"{:02}".format(n)}' for n in range(3)]
        duration = self._get_config()['time'] * 2

        creature = Creature()
        creature.fade_creature('in')
        ba.timer(max(0.01, duration-0.22), lambda: creature.fade_creature('out'))
        ba.timer(max(0.02, duration), lambda: creature.destroy_creature)

        ba.playsound( ba.getsound( random.choice(sfxpool) ) )

        return duration

class Creature:
    def __init__(
        self
    ):
        self.node: ba.Node = ba.newnode(
                'image',
                attrs={
                    'texture': ba.gettexture('helloThereTex'),
                    'absolute_scale': False,
                    'vr_depth': -20,
                    'position': (0,0),
                    'scale': (1,1),
                    'color': (0.7,0.7,0.7),
                    'opacity': 0,
                    'attach': 'center',
                },
           )
        #(random.uniform(-0.3,0.5),random.uniform(-0.05,0.1))
        self._position_creature()

    def _position_creature(self):
        """ Positions our creature. """
        h,v = random.uniform(-0.5,0.5), random.uniform(-0.1, -0.25)

        dpool = {
            'up': {
                'attach': 'topCenter',
                'rotate': 180,
                'pos': (h,v),
            },
            'down': {
                'attach': 'bottomCenter',
                'rotate': 0,
                'pos': (-h,-v),
            },
            'left': {
                'attach': 'centerLeft',
                'rotate': 270,
                'pos': (-v, -h),
            },
            'right': {
                'attach': 'centerRight',
                'rotate': 90,
                'pos': (v, h),
            }
        }

        cpos = dpool[random.choice( list( dpool.keys() ) )]

        self.node.attach = cpos['attach']
        self.node.rotate = cpos['rotate']
        self.node.position = cpos['pos']

    def fade_creature(self, mode: str = 'in'):
        """ Fades our Creature in and out, provided by the user. """
        if not self.node.exists(): return

        if mode == 'in': anim = [0,1]
        elif mode == 'out': anim = [1,0]
        else:
            raise Exception(f'Unable to fade creature with "{mode}".')

        ba.animate(self.node, 'opacity', {
            0: anim[0],
            0.22: anim[1],
        })

    def destroy_creature(self):
        """ KILLS the creature. :( """
        self.node.delete()

append_chaos_event(TempHelloThere)

class TempBlurryVision(ChaosEvent):
    name = 'Blurry Vision'
    icon = 'chaosBlurryVision'

    def event(self):
        """ Makes our vision blurry as heck. """
        if self._get_variable('is_blurry', False): return False

        duration = self._get_config()['time'] * 2.25

        self._set_variable('is_blurry', True)
        self.do_blur(duration)
        ba.timer(duration, self.take_it_back)

        return duration

    def do_blur(self, duration: float):
        """ Blur. """
        for chunk in dir(self.activity.map):
            tnode = getattr(self.activity.map, chunk)
            if type(tnode) == ba.Node:
                try:
                    ba.animate(tnode, 'opacity', {
                        0: tnode.opacity,
                        duration * 0.015: tnode.opacity*0.1,
                        duration - (duration*0.015): tnode.opacity*0.1,
                        duration: tnode.opacity,
                    })
                except: continue

    def take_it_back(self): self._set_variable('is_blurry', False)

append_chaos_event(TempBlurryVision)

class TempModernServer(ChaosEvent):
    name = 'Modern Server'
    icon = 'chaosModernServer'

    def event(self):
        self.texts = [
            "Join our discord!!",
            "type /rank to rank or something!",
            "Insanity",
            "the #1 (self proclaimed) best server!",
            "Buy now!",
            "Donate!! pls!!",
            "Looking for admin! Call now!",
            "We are recording you!",
            "Sample Text",
            "Don't look at the console, pls",
            "Packed with dopamine!",
            "Cheeseburger",
            "100% not stolen scripts! (lie)",
            "Revolutionary!!",
            "Sponsored by: Raid Shadow Legends",
            "Sponsored by: Lords Mobile",
            "Sponsored by: Eric Froemling himself!",
            "Sponsored by: My keyboard",
            "As painful as boiling water!",
            "We are collecting your data.",
            "Yeah uh-huh!",
            "Explodinary Servers! Official!",
            "Real SoK joined!!!?!",
            "lol!",
            "Server resets in 0:1:4!",
            "shoutout to all these people: ",
            "The",
            "ValueError: can't get string from value: \"serverTextRow\"",
            "Totally not a BombDash port!",
            "Original powerups!!",
            "Share with your friends!",
            "@efro give me repo perms pls!!",
            "@efro update game pls!!",
            "@efro add my map pls!!",
        ]

        duration = self._get_config()['time'] * 2.333
        iterations = random.randint(30, 55+(30 if not self._is_coop else 0))

        self.generate_mayhem(iterations, duration)

        return duration

    def generate_mayhem(self,
                        itr: int,
                        duration: float) -> float:
        """ Summons all those funny texts and returns the lifespan of all of them. """

        def create_offset(d: float) -> float: return d*(random.uniform(0.07,0.4))

        def create_text(fadein: float,
                        life: float,
                        fadeout: float):
            """ Actually creates and handles the text. """
            txt = ba.newnode(
                'text',
                attrs={
                    'text': ba.Lstr(translate=('chaosModernServer', random.choice(self.texts))),
                    'maxwidth': 300,
                    'position': (random.uniform(-550,550),
                                 random.uniform(-330,330)),
                    'h_attach': 'center',
                    'h_align': 'center',
                    'v_attach': 'center',
                    'v_align': 'center',
                    'vr_depth': random.uniform(-10,10),
                    'color': give_color(),
                    'rotate': random.uniform(-10, 10),
                    'scale': random.uniform(0.8, 1.5),
                },
            )

            ba.animate(txt, 'scale', {
                0:0,
                fadein:txt.scale,
                life-fadeout:txt.scale,
                life*0.95:txt.scale,
                life:0,
            })

            ba.timer(life, txt.delete)

        def give_color() -> tuple: return ([random.uniform(0.75,1.2) for x in range(4)])

        for i in range(itr):
            fi,fo = create_offset(duration), create_offset(duration)
            create_text(fi, duration, fo)

append_chaos_event(TempModernServer)

class TempSwitcheroo(ChaosEvent):
    name = 'Switcheroo'
    icon = 'chaosSwitcheroo'

    def event(self):
        """ Switches everyone's position! """
        # Return if we have less than 2 players and less than 2 bots
        players, bots = self._get_players(), self._get_bots()

        if ( len(players) < 2 and
             len(bots) < 2 ): return False

        _might_disappoint = True

        # We handle players and bots separately; we don't want funny mischief in modes like Runaround
        for group in [players, bots]:
            allpos: list = []
            for ent in group:
                if (ent.node.exists() and
                    ent.is_alive()):
                    # That's a long boi
                    allpos.append(tuple([x - (0 if i != 1 else 0.8) for i,x in enumerate(ent.node.position)]))
            if len(allpos) > 1:
                for ent in group:
                    if (ent.node.exists() and
                        ent.is_alive()):

                        sel = random.randint(0, len(allpos)-1)
                        pos = allpos[sel]

                        mpos_c, spos_c = ([round(x, 3) for x in ent.node.position]), ([round(x + (0 if i != 1 else 0.8), 3) for i,x in enumerate(pos)])

                        if mpos_c == spos_c:
                            sel = (sel+1) % len(allpos)
                            pos = allpos[sel]

                        allpos.pop(sel)

                        ent.handlemessage(ba.StandMessage(pos))
                        _might_disappoint = False

        if _might_disappoint: # If this happens, we didn't teleport anyone at all
                              # And it's better if we just reroll :p
            return False

append_chaos_event(TempSwitcheroo)

class TempMeteorShower(ChaosEvent):
    name = 'Meteor Shower'
    icon = 'chaosMeteorShower'

    def event(self):
        self.worldbounds = self.activity.map.get_def_bound_box('map_bounds')

        self.bombpool = (['normal']) if self._is_coop else self.get_bomb_pool()

        duration = self._get_config()['time'] * 2.5

        rate = 1 / (4 if self._is_coop else 8)

        self.activity._meteor_rain_clock = ba.Timer(rate, self.do_bomb, repeat=True)
        self.activity._meteor_rain_timer = ba.Timer(duration, self.stop)

        return duration

    def get_bomb_pool(self) -> list:
        return (
         ['normal'] * 66 +
         ['impact'] +
         ['tnt'] +
         ['tnt_ice'] +
         ['tnt_toxic'] +
         ['ice'] * 4 +
         ['toxic'] * 4 +
         ['sticky'] * 5 +
         ['tacky'] * 6 +
         ['steampunk'] * 5 +
         ['clouder'] * 5
        )

    def do_bomb(self):
        from bastd.actor.bomb import Bomb
        type = random.choice(self.bombpool)

        pos = (
            random.uniform(self.worldbounds[0], self.worldbounds[3],)*0.9,
            random.uniform(self.worldbounds[4], self.worldbounds[4],),
            random.uniform(self.worldbounds[2], self.worldbounds[5],)*0.9,
               )

        vel = (
            (-5.0 + random.random() * 15.0) * -( ( pos[0] - ( self.worldbounds[0] + self.worldbounds[3] ) / 2 ) / 4 ),
            random.uniform(-3.066, -4.12),
            (-5.0 + random.random() * 15.0) * -( ( pos[2] - ( self.worldbounds[2] + self.worldbounds[5] ) / 2 ) / 4 ),
        )

        Bomb(position=pos, velocity=vel, bomb_type=type).autoretain()

    def stop(self):
        self.activity._meteor_rain_clock = None
        self.activity._meteor_rain_timer = None

append_chaos_event(TempMeteorShower)

class TempAnvil(ChaosEvent):
    name = 'Anvil!'
    icon = 'chaosAnvil'
    blacklist = [
        ba.CoopSession
    ]

    def event(self):
        self._anvilmat = ba.Material()
        self._anvilmat.add_actions(
            conditions=('they_have_material', self._anvilmat),
            actions=(
                ('modify_part_collision', 'collide', False),
                ('modify_part_collision', 'physical', False),
            ),
        )

        if len(self._get_everyone()) < 1: return False

        ceilingpoint = self.activity.map.get_def_bound_box('map_bounds')[4]
        evtime = self._get_config()['time']; delay = random.uniform(0, min(3, evtime/3))

        def do_anvil(spaz: ba.Actor):
            if spaz.is_alive() and spaz.node.exists():
                avp = ([x if i != 1 else (min(ceilingpoint - 0.5, x + 7)) for i, x in enumerate(spaz.node.position)])
                Anvil(evtime*0.9, avp, self._is_coop, self._anvilmat).autoretain()

        def do_it():
            for entity in self._get_everyone():
                do_anvil(entity)

        ba.timer(delay, do_it)

        return {
            'delay': delay + 0.1
        }

class Anvil(ba.Actor):
    def __init__(self,
                 frequency: float,
                 position:  tuple,
                 is_coop:   bool,
                 anvilmat:  ba.Material):
        super().__init__()
        shared = SharedObjects.get()

        self._len = frequency
        self._is_coop = is_coop

        squishmat = ba.Material()
        squishmat.add_actions(
            conditions=('they_have_material', shared.object_material),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('call', 'at_connect', self._squash),
            ),
        )

        dinkmat = ba.Material()
        dinkmat.add_actions(
            conditions=('they_have_material', shared.footing_material),
            actions=(
                ('impact_sound', ba.getsound('anvilHit'), 2, 0.8),
            ),
        )

        self._missmats = [squishmat, shared.footing_material, anvilmat, dinkmat]
        self._hitmats = [shared.footing_material, anvilmat]

        self.node = ba.newnode(
            'prop',
            delegate=self,
            attrs={
                'position': position,
                'velocity': (0,-6,0),
                'model': ba.getmodel('anvilModel'),
                'light_model': ba.getmodel('anvilModel'),
                'body': 'crate',
                'body_scale': 1.5,
                'model_scale': 0.75,
                'shadow_size': 1.0,
                'color_texture': ba.gettexture('anvilColor'),
                'reflection': 'powerup',
                'reflection_scale': [2],
                'materials': self._missmats,
                'gravity_scale': 5,
                'density': 0.7
            })
        ba.animate(self.node, 'model_scale', {0: 0, 0.2: 1.3, 0.26: self.node.model_scale})
        ba.timer(self._len, self._handle_magic_disappear)

    def _squash(self):
        from bastd.actor.spaz import Spaz
        from bastd.actor.bomb import Bomb, Blast
        from bastd.actor.powerupbox import PowerupBox
        collision = ba.getcollision()
        try:
            if not self.node.velocity[1] < -10: return
            them = collision.opposingnode.getdelegate(ba.Actor, None)
            tnode = them.node
            they = type(them)

            if they is Bomb:
                them.explode()

            elif they is PowerupBox:
                Blast(tnode.position, (0,0,0), 1.33)

            else:
                try:
                    if them.is_alive():
                        ba.playsound(ba.getsound('anvilGib'), 1.25, tnode.position)
                    tnode.handlemessage('impulse', tnode.position[0], tnode.position[1], tnode.position[2],
                                                0, 0, 0,
                                                -1200, -1200, 0, 0, 0, 1, 0)
                    them.shatter(extreme=True)
                    self.node.materials = self._hitmats
                except:
                    try: them.delete()
                    except: pass


        except ba.NotFoundError:
            return

    def _handle_magic_disappear(self):
        if self.node.exists():
            ba.emitfx(position=self.node.position,
                      count=16,
                      scale=2,
                      spread=1.1,
                      chunk_type='spark')
            self.handlemessage(ba.DieMessage())


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

append_chaos_event(TempAnvil)

class TempMexicoFilter(ChaosEvent):
    name = 'Obligatory Mexico Filter'
    icon = 'chaosMexicanFilter'

    blacklist = [
        pathwayPandemonium.PathwayPandemoniumGame,
    ]

    def event(self):
        if self._get_variable('vfx', False): return False
        self._set_variable('vfx', True)

        duration = self._get_config()['time'] * 1.6

        self.do_sepia(duration)
        ba.timer(duration, ba.Call(self._set_variable, 'vfx', False))

        return duration

    def do_sepia(self, duration):
        """ Sepias the screen. """
        g = self.activity.globalsnode

        duration = (max(0.3, duration))

        ba.animate_array(g, 'tint', 3, {
            0: g.tint,
            0.1: (1.5, 1.2, 0.4),
            duration - 0.1: (1.5, 1.2, 0.4),
            duration:  g.tint,
        })

append_chaos_event(TempMexicoFilter)

class TempStreamerMode(ChaosEvent):
    name = 'Streamer Mode'
    icon = 'chaosStreamerMode'

    def event(self):
        transmutes = [ba.app.spaz_appearances.get(x) for x in get_appearances()]

        for spaz in self._get_everyone():
            if not spaz.node.exists(): continue
            transmute_choice = random.choice(transmutes)
            self.transmute(spaz, transmute_choice)

        # Add "is_area_of_interest" to bots so the camera follows them as well
        for bot in self._get_bots():
            bot.node.is_area_of_interest = True

    def transmute(self, spaz: Spaz, transmute: Appearance):
        """ Confuse the heck out of everyone by randomizing everyone's character and name! """
        # Transformio
        shared.transform_spaz_appearance(spaz, transmute)

        main, high = self.random_color(), self.random_color()
        spaz.node.color     = main
        spaz.node.name_color= main
        spaz.node.highlight = high
        spaz.node.name      = random.choice( ba.internal.get_random_names() )

    def random_color(self): return tuple([random.randint(0,255)/255 for x in range(3)])

append_chaos_event(TempStreamerMode)

class TempSuddenEggHunt(ChaosEvent):
    name = 'Sudden Egg Hunt'
    icon = 'chaosEggHunt'

    blacklist = [
        ba.CoopSession
    ]

    def event(self):
        self.eggmat = ba.Material()
        self.eggmat.add_actions(
            conditions=('they_have_material', SharedObjects.get().player_material),
            actions=(('call', 'at_connect', self._egg_pickup),),
        )

        self.worldbounds = self.activity.map.get_def_bound_box('map_bounds')

        # Bunnies!
        for entity in self._get_everyone():
            self.bunnify(entity)

        # Egg spawning
        egg_a = random.randint(20, 30)
        for _ in range(egg_a):
            pos = (
                random.uniform(self.worldbounds[0], self.worldbounds[3],) * 0.76,
                random.uniform(self.worldbounds[4], self.worldbounds[4],) - 0.5,
                random.uniform(self.worldbounds[2], self.worldbounds[5],) * 0.76,
            )

            lifespan = (self._get_config()['time'] * 4) * random.uniform(0.6, 1.2)

            ExplosiveEgg(pos, self.eggmat, lifespan).autoretain()

    def _egg_pickup(self) -> None:
        """ Make our egg explode when picked up by a live player. """
        collision = ba.getcollision()

        # Prevent this from running if picked up by a non-spaz entity
        try:
            egg = collision.sourcenode.getdelegate(ExplosiveEgg, True)
            spaz: Spaz = collision.opposingnode.getdelegate(
                Spaz, True)
        except ba.NotFoundError:
            return

        # Summon an explosion in the egg's position and delete it afterwards
        Blast(egg.node.position, (0,0,0), 2.5, 'normal', spaz.source_player)
        egg.handlemessage(ba.DieMessage())

    def bunnify(self,
                spaz: Spaz):
        """ Transforms this spaz into a bunny. """
        # Don't run if this player's spaz node doesn't exist.
        if not spaz.node.exists(): return

        # Get our appearance set
        basebun = ba.app.spaz_appearances.get('Easter Bunny')

        # Override sounds
        spaz.node.attack_sounds         = [ba.getsound(s) for s in basebun.attack_sounds]
        spaz.node.jump_sounds           = [ba.getsound(s) for s in basebun.jump_sounds]
        spaz.node.impact_sounds         = [ba.getsound(s) for s in basebun.impact_sounds]
        spaz.node.pickup_sounds         = [ba.getsound(s) for s in basebun.pickup_sounds]
        spaz.node.death_sounds          = [ba.getsound(s) for s in basebun.death_sounds]
        spaz.node.fall_sounds           = [ba.getsound(s) for s in basebun.fall_sounds]
        # Override textures
        spaz.node.color_texture         = ba.gettexture(basebun.color_texture)
        spaz.node.color_mask_texture    = ba.gettexture(basebun.color_mask_texture)
        # Override models
        spaz.node.head_model            = ba.getmodel(basebun.head_model)
        spaz.node.torso_model           = ba.getmodel(basebun.torso_model)
        spaz.node.pelvis_model          = ba.getmodel(basebun.pelvis_model)
        spaz.node.upper_arm_model       = ba.getmodel(basebun.upper_arm_model)
        spaz.node.forearm_model         = ba.getmodel(basebun.forearm_model)
        spaz.node.hand_model            = ba.getmodel(basebun.hand_model)
        spaz.node.upper_leg_model       = ba.getmodel(basebun.upper_leg_model)
        spaz.node.lower_leg_model       = ba.getmodel(basebun.lower_leg_model)
        spaz.node.toes_model            = ba.getmodel(basebun.toes_model)

class ExplosiveEgg(ba.Actor):
    """ Custom Egg Entity for our Sudden Egg Hunt event. """
    def __init__(self,
                 position: tuple,
                 eggmat: ba.Material,
                 lifespan: float):
        super().__init__()

        shared = SharedObjects.get()

        texpool = [
            ba.gettexture('bombColor'),
            ba.gettexture('bombColorIce'),
            ba.gettexture('bombStickyColor'),
        ]
        ctex = random.choice(texpool)

        self._spawn_pos = (position[0], position[1] + 0.5, position[2])
        mats = [shared.object_material, eggmat]

        self.node = ba.newnode(
            'prop',
            delegate=self,
            attrs={
                'model': ba.getmodel('egg'),
                'color_texture': ctex,
                'body': 'capsule',
                'reflection': 'soft',
                'model_scale': 0.5,
                'body_scale': 0.6,
                'density': 4.0,
                'reflection_scale': [0.15],
                'shadow_size': 0.6,
                'position': self._spawn_pos,
                'materials': mats,
            },
        )

        # Death anim
        ba.animate(self.node, 'model_scale', {
            0:self.node.model_scale,
            lifespan*0.95:self.node.model_scale,
            lifespan:0,
        })
        ba.timer(lifespan, ba.Call(self.handlemessage, ba.DieMessage()))

    def exists(self) -> bool: return bool(self.node)

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):
            if self.node:
                self.node.delete()
        elif isinstance(msg, ba.OutOfBoundsMessage):
            self.handlemessage(ba.DieMessage())
        elif isinstance(msg, ba.HitMessage):
            if self.node:
                self.node.handlemessage(
                    'impulse',
                    msg.pos[0],
                    msg.pos[1],
                    msg.pos[2],
                    msg.velocity[0],
                    msg.velocity[1],
                    msg.velocity[2],
                    1.0 * msg.magnitude,
                    1.0 * msg.velocity_magnitude,
                    msg.radius,
                    0,
                    msg.force_direction[0],
                    msg.force_direction[1],
                    msg.force_direction[2],
                )
        else:
            super().handlemessage(msg)

append_chaos_event(TempSuddenEggHunt)

class TempNothing(ChaosEvent):
    name = 'Nothing!'
    icon = 'chaosNothing'

    def event(self):
        real = random.uniform(1,10) < 9

        # If we're "real", don't do absolutely nothing
        if real:
            return

        # Else, fake a nothing, and then pick another event afterwards
        else:
            delay = self._get_config()['time'] * random.uniform(0.4, 0.7)
            self.fake_announce()
            ba.timer(delay-0.9, ba.Call(self.fake_announce, 'Sike!'))
            ba.timer(delay+0.4, self.manager.do_event)
            return {
                'announce': False,
                'delay': delay
            }

    def fake_announce(self,
                      txt: str | ba.Lstr = None ):
        """ Does a fake announce text thing. """
        if not txt: txt = ba.Lstr(translate=('chaosEventNames', self.name))
        ba.timer(0.25, lambda: ba.playsound(ba.getsound('scoreHit01')))
        ZoomText(
            txt,
            lifespan=1.25,
            jitter=2.0,
            position=(0, -230 - 1 * 20),
            scale=0.7,
            maxwidth=800,
            trail=True,
            color=(0.7,1.1,0.95),
        ).autoretain()

append_chaos_event(TempNothing)

class TempDashing(ChaosEvent):
    name = 'Quite Dashing'
    icon = 'powerupDash'

    def event(self):
        spaz: Spaz

        for spaz in self._get_players():
            spaz.reset_powerup_count()
            spaz.set_dash_count(
                (6 if self._is_coop else
                ( spaz.dash_count + random.randint(4,12) ) ))
            bseVFX('puff', spaz.node.position, (0,-1,0))

append_chaos_event(TempDashing)

class TempEpicTime(ChaosEvent):
    name = 'So Epic!'
    icon = 'chaosEpic'

    def event(self):
        if self._get_variable('so_epic', False): return False
        self._set_variable('so_epic', True)

        #self.announce()

        self.clock = duration = ( self._get_config()['time'] * 1.8 ) * ( 1.5 if self.activity.globalsnode.slow_motion else 1 )
        self.clock *= 30

        self.switch_mode(False)
        self.timer: ba.Timer | None = ba.Timer(
                                              1/30,
                                              self._update,
                                              repeat=True,
                                              timetype=ba.TimeType.BASE
                                              )

        return {
            'time': duration,
            'timetype': ba.TimeType.BASE
        }

    def _update(self):
        if not self.activity.globalsnode.paused:
            self.time_down()

    def time_down(self):
        self.clock -= 1

        if self.clock <= 0:
            self.switch_mode()
            self.timer = None

    def switch_mode(self, end = True):
        """ Toggles slow motion. """
        self.activity.globalsnode.slow_motion = not self.activity.globalsnode.slow_motion
        # Set variable to False when ending
        if end:
            self._set_variable('so_epic', False)

    def announce(self):
        ZoomText(
            ba.Lstr(translate=('chaosEventNames', f'So {"Epic" if not self.activity.globalsnode.slow_motion else "Normal"}!')),
            lifespan=1.25,
            jitter=2.0,
            position=(0, -230 - 1 * 20),
            scale=0.7,
            maxwidth=800,
            trail=True,
            color=(0.7,1.1,0.95),
        ).autoretain()

append_chaos_event(TempEpicTime)

class TempDiscordStage(ChaosEvent):
    name = 'Coffee Time!'
    icon = 'chaosCoffee'

    def event(self):
        """"""

class StagePopupManager:
    """"""

#append_chaos_event(TempDiscordStage)

class TempWindowsNotifications(ChaosEvent):
    name = 'Windows Alerts'
    icon = 'chaosWindows'

    def event(self):
        self.phandler = WindowsPopupHandler()

class WindowsPopupHandler:
    def __init__(self) -> None:
        self._dying = False
        self.notifs: dict = {}; self.itr = -1

    def add_notif(self):
        itr = self.itr = self.itr + 1

        self.notifs[itr](
            ba.newnode(
                'text',
                attrs={
                    'text': ba.Lstr(translate=('chaosModernServer', random.choice(self.texts))),
                    'maxwidth': 300,
                    'position': (random.uniform(-550,550),
                                 random.uniform(-330,330)),
                    'h_attach': 'center',
                    'h_align': 'center',
                    'v_attach': 'center',
                    'v_align': 'center',
                    'vr_depth': random.uniform(-10,10),
                    'color': (1,1,1),
                    'rotate': random.uniform(-10, 10),
                    'scale': random.uniform(0.8, 1.5),
                },
            )
        )

    def die(self):
        self._dying = True

class WindowsPopupNode:
    def __init__(
        self,
        icon_texture: str | ba.Texture,
        app_title: str,
        window_title: str | None,
        message_header: str | None,
        message: str | None,
        side_image: str | ba.Texture | None = None,
        sound: str | ba.Sound | None = None,
        size: tuple = (363,54),
        ) -> None:
        """ Creates a spot-on fake windows pop-up with the provided characteristics. """
        icon = icon_texture
        app = app_title
        title = window_title
        msgtop = message_header
        msg = message
        thb = side_image

        titleextra = 38.35 if title else 0
        headerextra = 26 if msgtop else 0
        msgjust = ((20 + (17.55 * (len(msg.splitlines())))) + (8 if thb and len(msg.splitlines()) < 2 else 0)) if msg else 0
        sx,sy = size[0], (size[1] + msgjust + titleextra + headerextra)

        ox,oy = -17,53
        ics = 16
        xbs = 10
        bis = 59
        smult = 0.63

        imgoff = bis + 16 if thb else 0

        bgsize = ([s * smult for s in [sx,sy]])
        offset = ([(p * smult) - ((bgsize[i] / 2) * (1 if i == 0 else -1)) for i,p in enumerate([ox,oy])])

        basepos = ([(p - ((sx,sy)[i]/2 *smult)) for i,p in enumerate(offset)])

        icotex = ba.gettexture(icon) if type(icon) is str else icon
        bartex = (ba.gettexture(thb) if type(thb) is str else thb) if thb else None

        icos = ics*smult; icosize = ([icos for _ in range(2)])
        icooff = ((icos/2) + (16*smult),
                  -(icos/2) + ((sy - 19)*smult))
        icopos = ([p + (icooff[i]) for i,p in enumerate(basepos)])

        bims = bis*smult; bimsize = ([bims for _ in range(2)])

        xbsi = xbs*smult; xbsize = ([xbsi for _ in range(2)])
        xboff = (((sx-22)*smult) - (xbsi/2),
                 ((sy-21)*smult) - (xbsi/2),
                 )
        xbpos = ([p + (xboff[i]) for i,p in enumerate(basepos)])

        appoffx = (10,0)
        apppos = ([p + (appoffx[i]) for i,p in enumerate(icopos)])

        tleoff = ((16*smult),
                  ((sy - 61)*smult))
        tlepos = ([p + (tleoff[i]) for i,p in enumerate(basepos)])

        simoff = (16 + (bis/2), 37.35-10-(bis/2) +msgjust)
        simpos = ([p + (simoff[i]*smult) for i,p in enumerate(basepos)])

        mtloff = (16 + imgoff, 37.35-20 +msgjust)
        mtlpos = ([p + (mtloff[i]*smult) for i,p in enumerate(basepos)])

        msgoff = (16 + imgoff, 26.35-20 +msgjust)
        msgpos = ([p + (msgoff[i]*smult) for i,p in enumerate(basepos)])

        self.backgroundblur: ba.Node = ba.newnode(
            'image',
            attrs={
                'texture': ba.gettexture('popupBlur'),
                'absolute_scale': True,
                'vr_depth': -20,
                'position': offset,
                'scale': bgsize,
                'color': (0.1, 0.1, 0.1),
                'opacity': 0.44,
                'attach': 'bottomRight',
            },
        )

        self.background: ba.Node = ba.newnode(
            'image',
            attrs={
                'texture': ba.gettexture('null'),
                'absolute_scale': True,
                'vr_depth': -20,
                'position': offset,
                'scale': bgsize,
                'color': (0.1, 0.1, 0.1),
                'opacity': 0.66,
                'attach': 'bottomRight',
            },
        )

        self.icon: ba.Node = ba.newnode(
            'image',
            attrs={
                'texture': icotex,
                'absolute_scale': True,
                'vr_depth': -20,
                'position': icopos,
                'scale': icosize,
                'color': (1, 1, 1),
                'opacity': 1,
                'attach': 'bottomRight',
            },
        )

        self.xicon: ba.Node = ba.newnode(
            'image',
            attrs={
                'texture': ba.gettexture('popupClose'),
                'absolute_scale': True,
                'vr_depth': -20,
                'position': xbpos,
                'scale': xbsize,
                'color': (1, 1, 1),
                'opacity': 0.44,
                'attach': 'bottomRight',
            },
        )

        self.app_text: ba.Node = ba.newnode(
            'text',
            attrs={
                'text': app,
                'maxwidth': sx/smult,
                'position': apppos,
                'h_attach': 'right',
                'h_align': 'left',
                'v_attach': 'bottom',
                'v_align': 'center',
                'vr_depth': -5,
                'color': tuple([2 for _ in range(3)]),
                'scale': 0.4905*smult,# 0.3088
            },
        )

        if title:
            self.app_title: ba.Node = ba.newnode(
                'text',
                attrs={
                    'text': title,
                    'maxwidth': sx/smult *0.966,
                    'position': tlepos,
                    'h_attach': 'right',
                    'h_align': 'left',
                    'v_attach': 'bottom',
                    'v_align': 'center',
                    'vr_depth': -5,
                    'color': tuple([2.6 for _ in range(3)]),
                    'scale': 0.5873*smult,
                },
            )

        if msgtop:
            self.msg_title: ba.Node = ba.newnode(
                'text',
                attrs={
                    'text': msgtop,
                    'maxwidth': sx/smult * 0.966,
                    'position': mtlpos,
                    'h_attach': 'right',
                    'h_align': 'left',
                    'v_attach': 'bottom',
                    'v_align': 'center',
                    'vr_depth': -5,
                    'color': tuple([2.6 for _ in range(3)]),
                    'scale': 0.5873*smult,
                },
            )

        if msg:
            self.msg_body: ba.Node = ba.newnode(
                'text',
                attrs={
                    'text': msg,
                    'position': msgpos,
                    'h_attach': 'right',
                    'h_align': 'left',
                    'v_attach': 'bottom',
                    'v_align': 'top',
                    'vr_depth': -5,
                    'color': tuple([1.0 if i != 3 else 0.5 for i in range(4)]),
                    'scale': 0.553*smult,
                },
            )

        if thb:
            self.sidepic: ba.Node = ba.newnode(
                'image',
                attrs={
                    'texture': bartex,
                    'absolute_scale': True,
                    'vr_depth': -20,
                    'position': simpos,
                    'scale': bimsize,
                    'color': (1, 1, 1),
                    'opacity': 1,
                    'attach': 'bottomRight',
                },
            )

        if sound: self._sound(sound)

    def _sound(self,
               sound):
        sound = ba.getsound(sound) if type(sound) is str else sound
        ba.playsound(sound)

class TempGameReset(ChaosEvent):
    name = 'Game Reset'
    icon = 'chaosReset'

    blacklist = [
        ba.CoopSession
    ]

    def event(self):
        """ Resets everyone's scores and kills thrown bombs. """
        # Make the event less likely to happen by rolling a random 0 to 1 number
        if not random.random() > 0.975: return False

        self.reset_scores()

        delist = [Bomb, Egg, Flag, PowerupBox, Puck]

        for node in ba.getnodes():
            try:
                for tdel in delist:
                    if node.getdelegate(tdel, None):
                        self.node_fulmination(node)
            except ba.NodeNotFoundError: continue

        for player in self.activity.players:
            self.reset_lives(player)
            self.relocate_player(player)

    def node_fulmination(self, node: ba.Node):
        """ Nukes the provided node with a cool puff animation. """
        if not node.exists(): return

        try: vel = node.velocity
        except: vel = (0,0,0)

        bseVFX('puff',
               node.position,
               vel)
        if node.getdelegate(Spaz, None): return
        node.handlemessage(ba.DieMessage())

    def reset_scores(self):
        """ Resets all players' scores. """
        try:
            for team in self.activity.teams:
                team.score = 0
        except: return

        try:
            self.activity._update_scoreboard()
        except: return

    def reset_lives(self, player: Spaz):
        """ Resets a player's lives in modes like Elimination. """
        try:
            player.lives = self.activity.settings_raw['Lives Per Player']+1
            self.activity._update_icons()
        except: return

    def relocate_player(self, player):
        """ StandMessage-s a player to their respective respawn location. """
        spaz: Spaz = player.actor
        if not spaz.node.exists(): return

        # Cool particles
        bseVFX('puff',
               spaz.node.position,
               spaz.node.velocity)

        # Relocate
        position = (self.activity.map.get_start_position(player.team.id) if isinstance(self.session, ba.DualTeamSession) else
                    self.activity.map.get_ffa_start_position(self.activity.players))
        spaz.node.handlemessage(ba.StandMessage(position, random.uniform(0,360)))

        # Reset some standard values
        spaz.hitpoints = spaz.hitpoints_max
        spaz.node.hurt = 0

        if spaz.shield:
            spaz.shield.delete()
            spaz.shield = None
            spaz.shield_decay_timer = None

        # Unvital, reset count powerups
        spaz.unvital()
        spaz.reset_powerup_count()

        # Remove triple bombs
        spaz.node.mini_billboard_1_texture = ba.gettexture('empty')
        spaz.node.mini_billboard_1_start_time = 0
        spaz.node.mini_billboard_1_end_time = 0
        spaz._multi_bomb_wear_off_flash_timer = None
        spaz._multi_bomb_wear_off_timer = None
        spaz._multi_bomb_wear_off()

        # Remove bomb type
        spaz.node.mini_billboard_2_texture = ba.gettexture('empty')
        spaz.node.mini_billboard_2_start_time = 0
        spaz.node.mini_billboard_2_end_time = 0
        spaz._bomb_wear_off_flash_timer = None
        spaz._bomb_wear_off_timer = None
        spaz._bomb_wear_off()

        # Remove gloves
        spaz.node.mini_billboard_3_texture = ba.gettexture('empty')
        spaz.node.mini_billboard_3_start_time = 0
        spaz.node.mini_billboard_3_end_time = 0
        spaz._boxing_gloves_wear_off_flash_timer = None
        spaz._boxing_gloves_wear_off_timer = None
        spaz._flying_gloves_wear_off()
        spaz._gloves_wear_off()

        # Call a healie cuz I'm too lazy to remove all negative effects manually
        spaz.handlemessage(ba.PowerupMessage('health', None, False))

        # Unfreeze
        spaz.handlemessage(ba.ThawMessage())

append_chaos_event(TempGameReset)

class TempPowerupBait(ChaosEvent):
    name = 'Powerup Bait'
    icon = 'chaosBait'

    blacklist = [
        ba.CoopSession
    ]

    def event(self):
        """ Switches and replaces all powerups with curses! :)
            Also increases their lifespan just for the funsies. """

        texpool = [
            'powerupBomb',
            'powerupPunch',
            'powerupDash',
            'chaosJumpymania',
            'powerupIceBombs',
            'powerupStickyBombs',
            'powerupTackyBombs',
            'powerupVitalBombs',
            'powerupClouder',
            'powerupSteampunk',
            'powerupClusterBombs',
            'powerupToxicBombs',
            'powerupFlutterMines',
            'powerupGlueMines',
            'powerupShield',
            'powerupImpactBombs',
            'powerupHealth',
            'powerupVitamin',
            'powerupLandMines',
            'powerupSkyMines',
            'powerupPresent',
            ]

        node: ba.Node
        for node in ba.getnodes():
            if node.getdelegate(PowerupBox, None):
                powerup: PowerupBox = node.getdelegate(PowerupBox, None)
                powerup.poweruptype = 'curse'
                powerup.expire_flash_timer = ba.Timer(
                    DEFAULT_POWERUP_INTERVAL - 2.35,
                    ba.WeakCall(powerup._start_flashing),
                )
                powerup.expire_timer = ba.Timer(
                    DEFAULT_POWERUP_INTERVAL - 0.75,
                    ba.WeakCall(powerup.handlemessage, ba.DieMessage()),
                )

                node.color_texture = ba.gettexture(random.choice(texpool))
                node.flashing = False

append_chaos_event(TempPowerupBait)

class TempPowerupBlast(ChaosEvent):
    name = 'Powerup Blast'
    icon = 'chaosPowerupBlast'

    def event(self):
        """ Spawns a powerup in top of a powerup in top of a powerup in top of a powerup in top... """
        nodes = []

        node: ba.Node
        for node in ba.getnodes():
            if node.getdelegate(PowerupBox, None):
                nodes.append(node)

        # Reroll event if there's no powerup boxes
        if not len(nodes) > 0: return False

        eitr = [3, 15]
        for i in range(len(nodes)):
            if i > 9:
                eitr = [max(1, eitr[1]*0.33), max(1, eitr[1] - 1)]
                eitr = ([int(v) for v in eitr])

        for node in nodes:
            offs = 0.4
            itr = random.randint(eitr[0], eitr[1])
            for i in range(itr):
                pos = ([p + (offs if i == 1 else 0) for p in node.position])
                PowerupBox(
                    position=pos,
                    poweruptype=PowerupBoxFactory.get().get_random_powerup_type(
                        excludetypes='curse' if self._is_coop else None
                        ),
                ).autoretain()

append_chaos_event(TempPowerupBlast)

class TempDrunkCameraMan(ChaosEvent):
    name = 'Drunk Cameraman'
    icon = 'chaosCamera'

    def event(self):
        if self._get_variable('drunken', False): return False
        self._set_variable('drunken', True)

        self.defaults = {}

        self.update_defaults()

        duration = self._get_config()['time'] * 1.5
        self.switches = switches = random.randint(int(duration/2), int(duration*2))
        self.st = switchtime = duration/switches

        self.camera_routine()

        return duration

    def update_defaults(self):
        for node in ba.getnodes():
            try:
                if self.defaults.get(node, 'nope') != 'nope': continue
                self.defaults[node] = node.is_area_of_interest
            except: continue

    def restore_defaults(self):
        for group in self.defaults.items():
            try:
                node = group[0]; d = group[1]
                node.is_area_of_interest = d
            except ba.NodeNotFoundError: continue

        self._set_variable('drunken', False)

    def camera_routine(self, itr:int = 0):
        self.update_defaults()

        itr += 1
        if not itr > self.switches:
            cnodes = []
            for node in ba.getnodes():
                try:
                    node.is_area_of_interest = False
                    cnodes.append(node)
                except: continue

            random.choice(cnodes).is_area_of_interest = True

            ba.timer(self.st, ba.Call(self.camera_routine, itr))

        else: self.restore_defaults()

append_chaos_event(TempDrunkCameraMan)

class TempScreenFilter(ChaosEvent):
    name = 'Screen Filter'
    icon = 'chaosFilter'

    def event(self):
        if self._get_variable('vfx', False): return False
        self._set_variable('vfx', True)

        self.overlay: ba.Node | None = None

        self.d = duration = self._get_config()['time'] * 2.15

        color = ([random.uniform(0,1) for _ in range(3)])
        self.overlap_image(color)
        ba.timer(duration, self.overgone)

        return duration

    def overlap_image(self,
                      color: tuple):
        """ Creates an overlay image with the provided color. """
        self.overlay = ba.newnode(
            'image',
            delegate=self,
            attrs={
                'fill_screen': True,
                'texture': ba.gettexture('null'),
                'color': color,
                'opacity': 0,
            },
        )

        ba.animate(self.overlay, 'opacity', {
            0               : 0,
            self.d*0.075    : 0.66,
        })

    def overgone(self):
        """ Deletes the overlay. """
        if self.overlay:
            ba.animate(self.overlay, 'opacity', {
                0               : self.overlay.opacity,
                self.d*0.075    : 0,
            })
            ba.timer(self.d*0.08, self.overlay.delete)

        self._set_variable('vfx', False)

append_chaos_event(TempScreenFilter)

class TempBrokenScreen(ChaosEvent):
    name = 'Oops! Broken Screen!'
    icon = 'chaosBrokenScreen'

    def event(self):
        if self._get_variable('vfx', False): return False
        self._set_variable('vfx', True)

        self.overlay: ba.Node | None = None

        self.d = duration = self._get_config()['time'] * 1.77

        self.overlap_image()
        ba.timer(duration, self.overgone)

        return duration

    def overlap_image(self):
        """ Creates an overlay image with the provided color. """
        self.overlay = ba.newnode(
            'image',
            delegate=self,
            attrs={
                'fill_screen': True,
                'texture': ba.gettexture('youDroppedYourPhoneDummy'),
                'color': (1,1,1),
                'opacity': 0,
            },
        )

        ba.playsound(ba.getsound('youDroppedYourAudioFileSilly'), volume=2.7)

        ba.animate(self.overlay, 'opacity', {
            0               : 0,
            self.d*0.004    : 1,
            self.d*0.88     : 0.77,
        })

    def overgone(self):
        """ Deletes the overlay. """
        if self.overlay:
            ba.animate(self.overlay, 'opacity', {
                0   : self.overlay.opacity,
                1   : 0,
            })
            ba.timer(2, self.overlay.delete)

        self._set_variable('vfx', False)

append_chaos_event(TempBrokenScreen)

class TempGetGlued(ChaosEvent):
    name = 'Get Glued'
    icon = 'chaosGlued'

    def event(self):
        duration = max(0.75, min(1.35, self._get_config()['time']*0.14))

        if not len(self._get_everyone()) > 0: return False

        for spaz in self._get_everyone():
            if not spaz.node.exists(): continue

            p = ([p + (1.5 if i == 1 else 0) for i,p in enumerate(spaz.node.position)])
            v = ([v*1.1 for v in spaz.node.velocity])
            max_time    = duration
            radius      = 0.6

            Glue((
                p[0],
                p[1],
                p[2]
                ),
                 v,
                 max_time
                 ).autoretain()

            Glue((
                p[0]-radius,
                p[1],
                p[2]
                ),
                 v,
                 max_time
                 ).autoretain()

            Glue((
                p[0]-radius*0.75,
                p[1],
                p[2]+radius*0.75
                ),
                 v,
                 max_time
                 ).autoretain()

            Glue((
                p[0],
                p[1],
                p[2]+radius
                ),
                 v,
                 max_time
                 ).autoretain()

            Glue((
                p[0]+radius*0.75,
                p[1],
                p[2]+radius*0.75
                ),
                 v,
                 max_time
                 ).autoretain()

            Glue((
                p[0]+radius,
                p[1],
                p[2]
                ),
                 v,
                 max_time
                 ).autoretain()

            Glue((
                p[0]+radius*0.75,
                p[1],
                p[2]-radius*0.75
                ),
                 v,
                 max_time
                 ).autoretain()

            Glue((
                p[0],
                p[1],
                p[2]-radius
                ),
                 v,
                 max_time
                 ).autoretain()

            Glue((
                p[0]-radius*0.75,
                p[1],
                p[2]-radius*0.75,
                ),
                 v,
                 max_time
                 ).autoretain()

        return duration

append_chaos_event(TempGetGlued)

class TempMindBlown(ChaosEvent):
    name = 'Mind Blown'
    icon = 'chaosMindBlown'

    def event(self):
        """ Explodes everyone's heads. """
        victims = []

        for spaz in self._get_everyone():
            if not spaz.node.head_model == ba.getmodel('zero') and spaz.node.exists() and spaz.is_alive():
                victims.append(spaz)

        if not len(victims) > 0: return False

        for spaz in victims:
            self.do_blast(spaz)
            spaz.node.head_model = ba.getmodel('zero')
            spaz.node.style = 'bones'
            spaz.node.handlemessage('knockout', 1000)

            pos = ([p + (0.5 if i == 1 else 0) for i,p in enumerate(spaz.node.position)])
            vel = ([v * (1.25 if i == 1 else 0.9) + (1.2 if i == 1 else 0) for i,v in enumerate(spaz.node.velocity)])
            bseVFX('confetti', pos, vel)

        ba.playsound(ba.getsound('headBlown'), volume=2.4)

    def do_blast(self,
                 spaz: Spaz):
        """ Creates a fake decorative explosion. """
        pos = ([p + (0.5 if i == 1 else 0) for i,p in enumerate(spaz.node.position)])
        vel = ([v * 0.77 for v in spaz.node.velocity])

        explosion = ba.newnode(
            'explosion',
            attrs={
                'position': pos,
                'velocity': vel,
                'radius': 1.2,
                'color': spaz.node.color,
            },
        )

        ba.emitfx(
            position=pos,
            emit_type='distortion',
            spread=1.0,
        )
        ba.emitfx(position=pos,
                  velocity=vel,
                  count=6,
                  spread=0.7,
                  chunk_type='metal')

        ba.timer(2, explosion.delete)

append_chaos_event(TempMindBlown)

class TempWiimotes(ChaosEvent):
    name = 'Wiimotes'
    icon = ''

    def event(self):
        pass

class WiiCursor:
    pass

class TempEvilBouncies(ChaosEvent):
    name = 'Evil Bouncies'
    icon = 'chaosJumpies'

    def event(self):
        duration = self._get_config()['time'] * (2 if self._is_coop else random.randint(4, 6))

        did = False

        for defs in [
            self.activity.map.powerup_spawn_points,
            ]:
            for pos in defs:
                for _ in range(1 if self._is_coop else random.randint(1, 3)):
                    p = ([p + (0 if i == 1 else (random.uniform(0.4, 3) * random.choice([-1,1])) if not self._is_coop else 0) for i,p in enumerate(pos)])
                    ChaoticJumpPad(p, duration).autoretain()
                did = True

        if not did: return False

        return duration

class ChaoticJumpPad(ba.Actor):

    def __init__(
        self,
        position: tuple,
        lifespan: float,
        ):
        """ Creates a modified jumppad that sends whoever touches it flying! """
        super().__init__()
        self.bounce_sound = ba.getsound('jumpPadSilly')
        self.dying = False

        self.pos = position

        shared = SharedObjects.get()

        matpad = ba.Material()
        matpad.add_actions(
            conditions=('they_have_material', shared.pickup_material),
            actions=('modify_part_collision', 'collide', False),
        )
        matpad.add_actions(
            conditions=('they_have_material', shared.footing_material),
            actions=('modify_part_collision', 'collide', True),
        )
        matpad.add_actions(
            conditions=('they_have_material', shared.object_material),
            actions=('modify_part_collision', 'physical', False),
        )
        matpad.add_actions(
            conditions=(
                ('they_have_material', shared.object_material),
                'or',
                ('they_have_material', shared.player_material),
                ),
            actions=(('call', 'at_connect', self.used_pad),),
        )

        self.node = ba.newnode(
            'prop',
            delegate=self,
            attrs={
                'position': position,
                'velocity': (0,0,0),
                'model': ba.getmodel('jumpPadModel'),
                'light_model': ba.getmodel('jumpPadModel'),
                'body': 'landMine',
                'body_scale': 1.2,
                'shadow_size': 0,
                'color_texture': ba.gettexture('jumpPadAltColor'),
                'reflection': 'powerup',
                'reflection_scale': [1.25],
                'materials': [matpad],
            },
        )

        self.light = ba.newnode(
            'light',
             owner=self.node,
             attrs={'position':self.node.position,
                     'radius':0.0,
                     'intensity':0.0,
                     'color': (1,0,1),
                     'volume_intensity_scale': 1.0})

        self.node.connectattr('position',self.light,'position')

        self.repo_timer = ba.Timer(0.01, self.repo)
        ba.timer(lifespan, self.fancy_die)

    def repo(self):
        if not self.node.exists():
            self.repo_timer = None
            return

        self.handlemessage(ba.StandMessage(self.pos, 0))

    def used_pad(self):
        """ Sends whoever / whatever used this node flying! (Only applies to certain nodes.) """
        if self.dying: return

        node = ba.getcollision().opposingnode
        ntype = node.getnodetype()
        is_spaz = ntype == 'spaz'
        if ntype in ['spaz', 'bomb', 'prop']:
            xforce = -90
            yforce = (180 if is_spaz else 40)
            for _ in range(24):
                v = node.velocity
                node.handlemessage('impulse', node.position[0], node.position[1], node.position[2],
                                   0, 25, 0,
                                   yforce, 0.05, 0, 0,
                                   0, 20*400, 0)

                node.handlemessage('impulse', node.position[0], node.position[1], node.position[2],
                                   0, 25, 0,
                                   xforce, 0.05, 0, 0,
                                   v[0]*15*2, 0, v[2]*15*2)
        else: return

        ba.playsound(self.bounce_sound, 1.1, position=self.node.position)
        ba.emitfx(position=self.node.position,
          velocity=self.node.velocity,
          count=int(6.0 + random.random() * 12) if not ba.app.config.get("BSE: Reduced Particles", False) else 4,
          scale=0.8,
          spread=1,
          chunk_type='spark')
        ba.animate(self.node, 'model_scale', {0: 1.0, 0.2: 1.5, 0.4: 1.0,})
        ba.animate(self.light,'intensity',{0: 0.75, 1: 0.0})
        ba.animate(self.light,'radius',{0: 0.2, 1: 0.0})

    def fancy_die(self):
        """ Does an animation before dying. """
        if self.dying: return

        self.dying = True
        ba.animate(self.node, 'model_scale', {0: self.node.model_scale, 0.5: 0,})
        ba.timer(1, self.die)

    def die(self):
        """ Kill both node and light. """
        self.dying = True
        self.node.delete()
        self.light.delete()

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):
            self.die()
        elif isinstance(msg, ba.OutOfBoundsMessage):
            self.die()
        return super().handlemessage(msg)

append_chaos_event(TempEvilBouncies)

class TempMoonGravity(ChaosEvent):
    name = 'Moon Gravity'
    icon = 'chaosMoonGravity'

    blacklist = [
        runaround.RunaroundGame,
        kablooyaRunaround.RunaroundGame,
        explodinaryRunaround.RunaroundGame,
        pathwayPandemonium.PathwayPandemoniumGame
    ]

    def event(self):
        if self._get_variable('moon_theory', False): return False
        self._set_variable('moon_theory', True)

        duration = self._get_config()['time'] * 3
        time = 1/8
        self.itr = duration/time
        self.citr = 0

        self.moon_theory()
        self.moon_timer = ba.Timer(time, self.moon_theory, repeat=True)

        return duration

    def moon_theory(self):
        """ https://open.spotify.com/track/4AyjstjONX27kSFbVG0Hgq?si=74c88208ce074ed7 """
        for node in ba.getnodes():
            if node.exists() and node.getnodetype() in ['spaz', 'prop', 'bomb']:
                self.do_impulse(node)

        if self.citr > self.itr:
            self._set_variable('moon_theory', False)
            self.moon_timer = None
            return

        self.citr += 1

    def do_impulse(self,
                   node):
        """ Gives a tiny impulse upwards to give the illusion we have low gravity. """
        node.handlemessage('impulse',
                           node.position[0], node.position[1], node.position[2],
                           0, 25, 0,
                           32, 0.05, 0, 0,
                           0, 0.8, 0)

append_chaos_event(TempMoonGravity)

class Temp16to9Ratio(ChaosEvent):
    name = 'Cinematic Mode'
    icon = 'chaosCinema'

    def event(self):
        if self._get_variable('as_ratio', False): return False
        self._set_variable('as_ratio', True)

        self.overlay: ba.Node | None = None

        self.d = duration = self._get_config()['time'] * 3
        self.overlap_image()

        ba.timer(duration, self.overgone)
        return duration

    def overlap_image(self):
        """ Creates an overlay image with the provided color. """
        self.overlay = ba.newnode(
            'image',
            delegate=self,
            attrs={
                'fill_screen': True,
                'texture': ba.gettexture('ratio16to9'),
                'color': (1,1,1),
                'opacity': 0,
            },
        )

        ba.animate(self.overlay, 'opacity', {
            0               : 0,
            self.d*0.015    : 1,
        })

    def overgone(self):
        """ Deletes the overlay. """
        if self.overlay:
            ba.animate(self.overlay, 'opacity', {
                0               : self.overlay.opacity,
                self.d*0.015    : 0,
            })
            ba.timer(self.d*0.08, self.overlay.delete)

        self._set_variable('as_ratio', False)

append_chaos_event(Temp16to9Ratio)

class TempFakeCrash(ChaosEvent):
    name = 'Fake Crash'
    icon = 'chaosCrash'

    def event(self):
        # Prevent this from running if the activity has ended
        # (else we finish prematurely and leave the host with no audio and soft-locked for like 10 seconds.)
        has_ended = False
        try:
            has_ended = self.activity._has_ended
        except: pass

        if has_ended: return False

        # Make the event less likely to happen by rolling a random 0 to 1 number
        if not random.random() > 0.9: return False

        self.activity.globalsnode.paused = True
        self.omv, self.osv = ba.app.config.get('Music Volume', 1.0), ba.app.config.get('Sound Volume', 1.0)

        ba.app.config['Music Volume'] = 0
        ba.app.config['Sound Volume'] = 0
        ba.app.config.apply()

        # This only applies to host, but will also make clients believe they crashed lol
        ba.internal.lock_all_input()
        _ba.set_camera_manual(True)
        delay = random.uniform(2.5, 6)

        if random.random() > 0.69:
            ba.timer(delay * (random.uniform(0.6,0.9)), self.stutter, timetype=ba.TimeType.BASE)

        ba.timer(delay, self.uncrash, timetype=ba.TimeType.BASE)

        return

    def uncrash(self):
        """ Lifts all crash "effects". """
        self.activity.globalsnode.paused = False
        ba.internal.unlock_all_input()
        _ba.set_camera_manual(False)
        ba.app.config['Music Volume'] = self.omv
        ba.app.config['Sound Volume'] = self.osv
        ba.app.config.apply()

    def stutter(self):
        """ Did I? """
        def p(): self.activity.globalsnode.paused = True

        self.activity.globalsnode.paused = False
        ba.timer(0.01, p, timetype=ba.TimeType.BASE)

append_chaos_event(TempFakeCrash)

class TempMinecraftUpdate(ChaosEvent):
    name = 'AHOY!'
    icon = ''

    def event(self):
        """ https://www.reddit.com/r/thomastheplankengine/comments/t20gx4/mojang_added_pirate_ships_as_randomlygenerated/ """
        if not self.activity.map.name == 'Fuse Cruise' or not random.random() > 0.9: return False
        # AHOY
        ba.playsound(ba.getsound('AHOY'), volume = 0.9)

        # AHOY
        self.AHOY = ba.newnode(
            'image',
            delegate=self,
            attrs={
                'fill_screen': True,
                'texture': ba.gettexture('AHOY'),
                'color': (1,1,1),
                'opacity': 1,
            },
        )

        ba.animate(self.AHOY, 'opacity', {
            0       : 1,
            0.9     : 1,
            2.25    : 0,
        })

        ba.timer(3, self.AHOY.delete)

        return {
            'announce': False
        }

# This event is so rare it will become a myth
append_chaos_event(TempMinecraftUpdate)

class TempCSSource(ChaosEvent):
    name = 'CS Sourcent'
    icon = 'chaosSource'

    def event(self):
        """ Replaces *most* nodes with a missing texture. """
        if self._get_variable('texture_swap', False): return False
        self._set_variable('texture_swap', True)
        self.resdict = {

        }

        self.d = duration = self._get_config()['time'] * 2.75

        self.unskin_routine(-1)
        self._timer = ba.Timer(1/30, self.unskin_routine, repeat=True, timetype=ba.TimeType.BASE)

        ba.timer(duration, self.unvar)
        return duration

    def unskin_routine(self, itr = 0):
        """ Gets and wipes everyone's textures. """
        for node in ba.getnodes():
            try:
                if node.color_texture != ba.gettexture('missingTexture'):
                    self.resdict[node] = node.color_texture
                    node.color_texture = ba.gettexture('missingTexture')

            except (AttributeError, ba.NodeNotFoundError): continue

    def restore(self, node: ba.Node): node.color_texture = self.resdict[node]

    def unvar(self):
        """ Resets everyone. """
        self._timer = None

        self._set_variable('texture_swap', False)
        for node, v in self.resdict.items():
            try:
                node.color_texture = v
            except ba.NodeNotFoundError: continue

        self.resdict = None

append_chaos_event(TempCSSource)

class TempDiscordBox(ChaosEvent):
    name = 'Discord Box'
    icon = 'chaosDiscordBox'

    def event(self):
        """ Spawns a box with the Discord logo on it.
            It does something silly on blast, and leaves a decal behind. """
        pos = ([p + (0.5 if i == 1 else 0) for i,p in enumerate(self.activity.map.get_flag_position())])
        TheDiscordBox(pos).autoretain()

class TheDiscordBox(ba.Actor):
    """ A discord box that blows up epicly after a given amount of time. """
    def __init__(self,
                 position: tuple):
        super().__init__()

        shared = SharedObjects.get()

        texspeed = 33
        texpattern = (
            [ba.gettexture('discordCrate00')] * int(1.2 * texspeed) +
            [ba.gettexture('discordCrate01')] * int(0.8 * texspeed) +
            [ba.gettexture('discordCrate02'), ba.gettexture('discordCrate01')] * int(0.5 * texspeed)
        )

        self._lifespan = lifespan = 2.95
        self._spawn_pos = (position[0], position[1] + 0.5, position[2])
        mats = [shared.object_material]

        # Nod
        self.node = ba.newnode(
            'prop',
            delegate=self,
            attrs={
                'model': ba.getmodel('tnt'),
                'color_texture': texpattern[0],
                'body': 'box',
                'reflection': 'powerup',
                'model_scale': 1,
                'body_scale': 1,
                'density': 6.0,
                'reflection_scale': [0.1],
                'shadow_size': 0.75,
                'position': self._spawn_pos,
                'materials': mats,
            },
        )
        # Tex. Sequence
        self.texture_sequence = ba.newnode(
            'texture_sequence',
            owner=self.node,
            attrs={
                'rate': texspeed,
                'input_textures': texpattern
            }
        )
        self.texture_sequence.connectattr(
            'output_texture', self.node, 'color_texture'
        )
        ba.timer(3, self.texture_sequence.delete)

        # Funny sound
        self.epic_ringtone = ba.newnode(
            'sound',
            attrs={
                'sound': ba.getsound('discordRingBox'),
                'positional': True,
                'loop': False,
                'volume': 3,
            },
        )
        self.node.connectattr('position', self.epic_ringtone, 'position')

        # Light!
        acls = [
            (0.15, 0.15, 0.3),
            (0.3, 0.15, 0.3),
            (0.3, 0.15, 0.15),
            ]
        self.ambient_light = ba.newnode(
            'light',
            attrs={
                'position': position,
                'radius':0.4,
                'intensity':0.5,
                'color': (0.1, 0.1, 0.1),
            },
        )
        self.node.connectattr('model_scale', self.ambient_light, 'radius')
        self.node.connectattr('model_scale', self.ambient_light, 'intensity')
        self.node.connectattr('position', self.ambient_light, 'position')
        ba.animate_array(self.ambient_light, 'color', 3, {
            0               : acls[0],
            lifespan*0.7    : acls[1],
            lifespan*0.95   : acls[2],
            lifespan        : acls[2],
        })

        # Light 2!
        pcls = [
            (0.3, 0.3, 0.75),
            (0.75, 0.3, 0.75),
            (0.75, 0.3, 0.3),
            ]
        self.power_light = ba.newnode(
            'light',
            attrs={
                'position': position,
                'radius':0.15,
                'intensity':0.3,
                'color': (0,0,0),
            },
        )
        self.node.connectattr('position', self.power_light, 'position')
        ba.animate_array(self.power_light, 'color', 3, {
            0               : pcls[0],
            lifespan*0.7    : pcls[1],
            lifespan*0.95   : pcls[2],
            lifespan        : pcls[2],
        })

        # Death anim
        ba.animate(self.node, 'model_scale', {
            0               : 0,
            0.1             : self.node.model_scale,
            lifespan*0.88   : self.node.model_scale*1.1,
            lifespan*0.95   : self.node.model_scale*1.5,
            lifespan*0.975  : self.node.model_scale*0.66,
            lifespan        : self.node.model_scale*1.75,
        })

        self.fling_softly()
        ba.timer(lifespan*0.88, self.fling_softly)
        ba.timer(lifespan, ba.Call(self.handlemessage, ba.DieMessage()))

        self._dying = False

    def fling_softly(self):
        node = self.node
        def sec():
            node.handlemessage(
                'impulse',
                node.position[0], node.position[1]*1.5, node.position[2],
                2, 4, 2,
                128, 1.5, 0, 0,
                0.5, -1, -1
            )

        if node.exists():
            for _ in range(2):
                node.handlemessage(
                    'impulse',
                    node.position[0], node.position[1], node.position[2],
                    0, 25, 0,
                    128, 2.5, 0, 0,
                    0, 0.8, 0
                )
            ba.timer(0.075, sec)

    def exists(self) -> bool: return bool(self.node)

    def die(self):
        """ Dies :) """
        if self.node and not self._dying:
            self.do_blast()
            self._dying = True

            for node in [
                self.node,
                self.texture_sequence,
                self.ambient_light,
                self.power_light,
                self.epic_ringtone,
            ]:
                try:
                    ba.timer(0.1, node.delete)
                except: continue

    def do_blast(self):
        """ Does a funny """
        if not self.node.exists(): return
        node = self.node

        effects: list[callable] = [
            self.spawn_gifts,
        ]

        exs = (
            'explosion01',
            'explosion02',
            'explosion03',
            'explosion04',
            'explosion05',
        )

        ex = ba.newnode(
            'explosion',
            attrs={
                'position': node.position,
                'velocity': [v*0.77 for v in node.velocity],
                'radius': 4.5,
                'color': (0.3, 0.3, 1.2)
            },
        )
        ba.emitfx(
            position=node.position,
            velocity=node.velocity,
            count=24,
            scale=2.4,
            spread=2.6,
            chunk_type='spark',
        )
        bseVFX('confetti', node.position, node.velocity)

        random.choice(effects)()

        ba.playsound(ba.getsound(random.choice(exs)), position = node.position, volume = 3)

    def spawn_gifts(self):
        """ Summons powerup with a 10% chance for all of them to be curses if not in coop. """
        node = self.node
        for _ in range(random.randint(10,16)):
            coop = type(ba.getsession()) is ba.CoopSession
            pt = (
                PowerupBoxFactory.get().get_random_powerup_type(excludetypes=['curse' if coop else '']) if random.random() > 0.1 or coop else
                'curse'
            )
            powerup = PowerupBox(
                node.position,
                node.velocity,
                pt,
                True,
            ).autoretain()

            # Replace the powerup's texture with a funny one sent by our lovely users on Discord!
            texpool = [f'discordDecal{"{:02d}".format(v)}' for v in range(17)]
            powerup.node.color_texture = ba.gettexture(random.choice(texpool))
            powerup.node.reflection = 'sharper'
            powerup.node.reflection_scale = [-0.5]

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):
            self.die()
        elif isinstance(msg, ba.OutOfBoundsMessage):
            self.handlemessage(ba.DieMessage())
        elif isinstance(msg, ba.HitMessage):
            if self.node:
                self.node.handlemessage(
                    'impulse',
                    msg.pos[0],
                    msg.pos[1],
                    msg.pos[2],
                    msg.velocity[0],
                    msg.velocity[1],
                    msg.velocity[2],
                    0.15 * msg.magnitude,
                    0.15 * msg.velocity_magnitude,
                    msg.radius,
                    0,
                    msg.force_direction[0],
                    msg.force_direction[1],
                    msg.force_direction[2],
                )
        else:
            super().handlemessage(msg)

append_chaos_event(TempDiscordBox)

class TempSpazRain(ChaosEvent):
    name = 'Spaz Rain'
    icon = 'chaosSpazRain'

    def event(self):
        self.worldbounds = self.activity.map.get_def_bound_box('map_bounds')
        self.appearances = get_appearances() if random.random() > 0.75 else ['Spaz']

        self.duration = duration = self._get_config()['time'] * 1.8

        rate = 1 / (4 if self._is_coop else 12)

        self.activity._spazito_rain_clock = ba.Timer(rate, self.do_spaz, repeat=True)
        self.activity._spazito_rain_timer = ba.Timer(duration, self.stop)

        return duration

    def do_spaz(self):
        """ Summons a spaz from within the skies! """
        pos = (
            random.uniform(self.worldbounds[0], self.worldbounds[3],)*0.9,
            random.uniform(self.worldbounds[4], self.worldbounds[4],) - 2,
            random.uniform(self.worldbounds[2], self.worldbounds[5],)*0.9,
               )

        vel = (
            (-5.0 + random.random() * 15.0) * -( ( pos[0] - ( self.worldbounds[0] + self.worldbounds[3] ) / 2 ) / 4 ),
            random.uniform(-3.066, -4.12),
            (-5.0 + random.random() * 15.0) * -( ( pos[2] - ( self.worldbounds[2] + self.worldbounds[5] ) / 2 ) / 4 ),
        )

        # Generate colors
        color1, color2 = tuple([random.randint(0,255)/255 for x in range(3)]), tuple([random.randint(0,255)/255 for x in range(3)])
        # Create our spaz creature
        spaz = Spaz(
            color1,
            color2,
            random.choice(self.appearances),
            None,
            False,
            False,
            True,
            True,
            ).autoretain()
        # Teleport them where we want him to be
        spaz.handlemessage(ba.StandMessage(pos))
        # Remove their vocal chords (sometimes)
        if random.random() > 0.33:
            spaz.node.attack_sounds         = []
            spaz.node.jump_sounds           = []
            spaz.node.impact_sounds         = []
            spaz.node.pickup_sounds         = []
            spaz.node.death_sounds          = []
            spaz.node.fall_sounds           = []
        spaz.node.handlemessage('impulse',
                                vel[0], vel[1], vel[2],
                                1, 1, 1,
                                45, 45, 0, 0,
                                1, 1, 1)
        # We are not interested in this spaz! (We don't want the camera to focus on this creature)
        spaz.node.is_area_of_interest = False
        # They're like balloons!
        spaz.impact_scale = random.uniform(0.25, 3)

        # Make them get stunned forever and die after a set period of time
        spaz.stun_clock = ba.Timer(1, ba.Call(spaz.node.handlemessage, 'knockout', 900), repeat=True)
        ba.timer((self.duration*0.8) * random.uniform(0.95, 1.1), ba.Call(spaz.handlemessage, ba.DieMessage()))

    def stop(self):
        self.activity._spazito_rain_clock = None
        self.activity._spazito_rain_timer = None

append_chaos_event(TempSpazRain)
