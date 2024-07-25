# Released under the MIT License. See LICENSE for details.
#
"""Various classes for bombs, mines, tnt, etc."""

# FIXME
# pylint: disable=too-many-lines

from __future__ import annotations

import random
from typing import TYPE_CHECKING, TypeVar

import ba
import math
from bastd.gameutils import SharedObjects
from explodinary.custom.particle import bseVFX
from bastd.actor import spaz

if TYPE_CHECKING:
    from typing import Any, Sequence, Callable

# pylint: disable=invalid-name
PlayerType = TypeVar('PlayerType', bound='ba.Player')
# pylint: enable=invalid-name


class BombFactory:
    """Wraps up media and other resources used by ba.Bombs.

    Category: **Gameplay Classes**

    A single instance of this is shared between all bombs
    and can be retrieved via bastd.actor.bomb.get_factory().
    """

    bomb_model: ba.Model
    """The ba.Model of a standard bomb."""

    sticky_bomb_model: ba.Model
    """The ba.Model of a sticky-bomb."""
    
    ice_bomb_model: ba.Model
    """The ba.Model of a ice-bomb."""

    impact_bomb_model: ba.Model
    """The ba.Model of an impact-bomb."""

    land_mine_model: ba.Model
    """The ba.Model of a land-mine."""
    
    lite_mine_model: ba.Model
    """The ba.Model of a lite-mine."""
    
    glue_mine_model: ba.Model
    """The ba.Model of a lite-mine."""
    
    tacky_bomb_model: ba.Model
    """The ba.Model for tacky bombs."""
    
    vital_bomb_model: ba.Model
    """The ba.Model for vital bombs."""
    
    clouder_bomb_model: ba.Model
    """The ba.Model for clouder bombs."""
    
    cluster_bomb_model: ba.Model
    """The ba.Model of a cluster bomb."""
    
    steampunk_bomb_model: ba.Model
    """The ba.Model for steam bombs."""
    
    toxic_bomb_model: ba.Model
    """The ba.Model for toxic bombs."""
    
    flutter_mine_model: ba.Model
    """The ba.Model for flutter mines."""
    
    present_bomb_model: ba.Model
    """The ba.model for presents"""
    
    jumppad_bomb_model: ba.Model
    """The ba.model for Jump-Pads"""
    
    slingshot_bomb_model: ba.Model
    """The ba.model for slingshots"""
    
    flying_glove_model: ba.Model
    """The ba.model for a flying glove"""
    
    tnt_model: ba.Model
    """The ba.Model of a tnt box."""
    
    tnt_toxic_model: ba.Model
    """The ba.Model of a toxic tnt box."""
    
    tnt_glue_model: ba.Model
    """The ba.Model of a glue tnt box."""
    
    regular_tex: ba.Texture
    """The ba.Texture for regular bombs."""

    ice_tex: ba.Texture
    """The ba.Texture for ice bombs."""

    sticky_tex: ba.Texture
    """The ba.Texture for sticky bombs."""

    impact_tex: ba.Texture
    """The ba.Texture for impact bombs."""
    
    impact_lit_tex: ba.Texture
    """The ba.Texture for impact bombs with lights lit."""

    land_mine_tex: ba.Texture
    """The ba.Texture for land-mines."""
    
    glue_mine_tex: ba.Texture
    """The ba.Texture for glue-mines."""
    
    glue_mine_lit_tex: ba.Texture
    """The ba.Texture for glue-mines with lights lit."""
    
    jumppad_tex: ba.Texture
    """The ba.Texture for Jump-Pads."""
    
    slingshot_tex: ba.Texture
    """The ba.Texture for slingshots."""
    
    flying_glove_tex: ba.Texture
    """The ba.Texture for flying gloves."""

    land_mine_lit_tex: ba.Texture
    """The ba.Texture for land-mines with the light lit."""
    
    lite_mine_tex: ba.Texture
    """The ba.Texture for lite-mines."""

    lite_mine_lit_tex: ba.Texture
    """The ba.Texture for lite-mines with the light lit."""
    
    vital_tex: ba.Texture
    """The ba.Texture for vital bombs."""

    vital_lit_tex: ba.Texture
    """The ba.Texture for vital bombs with the light lit."""
    
    tacky_lit_tex: ba.Texture
    """The ba.Texture for tacky bombs with lights lit."""
    
    clouder_tex: ba.Texture
    """The ba.Texture for clouder bombs."""
    
    cluster_tex: ba.Texture
    """The ba.Texture for cluster bombs."""
    
    steampunk_tex: ba.Texture
    """The ba.Texture for steam bombs."""
    
    toxic_tex: ba.Texture
    """The ba.Texture for toxic bombs."""
    
    flutter_mine_tex: ba.Texture
    """The ba.Texture for flutter-mines."""
    
    flutter_mine_lit_tex: ba.Texture
    """The ba.Texture for flutter-mines with the light lit."""
    
    present_bomb_tex: ba.Texture #6 seconds
    """The ba.Texture for present 15 seconds before explosion."""
    
    present_bomb_tex2: ba.Texture #4 seconds
    """The ba.Texture for present 10 seconds before explosion."""
    
    present_bomb_tex3: ba.Texture #2 seconds
    """The ba.Texture for present 5 seconds before explosion."""
    
    present_bomb_texEx: ba.Texture #Just before exploding
    """The ba.Texture for present just before explosion."""
    
    tnt_tex: ba.Texture
    """The ba.Texture for tnt boxes."""
    
    tnt_ice_tex: ba.Texture
    """The ba.Texture for ice tnt boxes."""
    
    tnt_toxic_tex: ba.Texture
    """The ba.Texture for toxic tnt boxes."""
    
    tnt_glue_tex: ba.Texture
    """The ba.Texture for glue tnt boxes."""

    hiss_sound: ba.Sound
    """The ba.Sound for the hiss sound an ice bomb makes."""
    
    alarm_sound: ba.Sound
    """The ba.Sound for the alarm clock sound an ice bomb makes."""

    debris_fall_sound: ba.Sound
    """The ba.Sound for random falling debris after an explosion."""

    wood_debris_fall_sound: ba.Sound
    """A ba.Sound for random wood debris falling after an explosion."""

    explode_sounds: Sequence[ba.Sound]
    """A tuple of ba.Sound-s for explosions."""
    
    buff_sound: ba.Sound
    """A ba.Sound of a buffed explosion."""
    
    nerf_sound: ba.Sound
    """A ba.Sound of a nerfed explosion."""
    
    freeze_sound: ba.Sound
    """A ba.Sound of an ice bomb freezing something."""

    fuse_sound: ba.Sound
    """A ba.Sound of a burning fuse."""
    
    engine_sound: ba.Sound
    """A ba.Sound of Iron Bomb's engine."""
    
    engine_near_sound: ba.Sound
    """A ba.Sound of Iron Bomb's engine close to exploding."""

    activate_sound: ba.Sound
    """A ba.Sound for an activating impact bomb."""
    
    confetti_sound: ba.Sound
    """A ba.Sound for confetti of present."""
    
    warn_sound: ba.Sound
    """A ba.Sound for an impact bomb about to explode due to time-out."""

    bomb_material: ba.Material
    """A ba.Material applied to all bombs."""
    
    present_material: ba.Material
    """A ba.Material applied to present."""
    
    no_pick_material: ba.Material
    """A ba.Material that disables picking up."""
    
    normal_sound_material: ba.Material
    """A ba.Material that generates standard bomb noises on impacts, etc."""

    sticky_material: ba.Material
    """A ba.Material that makes 'splat' sounds and makes collisions softer."""
    
    tacky_material: ba.Material
    """A ba.Material that makes 'drip' sounds and makes collisions softer."""

    land_mine_no_explode_material: ba.Material
    """A ba.Material that keeps land-mines from blowing up.
       Applied to land-mines when they are created to allow land-mines to
       touch without exploding."""

    land_mine_blast_material: ba.Material
    """A ba.Material applied to activated land-mines that causes them to
       explode on impact."""

    impact_blast_material: ba.Material
    """A ba.Material applied to activated impact-bombs that causes them to
       explode on impact."""
    
    glove_material: ba.Material
    """A ba.Material applied to gloves"""

    blast_material: ba.Material
    """A ba.Material applied to bomb blast geometry which triggers impact
       events with what it touches."""

    dink_sounds: Sequence[ba.Sound]
    """A tuple of ba.Sound-s for when bombs hit the ground."""

    sticky_impact_sound: ba.Sound
    """The ba.Sound for a squish made by a sticky bomb hitting something."""
    
    sticky_impact_player_sound: ba.Sound
    """The ba.Sound for a squish made by a sticky bomb hitting a player."""
    
    tacky_impact_sound: ba.Sound
    """The ba.Sound for a squish made by a tacky bomb, just to differentiate it from sticky bomb."""
    
    tacky_impact_player_sound: ba.Sound
    """The ba.Sound for a squish made by a tacky bomb hitting a player."""

    roll_sound: ba.Sound
    """ba.Sound for a rolling bomb."""
    
    skymine_sound: ba.Sound
    """A ba.Sound for the blast of sky mines."""
    
    glue_mine_sound: ba.Sound
    """A ba.Sound for the blast of glue mines."""
    
    present_blast: ba.Sound
    """A ba.Sound for the blast of Unwanted Present."""
    
    tacky_blast: ba.Sound
    """A ba.Sound for the blast of Tacky Bomb."""
    
    flying_glove_blast: ba.Sound
    """A ba.Sound for the blast of Flying Glove."""
    
    vital_blast: ba.Sound
    """A ba.Sound for the blast of Vital Bomb."""
    
    cluster_blast: ba.Sound
    """A ba.Sound for the blast of Vital Bomb."""
    
    vitaken_sound: ba.Sound
    """A ba.Sound for when a vital bomb is deployed"""
    
    vitready_sound: ba.Sound
    """A ba.Sound for a vital bomb about to explode."""
    
    clouder_blast: ba.Sound
    """A ba.Sound for the blast of Flutter Bomb."""

    steampunk_blast: ba.Sound
    """A ba.Sound for the blast of Iron Bomb."""
    
    cluster_blast: ba.Sound
    """A ba.Sound for the blast of Iron Bomb."""
    
    jumppad_sound: ba.Sound
    """A ba.Sound when the Jump-Pads are used."""
    
    slingshot_sound: ba.Sound
    """A ba.Sound when the slingshots are used."""
    
    _STORENAME = ba.storagename()

    @classmethod
    def get(cls) -> BombFactory:
        """Get/create a shared bastd.actor.bomb.BombFactory object."""
        activity = ba.getactivity()
        factory = activity.customdata.get(cls._STORENAME)
        if factory is None:
            factory = BombFactory()
            activity.customdata[cls._STORENAME] = factory
        assert isinstance(factory, BombFactory)
        return factory

    def random_explode_sound(self) -> ba.Sound:
        """Return a random explosion ba.Sound from the factory."""
        return self.explode_sounds[random.randrange(len(self.explode_sounds))]

    def __init__(self) -> None:
        """Instantiate a BombFactory.

        You shouldn't need to do this; call bastd.actor.bomb.get_factory()
        to get a shared instance.
        """
        shared = SharedObjects.get()

        self.bomb_model = ba.getmodel('bomb')
        self.sticky_bomb_model = ba.getmodel('bombSticky')
        self.ice_bomb_model = ba.getmodel('bombIce')
        self.impact_bomb_model = ba.getmodel('impactBomb')
        self.land_mine_model = ba.getmodel('landMine')
        self.glue_mine_model = ba.getmodel('glueMine')
        self.flutter_mine_model = ba.getmodel('flutterMine')
        self.lite_mine_model = ba.getmodel('skyMine')
        self.tacky_bomb_model = ba.getmodel('tackyBomb')
        self.vital_bomb_model = ba.getmodel('vitalBomb')
        self.present_bomb_model = ba.getmodel('presentBomb')
        self.clouder_bomb_model = ba.getmodel('clouderBomb')
        self.steampunk_bomb_model = ba.getmodel('steampunkBomb')
        self.cluster_bomb_model = ba.getmodel('clusterBomb')
        self.toxic_bomb_model = ba.getmodel('toxicBomb')
        self.tnt_model = ba.getmodel('tnt')
        self.tnt_toxic_model = ba.getmodel('tntToxic')
        self.tnt_glue_model = ba.getmodel('tntGlue')
        self.jumppad_model = ba.getmodel('jumpPadModel')
        self.slingshot_model = ba.getmodel('slingshotModel')
        self.flying_glove_model = ba.getmodel('flyingGlovesModel')

        self.regular_tex = ba.gettexture('bombColor')
        self.ice_tex = ba.gettexture('bombColorIce')
        self.sticky_tex = ba.gettexture('bombStickyColor')
        self.impact_tex = ba.gettexture('impactBombColor')
        self.impact_lit_tex = ba.gettexture('impactBombColorLit')
        self.land_mine_tex = ba.gettexture('landMine')
        self.land_mine_lit_tex = ba.gettexture('landMineLit')
        self.vital_tex = ba.gettexture('vitalBomb')
        self.vital_lit_tex = ba.gettexture('vitalBombLit')
        self.lite_mine_tex = ba.gettexture('skyMine')
        self.glue_mine_tex = ba.gettexture('glueMine')
        self.jumppad_tex = ba.gettexture('jumpPadColor')
        self.slingshot_tex = ba.gettexture('slingshotColor')
        self.flying_glove_tex = ba.gettexture('flyingGlovesColor')
        self.lite_mine_lit_tex = ba.gettexture('skyMineLit')
        self.glue_mine_lit_tex = ba.gettexture('glueMineLit')
        self.flutter_mine_tex = ba.gettexture('flutterMineColor')
        self.flutter_mine_lit_tex = ba.gettexture('flutterMineColorLit')
        self.tacky_lit_tex = ba.gettexture('tackyBombColorLit')
        self.clouder_tex = ba.gettexture('clouderBombColor')
        self.steampunk_tex = ba.gettexture('steampunkBombColor')
        self.cluster_tex = ba.gettexture('clusterBombColor')
        self.toxic_tex = ba.gettexture('toxicBombColor')
        self.present_bomb_tex = ba.gettexture('presentBombColor')
        self.present_bomb_tex2 = ba.gettexture('presentBombColor2')
        self.present_bomb_tex3 = ba.gettexture('presentBombColor3')
        self.present_bomb_texEx = ba.gettexture('presentBombColorEx')
        self.tnt_tex = ba.gettexture('tnt')
        self.tnt_ice_tex = ba.gettexture('tntIce')
        self.tnt_toxic_tex = ba.gettexture('tntToxic')
        self.tnt_glue_tex = ba.gettexture('tntGlue')

        self.hiss_sound = ba.getsound('hiss')
        self.alarm_sound = ba.getsound('alarmClock')
        self.confetti_sound = ba.getsound('confetti')
        self.debris_fall_sound = ba.getsound('debrisFall')
        self.wood_debris_fall_sound = ba.getsound('woodDebrisFall')
        self.jumppad_sound = ba.getsound('jumpPadSound')
        self.slingshot_sound = ba.getsound('slingshotSound')

        self.explode_sounds = (
            ba.getsound('explosion01'),
            ba.getsound('explosion02'),
            ba.getsound('explosion03'),
            ba.getsound('explosion04'),
            ba.getsound('explosion05'),
        )
        self.skymine_sound = ba.getsound ('skyMine_blast')
        self.buff_sound = ba.getsound('explosionBuffed')
        self.nerf_sound = ba.getsound('explosionNerfed')
        self.freeze_sound = ba.getsound('freeze')
        self.fuse_sound = ba.getsound('fuse01')
        self.engine_sound = ba.getsound('engineSound')
        self.engine_near_sound = ba.getsound('engineNear')
        self.activate_sound = ba.getsound('activateBeep')
        self.warn_sound = ba.getsound('warnBeep')
        self.present_blast = ba.getsound('presentBlast')
        self.vital_blast = ba.getsound('vitalBlast')
        self.flying_glove_blast = ba.getsound('flyingGlovesBlast')
        self.glue_mine_sound = ba.getsound('glueTNTBlast')
        self.tacky_blast = ba.getsound('tackyBlast')
        self.tacky_impact_sound = ba.getsound('tackyImpact')
        self.tacky_impact_player_sound = ba.getsound('tackyImpactPlayer')
        self.clouder_blast = ba.getsound('clouderBlast')
        self.steampunk_blast = ba.getsound('steampunkBlast')
        self.cluster_blast = ba.getsound('clusterBlast')
        self.toxic_blast = ba.getsound('toxicBlast')
        self.tnt_toxic_blast = ba.getsound('toxicTNTBlast')
        self.tnt_glue_blast = ba.getsound('glueTNTBlast')
        self.tnt_ice_blast = ba.getsound('iceTNTBlast')
        self.vitaken_sound = ba.getsound('vitalTaken')
        self.vitready_sound = ba.getsound('vitalReady')
        # Set up our material so new bombs don't collide with objects
        # that they are initially overlapping.
        self.bomb_material = ba.Material()
        self.normal_sound_material = ba.Material()
        self.sticky_material = ba.Material()
        self.tacky_material = ba.Material()
        self.bomb_material.add_actions(
            conditions=(
                (
                    ('we_are_younger_than', 100),
                    'or',
                    ('they_are_younger_than', 100),
                ),
                'and',
                ('they_have_material', shared.object_material),
            ),
            actions=('modify_node_collision', 'collide', False),
        )

        # We want pickup materials to always hit us even if we're currently
        # not colliding with their node. (generally due to the above rule)
        self.bomb_material.add_actions(
            conditions=('they_have_material', shared.pickup_material),
            actions=('modify_part_collision', 'use_node_collide', False),
        )

        self.bomb_material.add_actions(
            actions=('modify_part_collision', 'friction', 0.3)
        )

        self.land_mine_no_explode_material = ba.Material()
        self.land_mine_blast_material = ba.Material()
        self.land_mine_blast_material.add_actions(
            conditions=(
                ('we_are_older_than', 200),
                'and',
                ('they_are_older_than', 200),
                'and',
                ('eval_colliding',),
                'and',
                (
                    (
                        'they_dont_have_material',
                        self.land_mine_no_explode_material,
                    ),
                    'and',
                    (
                        ('they_have_material', shared.object_material),
                        'or',
                        ('they_have_material', shared.player_material),
                    ),
                ),
            ),
            actions=('message', 'our_node', 'at_connect', ImpactMessage()),
        )

        self.impact_blast_material = ba.Material()
        self.impact_blast_material.add_actions(
            conditions=(
                ('we_are_older_than', 200),
                'and',
                ('they_are_older_than', 200),
                'and',
                ('eval_colliding',),
                'and',
                (
                    ('they_have_material', shared.footing_material),
                    'or',
                    ('they_have_material', shared.object_material),
                ),
            ),
            actions=('message', 'our_node', 'at_connect', ImpactMessage()),
        )
        
        self.glove_material = ba.Material()
        self.glove_material.add_actions(
            conditions=(
                ('we_are_older_than', 10),
                'and',
                ('they_are_older_than', 200),
                'and',
                ('eval_colliding',),
                'and',
                (
                    ('they_have_material', shared.footing_material),
                    'or',
                    ('they_have_material', shared.object_material),
                ),
            ),
            actions=('message', 'our_node', 'at_connect', ImpactMessage()),
        )

        self.blast_material = ba.Material()
        self.blast_material.add_actions(
            conditions=('they_have_material', shared.object_material),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('message', 'our_node', 'at_connect', ExplodeHitMessage()),
            ),
        )
        
        self.present_material = ba.Material()
        self.present_material.add_actions(
            conditions=(
                ('we_are_older_than', 200),
                'and',
                ('they_are_older_than', 200),
                'and',
                ('eval_colliding',),
                'and',
                (
                    ('they_have_material', shared.footing_material),
                    'or',
                    ('they_have_material', shared.object_material),
                ),
            ),
            actions=('message', 'our_node', 'at_connect', PresentMessage()),
        )
        
        self.no_pick_material = ba.Material()
        self.no_pick_material.add_actions(
            conditions=('they_have_material', shared.pickup_material),
            actions=('modify_part_collision', 'collide', False),
        )
        
        self.jumppad_material = ba.Material()
        self.jumppad_material.add_actions(
            conditions=('they_have_material', shared.pickup_material),
            actions=('modify_part_collision', 'collide', False),
        )
        self.jumppad_material.add_actions(
            conditions=('they_have_material', shared.footing_material),
            actions=('modify_part_collision', 'collide', True),
        )
        self.jumppad_material.add_actions(
            conditions=('they_have_material', shared.object_material),
            actions=('modify_part_collision', 'physical', False),
        )
        self.jumppad_material.add_actions(
            conditions=(
                ('they_have_material', shared.object_material),
                'or',
                ('they_have_material', shared.player_material),
                ),
            actions=(('message', 'our_node', 'at_connect', JumpPadMessage())),
        )
        
        self.slingshot_material = ba.Material()
        self.slingshot_material.add_actions(
            conditions=(
                ('we_are_older_than', 200),
                'and',
                ('they_are_older_than', 200),
                'and',
                ('eval_colliding',),
                'and',
                (
                    (
                        'they_dont_have_material',
                        self.land_mine_no_explode_material,
                    ),
                    'and',
                    (
                        ('they_have_material', shared.object_material),
                        'or',
                        ('they_have_material', shared.player_material),
                    ),
                ),
            ),
            actions=('message', 'our_node', 'at_connect', slingshotMessage()),
        )
        
        self.slingshot_material.add_actions(
            conditions=(
                ('they_have_material', shared.object_material),
                'or',
                ('they_dont_have_material', shared.footing_material),
            ),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
            ),
        )
                     
        self.dink_sounds = (
            ba.getsound('bombDrop01'),
            ba.getsound('bombDrop02'),
        )
        self.sticky_impact_sound = ba.getsound('stickyImpact')
        self.sticky_impact_player_sound = ba.getsound('stickyImpactPlayer')
        self.roll_sound = ba.getsound('bombRoll01')

        # Collision sounds.
        self.normal_sound_material.add_actions(
            conditions=('they_have_material', shared.footing_material),
            actions=(
                ('impact_sound', self.dink_sounds, 2, 0.8),
                ('roll_sound', self.roll_sound, 3, 6),
            ),
        )

        self.sticky_material.add_actions(
            actions=(
                ('modify_part_collision', 'stiffness', 0.1),
                ('modify_part_collision', 'damping', 1.0),
            )
        )

        self.sticky_material.add_actions(
            conditions=(
                ('they_have_material', shared.player_material),
                'or',
                ('they_have_material', shared.footing_material),
            ),
            actions=('message', 'our_node', 'at_connect', SplatMessage()),
        )
        
        self.tacky_material.add_actions(actions=(('modify_part_collision',
                                                   'stiffness', 0.4),
                                                  ('modify_part_collision',
                                                   'damping', 0.4)))
                                                   
        self.tacky_material.add_actions(
            conditions=(
                ('they_have_material', shared.player_material),
                'or',
                ('they_have_material', shared.footing_material),
            ),
            actions=('message', 'our_node', 'at_connect', DripMessage()),
        )
        
