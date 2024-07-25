# Released under the MIT License. See LICENSE for details.
#
"""Chaos related functionality by Era0S"""

from __future__ import annotations
from typing import TYPE_CHECKING

import math
import random

import ba
from bastd.actor.spazbot import SpazBot
from bastd.gameutils import SharedObjects
from bastd.actor.playerspaz import PlayerSpaz
from explodinary.chaos import ChaosEvent, append_chaos_event

if TYPE_CHECKING:
    from typing import Any, Sequence

def chasattr(obj: object, attr: str):
    try:
        getattr(obj, attr)
        return True
    except (AttributeError, RuntimeError):
        return False


class BlackHole(ba.Actor):
    """A black hole that tries to consume and destroy all objects

    category: Gameplay Classes
    """

    def __init__(
        self,
        position: Sequence[float] = (0.0, 0.0, 0.0),
        source_player: ba.Player | None = None,
        radius: float = 10.0,
        xspeed: float = 1.0,
    ):
        super().__init__()
        self._source_player = source_player
        shared = SharedObjects.get()
        dev_material = ba.Material()
        dev_material.add_actions(conditions=(
            'they_have_material', shared.object_material),
            actions=('modify_part_collision', 'collide', True))
        dev_material.add_actions(actions=(
            ('modify_part_collision', 'physical', False),
            ('call', 'at_connect', self.kill)))
        self.node = ba.newnode(
            'region',
            delegate=self,
            attrs={
                'position': position,
                'scale': (0, 0, 0),
                'type': 'sphere',
                'materials': [dev_material],
            },
        )
        ba.animate_array(
            self.node,
            'scale',
            3,
            {0: (0, 0, 0),
             radius / xspeed: (radius / 10, radius / 10, radius / 10)}
        )
        un_material = ba.Material()
        un_material.add_actions(actions=('modify_part_collision', 'collide',
                                         False))
        self.visual_node0 = ba.newnode(
            'prop',
            owner=self.node,
            attrs={
                'body': 'sphere',
                'model': ba.getmodel('shield'),
                'color_texture': ba.gettexture('black'),
                'shadow_size': 0,
                'reflection_scale': [0],
                'materials': [un_material],
                'gravity_scale': 0,
                'density': 0,
            }
        )
        self.visual_node0.is_area_of_interest = True
        mnode = ba.newnode('math', owner=self.node,
                           attrs={'input1': (0, 0.1, 0), 'operation': 'add'})
        self.node.connectattr('position', mnode, 'input2')
        mnode.connectattr('output', self.visual_node0, 'position')
        ba.animate(self.visual_node0, 'model_scale',
                   {0: 0, radius / xspeed: radius / 10})
        self.visual_node1 = ba.newnode('shield',
                                       owner=self.node,
                                       attrs={'color': (5, 5, 5)})
        self.node.connectattr('position', self.visual_node1, 'position')
        ba.animate(self.visual_node1, 'radius',
                   {0: 0, radius / xspeed: radius / 10 * 2.1})
        self._update_timer = ba.Timer(1 / 60, self._update, True)
        self._dtimer: ba.Timer | None = None
        self._black_hole_sound = ba.getsound('blackHole')
        self.snode = ba.newnode(
            'sound',
            owner=self.node,
            attrs={'sound': self._black_hole_sound}
        )
        ba.animate(self.snode, 'volume', {0: 0, radius / xspeed: radius / 5})

    def _update(self):
        for node in ba.getnodes():
            if (chasattr(node, 'materials') and chasattr(node, 'position')
                and SharedObjects.get().object_material in node.materials
                and (
                    not chasattr(node, 'invincible')
                    or (chasattr(node, 'invincible') and not node.invincible)
                    )):
                drct = (self.node.position[0] - node.position[0],
                        self.node.position[1] - node.position[1],
                        self.node.position[2] - node.position[2])
                dstnc = math.sqrt(drct[0] ** 2 + drct[1] ** 2 + drct[2] ** 2)
                cradius = self.node.scale[0] * 10
                if dstnc <= cradius:
                    nv = (drct[0] / dstnc, drct[1] / dstnc, drct[2] / dstnc)
                    node.handlemessage('impulse',
                                       node.position[0],
                                       node.position[1],
                                       node.position[2],
                                       nv[0], nv[1], nv[2],
                                       cradius * 2, 0, 0, 0,
                                       nv[0], nv[1], nv[2])

    def kill(self):
        node = ba.getcollision().opposingnode
        spaz = (node.getdelegate(PlayerSpaz) or node.getdelegate(SpazBot))
        if spaz and (spaz.last_player_attacked_by in (None, spaz)
                     or ba.time() - spaz.last_attacked_time >= 4):
            spaz.last_attacked_time = ba.time()
            spaz.last_player_attacked_by = ba.existing(self._source_player)
            spaz.last_attacked_type = ('explosion', 'dev')
        ba.emitfx(position=node.position,
                  velocity=node.velocity,
                  count=random.randrange(3,7) if not ba.app.config.get("BSE: Reduced Particles", False) else 2,
                  scale=1,
                  spread=3,
                  chunk_type='spark')
        light = ba.newnode(
            'light',
            attrs={
                'position': node.position,
                'height_attenuated': False,
                'color': (0.5, 0.25, 1),
                'intensity': 20,
            },
        )
        ba.animate(light, 'radius', {0: 0, 0.1: 0.1, 0.2: 0.1, 0.3: 0})
        ba.timer(0.3, light.delete)
        node.handlemessage(ba.DieMessage())
        node.delete()

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):
            if self.node:
                if msg.immediate:
                    self.node.delete()
                else:
                    ba.animate(self.visual_node0, 'model_scale',
                               {0: self.visual_node0.model_scale, 0.1: 0,
                                0.2: 0.25, 0.3: 0.25, 0.4: 0})
                    ba.animate(self.visual_node1, 'radius',
                               {0: self.visual_node1.radius, 0.1: 0, 0.2: 0.5,
                                0.3: 0.5, 0.4: 0})
                    ba.animate(self.snode, 'volume',
                               {0: self.snode.volume, 0.1: 0})
                    ba.timer(0.4, self.last_breath)
                    ba.timer(0.4, self.node.delete)
                self._update_timer = None
        else:
            super().handlemessage(msg)

    def last_breath(self):
        self._dtimer = ba.Timer(1 / 60, ba.Call(
            ba.emitfx, self.node.position, count=100, spread=6,
            emit_type='distortion'
        ), True)
        from bastd.actor.bomb import Blast
        Blast(self.node.position, blast_type='tnt', hit_subtype='tnt')
        ba.timer(1, ba.Call(self.__setattr__, '_dtimer', None))


class EraBlackHoleEvent(ChaosEvent):
    name = 'Black Hole'
    icon = 'chaosBlackHole'

    blacklist = [
        ba.CoopSession
    ]

    def event(self):
        bnds = self.activity.map.get_def_bound_box('area_of_interest_bounds')
        pos = (((bnds[0] + bnds[3]) / 2, (bnds[1] + bnds[4]) / 2,
                (bnds[2] + bnds[5]) / 2)
               if isinstance(self.session, ba.DualTeamSession)
               else (random.uniform(bnds[0], bnds[3]),
                     random.uniform(bnds[1], bnds[4]),
                     random.uniform(bnds[2], bnds[5])))
        bh = BlackHole(pos).autoretain()
        ba.timer(20, ba.WeakCall(bh.handlemessage, ba.DieMessage()))
        # drop the reference, shouldn't need to do this but it wont hurt to do
        bh = None


append_chaos_event(EraBlackHoleEvent)
