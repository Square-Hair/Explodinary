"""Nerd info. module."""

import bascenev1 as bs

explodinary: dict = {
    "version": "2.5",
    "title": "The Drip and Stylish Update (WIP)",
}
# We use a hash in the global modifier to ensure
# the score names are different when the official version ships
gb_sn = f"{hash(explodinary['title'])}"
sndata: dict = {  # internal scoreboard names
    "level": f"bse{gb_sn}l",
    "campaign": f"bse{gb_sn}c",
    "internal": f"bse{gb_sn}i",
}

bombsquad: dict = {
    "author": "Eric Froemling",
    "copyright": ["2011", "2024"],
}

MAX_PLAYLISTS = 30 + 70

# Default game type length
FFA_GAME_LENGTH = 24
TEAMS_GAME_LENGTH = 7
FFA_GAME_INCREMENT = 4
TEAMS_GAME_INCREMENT = 2

SERIES_DURATION = {"FFA": FFA_GAME_LENGTH, "Teams": TEAMS_GAME_LENGTH}
SERIES_INCREMENT = {"FFA": FFA_GAME_INCREMENT, "Teams": TEAMS_GAME_INCREMENT}

PLAYLIST_NAME_BLACKLIST = ["__default__", "__playlist_create__"]


def load_custom_series_length():
    """Load the user's custom series length."""
    bs.app.classic.ffa_series_length = clay.config.fetch(
        "FFA Series Length", SERIES_DURATION.get("FFA")
    )
    bs.app.classic.teams_series_length = clay.config.fetch(
        "Teams Series Length", SERIES_DURATION.get("Teams")
    )


def playlist_safety_checks():
    """Remove any bad playlists."""
    # Check all available playlist lists.
    for group in ["Free-for-All", "Team Tournament"]:
        for name, _ in bs.app.config.get(f"{group} Playlists", {}).items():
            # If a playlist name is in the list of
            # faulty names, remove it.
            if name in PLAYLIST_NAME_BLACKLIST:
                bs.app.plus.add_v1_account_transaction(
                    {
                        "type": "REMOVE_PLAYLIST",
                        "playlistType": group,
                        "playlistName": name,
                    }
                )
    # Run all transactions.
    bs.app.plus.run_v1_account_transactions()
