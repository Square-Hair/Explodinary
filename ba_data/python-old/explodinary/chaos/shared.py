import ba
from bastd.actor.spaz import Spaz
from bastd.actor.spazappearance import Appearance
import random

def transform_spaz_appearance(spaz: Spaz, transmute: Appearance):
    ''' Transforms our lovely Spaz entity! '''
    spaz.node.attack_sounds         = [ba.getsound(s) for s in transmute.attack_sounds]
    spaz.node.jump_sounds           = [ba.getsound(s) for s in transmute.jump_sounds]
    spaz.node.impact_sounds         = [ba.getsound(s) for s in transmute.impact_sounds]
    spaz.node.pickup_sounds         = [ba.getsound(s) for s in transmute.pickup_sounds]
    spaz.node.death_sounds          = [ba.getsound(s) for s in transmute.death_sounds]
    spaz.node.fall_sounds           = [ba.getsound(s) for s in transmute.fall_sounds]
    
    spaz.node.color_texture         = ba.gettexture(transmute.color_texture)
    spaz.node.color_mask_texture    = ba.gettexture(transmute.color_mask_texture)
    
    spaz.node.head_model            = ba.getmodel(transmute.head_model)
    spaz.node.torso_model           = ba.getmodel(transmute.torso_model)
    spaz.node.pelvis_model          = ba.getmodel(transmute.pelvis_model)
    spaz.node.upper_arm_model       = ba.getmodel(transmute.upper_arm_model)
    spaz.node.forearm_model         = ba.getmodel(transmute.forearm_model)
    spaz.node.hand_model            = ba.getmodel(transmute.hand_model)
    spaz.node.upper_leg_model       = ba.getmodel(transmute.upper_leg_model)
    spaz.node.lower_leg_model       = ba.getmodel(transmute.lower_leg_model)
    spaz.node.toes_model            = ba.getmodel(transmute.toes_model)
    
    if spaz.node.style != 'female' and transmute.style != 'female': # Female style's hair is a buggy mess
        spaz.node.style             = transmute.style
        
def distribute(duration: float,
               segments: int) -> list:
    ''' Distributes the duration of the effect into a list, segmenting the length into smaller numbers. '''
    fractions = [random.uniform(0, 1) for _ in range(segments)]
    csum = sum(fractions)
    
    return [frac * (duration / csum) for frac in fractions]