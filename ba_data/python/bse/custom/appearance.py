""" A bulk of our custom made characters! """

from bascenev1lib.actor.spazappearance import Appearance

# Sensei ##########################################
t = Appearance("Master Serpent")

t.color_texture = "ninjaColor"
t.color_mask_texture = "ninjaColorMask"
t.default_color = (1, 1, 0)
t.default_highlight = (1, 0.8, 0.5)
t.icon_texture = "bse_masterSerpentIcon"
t.icon_mask_texture = "bse_masterSerpentIconColorMask"
t.head_mesh = "bse_samuraiHead"
t.torso_mesh = "bse_samuraiTorso"
t.pelvis_mesh = "bse_samuraiPelvis"
t.upper_arm_mesh = "bse_samuraiUpperArm"
t.forearm_mesh = "bse_samuraiForeArm"
t.hand_mesh = "bse_samuraiHand"
t.upper_leg_mesh = "bse_samuraiUpperLeg"
t.lower_leg_mesh = "bse_samuraiLowerLeg"
t.toes_mesh = "bse_samuraiToes"
ninja_attacks = ["ninjaAttack" + str(i + 1) + "" for i in range(7)]
ninja_hits = ["ninjaHit" + str(i + 1) + "" for i in range(8)]
ninja_jumps = ["ninjaAttack" + str(i + 1) + "" for i in range(7)]
t.jump_sounds = ninja_jumps
t.attack_sounds = ninja_attacks
t.impact_sounds = ninja_hits
t.death_sounds = ["ninjaDeath1"]
t.pickup_sounds = ninja_attacks
t.fall_sounds = ["ninjaFall1"]
t.style = "ninja"

# Stolt #######################################
t = Appearance("Stolt")

t.color_texture = "neoSpazColor"
t.color_mask_texture = "neoSpazColorMask"
t.default_color = (1, 0.15, 0.15)
t.default_highlight = (0.4, 0.05, 0.05)
t.icon_texture = "bse_stoltIcon"
t.icon_mask_texture = "bse_stoltIconColorMask"
t.head_mesh = "bse_stoltHead"
t.torso_mesh = "bse_stoltTorso"
t.pelvis_mesh = "bse_stoltPelvis"
t.upper_arm_mesh = "bse_stoltUpperArm"
t.forearm_mesh = "bse_stoltForeArm"
t.hand_mesh = "bse_stoltHand"
t.upper_leg_mesh = "bse_stoltUpperLeg"
t.lower_leg_mesh = "bse_stoltLowerLeg"
t.toes_mesh = "bse_stoltToes"
t.jump_sounds = [
    "bse_stoltJump01",
    "bse_stoltJump02",
    "bse_stoltJump03",
    "bse_stoltJump04",
]
t.attack_sounds = [
    "bse_stoltAttack01",
    "bse_stoltAttack02",
    "bse_stoltAttack03",
    "bse_stoltAttack04",
]
t.impact_sounds = [
    "bse_stoltImpact01",
    "bse_stoltImpact02",
    "bse_stoltImpact03",
    "bse_stoltImpact04",
]
t.death_sounds = ["bse_stoltDeath01"]
t.pickup_sounds = ["bse_stoltPickup01"]
t.fall_sounds = ["bse_stoltFall01"]
t.style = "kronk"

# Waiter ###########################################
t = Appearance("Melvin")

t.color_texture = "bse_waiterColor"
t.color_mask_texture = "bse_waiterColorMask"
t.default_color = (0.13, 0.13, 0.13)
t.default_highlight = (0.1, 0.6, 0.1)
t.icon_texture = "bse_waiterIconColor"
t.icon_mask_texture = "bse_waiterIconColorMask"
t.head_mesh = "bse_waiterHead"
t.torso_mesh = "bse_waiterTorso"
t.pelvis_mesh = "kronkPelvis"
t.upper_arm_mesh = "bse_waiterUpperArm"
t.forearm_mesh = "bse_waiterForeArm"
t.hand_mesh = "bse_waiterHand"
t.upper_leg_mesh = "bse_waiterUpperLeg"
t.lower_leg_mesh = "bse_waiterLowerLeg"
t.toes_mesh = "bse_waiterToes"
mel_sounds = [
    "mel01",
    "mel02",
    "mel03",
    "mel04",
    "mel05",
    "mel06",
    "mel07",
    "mel08",
    "mel09",
    "mel10",
]
t.attack_sounds = mel_sounds
t.jump_sounds = mel_sounds
t.impact_sounds = mel_sounds
t.death_sounds = ["melDeath01"]
t.pickup_sounds = mel_sounds
t.fall_sounds = ["melFall01"]
t.style = "mel"

# Cyber-Zoe #####################################
t = Appearance("Z03 3000")

