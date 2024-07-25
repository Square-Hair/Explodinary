# Released under the MIT License. See LICENSE for details.
#
"""Appearance functionality for spazzes."""
from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import ba.internal

if TYPE_CHECKING:
    pass


def get_appearances(include_locked: bool = False) -> list[str]:
    """Get the list of available spaz appearances."""
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-branches
    get_purchased = ba.internal.get_purchased
    disallowed = []
    if not include_locked:
        # hmm yeah this'll be tough to hack...
        if not get_purchased('characters.santa'):
            disallowed.append('Santa Claus')
        if not get_purchased('characters.frosty'):
            disallowed.append('Frosty')
        if not get_purchased('characters.bones'):
            disallowed.append('Bones')
            disallowed.append('Bosbone')
        if not get_purchased('characters.bernard'):
            disallowed.append('Bernard')
        if not get_purchased('characters.pixie'):
            disallowed.append('Pixel')
        if not get_purchased('characters.pascal'):
            disallowed.append('Pascal')
        if not get_purchased('characters.actionhero'):
            disallowed.append('Todd McBurton')
        if not get_purchased('characters.taobaomascot'):
            disallowed.append('Taobao Mascot')
        if not get_purchased('characters.agent'):
            disallowed.append('Agent Johnson')
        if not get_purchased('characters.jumpsuit'):
            disallowed.append('Lee')
        if not get_purchased('characters.assassin'):
            disallowed.append('Zola')
        if not get_purchased('characters.wizard'):
            disallowed.append('Grumbledorf')
        if not get_purchased('characters.cowboy'):
            disallowed.append('Butch')
        if not get_purchased('characters.witch'):
            disallowed.append('Witch')
        if not get_purchased('characters.warrior'):
            disallowed.append('Warrior')
        if not get_purchased('characters.superhero'):
            disallowed.append('Middle-Man')
        if not get_purchased('characters.alien'):
            disallowed.append('Alien')
        if not get_purchased('characters.oldlady'):
            disallowed.append('OldLady')
        if not get_purchased('characters.gladiator'):
            disallowed.append('Gladiator')
        if not get_purchased('characters.wrestler'):
            disallowed.append('Wrestler')
        if not get_purchased('characters.operasinger'):
            disallowed.append('Gretel')
        if not get_purchased('characters.robot'):
            disallowed.append('Robot')
        if not get_purchased('characters.cyborg'):
            disallowed.append('B-9000')
        if not get_purchased('characters.bunny'):
            disallowed.append('Easter Bunny')
        if not get_purchased('characters.kronk'):
            disallowed.append('Kronk')
        if not get_purchased('characters.zoe'):
            disallowed.append('Zoe')
        if not get_purchased('characters.jackmorgan'):
            disallowed.append('Jack Morgan')
        if not get_purchased('characters.mel'):
            disallowed.append('Mel')
        if not get_purchased('characters.snakeshadow'):
            disallowed.append('Snake Shadow')
        if not ba.app.config.get("BSE: Oversilly Oversillier", False):
            disallowed.append('Oversilly')
        if not ba.app.config.get("BSE: Adios Amigo", False):
            disallowed.append('Amigo')
        if not get_purchased('characters.helpy_bse'):
            disallowed.append('Helpy')
        if not get_purchased('characters.amigo_bse'):
            disallowed.append('Spencer')
    return [
        s for s in list(ba.app.spaz_appearances.keys()) if s not in disallowed
    ]


class Appearance:
    """Create and fill out one of these suckers to define a spaz appearance"""

    def __init__(self, name: str):
        self.name = name
        if self.name in ba.app.spaz_appearances:
            raise Exception('spaz appearance name "' + self.name +
                            '" already exists.')
        ba.app.spaz_appearances[self.name] = self
        self.base_appearance = None
        self.color_texture = ''
        self.color_mask_texture = ''
        self.icon_texture = ''
        self.icon_mask_texture = ''
        self.head_model = ''
        self.torso_model = ''
        self.pelvis_model = ''
        self.upper_arm_model = ''
        self.forearm_model = ''
        self.hand_model = ''
        self.upper_leg_model = ''
        self.lower_leg_model = ''
        self.toes_model = ''
        self.jump_sounds: list[str] = []
        self.attack_sounds: list[str] = []
        self.impact_sounds: list[str] = []
        self.death_sounds: list[str] = []
        self.pickup_sounds: list[str] = []
        self.fall_sounds: list[str] = []
        self.style = 'spaz'
        self.default_color: tuple[float, float, float] | None = None
        self.default_highlight: tuple[float, float, float] | None = None


