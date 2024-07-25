# Released under the MIT License. See LICENSE for details.
#
"""Provides a window to customize team names and colors."""

from __future__ import annotations
from enum import Enum

import ba
from bastd.ui import popup

from explodinary.lib import bseconfig

class ChaosSettingsPopupWindow(popup.PopupWindow):
    """A popup window to customize our chaos settings."""

    def __init__(self, scale_origin: tuple[float, float]):
        w = self._width = 600
        h = self._height = 500
        self._transitioning_out = False
        self._max_name_length = 16

        # Creates our root_widget.
        uiscale = ba.app.ui.uiscale
        
        scale = (
            1.4
            if uiscale is ba.UIScale.SMALL
            else 1.15
            if uiscale is ba.UIScale.MEDIUM
            else 1
        )
        
        pscale = (
            1.5
            if uiscale is ba.UIScale.SMALL
            else 1.5
            if uiscale is ba.UIScale.MEDIUM
            else 1.0
        )
        self.popup_menu_scale = pscale * 1.2
        
        self._r = 'explodinary.bseSettingsWindow.chaosSubMenu.main'
        super().__init__(
            position=scale_origin,
            size=(w, h),
            scale=scale
        )

        cancelbtn = ba.buttonwidget(
            parent=self.root_widget,
            autoselect=True,
            on_activate_call=self._on_cancel_press,
            size=(60, 60),
            scale=1.0,
            text_scale=1.2,
            label=ba.charstr(ba.SpecialChar.BACK),
            button_type='backSmall',
            position=(self._width * 0.075, self._height * 0.8),
        )

        title = ba.textwidget(
            parent=self.root_widget,
            text=ba.Lstr(resource='explodinary.chaosModeText'),
            position=(w/2, h*0.92),
            size=(0, 0),
            scale=1.2,
            maxwidth=400,
            color=ba.app.ui.title_color,
            h_align='center',
            v_align='center',
        )

        # Enable
        chk = ba.checkboxwidget(
            parent=self.root_widget,
            position=(w/2-125, h*0.79),
            size=(120, 30),
            value=bseconfig.chaos_get('Enabled'),
            maxwidth=200,
            on_value_change_call=self._check_enable,
            text=ba.Lstr(translate=('', '${A} ${B}'), subs=[
                ('${A}', ba.Lstr(resource='configGamepadWindow.secondaryEnableText')),
                ('${B}', ba.Lstr(resource='explodinary.chaosModeText'))
            ]),
            autoselect=True,
        )

        yoff = 65
        # Event Time
        x = self._build_setting(
            position=(w/2, h*0.6 + yoff),
            title=ba.Lstr(resource=f'{self._r}.timer'),
            key='Time',
            choices=[3,7,12,21],
            choices_display=[
                ba.Lstr(resource=f'{self._r}.freq_blitz'),
                ba.Lstr(resource=f'{self._r}.freq_unhinged'),
                ba.Lstr(resource=f'{self._r}.freq_chaotic'),
                ba.Lstr(resource=f'{self._r}.freq_exceptional'),
                ]
            )
        
        ba.widget(edit=chk, down_widget=x.get_button())

        yoff -= 55
        # Timer settings
        self._build_setting(
            position=(w/2, h*0.6 + yoff),
            title=ba.Lstr(resource=f'{self._r}.timergroup'),
            press_call=self._timer_settings,
            button_label=ba.Lstr(resource = 'configureText')
            )
        yoff -= 55
        # Event list settings
        x = self._build_setting(
            position=(w/2, h*0.6 + yoff),
            title=ba.Lstr(resource=f'{self._r}.evlengroup'),
            press_call=self._list_settings,
            button_label=ba.Lstr(resource = 'configureText')
            )
        yoff -= 88
        # Announce event
        c = ba.checkboxwidget(
            parent=self.root_widget,
            position=(w/2-125, h*0.6 + yoff),
            size=(120, 30),
            value=bseconfig.chaos_get('DoAnnounce'),
            maxwidth=200,
            on_value_change_call=self._check_announce,
            text=ba.Lstr(resource=f'{self._r}.announce'),
            autoselect=True,
        )
        ba.widget(
            edit=c,
            up_widget=x,
        )
        yoff -= 55
        # Do countdown sounds
        ba.checkboxwidget(
            parent=self.root_widget,
            position=(w/2-125, h*0.6 + yoff),
            size=(120, 30),
            value=bseconfig.chaos_get('DoSound'),
            maxwidth=200,
            on_value_change_call=self._check_sound,
            text=ba.Lstr(resource=f'{self._r}.sounds'),
            autoselect=True,
        )
        yoff -= 55
        # Replace music
        ba.checkboxwidget(
            parent=self.root_widget,
            position=(w/2-125, h*0.6 + yoff),
            size=(120, 30),
            value=bseconfig.chaos_get('DoMusic'),
            maxwidth=200,
            on_value_change_call=self._check_music,
            text=ba.Lstr(resource=f'{self._r}.music'),
            autoselect=True,
        )

    ## Switch some config values
    def _check_enable(self, v:bool) -> None      : bseconfig.chaos_set('Enabled', v)
    def _check_announce(self, v:bool) -> None   : bseconfig.chaos_set('DoAnnounce', v)
    def _check_sound(self, v:bool) -> None      : bseconfig.chaos_set('DoSound', v)
    def _check_music(self, v:bool) -> None      : bseconfig.chaos_set('DoMusic', v)

    def _evlen_change(self, a:int) -> None:
        mmin, mmax = 3, 18
        v = bseconfig.chaos_get('Event_len')
        rv = max(mmin, min(mmax, v+a))
        bseconfig.chaos_set('Event_len', rv)
        ba.app.config.commit()
        ba.textwidget(edit=self._evlentxt, text=str(rv))

    ### Open subsettings
    def _timer_settings(self) -> None: ChaosSubsettingsPopup(scale_origin=((0,0)), subsetting='timer'), 
    def _list_settings(self) -> None: ChaosSubsettingsPopup(scale_origin=((0,0)), subsetting='list'), 

    def _event_picker(self) -> None:
        """ Calls our Chaos Event Toggler popup window. """
        ChaosEventToggler(
            scale_origin=(
                (0,0)
            )
        )

    def _ok(self) -> None:
        self._transition_out()

    def _transition_out(self, transition: str = 'out_scale') -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            ba.containerwidget(edit=self.root_widget, transition=transition)

    def on_popup_cancel(self) -> None:
        ba.playsound(ba.getsound('swish'))
        self._transition_out()

    def _on_cancel_press(self) -> None:
        self._transition_out()

    def _build_setting(
            self,
            position: tuple[float, float],
            title: str | any,
            subtitle: str | None = None,
            key: str = 'Generic Setting',
            choices: list | None = None,
            choices_display: list | None = None,
            on_change_call: any | None = None,
            press_call: any | None = None,
            button_label: str | ba.Lstr = '',
    ) -> popup.PopupMenu:
        
        # Default to True & False settings if not assigned
        if not choices: choices = [True,False]
        if not choices_display:
            choices_display = [
                ba.Lstr(resource='explodinary.bseSettingsWindow' + '.generic.enabled'),
                ba.Lstr(resource='explodinary.bseSettingsWindow' + '.generic.disabled'),
            ]

        # Position stuff
        global_offset = 105
        title_position = (position[0] - global_offset,
                          position[1] - (12.5 if not subtitle else 0))
        sub_position =  (position[0] - global_offset,
                         position[1] - 25)
        btn_position = (position[0] + global_offset - 75,
                        position[1] - 35)

        # Title
        ba.textwidget(
            parent=self.root_widget,
            position=title_position,
            size=(0, 0),
            text=title,
            scale=0.875,
            res_scale=1.5,
            maxwidth=300,
            color=ba.app.ui.infotextcolor,
            h_align='center',
            v_align='center',
        )
        
        # Subtitle if it exists
        if subtitle:
            ba.textwidget(
                parent=self.root_widget,
                position=sub_position,
                size=(0, 0),
                text=subtitle,
                scale=0.6,
                res_scale=1.5,
                maxwidth=250,
                color=(0.7,0.7,0.7),
                h_align='center',
                v_align='center',
            )
            
        # Don't do a popup if we have a press call
        if press_call: return (ba.buttonwidget(
            parent=self.root_widget,
            position=btn_position,
            size=(160.0, 50.0),
            autoselect=True,
            scale=1.0,
            label=button_label,
            on_activate_call=press_call
        ))

        def generic_save(v): bseconfig.chaos_set(key, v)

        # Popup button
        return( popup.PopupMenu(
            parent=self.root_widget,
            position=btn_position,
            width=150,
            scale=self.popup_menu_scale,
            choices=choices,
            choices_display=choices_display,
            current_choice=bseconfig.chaos_get(key),
            on_value_change_call=on_change_call if on_change_call is not None else generic_save
        ) )
   