t.color_texture = "cyborgColor"
t.color_mask_texture = "cyborgColorMask"
t.default_color = (1, 1, 1)
t.default_highlight = (0.2, 1, 0.2)
t.icon_texture = "bse_cyberZoeIcon"
t.icon_mask_texture = "bse_cyberZoeIconColorMask"
t.head_mesh = "bse_cyberzoeHead"
t.torso_mesh = "bse_cyberzoeTorso"
t.pelvis_mesh = "bse_cyberzoePelvis"
t.upper_arm_mesh = "bse_cyberzoeUpperArm"
t.forearm_mesh = "bse_cyberzoeForeArm"
t.hand_mesh = "bse_cyberzoeHand"
t.upper_leg_mesh = "bse_cyberzoeUpperLeg"
t.lower_leg_mesh = "bse_cyberzoeLowerLeg"
t.toes_mesh = "bse_cyberzoeToes"
t.jump_sounds = [
    "bse_cyberzoeJump01",
    "bse_cyberzoeJump02",
    "bse_cyberzoeJump03",
]
t.attack_sounds = [
    "bse_cyberzoeAttack01",
    "bse_cyberzoeAttack02",
    "bse_cyberzoeAttack03",
    "bse_cyberzoeAttack04",
]
t.impact_sounds = [
    "bse_cyberzoeImpact01",
    "bse_cyberzoeImpact02",
    "bse_cyberzoeImpact03",
    "bse_cyberzoeImpact04",
]
t.death_sounds = ["bse_cyberzoeDeath01"]
t.pickup_sounds = ["bse_cyberzoePickup01"]
t.fall_sounds = ["bse_cyberzoeFall01"]
t.style = "cyborg"

# Ye Olde Sparrow #######################################
t = Appearance("Ye Olde' Sparrow")

t.color_texture = "bse_yeOldeCptnColor"
t.color_mask_texture = "jackColorMask"
t.default_color = (0.13, 0.13, 0.13)
t.default_highlight = (1, 1, 0)
t.icon_texture = "bse_yeOldeCptnIcon"
t.icon_mask_texture = "bse_yeOldeCptnIconColorMask"
t.head_mesh = "bse_yeOldeCptnHead"
t.torso_mesh = "bse_yeOldeCptnTorso"
t.pelvis_mesh = "kronkPelvis"
t.upper_arm_mesh = "jackUpperArm"
t.forearm_mesh = "jackForeArm"
t.hand_mesh = "bse_yeOldeCptnHand"
t.upper_leg_mesh = "jackUpperLeg"
t.lower_leg_mesh = "jackLowerLeg"
t.toes_mesh = "jackToes"
hit_sounds = [
    "jackHit01",
    "jackHit02",
    "jackHit03",
    "jackHit04",
    "jackHit05",
    "jackHit06",
    "jackHit07",
]
sounds = ["jack01", "jack02", "jack03", "jack04", "jack05", "jack06"]
t.attack_sounds = sounds
t.jump_sounds = sounds
t.impact_sounds = hit_sounds
t.death_sounds = ["jackDeath01"]
t.pickup_sounds = sounds
t.fall_sounds = ["jackFall01"]
t.style = "pirate"

# Splash ###################################
t = Appearance("Splash")

t.color_texture = "bse_splashColor"
t.color_mask_texture = "bse_splashColorMask"
t.default_color = (0.2, 1, 0.2)
t.default_highlight = (1, 1, 0)
t.icon_texture = "bse_splashIconColor"
t.icon_mask_texture = "bse_splashIconColorMask"
t.head_mesh = "bse_zero"
t.torso_mesh = "bse_splashTorso"
t.pelvis_mesh = "bse_zero"
t.upper_arm_mesh = "bse_zero"
t.forearm_mesh = "bse_zero"
t.hand_mesh = "bse_splashHand"
t.upper_leg_mesh = "bse_zero"
t.lower_leg_mesh = "bse_zero"
t.toes_mesh = "bse_splashToes"
splash_sounds = [
    "bse_splash1",
    "bse_splash2",
    "bse_splash3",
    "bse_splash4",
    "bse_splash5",
    "bse_splash6",
]
t.attack_sounds = splash_sounds
t.jump_sounds = splash_sounds
t.impact_sounds = splash_sounds
t.death_sounds = ["bse_splashDeath"]
t.pickup_sounds = splash_sounds
t.fall_sounds = ["bse_splashFall"]
t.style = "ali"

# Ronnie ###################################
t = Appearance("Ronnie")

