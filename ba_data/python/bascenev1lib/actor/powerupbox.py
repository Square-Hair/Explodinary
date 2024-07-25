# Released under the MIT License. See LICENSE for details.
#
"""Defines Actor(s)."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

import bascenev1 as bs
from bascenev1lib.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any, Sequence

DEFAULT_POWERUP_INTERVAL = 8.0


class _TouchedMessage:
    pass

class PoisonedMessage:
    pass

class SparkyMessage:
    pass

class JumpPadMessage:
    """Let the Jump-Pad do it's magic."""

class PowerupBoxFactory:
    """A collection of media and other resources used by bs.Powerups.

    Category: **Gameplay Classes**

    A single instance of this is shared between all powerups
    and can be retrieved via bs.Powerup.get_factory().
    """

    _STORENAME = bs.storagename()

    def __init__(self) -> None:
        """Instantiate a PowerupBoxFactory.

        You shouldn't need to do this; call Powerup.get_factory()
        to get a shared instance.
        """
        from bascenev1 import get_default_powerup_distribution

        shared = SharedObjects.get()
        self._lastpoweruptype: str | None = None
        self.model = bs.getmesh('powerup')
        self.model_simple = bs.getmesh('powerupSimple')
        # Note from Temp: Don't forget to add your textures as well @ def poweruptex()!
        self.tex_bomb =                 bs.gettexture('powerupBomb')
        self.tex_punch =                bs.gettexture('powerupPunch')
        self.tex_dash =                 bs.gettexture('bse_powerupDash')
        self.tex_fly_punch =            bs.gettexture('bse_chaosJumpymania')
        self.tex_ice_bombs =            bs.gettexture('powerupIceBombs')
        self.tex_sticky_bombs =         bs.gettexture('powerupStickyBombs')
        self.tex_tacky_bombs =          bs.gettexture('bse_powerupTackyBombs')
        self.tex_vital_bombs =          bs.gettexture('bse_powerupVitalBombs')
        self.tex_clouder_bombs =        bs.gettexture('bse_powerupClouder')
        self.tex_steampunk_bombs =      bs.gettexture('bse_powerupSteampunk')
        self.tex_cluster_bombs =        bs.gettexture('bse_powerupClusterBombs')
        self.tex_toxic_bombs =          bs.gettexture('bse_powerupToxicBombs')
        self.tex_flutter_mines =        bs.gettexture('bse_powerupFlutterMines')
        self.tex_glue_mines =           bs.gettexture('bse_powerupGlueMines')
        self.tex_shield =               bs.gettexture('powerupShield')
        self.tex_impact_bombs =         bs.gettexture('powerupImpactBombs')
        self.tex_health =               bs.gettexture('powerupHealth')
        self.tex_vitamin =              bs.gettexture('bse_powerupVitamin')
        self.tex_land_mines =           bs.gettexture('powerupLandMines')
        self.tex_lite_mines =           bs.gettexture('bse_powerupSkyMines')
        self.tex_present =              bs.gettexture('bse_powerupPresent')
        self.tex_curse =                bs.gettexture('powerupCurse')
        self.health_powerup_sound =     bs.getsound('healthPowerup')
        self.vitamin_powerup_sound =    bs.getsound('bse_vitaminPowerup')
        self.powerup_sound =            bs.getsound('powerup01')
        self.powerdown_sound =          bs.getsound('powerdown01')
        self.drop_sound =               bs.getsound('boxDrop')
        self.spark_sound =              bs.getsound('bse_sparkSound')

        # Material for powerups.
        self.powerup_material = bs.Material()

        # Material for anyone wanting to accept powerups.
        self.powerup_accept_material = bs.Material()

        # Pass a powerup-touched message to applicable stuff.
        self.powerup_material.add_actions(
            conditions=('they_have_material', self.powerup_accept_material),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('message', 'our_node', 'at_connect', _TouchedMessage()),
            ),
        )

        # We don't wanna be picked up.
        self.powerup_material.add_actions(
            conditions=('they_have_material', shared.pickup_material),
            actions=('modify_part_collision', 'collide', False),
        )

        self.powerup_material.add_actions(
            conditions=('they_have_material', shared.footing_material),
            actions=('impact_sound', self.drop_sound, 0.5, 0.1),
        )

        self._powerupdist: list[str] = []
        for powerup, freq in get_default_powerup_distribution():
            for _i in range(int(freq)):
                self._powerupdist.append(powerup)

        # Make expire times manipulable
        self.expire_flash_timer: bs.Timer | None = None
        self.expire_timer: bs.Timer | None = None

    def get_random_powerup_type(
        self,
        forcetype: str | None = None,
        excludetypes: list[str] | None = None,
    ) -> str:
        """Returns a random powerup type (string).

        See bs.Powerup.poweruptype for available type values.

        There are certain non-random aspects to this; a 'curse' powerup,
        for instance, is always followed by a 'health' powerup (to keep things
        interesting). Passing 'forcetype' forces a given returned type while
        still properly interacting with the non-random aspects of the system
        (ie: forcing a 'curse' powerup will result
        in the next powerup being health).
        """
        if excludetypes is None:
            excludetypes = []
        if forcetype:
            ptype = forcetype
        else:
            # If the last one was a curse, make this one a health to
            # provide some hope.
            if self._lastpoweruptype == 'curse':
                ptype = 'health'

            else:
                while True:
                    if len(self._powerupdist) < 1: return
                    ptype = self._powerupdist[
                        random.randint(0, len(self._powerupdist) - 1)
                    ]
                    if ptype not in excludetypes:
                        break
        self._lastpoweruptype = ptype
        return ptype

    @classmethod
    def get(cls) -> PowerupBoxFactory:
        """Return a shared bs.PowerupBoxFactory object, creating if needed."""
        activity = bs.getactivity()
        if activity is None:
            raise bs.ContextError('No current activity.')
        factory = activity.customdata.get(cls._STORENAME)
        if factory is None:
            factory = activity.customdata[cls._STORENAME] = PowerupBoxFactory()
        assert isinstance(factory, PowerupBoxFactory)
        return factory

