"""Ui wrappers to overwrite vanilla ones.
We do this to keep them sort of mod friendly, allowing them to be
modified by third parties and plugins later on."""
from __future__ import annotations

import bauiv1 as bui
import bascenev1 as bs

# settings window
import bauiv1lib.settings.allsettings
import bse.ui.settings.allsettings
bauiv1lib.settings.allsettings.AllSettingsWindow = (
    bse.ui.settings.allsettings.AllSettingsWindow
)

# main & pause menu
from bauiv1lib import mainmenu as sourcemainmenu
from bascenev1lib.mainmenu import MainMenuSession
from bse.ui import mainmenu as claymainmenu, pausemenu as claypausemenu

def MenuHandler():
    """Menu divider, opens main menu in menu and pause menu mid-game."""
    def wrapper(*args, **kwargs):
        # main menu
        if isinstance(
            bs.get_foreground_host_session(),
            MainMenuSession,
        ):
            return claymainmenu.MainMenuWindow(*args, **kwargs)
        # midgame
        else:
            return claypausemenu.PauseMenuWindow(*args, **kwargs)
    return wrapper
# run our function over the main menu window one
sourcemainmenu.MainMenuWindow = MenuHandler()

# credits
from bauiv1lib.creditslist import CreditsListWindow
class CreditsWrapper(CreditsListWindow):
    """Back button wrapper."""
    def _back(self) -> None:
        from bse.ui.credits.credits_menu import CreditsMenuWindow

        bui.containerwidget(
            edit=self._root_widget, transition=self._transition_out
        )
        assert bui.app.classic is not None
        bui.app.ui_v1.set_main_menu_window(
            CreditsMenuWindow(transition="in_left").get_root_widget(),
            from_window=False
        )
CreditsListWindow._back = CreditsWrapper._back

# play
from bauiv1lib import play as sourceplaywindow
from bse.ui.play import PlayWindow
sourceplaywindow.PlayWindow = PlayWindow