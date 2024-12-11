# Released under the MIT License. See LICENSE for details.
#
"""Provides a window to display game credits."""

from __future__ import annotations

from typing import TYPE_CHECKING

import bascenev1 as bs
import bauiv1 as bui

if TYPE_CHECKING:
    from typing import Sequence


class CreditsTestersWindow(bui.Window):
    """Window for displaying game credits."""

    def __init__(self, origin_widget: bui.Widget | None = None):
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements
        import json

        bui.set_analytics_screen("Credits BS Window")

        self.sok_color = (0.1, 0.4, 0.3)

        self._back_button: bui.Widget | None = None

        # PFPs
        self.breaker_tex = bui.gettexture("bse_pfpBreaker")
        self.corrolot_tex = bui.gettexture("bse_pfpCorro")
        self.davii_tex = bui.gettexture("bse_pfpDavii")
        self.nox_tex = bui.gettexture("bse_pfpNox")

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
        height = 398 if uiscale is bui.UIScale.SMALL else 500

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
            self._back_button = bui.buttonwidget(
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
            bui.containerwidget(
                edit=self._root_widget, cancel_button=self._back_button
            )

            bui.buttonwidget(
                edit=self._back_button,
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
            text=bui.Lstr(resource=f"{self._r}.btn.test"),
            h_align="center",
            color=bui.app.ui_v1.title_color,
            maxwidth=330,
            v_align="center",
        )

        scroll = bui.scrollwidget(
            parent=self._root_widget,
            color=(0.1, 0.85, 0.45),
            position=(40 + x_inset, 35),
            size=(width - (80 + 2 * x_inset), height - 100),
            capture_arrows=True,
        )

        if bui.app.ui_v1.use_toolbars:
            bui.widget(
                edit=scroll,
                right_widget=bui.internal.get_special_widget("party_button"),
            )
            if uiscale is bui.UIScale.SMALL:
                bui.widget(
                    edit=scroll,
                    left_widget=bui.internal.get_special_widget("back_button"),
                )

        credits_text = (
            "               \n"
            "               Breaker\n\n"
            "               Corrolot\n\n"
            "               Davii\n\n"
            "               Noxen\n\n"
        )

        txt = credits_text
        lines = txt.splitlines()
        line_height = 40

        scale = 1
        self._sub_width = width - 80
        self._sub_height = line_height * len(lines) + 40

        container = self._subcontainer = bui.containerwidget(
            parent=scroll,
            size=(self._sub_width, self._sub_height),
            background=False,
            claims_left_right=False,
            claims_tab=False,
        )

        voffs = 0
        for line in lines:
            bui.textwidget(
                parent=container,
                padding=4,
                color=(0.7, 0.9, 0.7, 1.0),
                scale=scale,
                flatness=1.0,
                size=(0, 0),
                position=(0, self._sub_height - 20 + voffs),
                h_align="left",
                v_align="top",
                text=bui.Lstr(value=line),
            )
            voffs -= line_height

        # Breaker
        bui.imagewidget(
            parent=container,
            position=(15, 300),
            size=(70, 70),
            texture=self.breaker_tex,
        )
        self._breakerYT_button = bui.buttonwidget(
            parent=container,
            position=(215, 310),
            color=(0.8, 0.3, 0.25),
            textcolor=(1, 1, 1),
            size=(100, 35),
            label="Youtube",
            on_activate_call=bui.Call(
                bui.open_url, "https://www.youtube.com/@breaker6501"
            ),
        )
        # Corrolot
        bui.imagewidget(
            parent=container,
            position=(15, 215),
            size=(70, 70),
            texture=self.corrolot_tex,
        )
        self._corroYT_button = bui.buttonwidget(
            parent=container,
            position=(215, 225),
            color=(0.8, 0.3, 0.25),
            textcolor=(1, 1, 1),
            size=(100, 35),
            label="Youtube",
            on_activate_call=bui.Call(
                bui.open_url, "https://www.youtube.com/@corrolot"
            ),
        )
        # Davii
        bui.imagewidget(
            parent=container,
            position=(15, 130),
            size=(70, 70),
            texture=self.davii_tex,
        )
        self._daviiYT_button = bui.buttonwidget(
            parent=container,
            position=(215, 150),
            color=(0.8, 0.3, 0.25),
            textcolor=(1, 1, 1),
            size=(100, 35),
            label="Youtube",
            on_activate_call=bui.Call(
                bui.open_url, "https://www.youtube.com/@DaviiWasTaken"
            ),
        )
        # Noxen
        bui.imagewidget(
            parent=container,
            position=(15, 45),
            size=(70, 70),
            texture=self.nox_tex,
        )
        self._noxYT_button = bui.buttonwidget(
            parent=container,
            position=(215, 65),
            color=(0.8, 0.3, 0.25),
            textcolor=(1, 1, 1),
            size=(100, 35),
            label="Youtube",
            on_activate_call=bui.Call(
                bui.open_url, "https://www.youtube.com/@NoxenZero"
            ),
        )

    def _back(self) -> None:
        # pylint: disable=cyclic-import
        from bse.ui.credits.creditslist_bse import CreditsBSEWindow

        bui.containerwidget(
            edit=self._root_widget, transition=self._transition_out
        )
        bui.app.ui_v1.set_main_menu_window(
            CreditsBSEWindow(transition="in_left").get_root_widget(),
            from_window=False
        )
