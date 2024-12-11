# Released under the MIT License. See LICENSE for details.
#
"""Provides the top level play window."""

from __future__ import annotations

import bascenev1 as bs
import bauiv1 as bui

quick_config = bs.app.config.get(
    "quick_game_button", {"selected": None, "config": {}}
)


class CreditsMenuWindow(bui.Window):
    """Window for selecting overall play type."""

    def __init__(
        self,
        transition: str = "in_right",
        origin_widget: bui.Widget | None = None,
    ):
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-locals
        import threading

        # Preload some modules we use in a background thread so we won't
        # have a visual hitch when the user taps them.
        threading.Thread(target=self._preload_modules).start()

        # We can currently be used either for main menu duty or for selecting
        # playlists (should make this more elegant/general).
        self._is_main_menu = not bui.app.ui_v1.selecting_private_party_playlist
        self.sok_color = (0.1, 0.85, 0.45)
        self.sok_color2 = (0.1, 0.4, 0.3)
        self.sok_color3 = (0.9, 0.8, 0.25)
        uiscale = bui.app.ui_v1.uiscale
        width = 800 if uiscale is bui.UIScale.SMALL else 600
        x_offs = 100 if uiscale is bui.UIScale.SMALL else 0
        height = 400
        height2 = 265
        button_width = 400
        button_width2 = 200

        scale_origin: tuple[float, float] | None
        if origin_widget is not None:
            self._transition_out = "out_scale"
            scale_origin = origin_widget.get_screen_space_center()
            transition = "in_scale"
        else:
            self._transition_out = "out_right"
            scale_origin = None

        self._r = "explodinary.credits"

        super().__init__(
            root_widget=bui.containerwidget(
                size=(width, height),
                transition=transition,
                toolbar_visibility="menu_full",
                scale_origin_stack_offset=scale_origin,
                scale=(
                    1.6
                    if uiscale is bui.UIScale.SMALL
                    else 0.9 if uiscale is bui.UIScale.MEDIUM else 0.8
                ),
                stack_offset=(0, 0) if uiscale is bui.UIScale.SMALL else (0, 0),
            )
        )
        self._back_button = back_button = btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(55 + x_offs, height - 132),
            size=(120, 60),
            scale=1.1,
            color=self.sok_color3,
            text_res_scale=1.5,
            text_scale=1.2,
            autoselect=True,
            label=bui.Lstr(resource="backText"),
            button_type="back",
        )

        txt = bui.textwidget(
            parent=self._root_widget,
            position=(width * 0.515, height - 101),
            # position=(width * 0.5, height -
            #           (101 if main_menu else 61)),
            size=(0, 0),
            text=bui.Lstr(resource=f"{self._r}.title"),
            scale=1.7,
            res_scale=2.0,
            maxwidth=400,
            color=bui.app.ui_v1.heading_color,
            h_align="center",
            v_align="center",
        )

        bui.buttonwidget(
            edit=btn,
            button_type="backSmall",
            size=(60, 60),
            color=self.sok_color3,
            label=bui.charstr(bui.SpecialChar.BACK),
        )
        if bui.app.ui_v1.use_toolbars and uiscale is bui.UIScale.SMALL:
            bui.textwidget(edit=txt, text="")

        v = height - (110 if self._is_main_menu else 90)
        v2 = height2 - (100 if self._is_main_menu else 80)
        v -= 100
        clr = (0.6, 0.7, 0.6, 1.0)
        v -= 280 if self._is_main_menu else 180
        v += (
            30
            if bui.app.ui_v1.use_toolbars and uiscale is bui.UIScale.SMALL
            else 0
        )
        hoffs = x_offs + 75 if self._is_main_menu else x_offs - 95
        hoffs_versus = x_offs + 315 if self._is_main_menu else x_offs - 335
        hoffs2 = x_offs + 90 if self._is_main_menu else x_offs - 110
        scl = 1.13 if self._is_main_menu else 0.68
        scl2 = 0.6 if self._is_main_menu else 0.15

        self._logo_model = bui.getmesh("bse_logoUI")
        self.logo_tex = bui.gettexture("bse_logo")

        self._logo_bs_model = bui.getmesh("bse_logoUI_bs")
        self.logo_bs_tex = bui.gettexture("bse_logo_bs")

        self._bse_button: bui.Widget | None = None
        self._bse_bse_button: bui.Widget | None = None
        self._hub_button: bui.Widget | None = None
        self._quick_game_button: bui.Widget | None = None

        # Only show coop button in main-menu variant.
        if self._is_main_menu:
            self._bse_button = btn = bui.buttonwidget(
                parent=self._root_widget,
                position=(
                    hoffs2 - 20,
                    v + (scl * 155 if self._is_main_menu else 140),
                ),
                size=(
                    scl * button_width2,
                    scl * (150 if self._is_main_menu else 220),
                ),
                extra_touch_border_scale=0.1,
                autoselect=True,
                label="",
                button_type="square",
                text_scale=1.13,
                color=self.sok_color,
                on_activate_call=self._bse,
            )

            if bui.app.ui_v1.use_toolbars and uiscale is bui.UIScale.SMALL:
                bui.widget(
                    edit=btn,
                    left_widget=bui.internal.get_special_widget("back_button"),
                )
                bui.widget(
                    edit=btn,
                    up_widget=bui.internal.get_special_widget("account_button"),
                )
                bui.widget(
                    edit=btn,
                    down_widget=bui.internal.get_special_widget(
                        "settings_button"
                    ),
                )

            if bui.app.ui_v1.use_toolbars and uiscale is bui.UIScale.SMALL:
                bui.widget(
                    edit=btn,
                    left_widget=bui.internal.get_special_widget("back_button"),
                )
                bui.widget(
                    edit=btn,
                    up_widget=bui.internal.get_special_widget("account_button"),
                )
                bui.widget(
                    edit=btn,
                    down_widget=bui.internal.get_special_widget(
                        "settings_button"
                    ),
                )

            bui.imagewidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(hoffs2 + scl2 * 82, v2 + scl2 * (-27)),
                size=(scl2 * 145, scl2 * 145),
                texture=self.logo_tex,
            )

            bui.textwidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(hoffs_versus + scl * (-318), v + scl * 172),
                size=(scl * button_width, scl * 50),
                text=bui.Lstr(
                    resource=f"{self._r}.bse",
                ),
                res_scale=1.5,
                maxwidth=scl * button_width * 0.7,
                h_align="center",
                v_align="center",
                color=(0.7, 0.9, 0.7, 1.0),
                scale=scl,
            )

        self._bombsq_button = btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(
                hoffs2 + 220,
                v + (scl * 155 if self._is_main_menu else 140),
            ),
            size=(
                scl * button_width2,
                scl * (150 if self._is_main_menu else 220),
            ),
            extra_touch_border_scale=0.1,
            autoselect=True,
            label="",
            button_type="square",
            text_scale=1.13,
            color=self.sok_color,
            on_activate_call=self._bombsquad,
        )

        bui.imagewidget(
            parent=self._root_widget,
            draw_controller=btn,
            position=(hoffs2 + scl2 * 481, v2 + scl2 * (-39)),
            size=(scl2 * 148, scl2 * 148),
            texture=self.logo_bs_tex,
        )

        bui.textwidget(
            parent=self._root_widget,
            draw_controller=btn,
            position=(hoffs_versus + scl * (-107), v + scl * 170),
            size=(scl * button_width, scl * 50),
            text=bui.Lstr(resource=f"{self._r}.bs"),
            res_scale=1.5,
            maxwidth=scl * button_width * 0.7,
            h_align="center",
            v_align="center",
            color=(0.7, 0.9, 0.7, 1.0),
            scale=scl,
        )

        if bui.app.ui_v1.use_toolbars:
            bui.widget(
                edit=btn,
                up_widget=bui.internal.get_special_widget(
                    "tickets_plus_button"
                ),
                right_widget=bui.internal.get_special_widget("party_button"),
            )

        hoffs += 0 if self._is_main_menu else 300
        v -= 155 if self._is_main_menu else 0

        if bui.app.ui_v1.use_toolbars and uiscale is bui.UIScale.SMALL:
            back_button.delete()
            bui.containerwidget(
                edit=self._root_widget,
                on_cancel_call=self._back,
                color=self.sok_color2,
                selected_child=(
                    self._bse_bse_button
                    if self._is_main_menu
                    else self._bombsq_button
                ),
            )
        else:
            bui.buttonwidget(edit=back_button, on_activate_call=self._back)
            bui.containerwidget(
                edit=self._root_widget,
                cancel_button=back_button,
                color=self.sok_color2,
                selected_child=(
                    self._bse_bse_button
                    if self._is_main_menu
                    else self._bombsq_button
                ),
            )

        self._restore_state()

    # noinspection PyUnresolvedReferences
    @staticmethod
    def _preload_modules() -> None:
        """Preload modules we use (called in bg thread)."""
        import bauiv1lib.creditslist as _unused1
        import bse.ui.credits.creditslist_bse as _unused2
        import bse.ui.credits.credits_contributors as _unused3
        import bse.ui.credits.credits_testers as _unused4

    def _back(self) -> None:
        # pylint: disable=cyclic-import
        if self._is_main_menu:
            from bauiv1lib.mainmenu import MainMenuWindow

            self._save_state()
            bui.app.ui_v1.set_main_menu_window(
                MainMenuWindow(transition="in_left").get_root_widget()
            )
            bui.containerwidget(
                edit=self._root_widget, transition=self._transition_out
            )
        else:
            from bauiv1lib.gather import GatherWindow

            self._save_state()
            bui.app.ui_v1.set_main_menu_window(
                GatherWindow(transition="in_left").get_root_widget()
            )
            bui.containerwidget(
                edit=self._root_widget, transition=self._transition_out
            )

    def _bse(self) -> None:
        # pylint: disable=cyclic-import
        from bse.ui.credits.creditslist_bse import CreditsBSEWindow

        self._save_state()
        bui.containerwidget(edit=self._root_widget, transition="out_left")
        bui.app.ui_v1.set_main_menu_window(
            CreditsBSEWindow(origin_widget=self._bse_button).get_root_widget()
        )

    def _bombsquad(self) -> None:
        # pylint: disable=cyclic-import
        from bauiv1lib.creditslist import CreditsListWindow

        self._save_state()
        bui.containerwidget(edit=self._root_widget, transition="out_left")
        bui.app.ui_v1.set_main_menu_window(
            CreditsListWindow(origin_widget=self._bse_button).get_root_widget()
        )

    def _team_tourney(self) -> None:
        # pylint: disable=cyclic-import
        from bauiv1lib.playlist.browser import PlaylistBrowserWindow

        self._save_state()
        bui.containerwidget(edit=self._root_widget, transition="out_left")
        bui.app.ui_v1.set_main_menu_window(
            PlaylistBrowserWindow(
                origin_widget=self._bombsq_button,
                sessiontype=bui.DualTeamSession,
            ).get_root_widget()
        )

    def _save_state(self) -> None:
        try:
            sel = self._root_widget.get_selected_child()
            if sel == self._bombsq_button:
                sel_name = "BS"
            elif self._bse_button is not None and sel == self._bse_button:
                sel_name = "BSE"
            elif sel == self._back_button:
                sel_name = "Back"
            else:
                raise ValueError(f"unrecognized selection {sel}")
            bui.app.ui_v1.window_states[type(self)] = sel_name
        except Exception:
            bui.print_exception(f"Error saving state for {self}.")

    def _restore_state(self) -> None:
        try:
            sel_name = bui.app.ui_v1.window_states.get(type(self))
            if sel_name == "BS":
                sel = self._bombsq_button
            elif sel_name == "BSE":
                sel = self._bse_button
            elif sel_name == "Back":
                sel = self._back_button
            else:
                sel = (
                    self._bse_button
                    if self._bse_button is not None
                    else self._bombsq_button
                )
            bui.containerwidget(edit=self._root_widget, selected_child=sel)
        except Exception:
            bui.print_exception(f"Error restoring state for {self}.")