def register_appearances() -> None:
    """Register our builtin spaz appearances."""

    # this is quite ugly but will be going away so not worth cleaning up
    # pylint: disable=invalid-name
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements

    # Spaz #######################################
    spaz = Appearance('Spaz')
    spaz.base_appearance = None
    spaz.color_texture = 'neoSpazColor'
    spaz.color_mask_texture = 'neoSpazColorMask'
    spaz.icon_texture = 'neoSpazIcon'
    spaz.icon_mask_texture = 'neoSpazIconColorMask'
    spaz.head_model = 'neoSpazHead'
    spaz.torso_model = 'neoSpazTorso'
    spaz.pelvis_model = 'neoSpazPelvis'
    spaz.upper_arm_model = 'neoSpazUpperArm'
    spaz.forearm_model = 'neoSpazForeArm'
    spaz.hand_model = 'neoSpazHand'
    spaz.upper_leg_model = 'neoSpazUpperLeg'
    spaz.lower_leg_model = 'neoSpazLowerLeg'
    spaz.toes_model = 'neoSpazToes'
    spaz.jump_sounds = ['spazJump01', 'spazJump02', 'spazJump03', 'spazJump04']
    spaz.attack_sounds = [
        'spazAttack01', 'spazAttack02', 'spazAttack03', 'spazAttack04'
    ]
    spaz.impact_sounds = [
        'spazImpact01', 'spazImpact02', 'spazImpact03', 'spazImpact04'
    ]
    spaz.death_sounds = ['spazDeath01']
    spaz.pickup_sounds = ['spazPickup01']
    spaz.fall_sounds = ['spazFall01']
    spaz.style = 'spaz'

    # Zoe #####################################
    zoe = Appearance('Zoe')
    zoe.base_appearance = None
    zoe.color_texture = 'zoeColor'
    zoe.color_mask_texture = 'zoeColorMask'
    zoe.default_color = (0.6, 0.6, 0.6)
    zoe.default_highlight = (0, 1, 0)
    zoe.icon_texture = 'zoeIcon'
    zoe.icon_mask_texture = 'zoeIconColorMask'
    zoe.head_model = 'zoeHead'
    zoe.torso_model = 'zoeTorso'
    zoe.pelvis_model = 'zoePelvis'
    zoe.upper_arm_model = 'zoeUpperArm'
    zoe.forearm_model = 'zoeForeArm'
    zoe.hand_model = 'zoeHand'
    zoe.upper_leg_model = 'zoeUpperLeg'
    zoe.lower_leg_model = 'zoeLowerLeg'
    zoe.toes_model = 'zoeToes'
    zoe.jump_sounds = ['zoeJump01', 'zoeJump02', 'zoeJump03']
    zoe.attack_sounds = [
        'zoeAttack01', 'zoeAttack02', 'zoeAttack03', 'zoeAttack04'
    ]
    zoe.impact_sounds = [
        'zoeImpact01', 'zoeImpact02', 'zoeImpact03', 'zoeImpact04'
    ]
    zoe.death_sounds = ['zoeDeath01']
    zoe.pickup_sounds = ['zoePickup01']
    zoe.fall_sounds = ['zoeFall01']
    zoe.style = 'female'

    # Ninja ##########################################
    ninja = Appearance('Snake Shadow')
    ninja.base_appearance = None
    ninja.color_texture = 'ninjaColor'
    ninja.color_mask_texture = 'ninjaColorMask'
    ninja.default_color = (1, 1, 1)
    ninja.default_highlight = (0.55, 0.8, 0.55)
    ninja.icon_texture = 'ninjaIcon'
    ninja.icon_mask_texture = 'ninjaIconColorMask'
    ninja.head_model = 'ninjaHead'
    ninja.torso_model = 'ninjaTorso'
    ninja.pelvis_model = 'ninjaPelvis'
    ninja.upper_arm_model = 'ninjaUpperArm'
    ninja.forearm_model = 'ninjaForeArm'
    ninja.hand_model = 'ninjaHand'
    ninja.upper_leg_model = 'ninjaUpperLeg'
    ninja.lower_leg_model = 'ninjaLowerLeg'
    ninja.toes_model = 'ninjaToes'
    ninja_attacks = ['ninjaAttack' + str(i + 1) + '' for i in range(7)]
    ninja_hits = ['ninjaHit' + str(i + 1) + '' for i in range(8)]
    ninja_jumps = ['ninjaAttack' + str(i + 1) + '' for i in range(7)]
    ninja.jump_sounds = ninja_jumps
    ninja.attack_sounds = ninja_attacks
    ninja.impact_sounds = ninja_hits
    ninja.death_sounds = ['ninjaDeath1']
    ninja.pickup_sounds = ninja_attacks
    ninja.fall_sounds = ['ninjaFall1']
    ninja.style = 'ninja'

    # Barbarian #####################################
    kronk = Appearance('Kronk')
    kronk.base_appearance = None
    kronk.color_texture = 'kronk'
    kronk.color_mask_texture = 'kronkColorMask'
    kronk.default_color = (0.4, 0.5, 0.4)
    kronk.default_highlight = (1, 0.5, 0.3)
    kronk.icon_texture = 'kronkIcon'
    kronk.icon_mask_texture = 'kronkIconColorMask'
    kronk.head_model = 'kronkHead'
    kronk.torso_model = 'kronkTorso'
    kronk.pelvis_model = 'kronkPelvis'
    kronk.upper_arm_model = 'kronkUpperArm'
    kronk.forearm_model = 'kronkForeArm'
    kronk.hand_model = 'kronkHand'
    kronk.upper_leg_model = 'kronkUpperLeg'
    kronk.lower_leg_model = 'kronkLowerLeg'
    kronk.toes_model = 'kronkToes'
    kronk_sounds = [
        'kronk1', 'kronk2', 'kronk3', 'kronk4', 'kronk5', 'kronk6', 'kronk7',
        'kronk8', 'kronk9', 'kronk10'
    ]
    kronk.jump_sounds = kronk_sounds
    kronk.attack_sounds = kronk_sounds
    kronk.impact_sounds = kronk_sounds
    kronk.death_sounds = ['kronkDeath']
    kronk.pickup_sounds = kronk_sounds
    kronk.fall_sounds = ['kronkFall']
    kronk.style = 'kronk'

    # Chef ###########################################
    mel = Appearance('Mel')
    mel.base_appearance = None
    mel.color_texture = 'melColor'
    mel.color_mask_texture = 'melColorMask'
    mel.default_color = (1, 1, 1)
    mel.default_highlight = (0.1, 0.6, 0.1)
    mel.icon_texture = 'melIcon'
    mel.icon_mask_texture = 'melIconColorMask'
    mel.head_model = 'melHead'
    mel.torso_model = 'melTorso'
    mel.pelvis_model = 'kronkPelvis'
    mel.upper_arm_model = 'melUpperArm'
    mel.forearm_model = 'melForeArm'
    mel.hand_model = 'melHand'
    mel.upper_leg_model = 'melUpperLeg'
    mel.lower_leg_model = 'melLowerLeg'
    mel.toes_model = 'melToes'
    mel_sounds = [
        'mel01', 'mel02', 'mel03', 'mel04', 'mel05', 'mel06', 'mel07', 'mel08',
        'mel09', 'mel10'
    ]
    mel.attack_sounds = mel_sounds
    mel.jump_sounds = mel_sounds
    mel.impact_sounds = mel_sounds
    mel.death_sounds = ['melDeath01']
    mel.pickup_sounds = mel_sounds
    mel.fall_sounds = ['melFall01']
    mel.style = 'mel'

    # Pirate #######################################
    jack = Appearance('Jack Morgan')
    jack.base_appearance = None
    jack.color_texture = 'jackColor'
    jack.color_mask_texture = 'jackColorMask'
    jack.default_color = (1, 0.2, 0.1)
    jack.default_highlight = (1, 1, 0)
    jack.icon_texture = 'jackIcon'
    jack.icon_mask_texture = 'jackIconColorMask'
    jack.head_model = 'jackHead'
    jack.torso_model = 'jackTorso'
    jack.pelvis_model = 'kronkPelvis'
    jack.upper_arm_model = 'jackUpperArm'
    jack.forearm_model = 'jackForeArm'
    jack.hand_model = 'jackHand'
    jack.upper_leg_model = 'jackUpperLeg'
    jack.lower_leg_model = 'jackLowerLeg'
    jack.toes_model = 'jackToes'
    hit_sounds = [
        'jackHit01', 'jackHit02', 'jackHit03', 'jackHit04', 'jackHit05',
        'jackHit06', 'jackHit07'
    ]
    sounds = ['jack01', 'jack02', 'jack03', 'jack04', 'jack05', 'jack06']
    jack.attack_sounds = sounds
    jack.jump_sounds = sounds
    jack.impact_sounds = hit_sounds
    jack.death_sounds = ['jackDeath01']
    jack.pickup_sounds = sounds
    jack.fall_sounds = ['jackFall01']
    jack.style = 'pirate'

    # Santa ######################################
    santa = Appearance('Santa Claus')
    santa.base_appearance = None
    santa.color_texture = 'santaColor'
    santa.color_mask_texture = 'santaColorMask'
    santa.default_color = (1, 0, 0)
    santa.default_highlight = (1, 1, 1)
    santa.icon_texture = 'santaIcon'
    santa.icon_mask_texture = 'santaIconColorMask'
    santa.head_model = 'santaHead'
    santa.torso_model = 'santaTorso'
    santa.pelvis_model = 'kronkPelvis'
    santa.upper_arm_model = 'santaUpperArm'
    santa.forearm_model = 'santaForeArm'
    santa.hand_model = 'santaHand'
    santa.upper_leg_model = 'santaUpperLeg'
    santa.lower_leg_model = 'santaLowerLeg'
    santa.toes_model = 'santaToes'
    santa.impact_sounds = ['santaHit01', 'santaHit02', 'santaHit03', 'santaHit04']
    santa.attack_sounds = ['santa01', 'santa02', 'santa03', 'santa04', 'santa05']
    santa.jump_sounds = ['santa01', 'santa02', 'santa03', 'santa04', 'santa05']
    santa.death_sounds = ['santaDeath']
    santa.pickup_sounds = ['santa01', 'santa02', 'santa03', 'santa04', 'santa05']
    santa.fall_sounds = ['santaFall']
    santa.style = 'santa'

    # Snowman ###################################
    frosty = Appearance('Frosty')
    frosty.base_appearance = None
    frosty.color_texture = 'frostyColor'
    frosty.color_mask_texture = 'frostyColorMask'
    frosty.default_color = (0.5, 0.5, 1)
    frosty.default_highlight = (1, 0.5, 0)
    frosty.icon_texture = 'frostyIcon'
    frosty.icon_mask_texture = 'frostyIconColorMask'
    frosty.head_model = 'frostyHead'
    frosty.torso_model = 'frostyTorso'
    frosty.pelvis_model = 'frostyPelvis'
    frosty.upper_arm_model = 'frostyUpperArm'
    frosty.forearm_model = 'frostyForeArm'
    frosty.hand_model = 'frostyHand'
    frosty.upper_leg_model = 'frostyUpperLeg'
    frosty.lower_leg_model = 'frostyLowerLeg'
    frosty.toes_model = 'frostyToes'
    frosty_sounds = [
        'frosty01', 'frosty02', 'frosty03', 'frosty04', 'frosty05'
    ]
    frosty_hit_sounds = ['frostyHit01', 'frostyHit02', 'frostyHit03']
    frosty.attack_sounds = frosty_sounds
    frosty.jump_sounds = frosty_sounds
    frosty.impact_sounds = frosty_hit_sounds
    frosty.death_sounds = ['frostyDeath']
    frosty.pickup_sounds = frosty_sounds
    frosty.fall_sounds = ['frostyFall']
    frosty.style = 'frosty'

    # Skeleton ################################
    bones = Appearance('Bones')
    bones.base_appearance = None
    bones.color_texture = 'bonesColor'
    bones.color_mask_texture = 'bonesColorMask'
    bones.default_color = (0.6, 0.9, 1)
    bones.default_highlight = (0.6, 0.9, 1)
    bones.icon_texture = 'bonesIcon'
    bones.icon_mask_texture = 'bonesIconColorMask'
    bones.head_model = 'bonesHead'
    bones.torso_model = 'bonesTorso'
    bones.pelvis_model = 'bonesPelvis'
    bones.upper_arm_model = 'bonesUpperArm'
    bones.forearm_model = 'bonesForeArm'
    bones.hand_model = 'bonesHand'
    bones.upper_leg_model = 'bonesUpperLeg'
    bones.lower_leg_model = 'bonesLowerLeg'
    bones.toes_model = 'bonesToes'
    bones_sounds = ['bones1', 'bones2', 'bones3']
    bones_hit_sounds = ['bones1', 'bones2', 'bones3']
    bones.attack_sounds = bones_sounds
    bones.jump_sounds = bones_sounds
    bones.impact_sounds = bones_hit_sounds
    bones.death_sounds = ['bonesDeath']
    bones.pickup_sounds = bones_sounds
    bones.fall_sounds = ['bonesFall']
    bones.style = 'bones'
    
    # Bosbone ################################
    bosbone = Appearance('Bosbone')
    bosbone.base_appearance = bones
    bosbone.color_texture = 'bosboneColor'
    bosbone.color_mask_texture = 'bosboneColorMask'
    bosbone.default_color = (0.6, 0.9, 1)
    bosbone.default_highlight = (0.6, 0.9, 1)
    bosbone.icon_texture = 'bosboneIcon'
    bosbone.icon_mask_texture = 'bosboneIconColorMask'
    bosbone.head_model = 'bosboneHead'
    bosbone.torso_model = 'bosboneTorso'
    bosbone.pelvis_model = 'bosbonePelvis'
    bosbone.upper_arm_model = 'bonesUpperArm'
    bosbone.forearm_model = 'bonesForeArm'
    bosbone.hand_model = 'bosboneHand'
    bosbone.upper_leg_model = 'bonesUpperLeg'
    bosbone.lower_leg_model = 'bonesLowerLeg'
    bosbone.toes_model = 'bonesToes'
    bosbone_sounds = ['bones1', 'bones2', 'bones3']
    bosbone_hit_sounds = ['bones1', 'bones2', 'bones3']
    bosbone.attack_sounds = bosbone_sounds
    bosbone.jump_sounds = bosbone_sounds
    bosbone.impact_sounds = bosbone_hit_sounds
    bosbone.death_sounds = ['bonesDeath']
    bosbone.pickup_sounds = bosbone_sounds
    bosbone.fall_sounds = ['bonesFall']
    bosbone.style = 'bones'

    # Bear ###################################
    bernard = Appearance('Bernard')
    bernard.base_appearance = None
    bernard.color_texture = 'bearColor'
    bernard.color_mask_texture = 'bearColorMask'
    bernard.default_color = (0.7, 0.5, 0.0)
    bernard.icon_texture = 'bearIcon'
    bernard.icon_mask_texture = 'bearIconColorMask'
    bernard.head_model = 'bearHead'
    bernard.torso_model = 'bearTorso'
    bernard.pelvis_model = 'bearPelvis'
    bernard.upper_arm_model = 'bearUpperArm'
    bernard.forearm_model = 'bearForeArm'
    bernard.hand_model = 'bearHand'
    bernard.upper_leg_model = 'bearUpperLeg'
    bernard.lower_leg_model = 'bearLowerLeg'
    bernard.toes_model = 'bearToes'
    bear_sounds = ['bear1', 'bear2', 'bear3', 'bear4']
    bear_hit_sounds = ['bearHit1', 'bearHit2']
    bernard.attack_sounds = bear_sounds
    bernard.jump_sounds = bear_sounds
    bernard.impact_sounds = bear_hit_sounds
    bernard.death_sounds = ['bearDeath']
    bernard.pickup_sounds = bear_sounds
    bernard.fall_sounds = ['bearFall']
    bernard.style = 'bear'

    # Penguin ###################################
    pascal = Appearance('Pascal')
    pascal.base_appearance = None
    pascal.color_texture = 'penguinColor'
    pascal.color_mask_texture = 'penguinColorMask'
    pascal.default_color = (0.3, 0.5, 0.8)
    pascal.default_highlight = (1, 0, 0)
    pascal.icon_texture = 'penguinIcon'
    pascal.icon_mask_texture = 'penguinIconColorMask'
    pascal.head_model = 'penguinHead'
    pascal.torso_model = 'penguinTorso'
    pascal.pelvis_model = 'penguinPelvis'
    pascal.upper_arm_model = 'penguinUpperArm'
    pascal.forearm_model = 'penguinForeArm'
    pascal.hand_model = 'penguinHand'
    pascal.upper_leg_model = 'penguinUpperLeg'
    pascal.lower_leg_model = 'penguinLowerLeg'
    pascal.toes_model = 'penguinToes'
    penguin_sounds = ['penguin1', 'penguin2', 'penguin3', 'penguin4']
    penguin_hit_sounds = ['penguinHit1', 'penguinHit2']
    pascal.attack_sounds = penguin_sounds
    pascal.jump_sounds = penguin_sounds
    pascal.impact_sounds = penguin_hit_sounds
    pascal.death_sounds = ['penguinDeath']
    pascal.pickup_sounds = penguin_sounds
    pascal.fall_sounds = ['penguinFall']
    pascal.style = 'penguin'

    # Ali ###################################
    ali = Appearance('Taobao Mascot')
    ali.base_appearance = None
    ali.color_texture = 'aliColor'
    ali.color_mask_texture = 'aliColorMask'
    ali.default_color = (1, 0.5, 0)
    ali.default_highlight = (1, 1, 1)
    ali.icon_texture = 'aliIcon'
    ali.icon_mask_texture = 'aliIconColorMask'
    ali.head_model = 'aliHead'
    ali.torso_model = 'aliTorso'
    ali.pelvis_model = 'aliPelvis'
    ali.upper_arm_model = 'aliUpperArm'
    ali.forearm_model = 'aliForeArm'
    ali.hand_model = 'aliHand'
    ali.upper_leg_model = 'aliUpperLeg'
    ali.lower_leg_model = 'aliLowerLeg'
    ali.toes_model = 'aliToes'
    ali_sounds = ['ali1', 'ali2', 'ali3', 'ali4']
    ali_hit_sounds = ['aliHit1', 'aliHit2']
    ali.attack_sounds = ali_sounds
    ali.jump_sounds = ali_sounds
    ali.impact_sounds = ali_hit_sounds
    ali.death_sounds = ['aliDeath']
    ali.pickup_sounds = ali_sounds
    ali.fall_sounds = ['aliFall']
    ali.style = 'ali'

    # cyborg ###################################
    cyborg = Appearance('B-9000')
    cyborg.base_appearance = None
    cyborg.color_texture = 'cyborgColor'
    cyborg.color_mask_texture = 'cyborgColorMask'
    cyborg.default_color = (0.5, 0.5, 0.5)
    cyborg.default_highlight = (1, 0, 0)
    cyborg.icon_texture = 'cyborgIcon'
    cyborg.icon_mask_texture = 'cyborgIconColorMask'
    cyborg.head_model = 'cyborgHead'
    cyborg.torso_model = 'cyborgTorso'
    cyborg.pelvis_model = 'cyborgPelvis'
    cyborg.upper_arm_model = 'cyborgUpperArm'
    cyborg.forearm_model = 'cyborgForeArm'
    cyborg.hand_model = 'cyborgHand'
    cyborg.upper_leg_model = 'cyborgUpperLeg'
    cyborg.lower_leg_model = 'cyborgLowerLeg'
    cyborg.toes_model = 'cyborgToes'
    cyborg_sounds = ['cyborg1', 'cyborg2', 'cyborg3', 'cyborg4']
    cyborg_hit_sounds = ['cyborgHit1', 'cyborgHit2']
    cyborg.attack_sounds = cyborg_sounds
    cyborg.jump_sounds = cyborg_sounds
    cyborg.impact_sounds = cyborg_hit_sounds
    cyborg.death_sounds = ['cyborgDeath']
    cyborg.pickup_sounds = cyborg_sounds
    cyborg.fall_sounds = ['cyborgFall']
    cyborg.style = 'cyborg'

    # Agent ###################################
    agent = Appearance('Agent Johnson')
    agent.base_appearance = None
    agent.color_texture = 'agentColor'
    agent.color_mask_texture = 'agentColorMask'
    agent.default_color = (0.3, 0.3, 0.33)
    agent.default_highlight = (1, 0.5, 0.3)
    agent.icon_texture = 'agentIcon'
    agent.icon_mask_texture = 'agentIconColorMask'
    agent.head_model = 'agentHead'
    agent.torso_model = 'agentTorso'
    agent.pelvis_model = 'agentPelvis'
    agent.upper_arm_model = 'agentUpperArm'
    agent.forearm_model = 'agentForeArm'
    agent.hand_model = 'agentHand'
    agent.upper_leg_model = 'agentUpperLeg'
    agent.lower_leg_model = 'agentLowerLeg'
    agent.toes_model = 'agentToes'
    agent_sounds = ['agent1', 'agent2', 'agent3', 'agent4']
    agent_hit_sounds = ['agentHit1', 'agentHit2']
    agent.attack_sounds = agent_sounds
    agent.jump_sounds = agent_sounds
    agent.impact_sounds = agent_hit_sounds
    agent.death_sounds = ['agentDeath']
    agent.pickup_sounds = agent_sounds
    agent.fall_sounds = ['agentFall']
    agent.style = 'agent'

    # Jumpsuit ###################################
    lee = Appearance('Lee')
    lee.base_appearance = None
    lee.color_texture = 'jumpsuitColor'
    lee.color_mask_texture = 'jumpsuitColorMask'
    lee.default_color = (0.3, 0.5, 0.8)
    lee.default_highlight = (1, 0, 0)
    lee.icon_texture = 'jumpsuitIcon'
    lee.icon_mask_texture = 'jumpsuitIconColorMask'
    lee.head_model = 'jumpsuitHead'
    lee.torso_model = 'jumpsuitTorso'
    lee.pelvis_model = 'jumpsuitPelvis'
    lee.upper_arm_model = 'jumpsuitUpperArm'
    lee.forearm_model = 'jumpsuitForeArm'
    lee.hand_model = 'jumpsuitHand'
    lee.upper_leg_model = 'jumpsuitUpperLeg'
    lee.lower_leg_model = 'jumpsuitLowerLeg'
    lee.toes_model = 'jumpsuitToes'
    jumpsuit_sounds = ['jumpsuit1', 'jumpsuit2', 'jumpsuit3', 'jumpsuit4']
    jumpsuit_hit_sounds = ['jumpsuitHit1', 'jumpsuitHit2']
    lee.attack_sounds = jumpsuit_sounds
    lee.jump_sounds = jumpsuit_sounds
    lee.impact_sounds = jumpsuit_hit_sounds
    lee.death_sounds = ['jumpsuitDeath']
    lee.pickup_sounds = jumpsuit_sounds
    lee.fall_sounds = ['jumpsuitFall']
    lee.style = 'spaz'

    # ActionHero ###################################
    todd = Appearance('Todd McBurton')
    todd.base_appearance = None
    todd.color_texture = 'actionHeroColor'
    todd.color_mask_texture = 'actionHeroColorMask'
    todd.default_color = (0.3, 0.5, 0.8)
    todd.default_highlight = (1, 0, 0)
    todd.icon_texture = 'actionHeroIcon'
    todd.icon_mask_texture = 'actionHeroIconColorMask'
    todd.head_model = 'actionHeroHead'
    todd.torso_model = 'actionHeroTorso'
    todd.pelvis_model = 'actionHeroPelvis'
    todd.upper_arm_model = 'actionHeroUpperArm'
    todd.forearm_model = 'actionHeroForeArm'
    todd.hand_model = 'actionHeroHand'
    todd.upper_leg_model = 'actionHeroUpperLeg'
    todd.lower_leg_model = 'actionHeroLowerLeg'
    todd.toes_model = 'actionHeroToes'
    action_hero_sounds = [
        'actionHero1', 'actionHero2', 'actionHero3', 'actionHero4'
    ]
    action_hero_hit_sounds = ['actionHeroHit1', 'actionHeroHit2']
    todd.attack_sounds = action_hero_sounds
    todd.jump_sounds = action_hero_sounds
    todd.impact_sounds = action_hero_hit_sounds
    todd.death_sounds = ['actionHeroDeath']
    todd.pickup_sounds = action_hero_sounds
    todd.fall_sounds = ['actionHeroFall']
    todd.style = 'spaz'

    # Assassin ###################################
    zola = Appearance('Zola')
    zola.base_appearance = None
    zola.color_texture = 'assassinColor'
    zola.color_mask_texture = 'assassinColorMask'
    zola.default_color = (0.3, 0.5, 0.8)
    zola.default_highlight = (1, 0, 0)
    zola.icon_texture = 'assassinIcon'
    zola.icon_mask_texture = 'assassinIconColorMask'
    zola.head_model = 'assassinHead'
    zola.torso_model = 'assassinTorso'
    zola.pelvis_model = 'assassinPelvis'
    zola.upper_arm_model = 'assassinUpperArm'
    zola.forearm_model = 'assassinForeArm'
    zola.hand_model = 'assassinHand'
    zola.upper_leg_model = 'assassinUpperLeg'
    zola.lower_leg_model = 'assassinLowerLeg'
    zola.toes_model = 'assassinToes'
    assassin_sounds = ['assassin1', 'assassin2', 'assassin3', 'assassin4']
    assassin_hit_sounds = ['assassinHit1', 'assassinHit2']
    zola.attack_sounds = assassin_sounds
    zola.jump_sounds = assassin_sounds
    zola.impact_sounds = assassin_hit_sounds
    zola.death_sounds = ['assassinDeath']
    zola.pickup_sounds = assassin_sounds
    zola.fall_sounds = ['assassinFall']
    zola.style = 'spaz'

    # Wizard ###################################
    wizard = Appearance('Grumbledorf')
    wizard.base_appearance = None
    wizard.color_texture = 'wizardColor'
    wizard.color_mask_texture = 'wizardColorMask'
    wizard.default_color = (0.2, 0.4, 1.0)
    wizard.default_highlight = (0.06, 0.15, 0.4)
    wizard.icon_texture = 'wizardIcon'
    wizard.icon_mask_texture = 'wizardIconColorMask'
    wizard.head_model = 'wizardHead'
    wizard.torso_model = 'wizardTorso'
    wizard.pelvis_model = 'wizardPelvis'
    wizard.upper_arm_model = 'wizardUpperArm'
    wizard.forearm_model = 'wizardForeArm'
    wizard.hand_model = 'wizardHand'
    wizard.upper_leg_model = 'wizardUpperLeg'
    wizard.lower_leg_model = 'wizardLowerLeg'
    wizard.toes_model = 'wizardToes'
    wizard_sounds = ['wizard1', 'wizard2', 'wizard3', 'wizard4']
    wizard_hit_sounds = ['wizardHit1', 'wizardHit2']
    wizard.attack_sounds = wizard_sounds
    wizard.jump_sounds = wizard_sounds
    wizard.impact_sounds = wizard_hit_sounds
    wizard.death_sounds = ['wizardDeath']
    wizard.pickup_sounds = wizard_sounds
    wizard.fall_sounds = ['wizardFall']
    wizard.style = 'spaz'

    # Cowboy ###################################
    cowboy = Appearance('Butch')
    cowboy.base_appearance = None
    cowboy.color_texture = 'cowboyColor'
    cowboy.color_mask_texture = 'cowboyColorMask'
    cowboy.default_color = (0.3, 0.5, 0.8)
    cowboy.default_highlight = (1, 0, 0)
    cowboy.icon_texture = 'cowboyIcon'
    cowboy.icon_mask_texture = 'cowboyIconColorMask'
    cowboy.head_model = 'cowboyHead'
    cowboy.torso_model = 'cowboyTorso'
    cowboy.pelvis_model = 'cowboyPelvis'
    cowboy.upper_arm_model = 'cowboyUpperArm'
    cowboy.forearm_model = 'cowboyForeArm'
    cowboy.hand_model = 'cowboyHand'
    cowboy.upper_leg_model = 'cowboyUpperLeg'
    cowboy.lower_leg_model = 'cowboyLowerLeg'
    cowboy.toes_model = 'cowboyToes'
    cowboy_sounds = ['cowboy1', 'cowboy2', 'cowboy3', 'cowboy4']
    cowboy_hit_sounds = ['cowboyHit1', 'cowboyHit2']
    cowboy.attack_sounds = cowboy_sounds
    cowboy.jump_sounds = cowboy_sounds
    cowboy.impact_sounds = cowboy_hit_sounds
    cowboy.death_sounds = ['cowboyDeath']
    cowboy.pickup_sounds = cowboy_sounds
    cowboy.fall_sounds = ['cowboyFall']
    cowboy.style = 'spaz'

    # Witch ###################################
    witch = Appearance('Witch')
    witch.base_appearance = None
    witch.color_texture = 'witchColor'
    witch.color_mask_texture = 'witchColorMask'
    witch.default_color = (0.3, 0.5, 0.8)
    witch.default_highlight = (1, 0, 0)
    witch.icon_texture = 'witchIcon'
    witch.icon_mask_texture = 'witchIconColorMask'
    witch.head_model = 'witchHead'
    witch.torso_model = 'witchTorso'
    witch.pelvis_model = 'witchPelvis'
    witch.upper_arm_model = 'witchUpperArm'
    witch.forearm_model = 'witchForeArm'
    witch.hand_model = 'witchHand'
    witch.upper_leg_model = 'witchUpperLeg'
    witch.lower_leg_model = 'witchLowerLeg'
    witch.toes_model = 'witchToes'
    witch_sounds = ['witch1', 'witch2', 'witch3', 'witch4']
    witch_hit_sounds = ['witchHit1', 'witchHit2']
    witch.attack_sounds = witch_sounds
    witch.jump_sounds = witch_sounds
    witch.impact_sounds = witch_hit_sounds
    witch.death_sounds = ['witchDeath']
    witch.pickup_sounds = witch_sounds
    witch.fall_sounds = ['witchFall']
    witch.style = 'spaz'

    # Warrior ###################################
    warrior = Appearance('Warrior')
    warrior.base_appearance = None
    warrior.color_texture = 'warriorColor'
    warrior.color_mask_texture = 'warriorColorMask'
    warrior.default_color = (0.3, 0.5, 0.8)
    warrior.default_highlight = (1, 0, 0)
    warrior.icon_texture = 'warriorIcon'
    warrior.icon_mask_texture = 'warriorIconColorMask'
    warrior.head_model = 'warriorHead'
    warrior.torso_model = 'warriorTorso'
    warrior.pelvis_model = 'warriorPelvis'
    warrior.upper_arm_model = 'warriorUpperArm'
    warrior.forearm_model = 'warriorForeArm'
    warrior.hand_model = 'warriorHand'
    warrior.upper_leg_model = 'warriorUpperLeg'
    warrior.lower_leg_model = 'warriorLowerLeg'
    warrior.toes_model = 'warriorToes'
    warrior_sounds = ['warrior1', 'warrior2', 'warrior3', 'warrior4']
    warrior_hit_sounds = ['warriorHit1', 'warriorHit2']
    warrior.attack_sounds = warrior_sounds
    warrior.jump_sounds = warrior_sounds
    warrior.impact_sounds = warrior_hit_sounds
    warrior.death_sounds = ['warriorDeath']
    warrior.pickup_sounds = warrior_sounds
    warrior.fall_sounds = ['warriorFall']
    warrior.style = 'spaz'

    # Superhero ###################################
    middleman = Appearance('Middle-Man')
    middleman.base_appearance = None
    middleman.color_texture = 'superheroColor'
    middleman.color_mask_texture = 'superheroColorMask'
    middleman.default_color = (0.3, 0.5, 0.8)
    middleman.default_highlight = (1, 0, 0)
    middleman.icon_texture = 'superheroIcon'
    middleman.icon_mask_texture = 'superheroIconColorMask'
    middleman.head_model = 'superheroHead'
    middleman.torso_model = 'superheroTorso'
    middleman.pelvis_model = 'superheroPelvis'
    middleman.upper_arm_model = 'superheroUpperArm'
    middleman.forearm_model = 'superheroForeArm'
    middleman.hand_model = 'superheroHand'
    middleman.upper_leg_model = 'superheroUpperLeg'
    middleman.lower_leg_model = 'superheroLowerLeg'
    middleman.toes_model = 'superheroToes'
    superhero_sounds = ['superhero1', 'superhero2', 'superhero3', 'superhero4']
    superhero_hit_sounds = ['superheroHit1', 'superheroHit2']
    middleman.attack_sounds = superhero_sounds
    middleman.jump_sounds = superhero_sounds
    middleman.impact_sounds = superhero_hit_sounds
    middleman.death_sounds = ['superheroDeath']
    middleman.pickup_sounds = superhero_sounds
    middleman.fall_sounds = ['superheroFall']
    middleman.style = 'spaz'

    # Alien ###################################
    alien = Appearance('Alien')
    alien.base_appearance = None
    alien.color_texture = 'alienColor'
    alien.color_mask_texture = 'alienColorMask'
    alien.default_color = (0.3, 0.5, 0.8)
    alien.default_highlight = (1, 0, 0)
    alien.icon_texture = 'alienIcon'
    alien.icon_mask_texture = 'alienIconColorMask'
    alien.head_model = 'alienHead'
    alien.torso_model = 'alienTorso'
    alien.pelvis_model = 'alienPelvis'
    alien.upper_arm_model = 'alienUpperArm'
    alien.forearm_model = 'alienForeArm'
    alien.hand_model = 'alienHand'
    alien.upper_leg_model = 'alienUpperLeg'
    alien.lower_leg_model = 'alienLowerLeg'
    alien.toes_model = 'alienToes'
    alien_sounds = ['alien1', 'alien2', 'alien3', 'alien4']
    alien_hit_sounds = ['alienHit1', 'alienHit2']
    alien.attack_sounds = alien_sounds
    alien.jump_sounds = alien_sounds
    alien.impact_sounds = alien_hit_sounds
    alien.death_sounds = ['alienDeath']
    alien.pickup_sounds = alien_sounds
    alien.fall_sounds = ['alienFall']
    alien.style = 'spaz'

    # OldLady ###################################
    oldlady = Appearance('OldLady')
    oldlady.base_appearance = None
    oldlady.color_texture = 'oldLadyColor'
    oldlady.color_mask_texture = 'oldLadyColorMask'
    oldlady.default_color = (0.3, 0.5, 0.8)
    oldlady.default_highlight = (1, 0, 0)
    oldlady.icon_texture = 'oldLadyIcon'
    oldlady.icon_mask_texture = 'oldLadyIconColorMask'
    oldlady.head_model = 'oldLadyHead'
    oldlady.torso_model = 'oldLadyTorso'
    oldlady.pelvis_model = 'oldLadyPelvis'
    oldlady.upper_arm_model = 'oldLadyUpperArm'
    oldlady.forearm_model = 'oldLadyForeArm'
    oldlady.hand_model = 'oldLadyHand'
    oldlady.upper_leg_model = 'oldLadyUpperLeg'
    oldlady.lower_leg_model = 'oldLadyLowerLeg'
    oldlady.toes_model = 'oldLadyToes'
    old_lady_sounds = ['oldLady1', 'oldLady2', 'oldLady3', 'oldLady4']
    old_lady_hit_sounds = ['oldLadyHit1', 'oldLadyHit2']
    oldlady.attack_sounds = old_lady_sounds
    oldlady.jump_sounds = old_lady_sounds
    oldlady.impact_sounds = old_lady_hit_sounds
    oldlady.death_sounds = ['oldLadyDeath']
    oldlady.pickup_sounds = old_lady_sounds
    oldlady.fall_sounds = ['oldLadyFall']
    oldlady.style = 'spaz'

    # Gladiator ###################################
    gladiator = Appearance('Gladiator')
    gladiator.base_appearance = None
    gladiator.color_texture = 'gladiatorColor'
    gladiator.color_mask_texture = 'gladiatorColorMask'
    gladiator.default_color = (0.3, 0.5, 0.8)
    gladiator.default_highlight = (1, 0, 0)
    gladiator.icon_texture = 'gladiatorIcon'
    gladiator.icon_mask_texture = 'gladiatorIconColorMask'
    gladiator.head_model = 'gladiatorHead'
    gladiator.torso_model = 'gladiatorTorso'
    gladiator.pelvis_model = 'gladiatorPelvis'
    gladiator.upper_arm_model = 'gladiatorUpperArm'
    gladiator.forearm_model = 'gladiatorForeArm'
    gladiator.hand_model = 'gladiatorHand'
    gladiator.upper_leg_model = 'gladiatorUpperLeg'
    gladiator.lower_leg_model = 'gladiatorLowerLeg'
    gladiator.toes_model = 'gladiatorToes'
    gladiator_sounds = ['gladiator1', 'gladiator2', 'gladiator3', 'gladiator4']
    gladiator_hit_sounds = ['gladiatorHit1', 'gladiatorHit2']
    gladiator.attack_sounds = gladiator_sounds
    gladiator.jump_sounds = gladiator_sounds
    gladiator.impact_sounds = gladiator_hit_sounds
    gladiator.death_sounds = ['gladiatorDeath']
    gladiator.pickup_sounds = gladiator_sounds
    gladiator.fall_sounds = ['gladiatorFall']
    gladiator.style = 'spaz'

    # Wrestler ###################################
    wrestler = Appearance('Wrestler')
    wrestler.base_appearance = None
    wrestler.color_texture = 'wrestlerColor'
    wrestler.color_mask_texture = 'wrestlerColorMask'
    wrestler.default_color = (0.3, 0.5, 0.8)
    wrestler.default_highlight = (1, 0, 0)
    wrestler.icon_texture = 'wrestlerIcon'
    wrestler.icon_mask_texture = 'wrestlerIconColorMask'
    wrestler.head_model = 'wrestlerHead'
    wrestler.torso_model = 'wrestlerTorso'
    wrestler.pelvis_model = 'wrestlerPelvis'
    wrestler.upper_arm_model = 'wrestlerUpperArm'
    wrestler.forearm_model = 'wrestlerForeArm'
    wrestler.hand_model = 'wrestlerHand'
    wrestler.upper_leg_model = 'wrestlerUpperLeg'
    wrestler.lower_leg_model = 'wrestlerLowerLeg'
    wrestler.toes_model = 'wrestlerToes'
    wrestler_sounds = ['wrestler1', 'wrestler2', 'wrestler3', 'wrestler4']
    wrestler_hit_sounds = ['wrestlerHit1', 'wrestlerHit2']
    wrestler.attack_sounds = wrestler_sounds
    wrestler.jump_sounds = wrestler_sounds
    wrestler.impact_sounds = wrestler_hit_sounds
    wrestler.death_sounds = ['wrestlerDeath']
    wrestler.pickup_sounds = wrestler_sounds
    wrestler.fall_sounds = ['wrestlerFall']
    wrestler.style = 'spaz'

    # OperaSinger ###################################
    gretel = Appearance('Gretel')
    gretel.base_appearance = None
    gretel.color_texture = 'operaSingerColor'
    gretel.color_mask_texture = 'operaSingerColorMask'
    gretel.default_color = (0.3, 0.5, 0.8)
    gretel.default_highlight = (1, 0, 0)
    gretel.icon_texture = 'operaSingerIcon'
    gretel.icon_mask_texture = 'operaSingerIconColorMask'
    gretel.head_model = 'operaSingerHead'
    gretel.torso_model = 'operaSingerTorso'
    gretel.pelvis_model = 'operaSingerPelvis'
    gretel.upper_arm_model = 'operaSingerUpperArm'
    gretel.forearm_model = 'operaSingerForeArm'
    gretel.hand_model = 'operaSingerHand'
    gretel.upper_leg_model = 'operaSingerUpperLeg'
    gretel.lower_leg_model = 'operaSingerLowerLeg'
    gretel.toes_model = 'operaSingerToes'
    opera_singer_sounds = [
        'operaSinger1', 'operaSinger2', 'operaSinger3', 'operaSinger4'
    ]
    opera_singer_hit_sounds = ['operaSingerHit1', 'operaSingerHit2']
    gretel.attack_sounds = opera_singer_sounds
    gretel.jump_sounds = opera_singer_sounds
    gretel.impact_sounds = opera_singer_hit_sounds
    gretel.death_sounds = ['operaSingerDeath']
    gretel.pickup_sounds = opera_singer_sounds
    gretel.fall_sounds = ['operaSingerFall']
    gretel.style = 'spaz'

    # Pixie ###################################
    pixie = Appearance('Pixel')
    pixie.base_appearance = None
    pixie.color_texture = 'pixieColor'
    pixie.color_mask_texture = 'pixieColorMask'
    pixie.default_color = (0, 1, 0.7)
    pixie.default_highlight = (0.65, 0.35, 0.75)
    pixie.icon_texture = 'pixieIcon'
    pixie.icon_mask_texture = 'pixieIconColorMask'
    pixie.head_model = 'pixieHead'
    pixie.torso_model = 'pixieTorso'
    pixie.pelvis_model = 'pixiePelvis'
    pixie.upper_arm_model = 'pixieUpperArm'
    pixie.forearm_model = 'pixieForeArm'
    pixie.hand_model = 'pixieHand'
    pixie.upper_leg_model = 'pixieUpperLeg'
    pixie.lower_leg_model = 'pixieLowerLeg'
    pixie.toes_model = 'pixieToes'
    pixie_sounds = ['pixie1', 'pixie2', 'pixie3', 'pixie4']
    pixie_hit_sounds = ['pixieHit1', 'pixieHit2']
    pixie.attack_sounds = pixie_sounds
    pixie.jump_sounds = pixie_sounds
    pixie.impact_sounds = pixie_hit_sounds
    pixie.death_sounds = ['pixieDeath']
    pixie.pickup_sounds = pixie_sounds
    pixie.fall_sounds = ['pixieFall']
    pixie.style = 'pixie'

    # Robot ###################################
    robot = Appearance('Robot')
    robot.base_appearance = None
    robot.color_texture = 'robotColor'
    robot.color_mask_texture = 'robotColorMask'
    robot.default_color = (0.3, 0.5, 0.8)
    robot.default_highlight = (1, 0, 0)
    robot.icon_texture = 'robotIcon'
    robot.icon_mask_texture = 'robotIconColorMask'
    robot.head_model = 'robotHead'
    robot.torso_model = 'robotTorso'
    robot.pelvis_model = 'robotPelvis'
    robot.upper_arm_model = 'robotUpperArm'
    robot.forearm_model = 'robotForeArm'
    robot.hand_model = 'robotHand'
    robot.upper_leg_model = 'robotUpperLeg'
    robot.lower_leg_model = 'robotLowerLeg'
    robot.toes_model = 'robotToes'
    robot_sounds = ['robot1', 'robot2', 'robot3', 'robot4']
    robot_hit_sounds = ['robotHit1', 'robotHit2']
    robot.attack_sounds = robot_sounds
    robot.jump_sounds = robot_sounds
    robot.impact_sounds = robot_hit_sounds
    robot.death_sounds = ['robotDeath']
    robot.pickup_sounds = robot_sounds
    robot.fall_sounds = ['robotFall']
    robot.style = 'spaz'

    # Bunny ###################################
    bunny = Appearance('Easter Bunny')
    bunny.base_appearance = None
    bunny.color_texture = 'bunnyColor'
    bunny.color_mask_texture = 'bunnyColorMask'
    bunny.default_color = (1, 1, 1)
    bunny.default_highlight = (1, 0.5, 0.5)
    bunny.icon_texture = 'bunnyIcon'
    bunny.icon_mask_texture = 'bunnyIconColorMask'
    bunny.head_model = 'bunnyHead'
    bunny.torso_model = 'bunnyTorso'
    bunny.pelvis_model = 'bunnyPelvis'
    bunny.upper_arm_model = 'bunnyUpperArm'
    bunny.forearm_model = 'bunnyForeArm'
    bunny.hand_model = 'bunnyHand'
    bunny.upper_leg_model = 'bunnyUpperLeg'
    bunny.lower_leg_model = 'bunnyLowerLeg'
    bunny.toes_model = 'bunnyToes'
    bunny_sounds = ['bunny1', 'bunny2', 'bunny3', 'bunny4']
    bunny_hit_sounds = ['bunnyHit1', 'bunnyHit2']
    bunny.attack_sounds = bunny_sounds
    bunny.jump_sounds = ['bunnyJump']
    bunny.impact_sounds = bunny_hit_sounds
    bunny.death_sounds = ['bunnyDeath']
    bunny.pickup_sounds = bunny_sounds
    bunny.fall_sounds = ['bunnyFall']
    bunny.style = 'bunny'
    
    # Sensei ##########################################
    sensei = Appearance('Master Serpent')
    sensei.base_appearance = ninja
    sensei.color_texture = 'ninjaColor'
    sensei.color_mask_texture = 'ninjaColorMask'
    sensei.default_color = (1, 1, 0)
    sensei.default_highlight = (1, 0.8, 0.5)
    sensei.icon_texture = 'masterSerpentIcon'
    sensei.icon_mask_texture = 'masterSerpentIconColorMask'
    sensei.head_model = 'samuraiHead'
    sensei.torso_model = 'samuraiTorso'
    sensei.pelvis_model = 'samuraiPelvis'
    sensei.upper_arm_model = 'samuraiUpperArm'
    sensei.forearm_model = 'samuraiForeArm'
    sensei.hand_model = 'samuraiHand'
    sensei.upper_leg_model = 'samuraiUpperLeg'
    sensei.lower_leg_model = 'samuraiLowerLeg'
    sensei.toes_model = 'samuraiToes'
    ninja_attacks = ['ninjaAttack' + str(i + 1) + '' for i in range(7)]
    ninja_hits = ['ninjaHit' + str(i + 1) + '' for i in range(8)]
    ninja_jumps = ['ninjaAttack' + str(i + 1) + '' for i in range(7)]
    sensei.jump_sounds = ninja_jumps
    sensei.attack_sounds = ninja_attacks
    sensei.impact_sounds = ninja_hits
    sensei.death_sounds = ['ninjaDeath1']
    sensei.pickup_sounds = ninja_attacks
    sensei.fall_sounds = ['ninjaFall1']
    sensei.style = 'ninja'
    
    # Stolt #######################################
    stolt = Appearance('Stolt')
    stolt.base_appearance = spaz
    stolt.color_texture = 'neoSpazColor'
    stolt.color_mask_texture = 'neoSpazColorMask'
    stolt.default_color = (1, 0.15, 0.15)
    stolt.default_highlight = (0.4, 0.05, 0.05)
    stolt.icon_texture = 'stoltIcon'
    stolt.icon_mask_texture = 'stoltIconColorMask'
    stolt.head_model = 'stoltHead'
    stolt.torso_model = 'stoltTorso'
    stolt.pelvis_model = 'stoltPelvis'
    stolt.upper_arm_model = 'stoltUpperArm'
    stolt.forearm_model = 'stoltForeArm'
    stolt.hand_model = 'stoltHand'
    stolt.upper_leg_model = 'stoltUpperLeg'
    stolt.lower_leg_model = 'stoltLowerLeg'
    stolt.toes_model = 'stoltToes'
    stolt.jump_sounds = ['stoltJump01', 'stoltJump02', 'stoltJump03', 'stoltJump04']
    stolt.attack_sounds = [
        'stoltAttack01', 'stoltAttack02', 'stoltAttack03', 'stoltAttack04'
    ]
    stolt.impact_sounds = [
        'stoltImpact01', 'stoltImpact02', 'stoltImpact03', 'stoltImpact04'
    ]
    stolt.death_sounds = ['stoltDeath01']
    stolt.pickup_sounds = ['stoltPickup01']
    stolt.fall_sounds = ['stoltFall01']
    stolt.style = 'kronk'
    
    # Waiter ###########################################
    melvin = Appearance('Melvin')
    melvin.base_appearance = mel
    melvin.color_texture = 'waiterColor'
    melvin.color_mask_texture = 'waiterColorMask'
    melvin.default_color = (0.13, 0.13, 0.13)
    melvin.default_highlight = (0.1, 0.6, 0.1)
    melvin.icon_texture = 'waiterIconColor'
    melvin.icon_mask_texture = 'waiterIconColorMask'
    melvin.head_model = 'waiterHead'
    melvin.torso_model = 'waiterTorso'
    melvin.pelvis_model = 'kronkPelvis'
    melvin.upper_arm_model = 'waiterUpperArm'
    melvin.forearm_model = 'waiterForeArm'
    melvin.hand_model = 'waiterHand'
    melvin.upper_leg_model = 'waiterUpperLeg'
    melvin.lower_leg_model = 'waiterLowerLeg'
    melvin.toes_model = 'waiterToes'
    mel_sounds = [
        'mel01', 'mel02', 'mel03', 'mel04', 'mel05', 'mel06', 'mel07', 'mel08',
        'mel09', 'mel10'
    ]
    melvin.attack_sounds = mel_sounds
    melvin.jump_sounds = mel_sounds
    melvin.impact_sounds = mel_sounds
    melvin.death_sounds = ['melDeath01']
    melvin.pickup_sounds = mel_sounds
    melvin.fall_sounds = ['melFall01']
    melvin.style = 'mel'
    
 # Cyber-Zoe #####################################
    z03 = Appearance('Z03 3000')
    z03.base_appearance = zoe
    z03.color_texture = 'cyborgColor'
    z03.color_mask_texture = 'cyborgColorMask'
    z03.default_color = (1, 1, 1)
    z03.default_highlight = (0.2, 1, 0.2)
    z03.icon_texture = 'cyberZoeIcon'
    z03.icon_mask_texture = 'cyberZoeIconColorMask'
    z03.head_model = 'cyberzoeHead'
    z03.torso_model = 'cyberzoeTorso'
    z03.pelvis_model = 'cyberzoePelvis'
    z03.upper_arm_model = 'cyberzoeUpperArm'
    z03.forearm_model = 'cyberzoeForeArm'
    z03.hand_model = 'cyberzoeHand'
    z03.upper_leg_model = 'cyberzoeUpperLeg'
    z03.lower_leg_model = 'cyberzoeLowerLeg'
    z03.toes_model = 'cyberzoeToes'
    z03.jump_sounds = ['cyberzoeJump01', 'cyberzoeJump02', 'cyberzoeJump03']
    z03.attack_sounds = [
        'cyberzoeAttack01', 'cyberzoeAttack02', 'cyberzoeAttack03', 'cyberzoeAttack04'
    ]
    z03.impact_sounds = [
        'cyberzoeImpact01', 'cyberzoeImpact02', 'cyberzoeImpact03', 'cyberzoeImpact04'
    ]
    z03.death_sounds = ['cyberzoeDeath01']
    z03.pickup_sounds = ['cyberzoePickup01']
    z03.fall_sounds = ['cyberzoeFall01']
    z03.style = 'cyborg'
    
 # Ye Olde Sparrow #######################################
    sparrow = Appearance('Ye Olde\' Sparrow')
    sparrow.base_appearance = jack
    sparrow.color_texture = 'yeOldeCptnColor'
    sparrow.color_mask_texture = 'jackColorMask'
    sparrow.default_color = (0.13, 0.13, 0.13)
    sparrow.default_highlight = (1, 1, 0)
    sparrow.icon_texture = 'yeOldeCptnIcon'
    sparrow.icon_mask_texture = 'yeOldeCptnIconColorMask'
    sparrow.head_model = 'yeOldeCptnHead'
    sparrow.torso_model = 'yeOldeCptnTorso'
    sparrow.pelvis_model = 'kronkPelvis'
    sparrow.upper_arm_model = 'jackUpperArm'
    sparrow.forearm_model = 'jackForeArm'
    sparrow.hand_model = 'yeOldeCptnHand'
    sparrow.upper_leg_model = 'jackUpperLeg'
    sparrow.lower_leg_model = 'jackLowerLeg'
    sparrow.toes_model = 'jackToes'
    hit_sounds = [
        'jackHit01', 'jackHit02', 'jackHit03', 'jackHit04', 'jackHit05',
        'jackHit06', 'jackHit07'
    ]
    sounds = ['jack01', 'jack02', 'jack03', 'jack04', 'jack05', 'jack06']
    sparrow.attack_sounds = sounds
    sparrow.jump_sounds = sounds
    sparrow.impact_sounds = hit_sounds
    sparrow.death_sounds = ['jackDeath01']
    sparrow.pickup_sounds = sounds
    sparrow.fall_sounds = ['jackFall01']
    sparrow.style = 'pirate'

 # Splash ###################################
    splash = Appearance("Splash")
    splash.base_appearance = None
    splash.color_texture = "splashColor"
    splash.color_mask_texture = "splashColorMask"
    splash.default_color = (0.2,1,0.2)
    splash.default_highlight = (1,1,0)
    splash.icon_texture = "splashIconColor"
    splash.icon_mask_texture = "splashIconColorMask"
    splash.head_model =     "zero"
    splash.torso_model =    "splashTorso"
    splash.pelvis_model =   "zero"
    splash.upper_arm_model = "zero"
    splash.forearm_model =  "zero"
    splash.hand_model =     "splashHand"
    splash.upper_leg_model = "zero"
    splash.lower_leg_model = "zero"
    splash.toes_model =     "splashToes"
    splash_sounds = ['splash1','splash2','splash3','splash4','splash5','splash6']
    splash.attack_sounds = splash_sounds
    splash.jump_sounds = splash_sounds
    splash.impact_sounds = splash_sounds
    splash.death_sounds = ["splashDeath"]
    splash.pickup_sounds = splash_sounds
    splash.fall_sounds = ["splashFall"]
    splash.style = 'ali'
    
 # Ronnie ###################################
    ronnie = Appearance("Ronnie")
    ronnie.base_appearance = None
    ronnie.color_texture = "ronnieColor"
    ronnie.color_mask_texture = "ronnieColorMask"
    ronnie.default_color = (1,1,1)
    ronnie.default_highlight = (0.5,0.25,1)
    ronnie.icon_texture = "ronnieIcon"
    ronnie.icon_mask_texture = "ronnieIconColorMask"
    ronnie.head_model =     "ronnieHead"
    ronnie.torso_model =    "ronnieTorso"
    ronnie.pelvis_model =   "aliPelvis"
    ronnie.upper_arm_model = "ronnieUpperArm"
    ronnie.forearm_model =  "ronnieForeArm"
    ronnie.hand_model =     "zero"
    ronnie.upper_leg_model = "ronnieUpperLeg"
    ronnie.lower_leg_model = "ronnieLowerLeg"
    ronnie.toes_model =     "ronnieToes"
    ronnie_sounds = ['ronnie1','ronnie2','ronnie3','ronnie4','ronnie5','ronnie6','ronnie7']
    ronnie.attack_sounds = ronnie_sounds
    ronnie.jump_sounds = ronnie_sounds
    ronnie.impact_sounds = ['ronnieHurt1','ronnieHurt2','ronnieHurt3','ronnieHurt4','ronnieHurt5']
    ronnie.death_sounds = ["ronnieDeath"]
    ronnie.pickup_sounds = ronnie_sounds
    ronnie.fall_sounds = ["ronnieFall"]
    ronnie.style = 'agent'
    
 # Super Kronk #####################################
    superkronk = Appearance('The Amazing Kronkman')
    superkronk.base_appearance = kronk
    superkronk.color_texture = 'superKronk'
    superkronk.color_mask_texture = 'superKronkColorMask'
    superkronk.default_color = (1, 0.15, 0.15)
    superkronk.default_highlight = (1, 1, 0)
    superkronk.icon_texture = 'superKronkIcon'
    superkronk.icon_mask_texture = 'superKronkIconColorMask'
    superkronk.head_model = 'superKronkHead'
    superkronk.torso_model = 'superKronkTorso'
    superkronk.pelvis_model = 'superKronkPelvis'
    superkronk.upper_arm_model = 'superKronkUpperArm'
    superkronk.forearm_model = 'superKronkForeArm'
    superkronk.hand_model = 'superKronkHand'
    superkronk.upper_leg_model = 'superKronkUpperLeg'
    superkronk.lower_leg_model = 'superKronkLowerLeg'
    superkronk.toes_model = 'superKronkToes'
    kronk_sounds = [
        'kronk1', 'kronk2', 'kronk3', 'kronk4', 'kronk5', 'kronk6', 'kronk7',
        'kronk8', 'kronk9', 'kronk10'
    ]
    superkronk.jump_sounds = kronk_sounds
    superkronk.attack_sounds = kronk_sounds
    superkronk.impact_sounds = kronk_sounds
    superkronk.death_sounds = ['kronkDeath']
    superkronk.pickup_sounds = kronk_sounds
    superkronk.fall_sounds = ['kronkFall']
    superkronk.style = 'kronk'