def poweruptex() -> dict:
    import bauiv1 as bui
    return({
        'triple_bombs':     bui.gettexture('powerupBomb'),
        'punch':            bui.gettexture('powerupPunch'),
        'dash':             bui.gettexture('bse_powerupDash'),
        'fly_punch':        bui.gettexture('bse_powerupFlyingPunch'),
        'ice_bombs':        bui.gettexture('powerupIceBombs'),
        'impact_bombs':     bui.gettexture('powerupImpactBombs'),
        'land_mines':       bui.gettexture('powerupLandMines'),
        'lite_mines':       bui.gettexture('bse_powerupSkyMines'),
        'sticky_bombs':     bui.gettexture('powerupStickyBombs'),
        'tacky_bombs':      bui.gettexture('bse_powerupTackyBombs'),
        'vital_bombs':      bui.gettexture('bse_powerupVitalBombs'),
        'clouder_bombs':    bui.gettexture('bse_powerupClouder'),
        'flutter_mines':    bui.gettexture('bse_powerupFlutterMines'),
        'glue_mines':       bui.gettexture('bse_powerupGlueMines'),
        'steampunk_bombs':  bui.gettexture('bse_powerupSteampunk'),
        'cluster_bombs':    bui.gettexture('bse_powerupClusterBombs'),
        'toxic_bombs':      bui.gettexture('bse_powerupToxicBombs'),
        'present':          bui.gettexture('bse_powerupPresent'),
        'shield':           bui.gettexture('powerupShield'),
        'health':           bui.gettexture('powerupHealth'),
        'curse':            bui.gettexture('powerupCurse'),
        })

