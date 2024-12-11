# Released under the MIT License. See LICENSE for details.
#
"""Provides a window to display game credits."""

from __future__ import annotations

from typing import TYPE_CHECKING

import bascenev1 as bs
import bauiv1 as bui


class CreditsBSEWindow(bui.Window):
    """Window for displaying game credits."""

    def __init__(
        self,
        transition: str = "in_right",
        origin_widget: bui.Widget | None = None,
    ):
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements

        bui.set_analytics_screen("Credits BSE Window")

        self.sok_color = (0.1, 0.4, 0.3)
        self.sok_text_color = (0.7, 0.9, 0.7, 1.0)

        # if they provided an origin-widget, scale up from that
        scale_origin: tuple[float, float] | None
        if origin_widget is not None:
            self._transition_out = "out_scale"
            scale_origin = origin_widget.get_screen_space_center()
            transition = "in_scale"
        else:
            self._transition_out = "out_right"
            scale_origin = None
            transition = "in_right"

        uiscale = bui.app.ui_v1.uiscale
        width = 870 if uiscale is bui.UIScale.SMALL else 670
        x_inset = 100 if uiscale is bui.UIScale.SMALL else 0
        height = 398

        self._r = "bseCredits"
        super().__init__(
            root_widget=bui.containerwidget(
                size=(width, height),
                transition=transition,
                color=self.sok_color,
                toolbar_visibility="menu_minimal",
                scale_origin_stack_offset=scale_origin,
                scale=(
                    2.0
                    if uiscale is bui.UIScale.SMALL
                    else 1.3 if uiscale is bui.UIScale.MEDIUM else 1.0
                ),
                stack_offset=(
                    (0, -8) if uiscale is bui.UIScale.SMALL else (0, 0)
                ),
            )
        )

        if bui.app.ui_v1.use_toolbars and uiscale is bui.UIScale.SMALL:
            bui.containerwidget(
                edit=self._root_widget, on_cancel_call=self._back
            )
        else:
            self._back_button = btn = bui.buttonwidget(
                parent=self._root_widget,
                position=(
                    40 + x_inset,
                    height - (68 if uiscale is bui.UIScale.SMALL else 62),
                ),
                size=(140, 60),
                scale=0.8,
                label=bui.Lstr(resource="backText"),
                button_type="back",
                on_activate_call=self._back,
                autoselect=True,
            )
            bui.containerwidget(edit=self._root_widget, cancel_button=btn)

            bui.buttonwidget(
                edit=btn,
                button_type="backSmall",
                position=(
                    40 + x_inset,
                    height - (68 if uiscale is bui.UIScale.SMALL else 62) + 5,
                ),
                size=(60, 48),
                label=bui.charstr(bui.SpecialChar.BACK),
            )

        bui.textwidget(
            parent=self._root_widget,
            position=(0, height - (59 if uiscale is bui.UIScale.SMALL else 54)),
            size=(width, 30),
            text=bui.Lstr(
                resource=f"{self._r}.title",
                subs=[("${APP_NAME}", bui.Lstr(resource="titleText"))],
            ),
            h_align="center",
            color=bui.app.ui_v1.title_color,
            maxwidth=330,
            v_align="center",
        )

        self.scroll = scroll = bui.scrollwidget(
            parent=self._root_widget,
            color=(0.1, 0.85, 0.45),
            position=(40 + x_inset, 35),
            size=(width - (80 + 2 * x_inset), height - 100),
            claims_left_right=True,
            capture_arrows=True,
        )

        lines = 2
        line_height = 20

        sw = self._sub_width = width - 80
        sh = self._sub_height = line_height * (lines) + 40

        sw = width - (80 + 2 * x_inset)

        self._subcontainer = bui.containerwidget(
            parent=scroll,
            size=(self._sub_width, self._sub_height),
            background=False,
            claims_left_right=True,
            claims_tab=True,
        )

        # Contributors
        self._contr_button = bui.buttonwidget(
            parent=self._subcontainer,
            position=((sw * 0.5) - (150 / 2), (-height + 100) + 150),
            autoselect=True,
            size=(150, 45),
            extra_touch_border_scale=0.1,
            label=bui.Lstr(resource=f"{self._r}.btn.cont"),
            text_scale=1.13,
            color=self.sok_color,
            on_activate_call=self._contributors,
        )
        # Testers
        self._test_button = bui.buttonwidget(
            parent=self._subcontainer,
            position=((sw * 0.5) - (150 / 2), (-height + 100) + 100),
            autoselect=True,
            size=(150, 45),
            extra_touch_border_scale=0.1,
            label=bui.Lstr(resource=f"{self._r}.btn.test"),
            text_scale=1,
            color=self.sok_color,
            on_activate_call=self._testers,
        )

        icoscl = 125

        fellas = {
            "SoK": {
                "mult": 0.2,
                "icon": bui.gettexture("bse_pfpSoK"),
                "desc": bui.Lstr(resource=f"{self._r}.desc00"),
                "ybut": "https://www.youtube.com/@sok05",
                "dbut": "https://www.buymeacoffee.com/sok05",
            },
            "Temp": {
                "mult": 1 - 0.2,
                "icon": bui.gettexture("bse_pfpTemp"),
                "desc": bui.Lstr(resource=f"{self._r}.desc01"),
                "ybut": "https://www.youtube.com/@trialtemp",
                "dbut": "https://paypal.me/3alTemp",
            },
        }

        itr = 0
        for fella, vars in fellas.items():
            bui.imagewidget(
                parent=self._subcontainer,
                position=((sw * vars["mult"]) - (icoscl / 2), -icoscl / 2),
                size=(icoscl, icoscl),
                texture=vars["icon"],
            )
            bui.textwidget(
                parent=self._subcontainer,
                position=(sw * vars["mult"], -60),
                size=(0, 0),
                text=fella,
                scale=1.75,
                res_scale=2.0,
                maxwidth=400,
                color=(1.1, 1.1, 1.1),
                h_align="center",
                v_align="center",
            )
            bui.textwidget(
                parent=self._subcontainer,
                position=(sw * vars["mult"], -90),
                size=(0, 0),
                text=vars["desc"],
                scale=0.6,
                res_scale=2.0,
                maxwidth=450,
                color=(1.1, 1.1, 1.1),
                h_align="center",
                v_align="center",
            )
            ytbtn = bui.buttonwidget(
                parent=self._subcontainer,
                autoselect=True,
                position=(
                    (sw * vars["mult"]) - (150 / 2),
                    (-height + 100) + 150,
                ),
                color=(0.8, 0.3, 0.25),
                textcolor=(1, 1, 1),
                size=(150, 45),
                label=bui.Lstr(resource=f"{self._r}.btn.yt"),
                on_activate_call=bui.Call(bui.open_url, vars["ybut"]),
            )
            dnbtn = bui.buttonwidget(
                parent=self._subcontainer,
                autoselect=True,
                position=(
                    (sw * vars["mult"]) - (150 / 2),
                    (-height + 100) + 100,
                ),
                color=(1, 0.85, 0),
                textcolor=(1, 1, 1),
                size=(150, 45),
                label=bui.Lstr(resource=f"{self._r}.btn.donate"),
                on_activate_call=bui.Call(bui.open_url, vars["dbut"]),
            )
            if itr == 0:
                bui.buttonwidget(
                    edit=self._back_button,
                    down_widget=ytbtn,
                )
            bui.buttonwidget(edit=ytbtn, up_widget=self._back_button)
            itr += 1

        bui.buttonwidget(edit=self._contr_button, up_widget=self._back_button)

        self._restore_state()

    def _get_states(self) -> None:
        """Returns a button and it's state.
        Used in _save_state & _restore_state"""
        return [
            (self.scroll, "scroll"),
            (self._back_button, "back"),
        ]

    def _save_state(self) -> None:
        sel = self._root_widget.get_selected_child()
        sel_name = None

        for button, state in self._get_states():
            if sel == button:
                sel_name = state
        if not sel_name:
            raise Exception(f'Selected button\'s save state not found: "{sel}"')

        # Try saving!
        try:
            bui.app.ui_v1.window_states[type(self)] = sel_name
        except Exception:
            bui.print_exception(
                f'Error saving state for "{self}" with "{sel} / {sel_name}".'
            )

    def _restore_state(self) -> None:
        sel_name = bui.app.ui_v1.window_states.get(type(self))
        sel = None

        for button, state in self._get_states():
            if sel_name == state:
                sel = button
        if not sel_name or not sel:
            sel_name = self._get_states()[0][1]

        # Try restoring!
        try:
            bui.containerwidget(edit=self._root_widget, selected_child=sel)
        except Exception:
            bui.print_exception(
                f'Error saving state for "{self}" with "{sel} / {sel_name}".'
            )

    def _contributors(self) -> None:
        # pylint: disable=cyclic-import
        from bse.ui.credits.credits_contributors import (
            CreditsContributorsWindow,
        )

        self._save_state()

        bui.containerwidget(edit=self._root_widget, transition="out_left")
        bui.app.ui_v1.set_main_menu_window(
            CreditsContributorsWindow(
                origin_widget=self._contr_button
            ).get_root_widget()
        )

    def _testers(self) -> None:
        # pylint: disable=cyclic-import
        from bse.ui.credits.credits_testers import CreditsTestersWindow

        self._save_state()

        bui.containerwidget(edit=self._root_widget, transition="out_left")
        bui.app.ui_v1.set_main_menu_window(
            CreditsTestersWindow(
                origin_widget=self._contr_button
            ).get_root_widget()
        )

    def _back(self) -> None:
        from bse.ui.credits.credits_menu import CreditsMenuWindow

        self._save_state()

        bui.containerwidget(
            edit=self._root_widget, transition=self._transition_out
        )
        bui.app.ui_v1.set_main_menu_window(
            CreditsMenuWindow(transition="in_left").get_root_widget()
        )