# Mictlan ###################################
    mictlan = Appearance("Mictlan")
    mictlan.base_appearance = None
    mictlan.color_texture = "mictlanColor"
    mictlan.color_mask_texture = "mictlanColorMask"
    mictlan.default_color = (0.1,0.1,1)
    mictlan.default_highlight = (0.1,0.1,0.5)
    mictlan.icon_texture = "mictlanIcon"
    mictlan.icon_mask_texture = "mictlanIconColorMask"
    mictlan.head_model =     "mictlanHead"
    mictlan.torso_model =    "mictlanTorso"
    mictlan.pelvis_model =   "mictlanPelvis"
    mictlan.upper_arm_model = "zero"
    mictlan.forearm_model =  "zero"
    mictlan.hand_model =     "mictlanHand"
    mictlan.upper_leg_model = "zero"
    mictlan.lower_leg_model = "zero"
    mictlan.toes_model =     "mictlanToes"
    mictlan_sounds = ['mictlan1','mictlan2','mictlan3','mictlan4','mictlan5','mictlan6']
    mictlan.attack_sounds = mictlan_sounds
    mictlan.jump_sounds = mictlan_sounds
    mictlan.impact_sounds = ['mictlanHurt1','mictlanHurt2','mictlanHurt3','mictlanHurt4','mictlanHurt5']
    mictlan.death_sounds = ["mictlanDeath"]
    mictlan.pickup_sounds = mictlan_sounds
    mictlan.fall_sounds = ["mictlanFall"]
    mictlan.style = 'ali'
    
