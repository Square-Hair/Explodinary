# Released under the MIT License. See LICENSE for details.
#
"""Provides UI for graphics settings."""

from __future__ import annotations

from typing import TYPE_CHECKING

import bauiv1 as bui
from bauiv1lib import popup

import bse

if TYPE_CHECKING:
    pass

section = {"last": 0}


class ExplodinarySettings(bui.Window):
    """Window for graphics settings."""

    def __init__(
        self,
        transition: str = "in_right",
        origin_widget: bui.Widget | None = None,
    ):
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements

        # if they provided an origin-widget, scale up from that
        scale_origin: tuple[float, float] | None
        if origin_widget is not None:
            self._transition_out = "out_scale"
            scale_origin = origin_widget.get_screen_space_center()
            transition = "in_scale"
        else:
            self._transition_out = "out_right"
            scale_origin = None

        self._r = "bseSettingsWindow"

        uiscale = bui.app.ui_v1.uiscale
        height = self.height = 575 if uiscale is bui.UIScale.SMALL else 550
        width = self.width = 900 if uiscale is bui.UIScale.SMALL else 550
        spacing = 32

        self._have_selected_child = False

        base_scale = (
            1.5
            if uiscale is bui.UIScale.SMALL
            else 1.2 if uiscale is bui.UIScale.MEDIUM else 1.0
        )
        self.popup_menu_scale = base_scale * 1.2
        tyoff = -35 if uiscale is bui.UIScale.SMALL else 0

        super().__init__(
            root_widget=bui.containerwidget(
                size=(width, height),
                transition=transition,
                color=(0.1, 0.4, 0.3),
                scale_origin_stack_offset=scale_origin,
                scale=base_scale,
                stack_offset=(
                    (0, -30) if uiscale is bui.UIScale.SMALL else (0, 0)
                ),
            )
        )

        self._backbtn = btn = bui.buttonwidget(
            parent=self._root_widget,
            position=(35 - tyoff, height - 60 + tyoff),
            size=(120, 60),
            scale=0.8,
            text_scale=1.2,
            autoselect=True,
            label=bui.Lstr(resource="backText"),
            button_type="back",
            on_activate_call=self._back,
        )

        bui.containerwidget(edit=self._root_widget, cancel_button=btn)

        self._title = bui.textwidget(
            parent=self._root_widget,
            position=(0, height - 44 + tyoff),
            size=(width, 25),
            text=bui.Lstr(resource=self._r + ".titleText"),
            color=bui.app.ui_v1.title_color,
            h_align="center",
            v_align="top",
        )

        self._subtitle = bui.textwidget(
            parent=self._root_widget,
            position=(0, height - 70 + tyoff),
            size=(width, 25),
            text="?",
            color=bui.app.ui_v1.infotextcolor,
            scale=0.75,
            h_align="center",
            v_align="top",
        )

        bui.buttonwidget(
            edit=btn,
            button_type="backSmall",
            size=(60, 60),
            label=bui.charstr(bui.SpecialChar.BACK),
        )

        self.travel_buttons: dict = {}
        # Section buttons for big UI
        npos = (
            (width / 8),
            (height * 0.1 + (50 if uiscale is bui.UIScale.SMALL else 0)),
        )
        wlab = "<"
        for x in range(2):
            self.travel_buttons[x] = bui.buttonwidget(
                parent=self._root_widget,
                position=npos,
                size=(45, 45),
                scale=1,
                text_scale=1.2,
                autoselect=True,
                label=wlab,
                button_type="square",
                on_activate_call=bui.Call(self._travel, x),
                color=(0.1, 0.85, 0.45),
                textcolor=(0.6, 0.85, 0.71),
            )
            npos = (
                width - (width / 8) - 30,
                (height * 0.1 + (50 if uiscale is bui.UIScale.SMALL else 0)),
            )
            wlab = ">"

        self._dont_delete: list = [
            self._backbtn,
            self._title,
            self._subtitle,
        ]
        for x in self.travel_buttons:
            self._dont_delete.append(self.travel_buttons[x])

        self._section = section["last"]
        self.tab_amount = 2

        self._has_changed_theme = False

        self.refresh()

    def refresh(self) -> None:
        """
        Updates what this UI contains
        called when pressing the arrows at the bottom
        """
        uiscale = bui.app.ui_v1.uiscale
        height = self.height = 575 if uiscale is bui.UIScale.SMALL else 550
        width = self.width = 900 if uiscale is bui.UIScale.SMALL else 550
        spacing = 32

        self._have_selected_child = False

        base_scale = (
            1.5
            if uiscale is bui.UIScale.SMALL
            else 1.2 if uiscale is bui.UIScale.MEDIUM else 1.0
        )
        self.popup_menu_scale = base_scale * 1.2
        tyoff = -25 if uiscale is bui.UIScale.SMALL else 0

        # Main values
        s_pos_x = width / 2
        s_pos_y = height - 109 + tyoff

        for c in self._root_widget.get_children():
            if not c in self._dont_delete:
                c.delete()

        for i, b in enumerate(self.travel_buttons):
            if (self._section == 0 and i == 0) or (
                self._section == self.tab_amount and i == 1
            ):
                bui.buttonwidget(
                    edit=self.travel_buttons[b],
                    color=(0.6, 0.6, 0.6),
                    textcolor=(0.4, 0.4, 0.4),
                    enable_sound=False,
                )
            else:
                bui.buttonwidget(
                    edit=self.travel_buttons[b],
                    color=(0.1, 0.85, 0.45),
                    textcolor=(0.6, 0.85, 0.71),
                    enable_sound=True,
                )

        if self._section == 0:
            # Custom offset
            s_pos_y += 10
            # Powerup subtitle
            bui.textwidget(
                edit=self._subtitle,
                text=bui.Lstr(resource=self._r + ".Powerup Configuration"),
            )

            # TNT Variants
            tnt = self._build_setting(
                position=(s_pos_x, s_pos_y),
                title=bui.Lstr(resource=f"{self._r}.tntVariants.name"),
                subtitle=bui.Lstr(resource=f"{self._r}.tntVariants.sub"),
                key="tnt_variants",
                default=True,
            )
            s_pos_y -= 67.5
            bui.widget(edit=self._backbtn, down_widget=tnt.get_button())

            # Powerup Popups
            self._build_setting(
                position=(s_pos_x, s_pos_y),
                title=bui.Lstr(resource=self._r + ".powerupPopups.name"),
                subtitle=bui.Lstr(resource=self._r + ".powerupPopups.sub"),
                key="powerup_text",
            )
            s_pos_y -= 60

            ### Item Distributions
            settingtitle = bui.textwidget(
                parent=self._root_widget,
                position=(s_pos_x, s_pos_y),
                size=(0, 0),
                text=bui.Lstr(resource=self._r + ".powerupDist.name"),
                scale=0.75,
                res_scale=1.5,
                maxwidth=250,
                color=bui.app.ui_v1.infotextcolor,
                h_align="center",
                v_align="center",
            )

            s_pos_y -= 25

            settingsub = bui.textwidget(
                parent=self._root_widget,
                position=(s_pos_x, s_pos_y),
                size=(0, 0),
                text=bui.Lstr(resource=self._r + ".powerupDist.sub"),
                scale=0.6,
                res_scale=1.5,
                maxwidth=250,
                color=(0.7, 0.7, 0.7),
                h_align="center",
                v_align="center",
            )
            s_pos_y -= 62
            from bse._powerup import all_powerup_dists

            # powerup distribution
            bse.cfg.fetch("powerup_dist", "Explodinary", do_set=True) # assign

            suffix = self._r + ".powerupDist.dists."

            dist_choice: list[list, list] = [[], []]
            from bascenev1._powerup import all_powerup_dists

            alldists = all_powerup_dists()

            for x in alldists.keys():
                dist_choice[0].append(x)
                dist_choice[1].append(
                    bui.Lstr(resource=f"{suffix}{alldists.get(x)[1]}.t")
                )

            pp = popup.PopupMenu(  # hehe, pp
                parent=self._root_widget,
                position=(s_pos_x - 75, s_pos_y),
                width=150,
                scale=self.popup_menu_scale,
                choices=dist_choice[0],
                choices_display=dist_choice[1],
                current_choice=bse.cfg.fetch("powerup_dist"),
                on_value_change_call=self._set_powerup_dist,
            )
            s_pos_y -= 14.5
            buttonsub = self._powerupdistdesc = bui.textwidget(
                parent=self._root_widget,
                position=(s_pos_x, s_pos_y),
                size=(0, 0),
                text="",
                scale=0.7,
                res_scale=1.5,
                maxwidth=425,
                color=(0.4, 0.865, 0.74),
                h_align="center",
                v_align="center",
            )
            psub_w = self.width / 1.9
            psub_h = self.width / 3.5
            s_pos_y -= 12.5 + psub_h
            self._powerupsuba = bui.scrollwidget(
                parent=self._root_widget,
                color=(0.1, 0.85, 0.45),
                highlight=True,
                autoselect=True,
                position=(s_pos_x - (psub_w / 2) + 2.5, s_pos_y - (tyoff * 6)),
                size=(0, 0),
                simple_culling_v=10.0,
                claims_up_down=True,
                claims_tab=True,
                selection_loops_to_parent=True,
                capture_arrows=True,
            )
            self._update_powerup_container(bse.cfg.fetch('powerup_dist'))
        elif self._section == 1:
            # Gameplay subtitle
            bui.textwidget(
                edit=self._subtitle,
                text=bui.Lstr(resource=self._r + ".Gameplay"),
            )

            # Quickturn
            qt = self._build_setting(
                position=(s_pos_x, s_pos_y),
                title=bui.Lstr(resource=f"{self._r}.quickturn.name"),
                subtitle=bui.Lstr(resource=f"{self._r}.quickturn.sub"),
                key="quickturn",
            )
            s_pos_y -= 67.5
            bui.widget(edit=self._backbtn, down_widget=qt.get_button())

            # Chaos Mode
            cm = self._build_setting(
                position=(s_pos_x, s_pos_y),
                title=bui.Lstr(resource=f"{self._r}.chaos.name"),
                subtitle=bui.Lstr(resource=f"{self._r}.chaos.sub"),
                key="chaos.enabled",
                default=False,
            )
            s_pos_y -= 67.5
            bui.buttonwidget(
                edit=cm.get_button(),
                label=bui.Lstr(resource="configureText"),
                on_activate_call=self._chaos_press,
            )

            # Cutscene Skip
            thk = f"{self._r}.skipscene.choices"
            cts = self._build_setting(
                position=(s_pos_x, s_pos_y),
                title=bui.Lstr(resource=f"{self._r}.skipscene.name"),
                subtitle=bui.Lstr(resource=f"{self._r}.skipscene.sub"),
                key="skip_cutscenes",
                choices_display=[
                    bui.Lstr(resource=f"{thk}.y"),
                    bui.Lstr(resource=f"{thk}.n"),
                ],
                default=False,
            )
            s_pos_y -= 67.5

        elif self._section == 2:
            # Customization subtitle
            bui.textwidget(
                edit=self._subtitle,
                text=bui.Lstr(resource=self._r + ".Customization"),
            )

            # Menu Theme
            thk = f"{self._r}.menuTheme.themes"
            mt = self._build_setting(
                position=(s_pos_x, s_pos_y),
                title=bui.Lstr(resource=f"{self._r}.menuTheme.name"),
                subtitle=bui.Lstr(resource=f"{self._r}.menuTheme.sub"),
                key="menu_theme",
                default="Classic",
                choices=[
                    "Classic",
                    "Adventure",
                    "Island",
                    "Forest",
                    "Mountain",
                    "Spooky",
                ],
                choices_display=[
                    bui.Lstr(resource=f"{thk}.00"),
                    bui.Lstr(resource=f"{thk}.01"),
                    bui.Lstr(resource=f"{thk}.02"),
                    bui.Lstr(resource=f"{thk}.03"),
                    bui.Lstr(resource=f"{thk}.04"),
                    bui.Lstr(resource=f"{thk}.05"),
                ],
                on_change_call=self._changed_theme,
            )
            s_pos_y -= 67.5

            # BSE Particles
            thk = f"{self._r}.bseParticles.choices"
            bsep = self._build_setting(
                position=(s_pos_x, s_pos_y),
                title=bui.Lstr(resource=f"{self._r}.bseParticles.name"),
                subtitle=bui.Lstr(resource=f"{self._r}.bseParticles.sub"),
                key="particle_custom",
                default="Max",
                choices=["Max", "Min", "None"],
                choices_display=[
                    bui.Lstr(resource=f"{thk}.00"),
                    bui.Lstr(resource=f"{thk}.01"),
                    bui.Lstr(resource=f"{thk}.02"),
                ],
            )
            s_pos_y -= 67.5

            # Reduced Particles
            rp = self._build_setting(
                position=(s_pos_x, s_pos_y),
                title=bui.Lstr(resource=f"{self._r}.reducedParticles.name"),
                subtitle=bui.Lstr(resource=f"{self._r}.reducedParticles.sub"),
                key="particle_redux",
                default=False,
            )
            s_pos_y -= 67.5

            # Announcer
            an = self._build_setting(
                position=(s_pos_x, s_pos_y),
                title=bui.Lstr(resource=self._r + ".announceGame.name"),
                subtitle=bui.Lstr(resource=self._r + ".announceGame.sub"),
                key="game_announcer",
                default=False,
            )
            s_pos_y -= 67.5

    def _set_powerup_dist(self, v: str) -> None:
        bse.cfg.write('powerup_dist', v)
        self._update_powerup_container(v)

    def _update_powerup_container(self, dist: str) -> None:
        """
        Removes all items from the powerup subcontainer and adds new
        ones representing the selected powerup distribution
        """
        from bascenev1._powerup import all_powerup_dists

        distlist = all_powerup_dists().get(dist)[0]

        def return_current_selection_description(pointer: str) -> str:
            try:
                return (
                    self._r
                    + f".powerupDist.dists.{all_powerup_dists().get(pointer)[1]}.d"
                )
            except:
                return self._r + f".powerupDist.dists.??.d"

        sub = self._powerupsuba
        psub_w = self.width / 1.9
        psub_h = self.width / 3.5
        tyoff = -25 if bui.app.ui_v1.uiscale is bui.UIScale.SMALL else 0

        bui.scrollwidget(edit=sub, size=(psub_w, psub_h + (tyoff * 6)))

        bui.textwidget(
            edit=self._powerupdistdesc,
            text=bui.Lstr(resource=return_current_selection_description(dist)),
        )
        for x in sub.get_children():
            x.delete()

        # Proper subcontainer
        subc = bui.containerwidget(
            parent=sub, size=(psub_w, psub_h - 20), background=False
        )

        from bascenev1lib.actor.powerupbox import poweruptex

        alltex = poweruptex()

        # Bunch of positioning stuff
        self.prevscale = scale = 30
        pd = 5
        padding = scale + pd
        row_pad = scale / 2
        wrap_at = psub_w // (scale + (scale * 0.25))
        icopos_x = icostart_x = (psub_w / 2) - (
            (scale / 6) + ((padding * wrap_at - 1) / 2)
        )
        cont_off = max(
            ((padding + row_pad) * (len(alltex.keys()) // wrap_at)) - psub_h,
            psub_h - 20,
        )
        bias = 150
        icopos_y = icostart_y = (
            psub_h - (padding) + cont_off + (tyoff * 6 * 2.35) - bias
        )

        bui.containerwidget(
            edit=subc,
            size=(
                psub_w,
                psub_h + cont_off + (tyoff * 6 * 2.35) - bias,
            ),
        )

        n = 0
        btnl: list = []
        for x in enumerate(alltex.keys()):
            # Create powerup image
            me = next((ogo for ogo in distlist if ogo[0] == x[1]), None)
            c = bui.imagewidget(
                parent=subc,
                size=(scale, scale),
                position=(icopos_x, icopos_y),
                texture=alltex.get(x[1]),
            )

            weightval = bui.textwidget(
                parent=subc,
                position=(icopos_x + (scale * 0.5), icopos_y + (scale * 0.4)),
                scale=0.65,
                text=str(me[1]),
                color=(
                    (1, 1, 1, 0.7) if not me[1] == 0 else (0.7, 0.7, 0.7, 0.5)
                ),
                h_align="left",
                v_align="center",
            )

            def indicator_text() -> str:
                return bui.Lstr(
                    resource=f'{self._r}.powerupDist.rarity.{"{:02d}".format(me[1])}'
                )

            indicate = bui.textwidget(
                parent=subc,
                position=(
                    icopos_x + (-2 * (45 * 3.3 / self.prevscale)),
                    icopos_y
                    - (row_pad * 1.15)
                    - ((45 / self.prevscale) - 1) * 3.3,
                ),
                scale=0.55 * (self.prevscale / 45),
                maxwidth=self.prevscale,
                text=indicator_text(),
                color=(1, 1, 1),
                h_align="center",
                v_align="center",
            )

            if me[1] == 0:
                bui.imagewidget(
                    edit=c,
                    color=(0.15, 0.275, 0.15),
                )

            # Add a button widget every row for easier scrolling
            if n == 0:
                btnl.append(
                    bui.buttonwidget(
                        parent=subc,
                        label="",
                        size=(0, 0),
                        position=(icopos_x, icopos_y + (self.prevscale * 0.77)),
                        enable_sound=False,
                        texture=bui.gettexture("neoSpazIcon"),
                    )
                )

            n += 1
            icopos_x += padding

            # If we reach our wrapping point, go to our default positions minus some y axis
            if n == wrap_at:
                n = 0
                icopos_x = icostart_x
                icopos_y -= padding + row_pad

        ## [!] Apparently this causes a memory leak... Do not
        ## Make our dist. button travel down to the subcontainer safe and sound
        # bui.widget(
        #        edit=pp.get_button(),
        #        down_widget=subc,
        #    )

        ## Wire our travel buttons so we don't loop around & select to the dist. button once we scroll all the way up
        # bui.buttonwidget( # Up to Dist. button
        #    edit=btnl[0],
        #    up_widget=pp.get_button(),
        # )
        bui.buttonwidget(  # Down to itself or travel arrows
            edit=btnl[-1],
            down_widget=(
                self.travel_buttons[0]
                if len(self.travel_buttons) != 0
                else btnl[-1]
            ),
        )

    def _back(self) -> None:
        from bse.ui.settings import allsettings

        bui.containerwidget(
            edit=self._root_widget, transition=self._transition_out
        )
        if self._has_changed_theme:
            import bascenev1
            from bascenev1lib.mainmenu import MainMenuSession

            bui.app.ui_v1.set_main_menu_location("Settings Window")
            bascenev1.new_host_session(MainMenuSession)
        else:
            bui.app.ui_v1.set_main_menu_window(
                allsettings.AllSettingsWindow(
                    transition="in_left"
                ).get_root_widget(),
                from_window=False
            )

    def _travel(self, left_right: int) -> None:
        left_right = -1 if left_right == 0 else 1
        out = min(max(self._section + left_right, 0), self.tab_amount)
        if self._section != out:
            self._section = section["last"] = out
            self.refresh()

    def _chaos_press(self) -> None:
        from bse.ui.settings.chaospopup import ChaosSettingsPopupWindow

        assert self._chaos_mode_button
        ChaosSettingsPopupWindow(scale_origin=((0, 0)))

    def _changed_theme(self) -> None:
        """Tells our menu we have changed themes."""
        self._has_changed_theme = True

    def _build_setting(
        self,
        position: tuple[float, float],
        title: str | any,
        subtitle: str | None = None,
        key: str = "BSE: Generic Setting",
        default: any = True,
        choices: list | None = None,
        choices_display: list | None = None,
        theme_choices_display: list | None = None,
        on_change_call: any | None = None,
    ) -> popup.PopupMenu:

        # Default to True & False settings if not assigned
        if not choices:
            choices = [True, False]
        if not choices_display:
            choices_display = [
                bui.Lstr(resource=self._r + ".generic.enabled"),
                bui.Lstr(resource=self._r + ".generic.disabled"),
            ]
        if not theme_choices_display:
            theme_choices_display = [
                bui.Lstr(resource=self._r + ".theme.classic"),
                bui.Lstr(resource=self._r + ".theme.adventure"),
            ]

        # Position stuff
        global_offset = 105
        title_position = (
            position[0] - global_offset,
            position[1] - (12.5 if not subtitle else 0),
        )
        sub_position = (position[0] - global_offset, position[1] - 25)
        btn_position = (position[0] + global_offset - 75, position[1] - 35)

        # Title
        bui.textwidget(
            parent=self._root_widget,
            position=title_position,
            size=(0, 0),
            text=title,
            scale=0.75,
            res_scale=1.5,
            maxwidth=250,
            color=bui.app.ui_v1.infotextcolor,
            h_align="center",
            v_align="center",
        )

        # Subtitle if it exists
        if subtitle:
            bui.textwidget(
                parent=self._root_widget,
                position=sub_position,
                size=(0, 0),
                text=subtitle,
                scale=0.6,
                res_scale=1.5,
                maxwidth=250,
                color=(0.7, 0.7, 0.7),
                h_align="center",
                v_align="center",
            )

        bse.cfg.fetch(key, default, do_set=True)

        def generic_save(v):
            bse.cfg.write(key, v)

            if on_change_call:
                on_change_call()

        # Popup button
        return popup.PopupMenu(
            parent=self._root_widget,
            position=btn_position,
            width=150,
            scale=self.popup_menu_scale,
            choices=choices,
            choices_display=choices_display,
            current_choice=bse.cfg.fetch(key),
            on_value_change_call=generic_save,
        )