t.color_texture = "bse_ronnieColor"
t.color_mask_texture = "bse_ronnieColorMask"
t.default_color = (1, 1, 1)
t.default_highlight = (0.5, 0.25, 1)
t.icon_texture = "bse_ronnieIcon"
t.icon_mask_texture = "bse_ronnieIconColorMask"
t.head_mesh = "bse_ronnieHead"
t.torso_mesh = "bse_ronnieTorso"
t.pelvis_mesh = "aliPelvis"
t.upper_arm_mesh = "bse_ronnieUpperArm"
t.forearm_mesh = "bse_ronnieForeArm"
t.hand_mesh = "bse_zero"
t.upper_leg_mesh = "bse_ronnieUpperLeg"
t.lower_leg_mesh = "bse_ronnieLowerLeg"
t.toes_mesh = "bse_ronnieToes"
ronnie_sounds = [
    "bse_ronnie1",
    "bse_ronnie2",
    "bse_ronnie3",
    "bse_ronnie4",
    "bse_ronnie5",
    "bse_ronnie6",
    "bse_ronnie7",
]
t.attack_sounds = ronnie_sounds
t.jump_sounds = ronnie_sounds
t.impact_sounds = [
    "bse_ronnieHurt1",
    "bse_ronnieHurt2",
    "bse_ronnieHurt3",
    "bse_ronnieHurt4",
    "bse_ronnieHurt5",
]
t.death_sounds = ["bse_ronnieDeath"]
t.pickup_sounds = ronnie_sounds
t.fall_sounds = ["bse_ronnieFall"]
t.style = "agent"

# Super Kronk #####################################
t = Appearance("The Amazing Kronkman")

t.color_texture = "bse_superKronk"
t.color_mask_texture = "bse_superKronkColorMask"
t.default_color = (1, 0.15, 0.15)
t.default_highlight = (1, 1, 0)
t.icon_texture = "bse_superKronkIcon"
t.icon_mask_texture = "bse_superKronkIconColorMask"
t.head_mesh = "bse_superKronkHead"
t.torso_mesh = "bse_superKronkTorso"
t.pelvis_mesh = "bse_superKronkPelvis"
t.upper_arm_mesh = "bse_superKronkUpperArm"
t.forearm_mesh = "bse_superKronkForeArm"
t.hand_mesh = "bse_superKronkHand"
t.upper_leg_mesh = "bse_superKronkUpperLeg"
t.lower_leg_mesh = "bse_superKronkLowerLeg"
t.toes_mesh = "bse_superKronkToes"
kronk_sounds = [
    "kronk1",
    "kronk2",
    "kronk3",
    "kronk4",
    "kronk5",
    "kronk6",
    "kronk7",
    "kronk8",
    "kronk9",
    "kronk10",
]
t.jump_sounds = kronk_sounds
t.attack_sounds = kronk_sounds
t.impact_sounds = kronk_sounds
t.death_sounds = ["kronkDeath"]
t.pickup_sounds = kronk_sounds
t.fall_sounds = ["kronkFall"]
t.style = "kronk"

# Mictlan ###################################
t = Appearance("Mictlan")

t.color_texture = "bse_mictlanColor"
t.color_mask_texture = "bse_mictlanColorMask"
t.default_color = (0.1, 0.1, 1)
t.default_highlight = (0.1, 0.1, 0.5)
t.icon_texture = "bse_mictlanIcon"
t.icon_mask_texture = "bse_mictlanIconColorMask"
t.head_mesh = "bse_mictlanHead"
t.torso_mesh = "bse_mictlanTorso"
t.pelvis_mesh = "bse_mictlanPelvis"
t.upper_arm_mesh = "bse_zero"
t.forearm_mesh = "bse_zero"
t.hand_mesh = "bse_mictlanHand"
t.upper_leg_mesh = "bse_zero"
t.lower_leg_mesh = "bse_zero"
t.toes_mesh = "bse_mictlanToes"
mictlan_sounds = [
    "bse_mictlan1",
    "bse_mictlan2",
    "bse_mictlan3",
    "bse_mictlan4",
    "bse_mictlan5",
    "bse_mictlan6",
]
t.attack_sounds = mictlan_sounds
t.jump_sounds = mictlan_sounds
t.impact_sounds = [
    "bse_mictlanHurt1",
    "bse_mictlanHurt2",
    "bse_mictlanHurt3",
    "bse_mictlanHurt4",
    "bse_mictlanHurt5",
]
t.death_sounds = ["bse_mictlanDeath"]
t.pickup_sounds = mictlan_sounds
t.fall_sounds = ["bse_mictlanFall"]
t.style = "ali"

# Dominic ###################################
t = Appearance("Dominic")