# Dominic ###################################
    dominic = Appearance("Dominic")
    dominic.base_appearance = None
    dominic.color_texture = "domiColor"
    dominic.color_mask_texture = "domiColorMask"
    dominic.default_color = (1,0.8,0.5)
    dominic.default_highlight = (0.4,0.2,0.1)
    dominic.icon_texture = "dominicIcon"
    dominic.icon_mask_texture = "dominicIconColorMask"
    dominic.head_model =     "dominicHead"
    dominic.torso_model =    "dominicTorso"
    dominic.pelvis_model =   "dominicPelvis"
    dominic.upper_arm_model = "dominicUpperArm"
    dominic.forearm_model =  "dominicForeArm"
    dominic.hand_model =     "dominicHand"
    dominic.upper_leg_model = "dominicUpperLeg"
    dominic.lower_leg_model = "dominicLowerLeg"
    dominic.toes_model =     "dominicToes"
    ronnie_sounds = ['ronnie1','ronnie2','ronnie3','ronnie4','ronnie5','ronnie6','ronnie7']
    dominic.attack_sounds = ronnie_sounds
    dominic.jump_sounds = ronnie_sounds
    dominic.impact_sounds = ['ronnieHurt1','ronnieHurt2','ronnieHurt3','ronnieHurt4','ronnieHurt5']
    dominic.death_sounds = ["ronnieDeath"]
    dominic.pickup_sounds = ronnie_sounds
    dominic.fall_sounds = ["ronnieFall"]
    dominic.style = 'ninja'
 
  #2.0 VARIANTS!
  
