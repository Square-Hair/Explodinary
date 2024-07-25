# Released under the MIT License. See LICENSE for details.
#
"""Provides the top level play window."""

from __future__ import annotations

from typing import Any, Dict, Optional, Type

import ba
import ba.internal
import _ba

# Quick Game
from bastd.ui.playlist.addgame import PlaylistAddGameWindow
from ba._freeforallsession import FreeForAllSession
from bastd.activity.multiteamjoin import MultiTeamJoinActivity

quick_config = ba.app.config.get('quick_game_button', {'selected':None,'config':{}})

class PlayWindow(ba.Window):
    """Window for selecting overall play type."""

    def __init__(
        self,
        transition: str = 'in_right',
        origin_widget: ba.Widget | None = None,
    ):
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-locals
        import threading

        # Preload some modules we use in a background thread so we won't
        # have a visual hitch when the user taps them.
        threading.Thread(target=self._preload_modules).start()

        # We can currently be used either for main menu duty or for selecting
        # playlists (should make this more elegant/general).
        self._is_main_menu = not ba.app.ui.selecting_private_party_playlist
        self.sok_color = (0.1, 0.85, 0.45)
        self.sok_color2 = (0.1, 0.4, 0.3)
        self.sok_color3 = (0.9, 0.8, 0.25)
        uiscale = ba.app.ui.uiscale
        width = 1000 if uiscale is ba.UIScale.SMALL else 800
        x_offs = 100 if uiscale is ba.UIScale.SMALL else 0
        height = 550
        height2 = 265
        button_width = 400
        button_width2 = 200

        ba.app.ui.set_main_menu_location('Play Window')

        scale_origin: tuple[float, float] | None
        if origin_widget is not None:
            self._transition_out = 'out_scale'
            scale_origin = origin_widget.get_screen_space_center()
            transition = 'in_scale'
        else:
            self._transition_out = 'out_right'
            scale_origin = None

        self._r = 'playWindow'

        super().__init__(
            root_widget=ba.containerwidget(
                size=(width, height),
                transition=transition,
                toolbar_visibility='menu_full',
                scale_origin_stack_offset=scale_origin,
                scale=(
                    1.6
                    if uiscale is ba.UIScale.SMALL
                    else 0.9
                    if uiscale is ba.UIScale.MEDIUM
                    else 0.8
                ),
                stack_offset=(0, 0) if uiscale is ba.UIScale.SMALL else (0, 0),
            )
        )
        self._back_button = back_button = btn = ba.buttonwidget(
            parent=self._root_widget,
            position=(55 + x_offs, height - 132),
            size=(120, 60),
            scale=1.1,
            color=self.sok_color3,
            text_res_scale=1.5,
            text_scale=1.2,
            autoselect=True,
            label=ba.Lstr(resource='backText'),
            button_type='back',
        )

        txt = ba.textwidget(
            parent=self._root_widget,
            position=(width * 0.515, height - 101),
            # position=(width * 0.5, height -
            #           (101 if main_menu else 61)),
            size=(0, 0),
            text=ba.Lstr(
                resource=(self._r + '.titleText')
                if self._is_main_menu
                else 'playlistsText'
            ),
            scale=1.7,
            res_scale=2.0,
            maxwidth=400,
            color=ba.app.ui.heading_color,
            h_align='center',
            v_align='center',
        )

        ba.buttonwidget(
            edit=btn,
            button_type='backSmall',
            size=(60, 60),
            color=self.sok_color3,
            label=ba.charstr(ba.SpecialChar.BACK),
        )
        if ba.app.ui.use_toolbars and uiscale is ba.UIScale.SMALL:
            ba.textwidget(edit=txt, text='')

        v = height - (110 if self._is_main_menu else 90)
        v2 = height2 - (100 if self._is_main_menu else 80)
        v -= 100
        clr = (0.6, 0.7, 0.6, 1.0)
        v -= 280 if self._is_main_menu else 180
        v += 30 if ba.app.ui.use_toolbars and uiscale is ba.UIScale.SMALL else 0
        hoffs = x_offs + 75 if self._is_main_menu else x_offs - 95
        hoffs_versus = x_offs + 315 if self._is_main_menu else x_offs - 335
        hoffs2 = x_offs + 90 if self._is_main_menu else x_offs - 110
        scl = 1.13 if self._is_main_menu else 0.68
        scl2 = 0.6 if self._is_main_menu else 0.15
        
        self._logo_model = ba.getmodel('logoUI')
        self.logo_tex = ba.gettexture('logo')
        self.quick_game_tex = ba.gettexture('quickGameIcon')
        self.hub_tex = ba.gettexture('hubIcon')
        self._lineup_tex = ba.gettexture('playerLineup')
        angry_computer_transparent_model = ba.getmodel(
            'angryComputerTransparent'
        )
        self._lineup_1_transparent_model = ba.getmodel(
            'playerLineup1Transparent'
        )
        self._lineup_2_transparent_model = ba.getmodel(
            'playerLineup2Transparent'
        )
        self._lineup_3_transparent_model = ba.getmodel(
            'playerLineup3Transparent'
        )
        self._lineup_4_transparent_model = ba.getmodel(
            'playerLineup4Transparent'
        )
        self._eyes_model = ba.getmodel('plasticEyesTransparent')

        self._coop_button: ba.Widget | None = None
        self._bse_coop_button: ba.Widget | None = None
        self._hub_button: ba.Widget | None = None
        self._quick_game_button: ba.Widget | None = None

        # Only show coop button in main-menu variant.
        if self._is_main_menu:
            self._coop_button = btn = ba.buttonwidget(
                parent=self._root_widget,
                position=(hoffs2, v + (scl * 155 if self._is_main_menu else 140)),
                size=(
                    scl * button_width2,
                    scl * (150 if self._is_main_menu else 220),
                ),
                extra_touch_border_scale=0.1,
                autoselect=True,
                label='',
                button_type='square',
                text_scale=1.13,
                color=self.sok_color,
                on_activate_call=self._coop,
            )

            if ba.app.ui.use_toolbars and uiscale is ba.UIScale.SMALL:
                ba.widget(
                    edit=btn,
                    left_widget=_ba.get_special_widget('back_button'),
                )
                ba.widget(
                    edit=btn,
                    up_widget=_ba.get_special_widget('account_button'),
                )
                ba.widget(
                    edit=btn,
                    down_widget=_ba.get_special_widget(
                        'settings_button'
                    ),
                )

            self._draw_dude(
                0,
                btn,
                hoffs2,
                v2,
                scl2,
                position=(130, 120),
                color=(0.5, 0.75, 0.15),
            )
            self._draw_dude(
                1,
                btn,
                hoffs2,
                v2,
                scl2,
                position=(175, 123),
                color=(0.5, 0.75, 0.15),
            )
            self._draw_dude(
                2,
                btn,
                hoffs2,
                v2,
                scl2,
                position=(210, 97),
                color=(0.5, 0.75, 0.15),
            )
            self._draw_dude(
                3, btn, hoffs2, v2, scl2, position=(245, 107), color=(0.5, 0.75, 0.15),
            )
            ba.imagewidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(hoffs2 + scl2 * 190, v2 + scl2 * 220),
                size=(scl2 * 155, scl2 * 155),
                texture=self._lineup_tex,
                model_transparent=angry_computer_transparent_model,
            )

            ba.textwidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(hoffs2 + scl2 * (83), v2 + scl2 * 195),
                size=(scl2 * button_width2, scl2),
                text=ba.Lstr(
                    resource=f'explodinary.append.playModes.singlePlayerCoopText',
                    fallback_resource='playModes.coopText',
                ),
                maxwidth=scl * button_width * 0.4,
                res_scale=1.5,
                h_align='center',
                v_align='center',
                color=(0.7, 0.9, 0.7, 1.0),
                scale=scl * 1,
            )

            ba.textwidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(hoffs2 + scl2 * (83), v2 + (scl2 * 145)),
                size=(scl2 * button_width2, scl2 * 30),
                text=ba.Lstr(resource=self._r + '.oneToFourPlayersText'),
                h_align='center',
                v_align='center',
                scale=0.83 * scl2,
                flatness=1.0,
                maxwidth=scl2 * button_width2 * 0.7,
                color=clr,
            )
        #bse
            self._bse_coop_button = btn = ba.buttonwidget(
                parent=self._root_widget,
                position=(hoffs2, v + (scl * 15 if self._is_main_menu else 0)),
                size=(
                    scl * button_width2,
                    scl * (150 if self._is_main_menu else 220),
                ),
                extra_touch_border_scale=0.1,
                autoselect=True,
                label='',
                button_type='square',
                text_scale=1.13,
                color=self.sok_color,
                on_activate_call=self._bse_coop,
            )
            hoffs_plus = x_offs + 515 if self._is_main_menu else x_offs - 535
        #hub
            self._hub_button = ogo = ba.buttonwidget(
                parent=self._root_widget,
                position=(hoffs_plus, v + (scl * 155 if self._is_main_menu else 140)),
                size=(
                    scl * button_width2 - 10,
                    scl * (150 if self._is_main_menu else 220),
                ),
                extra_touch_border_scale=0.1,
                autoselect=True,
                label='',
                button_type='square',
                text_scale=1.13,
                color=self.sok_color,
                on_activate_call=self._press_hub,
            )
            
            ba.imagewidget(
                parent=self._root_widget,
                draw_controller=ogo,
                position=(hoffs_plus + scl2 * 100, v2 + scl2 * 220),
                size=(scl2 * 145, scl2 * 145),
                texture=self.hub_tex)
            
            ba.textwidget(
                parent=self._root_widget,
                draw_controller=ogo,
                position=(hoffs_plus + scl2 * (75), v2 + scl2 * 195),
                size=(scl2 * button_width2, scl2),
                text=ba.Lstr(
                    resource=f'explodinary.append.playModes.hubText'
                ),
                maxwidth=scl * button_width * 0.4,
                res_scale=1.5,
                h_align='center',
                v_align='center',
                color=(0.7, 0.9, 0.7, 1.0),
                scale=scl * 1,
            )
            
            ba.textwidget(
                parent=self._root_widget,
                draw_controller=ogo,
                position=(hoffs_plus + scl2 * (77), v2 + (scl2 * 145)),
                size=(scl2 * button_width2, scl2 * 30),
                text=ba.Lstr(resource=f'explodinary.append.playWindow.oneToTwelvePlayersText'),
                h_align='center',
                v_align='center',
                scale=0.83 * scl2,
                flatness=1.0,
                maxwidth=scl2 * button_width2 * 0.7,
                color=clr,
            )
        # Quick game
            self._quick_game_button = ghg = ba.buttonwidget(
                parent=self._root_widget,
                position=(hoffs_plus, v + (scl * 15 if self._is_main_menu else 0)),
                size=(
                    scl * button_width2 - 10,
                    scl * (150 if self._is_main_menu else 220),
                ),
                extra_touch_border_scale=0.1,
                autoselect=True,
                label='',
                button_type='square',
                text_scale=0.8,
                color=self.sok_color,
                on_activate_call=self._do_quick_game,
            )
            
            ba.imagewidget(
                parent=self._root_widget,
                draw_controller=ghg,
                position=(hoffs_plus + scl2 * 100, v2 + scl2 * (-40)),
                size=(scl2 * 145, scl2 * 145),
                texture=self.quick_game_tex)
                
            ba.textwidget(
                parent=self._root_widget,
                draw_controller=ghg,
                position=(hoffs_plus + scl2 * (75), v2 + scl2 * (-70)),
                size=(scl2 * button_width2, scl2),
                text=ba.Lstr(
                    resource=f'explodinary.append.playModes.quickGameText'
                ),
                maxwidth=scl * button_width * 0.4,
                res_scale=1.5,
                h_align='center',
                v_align='center',
                color=(0.7, 0.9, 0.7, 1.0),
                scale=scl * 0.9,
            )
            
            ba.textwidget(
                parent=self._root_widget,
                draw_controller=ghg,
                position=(hoffs_plus + scl2 * (77), v2 + (scl2 * (-120))),
                size=(scl2 * button_width2, scl2 * 30),
                text=ba.Lstr(resource=self._r + '.twoToEightPlayersText'),
                h_align='center',
                v_align='center',
                scale=0.83 * scl2,
                flatness=1.0,
                maxwidth=scl2 * button_width2 * 0.7,
                color=clr,
            )

            if ba.app.ui.use_toolbars and uiscale is ba.UIScale.SMALL:
                ba.widget(
                    edit=btn,
                    left_widget=_ba.get_special_widget('back_button'),
                )
                ba.widget(
                    edit=btn,
                    up_widget=_ba.get_special_widget('account_button'),
                )
                ba.widget(
                    edit=btn,
                    down_widget=_ba.get_special_widget(
                        'settings_button'
                    ),
                )
            
            ba.imagewidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(hoffs2 + scl2 * 125, v2 + scl2 * (-10)),
                size=(scl2 * 125, scl2 * 125),
                texture=self.logo_tex,
                model_transparent=self._logo_model,
            )
            
            ba.textwidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(hoffs2 + scl2 * (85), v2 + scl2 * (-50)),
                size=(scl2 * button_width2, scl2),
                text=ba.Lstr(
                    resource=f'explodinary.append.playModes.bseSinglePlayerCoopText',
                    fallback_resource='playModes.coopText',
                ),
                maxwidth=scl * button_width * 0.40,
                res_scale=1.5,
                h_align='center',
                v_align='center',
                color=(0.7, 0.9, 0.7, 1.0),
                scale=scl * 0.7,
            )

            ba.textwidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(hoffs2 + scl2 * (85), v2 + (scl2 * (-120))),
                size=(scl2 * button_width2, scl2 * 30),
                text=ba.Lstr(resource=f'explodinary.append.playWindow.oneToFivePlayersText'),
                h_align='center',
                v_align='center',
                scale=0.83 * scl2,
                flatness=1.0,
                maxwidth=scl2 * button_width2 * 0.7,
                color=clr,
            )
            
        scl = 0.5 if self._is_main_menu else 0.68
        hoffs += 440 if self._is_main_menu else 216
        v += 180 if self._is_main_menu else -68

        self._teams_button = btn = ba.buttonwidget(
            parent=self._root_widget,
            position=(hoffs_versus, v + (scl * 15 if self._is_main_menu else 0)),
            size=(
                scl * button_width,
                scl * (300 if self._is_main_menu else 360),
            ),
            extra_touch_border_scale=0.1,
            autoselect=True,
            label='',
            button_type='square',
            text_scale=1.13,
            color=self.sok_color,
            on_activate_call=self._team_tourney,
        )

        if ba.app.ui.use_toolbars:
            ba.widget(
                edit=btn,
                up_widget=_ba.get_special_widget('tickets_plus_button'),
                right_widget=_ba.get_special_widget('party_button'),
            )

        xxx = -14
        self._draw_dude(
            2,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 148, 30),
            color=(0.5, 0.25, 1.0),
        )
        self._draw_dude(
            3,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 181, 53),
            color=(0.5, 0.25, 1.0),
        )
        self._draw_dude(
            1,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 216, 33),
            color=(0.5, 0.25, 1.0),
        )
        self._draw_dude(
            0,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 245, 57),
            color=(0.5, 0.25, 1.0),
        )

        xxx = 155
        self._draw_dude(
            0,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 151, 30),
            color=(1, 0.88, 0),
        )
        self._draw_dude(
            1,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 189, 53),
            color=(1, 0.88, 0),
        )
        self._draw_dude(
            3,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 223, 27),
            color=(1, 0.88, 0),
        )
        self._draw_dude(
            2,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 257, 57),
            color=(1, 0.88, 0),
        )

        ba.textwidget(
            parent=self._root_widget,
            draw_controller=btn,
            position=(hoffs_versus + scl * (-10), v + scl * 95),
            size=(scl * button_width, scl * 50),
            text=ba.Lstr(
                resource='playModes.teamsText', fallback_resource='teamsText'
            ),
            res_scale=1.5,
            maxwidth=scl * button_width * 0.7,
            h_align='center',
            v_align='center',
            color=(0.7, 0.9, 0.7, 1.0),
            scale=scl * 2.3,
        )
        ba.textwidget(
            parent=self._root_widget,
            draw_controller=btn,
            position=(hoffs_versus + scl * (-10), v + (scl * 54)),
            size=(scl * button_width, scl * 30),
            text=ba.Lstr(resource=self._r + '.twoToEightPlayersText'),
            h_align='center',
            v_align='center',
            res_scale=1.5,
            scale=0.9 * scl,
            flatness=1.0,
            maxwidth=scl * button_width * 0.7,
            color=clr,
        )

        hoffs += 0 if self._is_main_menu else 300
        v -= 155 if self._is_main_menu else 0
        self._free_for_all_button = btn = ba.buttonwidget(
            parent=self._root_widget,
            position=(hoffs_versus, v + (scl * 15 if self._is_main_menu else 0)),
            size=(
                scl * button_width,
                scl * (300 if self._is_main_menu else 360),
            ),
            extra_touch_border_scale=0.1,
            autoselect=True,
            label='',
            button_type='square',
            text_scale=1.13,
            color=self.sok_color,
            on_activate_call=self._free_for_all,
        )

        xxx = -5
        self._draw_dude(
            0,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 140, 30),
            color=(0.4, 1.0, 0.4),
        )
        self._draw_dude(
            3,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 185, 53),
            color=(1.0, 0.4, 0.5),
        )
        self._draw_dude(
            1,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 220, 27),
            color=(0.4, 0.5, 1.0),
        )
        self._draw_dude(
            2,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 255, 57),
            color=(0.5, 1.0, 0.4),
        )
        xxx = 140
        self._draw_dude(
            2,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 148, 30),
            color=(1.0, 0.9, 0.4),
        )
        self._draw_dude(
            0,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 182, 53),
            color=(0.7, 1.0, 0.5),
        )
        self._draw_dude(
            3,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 233, 27),
            color=(0.7, 0.5, 0.9),
        )
        self._draw_dude(
            1,
            btn,
            hoffs_versus,
            v,
            scl,
            position=(xxx + 266, 53),
            color=(0.4, 0.5, 0.8),
        )
        ba.textwidget(
            parent=self._root_widget,
            draw_controller=btn,
            position=(hoffs_versus + scl * (-10), v + scl * 95),
            size=(scl * button_width, scl * 50),
            text=ba.Lstr(
                resource='playModes.freeForAllText',
                fallback_resource='freeForAllText',
            ),
            maxwidth=scl * button_width * 0.7,
            h_align='center',
            v_align='center',
            color=(0.7, 0.9, 0.7, 1.0),
            scale=scl * 1.9,
        )
        ba.textwidget(
            parent=self._root_widget,
            draw_controller=btn,
            position=(hoffs_versus + scl * (-10), v + (scl * 54)),
            size=(scl * button_width, scl * 30),
            text=ba.Lstr(resource=self._r + '.twoToEightPlayersText'),
            h_align='center',
            v_align='center',
            scale=0.9 * scl,
            flatness=1.0,
            maxwidth=scl * button_width * 0.7,
            color=clr,
        )

        if ba.app.ui.use_toolbars and uiscale is ba.UIScale.SMALL:
            back_button.delete()
            ba.containerwidget(
                edit=self._root_widget,
                on_cancel_call=self._back,
                color=self.sok_color2,
                selected_child=self._bse_coop_button
                if self._is_main_menu
                else self._teams_button,
            )
        else:
            ba.buttonwidget(edit=back_button, on_activate_call=self._back)
            ba.containerwidget(
                edit=self._root_widget,
                cancel_button=back_button,
                color=self.sok_color2,
                selected_child=self._bse_coop_button
                if self._is_main_menu
                else self._teams_button,
            )

        self._restore_state()

    # noinspection PyUnresolvedReferences
    @staticmethod
    def _preload_modules() -> None:
        """Preload modules we use (called in bg thread)."""
        import bastd.ui.mainmenu as _unused1
        import bastd.ui.account as _unused2
        import bastd.ui.coop.browser as _unused3
        import bastd.ui.playlist.browser as _unused4
        import explodinary.ui.bsebrowser as _unused5
        import explodinary.game.hub as _unused6

    def _back(self) -> None:
        # pylint: disable=cyclic-import
        if self._is_main_menu:
            from bastd.ui.mainmenu import MainMenuWindow

            self._save_state()
            ba.app.ui.set_main_menu_window(
                MainMenuWindow(transition='in_left').get_root_widget()
            )
            ba.containerwidget(
                edit=self._root_widget, transition=self._transition_out
            )
        else:
            from bastd.ui.gather import GatherWindow

            self._save_state()
            ba.app.ui.set_main_menu_window(
                GatherWindow(transition='in_left').get_root_widget()
            )
            ba.containerwidget(
                edit=self._root_widget, transition=self._transition_out
            )

    def _coop(self) -> None:
        # pylint: disable=cyclic-import
        from bastd.ui.account import show_sign_in_prompt
        from bastd.ui.coop.browser import CoopBrowserWindow

        if ba.internal.get_v1_account_state() != 'signed_in':
            show_sign_in_prompt()
            return
        self._save_state()
        ba.containerwidget(edit=self._root_widget, transition='out_left')
        ba.app.ui.set_main_menu_window(
            CoopBrowserWindow(origin_widget=self._coop_button).get_root_widget()
        )
        
    def _bse_coop(self) -> None:
        # pylint: disable=cyclic-import
        from bastd.ui.account import show_sign_in_prompt
        from explodinary.ui.bsebrowser import BSECoopBrowserWindow

        if ba.internal.get_v1_account_state() != 'signed_in':
            show_sign_in_prompt()
            return
        self._save_state()
        ba.containerwidget(edit=self._root_widget, transition='out_left')
        ba.app.ui.set_main_menu_window(
            BSECoopBrowserWindow(origin_widget=self._bse_coop_button).get_root_widget()
        )

    def _press_hub(self):
        self._save_state()
        # Input locking
        ba.internal.lock_all_input()
        ba.timer(0.25, ba.internal.unlock_all_input, timetype=ba.TimeType.REAL)

        # Run mode
        from explodinary import _versiondata
        ba.app.launch_hub_game(f"{_versiondata.internalsub}:Hub")

    def _do_quick_game(self) -> None:
        self._save_state()
        ba.containerwidget(edit=self._root_widget, transition='out_left')
        ba.app.ui.set_main_menu_window(SelectGameWindow().get_root_widget())

    def _team_tourney(self) -> None:
        # pylint: disable=cyclic-import
        from bastd.ui.playlist.browser import PlaylistBrowserWindow

        self._save_state()
        ba.containerwidget(edit=self._root_widget, transition='out_left')
        ba.app.ui.set_main_menu_window(
            PlaylistBrowserWindow(
                origin_widget=self._teams_button, sessiontype=ba.DualTeamSession
            ).get_root_widget()
        )

    def _free_for_all(self) -> None:
        # pylint: disable=cyclic-import
        from bastd.ui.playlist.browser import PlaylistBrowserWindow

        self._save_state()
        ba.containerwidget(edit=self._root_widget, transition='out_left')
        ba.app.ui.set_main_menu_window(
            PlaylistBrowserWindow(
                origin_widget=self._free_for_all_button,
                sessiontype=ba.FreeForAllSession,
            ).get_root_widget()
        )

    def _draw_dude(
        self,
        i: int,
        btn: ba.Widget,
        hoffs: float,
        v: float,
        scl: float,
        position: tuple[float, float],
        color: tuple[float, float, float],
    ) -> None:
        h_extra = -100
        v_extra = 130
        eye_color = (
            0.7 * 1.0 + 0.3 * color[0],
            0.7 * 1.0 + 0.3 * color[1],
            0.7 * 1.0 + 0.3 * color[2],
        )
        if i == 0:
            ba.imagewidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(
                    hoffs + scl * (h_extra + position[0]),
                    v + scl * (v_extra + position[1]),
                ),
                size=(scl * 60, scl * 80),
                color=color,
                texture=self._lineup_tex,
                model_transparent=self._lineup_1_transparent_model,
            )
            ba.imagewidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(
                    hoffs + scl * (h_extra + position[0] + 12),
                    v + scl * (v_extra + position[1] + 53),
                ),
                size=(scl * 36, scl * 18),
                texture=self._lineup_tex,
                color=eye_color,
                model_transparent=self._eyes_model,
            )
        elif i == 1:
            ba.imagewidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(
                    hoffs + scl * (h_extra + position[0]),
                    v + scl * (v_extra + position[1]),
                ),
                size=(scl * 45, scl * 90),
                color=color,
                texture=self._lineup_tex,
                model_transparent=self._lineup_2_transparent_model,
            )
            ba.imagewidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(
                    hoffs + scl * (h_extra + position[0] + 5),
                    v + scl * (v_extra + position[1] + 67),
                ),
                size=(scl * 32, scl * 16),
                texture=self._lineup_tex,
                color=eye_color,
                model_transparent=self._eyes_model,
            )
        elif i == 2:
            ba.imagewidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(
                    hoffs + scl * (h_extra + position[0]),
                    v + scl * (v_extra + position[1]),
                ),
                size=(scl * 45, scl * 90),
                color=color,
                texture=self._lineup_tex,
                model_transparent=self._lineup_3_transparent_model,
            )
            ba.imagewidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(
                    hoffs + scl * (h_extra + position[0] + 5),
                    v + scl * (v_extra + position[1] + 59),
                ),
                size=(scl * 34, scl * 17),
                texture=self._lineup_tex,
                color=eye_color,
                model_transparent=self._eyes_model,
            )
        elif i == 3:
            ba.imagewidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(
                    hoffs + scl * (h_extra + position[0]),
                    v + scl * (v_extra + position[1]),
                ),
                size=(scl * 48, scl * 96),
                color=color,
                texture=self._lineup_tex,
                model_transparent=self._lineup_4_transparent_model,
            )
            ba.imagewidget(
                parent=self._root_widget,
                draw_controller=btn,
                position=(
                    hoffs + scl * (h_extra + position[0] + 2),
                    v + scl * (v_extra + position[1] + 62),
                ),
                size=(scl * 38, scl * 19),
                texture=self._lineup_tex,
                color=eye_color,
                model_transparent=self._eyes_model,
            )
    
    def _save_state(self) -> None:
        try:
            sel = self._root_widget.get_selected_child()
            if sel == self._teams_button:
                sel_name = 'Team Games'
            elif self._coop_button is not None and sel == self._coop_button:
                sel_name = 'Co-op Games'
            elif self._bse_coop_button is not None and sel == self._bse_coop_button:
                sel_name = 'BSE Co-op Games'
            elif self._hub_button is not None and sel == self._hub_button:
                sel_name = 'Hub'
            elif self._quick_game_button is not None and sel == self._quick_game_button:
                sel_name = 'Quick Game'
            elif sel == self._free_for_all_button:
                sel_name = 'Free-for-All Games'
            elif sel == self._back_button:
                sel_name = 'Back'
            else:
                raise ValueError(f'unrecognized selection {sel}')
            ba.app.ui.window_states[type(self)] = sel_name
        except Exception:
            ba.print_exception(f'Error saving state for {self}.')

    def _restore_state(self) -> None:
        try:
            sel_name = ba.app.ui.window_states.get(type(self))
            if sel_name == 'Team Games':
                sel = self._teams_button
            elif sel_name == 'Co-op Games' and self._coop_button is not None:
                sel = self._coop_button
            elif sel_name == 'BSE Co-op Games' and self._bse_coop_button is not None:
                sel = self._bse_coop_button
            elif sel_name == 'Hub' and self._hub_button is not None:
                sel = self._hub_button
            elif sel_name == 'Quick Game' and self._quick_game_button is not None:
                sel = self._quick_game_button
            elif sel_name == 'Free-for-All Games':
                sel = self._free_for_all_button
            elif sel_name == 'Back':
                sel = self._back_button
            else:
                sel = (
                    self._coop_button
                    if self._coop_button is not None
                    else self._teams_button
                )
            ba.containerwidget(edit=self._root_widget, selected_child=sel)
        except Exception:
            ba.print_exception(f'Error restoring state for {self}.')
        
