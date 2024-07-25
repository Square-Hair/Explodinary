""" A module containing all the game's bots. """

import bascenev1lib.actor.spazbot as vanillabots
import bse.custom.spazbot as bsebots
import bse.custom.bsespazbot as bsecbots

# Vanilla bots
vanilla = [
    vanillabots.SpazBot, vanillabots.BomberBot, vanillabots.BomberBotLite, vanillabots.BomberBotStaticLite, 
    vanillabots.BomberBotStatic, vanillabots.BomberBotPro, vanillabots.BomberBotProShielded, vanillabots.BomberBotProStatic, 
    vanillabots.BomberBotProStaticShielded, vanillabots.BrawlerBot, vanillabots.BrawlerBotLite, vanillabots.BrawlerBotPro, 
    vanillabots.BrawlerBotProShielded, vanillabots.ChargerBot, vanillabots.BouncyBot, vanillabots.ChargerBotPro, 
    vanillabots.ChargerBotProShielded, vanillabots.TriggerBot, vanillabots.TriggerBotStatic, vanillabots.TriggerBotPro,
    vanillabots.TriggerBotProShielded, vanillabots.StickyBot, vanillabots.StickyBotStatic, vanillabots.ExplodeyBot,
    vanillabots.ExplodeyBotNoTimeLimit, vanillabots.ExplodeyBotShielded, 
]
# BSE bots
bse_generic = [
    bsebots.ToxicBot, bsebots.NoirBot, bsebots.StickyBotPro, bsebots.MellyBot, bsebots.WaiterBot, bsebots.WaiterBotPro,
    bsebots.WaiterBotProShielded, bsebots.FrostyBot, bsebots.   ExplodeyBotNoTimeLimitSlow, bsebots.SantaBot, bsebots.SantaBotPro,
    bsebots.MicBot, bsebots.MicBotPro, bsebots.SplashBot, bsebots.SoldatBot,
]
# BSE 1st Campaign bots
bse_campaign = [
    bsecbots.SpazBot, bsecbots.BomberBot, bsecbots.BomberBotLite, bsecbots.BomberBotStaticLite, bsecbots.BomberBotStatic, bsecbots.BomberBotPro,
    bsecbots.BomberBotProShielded, bsecbots.BomberBotProStatic, bsecbots.BomberBotProStaticShielded, bsecbots.ToxicBot, bsecbots.BrawlerBot,
    bsecbots.BrawlerBotLite, bsecbots.GolemBot, bsecbots.BrawlerBotPro, bsecbots.BrawlerBotProShielded, bsecbots.NoirBot, bsecbots.ChargerBot,
    bsecbots.BouncyBot, bsecbots.ChargerBotPro, bsecbots.ChargerBotProShielded, bsecbots.TriggerBot, bsecbots.TriggerBotStatic, bsecbots.TriggerBotPro,
    bsecbots.TriggerBotProShielded, bsecbots.StickyBot, bsecbots.StickyBotPro, bsecbots.MellyBot, bsecbots.WaiterBot, bsecbots.WaiterBotPro,
    bsecbots.WaiterBotProShielded,bsecbots.FrostyBot, bsecbots.FrostyBotPro, bsecbots.FrostyBotProShielded, bsecbots.FrostyBotStatic,
    bsecbots.StickyBotStatic, bsecbots.ExplodeyBot, bsecbots.ExplodeyBotNoTimeLimit, bsecbots.ExplodeyBotShielded, bsecbots.SantaBot,
    bsecbots.SantaBotPro, bsecbots.MicBot, bsecbots.MicBotPro, bsecbots.SplashBot, bsecbots.SoldatBot, bsecbots.OverseerBot, bsecbots.OverseerClone,
]

all = []

# Add all bots from previous lists to this one.
for botlist in [vanilla, bse_generic, bse_campaign]:
    all.extend(botlist)