# Soldat Spaz #######################################
    soldat = Appearance('Soldier Boy')
    soldat.base_appearance = spaz
    soldat.color_texture = 'soldatColor'
    soldat.color_mask_texture = 'soldatColorMask'
    soldat.default_color = (0.9, 0.5, 0.5)
    soldat.default_highlight = (1, 0.3, 0.5)
    soldat.icon_texture = 'soldatIcon'
    soldat.icon_mask_texture = 'soldatIconColorMask'
    soldat.head_model = 'soldatHead'
    soldat.torso_model = 'soldatTorso'
    soldat.pelvis_model = 'soldatPelvis'
    soldat.upper_arm_model = 'soldatUpperArm'
    soldat.forearm_model = 'neoSpazForeArm'
    soldat.hand_model = 'soldatHand'
    soldat.upper_leg_model = 'soldatUpperLeg'
    soldat.lower_leg_model = 'soldatLowerLeg'
    soldat.toes_model = 'neoSpazToes'
    ali_sounds = ['ali1', 'ali2', 'ali3', 'ali4']
    ali_hit_sounds = ['aliHit1', 'aliHit2', 'spazEff', 'spazOw']
    soldat.attack_sounds = ali_sounds
    soldat.jump_sounds = ali_sounds
    soldat.impact_sounds = ali_hit_sounds
    soldat.death_sounds = ['aliDeath']
    soldat.pickup_sounds = ali_sounds
    soldat.fall_sounds = ['aliFall']
    soldat.style = 'spaz'
    