# Quick game stuff

class SimplePlaylist:

    def __init__(self,
                 settings: dict,
                 gametype: type[ba.GameActivity]):
        self.settings = settings
        self.gametype = gametype

    def pull_next(self) -> None:
        if 'map' not in self.settings['settings']:
            settings = dict(
                map=self.settings['map'], **self.settings['settings'])
        else:
            settings = self.settings['settings']
        return dict(resolved_type=self.gametype, settings=settings)
        
class CustomSession(FreeForAllSession):

    def __init__(self, *args, **kwargs):
        # pylint: disable=cyclic-import
        self.use_teams = False
        self._tutorial_activity_instance = None
        ba.Session.__init__(self, depsets=[],
                            team_names=None,
                            team_colors=None,
                            min_players=1,
                            max_players=self.get_max_players())

        self._series_length = 1
        self._ffa_series_length = 1

        # Which game activity we're on.
        self._game_number = 0
        self._playlist = SimplePlaylist(self._config, self._gametype)
        
        quick_config['selected'] = self._gametype.__name__
        quick_config['config'] = self._config
        ba.app.config.commit()

        # Get a game on deck ready to go.
        self._current_game_spec: Optional[Dict[str, Any]] = None
        self._next_game_spec: Dict[str, Any] = self._playlist.pull_next()
        self._next_game: Type[ba.GameActivity] = (
            self._next_game_spec['resolved_type'])

        # Go ahead and instantiate the next game we'll
        # use so it has lots of time to load.
        self._instantiate_next_game()

        # Start in our custom join screen.
        self.setactivity(_ba.newactivity(MultiTeamJoinActivity))


