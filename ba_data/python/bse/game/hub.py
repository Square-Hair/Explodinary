from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Sequence

import ba
import random
from bastd.gameutils import SharedObjects
from explodinary.custom.particle import bseVFX

class Player(ba.Player['Team']):
    """Our player type for this game."""

class Team(ba.Team[Player]):
    """Our team type for this game."""

class BasketballDiedMessage:
    """Inform something that a basketball has died."""

    def __init__(self, basketball: Basketball):
        self.basketball = basketball

class Basketball(ba.Actor):
    """A lovely basketball."""
    
    def setballstart(self):
        self.node.gravity_scale = 1
        
    def __init__(self, position: Sequence[float] = (0.0, 1.0, 0.0)):
        super().__init__()
        shared = SharedObjects.get()
        activity = self.getactivity()

        # Spawn just above the provided point.
        self._spawn_pos = (position[0], position[1] + 1.0, position[2])
        self.last_players_to_touch: dict[int, Player] = {}
        self.scored = False
        assert activity is not None
        pmats = [shared.object_material, activity.basketball_material]
        self.node = ba.newnode(
            'prop',
            delegate=self,
            attrs={
                'model': activity.basketball_model,
                'color_texture': activity.basketball_tex,
                'body': 'sphere',
                'reflection': 'soft',
                'reflection_scale': [0.25],
                'shadow_size': 0.3,
                'is_area_of_interest': False,
                'position': self._spawn_pos,
                'materials': pmats,
                'density': 1.0,
            },
        )
        ba.animate(self.node, 'model_scale', {0: 0, 0.2: 1.3, 0.26: 1})
        ba.timer(100,self.setballstart,timeformat = ba.TimeFormat.MILLISECONDS,timetype = ba.TimeType.SIM)

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):
            assert self.node
            self.node.delete()
            activity = self._activity()
            if activity and not msg.immediate:
                activity.handlemessage(BasketballDiedMessage(self))

        # If we go out of bounds, move back to where we started.
        elif isinstance(msg, ba.OutOfBoundsMessage):
            assert self.node
            bseVFX('puff', self.node.position, (0,0,0))
            self.node.position = self._spawn_pos
            self.node.velocity = (0,0,0)
            ba.animate(self.node, 'model_scale', {0: 0, 0.2: 1.3, 0.26: 1})

        elif isinstance(msg, ba.HitMessage):
            assert self.node
            assert msg.force_direction is not None
            self.node.handlemessage(
                'impulse',
                msg.pos[0],
                msg.pos[1],
                msg.pos[2],
                msg.velocity[0],
                msg.velocity[1],
                msg.velocity[2],
                1.0 * msg.magnitude,
                1.0 * msg.velocity_magnitude,
                msg.radius,
                0,
                msg.force_direction[0],
                msg.force_direction[1],
                msg.force_direction[2],
            )

            # If this hit came from a player, log them as the last to touch us.
            s_player = msg.get_source_player(Player)
            if s_player is not None:
                activity = self._activity()
                if activity:
                    if s_player in activity.players:
                        self.last_players_to_touch[s_player.team.id] = s_player
        else:
            super().handlemessage(msg)

# ba_meta export game
class HubGame(ba.HubGameActivity[Player, Team]):
    """
    """

    name = 'Hub'
    description = ''
    allow_mid_activity_joins = True
    announce_player_deaths = False
    default_music = ba.MusicType.HUB

    @classmethod
    def get_supported_maps(cls, sessiontype: type[ba.Session]) -> list[str]:
        # For now we're hard-coding spawn positions and whatnot
        # so we need to be sure to specify that we only support
        # a specific map.
        return ['Hub']

    def __init__(self, settings: dict):
        super().__init__(settings)
        shared = SharedObjects.get()
        self.basketball_model = ba.getmodel('basketball')
        self.basketball_tex = ba.gettexture('basketballColor')
        self.basketball_material = ba.Material()
        self.basketball_material.add_actions(
            actions=('modify_part_collision', 'friction', 0.5)
        )
        self.basketball_material.add_actions(
            conditions=('they_have_material', shared.pickup_material),
            actions=('modify_part_collision', 'collide', True),
        )
        self.basketball_material.add_actions(
            conditions=(
                ('we_are_younger_than', 100),
                'and',
                ('they_have_material', shared.object_material),
            ),
            actions=('modify_node_collision', 'collide', False),
        )
        
        self._Basketball_spawn_pos: Sequence[float] | None = None
        self._score_regions: list[ba.NodeActor] | None = None
        self._basketball: Basketball | None = None
        
        ba.getsession().max_players = 12

    def on_begin(self) -> None:
        super().on_begin()
        
        self.propertoppers()
        self.no_map_barrier()
        self.setup_standard_powerup_drops()
        self.play_big_death_sound = False
        self._Basketball_spawn_pos = self.map.get_flag_position(None)
        self._spawn_basketball()

    def _kill_basketball(self) -> None:
        self._basketball = None
        
    def _show_info(self) -> None: return
    #def _show_scoreboard_info(self) -> None: return

    def spawn_player(self, player: Player) -> ba.Actor:
        spawn_points = ba.getactivity().map.get_def_points('ffa_spawn') or [
            (0, 0, 0, 0, 0, 0)
        ]
        point = random.choice(spawn_points)
        return self.spawn_player_spaz(player, position=point)

    def handlemessage(self, msg: Any) -> Any:
        # A player has died.
        if isinstance(msg, ba.PlayerDiedMessage):
            super().handlemessage(msg)  # Augment standard behavior.
            self.respawn_player(msg.getplayer(Player), 1)
            self.play_big_death_sound = False
        # Let the base class handle anything we don't.
        else:
            return super().handlemessage(msg)
        return None

    def propertoppers(self) -> None:
        ba.internal.set_party_icon_always_visible(True)
        ba.getsession()._custom_menu_ui = []
        self.allow_pausing = False

    def no_map_barrier(self) -> None:
        map = ba.getactivity().map
        try: map.player_wall.delete()
        except: return
    
    def _spawn_basketball(self) -> None:
        assert self._Basketball_spawn_pos is not None
        self._basketball = Basketball(position=self._Basketball_spawn_pos)