# Burglar Shadow ##########################################
    sneakySnake = Appearance('Sneaky Snake')
    sneakySnake.base_appearance = ninja
    sneakySnake.color_texture = 'ninjaColor'
    sneakySnake.color_mask_texture = 'ninjaColorMask'
    sneakySnake.default_color = (0.1, 0.35, 0.1)
    sneakySnake.default_highlight = (0.2, 1, 0.2)
    sneakySnake.icon_texture = 'sneakySnakeIcon'
    sneakySnake.icon_mask_texture = 'sneakySnakeIconColorMask'
    sneakySnake.head_model = 'sneakySnakeHead'
    sneakySnake.torso_model = 'sneakySnakeTorso'
    sneakySnake.pelvis_model = 'sneakySnakePelvis'
    sneakySnake.upper_arm_model = 'sneakySnakeUpperArm'
    sneakySnake.forearm_model = 'sneakySnakeForeArm'
    sneakySnake.hand_model = 'sneakySnakeHand'
    sneakySnake.upper_leg_model = 'sneakySnakeUpperLeg'
    sneakySnake.lower_leg_model = 'sneakySnakeLowerLeg'
    sneakySnake.toes_model = 'sneakySnakeToes'
    ninja_attacks = ['ninjaAttack' + str(i + 1) + '' for i in range(7)]
    ninja_hits = ['ninjaHit' + str(i + 1) + '' for i in range(8)]
    ninja_jumps = ['ninjaAttack' + str(i + 1) + '' for i in range(7)]
    sneakySnake.jump_sounds = ninja_jumps
    sneakySnake.attack_sounds = ninja_attacks
    sneakySnake.impact_sounds = ninja_hits
    sneakySnake.death_sounds = ['ninjaDeath1']
    sneakySnake.pickup_sounds = ninja_attacks
    sneakySnake.fall_sounds = ['ninjaFall1']
    sneakySnake.style = 'spaz'

