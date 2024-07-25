from __future__ import annotations

import ba
from bastd.actor.spaz import Spaz

class BossHealthbar:
    def __init__(self,
                 entity: Spaz,
                 name: str,
                 position: tuple,
                 attach: str,
                 deathtrigger: callable | None = None,
                 scale: tuple = (165*1.66, 30*1.66),
                 color: tuple = (1,0.2,0.11),
                 coloralt: tuple = (1.1,0.7,0.92),
                 ):
        """ Creates a node healthbar attached to a spaz entity """
        ## @Temp This code sucks ass!! -Temp
        ## @Temp This code sucks ass!! -Temp
        ## @Temp This code sucks ass!! -Temp
        ## @Temp This code sucks ass!! -Temp
        ## @Temp This code sucks ass!! -Temp
        ## @Temp This code sucks ass!! -Temp
        
        self.entity: Spaz = entity
        self.stuff: dict = {
            'hp': entity.hitpoints,
            'maxhp': entity.hitpoints_max,
        }

        self._internal_update_timer: ba.Timer = ba.Timer(
            0.025,
            self._update_stuff,
            repeat=True,
            timetype=ba.TimeType.BASE
            )

        self._bar_update_timer: ba.Timer = ba.Timer(
            0.01,
            self._update_bar,
            repeat=True
            )
        
        self._bar_bg: ba.Node | None = None
        self._bar: ba.Node | None = None
        self._cover: ba.Node | None = None
        self._bar_txt: ba.Node | None = None

        self.deathtrigger = deathtrigger

        self.stuff: dict = {
            'hp': entity.hitpoints,
            'maxhp': entity.hitpoints_max if entity.hitpoints_max > entity.hitpoints else entity.hitpoints,
        }

        self._x, self._y = [scale[0], scale[1]]
        self._pos = position
        self._attach = attach
        self._color = color
        self._color_alt = coloralt
        self._name = name

        self._update_stuff()
        self._build_bar()

    def _update_stuff(self):
        """ Updates our internal stuff """
        entity = self.entity

        self.stuff['hp'] = entity.hitpoints

        if self.stuff['hp'] < 1:
            self.stuff['hp'] = 0
            self._internal_update_timer = None
            self._bar_update_timer = None
            self._update_bar()
            self._destroy()

    def _update_bar(self):
        """ Updates the bar considering our current values """
        if self._bar:
            maxw = self._x
            defx = self._pos[0]
            
            hp, mhp = self.stuff['hp'], self.stuff['maxhp']
            radius = (hp/mhp)

            newwscale = maxw * radius
            newxpos = defx - ((maxw - newwscale)/2)

            self._bar.position = (newxpos, self._pos[1])
            self._bar.scale = (newwscale, self._y)

    def _build_bar(self):
        """ Builds the bar """
        if self._bar_bg: self._bar_bg.delete()
        self._bar_bg = ba.newnode(
            'image',
            attrs={
                'texture': ba.gettexture('bar'),
                'absolute_scale': True,
                'vr_depth': -7.5,
                'position': self._pos,
                'scale': (self._x,self._y),
                'color': (0.4,0.4,0.4),
                'opacity': 0.7,
                'attach': self._attach,
            },
        )

        if self._bar: self._bar.delete()
        self._bar = ba.newnode(
            'image',
            attrs={
                'texture': ba.gettexture('barAlt'),
                'absolute_scale': True,
                'vr_depth': -5,
                'position': self._pos,
                'scale': (self._x,self._y),
                'color': self._color,
                'opacity': 1,
                'attach': self._attach,
            },
        )

        if self._cover: self._cover.delete()
        self._cover = ba.newnode(
            'image',
            attrs={
                'texture': ba.gettexture('uiAtlas'),
                'model_transparent': ba.getmodel('meterTransparent'),
                'vr_depth': 2,
                'position': self._pos,
                'scale': (self._x*1.15,self._y*1.35),
                'opacity': 1.0,
                'color': self._color_alt,
                'attach': self._attach,
            },
        )

        if self._bar_txt: self._bar_txt.delete()
        istop = self._attach[:3] == 'top'
        vatt = 'top' if self._attach[:3] == 'top' else 'bottom' if self._attach[:6] == 'bottom' else 'center'
        hatt = 'left' if self._attach[-4:] == 'Left' else 'right' if self._attach[-5:] == 'Right' else 'center'
        self._bar_txt = ba.newnode(
            'text',
            attrs={
                'text': self._name,
                'maxwidth': 400,
                'position': (self._pos[0], self._pos[1] + ((-3 - self._y*1.35) if not istop else (3 + self._y*1.35))),
                'vr_depth': 5,
                'h_attach': hatt,
                'h_align': hatt,
                'v_attach': vatt,
                'v_align': vatt,
                'color': (1.0, 1.0, 1.0, 1.0),
                'shadow': 0.44,
                'flatness': 1,
                'scale': 1.2,
                'opacity': 1,
            }
        )

        all = [self._bar_bg, self._bar, self._cover, self._bar_txt, ]
        for a in all:
            ba.animate(a, 'opacity', {
                0:0,
                1.25:1,
            })

    def _destroy(self):
        if self.deathtrigger: self.deathtrigger()
        for a in [
            self._bar_bg,
            self._bar,
            self._cover,
            self._bar_txt,
            ]:
            ba.animate(a, 'opacity', {
                0:1,
                1:1,
                2.25:0,
            })
            ba.timer(2.25, a.delete)