class SplatMessage:
    """Tells an object to make a splat noise."""
    
class DripMessage:
    """Tells an object to make a drip noise."""


class ExplodeMessage:
    """Tells an object to explode."""


class ImpactMessage:
    """Tell an object it touched something."""

class ArmMessage:
    """Tell an object to become armed."""

class ReadyMessage:
    """Visuals for Vital Bomb before blast."""

class PresentMessage:
    """Tell da present to become DENSE!!!"""

class JumpPadMessage:
    """Let the Jump-Pad do it's magic."""

class slingshotMessage:
    """Let the slingshot do it's magic."""
    
class WarnMessage:
    """Tell an object to issue a warning sound."""
    
class AlarmMessage:
    """Tell the Unwanted Present to ding before exploding."""
    
class EngineMessage:
    """Tell the Steam Bomb to sound faster before exploding."""

class AnimeyMessage:
    """Various animations for bombs."""

class DeleteNodeMessage:
    """Tells the object to delete itself."""
    
class ExplodeHitMessage:
    """Tell an object it was hit by an explosion."""

class StandMessage:
    """Tell an object to stand where it needs to."""


class Blast(ba.Actor):
    """An explosion, as generated by a bomb or some other object.

    category: Gameplay Classes
    """

    def __init__(
        self,
        position: Sequence[float] = (0.0, 1.0, 0.0),
        velocity: Sequence[float] = (0.0, 0.0, 0.0),
        blast_radius: float = 2.0,
        blast_type: str = 'normal',
        source_player: ba.Player | None = None,
        hit_type: str = 'explosion',
        hit_subtype: str = 'normal',
    ):
        """Instantiate with given values."""

        # bah; get off my lawn!
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements

        super().__init__()

        shared = SharedObjects.get()
        factory = BombFactory.get()

        self.blast_type = blast_type
        self._source_player = source_player
        self.hit_type = hit_type
        self.hit_subtype = hit_subtype
        self.radius = blast_radius

        # Set our position a bit lower so we throw more things upward.
        rmats = (factory.blast_material, shared.attack_material)
        self.node = ba.newnode(
            'region',
            delegate=self,
            attrs={
                'position': (position[0], position[1] - 0.1, position[2]),
                'scale': (self.radius, self.radius, self.radius),
                'type': 'sphere',
                'materials': rmats,
            },
        )

        ba.timer(0.05, self.node.delete)

        # Throw in an explosion and flash.
        evel = (velocity[0], max(-1.0, velocity[1]), velocity[2])
        explosion = ba.newnode(
            'explosion',
            attrs={
                'position': position,
                'velocity': evel,
                'radius': self.radius,
                'big': (self.blast_type in ['tnt', 'tnt_toxic', 'tnt_ice', 'tnt_glue']),
            },
        )
        if self.blast_type == 'normal':
            explosion.color = (1.0, 0.88, 0.0)
        
        if self.blast_type == 'sticky':
            explosion.color = (0.67, 1.0, 0.41)
        
        if self.blast_type == 'land_mine':
            explosion.color = (0.34, 0.92, 0.67)
            
        if self.blast_type == 'lite_mine':
            self.blast_type = blast_type
            self._source_player = source_player
            self.hit_type = hit_type
            self.hit_subtype = 'lite'
            self.radius = blast_radius
            explosion.color = (0.34, 0.92, 0.67)
        
        if self.blast_type == 'impact':
            explosion.color = (0.13, 0.13, 0.13)
            
        if self.blast_type == 'tacky':
            explosion.color = (0.67, 1.0, 0.41)
        
        if self.blast_type == 'flying_glove':
            explosion.color = (0.34, 0.92, 0.67)
            
        if self.blast_type == 'vital':
            self.blast_type = blast_type
            self._source_player = source_player
            self.hit_type = hit_type
            self.hit_subtype = 'vital'
            self.radius = blast_radius
            explosion.color = (1.0, 0.88, 0.0)
            
        if self.blast_type == 'clouder':
            self.blast_type = blast_type
            self._source_player = source_player
            self.hit_type = hit_type
            self.hit_subtype = 'cloudy'
            self.radius = blast_radius
            explosion.color = (0.5, 0.25, 1)
            
        if self.blast_type == 'present':
            explosion.color = (1, 0, 0)
            
        if self.blast_type == 'steampunk':
            explosion.color = (0, 0, 0)
        
        if self.blast_type == 'cluster':
            explosion.color = (1, 0, 0)
        
        if self.blast_type == 'tnt_glue':
            explosion.color = (1, 0.8, 0.5)
        
        if self.blast_type in ['toxic', 'tnt_toxic']:
            self.blast_type = blast_type
            self._source_player = source_player
            self.hit_type = hit_type
            self.hit_subtype = 'toxic'
            self.radius = blast_radius
            explosion.color = (0.67, 1.0, 0.41)
            
        if self.blast_type == 'flutter_mine':
            self.blast_type = blast_type
            self._source_player = source_player
            self.hit_type = hit_type
            self.hit_subtype = 'flutter'
            self.radius = blast_radius
            explosion.color = (0.5, 0.25, 1)
        
        if self.blast_type == 'glue_mine':
            explosion.color = (1, 0.8, 0.5)
            
        if self.blast_type in ['ice', 'tnt_ice']:
            self.hit_subtype = 'ice'
            explosion.color = (0.2, 1, 0.67)

        ba.timer(1.0, explosion.delete)
        
        if self.blast_type != 'ice':
            ba.emitfx(
                position=position,
                velocity=velocity,
                count=int(1.0 + random.random() * 4),
                emit_type='tendrils',
                tendril_type='thin_smoke',
            )
        ba.emitfx(
            position=position,
            velocity=velocity,
            count=int(4.0 + random.random() * 4),
            emit_type='tendrils',
            tendril_type='ice' if self.blast_type in ['ice', 'tnt_ice'] else 'smoke',
        )
        ba.emitfx(
            position=position,
            emit_type='distortion',
            spread=1.0 if self.blast_type in ['tnt', 'tnt_ice', 'tnt_toxic', 'tnt_glue'] else 2.0,
        )
        
        # And emit some shrapnel.
        if self.blast_type == 'ice':

            def emit() -> None:
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=30 if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                    spread=2.0,
                    scale=0.4,
                    chunk_type='ice',
                    emit_type='stickers',
                )

            # It looks better if we delay a bit.
            ba.timer(0.05, emit)
        
        elif self.blast_type == 'tnt_ice':

            def emit() -> None:
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=30 if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                    spread=4.0,
                    scale=0.8,
                    chunk_type='ice',
                    emit_type='stickers',
                )
                
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=30 if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                    spread=4.0,
                    scale=0.8,
                    chunk_type='ice',
                )

            # It looks better if we delay a bit.
            ba.timer(0.05, emit)
            
        elif self.blast_type == 'sticky':

            def emit() -> None:
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 3,
                    spread=0.7,
                    chunk_type='slime',
                )
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 3,
                    scale=0.5,
                    spread=0.7,
                    chunk_type='slime',
                )
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=15 if not ba.app.config.get("BSE: Reduced Particles", False) else 7,
                    scale=0.6,
                    chunk_type='slime',
                    emit_type='stickers',
                )
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=20 if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                    scale=0.7,
                    chunk_type='spark',
                    emit_type='stickers',
                )
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=int(6.0 + random.random() * 12) if not ba.app.config.get("BSE: Reduced Particles", False) else 3,
                    scale=0.8,
                    spread=1.5,
                    chunk_type='spark',
                )

            # It looks better if we delay a bit.
            ba.timer(0.05, emit)
        
        elif self.blast_type == 'tacky':

            def emit() -> None:
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          spread=0.7,
                          chunk_type='metal')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          scale=0.5,
                          spread=0.7,
                          chunk_type='slime')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          scale=0.5,
                          spread=0.7,
                          chunk_type='slime')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=15 if not ba.app.config.get("BSE: Reduced Particles", False) else 6,
                          scale=0.6,
                          chunk_type='metal',
                          emit_type='stickers')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=20 if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                          scale=0.7,
                          chunk_type='spark',
                          emit_type='stickers')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(6.0 + random.random() * 12) if not ba.app.config.get("BSE: Reduced Particles", False) else 3,
                          scale=0.8,
                          spread=1.5,
                          chunk_type='spark')

            ba.timer(0.05, emit)
            
        elif self.blast_type == 'lite_mine':

            def emit() -> None:
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          spread=0.7,
                          chunk_type='spark')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          scale=0.5,
                          spread=0.7,
                          chunk_type='spark')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          scale=0.5,
                          spread=0.7,
                          chunk_type='metal')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=20 if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                          scale=0.7,
                          chunk_type='ice',
                          emit_type='stickers')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(6.0 + random.random() * 12) if not ba.app.config.get("BSE: Reduced Particles", False) else 3,
                          scale=0.8,
                          spread=1.5,
                          chunk_type='spark')

            ba.timer(0.05, emit)
        
        elif self.blast_type == 'flying_glove':

            def emit() -> None:
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=3,
                          spread=0.7,
                          chunk_type='spark')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=3,
                          scale=0.5,
                          spread=0.7,
                          chunk_type='spark')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=8 if not ba.app.config.get("BSE: Reduced Particles", False) else 4,
                          scale=0.7,
                          chunk_type='ice',
                          emit_type='stickers')
                          
            ba.timer(0.05, emit)
            
        elif self.blast_type == 'impact':

            def emit() -> None:
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                    scale=0.8,
                    chunk_type='metal',
                )
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                    scale=0.4,
                    chunk_type='metal',
                )
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=20 if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                    scale=0.7,
                    chunk_type='spark',
                    emit_type='stickers',
                )
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=int(8.0 + random.random() * 15) if not ba.app.config.get("BSE: Reduced Particles", False) else 4,
                    scale=0.8,
                    spread=1.5,
                    chunk_type='spark',
                )

            # It looks better if we delay a bit.
            ba.timer(0.05, emit)
            
        elif self.blast_type == 'present':

            def emit() -> None:
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(9.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 4,
                          spread=0.7,
                          chunk_type='spark')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          scale=0.5,
                          spread=0.7,
                          chunk_type='spark',
                          emit_type='stickers')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          scale=0.5,
                          spread=0.7,
                          chunk_type='spark',
                          emit_type='stickers')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=15 if not ba.app.config.get("BSE: Reduced Particles", False) else 7,
                          scale=0.6,
                          chunk_type='spark')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=20 if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                          scale=0.7,
                          chunk_type='spark',
                          emit_type='stickers')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(9.0 + random.random() * 12) if not ba.app.config.get("BSE: Reduced Particles", False) else 4,
                          scale=0.8,
                          spread=1.5,
                          chunk_type='spark',
                          emit_type='stickers')

            ba.timer(0.05, emit)
        
        elif self.blast_type == 'clouder':

            def emit() -> None:
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(9.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 5,
                          spread=0.7,
                          chunk_type='spark')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          scale=0.5,
                          spread=0.7,
                          chunk_type='spark',)
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          scale=0.5,
                          spread=0.7,
                          chunk_type='spark')

            ba.timer(0.05, emit)
        
        elif self.blast_type == 'steampunk':

            def emit() -> None:
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(8) if not ba.app.config.get("BSE: Reduced Particles", False) else 4,
                          spread=0.4,
                          chunk_type='splinter')
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=15 if not ba.app.config.get("BSE: Reduced Particles", False) else 7,
                    scale=1.0,
                    chunk_type='spark',
                    emit_type='stickers',
                )
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=int(25.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                    scale=0.7,
                    chunk_type='metal',
                )
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=4,
                    scale=1.0,
                    chunk_type='ice',
                    emit_type='stickers',
                )
                ba.emitfx(
                position=position,
                velocity=velocity,
                count=int(15) if not ba.app.config.get("BSE: Reduced Particles", False) else 7,
                spread=15,
                emit_type='tendrils',
                tendril_type='thin_smoke',
            )

            ba.timer(0.05, emit)
        
        elif self.blast_type == 'cluster':

            def emit() -> None:
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=15 if not ba.app.config.get("BSE: Reduced Particles", False) else 7,
                    scale=1.0,
                    chunk_type='spark',
                    emit_type='stickers',
                )
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=int(25.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                    scale=0.7,
                    chunk_type='metal',
                )

            ba.timer(0.05, emit)
        
        elif self.blast_type == 'toxic':

            def emit() -> None:
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          spread=0.7,
                          chunk_type='metal')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          scale=0.5,
                          spread=0.7,
                          chunk_type='metal')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          scale=0.5,
                          spread=0.7,
                          chunk_type='slime')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=15 if not ba.app.config.get("BSE: Reduced Particles", False) else 7,
                          scale=0.6,
                          chunk_type='metal',
                          emit_type='stickers')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=20 if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                          scale=0.7,
                          chunk_type='slime',
                          emit_type='stickers')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(6.0 + random.random() * 12) if not ba.app.config.get("BSE: Reduced Particles", False) else 3,
                          scale=0.8,
                          spread=1.5,
                          chunk_type='spark')

            ba.timer(0.05, emit)
        
        elif self.blast_type == 'tnt_toxic':

            def emit() -> None:
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          spread=1,
                          chunk_type='metal')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          scale=0.5,
                          spread=2,
                          chunk_type='metal')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          scale=0.5,
                          spread=2,
                          chunk_type='slime')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=15 if not ba.app.config.get("BSE: Reduced Particles", False) else 7,
                          scale=0.6,
                          chunk_type='metal',
                          emit_type='stickers')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=20 if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                          scale=0.7,
                          chunk_type='slime',
                          emit_type='stickers')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(6.0 + random.random() * 12) if not ba.app.config.get("BSE: Reduced Particles", False) else 3,
                          scale=0.8,
                          spread=2,
                          chunk_type='spark')

            ba.timer(0.05, emit)
            
        elif self.blast_type == 'flutter_mine':

            def emit() -> None:
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(10.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 5,
                          scale=1,
                          spread=0.7,
                          chunk_type='spark')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          scale=0.5,
                          spread=0.7,
                          chunk_type='spark',
                          emit_type='stickers')
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                          scale=0.5,
                          spread=0.7,
                          chunk_type='metal',
                          emit_type='stickers')


            ba.timer(0.05, emit)
        
        elif self.blast_type == 'glue_mine':

            def emit() -> None:
                ba.emitfx(position=position,
                          velocity=velocity,
                          count=int(10.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 5,
                          scale=1,
                          spread=0.7,
                          chunk_type='metal')


            ba.timer(0.05, emit)

        elif self.blast_type == 'vital':
            bseVFX('vitalbomb', position, velocity)
            
        else:  # Regular or land mine bomb shrapnel.
        
            def emit() -> None:
                if self.blast_type != 'tnt':
                    ba.emitfx(
                        position=position,
                        velocity=velocity,
                        count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                        chunk_type='rock',
                    )
                    ba.emitfx(
                        position=position,
                        velocity=velocity,
                        count=int(4.0 + random.random() * 8) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                        scale=0.5,
                        chunk_type='rock',
                    )
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=30 if not ba.app.config.get("BSE: Reduced Particles", False) else 15,
                    scale=1.0 if self.blast_type == 'tnt' else 0.7,
                    chunk_type='spark',
                    emit_type='stickers',
                )
                ba.emitfx(
                    position=position,
                    velocity=velocity,
                    count=int(18.0 + random.random() * 20) if not ba.app.config.get("BSE: Reduced Particles", False) else 9,
                    scale=1.0 if self.blast_type == 'tnt' else 0.8,
                    spread=1.5,
                    chunk_type='spark',
                )

                # TNT throws splintery chunks.
                if self.blast_type == 'tnt':

                    def emit_splinters() -> None:
                        ba.emitfx(
                            position=position,
                            velocity=velocity,
                            count=int(20.0 + random.random() * 25) if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                            scale=0.8,
                            spread=1.0,
                            chunk_type='splinter',
                        )

                    ba.timer(0.01, emit_splinters)

                # Every now and then do a sparky one.
                if self.blast_type == 'tnt' or random.random() < 0.1:

                    def emit_extra_sparks() -> None:
                        ba.emitfx(
                            position=position,
                            velocity=velocity,
                            count=int(10.0 + random.random() * 20) if not ba.app.config.get("BSE: Reduced Particles", False) else 5,
                            scale=0.8,
                            spread=1.5,
                            chunk_type='spark',
                        )

                    ba.timer(0.02, emit_extra_sparks)

            # It looks better if we delay a bit.
            ba.timer(0.05, emit)
            
        lcolor = (0.6, 0.6, 1.0) if self.blast_type == 'ice' else (1, 0.3, 0.1)
        light = ba.newnode(
            'light',
            attrs={
                'position': position,
                'volume_intensity_scale': 10.0,
                'color': lcolor,
            },
        )

        scl = random.uniform(0.6, 0.9)
        scorch_radius = light_radius = self.radius
        if self.blast_type in ['tnt', 'tnt_ice', 'tnt_toxic', 'tnt_glue']:
            light_radius *= 1.4
            scorch_radius *= 1.15
            scl *= 3.0

        iscale = 1.6
        ba.animate(
            light,
            'intensity',
            {
                0: 2.0 * iscale,
                scl * 0.02: 0.1 * iscale,
                scl * 0.025: 0.2 * iscale,
                scl * 0.05: 17.0 * iscale,
                scl * 0.06: 5.0 * iscale,
                scl * 0.08: 4.0 * iscale,
                scl * 0.2: 0.6 * iscale,
                scl * 2.0: 0.00 * iscale,
                scl * 3.0: 0.0,
            },
        )
        ba.animate(
            light,
            'radius',
            {
                0: light_radius * 0.2,
                scl * 0.05: light_radius * 0.55,
                scl * 0.1: light_radius * 0.3,
                scl * 0.3: light_radius * 0.15,
                scl * 1.0: light_radius * 0.05,
            },
        )
        ba.timer(scl * 3.0, light.delete)
        if self.blast_type == 'steampunk':
            light_radius *= 1.4
            scorch_radius *= 1.15
            scl *= 3.0

        iscale = 1.6
        ba.animate(
            light,
            'intensity',
            {
                0: 2.0 * iscale,
                scl * 0.02: 0.1 * iscale,
                scl * 0.025: 0.2 * iscale,
                scl * 0.05: 17.0 * iscale,
                scl * 0.06: 5.0 * iscale,
                scl * 0.08: 4.0 * iscale,
                scl * 0.2: 0.6 * iscale,
                scl * 2.0: 0.00 * iscale,
                scl * 3.0: 0.0,
            },
        )
        ba.animate(
            light,
            'radius',
            {
                0: light_radius * 0.2,
                scl * 0.05: light_radius * 0.55,
                scl * 0.1: light_radius * 0.3,
                scl * 0.3: light_radius * 0.15,
                scl * 1.0: light_radius * 0.05,
            },
        )
        ba.timer(scl * 3.0, light.delete)

        # Make a scorch that fades over time.
        scorch = ba.newnode(
            'scorch',
            attrs={
                'position': position,
                'size': scorch_radius * 0.5,
                'big': (self.blast_type in ['tnt', 'tnt_ice', 'tnt_toxic', 'tnt_glue']),
            },
        )
        if self.blast_type in ['ice', 'tnt_ice']:
            scorch.color = (1, 1, 1.5)

        ba.animate(scorch, 'presence', {3.000: 1, 13.000: 0})
        ba.timer(13.0, scorch.delete)

        if self.blast_type == 'ice':
            ba.playsound(factory.hiss_sound, position=light.position)

        lpos = light.position
        ba.playsound(factory.random_explode_sound(), position=lpos)
        ba.playsound(factory.debris_fall_sound, position=lpos)
        
        if self.blast_type == 'present':
            ba.playsound(factory.present_blast, position=light.position)
            
        if self.blast_type == 'tacky':
            ba.playsound(factory.tacky_blast, position=light.position)
            scorch.color = (0.75, 1, 0.2)

        ba.animate(scorch, 'presence', {3.000: 1, 13.000: 0})
        ba.timer(13.0, scorch.delete)

        if self.blast_type == 'clouder':
            ba.playsound(factory.clouder_blast, position=light.position)
            scorch.color = (0.5, 0.25, 1)
        
        if self.blast_type == 'vital':
            ba.playsound(factory.vital_blast, position=light.position)
            scorch.color = (1.0, 0.88, 0.0)
            
        if self.blast_type == 'toxic':
            ba.playsound(factory.toxic_blast, position=light.position)
            scorch.color = (0.75, 1, 0.2)
        
        if self.blast_type == 'tnt_toxic':
            ba.playsound(factory.tnt_toxic_blast, position=light.position)
            scorch.color = (0.75, 1, 0.2)
        
        if self.blast_type == 'tnt_glue':
            ba.playsound(factory.tnt_glue_blast, position=light.position)
            scorch.color = (1, 0.8, 0.5)
            
        if self.blast_type == 'tnt_ice':
            ba.playsound(factory.tnt_ice_blast, position=light.position)
            
            def _extra_boom() -> None:
                ba.playsound(factory.random_explode_sound(), position=lpos)

            ba.timer(0.25, _extra_boom)
            
        if self.blast_type == 'steampunk':
            ba.playsound(factory.steampunk_blast, position=light.position)
            scorch.color = (0, 0, 0)
            
        ba.animate(scorch, 'presence', {3.000: 1, 13.000: 0})
        ba.timer(13.0, scorch.delete)
        
        if self.blast_type == 'cluster':
            ba.playsound(factory.cluster_blast, position=light.position)
            scorch.color = (1, 0, 0)
            
        if self.blast_type == 'flutter_mine':
            ba.playsound(factory.clouder_blast, position=light.position)
            scorch.color = (0.5, 0.25, 1)
        
        if self.blast_type == 'glue_mine':
            ba.playsound(factory.glue_mine_sound, position=light.position)
            scorch.color = (1, 0.8, 0.5)
            
        if self.blast_type == 'lite_mine':
            scorch.color = (0.0, 0.6, 0.75)
        
        if self.blast_type == 'flying_glove':
            ba.playsound(factory.flying_glove_blast, position=light.position)
            scorch.color = (0.0, 0.6, 0.75)

        ba.animate(scorch, 'presence', {3.000: 1, 13.000: 0})
        ba.timer(13.0, scorch.delete)
        
        if self.blast_type == 'present':
            scorch.color = (1, 0, 0)

        ba.animate(scorch, 'presence', {3.000: 1.55, 13.000: 0})
        ba.timer(23.0, scorch.delete)
        
        ba.camerashake(intensity=5.0 if self.blast_type in ['tnt', 'tnt_ice', 'tnt_toxic', 'tnt_glue'] else 1.0)
        ba.camerashake(intensity=5.3 if self.blast_type == 'present' else 1.0)
        ba.camerashake(intensity=4.5 if self.blast_type == 'steampunk' else 1.0)
        # TNT is more epic.
        if self.blast_type == 'tnt':
            ba.playsound(factory.random_explode_sound(), position=lpos)

            def _extra_boom() -> None:
                ba.playsound(factory.random_explode_sound(), position=lpos)

            ba.timer(0.25, _extra_boom)

            def _extra_debris_sound() -> None:
                ba.playsound(factory.debris_fall_sound, position=lpos)
                ba.playsound(factory.wood_debris_fall_sound, position=lpos)

            ba.timer(0.4, _extra_debris_sound)
            
        if self.blast_type == 'lite_mine':
            ba.playsound(factory.skymine_sound, position=self.node.position,)
            
        if self.blast_type == 'steampunk':
            ba.playsound(factory.debris_fall_sound, position=lpos)
            ba.playsound(factory.wood_debris_fall_sound, position=lpos)
            
    def handlemessage(self, msg: Any) -> Any:
        assert not self.expired

        if isinstance(msg, ba.DieMessage):
            if self.node:
                self.node.delete()

        elif isinstance(msg, ExplodeHitMessage):
            node = ba.getcollision().opposingnode
            assert self.node
            nodepos = self.node.position
            mag = 2000.0
            if self.blast_type == 'ice':
                mag *= 0.5
            elif self.blast_type == 'land_mine':
                mag *= 2.5
            elif self.blast_type == 'lite_mine':
                mag *= 0.5
            elif self.blast_type == 'vital':
                mag *= 0.01
            elif self.blast_type == 'flutter_mine':
                mag *= 2
            elif self.blast_type == 'glue_mine':
                mag *= 0.55
            elif self.blast_type == 'present':
                mag *= 2.0
            elif self.blast_type == 'tacky':
                mag *= 1.6
            elif self.blast_type == 'flying_glove':
                mag *= 0.65
            elif self.blast_type == 'clouder':
                mag *= 2
            elif self.blast_type == 'steampunk':
                mag *= 1.5
            elif self.blast_type == 'cluster':
                mag *= 0.6
            elif self.blast_type == 'little_cluster':
                mag *= 0.7
            elif self.blast_type == 'toxic':
                mag *= 0.4
            elif self.blast_type == 'tnt':
                mag *= 2.0
            elif self.blast_type == 'tnt_ice':
                mag *= 1.1
            elif self.blast_type == 'tnt_toxic':
                mag *= 1.8
            elif self.blast_type == 'tnt_glue':
                mag *= 1.9

            node.handlemessage(
                ba.HitMessage(
                    pos=nodepos,
                    velocity=(0, 0, 0),
                    magnitude=mag,
                    hit_type=self.hit_type,
                    hit_subtype=self.hit_subtype,
                    radius=self.radius,
                    source_player=ba.existing(self._source_player),
                )
            )
            if self.blast_type == 'ice':
                ba.playsound(
                    BombFactory.get().freeze_sound, 10, position=nodepos
                )
                node.handlemessage(ba.FreezeMessage())
            
            if self.blast_type == 'tnt_ice':
                ba.playsound(
                    BombFactory.get().freeze_sound, 10, position=nodepos
                )
                node.handlemessage(ba.TNTFreezeMessage())
                
            if self.blast_type in ['toxic', 'tnt_toxic']:
                node.handlemessage(ba.ToxicMessage())
                node.handlemessage(ba.PoisonedMessage())
                
            if self.blast_type == 'vital':
                node.handlemessage(ba.VitalMessage(
                    pos=nodepos,
                    velocity=(0, 0, 0),
                    magnitude=mag,
                    hit_type=self.hit_type,
                    hit_subtype=self.hit_subtype,
                    radius=self.radius,
                    source_player=ba.existing(self._source_player),
                )
            )
                
        else:
            return super().handlemessage(msg)
        return None