# Cook ###########################################
    melly = Appearance('Melly')
    melly.base_appearance = mel
    melly.color_texture = 'mellyColor'
    melly.color_mask_texture = 'mellyColorMask'
    melly.default_color = (0.4, 0.05, 0.05)
    melly.default_highlight = (0.02, 0.35, 0.21)
    melly.icon_texture = 'mellyIcon'
    melly.icon_mask_texture = 'mellyIconColorMask'
    melly.head_model = 'mellyHead'
    melly.torso_model = 'mellyTorso'
    melly.pelvis_model = 'kronkPelvis'
    melly.upper_arm_model = 'melUpperArm'
    melly.forearm_model = 'mellyForeArm'
    melly.hand_model = 'melHand'
    melly.upper_leg_model = 'melUpperLeg'
    melly.lower_leg_model = 'melLowerLeg'
    melly.toes_model = 'melToes'
    melly_sounds = [
        'melly01', 'melly02', 'melly03', 'melly04', 'melly05', 'melly06', 'melly07', 'melly08',
        'melly09', 'melly10'
    ]
    melly.attack_sounds = melly_sounds
    melly.jump_sounds = melly_sounds
    melly.impact_sounds = melly_sounds
    melly.death_sounds = ['mellyDeath']
    melly.pickup_sounds = melly_sounds
    melly.fall_sounds = ['mellyFall']
    melly.style = 'mel'
    
# Kronk the Gentleman #####################################
    kronk_noir = Appearance('Kronk Noir')
    kronk_noir.base_appearance = kronk
    kronk_noir.color_texture = 'kronkGentleColor'
    kronk_noir.color_mask_texture = 'kronkGentleColorMask'
    kronk_noir.default_color = (0.13, 0.13, 0.13)
    kronk_noir.default_highlight = (0.4, 0.2, 0.1)
    kronk_noir.icon_texture = 'kronkGentleIcon'
    kronk_noir.icon_mask_texture = 'kronkGentleIconColorMask'
    kronk_noir.head_model = 'kronkGentleHead'
    kronk_noir.torso_model = 'kronkTorso'
    kronk_noir.pelvis_model = 'kronkPelvis'
    kronk_noir.upper_arm_model = 'kronkUpperArm'
    kronk_noir.forearm_model = 'kronkForeArm'
    kronk_noir.hand_model = 'kronkHand'
    kronk_noir.upper_leg_model = 'kronkGentleUpperLeg'
    kronk_noir.lower_leg_model = 'kronkGentleLowerLeg'
    kronk_noir.toes_model = 'kronkToes'
    kronk_sounds = [
        'kronk1', 'kronk2', 'kronk3', 'kronk4', 'kronk5', 'kronk6', 'kronk7',
        'kronk8', 'kronk9', 'kronk10'
    ]
    kronk_noir.jump_sounds = kronk_sounds
    kronk_noir.attack_sounds = kronk_sounds
    kronk_noir.impact_sounds = kronk_sounds
    kronk_noir.death_sounds = ['kronkDeath']
    kronk_noir.pickup_sounds = kronk_sounds
    kronk_noir.fall_sounds = ['kronkFall']
    kronk_noir.style = 'kronk'
    
# Zoette ###################################
    zoette = Appearance('Zoette')
    zoette.base_appearance = zoe
    zoette.color_texture = 'zoeColor'
    zoette.color_mask_texture = 'zoeColorMask'
    zoette.default_color = (0.1, 0.35, 0.1)
    zoette.default_highlight = (0.1, 0.5, 0)
    zoette.icon_texture = 'zoetteIcon'
    zoette.icon_mask_texture = 'zoetteIconColorMask'
    zoette.head_model = 'zoiciaHead'
    zoette.torso_model = 'zoiciaTorso'
    zoette.pelvis_model = 'zoiciaPelvis'
    zoette.upper_arm_model = 'zoiciaUpperArm'
    zoette.forearm_model = 'zoiciaForeArm'
    zoette.hand_model = 'zoiciaHand'
    zoette.upper_leg_model = 'zoiciaUpperLeg'
    zoette.lower_leg_model = 'zoiciaLowerLeg'
    zoette.toes_model = 'zoiciaToes'
    zoette.jump_sounds = ['zoeJump01', 'zoeJump02', 'zoeJump03']
    zoette.attack_sounds = [
        'zoeAttack01', 'zoeAttack02', 'zoeAttack03', 'zoeAttack04'
    ]
    zoette.impact_sounds = [
        'zoeImpact01', 'zoeImpact02', 'zoeImpact03', 'zoeImpact04'
    ]
    zoette.death_sounds = ['zoeDeath01']
    zoette.pickup_sounds = ['zoePickup01']
    zoette.fall_sounds = ['zoeFall01']
    zoette.style = 'female'

# Jackie #######################################
    jackie = Appearance('Jackie Panty')
    jackie.base_appearance = jack
    jackie.color_texture = 'jackColor'
    jackie.color_mask_texture = 'jackColorMask'
    jackie.default_color = (0.5, 0.5, 0.5)
    jackie.default_highlight = (1, 1, 1)
    jackie.icon_texture = 'jackieIcon'
    jackie.icon_mask_texture = 'jackieIconColorMask'
    jackie.head_model = 'jackieHead'
    jackie.torso_model = 'jackieTorso'
    jackie.pelvis_model = 'kronkPelvis'
    jackie.upper_arm_model = 'jackieUpperArm'
    jackie.forearm_model = 'jackieForeArm'
    jackie.hand_model = 'jackHand'
    jackie.upper_leg_model = 'jackUpperLeg'
    jackie.lower_leg_model = 'jackLowerLeg'
    jackie.toes_model = 'jackToes'
    hit_sounds = [
        'jackHit01', 'jackHit02', 'jackHit03', 'jackHit04', 'jackHit05',
        'jackHit06', 'jackHit07'
    ]
    sounds = ['jack01', 'jack02', 'jack03', 'jack04', 'jack05', 'jack06']
    jackie.attack_sounds = sounds
    jackie.jump_sounds = sounds
    jackie.impact_sounds = hit_sounds
    jackie.death_sounds = ['jackDeath01']
    jackie.pickup_sounds = sounds
    jackie.fall_sounds = ['jackFall01']
    jackie.style = 'pirate'
    