class ChaosSubsettingsPopup(popup.PopupWindow):
    """A popup window where you can toggle all chaos events."""

    def __init__(self,
                 scale_origin: tuple[float, float],
                 subsetting: str | None = None):
                
        self.sub = subsetting

        # Dimensions
        w = self._width = 533
        h = self._height = 200 if self.sub == 'timer' else 244 if self.sub == 'list' else 0 # >:3
        self._transitioning_out = False

        # Creates our root_widget.
        uiscale = ba.app.ui.uiscale
        
        scale = (
            1.4
            if uiscale is ba.UIScale.SMALL
            else 1.15
            if uiscale is ba.UIScale.MEDIUM
            else 1
        )
        pscale = (
            1.5
            if uiscale is ba.UIScale.SMALL
            else 1.5
            if uiscale is ba.UIScale.MEDIUM
            else 1.0
        )
        
        self.popup_menu_scale = pscale * 1.2
        
        self._r = f'explodinary.bseSettingsWindow.chaosSubMenu.{self.sub}'
        super().__init__(
            position=scale_origin,
            size=(w, h),
            scale=scale
        )

        cancelbtn = ba.buttonwidget(
            parent=self.root_widget,
            autoselect=True,
            on_activate_call=self._on_cancel_press,
            size=(60, 60),
            scale=1.0,
            text_scale=1.2,
            label=ba.charstr(ba.SpecialChar.BACK),
            button_type='backSmall',
            position=(self._width * 0.075, self._height * 0.8 - 30),
        )

        title = ba.textwidget(
            parent=self.root_widget,
            text=ba.Lstr(resource=f'{self._r}.title'),
            position=(w/2, h*0.8),
            size=(0, 0),
            scale=1.2,
            maxwidth=300,
            color=ba.app.ui.title_color,
            h_align='center',
            v_align='center',
        )
        
        alr = f'explodinary.bseSettingsWindow.chaosSubMenu.align'
        if self.sub == 'timer':
            # Enable timer
            ba.checkboxwidget(
                parent=self.root_widget,
                position=(w/2-125, h*0.5),
                size=(120, 30),
                value=bseconfig.chaos_get('Time_show'),
                maxwidth=200,
                on_value_change_call=self._toggle_timer,
                text=ba.Lstr(resource=f'{self._r}.enable'),
                autoselect=True,
            )
            # Alignment
            self._build_setting(
                position=(w/2, h*0.4),
                title=ba.Lstr(resource=f'{self._r}.position'),
                key='Time_pos',
                choices=['bottom', 'top'],
                choices_display=[
                    ba.Lstr(resource=f'{alr}.bottom'),
                    ba.Lstr(resource=f'{alr}.top'),
                ]
            )
        elif self.sub == 'list':
            # Enable event list
            ba.checkboxwidget(
                parent=self.root_widget,
                position=(w/2-125, h*0.576),
                size=(120, 30),
                value=bseconfig.chaos_get('Event_show'),
                maxwidth=200,
                on_value_change_call=self._toggle_event_list,
                text=ba.Lstr(resource=f'{self._r}.enable'),
                autoselect=True,
            )
            # Event length
            ba.textwidget(
                parent=self.root_widget,
                position=(w/2 - 105, h*0.48 - 5),
                size=(0, 0),
                text=ba.Lstr(resource=f'{self._r}.length'),
                scale=0.875,
                res_scale=1.5,
                maxwidth=300,
                color=ba.app.ui.infotextcolor,
                h_align='center',
                v_align='center',
            )
            for label, off, cv in [('-', 30, -1), ('+', 155, 1)]:
                ba.buttonwidget(
                    parent=self.root_widget,
                    position=(w/2 + off, h*0.48 - 20),
                    scale=0.8,
                    repeat=True,
                    text_scale=1.3,
                    size=(40, 40),
                    label=label,
                    autoselect=True,
                    enable_sound=False,
                    on_activate_call=ba.Call(self._event_len_change, cv),
                )
            self._ev_len_txt = ba.textwidget(
                parent=self.root_widget,
                position=(w/2 + 107, h*0.48 - 5),
                size=(0, 0),
                text=str(bseconfig.chaos_get('Event_len')),
                scale=1.11,
                res_scale=1.5,
                maxwidth=50,
                color=ba.app.ui.title_color,
                h_align='center',
                v_align='center',
            )
            # Alignment
            self._build_setting(
                position=(w/2, h*0.3),
                title=ba.Lstr(resource=f'{self._r}.position'),
                key='Event_pos',
                choices=['left', 'right'],
                choices_display=[
                    ba.Lstr(resource=f'{alr}.left'),
                    ba.Lstr(resource=f'{alr}.right'),
                ]
            )
        else: raise Exception(f'Unsupported sub: "{self.sub}"')
        
    def _toggle_timer(self, v: bool) -> None:
        """ Toggles the timer's config value. """
        bseconfig.chaos_set('Time_show', v)
        
    def _toggle_event_list(self, v: bool) -> None:
        """ Toggles the event list's config value. """
        bseconfig.chaos_set('Event_show', v)
        
    def _event_len_change(self, v: int) -> None:
        """ Changes the event list's length. """
        new_len = max( 3, min( 12, bseconfig.chaos_get('Event_len') + v) )
        bseconfig.chaos_set(
            'Event_len',
            max( 3,
                min( 12, bseconfig.chaos_get('Event_len') + v)
                )
            )
        # Update text
        ba.textwidget(
            edit=self._ev_len_txt,
            text=str(new_len)
        )
        ba.playsound(ba.getsound('swish'))
        
    def _ok(self) -> None:
        self._transition_out()

    def _transition_out(self, transition: str = 'out_scale') -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            ba.containerwidget(edit=self.root_widget, transition=transition)

    def on_popup_cancel(self) -> None:
        ba.playsound(ba.getsound('swish'))
        self._transition_out()

    def _on_cancel_press(self) -> None:
        self._transition_out()

    def _build_setting(
            self,
            position: tuple[float, float],
            title: str | any,
            subtitle: str | None = None,
            key: str = 'Generic Setting',
            choices: list | None = None,
            choices_display: list | None = None,
            on_change_call: any | None = None,
            press_call: any | None = None,
            button_label: str | ba.Lstr = '',
    ) -> popup.PopupMenu:
        # Check if the given key exists in our Chaos gallery
        try: bseconfig.chaos_get(key)
        except Exception: raise Exception
        
        # Default to True & False settings if not assigned
        if not choices: choices = [True,False]
        if not choices_display:
            choices_display = [
                ba.Lstr(resource='explodinary.bseSettingsWindow' + '.generic.enabled'),
                ba.Lstr(resource='explodinary.bseSettingsWindow' + '.generic.disabled'),
            ]

        # Position stuff
        global_offset = 105
        title_position = (position[0] - global_offset,
                          position[1] - (12.5 if not subtitle else 0))
        sub_position =  (position[0] - global_offset,
                         position[1] - 25)
        btn_position = (position[0] + global_offset - 75,
                        position[1] - 35)

        # Title
        ba.textwidget(
            parent=self.root_widget,
            position=title_position,
            size=(0, 0),
            text=title,
            scale=0.875,
            res_scale=1.5,
            maxwidth=300,
            color=ba.app.ui.infotextcolor,
            h_align='center',
            v_align='center',
        )
        
        # Subtitle if it exists
        if subtitle:
            ba.textwidget(
                parent=self.root_widget,
                position=sub_position,
                size=(0, 0),
                text=subtitle,
                scale=0.6,
                res_scale=1.5,
                maxwidth=250,
                color=(0.7,0.7,0.7),
                h_align='center',
                v_align='center',
            )
            
        # Don't do a popup if we have a press call
        if press_call: return (ba.buttonwidget(
            parent=self.root_widget,
            position=btn_position,
            size=(160.0, 50.0),
            autoselect=True,
            scale=1.0,
            label=button_label,
            on_activate_call=press_call
        ))

        def generic_save(v): bseconfig.chaos_set(key, v)

        # Popup button
        return( popup.PopupMenu(
            parent=self.root_widget,
            position=btn_position,
            width=150,
            scale=self.popup_menu_scale,
            choices=choices,
            choices_display=choices_display,
            current_choice=bseconfig.chaos_get(key),
            on_value_change_call=on_change_call if on_change_call is not None else generic_save
        ) )
   
