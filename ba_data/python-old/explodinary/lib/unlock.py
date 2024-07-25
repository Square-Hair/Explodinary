import ba
import random

class UnlockPopup:
    def __init__(self,
                 alt: bool = False):
        """ Shows a popup telling us we've unlocked something """
        self._alt = alt
        self._pop_text: str = 'You\'ve unlocked\na new character!' if not alt else 'Something wicked\nthis way comes'

        self._pos = (400,-180)
        self._attach = ['center','center','center']
        self._nobg: bool = False

        self._paw()

    def _paw(self):
        """ Generates our popup message """
        p = self._pos
        sx, sy = [324,110]
        lsx = 65
        br, lr = [2, 8-2]
        self._bg = ba.newnode(
            'image',
            attrs={
                'texture':          ba.gettexture('softRectVertical'),
                'absolute_scale':   True,
                'vr_depth':         -7.5,
                'position':         (p[0], p[1]),
                'scale':            (sx,sy),
                'color':            (0.1,0.2,1.1),
                'opacity':          0.7,
                'attach':           self._attach[0],
                'rotate':           br,
            },
        )
        self._bg1 = ba.newnode(
            'image',
            attrs={
                'texture':          ba.gettexture('softRectVertical'),
                'absolute_scale':   True,
                'vr_depth':         -7.5,
                'position':         (p[0]-8, p[1]+14),
                'scale':            (sx*1.05,sy*1.05),
                'color':            (0.2,1.2,0.4),
                'opacity':          0.1,
                'attach':           self._attach[0],
                'rotate':           br,
            },
        )
        self._bg2 = ba.newnode(
            'image',
            attrs={
                'texture':          ba.gettexture('softRectVertical'),
                'absolute_scale':   True,
                'vr_depth':         -7.5,
                'position':         (p[0]+8, p[1]-14),
                'scale':            (sx*1.05,sy*1.05),
                'color':            (1.1,0.9,0.025),
                'opacity':          0.1,
                'attach':           self._attach[0],
                'rotate':           br,
            },
        )
        self._lock = ba.newnode(
            'image',
            attrs={
                'texture':          ba.gettexture('lock'),
                'absolute_scale':   True,
                'vr_depth':         -7.5,
                'position':         (p[0] + (sx*0.25), p[1] + (sy*(-br/90)) + 2),
                'scale':            (lsx,lsx),
                'color':            (1,1,1),
                'opacity':          1,
                'attach':           self._attach[0],
                'rotate':           lr,
            },
        )
        self._text = ba.newnode(
            'text',
            attrs={
                'text':             self._pop_text,
                'maxwidth':         sx*0.8,
                'position':         (p[0] - (sx*0.15), p[1] + (sy*(-br/90)) + 2),
                'h_attach':         self._attach[1],
                'h_align':          self._attach[1],
                'v_attach':         self._attach[2],
                'v_align':          self._attach[2],
                'color':            (1.4,1.4,1.4),
                'scale':            0.9,
            }
        )
        self.nodes = [self._bg, self._bg1, self._bg2, self._lock, self._text]
        for node in self.nodes:
            ba.animate(node, 'opacity', {
                0:0,
                0.25:node.opacity,
            })

        self._bganim()

        ba.timer(0.3, self._animate_lock)
        ba.timer(4, self._unpaw)

    def _animate_lock(self):
        r = self._lock.rotate
        ba.animate(self._lock, 'rotate', {
            0: r,
            0.9: r-12,
            1.1: r-24,
            1.101: r+11,
            1.2: r+5,
            1.3: r,
        })
        ba.timer(1.1, self._clicklock)

    def _clicklock(self):
        lsx = 65
        ba.animate_array(self._lock, 'color', 3, {
            0: (3,3,3),
            0.45: self._lock.color,
        })
        for i,node in enumerate([self._bg1, self._bg2]):
            ba.animate(node, 'opacity', {
                0:0.22,
                1.25:0.142,
            })
            off = 12
            if i == 1: off = -off
            p = node.position
            ba.animate_array(node, 'position', 2, {
                0:    (p[0] + off,p[1]),
                4: p,
            })
        self._nobg = True
        ba.playsound(ba.getsound('ding'))
        self._lock.texture = ba.gettexture('lockOpen')
        self._lock.scale = (lsx*2, lsx*2)

    def _bganim(self):
        try:
            if self._nobg: return
            self._bg.opacity = random.uniform(0.62, 0.72)
            ba.timer(0.01, self._bganim)
        except: pass

    def _unpaw(self):
        """ Future temp here, I just realized this sounds highly furry and I apologize. """
        for node in self.nodes:
            ba.animate(node, 'opacity', {
                0:node.opacity,
                1:0,
            })
            ba.timer(1, node.delete)