class PowerupBox(bs.Actor):
    """A box that grants a powerup.

    category: Gameplay Classes

    This will deliver a bs.PowerupMessage to anything that touches it
    which has the bs.PowerupBoxFactory.powerup_accept_material applied.
    """

    poweruptype: str
    """The string powerup type.  This can be 'triple_bombs', 'punch',
       'ice_bombs', 'impact_bombs', 'land_mines', 'lite_mines', 'present' 'sticky_bombs', 'tacky_bombs', 'shield',
       'clouder_bombs', 'steampunk_bombs', 'toxic_bombs', 'vital_bombs', 'flutter_mines', 'health', or 'curse'."""

    node: bs.Node
    """The 'prop' bs.Node representing this box."""

    def __init__(
        self,
        position: Sequence[float] = (0.0, 1.0, 0.0),
        velocity: Sequence[float] = (0.0, 1.0, 0.0),
        poweruptype: str = 'triple_bombs',
        expire: bool = True,
        is_poisoned = False,
        is_sparky = False,
        frozen = False
    ):
        """Create a powerup-box of the requested type at the given position.

        see bs.Powerup.poweruptype for valid type strings.
        """

        super().__init__()
        shared = SharedObjects.get()
        factory = PowerupBoxFactory.get()
        self.poweruptype = poweruptype
        self._powersgiven = False
        self.is_poisoned = is_poisoned
        self.is_sparky = is_sparky
        self.frozen = frozen

        try: tex = poweruptex().get(poweruptype)
        except ValueError: raise ValueError('invalid poweruptype: ' + str(poweruptype))

        if len(position) != 3:
            raise ValueError('expected 3 floats for position')

        self.node = bs.newnode(
            'prop',
            delegate=self,
            attrs={
                'body': 'box',
                'position': position,
                'model': factory.model,
                'light_model': factory.model_simple,
                'shadow_size': 0.5,
                'color_texture': tex,
                'reflection': 'powerup',
                'reflection_scale': [1.0],
                'materials': (factory.powerup_material, shared.object_material),
            },
        )  # yapf: disable

        # Animate in.
        curve = bs.animate(self.node, 'model_scale', {0: 0, 0.14: 1.6, 0.2: 1})
        bs.timer(0.2, curve.delete)

        if expire:
            self.expire_flash_timer = bs.Timer(
                DEFAULT_POWERUP_INTERVAL - 2.35,
                bs.WeakCall(self._start_flashing),
            )
            self.expire_timer = bs.Timer(
                DEFAULT_POWERUP_INTERVAL - 0.75,
                bs.WeakCall(self.handlemessage, bs.DieMessage()),
            )

    def _start_flashing(self) -> None:
        if self.node:
            self.node.flashing = True

    def _poison_particles(self) -> None:
            if self.node.exists():
                if self.is_poisoned:
                    bs.emitfx(
                    position=self.node.position,
                    velocity=(0.0, 1.0, 0.0),
                    count=10,
                    spread=0.25,
                    scale=0.5,
                    chunk_type='slime',
                    );
            else: None

    def _toxic_light(self) -> None:
        if self.node.exists() and self.is_poisoned == True:
                if self.is_poisoned:
                    self.toxic_light = bs.newnode('light',
                                        owner=self.node,
                                        attrs={'position':self.node.position,
                                                'radius':0.1,
                                                'intensity':0.5,
                                                'color': (0.2, 1, 0.2),
                                                'volume_intensity_scale': 1.0})
                    self.node.connectattr('position',self.toxic_light,'position')
        else: None

    def _frozen_light(self) -> None:
        if self.node.exists() and self.frozen == True:
            if self.frozen:
                self.frozen_light = bs.newnode('light',
                                    owner=self.node,
                                    attrs={'position':self.node.position,
                                            'radius':0.1,
                                            'intensity':1,
                                            'color': (0, 0, 1),
                                            'volume_intensity_scale': 1.0})
                self.node.connectattr('position',self.frozen_light,'position')
        else: None

    def _sparky_particles(self) -> None:
            if self.node.exists():
                if self.is_sparky:
                    bs.emitfx(
                    position=self.node.position,
                    velocity=(0.0, 1.0, 0.0),
                    count=10,
                    spread=0.25,
                    scale=0.5,
                    chunk_type='spark',
                    );
            else: None

    def _sparky_light(self) -> None:
        if self.node.exists() and self.is_sparky == True:
                if self.is_sparky:
                    self.sparky_light = bs.newnode('light',
                                        owner=self.node,
                                        attrs={'position':self.node.position,
                                                'radius':0.1,
                                                'intensity':0.5,
                                                'color': (0.4, 0.8, 1),
                                                'volume_intensity_scale': 1.0})
                    self.node.connectattr('position',self.sparky_light,'position')
        else: None

    def handlemessage(self, msg: Any) -> Any:
        assert not self.expired

        if isinstance(msg, bs.PowerupAcceptMessage):
            factory = PowerupBoxFactory.get()
            assert self.node
            if self.poweruptype == 'health':
                bs.playsound(
                    factory.health_powerup_sound, 1.5, position=self.node.position
                )
            bs.playsound(factory.powerup_sound, 3, position=self.node.position)
            self._powersgiven = True
            self.handlemessage(bs.DieMessage())
            if self.poweruptype == 'vitamin':
                bs.playsound(
                    factory.vitamin_powerup_sound, 0.6, position=self.node.position
                )
            bs.playsound(factory.powerup_sound, 3, position=self.node.position)
            self._powersgiven = True
            self.handlemessage(bs.DieMessage())

        elif isinstance(msg, _TouchedMessage):
            factory = PowerupBoxFactory.get()
            if not self._powersgiven:
                node = bs.getcollision().opposingnode
                node.handlemessage(
                    bs.PowerupMessage(self.poweruptype, sourcenode=self.node)
                )
                if self.is_poisoned: node.handlemessage(bs.ToxicMessage())
                if self.is_sparky:
                    if node.exists():
                        node.handlemessage('knockout', 1000.0)
                        bs.playsound(factory.spark_sound, 1.5, position=self.node.position)
                        bs.emitfx(
                            position=node.position,
                            velocity=(0.0, 1.0, 0.0),
                            count=10,
                            spread=0.25,
                            scale=0.5,
                            chunk_type='spark',
                        );

        elif isinstance(msg, bs.DieMessage):
            if self.node:
                if msg.immediate:
                    self.node.delete()
                else:
                    bs.animate(self.node, 'model_scale', {0: 1, 0.1: 0})
                    bs.timer(0.1, self.node.delete)

        elif isinstance(msg, bs.OutOfBoundsMessage):
            self.handlemessage(bs.DieMessage())

        elif isinstance(msg, bs.HitMessage):
            # Toxify ourselves if hit by a toxic bomb's blast.
            if msg.hit_subtype == 'toxic':
                if self.poweruptype in ['health','shield','vitamin']: return
                if self.is_poisoned == True: return
                self.is_poisoned = True
                self._toxic_timer = bs.timer(0.2,bs.Call(self._poison_particles),repeat=True)
                self._toxic_light_timer = bs.timer(0.2,bs.Call(self._toxic_light))
            # Handle a good fling when hit by a flutter bomb / mine.
            elif msg.hit_subtype == 'vital':
                self.node.color_texture = bs.gettexture("powerupVitamin")
                self.node.model = bs.getmesh("powerupLittle")
                self.poweruptype = 'vitamin'
            elif msg.hit_subtype == 'lite':
                if self.poweruptype in ['health','shield','vitamin']: return
                if self.is_sparky == True: return
                self.is_sparky = True
                self._sparky_timer = bs.timer(0.2,bs.Call(self._sparky_particles),repeat=True)
                self._sparky_light_timer = bs.timer(0.2,bs.Call(self._sparky_light))
            elif msg.hit_subtype == 'ice':
                self.frozen = True
                shared = SharedObjects.get()
                factory = PowerupBoxFactory.get()
                self.node.reflection = 'powerup'
                self.node.reflection_scale = [8]
                icemat = bs.Material()
                icemat.add_actions(actions=('modify_part_collision', 'friction', 0.01))
                materials = (factory.powerup_material, shared.object_material)
                self.node.materials = materials + (icemat,)
                bs.emitfx(
                    position=self.node.position,
                    velocity=self.node.velocity,
                    count=4 if not bs.app.config.get("BSE: Reduced Particles", False) else 2,
                    spread=0.1,
                    scale=0.2,
                    chunk_type='ice',
                )
                xforce = 5
                yforce = 2
                for x in range(5):
                    v = self.node.velocity
                    self.node.handlemessage('impulse', self.node.position[0], self.node.position[1], self.node.position[2],
                                    0, 25, 0,
                                    yforce, 0.05, 0, 0,
                                    0, 20*600, 0)

                    self.node.handlemessage('impulse', self.node.position[0], self.node.position[1], self.node.position[2],
                                            0, 25, 0,
                                            xforce, 0.05, 0, 0,
                                            v[0]*15*2, 0, v[2]*15*2)

            elif msg.hit_subtype in ['cloudy','flutter']:
                multiplier: float = 4
                self.node.handlemessage(
                    'impulse',
                    msg.pos[0],
                    msg.pos[1] + 0.1,
                    msg.pos[2],
                    0,
                    0,
                    0,
                    msg.magnitude * 1.5,
                    msg.velocity_magnitude,
                    msg.radius * multiplier,
                    0,
                    msg.force_direction[0] * multiplier,
                    msg.force_direction[1] * multiplier,
                    msg.force_direction[2] * multiplier,
                )

            # Don't die on punches (that's annoying).
            elif msg.hit_type != 'punch':
                self.handlemessage(bs.DieMessage())

        else:
            return super().handlemessage(msg)
        return None
