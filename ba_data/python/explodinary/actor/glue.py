from __future__ import annotations

import ba
from bastd.gameutils import SharedObjects

from typing import Any

class GlueFactory(object):

    def __init__(self):
        
        shared = SharedObjects.get()
        
        self.glue_sound = ba.getsound('glueImpact1')
        self.glue_sound2 = ba.getsound('glueImpact2')
        self.glue_floor_sound = ba.getsound('glueImpactFloor')
        
        self.glue_model = ba.getmodel('glueModel')
        self.glue_tex = ba.gettexture('glueColor')

        
        self.glue_material = ba.Material()
        self.glue_material.add_actions(
            actions=(('modify_part_collision','stiffness',1),
                     ('modify_part_collision','damping',1.0)))
        self.glue_material.add_actions(
            conditions=(
                ('they_have_material', shared.player_material),
                'or',
                ('they_have_material', shared.footing_material),
            ),
            actions=('message', 'our_node', 'at_connect', SplatMessage()),
        )
        
    def on_begin(self):
        ba.gameactivity.on_begin(self) 

class SplatMessage(object):
    pass  

class DieMessage(object):
    pass     

class OutOfBoundsMessage(object):
    pass

class Glue(ba.Actor):
    
    def __init__(self,
                 position=(0,0,0),
                 velocity=(0,0,0),
                 decay_time=7):
        '''
        Instantiate with given values.
        '''
        
        ba.Actor.__init__(self)

        factory = GlueFactory()
        shared = SharedObjects.get()
        materials = (factory.glue_material, shared.object_material)
        
        self._last_sticky_sound_time = 0
        
        self.state = None
        self.is_sticky = True

        self._reglue_timer: ba.Timer | None = None
    
        self.node = ba.newnode(
            'prop',
            delegate=self,
            attrs={
                'position': position,
                'velocity': velocity,
                'model': factory.glue_model,
                'light_model': factory.glue_model,
                'body': 'sphere',
                'body_scale': 1,
                'model_scale': 0.8,
                'density': 2,
                'shadow_size': 0.2,
                'sticky': True,
                'color_texture': factory.glue_tex,
                'reflection': 'soft',
                'reflection_scale': [0.0],
                'materials': materials,
            },
        )
        self._animate('in')
        ba.timer(decay_time, ba.WeakCall(self.handlemessage, ba.DieMessage()))
    
    def _animate(self, tr = 'in') -> None:
        if not self.node: return
        if tr == 'in':
            ba.animate(self.node, 'model_scale', {
            0.0: 0.0,
            0.5: 0.9,
            0.8: 0.8,
            })
        elif tr == 'out':
            ba.animate(self.node, 'model_scale', {
            0.0: 0.8,
            0.3: 0.7,
            0.5: 0,
            })
        
    def _handle_die(self, instant: bool = False) -> None:
        if self.node:
            if not instant:
                self._animate('out')
                ba.timer(0.5, self.node.delete)
            else:
                self.node.delete()
            
    def _handle_oob(self) -> None:
        self._handle_die(True)
    
    def _handle_splat(self) -> None:
        node = ba.getcollision().opposingnode
        factory = GlueFactory()
        sounds = (factory.glue_sound, factory.glue_sound2)
        #if node.getnodetype() == 'spaz':
        #    ba.playsound(random.choice(sounds), 0.3, position=self.node.position)
        #else:
        #ba.playsound(factory.glue_floor_sound, 1.5, position=self.node.position)
    
    def _stick_toggle(self, toggle: bool | None = None):
        if not self.node: return

        factory = GlueFactory()
        shared = SharedObjects.get()
        if toggle is None:
            toggle = not self.is_sticky

        mats = [shared.object_material]
        if toggle: mats.append(factory.glue_material)

        self.node.materials = mats
        self.is_sticky = toggle

    def handlemessage(self, msg: Any) -> Any:
        assert not self.expired

        if isinstance(msg, ba.DieMessage):
            self._handle_die()
        elif isinstance(msg, ba.OutOfBoundsMessage):
            self._handle_oob()
        elif isinstance(msg, SplatMessage):
            self._handle_splat()
        elif isinstance(msg, ba.HitMessage):
            flutter = msg.hit_subtype in ['cloudy','flutter']
            if msg.hit_subtype == 'tnt_glue': return

            multiplier: float =  2.34 if flutter else 0.3
            unsticktime: float = 0.77 if flutter else 0.25

            # Unstick for a hot second
            self._stick_toggle(False)
            self._reglue_timer = ba.Timer(unsticktime, lambda: self._stick_toggle(True))

            self.node.handlemessage(
                'impulse',
                msg.pos[0],
                msg.pos[1] - 0.15,
                msg.pos[2],
                0,
                0,
                0,
                msg.magnitude * 2.5,
                msg.velocity_magnitude,
                msg.radius * multiplier,
                0,
                msg.force_direction[0]      * multiplier * 1.5,
                abs(msg.force_direction[1]) * multiplier,
                msg.force_direction[2]      * multiplier * 1.5,
            )
            if msg.hit_subtype == 'vital':
                self._handle_die()
        
        else:
            super().handlemessage(msg)