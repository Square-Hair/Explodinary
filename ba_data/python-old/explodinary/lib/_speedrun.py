from  __future__ import annotations

import random
from typing import TYPE_CHECKING, Sequence, TypeVar

import ba

class SpeedrunMode:
    def __init__(self,
                 activity: ba.Activity
                 ):
        """ Basics for our speedrun mode. """

        self._activity = activity
        """ Activity """

        self._activity._rt_timer_hud: ba.Node | None = None
        self._activity._igt_timer_hud: ba.Node | None = None

        self._rtcount: int = 0
        self._igtcount: int = 0
        self._rt_strtime: str = ['']
        self._igt_strtime: str = ['']
        """ Time measured in centiseconds and display """

        self.draw_timer()

        self._countupdate: ba.Timer = ba.Timer(0.01,
                                           self.cen_tick,
                                           repeat=True,
                                           timetype=ba.TimeType.BASE)
        
        self._clockupdate: ba.Timer = ba.Timer(0.01,
                                            self.tick,
                                            repeat=True,
                                            timetype=ba.TimeType.BASE)
        
        self._clockupdate2: ba.Timer = ba.Timer(0.01,
                                            self.game_tick,
                                            repeat=True)


    def draw_timer(self):
        self._activity._rt_timer_hud = ba.newnode(
            'text',
            attrs={
                'text': '',
                'maxwidth': 300,
                'position': (31, 62),
                'vr_depth': 10,
                'h_attach': 'left',
                'h_align': 'left',
                'v_attach': 'bottom',
                'v_align': 'center',
                'color': (0.7,0.7,0.7),
                'shadow': 1,
                'flatness': 1,
                'scale': 0.96,
                'opacity': 0.77,
            },
        )
        
        self._activity._igt_timer_hud = ba.newnode(
            'text',
            attrs={
                'text': '',
                'maxwidth': 300,
                'position': (20, 30),
                'vr_depth': 10,
                'h_attach': 'left',
                'h_align': 'left',
                'v_attach': 'bottom',
                'v_align': 'center',
                'color': (1.0, 1.0, 1.0),
                'shadow': 1,
                'flatness': 1,
                'scale': 1.25,
                'opacity': 0.95,
            },
        )

    def update_timer(self, time:int, strgoal:list):
        ms = (time % 100)
        ss = (time // 100) % 60
        mm = (time // 6000) % 60
        hh = (time // 360000)
        strgoal[0] = f'{"{:02d}:".format(hh) if hh else ""}{"{:02d}:{:02d}.{:02d}".format(mm,ss,ms)}'

    def cen_tick(self):
        """ Does a thing every 100th of a second. """
        self._rtcount += 1
        if not self._activity.globalsnode.paused: self._igtcount += 1

    def tick(self):
        """ Does a thing every game update. """
        self.update_timer(self._rtcount, self._rt_strtime)
        self._activity._rt_timer_hud.text = f'RT: {self._rt_strtime[0]}'

    def game_tick(self):
        """ Does a thing every game update. """
        self.update_timer(self._igtcount, self._igt_strtime)
        self._activity._igt_timer_hud.text = f'IGT: {self._igt_strtime[0]}'
