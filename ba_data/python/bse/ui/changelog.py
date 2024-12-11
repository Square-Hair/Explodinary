# Released under the MIT License. See LICENSE for details.
#
"""Provides a window to display game credits."""

from __future__ import annotations

from typing import TYPE_CHECKING

import bauiv1 as bui

from bse._data import changelogs

changelogs_keys: list = []

for key in changelogs.changelogs.keys():
    changelogs_keys.append(key)


class ChangelogWindow(bui.Window):
    """Window for displaying game credits."""

    def __init__(self, origin_widget: bui.Widget | None = None):
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements
        import json

        bui.set_analytics_screen("Credits Window")

        self.sok_color = (0.1, 0.4, 0.3)

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
        self.width = width = 870 if uiscale is bui.UIScale.SMALL else 750
        self.height = height = 398 if uiscale is bui.UIScale.SMALL else 500
        x_inset = 100 if uiscale is bui.UIScale.SMALL else 0

        self._r = "explodinary.explodinaryChangelog"
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
            backbtn = bui.buttonwidget(
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
            bui.containerwidget(edit=self._root_widget, cancel_button=backbtn)

            backbtn = bui.buttonwidget(
                edit=backbtn,
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
                resource=self._r + ".titleText",
                subs=[("${APP_NAME}", bui.Lstr(resource="titleText"))],
            ),
            h_align="center",
            color=bui.app.ui_v1.title_color,
            maxwidth=330,
            v_align="center",
        )

        self._scr = scroll = bui.scrollwidget(
            parent=self._root_widget,
            color=(0.1, 0.85, 0.45),
            position=(40 + x_inset + (width * 0.05), 35),
            size=(width * 0.925 - (80 + 2 * x_inset), height - 100),
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

        self._csel = csel = -1 % len(changelogs_keys)
        txt = changelogs.changelogs[changelogs_keys[csel]]
        lines = txt.splitlines()
        line_height = 20

        scale = 0.55
        self._sub_width = width - 80
        self._sub_height = line_height * len(lines) + 40

        container = self._subcontainer = bui.containerwidget(
            parent=scroll,
            size=(width - 80, height),
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

        wlab = "<"
        y = height * 0.5 - 40
        m = width * (0.2 if uiscale is bui.UIScale.SMALL else 0.08)
        npos = (m - 45, y)
        self.navbtn: list = []
        for x in range(2):
            self.navbtn.append(
                bui.buttonwidget(
                    parent=self._root_widget,
                    position=npos,
                    size=(45, 80),
                    scale=1,
                    text_scale=1.2,
                    autoselect=True,
                    label=wlab,
                    on_activate_call=bui.Call(self._change_log, x),
                    color=(0.1, 0.85, 0.45),
                    textcolor=(0.6, 0.85, 0.71),
                )
            )
            npos = (width - m + 15, y)
            wlab = ">"

        bui.buttonwidget(edit=backbtn, down_widget=scroll)

        bui.widget(
            edit=scroll, left_widget=self.navbtn[0], right_widget=self.navbtn[1]
        )

        self._update_nav_btns()
        self.update()

    def _update_nav_btns(self) -> None:
        csel = self._csel
        for i, b in enumerate(self.navbtn):
            if (
                i == 0
                and csel == 0
                or i == 1
                and csel == len(changelogs_keys) - 1
            ):
                bui.buttonwidget(
                    edit=b,
                    color=(0.6, 0.6, 0.6),
                    textcolor=(0.9, 0.9, 0.9),
                )
            else:
                bui.buttonwidget(
                    edit=b,
                    color=(0.1, 0.85, 0.45),
                    textcolor=(0.6, 0.85, 0.71),
                )

    def update(self) -> None:
        for child in self._subcontainer.get_children():
            child.delete()

        csel = self._csel
        txt = changelogs.changelogs[changelogs_keys[csel]]
        lines = txt.splitlines()
        line_height = 20

        scale = 0.55
        self._sub_width = self.width - 80
        self._sub_height = line_height * len(lines) + 40

        bui.containerwidget(
            edit=self._subcontainer,
            size=(self._sub_width - 80, self._sub_height),
        )

        voffs = 0
        for line in lines:
            bui.textwidget(
                parent=self._subcontainer,
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

    def _change_log(self, v) -> None:
        self._csel = min(
            len(changelogs_keys) - 1, max(0, self._csel + (-1 if not v else v))
        )
        self._update_nav_btns()
        self.update()

    def _back(self) -> None:
        from bauiv1lib.mainmenu import MainMenuWindow

        bui.containerwidget(
            edit=self._root_widget, transition=self._transition_out
        )
        bui.app.ui_v1.set_main_menu_window(
            MainMenuWindow(transition="in_left").get_root_widget()
        )
