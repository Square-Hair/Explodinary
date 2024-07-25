from __future__ import annotations

from typing import TYPE_CHECKING

import ba
from bastd.gameutils import SharedObjects
from bastd.actor.bomb import Bomb, Blast


if TYPE_CHECKING:
    from typing import Any, Callable

class ClusterFactory(object):
    
    impacto_material: ba.Material
    blast_material: ba.Material
    bomb_material: ba.Material
    
    def __init__(self):
        
        shared = SharedObjects.get()
        
        self.cluster_model = ba.getmodel('littleCluster')
        self.cluster_tex = ba.gettexture('clusterBombColor')
        
        self.impacto_material = ba.Material()
        self.impacto_material.add_actions(
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
        
        self.blast_material = ba.Material()
        self.blast_material.add_actions(
            conditions=('they_have_material', shared.object_material),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('message', 'our_node', 'at_connect', ExplodeHitMessage()),
            ),
        )
        
        self.bomb_material = ba.Material()
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
        self.bomb_material.add_actions(
            conditions=('they_have_material', shared.pickup_material),
            actions=('modify_part_collision', 'use_node_collide', False),
        )

        self.bomb_material.add_actions(
            actions=('modify_part_collision', 'friction', 0.3)
        )
        
    def on_begin(self):
        ba.gameactivity.on_begin(self) 

class DieMessage(object):
    pass     

class OutOfBoundsMessage(object):
    pass

class AnimeyMessage:
    """Animates.""" 

class ImpactMessage:
    """Touches."""      

class ExplodeMessage:
    """Explodes."""    

class ExplodeHitMessage:
    """Hits when explodes."""     

class Cluster(ba.Actor):
    
    def __init__(self, position=(0,0,0), velocity=(0,0,0), decay_time=7, source_player: ba.Player | None = None,):
        '''
        Instantiate with given values.
        '''
        
        ba.Actor.__init__(self)

        factory = ClusterFactory()
        shared = SharedObjects.get()
        materials = (factory.impacto_material, factory.bomb_material, shared.object_material,)
        
        self._last_sticky_sound_time = 0
        
        self._exploded = False
        self.blast_radius = 1
        self.blast_type = 'little_cluster'
        self.bomb_type = 'little_cluster'
        self.hit_subtype = 'little_cluster'
        self._source_player = source_player
        self._explode_callbacks: list[Callable[[Bomb, Blast], Any]] = []
    
        self.node = ba.newnode(
            'prop',
            delegate=self,
            attrs={
                'position': position,
                'velocity': velocity,
                'model': factory.cluster_model,
                'light_model': factory.cluster_model,
                'body': 'sphere',
                'body_scale': 1.5,
                'model_scale': 1.1,
                'density': 0.5,
                'shadow_size': 0.2,
                'color_texture': factory.cluster_tex,
                'reflection': 'powerup',
                'reflection_scale': [0.8],
                'materials': materials,
            },
        )
        self.animey_timer = ba.Timer(0.0, ba.WeakCall(self.handlemessage, AnimeyMessage()))

    def _handle_die(self) -> None:
        if self.node:
            self.node.delete()
    
    def _handle_impact(self) -> None:
        node = ba.getcollision().opposingnode
        self.handlemessage(ExplodeMessage())
    
    def _handle_animey(self):
        if not self.node: return
        ba.animate(self.node, 'model_scale', {
        0: 0,
        0.2: 1.1,
    })
    
    def explode(self) -> None:
        """Blows up the bomb if it has not yet done so."""
        from bastd.actor.bomb import Blast
        if self._exploded:
            return
        self._exploded = True
        if self.node:
            blast = Blast(
                position=self.node.position,
                velocity=self.node.velocity,
                blast_radius=self.blast_radius,
                blast_type=self.bomb_type,
                hit_subtype=self.hit_subtype,
                source_player=ba.existing(self._source_player),
            ).autoretain()
            for callback in self._explode_callbacks:
                callback(self, blast)
        
        ba.timer(0.001, ba.WeakCall(self.handlemessage, ba.DieMessage()))
            
    def _handle_oob(self) -> None:
        self.handlemessage(ba.DieMessage())
 
    def handlemessage(self, msg: Any) -> Any:
        assert not self.expired

        if isinstance(msg, ba.DieMessage):
            self._handle_die()
        elif isinstance(msg, ba.OutOfBoundsMessage):
            self._handle_oob()
        elif isinstance(msg, ImpactMessage):
            self._handle_impact()
        elif isinstance(msg, ExplodeMessage):
            self.explode()
        elif isinstance(msg, AnimeyMessage):
            self._handle_animey()
        
        elif isinstance(msg, ExplodeHitMessage):
            node = ba.getcollision().opposingnode
            assert self.node
            nodepos = self.node.position
            mag = 2000.0
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
            
        elif isinstance(msg, ba.HitMessage):
            if msg.hit_subtype in ['cloudy','flutter']:
                multiplier: float = 20
                self.node.handlemessage(
                    'impulse',
                    msg.pos[0],
                    msg.pos[1] + 0.1,
                    msg.pos[2],
                    0,
                    0,
                    0,
                    msg.magnitude * 2,
                    msg.velocity_magnitude,
                    msg.radius * multiplier,
                    0,
                    msg.force_direction[0] * multiplier,
                    msg.force_direction[1] * multiplier,
                    msg.force_direction[2] * multiplier,
                )
            if msg.hit_subtype == 'vital':
                self._handle_die()
        
        else:
            super().handlemessage(msg)
                