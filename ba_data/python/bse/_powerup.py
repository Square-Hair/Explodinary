"""TEMPORAL POWERUP DISTRIBUTIONS.
Remove this once the new bomb / powerup system rolls out here.
"""

def all_powerup_dists() -> set:
    """Get all the powerups!"""
    return {

        "Explodinary": [[
         ('triple_bombs', 3), ('ice_bombs', 3), ('punch', 1), ('fly_punch', 1), ('dash', 1),
         ('impact_bombs', 3), ('land_mines', 1), ('lite_mines', 1), ('flutter_mines', 1), ('glue_mines', 1), ('sticky_bombs', 3),
         ('tacky_bombs', 3), ('clouder_bombs', 3), ('steampunk_bombs', 2), ('cluster_bombs', 2), ('toxic_bombs', 2), ('vital_bombs', 1), ('shield', 1), ('present', 1), ('health', 1), ('curse', 1)
        ], "00"
        ],

        "Vanilla": [[
         ('triple_bombs', 3), ('ice_bombs', 3), ('punch', 1), ('fly_punch', 0), ('dash', 0),
         ('impact_bombs', 3), ('land_mines', 2), ('lite_mines', 0), ('flutter_mines', 0), ('glue_mines', 0), ('sticky_bombs', 3),
         ('tacky_bombs', 0), ('clouder_bombs', 0), ('steampunk_bombs', 0), ('cluster_bombs', 0),  ('toxic_bombs', 0), ('vital_bombs', 0), ('shield', 1), ('present', 0), ('health', 1), ('curse', 1)
        ], "01"
        ],

        "Simple": [[
         ('triple_bombs', 3), ('ice_bombs', 3), ('punch', 1), ('fly_punch', 0), ('dash', 0),
         ('impact_bombs', 3), ('land_mines', 2), ('lite_mines', 0), ('flutter_mines', 1), ('glue_mines', 0), ('sticky_bombs', 3),
         ('tacky_bombs', 3), ('clouder_bombs', 2), ('steampunk_bombs', 0), ('cluster_bombs', 0),  ('toxic_bombs', 0), ('vital_bombs', 0), ('shield', 1), ('present', 1), ('health', 1), ('curse', 1)
        ], "02"
        ],

        "Competitive": [[
         ('triple_bombs', 3), ('ice_bombs', 3), ('punch', 0), ('fly_punch', 1), ('dash', 1),
         ('impact_bombs', 3), ('land_mines', 2), ('lite_mines', 1), ('flutter_mines', 1), ('glue_mines', 1), ('sticky_bombs', 3),
         ('tacky_bombs', 3), ('clouder_bombs', 3), ('steampunk_bombs', 3), ('cluster_bombs', 1),  ('toxic_bombs', 2), ('vital_bombs', 1), ('shield', 0), ('present', 1), ('health', 0), ('curse', 0)
        ], "03"
        ],

        "Chaos": [[
         ('triple_bombs', 3), ('ice_bombs', 0), ('punch', 0), ('fly_punch', 0), ('dash', 0),
         ('impact_bombs', 0), ('land_mines', 0), ('lite_mines', 0), ('flutter_mines', 2), ('glue_mines', 2), ('sticky_bombs', 3),
         ('tacky_bombs', 3), ('clouder_bombs', 3), ('steampunk_bombs', 0), ('cluster_bombs', 0),  ('toxic_bombs', 0), ('vital_bombs', 0), ('shield', 0), ('present', 3), ('health', 0), ('curse', 1)
        ], "04"
        ],

        "No Powerups": [[
         ('triple_bombs', 0), ('ice_bombs', 0), ('punch', 0), ('fly_punch', 0), ('dash', 0),
         ('impact_bombs', 0), ('land_mines', 0), ('lite_mines', 0), ('flutter_mines', 0), ('glue_mines', 0), ('sticky_bombs', 0),
         ('tacky_bombs', 0), ('clouder_bombs', 0), ('steampunk_bombs', 0), ('cluster_bombs', 0),  ('toxic_bombs', 0), ('vital_bombs', 0), ('shield', 0), ('present', 0), ('health', 0), ('curse', 0)
        ], "05"
        ],

    }

def get_default_powerup_distribution() -> Sequence[tuple[str, int]]:
    """Standard set of powerups."""
    from ba._coopsession import CoopSession
    import ba

    all_dists = all_powerup_dists()
    try:
        if not isinstance(ba.getsession(), CoopSession):
            dist = all_dists.get(ba.app.config.get('BSE: Powerup Distribution', 'Explodinary'))[0]
        else:
            dist = all_dists.get('Explodinary')[0]
    except:
        dist = all_dists.get('Explodinary')[0]

    return dist