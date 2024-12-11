""" A mainmenu wrapper that separates our main and pause menus. """

from __future__ import annotations

from typing import TYPE_CHECKING
import logging

import bauiv1 as bui
import bascenev1 as bs

if TYPE_CHECKING:
    from typing import Any, Callable

# Load our OG main menu UI & session.
from bauiv1lib import mainmenu as sourcemainmenu
from bascenev1lib.mainmenu import MainMenuSession

# Load our divided main & pause menus.
from bse.ui import mainmenu as claymainmenu, pausemenu as claypausemenu


def MenuHandler():
    """Wrapper that handles showing the proper menu according to current game state."""

    def wrapper(*args, **kwargs):
        # Show main menu if we're in the main menu session.
        if isinstance(
            bs.get_foreground_host_session(),
            MainMenuSession,
        ):
            return claymainmenu.MainMenuWindow(*args, **kwargs)
        # Else, return our custom-made pause menu.
        else:
            return claypausemenu.PauseMenuWindow(*args, **kwargs)

    return wrapper


# Override our default main menu class with our custom-made handler.
sourcemainmenu.MainMenuWindow = MenuHandler()
