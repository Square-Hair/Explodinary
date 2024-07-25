# Released under the MIT License. See LICENSE for details.
#
"""Provides party related UI."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, cast

import ba
import ba.internal
from bastd.ui import popup

if TYPE_CHECKING:
    from typing import Sequence, Any


class PartyWindow(ba.Window):
    """Party list/chat window."""

    def __del__(self) -> None:
        ba.internal.set_party_window_open(False)

    def __init__(self, origin: Sequence[float] = (0, 0)):
        ba.internal.set_party_window_open(True)
        self._r = 'partyWindow'
        self._popup_type: str | None = None
        self._popup_party_member_client_id: int | None = None
        self._popup_party_member_is_host: bool | None = None
        self._width = 350
        uiscale = ba.app.ui.uiscale
        self._height = (
            320
            if uiscale is ba.UIScale.SMALL
            else 280
            if uiscale is ba.UIScale.MEDIUM
            else 400
        )
        super().__init__(
            root_widget=ba.containerwidget(
                size=(self._width, self._height),
                transition='in_scale',
                color = (0.1, 0.55, 0.3),
                parent=ba.internal.get_special_widget('overlay_stack'),
                on_outside_click_call=self.close_with_sound,
                scale_origin_stack_offset=origin,
                scale=(
                    1.8
                    if uiscale is ba.UIScale.SMALL
                    else 1.35
                    if uiscale is ba.UIScale.MEDIUM
                    else 1.0
                ),
                stack_offset=(260, -2)
                if uiscale is ba.UIScale.SMALL
                else (290, 60)
                if uiscale is ba.UIScale.MEDIUM
                else (380, 80),
            )
        )


        from explodinary.game.hub import HubGame
        import _ba
        self._in_hub = isinstance(
            _ba.get_foreground_host_activity(), HubGame
        )

        self._cancel_button = ba.buttonwidget(
            parent=self._root_widget,
            scale=0.7,
            position=(30, self._height - 47),
            size=(50, 50),
            label='',
            on_activate_call=self.close,
            autoselect=True,
            color=(0.1, 0.95, 0.45),
            icon=ba.gettexture('crossOut'),
            iconscale=1.2,
        )
        ba.containerwidget(
            edit=self._root_widget, cancel_button=self._cancel_button
        )

        self._menu_button = ba.buttonwidget(
            parent=self._root_widget,
            scale=0.7,
            position=(self._width - 60, self._height - 47),
            size=(50, 50),
            label='...',
            autoselect=True,
            button_type='square',
            on_activate_call=ba.WeakCall(self._on_menu_button_press),
            color=(0.1, 0.95, 0.45),
            iconscale=1.2,
        )

        info = ba.internal.get_connection_to_host_info()
        if info.get('name', '') != '':
            title = ba.Lstr(value=info['name'])
        else:
            title = ba.Lstr(resource=self._r + '.titleText')

        self._title_text = ba.textwidget(
            parent=self._root_widget,
            scale=0.9,
            color=(0.1, 0.95, 0.45),
            text=title,
            size=(0, 0),
            position=(self._width * 0.5, self._height - 29),
            maxwidth=self._width * 0.7,
            h_align='center',
            v_align='center',
        )

        self._empty_str = ba.textwidget(
            parent=self._root_widget,
            scale=0.75,
            size=(0, 0),
            position=(self._width * 0.5, self._height - 65),
            maxwidth=self._width * 0.85,
            h_align='center',
            v_align='center',
        )

        self._scroll_width = self._width - 50
        self._scrollwidget = ba.scrollwidget(
            parent=self._root_widget,
            size=(self._scroll_width, self._height - 200),
            position=(30, 80),
            color=(0.4, 0.6, 0.3),
        )
        self._columnwidget = ba.columnwidget(
            parent=self._scrollwidget, border=2, margin=0
        )
        ba.widget(edit=self._menu_button, down_widget=self._columnwidget)

        self._muted_text = ba.textwidget(
            parent=self._root_widget,
            position=(self._width * 0.5, self._height * 0.5),
            size=(0, 0),
            h_align='center',
            v_align='center',
            text=ba.Lstr(resource='chatMutedText'),
        )
        self._chat_texts: list[ba.Widget] = []

        # add all existing messages if chat is not muted
        if not ba.app.config.resolve('Chat Muted'):
            self._reload_chat_messages()

        self._text_len_counter = ba.textwidget(
            parent=self._root_widget,
            size=(60, 40),
            position=(240, 66),
            text='0/0',
            maxwidth=473,
            shadow=0.5,
            flatness=0.3,
            v_align='center',
            h_align='right',
            corner_scale=0.4,
            color=(1,1,1,0.4),
        )

        self._text_field = txt = ba.textwidget(
            parent=self._root_widget,
            editable=True,
            max_chars=70,
            size=(320, 40),
            position=(44, 39),
            text='',
            maxwidth=250,
            shadow=0.3,
            flatness=1.0,
            description=ba.Lstr(resource=self._r + '.chatMessageText'),
            autoselect=True,
            v_align='center',
            corner_scale=0.7,
        )
        self._text_field_old: str = '.'

        ba.widget(
            edit=self._scrollwidget,
            autoselect=True,
            left_widget=self._cancel_button,
            up_widget=self._cancel_button,
            down_widget=self._text_field,
        )
        ba.widget(
            edit=self._columnwidget,
            autoselect=True,
            up_widget=self._cancel_button,
            down_widget=self._text_field,
        )
        ba.containerwidget(edit=self._root_widget, selected_child=txt)
        btn = ba.buttonwidget(
            parent=self._root_widget,
            size=(50, 35),
            label=ba.Lstr(resource=self._r + '.sendText'),
            button_type='square',
            autoselect=True,
            color=(0.1, 0.95, 0.45),
            position=(self._width - 70, 35),
            on_activate_call=self._send_chat_message,
        )
        ba.textwidget(edit=txt, on_return_press_call=btn.activate)
        self._name_widgets: list[ba.Widget] = []
        self._roster: list[dict[str, Any]] | None = None
        self._update_timer = ba.Timer(
            1.0,
            ba.WeakCall(self._update),
            repeat=True,
            timetype=ba.TimeType.REAL,
        )

        self._text_len_counter_timer = ba.Timer(0.05, ba.WeakCall(self._update_text_len_counter), repeat=True)

        self._creative_button = self._creative_button_color = None
        if self._in_hub and False:
            self._creative_button_color = (0.66, 0.22, 0.65)
            self._creative_button = ba.buttonwidget(
                                    parent=self._root_widget,
                                    scale=0.7,
                                    position=(self._width - 60 - ((50 + 15) * 0.7), self._height - 47),
                                    size=(50, 50),
                                    icon=ba.gettexture('folder'),
                                    color=self._creative_button_color,
                                    autoselect=True,
                                    button_type='square',
                                    on_activate_call=ba.WeakCall(self._on_creative_menu_press),
                                    iconscale=1.2,
                                    )

        self._update()

    def on_chat_message(self, msg: str) -> None:
        """Called when a new chat message comes through."""
        if not ba.app.config.resolve('Chat Muted'):
            self._add_msg(msg)

    def _add_msg(self, msg: str) -> None:
        txt = ba.textwidget(
            parent=self._columnwidget,
            text=msg,
            h_align='left',
            v_align='center',
            size=(0, 13),
            scale=0.55,
            maxwidth=self._scroll_width * 0.88,
            shadow=0.3,
            flatness=1.0,
        )
        self._chat_texts.append(txt)
        if len(self._chat_texts) > 40:
            first = self._chat_texts.pop(0)
            first.delete()
        ba.containerwidget(edit=self._columnwidget, visible_child=txt)

    def _on_menu_button_press(self) -> None:
        is_muted = ba.app.config.resolve('Chat Muted')
        uiscale = ba.app.ui.uiscale
        popup.PopupMenuWindow(
            position=self._menu_button.get_screen_space_center(),
            scale=(
                2.3
                if uiscale is ba.UIScale.SMALL
                else 1.65
                if uiscale is ba.UIScale.MEDIUM
                else 1.23
            ),
            choices=['unmute' if is_muted else 'mute'],
            choices_display=[
                ba.Lstr(
                    resource='chatUnMuteText' if is_muted else 'chatMuteText'
                )
            ],
            current_choice='unmute' if is_muted else 'mute',
            delegate=self,
        )
        self._popup_type = 'menu'

    def _update(self) -> None:
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-nested-blocks

        # update muted state
        if ba.app.config.resolve('Chat Muted'):
            ba.textwidget(edit=self._muted_text, color=(1, 1, 1, 0.3))
            # clear any chat texts we're showing
            self._reload_chat_messages(load = False)
        else:
            ba.textwidget(edit=self._muted_text, color=(1, 1, 1, 0.0))

        # update roster section
        roster = ba.internal.get_game_roster()
        if roster != self._roster:
            self._roster = roster

            # clear out old
            for widget in self._name_widgets:
                widget.delete()
            self._name_widgets = []
            if not self._roster:
                top_section_height = 60
                ba.textwidget(
                    edit=self._empty_str,
                    text=ba.Lstr(resource=self._r + '.emptyText'),
                )
                ba.scrollwidget(
                    edit=self._scrollwidget,
                    size=(
                        self._width - 50,
                        self._height - top_section_height - 110,
                    ),
                    position=(30, 80),
                )
            else:
                columns = (
                    1
                    if len(self._roster) == 1
                    else 2
                    if len(self._roster) == 2
                    else 3
                )
                rows = int(math.ceil(float(len(self._roster)) / columns))
                c_width = (self._width * 0.9) / max(3, columns)
                c_width_total = c_width * columns
                c_height = 24
                c_height_total = c_height * rows
                for y in range(rows):
                    for x in range(columns):
                        index = y * columns + x
                        if index < len(self._roster):
                            t_scale = 0.65
                            pos = (
                                self._width * 0.53
                                - c_width_total * 0.5
                                + c_width * x
                                - 23,
                                self._height - 65 - c_height * y - 15,
                            )

                            # if there are players present for this client, use
                            # their names as a display string instead of the
                            # client spec-string
                            try:
                                if self._roster[index]['players']:
                                    # if there's just one, use the full name;
                                    # otherwise combine short names
                                    if len(self._roster[index]['players']) == 1:
                                        p_str = self._roster[index]['players'][
                                            0
                                        ]['name_full']
                                    else:
                                        p_str = '/'.join(
                                            [
                                                entry['name']
                                                for entry in self._roster[
                                                    index
                                                ]['players']
                                            ]
                                        )
                                        if len(p_str) > 25:
                                            p_str = p_str[:25] + '...'
                                else:
                                    p_str = self._roster[index][
                                        'display_string'
                                    ]
                            except Exception:
                                ba.print_exception(
                                    'Error calcing client name str.'
                                )
                                p_str = '???'

                            widget = ba.textwidget(
                                parent=self._root_widget,
                                position=(pos[0], pos[1]),
                                scale=t_scale,
                                size=(c_width * 0.85, 30),
                                maxwidth=c_width * 0.85,
                                color=(1, 1, 1) if index == 0 else (1, 1, 1),
                                selectable=True,
                                autoselect=True,
                                click_activate=True,
                                text=ba.Lstr(value=p_str),
                                h_align='left',
                                v_align='center',
                            )
                            self._name_widgets.append(widget)

                            # in newer versions client_id will be present and
                            # we can use that to determine who the host is.
                            # in older versions we assume the first client is
                            # host
                            if self._roster[index]['client_id'] is not None:
                                is_host = self._roster[index]['client_id'] == -1
                            else:
                                is_host = index == 0

                            # FIXME: Should pass client_id to these sort of
                            #  calls; not spec-string (perhaps should wait till
                            #  client_id is more readily available though).
                            ba.textwidget(
                                edit=widget,
                                on_activate_call=ba.Call(
                                    self._on_party_member_press,
                                    self._roster[index]['client_id'],
                                    is_host,
                                    widget,
                                ),
                            )
                            pos = (
                                self._width * 0.53
                                - c_width_total * 0.5
                                + c_width * x,
                                self._height - 65 - c_height * y,
                            )

                            # Make the assumption that the first roster
                            # entry is the server.
                            # FIXME: Shouldn't do this.
                            if is_host:
                                twd = min(
                                    c_width * 0.85,
                                    ba.internal.get_string_width(
                                        p_str, suppress_warning=True
                                    )
                                    * t_scale,
                                )
                                self._name_widgets.append(
                                    ba.textwidget(
                                        parent=self._root_widget,
                                        position=(
                                            pos[0] + twd + 1,
                                            pos[1] - 0.5,
                                        ),
                                        size=(0, 0),
                                        h_align='left',
                                        v_align='center',
                                        maxwidth=c_width * 0.96 - twd,
                                        color=(0.9, 0.8, 0.25),
                                        text=ba.Lstr(
                                            resource=self._r + '.hostText'
                                        ),
                                        scale=0.4,
                                        shadow=0.1,
                                        flatness=1.0,
                                    )
                                )
                ba.textwidget(edit=self._empty_str, text='')
                ba.scrollwidget(
                    edit=self._scrollwidget,
                    size=(
                        self._width - 50,
                        max(100, self._height - 139 - c_height_total),
                    ),
                    position=(30, 80),
                )

    def popup_menu_selected_choice(
        self, popup_window: popup.PopupMenuWindow, choice: str
    ) -> None:
        """Called when a choice is selected in the popup."""
        del popup_window  # unused
        if self._popup_type == 'partyMemberPress':
            if self._popup_party_member_is_host:
                ba.playsound(ba.getsound('error'))
                ba.screenmessage(
                    ba.Lstr(resource='internal.cantKickHostError'),
                    color=(1, 0, 0),
                )
            else:
                assert self._popup_party_member_client_id is not None

                # Ban for 5 minutes.
                result = ba.internal.disconnect_client(
                    self._popup_party_member_client_id, ban_time=5 * 60
                )
                if not result:
                    ba.playsound(ba.getsound('error'))
                    ba.screenmessage(
                        ba.Lstr(resource='getTicketsWindow.unavailableText'),
                        color=(1, 0, 0),
                    )
        elif self._popup_type == 'menu':
            if choice in ('mute', 'unmute'):
                cfg = ba.app.config
                cfg['Chat Muted'] = choice == 'mute'
                cfg.apply_and_commit()
                self._update()
                # Reload chat messages when unmuting.
                if not cfg.get('Chat Muted'):
                    self._reload_chat_messages()
        else:
            print(f'unhandled popup type: {self._popup_type}')

    def popup_menu_closing(self, popup_window: popup.PopupWindow) -> None:
        """Called when the popup is closing."""

    def _on_party_member_press(
        self, client_id: int, is_host: bool, widget: ba.Widget
    ) -> None:
        # if we're the host, pop up 'kick' options for all non-host members
        if ba.internal.get_foreground_host_session() is not None:
            kick_str = ba.Lstr(resource='kickText')
        else:
            # kick-votes appeared in build 14248
            if (
                ba.internal.get_connection_to_host_info().get('build_number', 0)
                < 14248
            ):
                return
            kick_str = ba.Lstr(resource='kickVoteText')
        uiscale = ba.app.ui.uiscale
        popup.PopupMenuWindow(
            position=widget.get_screen_space_center(),
            scale=(
                2.3
                if uiscale is ba.UIScale.SMALL
                else 1.65
                if uiscale is ba.UIScale.MEDIUM
                else 1.23
            ),
            choices=['kick'],
            choices_display=[kick_str],
            current_choice='kick',
            delegate=self,
        )
        self._popup_type = 'partyMemberPress'
        self._popup_party_member_client_id = client_id
        self._popup_party_member_is_host = is_host

    def _send_chat_message(self) -> None:
        """ Sends the message stored in the text field. """
        text = ba.textwidget(query=self._text_field)

        def reject_message(reason: str | ba.Lstr) -> None:
            """ Shows a message on-screen and plays an error sound. """
            ba.screenmessage(
                reason,
                color=(1,0,0)
                )
            ba.playsound(ba.getsound('error'))

        # Placeholder variables in case someone
        # wants to wire them up to settings or something.
        disallow_empty_messages = True
        disallow_large_messages = True

        # Prevent big messages from being sent, or else
        # they'll end up getting butchered by servers anyway.
        if len(text) > self._get_character_limit() and disallow_large_messages:
            reject_message(
                reason = ba.Lstr(translate=('serverResponses', 'Message is too long.'))
            )

        # Prevent empty messages from being sent, it's annoying.
        elif len(text) == 0 and disallow_empty_messages:
            reject_message(
                reason = ba.Lstr(translate=('serverResponses', 'Message can\'t be empty.'))
            )

        # Roll with our message if it is appropiate (and clear out our text field.)
        else:
            ba.internal.chatmessage(cast(str, text))
            ba.textwidget(edit=self._text_field, text='')

    def _text_field_changed(self) -> bool:
        """ Checks if our text field has been changed. """
        old, cur = self._text_field_old, ba.textwidget(query=self._text_field)
        # Compare our old text field with our current one, and overwrite the old one if they're different.
        if cur != old:
            self._text_field_old = cur
            return True
        return False
    
    def _update_text_len_counter(self) -> None:
        """ Updates "self._text_len_counter". """
        update_color = True
        charlimit = self._get_character_limit()

        # Run a quick check, return if nothing has changed.
        if not self._text_field_changed(): return

        text_length = tlen = len(ba.textwidget(query=self._text_field))
        
        txtcolor = (1,1,1,0.4)
        
        if update_color:
            if tlen > charlimit:
                txtcolor = (1,0.1,0.1,0.75)
            elif tlen > 0:
                txtcolor = (1,1,1,0.75)

        ba.textwidget(edit=self._text_len_counter,
                      text=f'{text_length}/{charlimit}',
                      color=txtcolor)

    def _get_character_limit(self) -> int:
        """ Returns how long a message can be. """
        return 70

    def _reload_chat_messages(self, load: bool = True) -> None:
        """ Clears up all messages and loads them back in. """
        if self._chat_texts:
            while self._chat_texts:
                first = self._chat_texts.pop()
                first.delete()

        # Load only when told to (useful when clearing chat via "Mute Chat".)
        if load:
            msgs = ba.internal.get_chat_messages()
            for msg in msgs:
                self._add_msg(msg)

    def _on_creative_menu_press(self) -> None:
        from explodinary.ui.hubcheat import HubCheatWindow
        HubCheatWindow(
            parent=self._root_widget,
            position=self._creative_button.get_screen_space_center(),
            offset=(-410.0, -110),
            bgcolor=self._creative_button_color,
        )

    def close(self) -> None:
        """Close the window."""
        ba.containerwidget(edit=self._root_widget, transition='out_scale')

    def close_with_sound(self) -> None:
        """Close the window and make a lovely sound."""
        ba.playsound(ba.getsound('swish'))
        self.close()