def get_bomb_types(
    include_bombs = True,
    include_tnt = True,
    include_land_mines = True,
    include_projectiles = True,
    include_non_bombs = True,
):
    ''' Returns all valid bomb types specified. '''
    if not include_bombs and not include_tnt and not include_land_mines and not include_projectiles and not include_non_bombs:
        raise Exception('bro...')
    return ( ([
            'ice',
            'impact',
            'normal',
            'sticky',
            'tacky',
            'vital',
            'clouder',
            'steampunk',
            'cluster',
            'toxic',
        ] if include_bombs else []) + ([
            'tnt',  
            'tnt_ice',
            'tnt_toxic',
            'tnt_glue',
            'present',
        ] if include_tnt else []) + ([
            'land_mine',
            'lite_mine',
            'flutter_mine',
            'glue_mine',
        ] if include_land_mines else []) + ([
            'flying_glove',
        ] if include_projectiles else []) + ([
            'jump_pad',
            'slingshot',
        ] if include_non_bombs else []) )

class Bomb(ba.Actor):
    """A standard bomb and its variants such as land-mines and tnt-boxes.

    category: Gameplay Classes
    """

    # Ew; should try to clean this up later.
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

    def __init__(
        self,
        position: Sequence[float] = (0.0, 1.0, 0.0),
        velocity: Sequence[float] = (0.0, 0.0, 0.0),
        bomb_type: str = 'normal',
        blast_radius: float = 2.0,
        bomb_scale: float = 1.0,
        source_player: ba.Player | None = None,
        owner: ba.Node | None = None,
    ):
        """Create a new Bomb.

        bomb_type can be 'ice','impact','land_mine','normal','sticky', or
        'tnt'. Note that for impact or land_mine bombs you have to call arm()
        before they will go off.
        """
        super().__init__()

        shared = SharedObjects.get()
        factory = BombFactory.get()

        if bomb_type not in get_bomb_types():
            raise ValueError('invalid bomb type: ' + bomb_type)
        self.bomb_type = bomb_type

        self._exploded = False
        self.scale = bomb_scale

        self.texture_sequence: ba.Node | None = None

        if self.bomb_type == 'sticky':
            self._last_sticky_sound_time = 0.0
        elif self.bomb_type == 'tacky':
            self._last_tacky_sound_time = 0.0

        self.blast_radius = blast_radius
        if self.bomb_type == 'ice':
            self.blast_radius *= 1.15
        elif self.bomb_type == 'impact':
            self.blast_radius *= 0.7
        elif self.bomb_type == 'flying_glove':
            self.blast_radius *= 0.85
        elif self.bomb_type == 'flutter_mine':
            self.blast_radius *= 0.8
        elif self.bomb_type == 'glue_mine':
            self.blast_radius *= 0.8
        elif self.bomb_type == 'tacky':
            self.blast_radius *= 0.55
        elif self.bomb_type == 'clouder':
            self.blast_radius *= 1
        elif self.bomb_type == 'steampunk':
            self.blast_radius *= 1.35
        elif self.bomb_type == 'cluster':
            self.blast_radius *= 1.2
        elif self.bomb_type == 'toxic':
            self.blast_radius *= 1.15
        elif self.bomb_type == 'vital':
            self.blast_radius *= 1.05
        elif self.bomb_type == 'land_mine':
            self.blast_radius *= 0.7
        elif self.bomb_type == 'lite_mine':
            self.blast_radius *= 0.6
        elif self.bomb_type == 'present':
            self.blast_radius *= 1.80
        elif self.bomb_type in ['tnt', 'tnt_ice', 'tnt_toxic', 'tnt_glue']:
            self.blast_radius *= 1.50

        self._explode_callbacks: list[Callable[[Bomb, Blast], Any]] = []

        # The player this came from.
        self._source_player = source_player
        self._vital_buff_state = 0

        # By default our hit type/subtype is our own, but we pick up types of
        # whoever sets us off so we know what caused a chain reaction.
        # UPDATE (July 2020): not inheriting hit-types anymore; this causes
        # weird effects such as land-mines inheriting 'punch' hit types and
        # then not being able to destroy certain things they normally could,
        # etc. Inheriting owner/source-node from things that set us off
        # should be all we need I think...
        self.hit_type = 'explosion'
        self.hit_subtype = self.bomb_type

        # Vital stuff
        self._vitalp_light: ba.Node | None = None
        self._vitalp_timer: ba.Timer | None = None
        self._buff_explosion_light: ba.Node | None = None

        # The node this came from.
        # FIXME: can we unify this and source_player?
        self.owner = owner

        # Adding footing-materials to things can screw up jumping and flying
        # since players carrying those things and thus touching footing
        # objects will think they're on solid ground.. perhaps we don't
        # wanna add this even in the tnt case?
        materials: tuple[ba.Material, ...]
        if self.bomb_type in ['tnt', 'tnt_ice', 'tnt_toxic', 'tnt_glue']:
            materials = (
                factory.bomb_material,
                shared.object_material,
            )
        else:
            materials = (factory.bomb_material, shared.object_material)

        if self.bomb_type == 'impact':
            materials = materials + (factory.impact_blast_material,)
        elif self.bomb_type == 'flying_glove':
            materials = (factory.bomb_material, factory.glove_material, factory.impact_blast_material,)
        elif self.bomb_type == 'land_mine':
            materials = materials + (factory.land_mine_no_explode_material,)
        elif self.bomb_type == ('lite_mine'):
            materials = materials + (factory.land_mine_no_explode_material, )
        elif self.bomb_type == ('flutter_mine'):
            materials = materials + (factory.land_mine_no_explode_material, )
        elif self.bomb_type == ('glue_mine'):
            materials = materials + (factory.land_mine_no_explode_material, )
        if self.bomb_type == 'sticky':
            materials = materials + (factory.sticky_material,)
        if self.bomb_type == 'present':
            materials = materials + (shared.footing_material, )
        if self.bomb_type == 'jump_pad':
            materials = (factory.jumppad_material, )
        elif self.bomb_type == 'slingshot':
            materials = (factory.bomb_material, factory.slingshot_material)
        else:
            materials = materials + (factory.normal_sound_material,)
        
        if self.bomb_type == 'tacky':
            materials = materials + (factory.tacky_material, )
        else:
            materials = materials + (factory.normal_sound_material, )
        if self.bomb_type == 'land_mine':
            fuse_time = None
            self.node = ba.newnode(
                'prop',
                delegate=self,
                attrs={
                    'position': position,
                    'velocity': velocity,
                    'model': factory.land_mine_model,
                    'light_model': factory.land_mine_model,
                    'body': 'landMine',
                    'body_scale': self.scale,
                    'shadow_size': 0.44,
                    'color_texture': factory.land_mine_tex,
                    'reflection': 'powerup',
                    'reflection_scale': [1.0],
                    'materials': materials,
                },
            )

        elif self.bomb_type == 'lite_mine':
            fuse_time = None
            self.node = ba.newnode('prop',
                                   delegate=self,
                                   attrs={
                                       'position': position,
                                       'velocity': velocity,
                                       'model': factory.lite_mine_model,
                                       'light_model': factory.lite_mine_model,
                                       'body': 'landMine',
                                       'body_scale': self.scale,
                                       'shadow_size': 0.44,
                                       'color_texture': factory.lite_mine_tex,
                                       'reflection': 'powerup',
                                       'reflection_scale': [1.5],
                                       'materials': materials,
                                       'density': 0.8
                                   })
        
        elif self.bomb_type == 'flutter_mine':
            fuse_time = None
            self.node = ba.newnode('prop',
                                   delegate=self,
                                   attrs={
                                       'position': position,
                                       'velocity': velocity,
                                       'model': factory.flutter_mine_model,
                                       'light_model': factory.flutter_mine_model,
                                       'body': 'landMine',
                                       'body_scale': self.scale,
                                       'shadow_size': 0.44,
                                       'color_texture': factory.flutter_mine_tex,
                                       'reflection': 'sharper',
                                       'reflection_scale': [1.5],
                                       'materials': materials,
                                       'density': 1
                                   })
        elif self.bomb_type == 'glue_mine':
            fuse_time = None
            self.node = ba.newnode('prop',
                                   delegate=self,
                                   attrs={
                                       'position': position,
                                       'velocity': velocity,
                                       'model': factory.glue_mine_model,
                                       'light_model': factory.glue_mine_model,
                                       'body': 'landMine',
                                       'body_scale': self.scale,
                                       'shadow_size': 0.44,
                                       'color_texture': factory.glue_mine_tex,
                                       'reflection': 'sharper',
                                       'reflection_scale': [1.5],
                                       'materials': materials,
                                       'density': 1
                                   })
        elif self.bomb_type == 'present':
            fuse_time = 30
            self.node = ba.newnode('prop',
                                   delegate=self,
                                   attrs={
                                       'position': position,
                                       'velocity': velocity,
                                       'model': factory.present_bomb_model,
                                       'light_model': factory.present_bomb_model,
                                       'body': 'crate',
                                       'body_scale': self.scale,
                                       'shadow_size': 0.5,
                                       'color_texture': factory.present_bomb_tex,
                                       'reflection': 'powerup',
                                       'reflection_scale': [0.23],
                                       'materials': materials,
                                       'density': 0.6
                                   })
        
        elif self.bomb_type == 'jump_pad':
            fuse_time = None
            self.node = ba.newnode('prop',
                                   delegate=self,
                                   attrs={
                                       'position': position,
                                       'velocity': velocity,
                                       'model': factory.jumppad_model,
                                       'light_model': factory.jumppad_model,
                                       'body': 'landMine',
                                       'body_scale': self.scale,
                                       'shadow_size': 0.5,
                                       'color_texture': factory.jumppad_tex,
                                       'reflection': 'powerup',
                                       'reflection_scale': [0.23],
                                       'materials': materials,
                                       'gravity_scale': 13
                                   })
            self.jumppad_light = ba.newnode('light',
                          owner=self.node,
                          attrs={'position':self.node.position,
                                  'radius':0.0,
                                  'intensity':0.0,
                                  'color': (0, 1, 0),
                                  'volume_intensity_scale': 1.0}) 
            self.node.connectattr('position',self.jumppad_light,'position')
            ba.Timer(1, ba.WeakCall(self.handlemessage, StandMessage()), repeat=True)
        
        elif self.bomb_type == 'slingshot':
            fuse_time = None
            self.node = ba.newnode('prop',
                                   delegate=self,
                                   attrs={
                                       'position': position,
                                       'velocity': velocity,
                                       'model': factory.slingshot_model,
                                       'light_model': factory.slingshot_model,
                                       'body': 'landMine',
                                       'body_scale': self.scale,
                                       'shadow_size': 0.5,
                                       'color_texture': factory.slingshot_tex,
                                       'reflection': 'soft',
                                       'reflection_scale': [0.23],
                                       'materials': materials,
                                       'gravity_scale': 13
                                   })
            self.slingshot_light = ba.newnode('light',
                          owner=self.node,
                          attrs={'position':self.node.position,
                                  'radius':0.0,
                                  'intensity':0.0,
                                  'color': (1, 0.5, 0),
                                  'volume_intensity_scale': 1.0}) 
            self.node.connectattr('position',self.slingshot_light,'position')
                                   
        elif self.bomb_type == 'tnt':
            fuse_time = None
            self.node = ba.newnode(
                'prop',
                delegate=self,
                attrs={
                    'position': position,
                    'velocity': velocity,
                    'model': factory.tnt_model,
                    'light_model': factory.tnt_model,
                    'body': 'crate',
                    'body_scale': self.scale,
                    'shadow_size': 0.5,
                    'color_texture': factory.tnt_tex,
                    'reflection': 'soft',
                    'reflection_scale': [0.23],
                    'materials': materials,
                },
            )
        
        elif self.bomb_type == 'tnt_ice':
            fuse_time = None
            self.node = ba.newnode(
                'prop',
                delegate=self,
                attrs={
                    'position': position,
                    'velocity': velocity,
                    'model': factory.tnt_model,
                    'light_model': factory.tnt_model,
                    'body': 'crate',
                    'body_scale': self.scale,
                    'shadow_size': 0.5,
                    'color_texture': factory.tnt_ice_tex,
                    'reflection': 'sharper',
                    'reflection_scale': [2],
                    'materials': materials,
                },
            )
            
        elif self.bomb_type == 'tnt_toxic':
            fuse_time = None
            self.node = ba.newnode(
                'prop',
                delegate=self,
                attrs={
                    'position': position,
                    'velocity': velocity,
                    'model': factory.tnt_toxic_model,
                    'light_model': factory.tnt_toxic_model,
                    'body': 'crate',
                    'body_scale': self.scale,
                    'shadow_size': 0.5,
                    'color_texture': factory.tnt_toxic_tex,
                    'reflection': 'soft',
                    'reflection_scale': [0.23],
                    'materials': materials,
                },
            )
        
        elif self.bomb_type == 'tnt_glue':
            fuse_time = None
            self.node = ba.newnode(
                'prop',
                delegate=self,
                attrs={
                    'position': position,
                    'velocity': velocity,
                    'model': factory.tnt_glue_model,
                    'light_model': factory.tnt_toxic_model,
                    'body': 'crate',
                    'body_scale': self.scale,
                    'shadow_size': 0.5,
                    'color_texture': factory.tnt_glue_tex,
                    'reflection': 'soft',
                    'reflection_scale': [0.23],
                    'materials': materials,
                },
            )
            
        elif self.bomb_type == 'impact':
            fuse_time = 10.0
            self.node = ba.newnode(
                'prop',
                delegate=self,
                attrs={
                    'position': position,
                    'velocity': velocity,
                    'body': 'sphere',
                    'body_scale': self.scale,
                    'model': factory.impact_bomb_model,
                    'shadow_size': 0.3,
                    'color_texture': factory.impact_tex,
                    'reflection': 'powerup',
                    'reflection_scale': [1.5],
                    'materials': materials,
                },
            )
            self.arm_timer = ba.Timer(
                0.2, ba.WeakCall(self.handlemessage, ArmMessage())
            )
            self.warn_timer = ba.Timer(
                fuse_time - 1.7, ba.WeakCall(self.handlemessage, WarnMessage())
            )
        
        elif self.bomb_type == 'flying_glove':
            fuse_time = 30
            self.node = ba.newnode(
                'prop',
                delegate=self,
                attrs={
                    'position': position,
                    'velocity': velocity,
                    'body': 'sphere',
                    'body_scale': self.scale,
                    'model_scale': 4,
                    'model': factory.flying_glove_model,
                    'shadow_size': 0.3,
                    'color_texture': factory.flying_glove_tex,
                    'reflection': 'soft',
                    'reflection_scale': [0.5],
                    'materials': materials,
                    'gravity_scale': 0.1
                },
            )
            self.node.handlemessage('impulse',self.node.position[0],self.node.position[1],self.node.position[2],
                                0,0,0,
                                400,400,0,0,self.node.velocity[0],self.node.velocity[1],self.node.velocity[2])
            self.glove_light = ba.newnode('light',
                          owner=self.node,
                          attrs={'position':self.node.position,
                                  'radius':0.08,
                                  'intensity':0.7,
                                  'color': (0.34, 0.92, 1),
                                  'volume_intensity_scale': 1.0}) 
            self.node.connectattr('position',self.glove_light,'position')
            
        else:
            fuse_time = 3.0
            if self.bomb_type == 'sticky':
                sticky = True
                model = factory.sticky_bomb_model
                rtype = 'sharper'
                rscale = 1.8
            elif self.bomb_type == 'tacky':
                fuse_time = 2.0
                sticky = True
                model = factory.tacky_bomb_model
                rtype = 'sharper'
                rscale = 1.0
            else:
                sticky = False
                model = factory.bomb_model
                rtype = 'sharper'
                rscale = 1.8
            if self.bomb_type == 'ice':
                tex = factory.ice_tex
                model = factory.ice_bomb_model
            elif self.bomb_type == 'sticky':
                tex = factory.sticky_tex
            elif self.bomb_type == 'tacky':
                tex = factory.tacky_lit_tex
            elif self.bomb_type == 'flutter_mine':
                tex = factory.flutter_mine_tex
            elif self.bomb_type == 'clouder':
                model = factory.clouder_bomb_model
                tex = factory.clouder_tex
                rtype = 'soft'
                rscale = 0.5
            elif self.bomb_type == 'vital':
                fuse_time = 3.0
                model = factory.vital_bomb_model
                tex = factory.vital_tex
                rtype = 'soft'
                rscale = 0.5
                self.arm_timer = ba.Timer(
                0.0, ba.WeakCall(self.handlemessage, ArmMessage())
                )
                self.ready_timer = ba.Timer(
                    fuse_time - 0.5, ba.WeakCall(self.handlemessage, ReadyMessage())
                )
            elif self.bomb_type == 'steampunk':
                fuse_time = 4
                model = factory.steampunk_bomb_model
                tex = factory.steampunk_tex
                rtype = 'soft'
                rscale = 0.23
                self.animey_timer = ba.Timer(
                0.0, ba.WeakCall(self.handlemessage, AnimeyMessage()))
                self.engine_timer = ba.Timer(fuse_time - 1, ba.WeakCall(self.handlemessage,
                                            EngineMessage()))
            elif self.bomb_type == 'cluster':
                fuse_time = 3
                model = factory.cluster_bomb_model
                tex = factory.cluster_tex
                rtype = 'powerup'
                rscale = 0.4
            elif self.bomb_type == 'toxic':
                model = factory.toxic_bomb_model
                tex = factory.toxic_tex
                rtype = 'powerup'
                rscale = 0.5
            else:
                tex = factory.regular_tex
            self.node = ba.newnode(
                'bomb',
                delegate=self,
                attrs={
                    'position': position,
                    'velocity': velocity,
                    'model': model,
                    'body_scale': self.scale,
                    'shadow_size': 0.3,
                    'color_texture': tex,
                    'sticky': sticky,
                    'owner': owner,
                    'reflection': rtype,
                    'reflection_scale': [rscale],
                    'materials': materials,
                },
            )

            sound = ba.newnode(
                'sound',
                owner=self.node,
                attrs={'sound': factory.fuse_sound, 'volume': 0.25},
            )
            self.node.connectattr('position', sound, 'position')
            ba.animate(self.node, 'fuse_length', {0.0: 1.0, fuse_time: 0.0})

        # Light the fuse!!!
        if self.bomb_type not in ('land_mine', 'lite_mine', 'flutter_mine', 'glue_mine', 'tnt', 'tnt_ice', 'tnt_toxic', 'tnt_glue', 'tacky', 'jump_pad', 'slingshot'):
            assert fuse_time is not None
            ba.timer(
                fuse_time, ba.WeakCall(self.handlemessage, ExplodeMessage())
            )

        ba.animate(
            self.node,
            'model_scale',
            {0: 0, 0.2: 1.3 * self.scale, 0.26: self.scale},
        )
        if self.bomb_type == 'tacky':
            assert fuse_time == 2.0
            ba.timer(fuse_time,
                     ba.WeakCall(self.handlemessage, ExplodeMessage()))
            self.node.connectattr('position', sound, 'position')
            ba.animate(self.node, 'fuse_length', {0.0: 0.66, fuse_time: 0.0})

        ba.animate(self.node, 'model_scale', {
            0: 0,
            0.0: 0.65 * self.scale,
            0.13: self.scale
        })    
        
        if self.bomb_type == 'steampunk':
            sound = ba.newnode(
                'sound',
                owner=self.node,
                attrs={'sound': factory.engine_sound, 'volume': 0.75},
            )
            ba.emitfx(
                position=position,
                velocity=velocity,
                count=int(4) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                spread=5,
                emit_type='tendrils',
                tendril_type='smoke',
            )
            self.node.connectattr('position', sound, 'position')
            ba.animate(self.node, 'fuse_length', {0.0: 1.3, fuse_time: 0.0})
        
        if self.bomb_type == 'tacky':
            ba.emitfx(
                position=position,
                velocity=velocity,
                count=5 if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                spread=0.2,
                scale=0.5,
                chunk_type='slime',
            )
         
        if self.bomb_type == 'toxic':
            def toxic_goo():
                    if self.node.exists():
                        ba.emitfx(
                            position=(self.node.position[0],self.node.position[1],self.node.position[2]),
                            velocity=self.node.velocity,
                            count=random.randrange(3,10) if not ba.app.config.get("BSE: Reduced Particles", False) else 5,
                            scale=0.4,
                            spread=0.1,
                            chunk_type='slime')
            ba.timer(0.3,ba.Call(toxic_goo), repeat=True)
            self.toxic_light = ba.newnode('light',
                          owner=self.node,
                          attrs={'position':self.node.position,
                                  'radius':0.05,
                                  'intensity':1.0,
                                  'color': (0.2, 1, 0.2),
                                  'volume_intensity_scale': 1.0}) 
            self.node.connectattr('position',self.toxic_light,'position')
        
        if self.bomb_type == 'tnt_toxic':
            self.toxic_light = ba.newnode('light',
                          owner=self.node,
                          attrs={'position':self.node.position,
                                  'radius':0.05,
                                  'intensity':1.0,
                                  'color': (0.2, 1, 0.2),
                                  'volume_intensity_scale': 1.0}) 
            self.node.connectattr('position',self.toxic_light,'position')
        
        if self.bomb_type == 'flying_glove':
            def sparkies():
                    if self.node.exists():
                        ba.emitfx(
                            position=(self.node.position[0],self.node.position[1],self.node.position[2]),
                            velocity=self.node.velocity,
                            count=random.randrange(3,7) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                            scale=0.4,
                            spread=0.1,
                            chunk_type='spark')
            ba.timer(0.01,ba.Call(sparkies), repeat=True)
            self.animey_timer = ba.Timer(0.0, ba.WeakCall(self.handlemessage, AnimeyMessage()))
            
    def get_source_player(
        self, playertype: type[PlayerType]
    ) -> PlayerType | None:
        """Return the source-player if one exists and is the provided type."""
        player: Any = self._source_player
        return (
            player
            if isinstance(player, playertype) and player.exists()
            else None
        )
    
    def on_expire(self) -> None:
        super().on_expire()

        # Release callbacks/refs so we don't wind up with dependency loops.
        self._explode_callbacks = []

    def _handle_die(self) -> None:
        if self.node:
            self.node.delete()

    def _handle_oob(self) -> None:
        self.handlemessage(ba.DieMessage())

    def _handle_impact(self) -> None:
        node = ba.getcollision().opposingnode

        # If we're an impact bomb and we came from this node, don't explode.
        # (otherwise we blow up on our own head when jumping).
        # Alternately if we're hitting another impact-bomb from the same
        # source, don't explode. (can cause accidental explosions if rapidly
        # throwing/etc.)
        node_delegate = node.getdelegate(object)
        if node:
            if self.bomb_type in ('flying_glove', 'impact') and (
                node is self.owner
                or (
                    isinstance(node_delegate, Bomb)
                    and node_delegate.bomb_type in ('flying_glove', 'impact')
                    and node_delegate.owner is self.owner
                )
            ):
                return
            self.handlemessage(ExplodeMessage())

    def _handle_dropped(self) -> None:
        if self.bomb_type == 'land_mine':
            self.arm_timer = ba.Timer(
                1.25, ba.WeakCall(self.handlemessage, ArmMessage())
            )
        elif self.bomb_type == 'lite_mine':
            self.arm_timer = ba.Timer(
                0.80, ba.WeakCall(self.handlemessage, ArmMessage()))
        elif self.bomb_type == 'flutter_mine':
            self.arm_timer = ba.Timer(
                1.45, ba.WeakCall(self.handlemessage, ArmMessage()))
        elif self.bomb_type == 'glue_mine':
            self.arm_timer = ba.Timer(
                1.25, ba.WeakCall(self.handlemessage, ArmMessage()))
        elif self.bomb_type == 'present':
            self.gravi_timer = ba.Timer(
                1, ba.WeakCall(self.handlemessage, PresentMessage()))
            self.arm_timer = ba.Timer(
                0.1, ba.WeakCall(self.handlemessage, ArmMessage()))
            self.animey_timer = ba.Timer(
                0.1, ba.WeakCall(self.handlemessage, AnimeyMessage()))
            self.alarm_timer = ba.Timer(5.5, ba.WeakCall(self.handlemessage,
                                             AlarmMessage()))

        # Once we've thrown any sticky powerup we can stick to it.
        elif self.bomb_type == 'sticky':

            def _setsticky(node: ba.Node) -> None:
                if node:
                    node.stick_to_owner = True

            ba.timer(0.25, lambda: _setsticky(self.node))
        elif self.bomb_type == 'tacky':

            def _setsticky(node: ba.Node) -> None:
                if node:
                    node.stick_to_owner = True

            ba.timer(0.25, lambda: _setsticky(self.node))

    def _handle_splat(self) -> None:
        node = ba.getcollision().opposingnode
        if (
            node is not self.owner
            and ba.time() - self._last_sticky_sound_time > 1.0
        ):
            self._last_sticky_sound_time = ba.time()
            assert self.node
            ba.playsound(
                BombFactory.get().sticky_impact_sound,
                2.0,
                position=self.node.position,
            )
            if node.getnodetype() == 'spaz':
                ba.playsound(
                BombFactory.get().sticky_impact_player_sound,
                0.3,
                position=self.node.position,
            )

    def _handle_drip(self) -> None:
        node = ba.getcollision().opposingnode
        if (node is not self.owner
                and ba.time() - self._last_tacky_sound_time > 1.0):
            self._last_tacky_sound_time = ba.time()
            assert self.node
            ba.playsound(BombFactory.get().tacky_impact_sound,
                         2.0,
                         position=self.node.position) 
            if node.getnodetype() == 'spaz':
                ba.playsound(
                BombFactory.get().tacky_impact_player_sound,
                0.3,
                position=self.node.position,
            )

    def add_explode_callback(self, call: Callable[[Bomb, Blast], Any]) -> None:
        """Add a call to be run when the bomb has exploded.

        The bomb and the new blast object are passed as arguments.
        """
        self._explode_callbacks.append(call)

    def _vitalized_bomb(self, buff: bool, cstatus: int | None = None) -> None:
        if not self.node:
            return
        
        if not cstatus:
            cstatus = self._vital_buff_state
        
        disregard = (buff and cstatus == -1) or (not buff and cstatus == 1)
        self._vital_buff_state += 1 if buff else -1
        cbuff = self._vital_buff_state > 0
        color = (0.4,0.366,0.12) if cbuff else (0.5,0.25,1)
        intensity = 0.7 if disregard else 1.15

        mult = 1.30

        if not self._vitalp_light:
            # Buff / Nerf respectively
            if buff:   
                self.blast_radius *= mult
            else:      
                self.blast_radius /= mult

            self._vitalp_light = ba.newnode(
                'light',
                attrs={
                    'position': self.node.position,
                    'volume_intensity_scale': 10.0,
                    'intensity':intensity,
                    'color': color,
                    'radius': 0.2,
                },
            )
            self.node.connectattr('position', self._vitalp_light, 'position')
        else:
            # Update the colors on the spot.
            self._vitalp_light.node.color = color
            # Make our light "disappear" if we "disregard", aka. neutralize a buff/nerf.
            self._vitalp_light.node.intensity = intensity

        if not self._vitalp_timer: self._vitalp_timer = ba.Timer(0.333,ba.Call(self._vitalized_particles, cbuff),repeat=True)

    def _vitalized_particles(self, ally:bool) -> None:
        if not self.node:
            self._vitalp_timer = None
            ba.animate_array(self._vitalp_light, 'color', 3, {
                0:self._vitalp_light.color,
                1:(0,0,0),
            })
            ba.Timer(0.1,self._vitalp_light.delete)
            return
        pool: list = [9,0.76] if ally else [5,0.544]
        
        chunk_type = 'metal' if not ally else 'spark'
        spread = 0.1 if not ally else 0.3
        ba.emitfx(
            position=self.node.position,
            velocity=(0,0,0),
            count=pool[0],
            scale=pool[1],
            chunk_type=chunk_type,
            spread=spread,
           )
        
    def explode(self) -> None:
        """Blows up the bomb if it has not yet done so."""
        if self._exploded:
            return
        self._exploded = True
        buff, nerf = [self._vital_buff_state > 0, self._vital_buff_state < 0]
        if self.node:
            blast = Blast(
                position=self.node.position,
                velocity=self.node.velocity,
                blast_radius=self.blast_radius,
                blast_type=self.bomb_type,
                source_player=ba.existing(self._source_player),
                hit_type=self.hit_type,
                hit_subtype=self.hit_subtype,
            ).autoretain()
            for callback in self._explode_callbacks:
                callback(self, blast)
        
            if buff: 
                ba.playsound(BombFactory.get().buff_sound, 0.8, position=self.node.position)
                self._buff_explosion_light = ba.newnode(
                    'light',
                    attrs={
                        'position': self.node.position,
                        'volume_intensity_scale': 10.0,
                        'intensity': 0.0,
                        'color': (1, 0.85, 0),
                        'radius': 0.0,
                    },
                )
                self.node.connectattr('position', self._buff_explosion_light, 'position')
                ba.animate(self._buff_explosion_light,'intensity',{0: 0.75, 1.5: 0.0},loop=False)
                ba.animate(self._buff_explosion_light,'radius',{0: self.blast_radius, 1: 0.0},loop=False)
                ba.timer(1, self._buff_explosion_light.delete)
                
                ba.emitfx(position=self.node.position,
                    velocity=self.node.velocity,
                    count=int(6.0 + random.random() * 12) if not ba.app.config.get("BSE: Reduced Particles", False) else 4,
                    scale=0.8,
                    spread=1,
                    chunk_type='spark')
                    
            if nerf:
                ba.playsound(BombFactory.get().nerf_sound, 0.65, position=self.node.position)
                ba.emitfx(position=self.node.position,
                    velocity=self.node.velocity,
                    count=int(6.0 + random.random() * 12) if not ba.app.config.get("BSE: Reduced Particles", False) else 4,
                    scale=0.8,
                    spread=1,
                    chunk_type='metal')
        
        if self.bomb_type == 'tnt_glue':
            from explodinary.actor.glue import Glue
            p = self.node.position
            v = self.node.velocity
            max_time =      (8.0 if buff else 7.0)
            glue_radius =   (3   if buff else 2  )
            distance =       0.9
            distance2 =      0.75
            height =         10
            time_increment = 1.25
            
            Glue((p[0],p[1],p[2]),
                 (0,height,0),
                 max_time
                 ).autoretain()
            
            for i in range(glue_radius):
                timeformula = (max_time-time_increment) + (time_increment*i)

                Glue((p[0]+distance+(i*distance),p[1],p[2]),
                (0,height,0),
                timeformula
                ).autoretain()
                
                Glue((p[0]-distance-(i*distance),p[1],p[2]),
                (0,height,0),
                timeformula
                ).autoretain()
            
            for i in range(glue_radius):
                timeformula = (max_time-time_increment) + (time_increment*i)

                Glue((p[0]+distance+(i*distance),p[1],p[2]),
                (0,height,0),
                timeformula
                ).autoretain()

                Glue((p[0]-distance-(i*distance),p[1],p[2]),
                (0,height,0),
                timeformula
                ).autoretain()

                Glue((p[0],p[1],p[2]+distance+(i*distance)),
                (0,height,0),
                timeformula
                ).autoretain()

                Glue((p[0],p[1],p[2]-distance-(i*distance)),
                (0,height,0),
                timeformula
                ).autoretain()

                Glue((p[0]-distance2-(i*distance2),p[1],p[2]-distance2-(i*distance2)),
                (0,height,0),
                timeformula
                ).autoretain()

                Glue((p[0]+distance2+(i*distance2),p[1],p[2]+distance2+(i*distance2)),
                (0,height,0),
                timeformula
                ).autoretain()

                Glue((p[0]+distance2+(i*distance2),p[1],p[2]-distance2-(i*distance)),
                (0,height,0),
                timeformula
                ).autoretain()

                Glue((p[0]-distance2-(i*distance2),p[1],p[2]+distance2+(i*distance2)),
                (0,height,0),
                timeformula
                ).autoretain()

                
        if self.bomb_type == 'glue_mine':
            from explodinary.actor.glue import Glue
            p = self.node.position
            v = self.node.velocity
            max_time =      (8.0 if buff else 7.0)
            glue_radius =   (2   if buff else 1  )
            distance =       0.9
            distance2 =      0.75
            height =         6
            time_increment = 0.75
            Glue((p[0],p[1],p[2]),
                    (0,height,0),
                    max_time).autoretain()
            for i in range(glue_radius):
                timeformula = (max_time-time_increment) + (time_increment*i)

                Glue((p[0]+distance+(i*distance),p[1],p[2]),
                (0,height,0),
                timeformula
                ).autoretain()
                
                Glue((p[0]-distance-(i*distance),p[1],p[2]),
                (0,height,0),
                timeformula
                ).autoretain()
            
            for i in range(glue_radius):
                timeformula = (max_time-time_increment) + (time_increment*i)

                Glue((p[0]+distance+(i*distance),p[1],p[2]),
                (0,height,0),
                timeformula
                ).autoretain()

                Glue((p[0]-distance-(i*distance),p[1],p[2]),
                (0,height,0),
                timeformula
                ).autoretain()

                Glue((p[0],p[1],p[2]+distance+(i*distance)),
                (0,height,0),
                timeformula
                ).autoretain()

                Glue((p[0],p[1],p[2]-distance-(i*distance)),
                (0,height,0),
                timeformula
                ).autoretain()

                Glue((p[0]-distance2-(i*distance2),p[1],p[2]-distance2-(i*distance2)),
                (0,height,0),
                timeformula
                ).autoretain()

                Glue((p[0]+distance2+(i*distance2),p[1],p[2]+distance2+(i*distance2)),
                (0,height,0),
                timeformula
                ).autoretain()

                Glue((p[0]+distance2+(i*distance2),p[1],p[2]-distance2-(i*distance)),
                (0,height,0),
                timeformula
                ).autoretain()

                Glue((p[0]-distance2-(i*distance2),p[1],p[2]+distance2+(i*distance2)),
                (0,height,0),
                timeformula
                ).autoretain()

        
        if self.bomb_type == 'cluster' and self.node.exists():
            from explodinary.actor.cluster import Cluster
            # Initial position:
            # Where did the bomb explode?
            def_pos = self.node.position
            # Radius of the square
            sr = (0.77 if buff else 0.69 if nerf else 0.87)
            # Our cluster positions
            cluster_pos = [(0,    0.15,  0),
                           (sr,   0.3,  sr),
                           (sr,   0.3,  -sr),
                           (-sr,  0.3,  sr),
                           (-sr,  0.3,  -sr)]
            if buff:
                cluster_pos.extend([
                    (sr*2,    0.45,   0),
                    (-sr*2,   0.45,   0),
                    (0,       0.45,    sr*2),
                    (0,       0.45,   -sr*2),
                ])
            altitude = 10

            for x in cluster_pos:
                dp = def_pos; cp = x
                position = [dp[0]+cp[0],
                            dp[1]+cp[1],
                            dp[2]+cp[2],
                            ]
                Cluster(position, (0,altitude,0), 7, self.get_source_player(ba.Player)).autoretain()

        # We blew up so we need to go away.
        # NOTE TO SELF: do we actually need this delay?
        ba.timer(0.001, ba.WeakCall(self.handlemessage, ba.DieMessage()))
                                    
    def _handle_launch(self) -> None:
        node = ba.getcollision().opposingnode
        if node.getnodetype() == 'spaz':
            node.handlemessage(ba.JumpyMessage())
        elif node.getnodetype() in ['bomb', 'prop']:
            xforce = 8
            yforce = 40
            for x in range(15):
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
        
        ba.playsound(BombFactory.get().jumppad_sound, 1.1, position=self.node.position)
        ba.emitfx(position=self.node.position,
          velocity=self.node.velocity,
          count=int(6.0 + random.random() * 12) if not ba.app.config.get("BSE: Reduced Particles", False) else 4,
          scale=0.8,
          spread=1,
          chunk_type='spark')
        ba.animate(self.node, 'model_scale', {0: 1.0, 0.2: 1.5, 0.4: 1.0,})
        ba.animate(self.jumppad_light,'intensity',{0: 0.75, 1: 0.0},loop=False)
        ba.animate(self.jumppad_light,'radius',{0: 0.2, 1: 0.0},loop=False)
    
    def _handle_sling(self) -> None:
        node = ba.getcollision().opposingnode
        if node.getnodetype() == 'spaz':
            node.handlemessage(ba.SlingMessage())
        elif node.getnodetype() in ['bomb', 'prop']:
            xforce = 70
            yforce = 50
            for x in range(5):
                v = node.velocity
                node.handlemessage('impulse', node.position[0], node.position[1], node.position[2],
                                   0, 25, 0,
                                   yforce, 0.05, 0, 0,
                                   0, 20*600, 0)
                
                node.handlemessage('impulse', node.position[0], node.position[1], node.position[2],
                                        0, 25, 0,
                                        xforce, 0.05, 0, 0,
                                        v[0]*15*2, 0, v[2]*15*2)
        else: return
        
        ba.playsound(BombFactory.get().slingshot_sound, 1.1, position=self.node.position)
        ba.emitfx(position=self.node.position,
          velocity=self.node.velocity,
          count=int(6.0 + random.random() * 12) if not ba.app.config.get("BSE: Reduced Particles", False) else 4,
          scale=1.2,
          spread=1,
          chunk_type='sweat')
        ba.animate(self.node, 'model_scale', {0: 1.5, 0.2: 0.5, 0.4: 1.0})
        ba.animate(self.slingshot_light,'intensity',{0: 0.75, 1: 0.0},loop=False)
        ba.animate(self.slingshot_light,'radius',{0: 0.2, 1: 0.0},loop=False)
    
                                    
    def animey(self):
        if not self.node:
            return
        if self.bomb_type == 'present':
            ba.animate(self.node, 'model_scale', {
            0: 1.0,
            1: 1.08,
            2: 1.16,
            3: 1.24,
            4: 1.32,
            5: 1.4,
            5.5: 1.44,
            5.7: 1.46,
            5.8: 0.8,
            5.9: 1.7,
        })
        
        if self.bomb_type == 'flying_glove':
            ba.animate(self.node, 'model_scale', {
            0: 0.8,
            2: 2
        })
        
        if self.bomb_type == 'steampunk':
            ba.animate(self.node, 'model_scale', {
            0.0: 1,
            0.2: 1.25,
            0.3: 1,
            0.4: 1.25,
            0.5: 1,
            0.6: 1.25,
            0.7: 1,
            0.8: 1.25,
            0.9: 1,
            1.0: 1.25,
            1.1: 1,
            1.2: 1.25,
            1.3: 1,
            1.4: 1.25,
            1.5: 1,
            1.6: 1.25,
            1.7: 1,
            1.8: 1.25,
            1.9: 1,
            2.0: 1.25,
            2.1: 1,
            2.2: 1.25,
            2.3: 1,
            2.4: 1.25,
            2.5: 1,
            2.6: 1.25,
            2.7: 1,
            2.8: 1.25,
            2.9: 1,
            3.0: 1.25,
            3.1: 1,
            3.2: 1.25,
            3.3: 1,
            3.4: 1.25,
            3.5: 1,
            3.6: 1.25,
            3.7: 1,
            3.8: 1,
            3.9: 0.8,
            4.0: 1.5,
        })
        
    def delete_node(self):
        self.node.delete
        
    # Various sound messages for bombs.
    def _handle_warn(self) -> None:
        if self.texture_sequence and self.node:
            self.texture_sequence.rate = 30
            ba.playsound(
                BombFactory.get().warn_sound, 0.5, position=self.node.position
            )

    def _handle_alarm(self):
        if self.node:
            ba.playsound(BombFactory.get().alarm_sound,
                         0.5,
                         position=self.node.position)
                         
    def _handle_engine(self):
        if self.node:
            sound = ba.newnode(
                    'sound',
                    owner=self.node,
                    attrs={'sound': BombFactory.get().engine_near_sound, 'volume': 0.75},
                )
            self.node.connectattr('position', sound, 'position')
                         
    def _add_material(self, material: ba.Material) -> None:
        if not self.node:
            return
        materials = self.node.materials
        if material not in materials:
            assert isinstance(materials, tuple)
            self.node.materials = materials + (material,)
    
    def present_gravity(self) -> None:
        if not self.node:
            return
        if self.bomb_type == 'present':
            self.node.gravity_scale = 15
            ba.timer(
                5, ba.WeakCall(self.handlemessage, ExplodeMessage())
            )
        self.present_light = ba.newnode('light',
                          owner=self.node,
                          attrs={'position':self.node.position,
                                  'radius':0.4,
                                  'intensity':0.5,
                                  'color': (1, 0, 0),
                                  'volume_intensity_scale': 1.0}) 
        self.node.connectattr('position',self.present_light,'position')
    
    def ready(self) -> None:
        if not self.node:
            return
        factory = BombFactory.get()
        intex: Sequence[ba.Texture]
        if self.bomb_type == 'vital':
            intex = (factory.vital_lit_tex, factory.vital_tex)
            self.texture_sequence = ba.newnode('texture_sequence',
                                               owner=self.node,
                                               attrs={
                                                   'rate': 20,
                                                   'input_textures': intex
                                               })
            ba.playsound(factory.vitready_sound, 0.4, position=self.node.position)
            ba.timer(3, self.texture_sequence.delete)
            
    def arm(self) -> None:
        """Arm the bomb (for land-mines and impact-bombs).

        These types of bombs will not explode until they have been armed.
        """
        if not self.node:
            return
        factory = BombFactory.get()
        intex: Sequence[ba.Texture]
        if self.bomb_type == 'land_mine':
            intex = (factory.land_mine_lit_tex, factory.land_mine_tex)
            self.texture_sequence = ba.newnode(
                'texture_sequence',
                owner=self.node,
                attrs={'rate': 30, 'input_textures': intex},
            )
            ba.timer(0.5, self.texture_sequence.delete)

            # We now make it explodable.
            ba.timer(
                0.25,
                ba.WeakCall(
                    self._add_material, factory.land_mine_blast_material
                ),
            ba.playsound(factory.activate_sound, 0.5, position=self.node.position)
            )
        elif self.bomb_type == 'lite_mine':
            intex = (factory.lite_mine_lit_tex, factory.lite_mine_tex)
            self.texture_sequence = ba.newnode('texture_sequence',
                                               owner=self.node,
                                               attrs={
                                                   'rate': 30,
                                                   'input_textures': intex
                                               })
            ba.timer(0.5, self.texture_sequence.delete)
            ba.playsound(factory.activate_sound, 0.5, position=self.node.position)
            # We now make it explodable.
            ba.timer(
                0.15,
                ba.WeakCall(self._add_material,
                            factory.land_mine_blast_material))
        elif self.bomb_type == 'flutter_mine':
            intex = (factory.flutter_mine_lit_tex, factory.flutter_mine_tex)
            self.texture_sequence = ba.newnode('texture_sequence',
                                               owner=self.node,
                                               attrs={
                                                   'rate': 30,
                                                   'input_textures': intex
                                               })
            ba.timer(0.5, self.texture_sequence.delete)
            ba.playsound(factory.activate_sound, 0.5, position=self.node.position)
            # We now make it explodable.
            ba.timer(
                0.15,
                ba.WeakCall(self._add_material,
                            factory.land_mine_blast_material))
        elif self.bomb_type == 'glue_mine':
            intex = (factory.glue_mine_lit_tex, factory.glue_mine_tex)
            self.texture_sequence = ba.newnode('texture_sequence',
                                               owner=self.node,
                                               attrs={
                                                   'rate': 30,
                                                   'input_textures': intex
                                               })
            ba.timer(0.5, self.texture_sequence.delete)
            ba.playsound(factory.activate_sound, 0.5, position=self.node.position)
            # We now make it explodable.
            ba.timer(
                0.15,
                ba.WeakCall(self._add_material,
                            factory.land_mine_blast_material))
        elif self.bomb_type == 'present':
            intex = (factory.present_bomb_tex, factory.present_bomb_tex2, factory.present_bomb_tex3, factory.present_bomb_texEx)
            self.texture_sequence = ba.newnode('texture_sequence',
                                               owner=self.node,
                                               attrs={
                                                   'rate': 1800,
                                                   'input_textures': intex
                                               })
            ba.timer(6, self.texture_sequence.delete)
            ba.playsound(factory.confetti_sound, 0.75, position=self.node.position)
            if self.node.exists():
                cv = ([v * 0.6 for v in self.node.velocity])
                bseVFX('confetti',
                       self.node.position,
                       cv)
                ba.emitfx(position=self.node.position,
                          velocity=self.node.velocity,
                          count=12 if not ba.app.config.get("BSE: Reduced Particles", False) else 4,
                          scale=0.6,
                          spread=1.5,
                          chunk_type='spark')
                self._add_material(factory.no_pick_material)
        elif self.bomb_type == 'vital':
            intex = (factory.vital_lit_tex, factory.vital_tex)
            self.texture_sequence = ba.newnode('texture_sequence',
                                               owner=self.node,
                                               attrs={
                                                   'rate': 400,
                                                   'input_textures': intex
                                               })
            ba.playsound(factory.vitaken_sound, 0.4, position=self.node.position)
            ba.timer(2.5, self.texture_sequence.delete)
        elif self.bomb_type == 'impact':
            intex = (
                factory.impact_lit_tex,
                factory.impact_tex,
                factory.impact_tex,
            )
            self.texture_sequence = ba.newnode(
                'texture_sequence',
                owner=self.node,
                attrs={'rate': 100, 'input_textures': intex},
            )
            ba.timer(
                0.25,
                ba.WeakCall(
                    self._add_material, factory.land_mine_blast_material
                ),
            ba.playsound(factory.activate_sound, 0.5, position=self.node.position)
            )
        elif self.bomb_type == 'flying_glove':
            ba.timer(
                0.25,
                ba.WeakCall(
                    self._add_material, factory.land_mine_blast_material
                ),
            ba.playsound(factory.activate_sound, 0.5, position=self.node.position)
            )
        else:
            raise Exception('arm() should only be called '
                            'on land-mines, sky-mines, presents or impact bombs')
        self.texture_sequence.connectattr(
            'output_texture', self.node, 'color_texture'
        )

    
    def presentSparks(self):
        if self.bomb_type == 'present':
                        ba.emitfx(position=self.node.position,
                          velocity=self.node.velocity,
                          count=int(6.0 + random.random() * 12) if not ba.app.config.get("BSE: Reduced Particles", False) else 3,
                          scale=0.8,
                          spread=1.5,
                          chunk_type='spark')
        # This code scares me
        # if node: ba.timer(4, lambda: presentSparks(self.node))

    def _handle_hit(self, msg: ba.HitMessage) -> None:
        ispunched = msg.srcnode and msg.srcnode.getnodetype() == 'spaz'
        indair = msg.hit_subtype == 'cloudy'
        flutter = msg.hit_subtype == 'flutter'
        vital = msg.hit_subtype == 'vital'        
        
        # We don't want to chain-explode presents nor send knockback to jump pads
        if self.bomb_type in ['present', 'jump_pad']: return
        
        # Normal bombs are triggered by non-punch impacts;
        # impact-bombs by all impacts.
        if not self._exploded and (
            not ispunched or self.bomb_type in ['impact', 'land_mine', 'lite_mine', 'flutter_mine', 'glue_mine', 'flying_glove']
        ) and not indair and not flutter and not vital:

            # Also lets change the owner of the bomb to whoever is setting
            # us off. (this way points for big chain reactions go to the
            # person causing them).
            source_player = msg.get_source_player(ba.Player)
            if source_player is not None:
                self._source_player = source_player

            ba.timer(
                0.1 + random.random() * 0.1,
                ba.WeakCall(self.handlemessage, ExplodeMessage()),
            )
            
        if msg.hit_subtype in 'clouder':
            msg.hit_subtype == 'cloudy'
        if msg.hit_subtype in 'vital':
            msg.hit_subtype == 'vital'
        if msg.hit_subtype in 'flutter_mine':
            msg.hit_subtype == 'flutter'
        if msg.hit_subtype in ['toxic', 'tnt_toxic']:
            msg.hit_subtype == 'toxic'
        if msg.hit_subtype in ['ice', 'tnt_ice']:
            msg.hit_subtype == 'ice'
        
        assert self.node
        
        st = self.hit_subtype
        buff, nerf = [self._vital_buff_state > 0, self._vital_buff_state < 0]
        mult = 3 if st=='cloudy' else 6 if st=='flutter' else 10 if st in ['cloudy','flutter'] and buff else 1

        self.node.handlemessage(
            'impulse',
            msg.pos[0],
            msg.pos[1],
            msg.pos[2],
            msg.velocity[0],
            msg.velocity[1],
            msg.velocity[2],
            msg.magnitude,
            msg.velocity_magnitude,
            msg.radius,
            0,
            msg.velocity[0] * mult,
            msg.velocity[1] * mult,
            msg.velocity[2] * mult,
        )
    
        if msg.srcnode:
            pass
                
    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ExplodeMessage):
            self.explode()
        elif isinstance(msg, ImpactMessage):
            self._handle_impact()
        elif isinstance(msg, SplatMessage):
            self._handle_splat()
        elif isinstance(msg, DripMessage):
            self._handle_drip()
        elif isinstance(msg, ba.DroppedMessage):
            self._handle_dropped()
        elif isinstance(msg, ba.HitMessage):
            self._handle_hit(msg)
        elif isinstance(msg, ba.DieMessage):
            self._handle_die()
        elif isinstance(msg, ba.OutOfBoundsMessage):
            self._handle_oob()
        elif isinstance(msg, ArmMessage):
            self.arm()
        elif isinstance(msg, PresentMessage):
            self.present_gravity()
        elif isinstance(msg, JumpPadMessage):
            self._handle_launch()
        elif isinstance(msg, slingshotMessage):
            self._handle_sling()
        elif isinstance(msg, WarnMessage):
            self._handle_warn()
        elif isinstance(msg, AlarmMessage):
            self._handle_alarm()
        elif isinstance(msg, AnimeyMessage):
            self.animey()
        elif isinstance(msg, ReadyMessage):
            self.ready()
        elif isinstance(msg, EngineMessage):
            self._handle_engine()
        elif isinstance(msg, DeleteNodeMessage):
            self.delete_node()
        # Reduce blastsies!
        elif isinstance(msg, ba.VitalMessage):
            # Get the source player of the blast
            assert self._source_player is not None
            sourceplayer, myplayer = msg.get_source_player(ba.Player), self._source_player
            # Attempts to check if the blast source player's team is the same as our bomb's
            try: myteam = sourceplayer.team == myplayer.team
            except AttributeError: myteam = False
            # Blacklist for TNTs
            # (They have no teams by default, resulting in a debuff... we don't want that.)
            # (Instead, we force these to get buffed every single time.)
            blacklist = ['tnt','tnt_ice','tnt_toxic','tnt_glue']
            # Buff: Statement to mark if we should get nerfed or buffed
            buff = myteam or self.bomb_type in blacklist
            vbs = self._vital_buff_state
            if buff and not vbs > 0:
                self._vitalized_bomb(True, vbs)
            elif not buff and not vbs < 0:
                self._vitalized_bomb(False, vbs)
        else:
            super().handlemessage(msg)