class ChaosEventToggler(popup.PopupWindow):
    """A popup window where you can toggle all chaos events."""

    class TabID(Enum):
        """Our available tab types."""

        NORMAL  = 'normal'
        SPECIAL = 'special'
        MANAGER = 'manager'

    def __init__(self, scale_origin: tuple[float, float]):
        w = self._width = 355
        h = self._height = 500
        self._transitioning_out = False
        self._max_name_length = 16

        # Creates our root_widget.
        uiscale = ba.app.ui.uiscale
        
        scale = (
            1.4
            if uiscale is ba.UIScale.SMALL
            else 1.15
            if uiscale is ba.UIScale.MEDIUM
            else 1
        )
        
        self._r = 'explodinary.bseSettingsWindow.chaosEvToggle'
        super().__init__(
            position=scale_origin,
            size=(w, h),
            scale=scale
        )

        tabs_def = [
            (self.TabID.NORMAL, ba.Lstr(resource=self._r + 'normal')),
            (self.TabID.SPECIAL, ba.Lstr(resource=self._r + 'special')),
            (self.TabID.MANAGER, ba.Lstr(resource=self._r + 'manager')),
        ]

        cancelbtn = ba.buttonwidget(
            parent=self.root_widget,
            autoselect=True,
            on_activate_call=self._on_cancel_press,
            size=(60, 60),
            scale=1.0,
            text_scale=1.2,
            label=ba.charstr(ba.SpecialChar.BACK),
            button_type='backSmall',
            position=(self._width * 0.075, self._height * 0.8),
        )

        title = ba.textwidget(
            parent=self.root_widget,
            text=ba.Lstr(resource='explodinary.chaosEventTogglerText'),
            position=(w/1.69, h*0.86),
            size=(0, 0),
            scale=1.4,
            maxwidth=400,
            color=ba.app.ui.title_color,
            h_align='center',
            v_align='center',
        )

        ba.containerwidget(
            edit=self.root_widget,
            selected_child=cancelbtn,
            cancel_button=cancelbtn,
        )
        
    def _ok(self) -> None:
        self._transition_out()

    def _transition_out(self, transition: str = 'out_scale') -> None:
        if not self._transitioning_out:
            self._transitioning_out = True
            ba.containerwidget(edit=self.root_widget, transition=transition)

    def on_popup_cancel(self) -> None:
        ba.playsound(ba.getsound('swish'))
        self._transition_out()

    def _on_cancel_press(self) -> None:
        self._transition_out()