# Steambot ###################################
    haze = Appearance('H4ZE')
    haze.base_appearance = None
    haze.color_texture = 'steambotColor'
    haze.color_mask_texture = 'steambotColorMask'
    haze.default_color = (0.5, 0.5, 0.5)
    haze.default_highlight = (1, 0, 0)
    haze.icon_texture = 'steamyIcon'
    haze.icon_mask_texture = 'steamyIconColorMask'
    haze.head_model = 'steamyHead'
    haze.torso_model = 'steamyTorso'
    haze.pelvis_model = 'steamyPelvis'
    haze.upper_arm_model = 'steamyUpperArm'
    haze.forearm_model = 'steamyForeArm'
    haze.hand_model = 'steamyHand'
    haze.upper_leg_model = 'zero'
    haze.lower_leg_model = 'zero'
    haze.toes_model = 'zero'
    haze_sounds = ['haze1', 'haze2', 'haze3', 'haze4']
    haze_hit_sounds = ['hazeHit1', 'hazeHit2']
    haze.attack_sounds = haze_sounds
    haze.jump_sounds = ['hazeJump']
    haze.impact_sounds = haze_hit_sounds
    haze.death_sounds = ['hazeDeath']
    haze.pickup_sounds = haze_sounds
    haze.fall_sounds = ['hazeFall']
    haze.style = 'cyborg'
    
# Toxic Spaz #######################################
    toxispaz = Appearance('Spazzy Toxicant')
    toxispaz.base_appearance = spaz
    toxispaz.color_texture = 'toxispazColor'
    toxispaz.color_mask_texture = 'toxiSpazColorMask'
    toxispaz.default_color = (0.49, 0.87, 0.45)
    toxispaz.default_highlight = (0.1, 0.35, 0.1)
    toxispaz.icon_texture = 'toxispazIcon'
    toxispaz.icon_mask_texture = 'toxispazIconColorMask'
    toxispaz.head_model = 'toxiSpazHead'
    toxispaz.torso_model = 'toxiSpazTorso'
    toxispaz.pelvis_model = 'toxiSpazPelvis'
    toxispaz.upper_arm_model = 'toxiSpazUpperArm'
    toxispaz.forearm_model = 'toxiSpazForeArm'
    toxispaz.hand_model = 'toxiSpazHand'
    toxispaz.upper_leg_model = 'toxiSpazUpperLeg'
    toxispaz.lower_leg_model = 'toxiSpazLowerLeg'
    toxispaz.toes_model = 'toxiSpazToes'
    toxispaz_sounds = ['toxispaz1', 'toxispaz2', 'toxispaz3', 'toxispaz4']
    toxispaz_hit_sounds = ['toxispazHit1', 'toxispazHit2', 'toxispazHit3', 'toxispazHit4', 'toxispazHit5', 'toxispazHit6']
    toxispaz.attack_sounds = toxispaz_sounds
    toxispaz.jump_sounds = toxispaz_sounds
    toxispaz.impact_sounds = toxispaz_hit_sounds
    toxispaz.death_sounds = ['toxispazDeath']
    toxispaz.pickup_sounds = toxispaz_sounds
    toxispaz.fall_sounds = ['toxispazFall']
    toxispaz.style = 'agent'

# Amigo ###################################
    amigo = Appearance("Amigo")
    amigo.base_appearance = None
    amigo.color_texture = "amigoColor"
    amigo.color_mask_texture = "amigoColorMask"
    amigo.default_color = (1,1,1)
    amigo.default_highlight = (0.5,0.15,0.15)
    amigo.icon_texture = "amigoIcon"
    amigo.icon_mask_texture = "amigoIconColorMask"
    amigo.head_model =     "amigoHead"
    amigo.torso_model =    "amigoTorso"
    amigo.pelvis_model =   "zero"
    amigo.upper_arm_model = "amigoUpperArm"
    amigo.forearm_model =  "amigoForeArm"
    amigo.hand_model =     "amigoHand"
    amigo.upper_leg_model = "amigoUpperLeg"
    amigo.lower_leg_model = "amigoLowerLeg"
    amigo.toes_model =     "amigoToes"
    amigo_sounds = ['amigo1','amigo2','amigo3','amigo4']
    amigo.attack_sounds = amigo_sounds
    amigo.jump_sounds = amigo_sounds
    amigo.impact_sounds = ['amigoHit1','amigoHit2','amigoHit3','amigoHit4']
    amigo.death_sounds = ["amigoDeath"]
    amigo.pickup_sounds = amigo_sounds
    amigo.fall_sounds = ["amigoFall"]
    amigo.style = 'agent'

# Helpy ###################################
    helpy = Appearance("Helpy")
    helpy.base_appearance = None
    helpy.color_texture = "helpyColor"
    helpy.color_mask_texture = "helpyColorMask"
    helpy.default_color = (1,1,1)
    helpy.default_highlight = (1,1,0)
    helpy.icon_texture = "helpyIcon"
    helpy.icon_mask_texture = "helpyIconColorMask"
    helpy.head_model =     "helpyHead"
    helpy.torso_model =    "helpyTorso"
    helpy.pelvis_model =   "zero"
    helpy.upper_arm_model = "zero"
    helpy.forearm_model =  "zero"
    helpy.hand_model =     "helpyHand"
    helpy.upper_leg_model = "zero"
    helpy.lower_leg_model = "zero"
    helpy.toes_model =     "helpyToes"
    helpy_sounds = ['helpy1', 'helpy2', 'helpy3']
    helpy.attack_sounds = helpy_sounds
    helpy.jump_sounds = helpy_sounds
    helpy.impact_sounds = ['helpyHit1', 'helpyHit2', 'helpyHit3', 'helpyHit4']
    helpy.death_sounds = ["helpyDeath"]
    helpy.pickup_sounds = helpy_sounds
    helpy.fall_sounds = ["helpyFall"]
    helpy.style = 'ali'

# Seagull ###################################
    seagull = Appearance('Spencer')
    seagull.base_appearance = None
    seagull.color_texture = 'seagullColor'
    seagull.color_mask_texture = 'seagullColorMask'
    seagull.default_color = (1, 1, 1)
    seagull.default_highlight = (0.13, 0.13, 0.13)
    seagull.icon_texture = 'seagullIcon'
    seagull.icon_mask_texture = 'seagullIconColorMask'
    seagull.head_model = 'seagullHead'
    seagull.torso_model = 'seagullTorso'
    seagull.pelvis_model = 'zero'
    seagull.upper_arm_model = 'seagullUpperArm'
    seagull.forearm_model = 'zero'
    seagull.hand_model = 'seagullHand'
    seagull.upper_leg_model = 'seagullUpperLeg'
    seagull.lower_leg_model = 'seagullLowerLeg'
    seagull.toes_model = 'seagullToes'
    penguin_sounds = ['penguin1', 'penguin2', 'penguin3', 'penguin4']
    penguin_hit_sounds = ['penguinHit1', 'penguinHit2']
    seagull.attack_sounds = penguin_sounds
    seagull.jump_sounds = penguin_sounds
    seagull.impact_sounds = penguin_hit_sounds
    seagull.death_sounds = ['penguinDeath']
    seagull.pickup_sounds = penguin_sounds
    seagull.fall_sounds = ['penguinFall']
    seagull.style = 'bear'

# Potato ###################################
    potato = Appearance("Crispin")
    potato.base_appearance = None
    potato.color_texture = "potatoColor"
    potato.color_mask_texture = "potatoColorMask"
    potato.default_color = (1,0.9,0.15)
    potato.default_highlight = (0.13,0.13,0.13)
    potato.icon_texture = "potatoIcon"
    potato.icon_mask_texture = "potatoIconColorMask"
    potato.head_model =     "zero"
    potato.torso_model =    "potatoTorso"
    potato.pelvis_model =   "zero"
    potato.upper_arm_model = "potatoUpperArm"
    potato.forearm_model =  "potatoForeArm"
    potato.hand_model =     "potatoHand"
    potato.upper_leg_model = "potatoUpperLeg"
    potato.lower_leg_model = "potatoLowerLeg"
    potato.toes_model =     "potatoToes"
    potato_sounds = ['potato1','potato2','potato3','potato4','potato5','potato6','potato7','potato8']
    potato.attack_sounds = potato_sounds
    potato.jump_sounds = potato_sounds
    potato.impact_sounds = potato_sounds
    potato.death_sounds = ["potatoDeath"]
    potato.pickup_sounds = potato_sounds
    potato.fall_sounds = ["potatoFall"]
    potato.style = 'agent'
    
#BSE CAMPAIGN REWARD! :D
    
# Oversilly ###################################
    oversilly = Appearance('Oversilly')
    oversilly.base_appearance = None
    oversilly.color_texture = 'oversillyColor'
    oversilly.color_mask_texture = 'oversillyColorMask'
    oversilly.default_color = (0.45, 0.8, 0.85)
    oversilly.default_highlight = (0.45, 0.8, 0.85)
    oversilly.icon_texture = 'oversillyIcon'
    oversilly.icon_mask_texture = 'oversillyIconColorMask'
    oversilly.head_model = 'oversillyHead'
    oversilly.torso_model = 'oversillyTorso'
    oversilly.pelvis_model = 'oversillyPelvis'
    oversilly.upper_arm_model = 'oversillyUpperArm'
    oversilly.forearm_model = 'oversillyForeArm'
    oversilly.hand_model = 'oversillyHand'
    oversilly.upper_leg_model = 'oversillyUpperLeg'
    oversilly.lower_leg_model = 'oversillyLowerLeg'
    oversilly.toes_model = 'overseerToes'
    oversilly_sounds = ['ali1', 'ali2', 'ali3', 'ali4']
    oversilly_hit_sounds = ['aliHit1', 'aliHit2']
    oversilly.attack_sounds = oversilly_sounds
    oversilly.jump_sounds = oversilly_sounds
    oversilly.impact_sounds = oversilly_hit_sounds
    oversilly.death_sounds = ['aliDeath']
    oversilly.pickup_sounds = oversilly_sounds
    oversilly.fall_sounds = ['aliFall']
    oversilly.style = 'spaz'