class TNTSpawner:
    """Regenerates TNT at a given point in space every now and then.

    category: Gameplay Classes
    """

    def __init__(self, position: Sequence[float], respawn_time: float = 20):
        """Instantiate with given position and respawn_time (in seconds)."""
        from ba._coopsession import CoopSession
        self._position = position
        self._tnt: Bomb | None = None
        self._respawn_time = respawn_time
        self._wait_time = 0.0

        # We set the order from here
        if isinstance(ba.getsession(), CoopSession) or ba.app.config.get("BSE: TNT Variants", True):
            self._tnt_list = ['tnt',
                              'tnt_ice',
                              'tnt_toxic',
                              'tnt_glue']
        else:
            self._tnt_list = ['tnt']
            
        self._tnt_latest: int = 0 # Number that tells us the last tnt dropped from that list

        self._update()
        
        # Go with slightly more than 1 second to avoid timer stacking.
        self._update_timer = ba.Timer(
            1.1, ba.WeakCall(self._update), repeat=True
        )

    def _update(self) -> None:
        tnt_alive = self._tnt is not None and self._tnt.node
        if not tnt_alive:
            # Respawn if its been long enough.. otherwise just increment our
            # how-long-since-we-died value.

            # We use our _tnt_latest value to select our next tnt type
            selected_tnt = self._tnt_list[self._tnt_latest]

            if self._tnt is None or self._wait_time >= self._respawn_time:
                self._tnt = Bomb(position=self._position, bomb_type=selected_tnt)
                
                #ba.screenmessage(f'Dropped: {str(se)}, {str(self._tnt_latest)}') # Debug stuff: Sends the last tnt type & list int dropped

                # Once we drop our TNT, add 1 to our _tnt_latest and make sure it wraps around our list
                self._tnt_latest = (self._tnt_latest + 1) % len(self._tnt_list)

                self._wait_time = 0.0
            else:
                self._wait_time += 1.1

