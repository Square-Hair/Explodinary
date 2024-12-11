# Released under the MIT License. See LICENSE for details.
#
"""UI for browsing available co-op levels/games/etc."""
# FIXME: Break this up.
# pylint: disable=too-many-lines

from __future__ import annotations

from typing import TYPE_CHECKING

import bascenev1 as bs
import bauiv1 as bui
import random
from bauiv1lib.coop import tips

if TYPE_CHECKING:
    from typing import Any

from explodinary import loader, _versiondata


class BSECoopBrowserWindow(bui.Window):
    """Window for browsing co-op levels/games/etc."""

    def __init__(
        self,
        transition: str | None = "in_right",
        origin_widget: bui.Widget | None = None,
    ):
        # pylint: disable=too-many-statements
        # pylint: disable=cyclic-import
        import threading

        # Preload some modules we use in a background thread so we won't
        # have a visual hitch when the user taps them.
        threading.Thread(target=self._preload_modules).start()

        bui.set_analytics_screen("BSE Coop Window")

        app = bui.app
        cfg = app.config

        # If they provided an origin-widget, scale up from that.
        scale_origin: tuple[float, float] | None
        if origin_widget is not None:
            self._transition_out = "out_scale"
            scale_origin = origin_widget.get_screen_space_center()
            transition = "in_scale"
        else:
            self._transition_out = "out_right"
            scale_origin = None

        # Try to recreate the same number of buttons we had last time so our
        # re-selection code works.
        self._tournament_button_count = app.config.get("Tournament Rows", 0)
        assert isinstance(self._tournament_button_count, int)

        self._plot_button: bui.Widget | None = None
        self._campaign_percent_text: bui.Widget | None = None

        uiscale = bui.app.ui_v1.uiscale
        self._width = 1320 if uiscale is bui.UIScale.SMALL else 1120
        self._x_inset = x_inset = 100 if uiscale is bui.UIScale.SMALL else 0
        self._height = (
            757
            if uiscale is bui.UIScale.SMALL
            else 830 if uiscale is bui.UIScale.MEDIUM else 900
        )
        app.ui.set_main_menu_location("BSE Coop Select")
        self._r = "coopSelectWindow"
        top_extra = 20 if uiscale is bui.UIScale.SMALL else 0

        self._tourney_data_up_to_date = False

        self._campaign_difficulty = bui.internal.get_v1_account_misc_val(
            "campaignDifficulty", "easy"
        )

        super().__init__(
            root_widget=bui.containerwidget(
                size=(self._width, self._height + top_extra),
                color=(0.1, 0.4, 0.3),
                toolbar_visibility="menu_full",
                scale_origin_stack_offset=scale_origin,
                stack_offset=(
                    (0, -15)
                    if uiscale is bui.UIScale.SMALL
                    else (0, 0) if uiscale is bui.UIScale.MEDIUM else (0, 0)
                ),
                transition=transition,
                scale=(
                    1.2
                    if uiscale is bui.UIScale.SMALL
                    else 0.8 if uiscale is bui.UIScale.MEDIUM else 0.75
                ),
            )
        )

        if app.ui.use_toolbars and uiscale is bui.UIScale.SMALL:
            self._back_button = None
        else:
            self._back_button = bui.buttonwidget(
                parent=self._root_widget,
                position=(
                    75 + x_inset,
                    self._height
                    - 87
                    - (49 if uiscale is bui.UIScale.SMALL else 0),
                ),
                size=(120, 60),
                scale=1.2,
                autoselect=True,
                label=bui.Lstr(resource="backText"),
                button_type="back",
            )

        self._last_tournament_query_time: float | None = None
        self._last_tournament_query_response_time: float | None = None
        self._doing_tournament_query = False

        self._selected_campaign_level = cfg.get(
            "Selected Coop Campaign Level", None
        )
        self._selected_custom_level = cfg.get(
            "Selected Coop Custom Level", None
        )

        # Don't want initial construction affecting our last-selected.
        self._do_selection_callbacks = False
        v = self._height - 95
        txt = bui.textwidget(
            parent=self._root_widget,
            position=(
                self._width * 0.5,
                v + 40 - (49 if uiscale is bui.UIScale.SMALL else 0),
            ),
            size=(0, 0),
            text=bui.Lstr(
                resource="playModes.bseBrowserText",
                fallback_resource="playModes.coopText",
            ),
            h_align="center",
            color=app.ui.title_color,
            scale=1.5,
            maxwidth=500,
            v_align="center",
        )

        if app.ui.use_toolbars and uiscale is bui.UIScale.SMALL:
            bui.textwidget(edit=txt, text="")

        if self._back_button is not None:
            bui.buttonwidget(
                edit=self._back_button,
                button_type="backSmall",
                size=(60, 50),
                label=bui.charstr(bui.SpecialChar.BACK),
            )

        self._selected_row = cfg.get("Selected Coop Row", None)

        self.star_tex = bui.gettexture("star")
        self.point_tex = bui.gettexture("point")
        self.lsbt = bui.getmodel("level_select_button_transparent")
        self.lsbo = bui.getmodel("level_select_button_opaque")
        self.a_outline_tex = bui.gettexture("achievementOutline")
        self.a_outline_model = bui.getmodel("achievementOutline")

        self._scroll_width = self._width - (130 + 2 * x_inset)
        self._scroll_height = self._height - (
            261 if uiscale is bui.UIScale.SMALL else 160
        )
        self._subcontainerwidth = 800.0
        self._subcontainerheight = 1600.0

        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            highlight=False,
            position=(
                (65 + x_inset, 120)
                if uiscale is bui.UIScale.SMALL
                else (65 + x_inset, 70)
            ),
            size=(self._scroll_width, self._scroll_height),
            simple_culling_v=10.0,
            claims_left_right=True,
            claims_tab=True,
            selection_loops_to_parent=True,
        )
        self._subcontainer: bui.Widget | None = None

        # Take note of our account state; we'll refresh later if this changes.
        self._account_state_num = bui.internal.get_v1_account_state_num()

        # Same for fg/bg state.
        self._fg_state = app.fg_state

        self._refresh()
        self._restore_state()

        # Even though we might display cached tournament data immediately, we
        # don't consider it valid until we've pinged.
        # the server for an update
        self._tourney_data_up_to_date = False

        # If we've got a cached tournament list for our account and info for
        # each one of those tournaments, go ahead and display it as a
        # starting point.
        if (
            app.accounts_v1.account_tournament_list is not None
            and app.accounts_v1.account_tournament_list[0]
            == bui.internal.get_v1_account_state_num()
            and all(
                t_id in app.accounts_v1.tournament_info
                for t_id in app.accounts_v1.account_tournament_list[1]
            )
        ):
            tourney_data = [
                app.accounts_v1.tournament_info[t_id]
                for t_id in app.accounts_v1.account_tournament_list[1]
            ]
            self._update_for_data(tourney_data)

        # This will pull new data periodically, update timers, etc.
        self._update_timer = bui.Timer(
            1.0,
            bui.WeakCall(self._update),
            timetype=bui.TimeType.REAL,
            repeat=True,
        )
        self._update()

    # noinspection PyUnresolvedReferences
    @staticmethod
    def _preload_modules() -> None:
        """Preload modules we use (called in bg thread)."""

    def _update(self) -> None:
        # Do nothing if we've somehow outlived our actual UI.
        if self._root_widget:
            return

        cur_time = bui.time(bui.TimeType.REAL)

        # If its been a while since we got a tournament update, consider the
        # data invalid (prevents us from joining tournaments if our internet
        # connection goes down for a while).
        if (
            self._last_tournament_query_response_time is None
            or bui.time(bui.TimeType.REAL)
            - self._last_tournament_query_response_time
            > 60.0 * 2
        ):
            self._tourney_data_up_to_date = False

        # If our account state has changed, do a full request.
        account_state_num = bui.internal.get_v1_account_state_num()
        if account_state_num != self._account_state_num:
            self._account_state_num = account_state_num
            self._save_state()
            self._refresh()

            # Also encourage a new tournament query since this will clear out
            # our current results.
            if not self._doing_tournament_query:
                self._last_tournament_query_time = None

        # If we've been backgrounded/foregrounded, invalidate our
        # tournament entries (they will be refreshed below asap).
        if self._fg_state != bui.app.fg_state:
            self._tourney_data_up_to_date = False

        # Send off a new tournament query if its been long enough or whatnot.
        if not self._doing_tournament_query and (
            self._last_tournament_query_time is None
            or cur_time - self._last_tournament_query_time > 30.0
            or self._fg_state != bui.app.fg_state
        ):
            self._fg_state = bui.app.fg_state
            self._last_tournament_query_time = cur_time
            self._doing_tournament_query = True
            bui.internal.tournament_query(
                args={"source": "coop window refresh", "numScores": 1},
                callback=bui.WeakCall(self._on_tournament_query_response),
            )

        # Decrement time on our tournament buttons.
        ads_enabled = bui.internal.have_incentivized_ad()
        for tbtn in self._tournament_buttons:
            tbtn.time_remaining = max(0, tbtn.time_remaining - 1)
            if tbtn.time_remaining_value_text is not None:
                bui.textwidget(
                    edit=tbtn.time_remaining_value_text,
                    text=(
                        bui.timestring(
                            tbtn.time_remaining,
                            centi=False,
                            suppress_format_warning=True,
                        )
                        if (
                            tbtn.has_time_remaining
                            and self._tourney_data_up_to_date
                        )
                        else "-"
                    ),
                )

            # Also adjust the ad icon visibility.
            if tbtn.allow_ads and bui.internal.has_video_ads():
                bui.imagewidget(
                    edit=tbtn.entry_fee_ad_image,
                    opacity=1.0 if ads_enabled else 0.25,
                )
                bui.textwidget(
                    edit=tbtn.entry_fee_text_remaining,
                    color=(0.6, 0.6, 0.6, 1 if ads_enabled else 0.2),
                )

        self._update_hard_mode_lock_image()

    def _update_hard_mode_lock_image(self) -> None:
        try:
            bui.imagewidget(
                edit=self._hard_button_lock_image,
                opacity=0.0 if bui.app.accounts_v1.have_pro_options() else 1.0,
            )
        except Exception:
            bui.print_exception("Error updating campaign lock.")

    def _update_for_data(self, data: list[dict[str, Any]] | None) -> None:

        # If the number of tournaments or challenges in the data differs from
        # our current arrangement, refresh with the new number.
        if (data is None and self._tournament_button_count != 0) or (
            data is not None and (len(data) != self._tournament_button_count)
        ):
            self._tournament_button_count = len(data) if data is not None else 0
            bui.app.config["Tournament Rows"] = self._tournament_button_count
            self._refresh()

        # Update all of our tourney buttons based on whats in data.
        for i, tbtn in enumerate(self._tournament_buttons):
            assert data is not None
            tbtn.update_for_data(data[i])

    def _on_tournament_query_response(
        self, data: dict[str, Any] | None
    ) -> None:
        accounts = bui.app.accounts_v1
        if data is not None:
            tournament_data = data["t"]  # This used to be the whole payload.
            self._last_tournament_query_response_time = bui.time(
                bui.TimeType.REAL
            )
        else:
            tournament_data = None

        # Keep our cached tourney info up to date.
        if data is not None:
            self._tourney_data_up_to_date = True
            accounts.cache_tournament_info(tournament_data)

            # Also cache the current tourney list/order for this account.
            accounts.account_tournament_list = (
                bui.internal.get_v1_account_state_num(),
                [e["tournamentID"] for e in tournament_data],
            )

        self._doing_tournament_query = False
        self._update_for_data(tournament_data)

    def _refresh_campaign_row(self) -> None:
        # pylint: disable=too-many-locals
        # pylint: disable=cyclic-import
        from bauiv1lib.coop.gamebutton import GameButton

        parent_widget = self._campaign_sub_container
        w_parent = self._subcontainer

        # Clear out anything in the parent widget already.
        for child in parent_widget.get_children():
            child.delete()

        h = 0
        v2 = -2

        self._plot_button = bui.buttonwidget(
            parent=parent_widget,
            label=bui.Lstr(resource="explodinary.plotButtonText"),
            size=(120, 70),
            text_scale=1,
            position=(h + 30, v2 + 80),
            button_type="square",
            color=(0.3, 0.5, 0.8),
            textcolor=(0.8, 0.8, 1, 1.0),
            autoselect=True,
            up_widget=self._campaign_h_scroll,
            on_activate_call=self._on_plot_info_press,
        )

        # self._speedrun_button = bui.buttonwidget(
        #    parent=w_parent,
        #    label=bui.Lstr(resource='explodinary.speedrunModeText'),
        #    size=(210, 35),
        #    text_scale=0.85,
        #    position=(730, 560),
        #    color=(0.9, 0.8, 0.25),
        #    textcolor=(1, 1, 0.8),
        #    autoselect=True,
        #    up_widget=self._campaign_h_scroll,
        #    on_activate_call=self._on_plot_info_press,
        # )

        h_spacing = 200
        campaign_buttons = []
        campaignname = _versiondata.campaignsub
        items = loader.campaign_levels
        if self._selected_campaign_level is None:
            self._selected_campaign_level = items[0]
        h = 160
        for i in items:
            is_last_sel = i == self._selected_campaign_level
            campaign_buttons.append(
                GameButton(
                    self, parent_widget, i, h, v2, is_last_sel, "campaign"
                ).get_button()
            )
            h += h_spacing

        for btn in campaign_buttons:
            bui.Widget(
                edit=btn,
                up_widget=self._back_button,
                down_widget=self._chaos_mode_button,
            )

        # Update our existing percent-complete text.
        campaign = bui.app.classic.getcampaign(campaignname)
        levels = campaign.levels
        levels_complete = sum((1 if l.complete else 0) for l in levels)

        # Last level cant be completed; hence the -1.
        progress = min(1.0, float(levels_complete) / (len(levels) - 1))
        p_str = str(int(progress * 100.0)) + "%"

        self._campaign_percent_text = bui.textwidget(
            edit=self._campaign_percent_text,
            text=bui.Lstr(
                value="${C} (${P})",
                subs=[
                    ("${C}", bui.Lstr(resource=self._r + ".campaignText")),
                    ("${P}", p_str),
                ],
            ),
        )

    def _on_plot_info_press(self) -> None:
        # pylint: disable=cyclic-import
        from bauiv1lib.confirm import ConfirmWindow

        txt = bui.Lstr(resource="explodinary.plotText")
        ConfirmWindow(
            txt,
            text_scale=2,
            cancel_button=False,
            width=550,
            height=260,
            origin_widget=self._plot_button,
        )

    def _refresh(self) -> None:
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals
        # pylint: disable=cyclic-import
        from bauiv1lib.coop.gamebutton import GameButton
        from bauiv1lib.coop.tournamentbutton import TournamentButton

        # (Re)create the sub-container if need be.
        if self._subcontainer is not None:
            self._subcontainer.delete()

        uiscale = bui.app.ui_v1.uiscale

        yoff = 0

        self._subcontainerheight = 620 + (
            90 if uiscale is bui.UIScale.SMALL else 0
        )

        self._subcontainer = bui.containerwidget(
            parent=self._scrollwidget,
            size=(self._subcontainerwidth, self._subcontainerheight + yoff),
            background=False,
            claims_left_right=True,
            claims_tab=True,
            selection_loops_to_parent=True,
        )

        bui.containerwidget(
            edit=self._root_widget, selected_child=self._scrollwidget
        )
        if self._back_button is not None:
            bui.containerwidget(
                edit=self._root_widget, cancel_button=self._back_button
            )

        w_parent = self._subcontainer
        h_base = 6

        v = self._subcontainerheight - 73

        # TIPS AND TRIVIA

        from explodinary.lib import bseconfig

        _is_chaos = bseconfig.chaos_get("Enabled")

        tipspool: list = []
        keys: list = ["tips", "trivia"]
        if _is_chaos:
            keys.extend(["chaos_tips", "chaos_trivia"])

        for key in keys:
            tipspref = []
            cpool = tips.bse[key]
            for tip in cpool["tips"]:
                tipspref.append(f'{cpool["codename"]}{tip}')
            tipspool.extend(tipspref)

        def pick_tip() -> dict:
            tip = random.choice(tipspool)

            prefix = tip[:4]
            is_chaos = bool(prefix in ["CTI:", "CTR:"])

            if tip[-4:] == ":WIN":  #:WIN windows check
                if not bui.app.platform == "windows":
                    tip = pick_tip()
                else:
                    tip = tip[:-4]

            return {
                "prefix": bui.Lstr(
                    resource=f"explodinary.bsebrowser.{prefix}.header"
                ),
                "text": bui.Lstr(translate=(f"bsetiptrans.{prefix}", tip[4:])),
                "chaos": is_chaos,
            }

        tip = pick_tip()
        txt = bui.Lstr(
            value="${A}\n${B}",
            subs=[
                ("${A}", tip["prefix"]),
                ("${B}", tip["text"]),
            ],
        )
        color = (1, 0.75, 1) if tip["chaos"] else (1, 1, 0.75)

        t_width = bui.internal.get_string_width(txt, suppress_warning=True)
        tipoff = 90 if uiscale is bui.UIScale.SMALL else 0
        bui.textwidget(
            parent=w_parent,
            position=(490, 265 + yoff + tipoff),
            size=(0, 0),
            text=txt,
            h_align="center",
            v_align="center",
            maxwidth=800,
            color=color,
            scale=1.1,
        )

        self._campaign_percent_text = bui.textwidget(
            parent=w_parent,
            position=(h_base + 27, v + 30 + yoff),
            size=(0, 0),
            text="",
            h_align="left",
            v_align="center",
            color=bui.app.ui_v1.title_color,
            scale=1.1,
        )

        row_v_show_buffer = 100
        v -= 198

        h_scroll = bui.hscrollwidget(
            parent=w_parent,
            size=(self._scroll_width - 10, 205),
            position=(-5, v),
            simple_culling_h=70,
            highlight=False,
            border_opacity=0.0,
            color=(0.45, 0.4, 0.5),
            on_select_call=lambda: self._on_row_selected("campaign"),
        )
        self._campaign_h_scroll = h_scroll
        bui.Widget(
            edit=h_scroll,
            show_buffer_top=row_v_show_buffer,
            show_buffer_bottom=row_v_show_buffer,
            autoselect=True,
        )
        if self._selected_row == "campaign":
            bui.containerwidget(
                edit=w_parent, selected_child=h_scroll, visible_child=h_scroll
            )
        bui.containerwidget(edit=h_scroll, claims_left_right=True)
        self._campaign_sub_container = bui.containerwidget(
            parent=h_scroll, size=(180 + 160 * 10, 200), background=False
        )

        self._chaos_mode_button = bui.buttonwidget(
            parent=w_parent,
            position=(730, v - 230),
            size=(210, 35),
            on_activate_call=bui.WeakCall(self._chaos_press),
            autoselect=True,
            textcolor=(1, 0.75, 1),
            color=(1.2, 0.4, 1.1),
            label=bui.Lstr(resource="explodinary.chaosModeText"),
        )

        # Tournaments

        self._tournament_buttons: list = []

        # v -= 291
        v -= 441

        # Custom Games. (called 'Practice' in UI these days).
        bui.textwidget(
            parent=w_parent,
            position=(h_base + 27, v + 30 + 198),
            size=(0, 0),
            text=bui.Lstr(
                resource="explodinary.additionalText",
                fallback_resource="coopSelectWindow.customText",
            ),
            h_align="left",
            v_align="center",
            color=bui.app.ui_v1.title_color,
            scale=1.1,
        )

        # If we've defined custom games, put them at the beginning.
        items = loader.custom_levels

        self._custom_h_scroll = custom_h_scroll = h_scroll = bui.hscrollwidget(
            parent=w_parent,
            size=(self._scroll_width - 10, 205),
            position=(-5, v),
            highlight=False,
            border_opacity=0.0,
            color=(0.45, 0.4, 0.5),
            on_select_call=bui.Call(self._on_row_selected, "custom"),
        )
        bui.Widget(
            edit=h_scroll,
            show_buffer_top=row_v_show_buffer,
            show_buffer_bottom=1.5 * row_v_show_buffer,
            autoselect=True,
        )
        if self._selected_row == "custom":
            bui.containerwidget(
                edit=w_parent, selected_child=h_scroll, visible_child=h_scroll
            )
        bui.containerwidget(edit=h_scroll, claims_left_right=True)
        sc2 = bui.containerwidget(
            parent=h_scroll,
            size=(max(self._scroll_width - 24, 30 + 200 * len(items)), 200),
            background=False,
        )
        h_spacing = 200
        self._custom_buttons: list[GameButton] = []
        h = 0
        v2 = -2
        for item in items:
            is_last_sel = item == self._selected_custom_level
            self._custom_buttons.append(
                GameButton(
                    self, sc2, item, h, v2, is_last_sel, "custom"
                ).get_button()
            )
            h += h_spacing

        for btn in self._custom_buttons:
            bui.Widget(edit=btn, up_widget=self._chaos_mode_button)

        # We can't fill in our campaign row until tourney buttons are in place.
        # (for wiring up)
        self._refresh_campaign_row()

        if self._back_button is not None:
            bui.buttonwidget(
                edit=self._back_button, on_activate_call=self._back
            )
        else:
            bui.containerwidget(
                edit=self._root_widget, on_cancel_call=self._back
            )

        # There's probably several 'onSelected' callbacks pushed onto the
        # event queue.. we need to push ours too so we're enabled *after* them.
        bui.pushcall(self._enable_selectable_callback)

    def _chaos_press(self) -> None:
        from bse.ui.settings.chaospopup import ChaosSettingsPopupWindow

        assert self._chaos_mode_button
        ChaosSettingsPopupWindow(scale_origin=((0, 0)))

    def _on_row_selected(self, row: str) -> None:
        if self._do_selection_callbacks:
            if self._selected_row != row:
                self._selected_row = row

    def _enable_selectable_callback(self) -> None:
        self._do_selection_callbacks = True

    def run_game(self, game: str) -> None:
        """Run the provided game."""
        # pylint: disable=too-many-branches
        # pylint: disable=cyclic-import
        from bauiv1lib.confirm import ConfirmWindow
        from bauiv1lib.purchase import PurchaseWindow
        from bauiv1lib.account import show_sign_in_prompt

        args: dict[str, Any] = {}

        if game == "Easy:The Last Stand":
            ConfirmWindow(
                bui.Lstr(
                    resource="difficultyHardUnlockOnlyText",
                    fallback_resource="difficultyHardOnlyText",
                ),
                cancel_button=False,
                width=460,
                height=130,
            )
            return

        # Infinite onslaught/runaround require pro; bring up a store link
        # if need be.
        if (
            game
            in (
                "Challenges:Infinite Runaround",
                "Challenges:Infinite Onslaught",
            )
            and not bui.app.accounts_v1.have_pro()
        ):
            if bui.internal.get_v1_account_state() != "signed_in":
                show_sign_in_prompt()
            else:
                PurchaseWindow(items=["pro"])
            return

        required_purchase: str | None
        if game in ["Challenges:Meteor Shower"]:
            required_purchase = "games.meteor_shower"
        elif game in [
            "Challenges:Target Practice",
            "Challenges:Target Practice B",
        ]:
            required_purchase = "games.target_practice"
        elif game in ["Challenges:Ninja Fight"]:
            required_purchase = "games.ninja_fight"
        elif game in ["Challenges:Pro Ninja Fight"]:
            required_purchase = "games.ninja_fight"
        elif game in [
            "Challenges:Easter Egg Hunt",
            "Challenges:Pro Easter Egg Hunt",
        ]:
            required_purchase = "games.easter_egg_hunt"
        else:
            required_purchase = None

        if required_purchase is not None and not bui.internal.get_purchased(
            required_purchase
        ):
            if bui.internal.get_v1_account_state() != "signed_in":
                show_sign_in_prompt()
            else:
                PurchaseWindow(items=[required_purchase])
            return

        self._save_state()

        if bui.app.launch_coop_game(game, args=args):
            bui.containerwidget(edit=self._root_widget, transition="out_left")

    def _back(self) -> None:
        # pylint: disable=cyclic-import
        from bauiv1lib.play import PlayWindow

        # If something is selected, store it.
        self._save_state()
        bui.containerwidget(
            edit=self._root_widget, transition=self._transition_out
        )
        bui.app.ui_v1.set_main_menu_window(
            PlayWindow(transition="in_left").get_root_widget()
        )

    def _save_state(self) -> None:
        cfg = bui.app.config
        try:
            sel = self._root_widget.get_selected_child()
            if sel == self._back_button:
                sel_name = "Back"
            elif sel == self._scrollwidget:
                sel_name = "Scroll"
            else:
                raise ValueError("unrecognized selection")
            bui.app.ui_v1.window_states[type(self)] = {"sel_name": sel_name}
        except Exception:
            bui.print_exception(f"Error saving state for {self}.")

        cfg["Selected Coop Row"] = self._selected_row
        cfg["Selected Coop Custom Level"] = self._selected_custom_level
        cfg["Selected Coop Campaign Level"] = self._selected_campaign_level
        cfg.commit()

    def _restore_state(self) -> None:
        try:
            sel_name = bui.app.ui_v1.window_states.get(type(self), {}).get(
                "sel_name"
            )
            if sel_name == "Back":
                sel = self._back_button
            elif sel_name == "Scroll":
                sel = self._scrollwidget
            else:
                sel = self._scrollwidget
            bui.containerwidget(edit=self._root_widget, selected_child=sel)
        except Exception:
            bui.print_exception(f"Error restoring state for {self}.")

    def sel_change(self, row: str, game: str) -> None:
        """(internal)"""
        if self._do_selection_callbacks:
            if row == "custom":
                self._selected_custom_level = game
            elif row == "campaign":
                self._selected_campaign_level = game