t.color_texture = "bse_domiColor"
t.color_mask_texture = "bse_domiColorMask"
t.default_color = (1, 0.8, 0.5)
t.default_highlight = (0.4, 0.2, 0.1)
t.icon_texture = "bse_dominicIcon"
t.icon_mask_texture = "bse_dominicIconColorMask"
t.head_mesh = "bse_dominicHead"
t.torso_mesh = "bse_dominicTorso"
t.pelvis_mesh = "bse_dominicPelvis"
t.upper_arm_mesh = "bse_dominicUpperArm"
t.forearm_mesh = "bse_dominicForeArm"
t.hand_mesh = "bse_dominicHand"
t.upper_leg_mesh = "bse_dominicUpperLeg"
t.lower_leg_mesh = "bse_dominicLowerLeg"
t.toes_mesh = "bse_dominicToes"
ronnie_sounds = [
    "bse_ronnie1",
    "bse_ronnie2",
    "bse_ronnie3",
    "bse_ronnie4",
    "bse_ronnie5",
    "bse_ronnie6",
    "bse_ronnie7",
]
t.attack_sounds = ronnie_sounds
t.jump_sounds = ronnie_sounds
t.impact_sounds = [
    "bse_ronnieHurt1",
    "bse_ronnieHurt2",
    "bse_ronnieHurt3",
    "bse_ronnieHurt4",
    "bse_ronnieHurt5",
]
t.death_sounds = ["bse_ronnieDeath"]
t.pickup_sounds = ronnie_sounds
t.fall_sounds = ["bse_ronnieFall"]
t.style = "ninja"

# Soldat Spaz #######################################
t = Appearance("Soldier Boy")

t.color_texture = "bse_soldatColor"
t.color_mask_texture = "bse_soldatColorMask"
t.default_color = (0.9, 0.5, 0.5)
t.default_highlight = (1, 0.3, 0.5)
t.icon_texture = "bse_soldatIcon"
t.icon_mask_texture = "bse_soldatIconColorMask"
t.head_mesh = "bse_soldatHead"
t.torso_mesh = "bse_soldatTorso"
t.pelvis_mesh = "bse_soldatPelvis"
t.upper_arm_mesh = "bse_soldatUpperArm"
t.forearm_mesh = "neoSpazForeArm"
t.hand_mesh = "bse_soldatHand"
t.upper_leg_mesh = "bse_soldatUpperLeg"
t.lower_leg_mesh = "bse_soldatLowerLeg"
t.toes_mesh = "neoSpazToes"
ali_sounds = ["ali1", "ali2", "ali3", "ali4"]
ali_hit_sounds = ["aliHit1", "aliHit2", "spazEff", "spazOw"]
t.attack_sounds = ali_sounds
t.jump_sounds = ali_sounds
t.impact_sounds = ali_hit_sounds
t.death_sounds = ["aliDeath"]
t.pickup_sounds = ali_sounds
t.fall_sounds = ["aliFall"]
t.style = "spaz"

# Burglar Shadow ##########################################
t = Appearance("Sneaky Snake")

t.color_texture = "ninjaColor"
t.color_mask_texture = "ninjaColorMask"
t.default_color = (0.1, 0.35, 0.1)
t.default_highlight = (0.2, 1, 0.2)
t.icon_texture = "bse_sneakySnakeIcon"
t.icon_mask_texture = "bse_sneakySnakeIconColorMask"
t.head_mesh = "bse_sneakySnakeHead"
t.torso_mesh = "bse_sneakySnakeTorso"
t.pelvis_mesh = "bse_sneakySnakePelvis"
t.upper_arm_mesh = "bse_sneakySnakeUpperArm"
t.forearm_mesh = "bse_sneakySnakeForeArm"
t.hand_mesh = "bse_sneakySnakeHand"
t.upper_leg_mesh = "bse_sneakySnakeUpperLeg"
t.lower_leg_mesh = "bse_sneakySnakeLowerLeg"
t.toes_mesh = "bse_sneakySnakeToes"
ninja_attacks = ["ninjaAttack" + str(i + 1) + "" for i in range(7)]
ninja_hits = ["ninjaHit" + str(i + 1) + "" for i in range(8)]
ninja_jumps = ["ninjaAttack" + str(i + 1) + "" for i in range(7)]
t.jump_sounds = ninja_jumps
t.attack_sounds = ninja_attacks
t.impact_sounds = ninja_hits
t.death_sounds = ["ninjaDeath1"]
t.pickup_sounds = ninja_attacks
t.fall_sounds = ["ninjaFall1"]
t.style = "spaz"

# Cook ###########################################
t = Appearance("Melly")

