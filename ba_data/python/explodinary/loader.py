from explodinary.game import (
    explodinaryOnslaught, explodinaryRunaround,
    kablooyaOnslaught, kablooyaRunaround, pathwayPandemonium,
    routeRoulette, timeyBombnuts, hub
)
from bastd.game import (
    arms_race, soccer, rockethell
)

from explodinary.campaign import (
    the_beginning, beyond_the_grotto, mysterious_swamp, alpine_gateway, 
    mount_chill, hot_air_havoc, blockland, confrontation, bomb_poem
)

import ba
from explodinary.custom import quickturn

# Deprecated: from bastd.ui import quick_game

# Hey, Temp here.
# This section recreates the user's plugin list, removing the previous plugin iterations
# If this didn't exist, a bunch of errors would print. It's nothing harmful but pretty silly that
# the game doesn't do this check by itself whenever a former plugin doesn't plugin anymore

did_a_thing = False

new_plugin_list = ba.app.config['Plugins'].copy()

for i,v in enumerate(ba.app.config['Plugins']):
    if v in [
            'bastd.actor.quickturn.MikiWavedashTest',
            'bastd.game.timeyBombnuts.TimeyBombnutsLevel',
            'bastd.game.explodinaryOnslaught.ExplodinaryOnslaughtLevel',
            'bastd.game.explodinaryRunaround.ExplodinaryInfiniteRunaroundLevel',
            'bastd.game.routeRoulette.RouteRouletteLevel',
            'bastd.game.kablooyaOnslaught.KablooyaOnslaughtLevel',
            'bastd.game.kablooyaRunaround.KablooyaRunaroundLevel',
            'explodinary.game.pathwayPandemonium.PathwayPandemoniumLevel',
            'bastd.game.arms_race.ArmsRaceGame',
            'bastd.ui.quick_game.QuickGamePlugin'
            ]:
        del new_plugin_list[v]
        did_a_thing = True

if did_a_thing:
    ba.app.config['Plugins'] = new_plugin_list
    ba.app.config.commit()

# It ends here bwap

bse_practice: list = [
    ['Timey Bombnuts',              timeyBombnuts.TimeyBombnutsGame,                        {'preset': 'endless'},  'treePreview' ], 
    ['BSE Infinite Onslaught',      explodinaryOnslaught.ExplodinaryOnslaughtGame,          {'preset': 'endless'},  'onslaughtArenaPreview' ], 
    ['BSE Infinite Runaround',      explodinaryRunaround.ExplodinaryInfiniteRunaroundGame,  {'preset': 'endless'},  'explRunaroundPreview'  ],
    ['Route Roulette',              routeRoulette.RouteRouletteGame,                        {'preset': 'endless'},  'roulettePreview'       ],
    ['Pathway Pandemonium',         pathwayPandemonium.PathwayPandemoniumGame,              {'preset': 'endless'},  'pathwayPreview'        ],
    ['Kablooya Onslaught',          kablooyaOnslaught.KablooyaOnslaughtGame,                {'preset': 'kablooya'}, 'kablooyaPreview'       ],
    ['Endless Kablooya Onslaught',  kablooyaOnslaught.EndlessKablooyaOnslaughtGame,         {'preset': 'endless'},  'kablooyaEndlessPreview'],
    ['Kablooya Runaround',          kablooyaRunaround.KablooyaRunaroundGame,                {'preset': 'uber'},     'towerSPreview'         ],
    ['Endless Kablooya Runaround',  kablooyaRunaround.EndlessKablooyaRunaroundGame,         {'preset': 'endless'},  'endlessTowerSPreview'  ],
]

bse_campaign: list = [
    ['The Beginning',               the_beginning.TheBeginningGame,                         {},                     'theBeginningPreview'   ],
    ['Mysterious Swamp',            mysterious_swamp.MysteriousSwampGame,                   {},                     'swampPreview'          ],
    ['Beyond The Grotto',           beyond_the_grotto.GrottoGame,                           {},                     'grottoPreview'         ],
    ['Alpine Gateway',              alpine_gateway.AlpineGatewayGame,                       {},                     'alpinePreview'         ],
    ['Mount Chill',                 mount_chill.MountChillGame,                             {},                     'mountChillPreview'     ],
    ['Hot Air Havoc',               hot_air_havoc.HotAirHavocGame,                          {},                     'hotAirPreview'         ],
    ['Blockland',                   blockland.BlocklandGame,                                {},                     'blocklandPreview'      ],
    ['Eyes Of The Abyss',           confrontation.ConfrontationGame,                        {},                     'confrontationPreview'  ],
    [' ',                           bomb_poem.BombPoemGame,                                 {},                     'confrontationPreview'  ],
]

bse_extras: list = [
    ['Hub',                         hub.HubGame,                                            {},                     'oversillyIcon'         ],
]

from explodinary import _versiondata
from ba._campaign import register_campaign, Campaign
    
# Practice row modes
_custom_levels, custom_levels = ([],[])
for campaign in [bse_practice]:
    # Append all levels from our campaign lists to the practice level list
    for level in campaign:
        _custom_levels.append(
            ba.Level(
                level[0],
                gametype                =   level[1],
                settings                =   level[2],
                preview_texture_name    =   level[3]
            )
        )
        custom_levels.append(f'{_versiondata.levelsub}:{level[0]}')
        
    # Register campaign with all levels!!
    register_campaign(
        Campaign(
            f'{_versiondata.levelsub}',
            sequential=False,
            levels=_custom_levels,
        )
    )

# Campaign levels
_campaign_levels, campaign_levels = ([],[])
for campaign in [bse_campaign]:
    # Add all our levels into a list before making our custom campaign
    for level in campaign:
        _campaign_levels.append(
            ba.Level(
                level[0],
                gametype                =   level[1],
                settings                =   level[2],
                preview_texture_name    =   level[3]
            )
        )
        campaign_levels.append(f'{_versiondata.campaignsub}:{level[0]}')

    # Register campaign with all levels!!
    register_campaign(
        Campaign(
            _versiondata.campaignsub,
            levels=_campaign_levels,
        )
    )

# Internal modes
_internal_levels, internal_levels = ([],[])
for campaign in [bse_extras]:
    # Add all our levels into a list before making our custom campaign
    for level in campaign:
        _internal_levels.append(
            ba.Level(
                level[0],
                gametype                =   level[1],
                settings                =   level[2],
                preview_texture_name    =   level[3]
            )
        )
        internal_levels.append(f'{_versiondata.internalsub}:{level[0]}')

    # Register campaign with all levels!!
    register_campaign(
        Campaign(
            _versiondata.internalsub,
            levels=_internal_levels
        )
    )
    
from explodinary.lib import bseconfig
# Build our new config dicts
bseconfig._create_bse_config()
bseconfig._build_chaos_settings()