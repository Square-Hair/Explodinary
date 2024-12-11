""" Replaces the base game credits' back function to return to our BSE credits selection menu. """

from __future__ import annotations

import bauiv1 as bui
from bauiv1lib.creditslist import CreditsListWindow


class CreditsWrapper(CreditsListWindow):
    def _back(self) -> None:
        from bse.ui.credits.credits_menu import CreditsMenuWindow

        bui.containerwidget(
            edit=self._root_widget, transition=self._transition_out
        )
        assert bui.app.classic is not None
        bui.app.ui_v1.set_main_menu_window(
            CreditsMenuWindow(transition="in_left").get_root_widget()
        )


CreditsListWindow._back = CreditsWrapper._back