t.color_texture = "bse_mellyColor"
t.color_mask_texture = "bse_mellyColorMask"
t.default_color = (0.4, 0.05, 0.05)
t.default_highlight = (0.02, 0.35, 0.21)
t.icon_texture = "bse_mellyIcon"
t.icon_mask_texture = "bse_mellyIconColorMask"
t.head_mesh = "bse_mellyHead"
t.torso_mesh = "bse_mellyTorso"
t.pelvis_mesh = "kronkPelvis"
t.upper_arm_mesh = "melUpperArm"
t.forearm_mesh = "bse_mellyForeArm"
t.hand_mesh = "melHand"
t.upper_leg_mesh = "melUpperLeg"
t.lower_leg_mesh = "melLowerLeg"
t.toes_mesh = "melToes"
melly_sounds = [
    "bse_melly01",
    "bse_melly02",
    "bse_melly03",
    "bse_melly04",
    "bse_melly05",
    "bse_melly06",
    "bse_melly07",
    "bse_melly08",
    "bse_melly09",
    "bse_melly10",
]
t.attack_sounds = melly_sounds
t.jump_sounds = melly_sounds
t.impact_sounds = melly_sounds
t.death_sounds = ["bse_mellyDeath"]
t.pickup_sounds = melly_sounds
t.fall_sounds = ["bse_mellyFall"]
t.style = "mel"

# Kronk the Gentleman #####################################
t = Appearance("Kronk Noir")

t.color_texture = "bse_kronkGentleColor"
t.color_mask_texture = "bse_kronkGentleColorMask"
t.default_color = (0.13, 0.13, 0.13)
t.default_highlight = (0.4, 0.2, 0.1)
t.icon_texture = "bse_kronkGentleIcon"
t.icon_mask_texture = "bse_kronkGentleIconColorMask"
t.head_mesh = "bse_kronkGentleHead"
t.torso_mesh = "kronkTorso"
t.pelvis_mesh = "kronkPelvis"
t.upper_arm_mesh = "kronkUpperArm"
t.forearm_mesh = "kronkForeArm"
t.hand_mesh = "kronkHand"
t.upper_leg_mesh = "bse_kronkGentleUpperLeg"
t.lower_leg_mesh = "bse_kronkGentleLowerLeg"
t.toes_mesh = "kronkToes"
kronk_sounds = [
    "kronk1",
    "kronk2",
    "kronk3",
    "kronk4",
    "kronk5",
    "kronk6",
    "kronk7",
    "kronk8",
    "kronk9",
    "kronk10",
]
t.jump_sounds = kronk_sounds
t.attack_sounds = kronk_sounds
t.impact_sounds = kronk_sounds
t.death_sounds = ["kronkDeath"]
t.pickup_sounds = kronk_sounds
t.fall_sounds = ["kronkFall"]
t.style = "kronk"

# Zoette ###################################
t = Appearance("Zoette")

t.color_texture = "zoeColor"
t.color_mask_texture = "zoeColorMask"
t.default_color = (0.1, 0.35, 0.1)
t.default_highlight = (0.1, 0.5, 0)
t.icon_texture = "bse_zoetteIcon"
t.icon_mask_texture = "bse_zoetteIconColorMask"
t.head_mesh = "bse_zoiciaHead"
t.torso_mesh = "bse_zoiciaTorso"
t.pelvis_mesh = "bse_zoiciaPelvis"
t.upper_arm_mesh = "bse_zoiciaUpperArm"
t.forearm_mesh = "bse_zoiciaForeArm"
t.hand_mesh = "bse_zoiciaHand"
t.upper_leg_mesh = "bse_zoiciaUpperLeg"
t.lower_leg_mesh = "bse_zoiciaLowerLeg"
t.toes_mesh = "bse_zoiciaToes"
t.jump_sounds = ["zoeJump01", "zoeJump02", "zoeJump03"]
t.attack_sounds = ["zoeAttack01", "zoeAttack02", "zoeAttack03", "zoeAttack04"]
t.impact_sounds = ["zoeImpact01", "zoeImpact02", "zoeImpact03", "zoeImpact04"]
t.death_sounds = ["zoeDeath01"]
t.pickup_sounds = ["zoePickup01"]
t.fall_sounds = ["zoeFall01"]
t.style = "female"

# Jackie #######################################
t = Appearance("Jackie Panty")

t.color_texture = "jackColor"
t.color_mask_texture = "jackColorMask"
t.default_color = (0.5, 0.5, 0.5)
t.default_highlight = (1, 1, 1)
t.icon_texture = "bse_jackieIcon"
t.icon_mask_texture = "bse_jackieIconColorMask"
t.head_mesh = "bse_jackieHead"
t.torso_mesh = "bse_jackieTorso"
t.pelvis_mesh = "kronkPelvis"
t.upper_arm_mesh = "bse_jackieUpperArm"
t.forearm_mesh = "bse_jackieForeArm"
t.hand_mesh = "jackHand"
t.upper_leg_mesh = "jackUpperLeg"
t.lower_leg_mesh = "jackLowerLeg"
t.toes_mesh = "jackToes"
hit_sounds = [
    "jackHit01",
    "jackHit02",
    "jackHit03",
    "jackHit04",
    "jackHit05",
    "jackHit06",
    "jackHit07",
]
sounds = ["jack01", "jack02", "jack03", "jack04", "jack05", "jack06"]
t.attack_sounds = sounds
t.jump_sounds = sounds
t.impact_sounds = hit_sounds
t.death_sounds = ["jackDeath01"]
t.pickup_sounds = sounds
t.fall_sounds = ["jackFall01"]
t.style = "pirate"

