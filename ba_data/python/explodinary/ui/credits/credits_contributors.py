# Released under the MIT License. See LICENSE for details.
#
"""Provides a window to display game credits."""

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
import ba.internal

if TYPE_CHECKING:
    from typing import Sequence


class CreditsContributorsWindow(ba.Window):
    """Window for displaying game credits."""

    def __init__(self, origin_widget: ba.Widget | None = None):
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements
        import json

        ba.set_analytics_screen('Credits BS Window')
        
        self.sok_color = (0.1, 0.4, 0.3)
        
        self._back_button: ba.Widget | None = None
        
        #PFPs
        self.miki_tex = ba.gettexture('pfpMiki')
        self.neo_tex = ba.gettexture('pfpNeo')
        self.shadow_tex = ba.gettexture('pfpShadow')
        self.angel_tex = ba.gettexture('pfpAngel')
        self.freaky_tex = ba.gettexture('pfpFreaky')
        #Icons
        self.yt_tex = ba.gettexture('ytWhite')
        self.sc_tex = ba.gettexture('soundcloudIcon')
        
        # if they provided an origin-widget, scale up from that
        scale_origin: tuple[float, float] | None
        if origin_widget is not None:
            self._transition_out = 'out_scale'
            scale_origin = origin_widget.get_screen_space_center()
            transition = 'in_scale'
        else:
            self._transition_out = 'out_right'
            scale_origin = None
            transition = 'in_right'

        uiscale = ba.app.ui.uiscale
        width = 870 if uiscale is ba.UIScale.SMALL else 670
        x_inset = 100 if uiscale is ba.UIScale.SMALL else 0
        height = 398 if uiscale is ba.UIScale.SMALL else 500

        self._r = 'explodinary.bseCredits'
        super().__init__(
            root_widget=ba.containerwidget(
                size=(width, height),
                transition=transition,
                color=self.sok_color,
                toolbar_visibility='menu_minimal',
                scale_origin_stack_offset=scale_origin,
                scale=(
                    2.0
                    if uiscale is ba.UIScale.SMALL
                    else 1.3
                    if uiscale is ba.UIScale.MEDIUM
                    else 1.0
                ),
                stack_offset=(0, -8) if uiscale is ba.UIScale.SMALL else (0, 0),
            )
        )

        if ba.app.ui.use_toolbars and uiscale is ba.UIScale.SMALL:
            ba.containerwidget(
                edit=self._root_widget, on_cancel_call=self._back
            )
        else:
            self._back_button = ba.buttonwidget(
                parent=self._root_widget,
                position=(
                    40 + x_inset,
                    height - (68 if uiscale is ba.UIScale.SMALL else 62),
                ),
                size=(140, 60),
                scale=0.8,
                label=ba.Lstr(resource='backText'),
                button_type='back',
                on_activate_call=self._back,
                autoselect=True,
            )
            ba.containerwidget(edit=self._root_widget, cancel_button=self._back_button)

            ba.buttonwidget(
                edit=self._back_button,
                button_type='backSmall',
                position=(
                    40 + x_inset,
                    height - (68 if uiscale is ba.UIScale.SMALL else 62) + 5,
                ),
                size=(60, 48),
                label=ba.charstr(ba.SpecialChar.BACK),
            )

        ba.textwidget(
            parent=self._root_widget,
            position=(0, height - (59 if uiscale is ba.UIScale.SMALL else 54)),
            size=(width, 30),
            text=ba.Lstr(resource=f'{self._r}.btn.cont'),
            h_align='center',
            color=ba.app.ui.title_color,
            maxwidth=330,
            v_align='center',
        )

        scroll = ba.scrollwidget(
            parent=self._root_widget,
            color=(0.1, 0.85, 0.45),
            position=(40 + x_inset, 35),
            size=(width - (80 + 2 * x_inset), height - 100),
            capture_arrows=True,
            claims_left_right=True,
        )

        if ba.app.ui.use_toolbars:
            if uiscale is ba.UIScale.SMALL:
                ba.widget(
                    edit=scroll,
                    left_widget=ba.internal.get_special_widget('back_button'),
                )

        fellas = [
            (
                'TheMikirog',
                ba.Lstr(resource=f'{self._r}.contributors.mikiDesc'),
                ba.gettexture('pfpMiki'),
                [(self.yt_tex, (0.8, 0.3, 0.25), 'https://www.youtube.com/@TheMikirog')],
            ),
            (
                'Nęo',
                ba.Lstr(resource=f'{self._r}.contributors.bitcDesc'),
                ba.gettexture('pfpNeo'),
                [(self.yt_tex, (0.8, 0.3, 0.25), 'https://www.youtube.com/@nyooon516')],
            ),
            (
                'ShadowQ',
                ba.Lstr(resource=f'{self._r}.contributors.shadDesc'),
                ba.gettexture('pfpShadow'),
                [(self.yt_tex, (0.8, 0.3, 0.25), 'https://www.youtube.com/@TheShadowQ'),
                 (self.sc_tex, (1, 0.5, 0), 'https://soundcloud.com/kacperrrmusic'),],
            ),
            (
                'byANG3L',
                ba.Lstr(resource=f'{self._r}.contributors.byanDesc'),
                ba.gettexture('pfpAngel'),
                [(self.yt_tex, (0.8, 0.3, 0.25), 'https://www.youtube.com/results?search_query=byangel+bombsquad')],
            ),
            (
                'Freakyyyy',
                ba.Lstr(resource=f'{self._r}.contributors.freaDesc'),
                ba.gettexture('pfpFreaky'),
                [],
            ),
        ]
        fella_amount = len(fellas)
        
        yoff_base = 120
        
        scale = 1
        self._sub_width = width - 80
        self._sub_height = yoff_base * fella_amount

        container = self._subcontainer = ba.containerwidget(
            parent=scroll,
            size=(self._sub_width, self._sub_height),
            background=False,
            claims_left_right=True,
            claims_tab=False,
        )
        
        yoff = self._sub_height - yoff_base/1.65
        btnitr = 0
        # Create a line for each fella
        for name, desc, icon, buttons in fellas:
            name_node = ba.textwidget(
                parent=container,
                position=(125, yoff + 15),
                text=name,
                scale=1.25,
                res_scale=2.0,
                maxwidth=400,
                h_align='left',
                v_align='center',
            )
            desc_node = ba.textwidget(
                parent=container,
                position=(125, yoff - 20),
                text=desc,
                scale=0.975,
                res_scale=2.0,
                maxwidth=400,
                h_align='left',
                v_align='center',
            )
            icon_node = ba.imagewidget(
                parent=container,
                position=(30, yoff - 20),
                size=(70, 70),
                texture=icon,
            )
            btnoff = 150
            for b_tex, b_color, b_link in buttons:
                lbtn = ba.buttonwidget(
                    parent=container,
                    position=(140 + btnoff, yoff + 15),
                    autoselect=True,
                    color=b_color,
                    button_type='square',
                    size=(25, 25),
                    label='',
                    on_activate_call=ba.Call(
                        ba.open_url, b_link
                    ),
                )
                ba.imagewidget(
                    parent=container,
                    draw_controller=lbtn,
                    position=(140 + btnoff + 2.5, yoff + 15 + 2.5),
                    size=(20, 20),
                    texture=b_tex,
                )
                if btnitr == 0:
                    ba.buttonwidget(
                        edit=lbtn,
                        up_widget=self._back_button,
                    )
                btnoff += 40
                btnitr += 1
            # Increase offset for our next fella
            yoff -= yoff_base

    def _back(self) -> None:
        # pylint: disable=cyclic-import
        from explodinary.ui.credits.creditslist_bse import CreditsBSEWindow
        ba.containerwidget(
            edit=self._root_widget, transition=self._transition_out
        )
        ba.app.ui.set_main_menu_window(
            CreditsBSEWindow(transition='in_left').get_root_widget()
        )

