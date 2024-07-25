from explodinary.chaos import ChaosEvent, append_chaos_event
from bastd.game.easteregghunt import EasterEggHuntGame
import ba

class MyChaosEvent(ChaosEvent):
    ''' Baseplate class for Chaos events. '''
    name = 'Chaos Event Name'       # Event's name
    icon = 'empty'                  # Event's texture icon
    event_type = 'normal'           # Event Category ("normal" or "manager" [or "force" for testing]), ignore / remove if not needed
    
    # Event will be dismissed if current activity / session matches an element in the list.
    # (You might want to do some importing beforehand for this.)
    blacklist = [
        #ba.FreeForAllSession   # This would prevent the event from running in Free for All sessions
        #EasterEggHuntGame      # This one would prevent it from running while playing Easter Egg Hunt
        ]
    
    def event(self):
        ''' The event itself. '''
        ba.screenmessage('Chaos Event goes here!')
        # You can add pretty much anything here! Go wild! Do whatever you please!
        # Remember to use support functions such as self._get_players() to code events quicker,
        # write "return (time)" to let the manager know how long your event is gonna last, and
        # use "return False" in case your event didn't go as expected so the manager can reroll it
        
if False: # Switching this to "True" would allow the event above to register as an event. As simple as that.
    append_chaos_event(MyChaosEvent)
    
import random

from typing import Any

from bastd.actor.spaz import Spaz
from bastd.actor.bomb import Blast
class TempExampleEvent(ChaosEvent):
    ''' - Sudden Egg Hunt -
        1. Turn everyone into bunnies
        2. Spawn explosive eggs around the map '''
        
    name = 'Sudden Egg Hunt'
    icon = 'bunnyIcon'
    
    blacklist = [
        ba.CoopSession # Prevent this event in Co-op
    ]
    
    def event(self):
        ''' Run our event routine. '''
        # Create our egg material
        self.eggmat = ba.Material()
        self.eggmat.add_actions(
            conditions=('they_have_material', SharedObjects.get().player_material),
            actions=(('call', 'at_connect', self._egg_pickup),),
        )
        
        # Get this map's bounding box
        self.worldbounds = self.activity.map.get_def_bound_box('map_bounds')
        
        # Pick all spaz entities in-game, including bots
        for entity in self._get_everyone():
            self.bunnify(entity)
        
        # Summon randomly between 15 and 40 eggs
        egg_a = random.randint(15, 40)
        for n in range(egg_a):
            pos = (
                random.uniform(self.worldbounds[0], self.worldbounds[3],) * 0.76,
                random.uniform(self.worldbounds[4], self.worldbounds[4],) - 0.5,
                random.uniform(self.worldbounds[2], self.worldbounds[5],) * 0.76,
            )
            # Give the egg a random lifespan depending on the timer's duration
            lifespan = (self._get_config()['time'] * 4) * random.uniform(0.6, 1.2)
            MyEgg(pos, self.eggmat, lifespan).autoretain()

    def _egg_pickup(self) -> None:
        ''' Make our egg explode when picked up by a live player. '''
        collision = ba.getcollision()

        # Prevent this from running if picked up by a non-spaz entity
        try:
            egg = collision.sourcenode.getdelegate(MyEgg, True)
            spaz: Spaz = collision.opposingnode.getdelegate(
                Spaz, True)
        except ba.NotFoundError:
            return
        
        # Summon an explosion in the egg's position and delete it afterwards
        Blast(egg.node.position, (0,0,0), 2.5, 'normal', spaz.source_player)
        egg.handlemessage(ba.DieMessage())
        
    def bunnify(self,
                spaz: Spaz):
        ''' Transforms this spaz into a bunny. '''
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

from bastd.gameutils import SharedObjects
class MyEgg(ba.Actor):
    ''' Custom Egg Entity for our Sudden Egg Hunt event. '''
    def __init__(self,
                 position: tuple,
                 eggmat: ba.Material,
                 lifespan: float):
        super().__init__()
        shared = SharedObjects.get()

        texpool = [ # Texture pool
            ba.gettexture('bombColor'),
            ba.gettexture('bombColorIce'),
            ba.gettexture('bombStickyColor'),
        ]
        # Spawn just above the provided point
        self._spawn_pos = (position[0], position[1] + 0.5, position[2])
        # Choose a texture randomly
        ctex = random.choice(texpool)
        # Assign an object material + the provided egg material from the event
        mats = [shared.object_material, eggmat]
        
        # Build the node itself
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
        
        # Do some cool fade out animation in case our egg despawns due to it's lifespan
        ba.animate(self.node, 'model_scale', {
            0:self.node.model_scale,
            lifespan*0.95:self.node.model_scale,
            lifespan:0,
        })
        # Delete egg after lifespan has passed
        ba.timer(lifespan, ba.Call(self.handlemessage, ba.DieMessage()))

    def exists(self) -> bool: # Function to return that in fact this node exists
        return bool(self.node)

    def handlemessage(self, msg: Any) -> Any: # Handling
        # Delete when dying
        if isinstance(msg, ba.DieMessage):
            if self.node:
                self.node.delete()
        # When hit, transfer hit force to it's node
        elif isinstance(msg, ba.HitMessage):
            if self.node:
                assert msg.force_direction is not None
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

if False: # Switch to True to enable this event.
    append_chaos_event(TempExampleEvent)