# Steambot ###################################
t = Appearance("H4ZE")

t.color_texture = "bse_steambotColor"
t.color_mask_texture = "bse_steambotColorMask"
t.default_color = (0.5, 0.5, 0.5)
t.default_highlight = (1, 0, 0)
t.icon_texture = "bse_steamyIcon"
t.icon_mask_texture = "bse_steamyIconColorMask"
t.head_mesh = "bse_steamyHead"
t.torso_mesh = "bse_steamyTorso"
t.pelvis_mesh = "bse_steamyPelvis"
t.upper_arm_mesh = "bse_steamyUpperArm"
t.forearm_mesh = "bse_steamyForeArm"
t.hand_mesh = "bse_steamyHand"
t.upper_leg_mesh = "bse_zero"
t.lower_leg_mesh = "bse_zero"
t.toes_mesh = "bse_zero"
haze_sounds = ["bse_haze1", "bse_haze2", "bse_haze3", "bse_haze4"]
haze_hit_sounds = ["bse_hazeHit1", "bse_hazeHit2"]
t.attack_sounds = haze_sounds
t.jump_sounds = ["bse_hazeJump"]
t.impact_sounds = haze_hit_sounds
t.death_sounds = ["bse_hazeDeath"]
t.pickup_sounds = haze_sounds
t.fall_sounds = ["bse_hazeFall"]
t.style = "cyborg"

# Toxic Spaz #######################################
t = Appearance("Spazzy Toxicant")

t.color_texture = "bse_toxispazColor"
t.color_mask_texture = "bse_toxiSpazColorMask"
t.default_color = (0.49, 0.87, 0.45)
t.default_highlight = (0.1, 0.35, 0.1)
t.icon_texture = "bse_toxispazIcon"
t.icon_mask_texture = "bse_toxispazIconColorMask"
t.head_mesh = "bse_toxiSpazHead"
t.torso_mesh = "bse_toxiSpazTorso"
t.pelvis_mesh = "bse_toxiSpazPelvis"
t.upper_arm_mesh = "bse_toxiSpazUpperArm"
t.forearm_mesh = "bse_toxiSpazForeArm"
t.hand_mesh = "bse_toxiSpazHand"
t.upper_leg_mesh = "bse_toxiSpazUpperLeg"
t.lower_leg_mesh = "bse_toxiSpazLowerLeg"
t.toes_mesh = "bse_toxiSpazToes"
toxispaz_sounds = [
    "bse_toxispaz1",
    "bse_toxispaz2",
    "bse_toxispaz3",
    "bse_toxispaz4",
]
toxispaz_hit_sounds = [
    "bse_toxispazHit1",
    "bse_toxispazHit2",
    "bse_toxispazHit3",
    "bse_toxispazHit4",
    "bse_toxispazHit5",
    "bse_toxispazHit6",
]
t.attack_sounds = toxispaz_sounds
t.jump_sounds = toxispaz_sounds
t.impact_sounds = toxispaz_hit_sounds
t.death_sounds = ["bse_toxispazDeath"]
t.pickup_sounds = toxispaz_sounds
t.fall_sounds = ["bse_toxispazFall"]
t.style = "agent"

# Amigo ###################################
t = Appearance("Amigo")

t.color_texture = "bse_amigoColor"
t.color_mask_texture = "bse_amigoColorMask"
t.default_color = (1, 1, 1)
t.default_highlight = (0.5, 0.15, 0.15)
t.icon_texture = "bse_amigoIcon"
t.icon_mask_texture = "bse_amigoIconColorMask"
t.head_mesh = "bse_amigoHead"
t.torso_mesh = "bse_amigoTorso"
t.pelvis_mesh = "bse_zero"
t.upper_arm_mesh = "bse_amigoUpperArm"
t.forearm_mesh = "bse_amigoForeArm"
t.hand_mesh = "bse_amigoHand"
t.upper_leg_mesh = "bse_amigoUpperLeg"
t.lower_leg_mesh = "bse_amigoLowerLeg"
t.toes_mesh = "bse_amigoToes"
amigo_sounds = ["bse_amigo1", "bse_amigo2", "bse_amigo3", "bse_amigo4"]
t.attack_sounds = amigo_sounds
t.jump_sounds = amigo_sounds
t.impact_sounds = [
    "bse_amigoHit1",
    "bse_amigoHit2",
    "bse_amigoHit3",
    "bse_amigoHit4",
]
t.death_sounds = ["bse_amigoDeath"]
t.pickup_sounds = amigo_sounds
t.fall_sounds = ["bse_amigoFall"]
t.style = "agent"