class ClassicTNTSpawner:
    """TNT respawn.

    category: Gameplay Classes
    """

    def __init__(self, position: Sequence[float], respawn_time: float = 20.0):
        """Instantiate with given position and respawn_time (in seconds)."""
        self._position = position
        self._tnt: Bomb | None = None
        self._respawn_time = 20
        self._wait_time = 0.0
        self._update()

        # Go with slightly more than 1 second to avoid timer stacking.
        self._update_timer = ba.Timer(
            1.1, ba.WeakCall(self._update), repeat=True
        )

    def _update(self) -> None:
        tnt_alive = self._tnt is not None and self._tnt.node
        if not tnt_alive:
            # Respawn if its been long enough.. otherwise just increment our
            # how-long-since-we-died value.
            if self._tnt is None or self._wait_time >= self._respawn_time:
                self._tnt = Bomb(position=self._position, bomb_type='tnt')
                self._wait_time = 0.0
            else:
                self._wait_time += 1.1
                
class JumpPadSpawner:
    """Regenerates a Jump-Pad at a given point in space every now and then.

    category: Gameplay Classes
    """

    def __init__(self, position: Sequence[float], respawn_time: float = 0.01):
        """Instantiate with given position and respawn_time (in seconds)."""
        self._position = position
        self._jump: Bomb | None = None
        self._respawn_time = 0.01
        self._wait_time = 0.0

        # We set the order from here
        self._jump_list = ['jump_pad',
                         ]
        self._jump_latest: int = 0 # Number that tells us the last jump dropped from that list

        self._update()
        
        # Go with slightly more than 1 second to avoid timer stacking.
        self._update_timer = ba.Timer(
            1.1, ba.WeakCall(self._update), repeat=True
        )

    def _update(self) -> None:
        jump_alive = self._jump is not None and self._jump.node
        if not jump_alive:
            # Respawn if its been long enough.. otherwise just increment our
            # how-long-since-we-died value.

            # We use our _jump_latest value to select our next jump type
            selected_jump = self._jump_list[self._jump_latest]

            if self._jump is None or self._wait_time >= self._respawn_time:
                self._jump = Bomb(position=self._position, bomb_type=selected_jump)
                
                #ba.screenmessage(f'Dropped: {str(se)}, {str(self._jump_latest)}') # Debug stuff: Sends the last jump type & list int dropped

                # Once we drop our jump, add 1 to our _jump_latest and make sure it wraps around our list
                self._jump_latest = (self._jump_latest + 1) % len(self._jump_list)

                self._wait_time = 0.0
            else:
                self._wait_time += 1.1

class SlingshotSpawner:
    """Regenerates a Slingshot at a given point in space every now and then.

    category: Gameplay Classes
    """

    def __init__(self, position: Sequence[float], respawn_time: float = 0.01):
        """Instantiate with given position and respawn_time (in seconds)."""
        self._position = position
        self._slingshot: Bomb | None = None
        self._respawn_time = 0.01
        self._wait_time = 0.0

        # We set the order from here
        self._slingshot_list = ['slingshot',
                         ]
        self._slingshot_latest: int = 0 # Number that tells us the last jump dropped from that list

        self._update()
        
        # Go with slightly more than 1 second to avoid timer stacking.
        self._update_timer = ba.Timer(
            1.1, ba.WeakCall(self._update), repeat=True
        )

    def _update(self) -> None:
        slingshot_alive = self._slingshot is not None and self._slingshot.node
        if not slingshot_alive:

            selected_slingshot = self._slingshot_list[self._slingshot_latest]

            if self._slingshot is None or self._wait_time >= self._respawn_time:
                self._slingshot = Bomb(position=self._position, bomb_type=selected_slingshot)

                self._slingshot_latest = (self._slingshot_latest + 1) % len(self._slingshot_list)

                self._wait_time = 0.0
            else:
                self._wait_time += 1.1