class SelectGameWindow(PlaylistAddGameWindow):

    def __init__(self, transition: str = 'in_right'):
        class EditController:
            _sessiontype = ba.FreeForAllSession

            def get_session_type(self) -> Type[ba.Session]:
                return self._sessiontype

        self._editcontroller = EditController()
        self._r = 'explodinary.quickGameMenu'
        uiscale = ba.app.ui.uiscale
        self._width = 750 if uiscale is ba.UIScale.SMALL else 650
        x_inset = 50 if uiscale is ba.UIScale.SMALL else 0
        self._height = (346 if uiscale is ba.UIScale.SMALL else
                        380 if uiscale is ba.UIScale.MEDIUM else 440)
        top_extra = 30 if uiscale is ba.UIScale.SMALL else 20
        self._scroll_width = 210

        self._root_widget = ba.containerwidget(
            size=(self._width, self._height + top_extra),
            transition=transition,
            scale=(2.17 if uiscale is ba.UIScale.SMALL else
                   1.5 if uiscale is ba.UIScale.MEDIUM else 1.0),
            stack_offset=(0, 1) if uiscale is ba.UIScale.SMALL else (0, 0),
            color=(0.1, 0.4, 0.3))

        self._back_button = ba.buttonwidget(parent=self._root_widget,
                                            position=(58 + x_inset,
                                                      self._height - 53),
                                            size=(165, 70),
                                            scale=0.75,
                                            text_scale=1.2,
                                            label=ba.Lstr(resource='backText'),
                                            autoselect=True,
                                            button_type='back',
                                            on_activate_call=self._back)
        self._select_button = select_button = ba.buttonwidget(
            parent=self._root_widget,
            position=(self._width - (172 + x_inset), self._height - 50),
            autoselect=True,
            size=(160, 60),
            scale=0.75,
            text_scale=1.2,
            label=ba.Lstr(resource='selectText'),
            on_activate_call=self._add)

        if ba.app.ui.use_toolbars:
            ba.widget(edit=select_button,
                      right_widget=_ba.get_special_widget('party_button'))

        ba.textwidget(parent=self._root_widget,
                      position=(self._width * 0.5, self._height - 28),
                      size=(0, 0),
                      scale=1.0,
                      text=ba.Lstr(resource=self._r + '.titleText'),
                      h_align='center',
                      color=ba.app.ui.title_color,
                      maxwidth=250,
                      v_align='center')
        v = self._height - 64

        self._selected_title_text = ba.textwidget(
            parent=self._root_widget,
            position=(x_inset + self._scroll_width + 50 + 30, v - 15),
            size=(0, 0),
            scale=1.0,
            color=(0.7, 1.0, 0.7, 1.0),
            maxwidth=self._width - self._scroll_width - 150 - x_inset * 2,
            h_align='left',
            v_align='center')
        v -= 30

        self._selected_description_text = ba.textwidget(
            parent=self._root_widget,
            position=(x_inset + self._scroll_width + 50 + 30, v),
            size=(0, 0),
            scale=0.7,
            color=(0.5, 0.8, 0.5, 1.0),
            maxwidth=self._width - self._scroll_width - 150 - x_inset * 2,
            h_align='left')

        scroll_height = self._height - 100

        v = self._height - 60

        self._scrollwidget = ba.scrollwidget(parent=self._root_widget,
                                             position=(x_inset + 61,
                                                       v - scroll_height),
                                             size=(self._scroll_width,
                                                   scroll_height),
                                             highlight=False)
        ba.widget(edit=self._scrollwidget,
                  up_widget=self._back_button,
                  left_widget=self._back_button,
                  right_widget=select_button)
        self._column: Optional[ba.Widget] = None

        v -= 35
        ba.containerwidget(edit=self._root_widget,
                           cancel_button=self._back_button,
                           start_button=select_button)
        self._selected_game_type: Optional[Type[ba.GameActivity]] = None

        ba.containerwidget(edit=self._root_widget,
                           selected_child=self._scrollwidget)

        self._game_types: list[type[ba.GameActivity]] = []

        # Get actual games loading in the bg.
        ba.app.meta.load_exported_classes(ba.GameActivity,
                                          self._on_game_types_loaded,
                                          completion_cb_in_bg_thread=True)

        # Refresh with our initial empty list. We'll refresh again once
        # game loading is complete.
        self._refresh()

        if quick_config['selected']:
            for gt in self._game_types:
                if gt.__name__ == quick_config['selected']:
                    self._refresh(selected=gt)
                    self._set_selected_game_type(gt)

    def _refresh(self,
                 select_get_more_games_button: bool = False,
                 selected: bool = None) -> None:
        # from ba.internal import get_game_types

        if self._column is not None:
            self._column.delete()

        self._column = ba.columnwidget(parent=self._scrollwidget,
                                       border=2,
                                       margin=0)

        for i, gametype in enumerate(self._game_types):

            def _doit() -> None:
                if self._select_button:
                    ba.timer(0.1,
                             self._select_button.activate,
                             timetype=ba.TimeType.REAL)

            txt = ba.textwidget(parent=self._column,
                                position=(0, 0),
                                size=(self._width - 88, 24),
                                text=gametype.get_display_string(),
                                h_align='left',
                                v_align='center',
                                color=(0.8, 0.8, 0.8, 1.0),
                                maxwidth=self._scroll_width * 0.8,
                                on_select_call=ba.Call(
                                    self._set_selected_game_type, gametype),
                                always_highlight=True,
                                selectable=True,
                                on_activate_call=_doit)
            if i == 0:
                ba.widget(edit=txt, up_widget=self._back_button)

        self._get_more_games_button = ba.buttonwidget(
            parent=self._column,
            autoselect=True,
            label=ba.Lstr(resource='addGameWindow' + '.getMoreGamesText'),
            color=(0.54, 0.52, 0.67),
            textcolor=(0.7, 0.65, 0.7),
            on_activate_call=self._on_get_more_games_press,
            size=(178, 50))
        if select_get_more_games_button:
            ba.containerwidget(edit=self._column,
                               selected_child=self._get_more_games_button,
                               visible_child=self._get_more_games_button)

    def _add(self) -> None:
        _ba.lock_all_input()  # Make sure no more commands happen.
        ba.timer(0.1, _ba.unlock_all_input, timetype=ba.TimeType.REAL)
        gameconfig = {}
        if quick_config['selected'] == self._selected_game_type.__name__:
            if quick_config['config']:
                gameconfig = quick_config['config']
        if 'map' in gameconfig:
            quick_config['settings']['map'] = gameconfig.pop('map')
        self._selected_game_type.create_settings_ui(
            self._editcontroller.get_session_type(),
            gameconfig,
            self._edit_game_done)

    def _edit_game_done(self, config: Optional[Dict[str, Any]]) -> None:
        if config:
            CustomSession._config = config
            CustomSession._gametype = self._selected_game_type
            self.start_game(CustomSession)
        else:
            ba.app.ui.clear_main_menu_window(transition='out_right')
            ba.app.ui.set_main_menu_window(
                SelectGameWindow(transition='in_left').get_root_widget())

    def _back(self) -> None:
        ba.containerwidget(edit=self._root_widget, transition='out_left')
        ba.app.ui.set_main_menu_window(
            PlayWindow(transition='in_left').get_root_widget())
    
    def start_game(self, session: ba.Session, fadeout: bool = True):
        def callback():
            if fadeout:
                _ba.unlock_all_input()
            try:
                _ba.new_host_session(session)
            except Exception:
                from bastd import mainmenu
                ba.print_exception('exception running session', session)

                # Drop back into a main menu session.
                _ba.new_host_session(mainmenu.MainMenuSession)

        if fadeout:
            _ba.fade_screen(False, time=0.25, endcall=callback)
            _ba.lock_all_input()
        else:
            callback()
    