# Helpy ###################################
t = Appearance("Helpy")

t.color_texture = "bse_helpyColor"
t.color_mask_texture = "bse_helpyColorMask"
t.default_color = (1, 1, 1)
t.default_highlight = (1, 1, 0)
t.icon_texture = "bse_helpyIcon"
t.icon_mask_texture = "bse_helpyIconColorMask"
t.head_mesh = "bse_helpyHead"
t.torso_mesh = "bse_helpyTorso"
t.pelvis_mesh = "bse_zero"
t.upper_arm_mesh = "bse_zero"
t.forearm_mesh = "bse_zero"
t.hand_mesh = "bse_helpyHand"
t.upper_leg_mesh = "bse_zero"
t.lower_leg_mesh = "bse_zero"
t.toes_mesh = "bse_helpyToes"
helpy_sounds = ["bse_helpy1", "bse_helpy2", "bse_helpy3"]
t.attack_sounds = helpy_sounds
t.jump_sounds = helpy_sounds
t.impact_sounds = [
    "bse_helpyHit1",
    "bse_helpyHit2",
    "bse_helpyHit3",
    "bse_helpyHit4",
]
t.death_sounds = ["bse_helpyDeath"]
t.pickup_sounds = helpy_sounds
t.fall_sounds = ["bse_helpyFall"]
t.style = "ali"

# Seagull ###################################
t = Appearance("Spencer")

t.color_texture = "bse_seagullColor"
t.color_mask_texture = "bse_seagullColorMask"
t.default_color = (1, 1, 1)
t.default_highlight = (0.13, 0.13, 0.13)
t.icon_texture = "bse_seagullIcon"
t.icon_mask_texture = "bse_seagullIconColorMask"
t.head_mesh = "bse_seagullHead"
t.torso_mesh = "bse_seagullTorso"
t.pelvis_mesh = "bse_zero"
t.upper_arm_mesh = "bse_seagullUpperArm"
t.forearm_mesh = "bse_zero"
t.hand_mesh = "bse_seagullHand"
t.upper_leg_mesh = "bse_seagullUpperLeg"
t.lower_leg_mesh = "bse_seagullLowerLeg"
t.toes_mesh = "bse_seagullToes"
penguin_sounds = ["penguin1", "penguin2", "penguin3", "penguin4"]
penguin_hit_sounds = ["penguinHit1", "penguinHit2"]
t.attack_sounds = penguin_sounds
t.jump_sounds = penguin_sounds
t.impact_sounds = penguin_hit_sounds
t.death_sounds = ["penguinDeath"]
t.pickup_sounds = penguin_sounds
t.fall_sounds = ["penguinFall"]
t.style = "bear"

# Potato ###################################
t = Appearance("Crispin")

t.color_texture = "bse_potatoColor"
t.color_mask_texture = "bse_potatoColorMask"
t.default_color = (1, 0.9, 0.15)
t.default_highlight = (0.13, 0.13, 0.13)
t.icon_texture = "bse_potatoIcon"
t.icon_mask_texture = "bse_potatoIconColorMask"
t.head_mesh = "bse_zero"
t.torso_mesh = "bse_potatoTorso"
t.pelvis_mesh = "bse_zero"
t.upper_arm_mesh = "bse_potatoUpperArm"
t.forearm_mesh = "bse_potatoForeArm"
t.hand_mesh = "bse_potatoHand"
t.upper_leg_mesh = "bse_potatoUpperLeg"
t.lower_leg_mesh = "bse_potatoLowerLeg"
t.toes_mesh = "bse_potatoToes"
potato_sounds = [
    "bse_potato1",
    "bse_potato2",
    "bse_potato3",
    "bse_potato4",
    "bse_potato5",
    "bse_potato6",
    "bse_potato7",
    "bse_potato8",
]
t.attack_sounds = potato_sounds
t.jump_sounds = potato_sounds
t.impact_sounds = potato_sounds
t.death_sounds = ["bse_potatoDeath"]
t.pickup_sounds = potato_sounds
t.fall_sounds = ["bse_potatoFall"]
t.style = "agent"

# Oversilly ###################################
t = Appearance("Oversilly")

t.color_texture = "bse_oversillyColor"
t.color_mask_texture = "bse_oversillyColorMask"
t.default_color = (0.45, 0.8, 0.85)
t.default_highlight = (0.45, 0.8, 0.85)
t.icon_texture = "bse_oversillyIcon"
t.icon_mask_texture = "bse_oversillyIconColorMask"
t.head_mesh = "bse_oversillyHead"
t.torso_mesh = "bse_oversillyTorso"
t.pelvis_mesh = "bse_oversillyPelvis"
t.upper_arm_mesh = "bse_oversillyUpperArm"
t.forearm_mesh = "bse_oversillyForeArm"
t.hand_mesh = "bse_oversillyHand"
t.upper_leg_mesh = "bse_oversillyUpperLeg"
t.lower_leg_mesh = "bse_oversillyLowerLeg"
t.toes_mesh = "bse_overseerToes"
oversilly_sounds = ["ali1", "ali2", "ali3", "ali4"]
oversilly_hit_sounds = ["aliHit1", "aliHit2"]
t.attack_sounds = oversilly_sounds
t.jump_sounds = oversilly_sounds
t.impact_sounds = oversilly_hit_sounds
t.death_sounds = ["aliDeath"]
t.pickup_sounds = oversilly_sounds
t.fall_sounds = ["aliFall"]
t.style = "spaz"

"""
'get_appearances' overwrite.
Lock some of our characters by replacing the 'get_appearances' function to be just like before!
TEMP;NOTE: Would've done a wrapper here but handling the original list plus our custom one is a bit of a hassle.
           Reconsider doing this in the future though for mod crosscompatibility! (Foreshadowing) 
"""


def explodinary_get_appearances(include_locked: bool = False) -> list[str]:
    """Get the list of available spaz appearances ft. Explodinary."""
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-branches
    import bascenev1 as bs

    plus = bs.app.plus
    assert plus is not None

    assert bs.app.classic is not None
    get_purchased = plus.get_purchased
    disallowed = []
    if not include_locked:
        # Hmm yeah this'll be tough to hack...
        if not get_purchased("characters.santa"):
            disallowed.append("Santa Claus")
        if not get_purchased("characters.frosty"):
            disallowed.append("Frosty")
        if not get_purchased("characters.bones"):
            disallowed.append("Bones")
        if not get_purchased("characters.bernard"):
            disallowed.append("Bernard")
        if not get_purchased("characters.pixie"):
            disallowed.append("Pixel")
        if not get_purchased("characters.pascal"):
            disallowed.append("Pascal")
        if not get_purchased("characters.actionhero"):
            disallowed.append("Todd McBurton")
        if not get_purchased("characters.taobaomascot"):
            disallowed.append("Taobao Mascot")
        if not get_purchased("characters.agent"):
            disallowed.append("Agent Johnson")
        if not get_purchased("characters.jumpsuit"):
            disallowed.append("Lee")
        if not get_purchased("characters.assassin"):
            disallowed.append("Zola")
        if not get_purchased("characters.wizard"):
            disallowed.append("Grumbledorf")
        if not get_purchased("characters.cowboy"):
            disallowed.append("Butch")
        if not get_purchased("characters.witch"):
            disallowed.append("Witch")
        if not get_purchased("characters.warrior"):
            disallowed.append("Warrior")
        if not get_purchased("characters.superhero"):
            disallowed.append("Middle-Man")
        if not get_purchased("characters.alien"):
            disallowed.append("Alien")
        if not get_purchased("characters.oldlady"):
            disallowed.append("OldLady")
        if not get_purchased("characters.gladiator"):
            disallowed.append("Gladiator")
        if not get_purchased("characters.wrestler"):
            disallowed.append("Wrestler")
        if not get_purchased("characters.operasinger"):
            disallowed.append("Gretel")
        if not get_purchased("characters.robot"):
            disallowed.append("Robot")
        if not get_purchased("characters.cyborg"):
            disallowed.append("B-9000")
        if not get_purchased("characters.bunny"):
            disallowed.append("Easter Bunny")
        if not get_purchased("characters.kronk"):
            disallowed.append("Kronk")
        if not get_purchased("characters.zoe"):
            disallowed.append("Zoe")
        if not get_purchased("characters.jackmorgan"):
            disallowed.append("Jack Morgan")
        if not get_purchased("characters.mel"):
            disallowed.append("Mel")
        if not get_purchased("characters.snakeshadow"):
            disallowed.append("Snake Shadow")

        # Explodinary Specials
        if not bs.app.config.get("BSE: Oversilly Oversillier", False):
            disallowed.append("Oversilly")
        if not bs.app.config.get("BSE: Adios Amigo", False):
            disallowed.append("Amigo")
        if not get_purchased("characters.helpy_bse"):
            disallowed.append("Helpy")
        if not get_purchased("characters.amigo_bse"):
            disallowed.append("Spencer")
        # Bosbone addon
        if not get_purchased("characters.bones"):
            disallowed.append("Bosbone")

    return [
        s
        for s in list(bs.app.classic.spaz_appearances.keys())
        if s not in disallowed
    ]


from bascenev1lib.actor import spazappearance

spazappearance.get_appearances = explodinary_get_appearances
