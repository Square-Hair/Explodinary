# Released under the MIT License. See LICENSE for details.
#
"""Standard maps."""
# pylint: disable=too-many-lines

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import Any


class HockeyStadium(ba.Map):
    """Stadium map used for ice hockey games."""

    from bastd.mapdata import hockey_stadium as defs

    name = 'Hockey Stadium'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'hockey', 'team_flag', 'keep_away', 'rocket_hell']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'hockeyStadiumPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'models': (
                ba.getmodel('hockeyStadiumOuter'),
                ba.getmodel('hockeyStadiumInner'),
                ba.getmodel('hockeyStadiumStands'),
            ),
            'vr_fill_model': ba.getmodel('footballStadiumVRFill'),
            'collide_model': ba.getcollidemodel('hockeyStadiumCollide'),
            'tex': ba.gettexture('hockeyStadium'),
            'stands_tex': ba.gettexture('footballStadium'),
        }
        mat = ba.Material()
        mat.add_actions(actions=('modify_part_collision', 'friction', 0.01))
        data['ice_material'] = mat
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'model': self.preloaddata['models'][0],
                'collide_model': self.preloaddata['collide_model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [
                    shared.footing_material,
                    self.preloaddata['ice_material'],
                ],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_model'],
                'vr_only': True,
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['stands_tex'],
            },
        )
        mats = [shared.footing_material, self.preloaddata['ice_material']]
        self.floor = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['models'][1],
                'color_texture': self.preloaddata['tex'],
                'opacity': 0.92,
                'opacity_in_low_or_medium_quality': 1.0,
                'materials': mats,
            },
        )
        self.stands = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['models'][2],
                'visible_in_reflections': False,
                'color_texture': self.preloaddata['stands_tex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.floor_reflection = True
        gnode.debris_friction = 0.3
        gnode.debris_kill_height = -0.3
        gnode.tint = (1.2, 1.3, 1.33)
        gnode.ambient_color = (1.15, 1.25, 1.6)
        gnode.vignette_outer = (0.66, 0.67, 0.73)
        gnode.vignette_inner = (0.93, 0.93, 0.95)
        gnode.vr_camera_offset = (0, -0.8, -1.1)
        gnode.vr_near_clip = 0.5
        self.is_hockey = True


class FootballStadium(ba.Map):
    """Stadium map for football games."""

    from bastd.mapdata import football_stadium as defs

    name = 'Football Stadium'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'football', 'team_flag', 'keep_away', 'rocket_hell']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'footballStadiumPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('footballStadium'),
            'vr_fill_model': ba.getmodel('footballStadiumVRFill'),
            'collide_model': ba.getcollidemodel('footballStadiumCollide'),
            'tex': ba.gettexture('footballStadium'),
        }
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'model': self.preloaddata['model'],
                'collide_model': self.preloaddata['collide_model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_model'],
                'lighting': False,
                'vr_only': True,
                'background': True,
                'color_texture': self.preloaddata['tex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.3, 1.2, 1.0)
        gnode.ambient_color = (1.3, 1.2, 1.0)
        gnode.vignette_outer = (0.57, 0.57, 0.57)
        gnode.vignette_inner = (0.9, 0.9, 0.9)
        gnode.vr_camera_offset = (0, -0.8, -1.1)
        gnode.vr_near_clip = 0.5

    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5


class Bridgit(ba.Map):
    """Map with a narrow bridge in the middle."""

    from bastd.mapdata import bridgit as defs

    name = 'Bridgit'
    dataname = 'bridgit'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        # print('getting playtypes', cls._getdata()['play_types'])
        return ['melee', 'team_flag', 'keep_away']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'bridgitPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model_top': ba.getmodel('bridgitLevelTop'),
            'model_bottom': ba.getmodel('bridgitLevelBottom'),
            'model_bg': ba.getmodel('natureBackground'),
            'bg_vr_fill_model': ba.getmodel('natureBackgroundVRFill'),
            'collide_model': ba.getcollidemodel('bridgitLevelCollide'),
            'tex': ba.gettexture('bridgitLevelColor'),
            'model_bg_tex': ba.gettexture('natureBackgroundColor'),
            'collide_bg': ba.getcollidemodel('natureBackgroundCollide'),
            'railing_collide_model': (
                ba.getcollidemodel('bridgitLevelRailingCollide')
            ),
            'bg_material': ba.Material(),
        }
        data['bg_material'].add_actions(
            actions=('modify_part_collision', 'friction', 10.0)
        )
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model_top'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.bottom = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bottom'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bg'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bg_vr_fill_model'],
                'lighting': False,
                'vr_only': True,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex'],
            },
        )
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        self.bg_collide = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['collide_bg'],
                'materials': [
                    shared.footing_material,
                    self.preloaddata['bg_material'],
                    shared.death_material,
                ],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.1, 1.2, 1.3)
        gnode.ambient_color = (1.1, 1.2, 1.3)
        gnode.vignette_outer = (0.65, 0.6, 0.55)
        gnode.vignette_inner = (0.9, 0.9, 0.93)


class BigG(ba.Map):
    """Large G shaped map for racing"""

    from bastd.mapdata import big_g as defs

    name = 'Big G'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return [
            'race',
            'melee',
            'keep_away',
            'team_flag',
            'king_of_the_hill',
            'conquest',
        ]

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'bigGPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model_top': ba.getmodel('bigG'),
            'model_bottom': ba.getmodel('bigGBottom'),
            'model_bg': ba.getmodel('natureBackground'),
            'bg_vr_fill_model': ba.getmodel('natureBackgroundVRFill'),
            'collide_model': ba.getcollidemodel('bigGCollide'),
            'tex': ba.gettexture('bigG'),
            'model_bg_tex': ba.gettexture('natureBackgroundColor'),
            'collide_bg': ba.getcollidemodel('natureBackgroundCollide'),
            'bumper_collide_model': ba.getcollidemodel('bigGBumper'),
            'bg_material': ba.Material(),
        }
        data['bg_material'].add_actions(
            actions=('modify_part_collision', 'friction', 10.0)
        )
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'color': (0.7, 0.7, 0.7),
                'model': self.preloaddata['model_top'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.bottom = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bottom'],
                'color': (0.7, 0.7, 0.7),
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bg'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bg_vr_fill_model'],
                'lighting': False,
                'vr_only': True,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex'],
            },
        )
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['bumper_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        self.bg_collide = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['collide_bg'],
                'materials': [
                    shared.footing_material,
                    self.preloaddata['bg_material'],
                    shared.death_material,
                ],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.1, 1.2, 1.3)
        gnode.ambient_color = (1.1, 1.2, 1.3)
        gnode.vignette_outer = (0.65, 0.6, 0.55)
        gnode.vignette_inner = (0.9, 0.9, 0.93)


class ExplodinaryRoundabout(ba.Map):
    """Modified Roundabout map."""

    from bastd.mapdata import expl_roundabout as defs

    name = 'Roundabout*'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'roundaboutPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('expl_roundaboutLevel'),
            'model_bottom': ba.getmodel('expl_roundaboutLevelBottom'),
            'model_bg': ba.getmodel('natureBackground'),
            'bg_vr_fill_model': ba.getmodel('natureBackgroundVRFill'),
            'collide_model': ba.getcollidemodel('expl_roundaboutLevelCollide'),
            'tex': ba.gettexture('roundaboutLevelColor'),
            'model_bg_tex': ba.gettexture('natureBackgroundColor'),
            'collide_bg': ba.getcollidemodel('natureBackgroundCollide'),
            'railing_collide_model': (
                ba.getcollidemodel('expl_roundaboutLevelBumper')
            ),
            'bg_material': ba.Material(),
        }
        data['bg_material'].add_actions(
            actions=('modify_part_collision', 'friction', 10.0)
        )
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, -1, 1))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.bottom = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bottom'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bg'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bg_vr_fill_model'],
                'lighting': False,
                'vr_only': True,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex'],
            },
        )
        self.bg_collide = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['collide_bg'],
                'materials': [
                    shared.footing_material,
                    self.preloaddata['bg_material'],
                    shared.death_material,
                ],
            },
        )
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.0, 1.05, 1.1)
        gnode.ambient_color = (1.0, 1.05, 1.1)
        gnode.shadow_ortho = True
        gnode.vignette_outer = (0.63, 0.65, 0.7)
        gnode.vignette_inner = (0.97, 0.95, 0.93)

class Roundabout(ba.Map):
    """Vanilla Roundabout for seamless online play."""

    from bastd.mapdata import roundabout as defs

    name = 'Roundabout'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'roundaboutPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('roundaboutLevel'),
            'model_bottom': ba.getmodel('roundaboutLevelBottom'),
            'model_bg': ba.getmodel('natureBackground'),
            'bg_vr_fill_model': ba.getmodel('natureBackgroundVRFill'),
            'collide_model': ba.getcollidemodel('roundaboutLevelCollide'),
            'tex': ba.gettexture('roundaboutLevelColor'),
            'model_bg_tex': ba.gettexture('natureBackgroundColor'),
            'collide_bg': ba.getcollidemodel('natureBackgroundCollide'),
            'railing_collide_model': (
                ba.getcollidemodel('roundaboutLevelBumper')
            ),
            'bg_material': ba.Material(),
        }
        data['bg_material'].add_actions(
            actions=('modify_part_collision', 'friction', 10.0)
        )
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, -1, 1))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.bottom = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bottom'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bg'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bg_vr_fill_model'],
                'lighting': False,
                'vr_only': True,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex'],
            },
        )
        self.bg_collide = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['collide_bg'],
                'materials': [
                    shared.footing_material,
                    self.preloaddata['bg_material'],
                    shared.death_material,
                ],
            },
        )
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.0, 1.05, 1.1)
        gnode.ambient_color = (1.0, 1.05, 1.1)
        gnode.shadow_ortho = True
        gnode.vignette_outer = (0.63, 0.65, 0.7)
        gnode.vignette_inner = (0.97, 0.95, 0.93)
        
class MonkeyFace(ba.Map):
    """Map sorta shaped like a monkey face; teehee!"""

    from bastd.mapdata import monkey_face as defs

    name = 'Monkey Face'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'monkeyFacePreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('monkeyFaceLevel'),
            'bottom_model': ba.getmodel('monkeyFaceLevelBottom'),
            'model_bg': ba.getmodel('natureBackground'),
            'bg_vr_fill_model': ba.getmodel('natureBackgroundVRFill'),
            'collide_model': ba.getcollidemodel('monkeyFaceLevelCollide'),
            'tex': ba.gettexture('monkeyFaceLevelColor'),
            'model_bg_tex': ba.gettexture('natureBackgroundColor'),
            'collide_bg': ba.getcollidemodel('natureBackgroundCollide'),
            'railing_collide_model': (
                ba.getcollidemodel('monkeyFaceLevelBumper')
            ),
            'bg_material': ba.Material(),
        }
        data['bg_material'].add_actions(
            actions=('modify_part_collision', 'friction', 10.0)
        )
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.bottom = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bottom_model'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bg'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bg_vr_fill_model'],
                'lighting': False,
                'vr_only': True,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex'],
            },
        )
        self.bg_collide = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['collide_bg'],
                'materials': [
                    shared.footing_material,
                    self.preloaddata['bg_material'],
                    shared.death_material,
                ],
            },
        )
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.1, 1.2, 1.2)
        gnode.ambient_color = (1.2, 1.3, 1.3)
        gnode.vignette_outer = (0.60, 0.62, 0.66)
        gnode.vignette_inner = (0.97, 0.95, 0.93)
        gnode.vr_camera_offset = (-1.4, 0, 0)

class BaboonFace(ba.Map):
    """Map sorta shaped like a baboon face; yahoo!"""

    from bastd.mapdata import baboon_face as defs

    name = 'Baboon Face'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag', 'king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'baboonFacePreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('baboonFaceLevel'),
            'model_bg': ba.getmodel('natureBackground'),
            'bg_vr_fill_model': ba.getmodel('natureBackgroundVRFill'),
            'collide_model': ba.getcollidemodel('baboonFaceLevelCollide'),
            'tex': ba.gettexture('baboonFaceLevelColor'),
            'model_bg_tex': ba.gettexture('natureBackgroundColor'),
            'collide_bg': ba.getcollidemodel('natureBackgroundCollide'),
            'railing_collide_model': ba.getcollidemodel('baboonFaceBumper'),
            'bg_material': ba.Material(),
        }
        data['bg_material'].add_actions(
            actions=('modify_part_collision', 'friction', 10.0)
        )
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bg'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bg_vr_fill_model'],
                'lighting': False,
                'vr_only': True,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex'],
            },
        )
        self.bg_collide = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['collide_bg'],
                'materials': [
                    shared.footing_material,
                    self.preloaddata['bg_material'],
                    shared.death_material,
                ],
            },
        )
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.1, 1.2, 1.2)
        gnode.ambient_color = (1.2, 1.3, 1.3)
        gnode.vignette_outer = (0.60, 0.62, 0.66)
        gnode.vignette_inner = (0.97, 0.95, 0.93)
        gnode.vr_camera_offset = (-1.4, 0, 0)
        
class ZigZag(ba.Map):
    """A very long zig-zaggy map"""

    from bastd.mapdata import zig_zag as defs

    name = 'Zigzag'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return [
            'melee',
            'keep_away',
            'team_flag',
            'conquest',
            'king_of_the_hill',
        ]

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'zigzagPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('zigZagLevel'),
            'model_bottom': ba.getmodel('zigZagLevelBottom'),
            'model_bg': ba.getmodel('natureBackground'),
            'bg_vr_fill_model': ba.getmodel('natureBackgroundVRFill'),
            'collide_model': ba.getcollidemodel('zigZagLevelCollide'),
            'tex': ba.gettexture('zigZagLevelColor'),
            'model_bg_tex': ba.gettexture('natureBackgroundColor'),
            'collide_bg': ba.getcollidemodel('natureBackgroundCollide'),
            'railing_collide_model': ba.getcollidemodel('zigZagLevelBumper'),
            'bg_material': ba.Material(),
        }
        data['bg_material'].add_actions(
            actions=('modify_part_collision', 'friction', 10.0)
        )
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bg'],
                'lighting': False,
                'color_texture': self.preloaddata['model_bg_tex'],
            },
        )
        self.bottom = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bottom'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bg_vr_fill_model'],
                'lighting': False,
                'vr_only': True,
                'background': True,
                'color_texture': self.preloaddata['model_bg_tex'],
            },
        )
        self.bg_collide = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['collide_bg'],
                'materials': [
                    shared.footing_material,
                    self.preloaddata['bg_material'],
                    shared.death_material,
                ],
            },
        )
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.0, 1.15, 1.15)
        gnode.ambient_color = (1.0, 1.15, 1.15)
        gnode.vignette_outer = (0.57, 0.59, 0.63)
        gnode.vignette_inner = (0.97, 0.95, 0.93)
        gnode.vr_camera_offset = (-1.5, 0, 0)


class ExplodinaryThePad(ba.Map):
    """The Pad modified for Explodinary."""

    from bastd.mapdata import expl_the_pad as defs

    name = 'The Pad*'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag', 'king_of_the_hill', 'rocket_hell']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'thePadPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('explThePadLevel'),
            'bottom_model': ba.getmodel('thePadLevelBottom'),
            'collide_model': ba.getcollidemodel('explThePadLevelCollide'),
            'tex': ba.gettexture('thePadLevelColor'),
            'bgtex': ba.gettexture('menuBG'),
            'bgmodel': ba.getmodel('thePadBG'),
            'railing_collide_model': ba.getcollidemodel('thePadLevelBumper'),
            'vr_fill_mound_model': ba.getmodel('thePadVRFillMound'),
            'vr_fill_mound_tex': ba.gettexture('vrFillMound'),
        }
        # fixme should chop this into vr/non-vr sections for efficiency
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.bottom = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bottom_model'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.56, 0.55, 0.47),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.1, 1.1, 1.0)
        gnode.ambient_color = (1.1, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.65, 0.75)
        gnode.vignette_inner = (0.95, 0.95, 0.93)

class ThePad(ba.Map):
    """Vanilla The Pad Level for seamless online play."""

    from bastd.mapdata import the_pad as defs

    name = 'The Pad'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'thePadPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('thePadLevel'),
            'bottom_model': ba.getmodel('thePadLevelBottom'),
            'collide_model': ba.getcollidemodel('thePadLevelCollide'),
            'tex': ba.gettexture('thePadLevelColor'),
            'bgtex': ba.gettexture('menuBG'),
            'bgmodel': ba.getmodel('thePadBG'),
            'railing_collide_model': ba.getcollidemodel('thePadLevelBumper'),
            'vr_fill_mound_model': ba.getmodel('thePadVRFillMound'),
            'vr_fill_mound_tex': ba.gettexture('vrFillMound'),
        }
        # fixme should chop this into vr/non-vr sections for efficiency
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.bottom = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bottom_model'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.56, 0.55, 0.47),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.1, 1.1, 1.0)
        gnode.ambient_color = (1.1, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.65, 0.75)
        gnode.vignette_inner = (0.95, 0.95, 0.93)
        
class DoomShroom(ba.Map):
    """A giant mushroom. Of doom!"""

    from bastd.mapdata import doom_shroom as defs

    name = 'Doom Shroom'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'doomShroomPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('doomShroomLevel'),
            'collide_model': ba.getcollidemodel('doomShroomLevelCollide'),
            'tex': ba.gettexture('doomShroomLevelColor'),
            'bgtex': ba.gettexture('doomShroomBGColor'),
            'bgmodel': ba.getmodel('doomShroomBG'),
            'vr_fill_model': ba.getmodel('doomShroomVRFill'),
            'stem_model': ba.getmodel('doomShroomStem'),
            'collide_bg': ba.getcollidemodel('doomShroomStemCollide'),
        }
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_model'],
                'lighting': False,
                'vr_only': True,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.stem = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['stem_model'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        self.bg_collide = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['collide_bg'],
                'materials': [shared.footing_material, shared.death_material],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.82, 1.25, 1)
        gnode.ambient_color = (0.9, 1.3, 1.1)
        gnode.shadow_ortho = False
        gnode.vignette_outer = (0.76, 0.76, 0.76)
        gnode.vignette_inner = (0.95, 0.95, 0.99)

    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        xpos = point.x
        zpos = point.z
        x_adj = xpos * 0.125
        z_adj = (zpos + 3.7) * 0.2
        if running:
            x_adj *= 1.4
            z_adj *= 1.4
        return x_adj * x_adj + z_adj * z_adj > 1.0

class SmoothShroom(ba.Map):
    """A giant mushroom. Of doom! And SMOOTH1!!!!!!!!"""

    from bastd.mapdata import doom_shroom as defs

    name = 'Doom Shroom*'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag', 'rocket_hell']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'doomShroomPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('doomShroomLevel'),
            'collide_model': ba.getcollidemodel('smoothShroomLevelCollide'),
            'tex': ba.gettexture('doomShroomLevelColor'),
            'bgtex': ba.gettexture('doomShroomBGColor'),
            'bgmodel': ba.getmodel('doomShroomBG'),
            'vr_fill_model': ba.getmodel('doomShroomVRFill'),
            'stem_model': ba.getmodel('doomShroomStem'),
            'collide_bg': ba.getcollidemodel('doomShroomStemCollide'),
        }
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_model'],
                'lighting': False,
                'vr_only': True,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.stem = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['stem_model'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        self.bg_collide = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['collide_bg'],
                'materials': [shared.footing_material, shared.death_material],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.82, 1.25, 1)
        gnode.ambient_color = (0.9, 1.3, 1.1)
        gnode.shadow_ortho = False
        gnode.vignette_outer = (0.76, 0.76, 0.76)
        gnode.vignette_inner = (0.95, 0.95, 0.99)

    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        xpos = point.x
        zpos = point.z
        x_adj = xpos * 0.125
        z_adj = (zpos + 3.7) * 0.2
        if running:
            x_adj *= 1.4
            z_adj *= 1.4
        return x_adj * x_adj + z_adj * z_adj > 1.0

class LakeFrigid(ba.Map):
    """An icy lake fit for racing."""

    from bastd.mapdata import lake_frigid as defs

    name = 'Lake Frigid'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag', 'race']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'lakeFrigidPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('lakeFrigid'),
            'model_top': ba.getmodel('lakeFrigidTop'),
            'model_reflections': ba.getmodel('lakeFrigidReflections'),
            'collide_model': ba.getcollidemodel('lakeFrigidCollide'),
            'tex': ba.gettexture('lakeFrigid'),
            'tex_reflections': ba.gettexture('lakeFrigidReflections'),
            'vr_fill_model': ba.getmodel('lakeFrigidVRFill'),
        }
        mat = ba.Material()
        mat.add_actions(actions=('modify_part_collision', 'friction', 0.01))
        data['ice_material'] = mat
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [
                    shared.footing_material,
                    self.preloaddata['ice_material'],
                ],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_top'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_reflections'],
                'lighting': False,
                'overlay': True,
                'opacity': 0.15,
                'color_texture': self.preloaddata['tex_reflections'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_model'],
                'lighting': False,
                'vr_only': True,
                'background': True,
                'color_texture': self.preloaddata['tex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1, 1, 1)
        gnode.ambient_color = (1, 1, 1)
        gnode.shadow_ortho = True
        gnode.vignette_outer = (0.86, 0.86, 0.86)
        gnode.vignette_inner = (0.95, 0.95, 0.99)
        gnode.vr_near_clip = 0.5
        self.is_hockey = True


class TipTop(ba.Map):
    """A pointy map good for king-of-the-hill-ish games."""

    from bastd.mapdata import tip_top as defs

    name = 'Tip Top'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag', 'king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'tipTopPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('tipTopLevel'),
            'bottom_model': ba.getmodel('tipTopLevelBottom'),
            'collide_model': ba.getcollidemodel('tipTopLevelCollide'),
            'tex': ba.gettexture('tipTopLevelColor'),
            'bgtex': ba.gettexture('tipTopBGColor'),
            'bgmodel': ba.getmodel('tipTopBG'),
            'railing_collide_model': ba.getcollidemodel('tipTopLevelBumper'),
        }
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, -0.2, 2.5))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'color': (0.7, 0.7, 0.7),
                'materials': [shared.footing_material],
            },
        )
        self.bottom = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bottom_model'],
                'lighting': False,
                'color': (0.7, 0.7, 0.7),
                'color_texture': self.preloaddata['tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'color': (0.4, 0.4, 0.4),
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.8, 0.9, 1.3)
        gnode.ambient_color = (0.8, 0.9, 1.3)
        gnode.vignette_outer = (0.79, 0.79, 0.69)
        gnode.vignette_inner = (0.97, 0.97, 0.99)


class CragCastle(ba.Map):
    """A lovely castle map."""

    from bastd.mapdata import crag_castle as defs

    name = 'Crag Castle'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag', 'conquest']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'cragCastlePreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('cragCastleLevel'),
            'bottom_model': ba.getmodel('cragCastleLevelBottom'),
            'collide_model': ba.getcollidemodel('cragCastleLevelCollide'),
            'tex': ba.gettexture('cragCastleLevelColor'),
            'bgtex': ba.gettexture('menuBG'),
            'bgmodel': ba.getmodel('thePadBG'),
            'railing_collide_model': (
                ba.getcollidemodel('cragCastleLevelBumper')
            ),
            'vr_fill_mound_model': ba.getmodel('cragCastleVRFillMound'),
            'vr_fill_mound_tex': ba.gettexture('vrFillMound'),
        }
        # fixme should chop this into vr/non-vr sections
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.bottom = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bottom_model'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.2, 0.25, 0.2),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.shadow_ortho = True
        gnode.shadow_offset = (0, 0, -5.0)
        gnode.tint = (1.15, 1.05, 0.75)
        gnode.ambient_color = (1.15, 1.05, 0.75)
        gnode.vignette_outer = (0.6, 0.65, 0.6)
        gnode.vignette_inner = (0.95, 0.95, 0.95)
        gnode.vr_near_clip = 1.0


class TowerD(ba.Map):
    """Map used for runaround mini-game."""

    from bastd.mapdata import tower_d as defs

    name = 'Tower D'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'towerDPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('towerDLevel'),
            'model_bottom': ba.getmodel('towerDLevelBottom'),
            'collide_model': ba.getcollidemodel('towerDLevelCollide'),
            'tex': ba.gettexture('towerDLevelColor'),
            'bgtex': ba.gettexture('menuBG'),
            'bgmodel': ba.getmodel('thePadBG'),
            'player_wall_collide_model': ba.getcollidemodel('towerDPlayerWall'),
            'player_wall_material': ba.Material(),
        }
        # fixme should chop this into vr/non-vr sections
        data['player_wall_material'].add_actions(
            actions=('modify_part_collision', 'friction', 0.0)
        )
        # anything that needs to hit the wall can apply this material
        data['collide_with_wall_material'] = ba.Material()
        data['player_wall_material'].add_actions(
            conditions=(
                'they_dont_have_material',
                data['collide_with_wall_material'],
            ),
            actions=('modify_part_collision', 'collide', False),
        )
        data['vr_fill_mound_model'] = ba.getmodel('stepRightUpVRFillMound')
        data['vr_fill_mound_tex'] = ba.gettexture('vrFillMound')
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 1, 1))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.node_bottom = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'model': self.preloaddata['model_bottom'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.53, 0.57, 0.5),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.player_wall = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['player_wall_collide_model'],
                'affect_bg_dynamics': False,
                'materials': [self.preloaddata['player_wall_material']],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.15, 1.11, 1.03)
        gnode.ambient_color = (1.2, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.73, 0.7)
        gnode.vignette_inner = (0.95, 0.95, 0.95)

    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        # see if we're within edge_box
        boxes = self.defs.boxes
        box_position = boxes['edge_box'][0:3]
        box_scale = boxes['edge_box'][6:9]
        box_position2 = boxes['edge_box2'][0:3]
        box_scale2 = boxes['edge_box2'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        xpos2 = (point.x - box_position2[0]) / box_scale2[0]
        zpos2 = (point.z - box_position2[2]) / box_scale2[2]
        # if we're outside of *both* boxes we're near the edge
        return (xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5) and (
            xpos2 < -0.5 or xpos2 > 0.5 or zpos2 < -0.5 or zpos2 > 0.5
        )

class HappyThoughts(ba.Map):
    """Flying map."""

    from bastd.mapdata import happy_thoughts as defs

    name = 'Happy Thoughts'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return [
            'melee',
            'keep_away',
            'team_flag',
            'conquest',
            'king_of_the_hill',
        ]

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'alwaysLandPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('alwaysLandLevel'),
            'bottom_model': ba.getmodel('alwaysLandLevelBottom'),
            'bgmodel': ba.getmodel('alwaysLandBG'),
            'collide_model': ba.getcollidemodel('alwaysLandLevelCollide'),
            'tex': ba.gettexture('alwaysLandLevelColor'),
            'bgtex': ba.gettexture('alwaysLandBGColor'),
            'vr_fill_mound_model': ba.getmodel('alwaysLandVRFillMound'),
            'vr_fill_mound_tex': ba.gettexture('vrFillMound'),
        }
        return data

    @classmethod
    def get_music_type(cls) -> ba.MusicType:
        return ba.MusicType.FLYING

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, -3.7, 2.5))
        shared = SharedObjects.get()
        ba.getactivity()._excluded_powerups = ['fly_punch', 'dash']
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.bottom = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bottom_model'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.2, 0.25, 0.2),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.happy_thoughts_mode = True
        gnode.shadow_offset = (0.0, 8.0, 5.0)
        gnode.tint = (1.3, 1.23, 1.0)
        gnode.ambient_color = (1.3, 1.23, 1.0)
        gnode.vignette_outer = (0.64, 0.59, 0.69)
        gnode.vignette_inner = (0.95, 0.95, 0.93)
        gnode.vr_near_clip = 1.0
        self.is_flying = True

        # throw out some tips on flying
        txt = ba.newnode(
            'text',
            attrs={
                'text': ba.Lstr(resource='pressJumpToFlyText'),
                'scale': 1.2,
                'maxwidth': 800,
                'position': (0, 200),
                'shadow': 0.5,
                'flatness': 0.5,
                'h_align': 'center',
                'v_attach': 'bottom',
            },
        )
        cmb = ba.newnode(
            'combine',
            owner=txt,
            attrs={'size': 4, 'input0': 0.3, 'input1': 0.9, 'input2': 0.0},
        )
        ba.animate(cmb, 'input3', {3.0: 0, 4.0: 1, 9.0: 1, 10.0: 0})
        cmb.connectattr('output', txt, 'color')
        ba.timer(10.0, txt.delete)


class ExplodinaryStepRightUp(ba.Map):
    """Step Right Up modified for Explodinary."""

    from bastd.mapdata import expl_step_right_up as defs

    name = 'Step Right Up*'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag', 'conquest']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'stepRightUpPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('explStepRightUpLevel'),
            'model_bottom': ba.getmodel('stepRightUpLevelBottom'),
            'collide_model': ba.getcollidemodel('explStepRightUpLevelCollide'),
            'tex': ba.gettexture('stepRightUpLevelColor'),
            'bgtex': ba.gettexture('menuBG'),
            'bgmodel': ba.getmodel('thePadBG'),
            'vr_fill_mound_model': ba.getmodel('stepRightUpVRFillMound'),
            'vr_fill_mound_tex': ba.gettexture('vrFillMound'),
        }
        # fixme should chop this into vr/non-vr chunks
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, -1, 2))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.node_bottom = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'model': self.preloaddata['model_bottom'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.53, 0.57, 0.5),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.2, 1.1, 1.0)
        gnode.ambient_color = (1.2, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.65, 0.75)
        gnode.vignette_inner = (0.95, 0.95, 0.93)

class StepRightUp(ba.Map):
    """Vanilla Step Right Up for seamless online play."""

    from bastd.mapdata import step_right_up as defs

    name = 'Step Right Up'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'stepRightUpPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('stepRightUpLevel'),
            'model_bottom': ba.getmodel('stepRightUpLevelBottom'),
            'collide_model': ba.getcollidemodel('stepRightUpLevelCollide'),
            'tex': ba.gettexture('stepRightUpLevelColor'),
            'bgtex': ba.gettexture('menuBG'),
            'bgmodel': ba.getmodel('thePadBG'),
            'vr_fill_mound_model': ba.getmodel('stepRightUpVRFillMound'),
            'vr_fill_mound_tex': ba.gettexture('vrFillMound'),
        }
        # fixme should chop this into vr/non-vr chunks
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, -1, 2))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.node_bottom = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'model': self.preloaddata['model_bottom'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.53, 0.57, 0.5),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.2, 1.1, 1.0)
        gnode.ambient_color = (1.2, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.65, 0.75)
        gnode.vignette_inner = (0.95, 0.95, 0.93)
        
class Courtyard(ba.Map):
    """A courtyard-ish looking map for co-op levels."""

    from bastd.mapdata import courtyard as defs

    name = 'Courtyard'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag', 'rocket_hell']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'courtyardPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('courtyardLevel'),
            'model_bottom': ba.getmodel('courtyardLevelBottom'),
            'collide_model': ba.getcollidemodel('courtyardLevelCollide'),
            'tex': ba.gettexture('courtyardLevelColor'),
            'bgtex': ba.gettexture('menuBG'),
            'bgmodel': ba.getmodel('thePadBG'),
            'player_wall_collide_model': (
                ba.getcollidemodel('courtyardPlayerWall')
            ),
            'player_wall_material': ba.Material(),
        }
        # FIXME: Chop this into vr and non-vr chunks.
        data['player_wall_material'].add_actions(
            actions=('modify_part_collision', 'friction', 0.0)
        )
        # anything that needs to hit the wall should apply this.
        data['collide_with_wall_material'] = ba.Material()
        data['player_wall_material'].add_actions(
            conditions=(
                'they_dont_have_material',
                data['collide_with_wall_material'],
            ),
            actions=('modify_part_collision', 'collide', False),
        )
        data['vr_fill_mound_model'] = ba.getmodel('stepRightUpVRFillMound')
        data['vr_fill_mound_tex'] = ba.gettexture('vrFillMound')
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.bottom = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_bottom'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.53, 0.57, 0.5),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        # in co-op mode games, put up a wall to prevent players
        # from getting in the turrets (that would foil our brilliant AI)
        if isinstance(ba.getsession(), ba.CoopSession):
            cmodel = self.preloaddata['player_wall_collide_model']
            self.player_wall = ba.newnode(
                'terrain',
                attrs={
                    'collide_model': cmodel,
                    'affect_bg_dynamics': False,
                    'materials': [self.preloaddata['player_wall_material']],
                },
            )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.2, 1.17, 1.1)
        gnode.ambient_color = (1.2, 1.17, 1.1)
        gnode.vignette_outer = (0.6, 0.6, 0.64)
        gnode.vignette_inner = (0.95, 0.95, 0.93)

    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        # count anything off our ground level as safe (for our platforms)
        # see if we're within edge_box
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5


class Rampage(ba.Map):
    """Wee little map with ramps on the sides."""

    from bastd.mapdata import rampage as defs

    name = 'Rampage'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag', 'rocket_hell']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'rampagePreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('rampageLevel'),
            'bottom_model': ba.getmodel('rampageLevelBottom'),
            'collide_model': ba.getcollidemodel('rampageLevelCollide'),
            'tex': ba.gettexture('rampageLevelColor'),
            'bgtex': ba.gettexture('rampageBGColor'),
            'bgtex2': ba.gettexture('rampageBGColor2'),
            'bgmodel': ba.getmodel('rampageBG'),
            'bgmodel2': ba.getmodel('rampageBG2'),
            'vr_fill_model': ba.getmodel('rampageVRFill'),
            'railing_collide_model': ba.getcollidemodel('rampageBumper'),
        }
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 0, 2))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.bottom = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bottom_model'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        self.bg2 = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel2'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex2'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_model'],
                'lighting': False,
                'vr_only': True,
                'background': True,
                'color_texture': self.preloaddata['bgtex2'],
            },
        )
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.2, 1.1, 0.97)
        gnode.ambient_color = (1.3, 1.2, 1.03)
        gnode.vignette_outer = (0.62, 0.64, 0.69)
        gnode.vignette_inner = (0.97, 0.95, 0.93)

    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5


class HoveringWood(ba.Map):
    """A map from JRMP - now in Satchel!"""

    from bastd.mapdata import hoveringWood as defs

    name = 'Hovering Plank-o-Wood'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'conquest', 'rocket_hell']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'hoveringWoodPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('hoveringWoodLevel'),
            'collide_model': ba.getcollidemodel('hoveringWoodLevelCollide'),
            'tex': ba.gettexture('hoveringWoodLevelColor'),
            'bgtex': ba.gettexture('hoveringWoodBGColor'),
            'bgmodel': ba.getmodel('thePadBG')
        }
        # fixme should chop this into vr/non-vr sections for efficiency
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.1, 1.1, 1.0)
        gnode.ambient_color = (1.1, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.65, 0.75)
        gnode.vignette_inner = (0.95, 0.95, 0.93)
    
class SpaceOdyssey(ba.Map):
    """Flying map. In space!"""

    from bastd.mapdata import space_odyssey as defs

    name = 'Galaxia Ultima'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return [
            'melee', 'keep_away', 'king_of_the_hill'
        ]

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'spacePreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('spaceOdysseyLevel'),
            'bgmodel': ba.getmodel('spaceBGModel'),
            'collide_model': ba.getcollidemodel('spaceOdysseyLevelCollide'),
            'tex': ba.gettexture('spaceLevel'),
            'bgtex': ba.gettexture('spaceBG')
        }
        return data

    @classmethod
    def get_music_type(cls) -> ba.MusicType:
        return ba.MusicType.FLYING

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, -3.7, 2.5))
        ba.getactivity()._excluded_powerups = ['fly_punch', 'dash']
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        gnode = ba.getactivity().globalsnode
        gnode.happy_thoughts_mode = True
        gnode.shadow_offset = (0.0, 8.0, 5.0)
        gnode.tint = (1.3, 1.23, 1.0)
        gnode.ambient_color = (1.3, 1.23, 1.0)
        gnode.vignette_outer = (0.64, 0.59, 0.69)
        gnode.vignette_inner = (0.95, 0.95, 0.93)
        gnode.vr_near_clip = 1.0
        self.is_flying = True

        # throw out some tips on flying
        txt = ba.newnode('text',
                         attrs={
                             'text': ba.Lstr(resource='pressJumpToFlyText'),
                             'scale': 1.2,
                             'maxwidth': 800,
                             'position': (0, 200),
                             'shadow': 0.5,
                             'flatness': 0.5,
                             'h_align': 'center',
                             'v_attach': 'bottom'
                         })
        cmb = ba.newnode('combine',
                         owner=txt,
                         attrs={
                             'size': 4,
                             'input0': 0.3,
                             'input1': 0.9,
                             'input2': 0.0
                         })
        ba.animate(cmb, 'input3', {3.0: 0, 4.0: 1, 9.0: 1, 10.0: 0})
        cmb.connectattr('output', txt, 'color')
        ba.timer(10.0, txt.delete)
        
class OnslaughtArena(ba.Map):
    """A map for Explodinary Infinite Onslaught."""

    from bastd.mapdata import doom_shroom as defs

    name = 'Onslaught Arena'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'doomShroomPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('onslaughtArenaLevel'),
            'collide_model': ba.getcollidemodel('onslaughtArenaLevelCollide'),
            'tex': ba.gettexture('onslaughtArenaLevelColor'),
            'bgtex': ba.gettexture('onslaughtArenaBG'),
            'bgmodel': ba.getmodel('onslaughtArenaBG')
        }
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.82, 1.10, 1.15)
        gnode.ambient_color = (0.75, 1.0, 0.2)
        gnode.shadow_ortho = False
        gnode.vignette_outer = (0.56, 0.7, 0.2)
        gnode.vignette_inner = (0.95, 0.95, 0.99)

    def is_point_near_edge(self,
                           point: ba.Vec3,
                           running: bool = False) -> bool:
        xpos = point.x
        zpos = point.z
        x_adj = xpos * 0.125
        z_adj = (zpos + 3.7) * 0.2
        if running:
            x_adj *= 1.4
            z_adj *= 1.4
        return x_adj * x_adj + z_adj * z_adj > 1.0
        
class ChopChop(ba.Map):
    """Map made out of literal wood."""

    from bastd.mapdata import chop_chop as defs

    name = 'Chop-Chop!'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag', 'rocket_hell']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'chopChopPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('chopChopLevel'),
            'collide_model': ba.getcollidemodel('chopChopLevelCollide'),
            'bottom_model': ba.getmodel('chopChopLevelBottom'),
            'bumper_collide_model': ba.getcollidemodel('chopChopLevelBumper'),
            'tex': ba.gettexture('chopChopLevelColor'),
            'bottom_tex': ba.gettexture('chopChopLevelBottomColor'),
            'bgtex': ba.gettexture('chopChopBG'),
            'bgmodel': ba.getmodel('bungleBungleBG'),
        }
        # fixme should chop this into vr/non-vr sections
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.bottom = ba.newnode('terrain',
            attrs={
                'model': self.preloaddata['bottom_model'],
                'lighting': False,
                'color_texture': self.preloaddata['bottom_tex']
                                 })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['bumper_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            })
        gnode = ba.getactivity().globalsnode
        gnode.shadow_ortho = True
        gnode.shadow_offset = (0, 0, -5.0)
        gnode.tint = (1.15, 1.05, 0.75)
        gnode.ambient_color = (0.93, 0.37, 0.29)
        gnode.vignette_outer = (0.6, 0.65, 0.6)
        gnode.vignette_inner = (0.95, 0.95, 0.95)
        
class WhereEaglesDare(ba.Map):
    """A map from JRMP - now in Explodinary!"""

    from bastd.mapdata import where_eagles_dare as defs

    name = 'Where Eagles Dare'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'whereEaglesDarePreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('whereEaglesDareLevel'),
            'collide_model': ba.getcollidemodel('whereEaglesDareLevelCollide'),
            'tex': ba.gettexture('whereEaglesDareLevelColor'),
            'bgtex': ba.gettexture('rampageBGColor'),
            'bgtex2': ba.gettexture('rampageBGColor2'),
            'bgmodel': ba.getmodel('rampageBG'),
            'bgmodel2': ba.getmodel('rampageBG2'),
            'vr_fill_model': ba.getmodel('rampageVRFill'),
            'railing_collide_model': ba.getcollidemodel('whereEaglesDareLevelBumper')
        }
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 0, 2))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        self.bg2 = ba.newnode('terrain',
                              attrs={
                                  'model': self.preloaddata['bgmodel2'],
                                  'lighting': False,
                                  'background': True,
                                  'color_texture': self.preloaddata['bgtex2']
                              })
        ba.newnode('terrain',
                   attrs={
                       'model': self.preloaddata['vr_fill_model'],
                       'lighting': False,
                       'vr_only': True,
                       'background': True,
                       'color_texture': self.preloaddata['bgtex2']
                   })
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True
            })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.15, 1.10, 0.82)
        gnode.ambient_color = (1.2, 1.3, 1.0)
        gnode.vignette_outer = (1, 1, 1)
        gnode.vignette_inner = (0.99, 0.99, 0.95)

    def is_point_near_edge(self,
                           point: ba.Vec3,
                           running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5
        
class Cardfoart(ba.Map):
    """A fort made out of cardboard. Get it?"""

    from bastd.mapdata import cardfoart as defs

    name = 'Cardfoart'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag', 'king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'cardfoartPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('cardfoartLevel'),
            'collide_model': ba.getcollidemodel('cardfoartLevelCollide'),
            'bumper_collide_model': ba.getcollidemodel('cardfoartLevelBumper'),
            'tex': ba.gettexture('cardfoartLevelColor'),
            'bgtex': ba.gettexture('arenaBG'),
            'bgmodel': ba.getmodel('bungleBungleBG'),  
        }
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 0, 2))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['bumper_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.15, 1.10, 0.82)
        gnode.ambient_color = (1.2, 1.3, 1.0)
        gnode.vignette_outer = (1, 1, 1)
        gnode.vignette_inner = (0.99, 0.99, 0.95)

class BetweenTheTeams(ba.Map):
    """A map with wings as team bases"""

    from bastd.mapdata import between_the_teams as defs

    name = 'The Winged Blocks'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag', 'king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'bttPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('bttLevel'),
            'collide_model': ba.getcollidemodel('bttLevelCollide'),
            'bumper_collide_model': ba.getcollidemodel('bttLevelBumper'),
            'tex': ba.gettexture('bttLevelColor'),
            'bgtex': ba.gettexture('bttBGColor'),
            'bgmodel': ba.getmodel('bttBG')
        }
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 0, 2))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['bumper_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.2, 1.1, 0.97)
        gnode.ambient_color = (1.3, 1.2, 1.03)
        gnode.vignette_outer = (0.62, 0.64, 0.69)
        gnode.vignette_inner = (0.97, 0.95, 0.93)

    def is_point_near_edge(self,
                           point: ba.Vec3,
                           running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5
        
class SculpeyForest(ba.Map):
    """A cute forest map"""

    from bastd.mapdata import forest as defs

    name = 'Sculpey Forest'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'rocket_hell']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'forestPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('forestLevel'),
            'collide_model': ba.getcollidemodel('forestLevelCollide'),
            'tex': ba.gettexture('forestLevelColor'),
            'bgtex': ba.gettexture('forestBGColor'),
            'bgmodel': ba.getmodel('forestLevelBG')
        }
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 0, 2))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.2, 0.7, 1)
        gnode.ambient_color = (0, 0, 1)
        gnode.vignette_outer = (0.62, 0.64, 0.69)
        gnode.vignette_inner = (0.97, 0.95, 0.93)

    def is_point_near_edge(self,
                           point: ba.Vec3,
                           running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5

class Walleyville(ba.Map):
    from bastd.mapdata import walleyville as defs
    name = 'Walleyville'

    @classmethod
    def get_play_types(cls) -> List[str]:
        """Return valid play types for this map."""
        return ['melee', 'king_of_the_hill', 'keep_away', 'team_flag']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'walleyvilleMapPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: Dict[str, Any] = {
            'model': ba.getmodel('walleyvilleLevel'),
            'modelWalls': ba.getmodel('walleyvilleWalls'),
            'collide_model': ba.getcollidemodel('walleyvilleLevelCollide'),
            'railing_collide_model': (ba.getcollidemodel('walleyvilleLevelBumper')),
            'tex': ba.gettexture('walleyvilleColor'),
            'texWalls': ba.gettexture('walleyvilleWallsColor'),
            'texBG': ba.gettexture('tipTopBGColor'),
            'tex_reflections': ba.gettexture('walleyvilleColor'),
            'model_bg': ba.getmodel('tipTopBG'),
            'slide_material': ba.Material()
        }  
        
        return data

    def __init__(self):
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'color': (0.9, 0.9, 0.9),
                'materials': [shared.footing_material]
            })
        self.nodealt = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'model': self.preloaddata['modelWalls'],
                'color': (0.9, 0.9, 0.9),
                'color_texture': self.preloaddata['texWalls'],
            })
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['railing_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True
            })
        self.background = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'model': self.preloaddata['model_bg'],
                'color': (1.1, 0.7, 0.2),
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['texBG']
            })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.1, 1.1, 1.1)
        gnode.ambient_color = (2, 0.7, 0.2)
        gnode.vignette_outer = (0.7, 0.7, 0.7)
        gnode.vignette_inner = (0.9, 0.9, 0.9)

class BlockFortress(ba.Map):
    """A simple square shaped map with a raised edge."""

    from bastd.mapdata import block_fortress as defs

    name = 'Block Fortress'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'king_of_the_hill', 'rocket_hell']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'arenaPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('arenaLevel'),
            'collide_model': ba.getcollidemodel('arenaLevelCollide'),
            'tex': ba.gettexture('arenaLevelColor'),
            'bgtex': ba.gettexture('arenaBG'),
            'bgmodel': ba.getmodel('thePadBG')
        }
        # fixme should chop this into vr/non-vr sections for efficiency
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.8, 0.8, 0.8)
        gnode.ambient_color = (0.6, 0.6, 0.6)
        gnode.vignette_outer = (1, 1, 1)
        gnode.vignette_inner = (0.95, 0.95, 0.95)
        
class Morning(ba.Map):
    """Map ported from JRMP - redesigned and renamed."""

    from bastd.mapdata import morning as defs

    name = 'Sunrise'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'morningPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('morningLevel'),
            'collide_model': ba.getcollidemodel('morningLevelCollide'),
            'bumper_collide_model': ba.getcollidemodel('morningLevelBumper'),
            'tex': ba.gettexture('morningLevelColor'),
            'bgtex': ba.gettexture('morningBG'),
            'bgmodel': ba.getmodel('morningBG'),
        }
        # fixme should chop this into vr/non-vr sections for efficiency
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        self.railing = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['bumper_collide_model'],
                'materials': [shared.railing_material],
                'bumper': True,
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.1, 1.1, 1.0)
        gnode.ambient_color = (1.1, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.65, 0.75)
        gnode.vignette_inner = (0.95, 0.95, 0.93)
        
class SoccerStadium(ba.Map):
    """Stadium map used for soccer."""

    from bastd.mapdata import soccer_stadium as defs

    name = 'Soccer Stadium'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'soccer', 'team_flag', 'keep_away', 'rocket_hell']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'soccerStadiumPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'models': (
                ba.getmodel('soccerStadiumOuter'),
                ba.getmodel('soccerStadiumInner'),
                ba.getmodel('hockeyStadiumStands'),
            ),
            'vr_fill_model': ba.getmodel('footballStadiumVRFill'),
            'collide_model': ba.getcollidemodel('soccerStadiumCollide'),
            'tex': ba.gettexture('soccerStadiumLevelColor'),
            'stands_tex': ba.gettexture('footballStadium'),
        }
        mat = ba.Material()
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'model': self.preloaddata['models'][0],
                'collide_model': self.preloaddata['collide_model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [
                    shared.footing_material,
                ],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_model'],
                'vr_only': True,
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['stands_tex'],
            },
        )
        mats = [shared.footing_material]
        self.floor = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['models'][1],
                'color_texture': self.preloaddata['tex'],
                'materials': mats,
            },
        )
        self.stands = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['models'][2],
                'color_texture': self.preloaddata['stands_tex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.debris_kill_height = -0.3
        gnode.tint = (1.2, 1.3, 1.33)
        gnode.ambient_color = (1.15, 1.25, 1.6)
        gnode.vignette_outer = (0.66, 0.67, 0.73)
        gnode.vignette_inner = (0.93, 0.93, 0.95)
        gnode.vr_camera_offset = (0, -0.8, -1.1)
        gnode.vr_near_clip = 0.5
        
class ExplodinaryRunaround(ba.Map):
    """Map used for Explodinary Runaround."""

    from bastd.mapdata import expl_runaround as defs

    name = 'Explodinary Runaround'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'explRunaroundPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('explRunaroundLevel'),
            'model_bottom': ba.getmodel('explRunaroundLevelBottom'),
            'collide_model': ba.getcollidemodel('explRunaroundLevelCollide'),
            'tex': ba.gettexture('explRunaroundLevelColor'),
            'tex_bottom': ba.gettexture('explRunaroundLevelBottomColor'),
            'bgtex': ba.gettexture('natureBackgroundColor'),
            'bgmodel': ba.getmodel('natureBackground'),
            'collide_bg':ba.getcollidemodel('natureBackgroundCollide'),
            'player_wall_collide_model': ba.getcollidemodel('expl_wall'),
            'player_wall_material': ba.Material(),
            'bg_material': ba.Material(),
        }
        
        # anything that needs to hit the wall can apply this material
        data['collide_with_wall_material'] = ba.Material()
        data['vr_fill_mound_model'] = ba.getmodel('stepRightUpVRFillMound')
        data['vr_fill_mound_tex'] = ba.gettexture('vrFillMound')
        data['bg_material'].add_actions(actions=('modify_part_collision', 'friction', 10.0))
        data['player_wall_material'].add_actions(
            conditions=(
                'they_dont_have_material',
                data['collide_with_wall_material'],
            ),
            actions=('modify_part_collision', 'collide', False)),
            
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 1, 1))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.node_bottom = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'model': self.preloaddata['model_bottom'],
                'lighting': False,
                'color_texture': self.preloaddata['tex_bottom'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.53, 0.57, 0.5),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.player_wall = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['player_wall_collide_model'],
                'affect_bg_dynamics': False,
                'materials': [self.preloaddata['player_wall_material']]
            },
        )
        self.bg_collide = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['collide_bg'],
                'materials': [
                    shared.footing_material,
                    self.preloaddata['bg_material'],
                    shared.death_material,
                ],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.15, 1.11, 1.03)
        gnode.ambient_color = (1.2, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.73, 0.7)
        gnode.vignette_inner = (0.95, 0.95, 0.95)

    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        # see if we're within edge_box
        boxes = self.defs.boxes
        box_position = boxes['edge_box'][0:3]
        box_scale = boxes['edge_box'][6:9]
        box_position2 = boxes['edge_box2'][0:3]
        box_scale2 = boxes['edge_box2'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        xpos2 = (point.x - box_position2[0]) / box_scale2[0]
        zpos2 = (point.z - box_position2[2]) / box_scale2[2]
        # if we're outside of *both* boxes we're near the edge
        return (xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5) and (
            xpos2 < -0.5 or xpos2 > 0.5 or zpos2 < -0.5 or zpos2 > 0.5
        )
        
class Snowhold(ba.Map):
    """A stronghold filled with snow and ice."""

    from bastd.mapdata import snowhold as defs

    name = 'Snowhold'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'team_flag', 'king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'snowholdPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('snowholdIceFloor'),
            'model_top': ba.getmodel('snowholdLevel'),
            'model_reflections': ba.getmodel('snowholdReflections'),
            'collide_model': ba.getcollidemodel('snowholdLevelCollide'),
            'ice_collide_model': ba.getcollidemodel('snowholdIceCollide'),
            'tex': ba.gettexture('snowholdLevelColor'),
            'tex_reflections': ba.gettexture('lakeFrigidReflections'),
            'bgtex': ba.gettexture('snowholdBGColor'),
            'bgtex2': ba.gettexture('snowholdBGColor2'),
            'bgtex3': ba.gettexture('snowholdBGColor3'),
            'bgmodel': ba.getmodel('rampageBG'),
            'bgmodel2': ba.getmodel('rampageBG2'),
            'bgmodel3': ba.getmodel('snowholdBGModel'),
        }
        mat = ba.Material()
        mat.add_actions(actions=('modify_part_collision', 'friction', 0.01))
        data['ice_material'] = mat
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['ice_collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [
                    shared.footing_material,
                    self.preloaddata['ice_material'],
                ],
            },
        )
        self.nodealt = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [
                    shared.footing_material,
                ],
            },
        )
        self.top = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_top'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        self.ref = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model_reflections'],
                'lighting': False,
                'overlay': True,
                'opacity': 0.15,
                'color_texture': self.preloaddata['tex_reflections'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.bg2 = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel2'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex2'],
            },
        )
        self.bg3 = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel3'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex3'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1, 1, 1)
        gnode.ambient_color = (1, 1, 1)
        gnode.shadow_ortho = True
        gnode.vignette_outer = (0.86, 0.86, 0.86)
        gnode.vignette_inner = (0.95, 0.95, 0.99)
        gnode.vr_near_clip = 0.5
        
        
#KABLOOYA GAMEMODES
class Kablooya(ba.Map):
    """A map dedicated for Kablooya Onslaught"""

    from bastd.mapdata import kablooya as defs

    name = 'Kablooya'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'kablooyaPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('waveOnslaughtLevel'),
            'collide_model': ba.getcollidemodel('waveOnslaughtLevelCollide'),
            'tex': ba.gettexture('waveOnslaughtLevelColor'),
            'bgtex': ba.gettexture('arenaBG'),
            'bgmodel': ba.getmodel('bungleBungleBG'),
        }
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 0, 2))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.15, 1.10, 0.82)
        gnode.ambient_color = (1.2, 1.3, 1.0)
        gnode.vignette_outer = (1, 1, 1)
        gnode.vignette_inner = (0.99, 0.99, 0.95)
    
    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5

class EndlessKablooya(ba.Map):
    """A map dedicated for Endless Kablooya Onslaught"""

    from bastd.mapdata import kablooya as defs

    name = 'Endless Kablooya'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'kablooyaEndlessPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('waveOnslaughtLevel'),
            'collide_model': ba.getcollidemodel('waveOnslaughtLevelCollide'),
            'tex': ba.gettexture('waveOnslaughtEndlessLevelColor'),
            'bgtex': ba.gettexture('arenaBG'),
            'bgmodel': ba.getmodel('bungleBungleBG'),
        }
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 0, 2))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.15, 1.10, 0.82)
        gnode.ambient_color = (1.2, 1.3, 1.0)
        gnode.vignette_outer = (1, 1, 1)
        gnode.vignette_inner = (0.99, 0.99, 0.95)
    
    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5
        
class TowerS(ba.Map):
    """Tower D reskin for Kablooya Runaround gamemode."""

    from bastd.mapdata import tower_d as defs

    name = 'Tower S'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'towerSPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('towerDLevel'),
            'model_bottom': ba.getmodel('towerDLevelBottom'),
            'collide_model': ba.getcollidemodel('towerDLevelCollide'),
            'tex': ba.gettexture('towerSLevelColor'),
            'bgtex': ba.gettexture('menuBG'),
            'bgmodel': ba.getmodel('thePadBG'),
            'player_wall_collide_model': ba.getcollidemodel('towerDPlayerWall'),
            'player_wall_material': ba.Material(),
        }
        # fixme should chop this into vr/non-vr sections
        data['player_wall_material'].add_actions(
            actions=('modify_part_collision', 'friction', 0.0)
        )
        # anything that needs to hit the wall can apply this material
        data['collide_with_wall_material'] = ba.Material()
        data['player_wall_material'].add_actions(
            conditions=(
                'they_dont_have_material',
                data['collide_with_wall_material'],
            ),
            actions=('modify_part_collision', 'collide', False),
        )
        data['vr_fill_mound_model'] = ba.getmodel('stepRightUpVRFillMound')
        data['vr_fill_mound_tex'] = ba.gettexture('vrFillMound')
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 1, 1))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.node_bottom = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'model': self.preloaddata['model_bottom'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.53, 0.57, 0.5),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.player_wall = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['player_wall_collide_model'],
                'affect_bg_dynamics': False,
                'materials': [self.preloaddata['player_wall_material']],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.15, 1.11, 1.03)
        gnode.ambient_color = (1.2, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.73, 0.7)
        gnode.vignette_inner = (0.95, 0.95, 0.95)

class EndlessS(ba.Map):
    """Tower D reskin for Endless Kablooya Runaround gamemode."""

    from bastd.mapdata import tower_d as defs

    name = 'Endless Tower S'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'endlessTowerSPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('towerDLevel'),
            'model_bottom': ba.getmodel('towerDLevelBottom'),
            'collide_model': ba.getcollidemodel('towerDLevelCollide'),
            'tex': ba.gettexture('endlessTowerSLevelColor'),
            'bgtex': ba.gettexture('menuBG'),
            'bgmodel': ba.getmodel('thePadBG'),
            'player_wall_collide_model': ba.getcollidemodel('towerDPlayerWall'),
            'player_wall_material': ba.Material(),
        }
        # fixme should chop this into vr/non-vr sections
        data['player_wall_material'].add_actions(
            actions=('modify_part_collision', 'friction', 0.0)
        )
        # anything that needs to hit the wall can apply this material
        data['collide_with_wall_material'] = ba.Material()
        data['player_wall_material'].add_actions(
            conditions=(
                'they_dont_have_material',
                data['collide_with_wall_material'],
            ),
            actions=('modify_part_collision', 'collide', False),
        )
        data['vr_fill_mound_model'] = ba.getmodel('stepRightUpVRFillMound')
        data['vr_fill_mound_tex'] = ba.gettexture('vrFillMound')
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 1, 1))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.node_bottom = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'model': self.preloaddata['model_bottom'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.53, 0.57, 0.5),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.player_wall = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['player_wall_collide_model'],
                'affect_bg_dynamics': False,
                'materials': [self.preloaddata['player_wall_material']],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.15, 1.11, 1.03)
        gnode.ambient_color = (1.2, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.73, 0.7)
        gnode.vignette_inner = (0.95, 0.95, 0.95)
        
    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        # see if we're within edge_box
        boxes = self.defs.boxes
        box_position = boxes['edge_box'][0:3]
        box_scale = boxes['edge_box'][6:9]
        box_position2 = boxes['edge_box2'][0:3]
        box_scale2 = boxes['edge_box2'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        xpos2 = (point.x - box_position2[0]) / box_scale2[0]
        zpos2 = (point.z - box_position2[2]) / box_scale2[2]
        # if we're outside of *both* boxes we're near the edge
        return (xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5) and (
            xpos2 < -0.5 or xpos2 > 0.5 or zpos2 < -0.5 or zpos2 > 0.5
        )

class PathwayPandemonium(ba.Map):
    """Map used for Pathway Pandemonium."""

    from bastd.mapdata import pathway_pandemonium as defs

    name = 'Pathway Pandemonium'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'pathwayPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('pathwayPandemoniumLevel'),
            'collide_model': ba.getcollidemodel('pathwayPandemoniumLevelCollide'),
            'tex': ba.gettexture('pathwayPandemoniumLevelColor'),
            'bgtex': ba.gettexture('snowholdBGColor'),
            'bgtex2': ba.gettexture('snowholdBGColor2'),
            'bgtex3': ba.gettexture('snowholdBGColor3'),
            'bgmodel': ba.getmodel('rampageBG'),
            'bgmodel2': ba.getmodel('rampageBG2'),
            'bgmodel3': ba.getmodel('snowholdBGModel'),
            'player_wall_collide_model': ba.getcollidemodel('pathwayWall'),
            'player_wall_material': ba.Material(),
        }
        
        # anything that needs to hit the wall can apply this material
        data['collide_with_wall_material'] = ba.Material()
        data['player_wall_material'].add_actions(
            conditions=(
                'they_dont_have_material',
                data['collide_with_wall_material'],
            ),
            actions=('modify_part_collision', 'collide', False)),
            
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 1, 1))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.player_wall = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['player_wall_collide_model'],
                'affect_bg_dynamics': False,
                'materials': [self.preloaddata['player_wall_material']]
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.bg2 = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel2'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex2'],
            },
        )
        self.bg3 = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel3'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex3'],
            },
        )
        gnode = ba.getactivity().globalsnode
        # (1.15, 1.11, 1.03)
        # (1.2, 1.1, 1.0)
        # (0.7, 0.73, 0.7)
        # (0.95, 0.95, 0.95)

        # Day/Night cycle
        time_cycle = [
            # Tint
            ['tint', {
                0: (1.05, 1.07, 1.1),
                75: (0.9, 0.7, 1.0),
                140: (0.54, 0.62, 0.95),
                170: (0.54, 0.62, 0.95),
                200: (1.05, 1.07, 1.1),
            }],
            # Ambient
            ['ambient_color', {
                0: (1.1, 1.12, 1.1),
                90: (2.1, 1.4, 3.9),
                140: (1.2, 1.4, 3.9),
                170: (1.2, 1.4, 3.9),
                200: (1.1, 1.12, 1.1),
            }],
            # Vignette OUT
            ['vignette_outer', {
                0: (0.7, 0.73, 0.8),
                110: (0.6, 0.68, 0.71),
                140: (0.62, 0.75, 0.8),
                170: (0.89, 0.89, 0.97),
                200: (0.7, 0.73, 0.8),
            }],
            # Vignette IN
            ['vignette_inner', {
                0: (1, 1, 1),
                140: (0.9, 0.94, 1),
                170: (0.9, 0.94, 1),
                200: (1, 1, 1),
            }],
        ]

        self._time_clocks = []

        for x in time_cycle: self._time_clocks.append(ba.animate_array(gnode, x[0], 3, x[1], loop=True))
            

    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        # see if we're within edge_box
        boxes = self.defs.boxes
        box_position = boxes['edge_box'][0:3]
        box_scale = boxes['edge_box'][6:9]
        box_position2 = boxes['edge_box2'][0:3]
        box_scale2 = boxes['edge_box2'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        xpos2 = (point.x - box_position2[0]) / box_scale2[0]
        zpos2 = (point.z - box_position2[2]) / box_scale2[2]
        # if we're outside of *both* boxes we're near the edge
        return (xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5) and (
            xpos2 < -0.5 or xpos2 > 0.5 or zpos2 < -0.5 or zpos2 > 0.5
        )

class SourFlower(ba.Map):
    """A giant Flower. Which is sour!"""

    from bastd.mapdata import sour_flower as defs

    name = 'Sour Flower'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'king_of_the_hill', 'rocket_hell']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'sourFlowerPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('sourFlowerLevel'),
            'collide_model': ba.getcollidemodel('sourFlowerLevelCollide'),
            'tex': ba.gettexture('sourFlowerLevelColor'),
            'bgtex': ba.gettexture('sourFlowerBGColor'),
            'bgmodel': ba.getmodel('doomShroomBG'),
            'vr_fill_model': ba.getmodel('doomShroomVRFill'),
        }
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_model'],
                'lighting': False,
                'vr_only': True,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.82, 1.25, 1)
        gnode.ambient_color = (0.9, 1.3, 1.1)
        gnode.shadow_ortho = False
        gnode.vignette_outer = (0.76, 0.76, 0.76)
        gnode.vignette_inner = (0.95, 0.95, 0.99)

    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        xpos = point.x
        zpos = point.z
        x_adj = xpos * 0.125
        z_adj = (zpos + 3.7) * 0.2
        if running:
            x_adj *= 1.4
            z_adj *= 1.4
        return x_adj * x_adj + z_adj * z_adj > 1.0

class FuseCruise(ba.Map):
    """A little, bombastic ship!"""

    from bastd.mapdata import fuse_cruise as defs

    name = 'Fuse Cruise'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'king_of_the_hill', 'rocket_hell']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'fuseCruisePreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('fuseCruiseLevel'),
            'collide_model': ba.getcollidemodel('fuseCruiseLevelCollide'),
            'water_collide_model': ba.getcollidemodel('fuseCruiseWaterCollide'),
            'seamodel': ba.getmodel('fuseCruiseSea'),
            'tex': ba.gettexture('fuseCruiseLevelColor'),
            'seatex': ba.gettexture('fuseCruiseSea'),
            'bgtex': ba.gettexture('sourFlowerBGColor'),
            'bgmodel': ba.getmodel('thePadBG'),
        }
        return data
    
    @classmethod
    def get_music_type(cls) -> ba.MusicType:
        return ba.MusicType.FUSE_CRUISE
        
    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        
        water_material = ba.Material()
        water_emit = ba.Material()
        
        water_material.add_actions(
            actions=(("modify_part_collision", "collide", True),
                     ("modify_part_collision", "physical", False),
                     ("call", "at_connect", self.water_collide)))

        
        water_emit.add_actions(
            actions=(("modify_part_collision", "collide", True),
                     ("modify_part_collision", "physical", False),
                     ("call", "at_connect", self.emit_water)))

        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.sea = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['seamodel'],
                'collide_model': self.preloaddata['water_collide_model'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['seatex'],
                'materials': [water_material, water_emit],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        sea_sound = ba.getsound('seaAmbience')
        ba.newnode('sound',owner=self.sea,attrs={'sound':sea_sound,'volume':0.25})
        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.8, 0.8, 0.8)
        gnode.ambient_color = (1, 1, 1)
        gnode.vignette_outer = (1, 1, 1)
        gnode.vignette_inner = (1, 1, 1)
    
    def emit_water(self):
        node = ba.getcollision().opposingnode
        ba.emitfx(
                position=node.position,
                velocity=node.velocity,
                count=20 if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                spread=1,
                scale=1,
                chunk_type='sweat',
            );
    
    def water_collide(self):
        node = ba.getcollision().opposingnode
        impact_sound = ba.getsound('waterImpactBig')
        if node.exists():
            ba.playsound(impact_sound, position=node.position)
            node.handlemessage('impulse', node.position[0], node.position[1], node.position[2],
                                    0, 0, 0,
                                    50, 50, 0, 0, 0, 1, 0)
        
    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        xpos = point.x
        zpos = point.z
        x_adj = xpos * 0.125
        z_adj = (zpos + 3.7) * 0.2
        if running:
            x_adj *= 1.4
            z_adj *= 1.4
        return x_adj * x_adj + z_adj * z_adj > 1.0

class Sunset(ba.Map):
    """Remake of Sunrise that became it's own map!"""

    from bastd.mapdata import sunset as defs

    name = 'Sunset'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return ['melee', 'keep_away', 'king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'sunsetPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('sunsetLevel'),
            'model_bottom': ba.getmodel('sunsetLevelBottom'),
            'collide_model': ba.getcollidemodel('sunsetLevelCollide'),
            #'bumper_collide_model': ba.getcollidemodel('morningLevelBumper'),
            'tex': ba.gettexture('sunsetLevelColor'),
            'bgtex': ba.gettexture('morningBG'),
            'bgmodel': ba.getmodel('morningBG'),
        }
        # fixme should chop this into vr/non-vr sections for efficiency
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.bottom = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'model': self.preloaddata['model_bottom'],
                'lighting': False,
                'color_texture': self.preloaddata['tex'],
            })
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        #self.railing = ba.newnode(
        #    'terrain',
        #    attrs={
        #        'collide_model': self.preloaddata['bumper_collide_model'],
        #        'materials': [shared.railing_material],
        #        'bumper': True,
        #    },
        #)
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.1, 1.1, 1.0)
        gnode.ambient_color = (1.1, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.65, 0.75)
        gnode.vignette_inner = (0.95, 0.95, 0.93)

class RouteRoulette(ba.Map):
    """Map used for Route Roulette."""

    from bastd.mapdata import roulette as defs

    name = 'Route Roulette'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'explRunaroundPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('rouletteLevel'),
            'collide_model': ba.getcollidemodel('rouletteLevelCollide'),
            'tex': ba.gettexture('rouletteLevelColor'),
            'bgtex': ba.gettexture('chopChopBG'),
            'bgmodel': ba.getmodel('thePadBG'),
            'player_wall_collide_model': ba.getcollidemodel('rouletteWall'),
            'player_wall_material': ba.Material(),
            'bg_material': ba.Material(),
        }
        
        # anything that needs to hit the wall can apply this material
        data['collide_with_wall_material'] = ba.Material()
        data['vr_fill_mound_model'] = ba.getmodel('stepRightUpVRFillMound')
        data['vr_fill_mound_tex'] = ba.gettexture('vrFillMound')
        data['bg_material'].add_actions(actions=('modify_part_collision', 'friction', 10.0))
        data['player_wall_material'].add_actions(
            conditions=(
                'they_dont_have_material',
                data['collide_with_wall_material'],
            ),
            actions=('modify_part_collision', 'collide', False)),
            
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 1, 1))
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.53, 0.57, 0.5),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.player_wall = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['player_wall_collide_model'],
                'affect_bg_dynamics': False,
                'materials': [self.preloaddata['player_wall_material']]
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.15, 1.11, 1.03)
        gnode.ambient_color = (1.2, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.73, 0.7)
        gnode.vignette_inner = (0.95, 0.95, 0.95)

    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        # see if we're within edge_box
        boxes = self.defs.boxes
        box_position = boxes['edge_box'][0:3]
        box_scale = boxes['edge_box'][6:9]
        box_position2 = boxes['edge_box2'][0:3]
        box_scale2 = boxes['edge_box2'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        xpos2 = (point.x - box_position2[0]) / box_scale2[0]
        zpos2 = (point.z - box_position2[2]) / box_scale2[2]
        # if we're outside of *both* boxes we're near the edge
        return (xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5) and (
            xpos2 < -0.5 or xpos2 > 0.5 or zpos2 < -0.5 or zpos2 > 0.5
        )

class Hub(ba.Map):
    """A charming field to chill on."""

    from bastd.mapdata import hub as defs

    name = 'Hub'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'rampagePreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('hubLevel'),
            'collide_model': ba.getcollidemodel('hubLevelCollide'),
            'water_collide_model': ba.getcollidemodel('hubWaterCollide'),
            'tex': ba.gettexture('hubLevelColor'),
            'bgtex': ba.gettexture('hoveringWoodBGColor'),
            'bgmodel': ba.getmodel('thePadBG')
        }
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 0, 2))
        shared = SharedObjects.get()
        
        
        water_material = ba.Material()
        water_emit = ba.Material()
        
        water_material.add_actions(
            actions=(("modify_part_collision", "collide", True),
                     ("modify_part_collision", "physical", False),
                     ("call", "at_connect", self.water_collide)))

        
        water_emit.add_actions(
            actions=(("modify_part_collision", "collide", True),
                     ("modify_part_collision", "physical", False),
                     ("call", "at_connect", self.emit_water)))
                     
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.water = ba.newnode(
            'terrain',
            attrs={
                'collide_model': self.preloaddata['water_collide_model'],
                'lighting': False,
                'background': True,
                'materials': [water_material, water_emit],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.2, 1.1, 0.97)
        gnode.ambient_color = (1.3, 1.2, 1.03)
        gnode.vignette_outer = (0.62, 0.64, 0.69)
        gnode.vignette_inner = (0.97, 0.95, 0.93)
    
    def emit_water(self):
        node = ba.getcollision().opposingnode
        ba.emitfx(
                position=node.position,
                velocity=node.velocity,
                count=7 if not ba.app.config.get("BSE: Reduced Particles", False) else 3,
                spread=0.25,
                scale=1,
                chunk_type='sweat',
            );
    
    def water_collide(self):
        node = ba.getcollision().opposingnode
        impact_sound = ba.getsound('waterImpactSmall')
        if node.exists():
            ba.playsound(impact_sound, position=node.position)
            node.handlemessage('impulse', node.position[0], node.position[1], node.position[2],
                                    0, 0, 0,
                                    37, 37, 0, 0, 0, 1, 0)

class Tree(ba.Map):
    """Daily Bombnuts on a Tree!!!"""

    from bastd.mapdata import doom_shroom as defs

    name = 'Tree'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'doomShroomPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('bombnutsLevel'),
            'collide_model': ba.getcollidemodel('bombnutsLevelCollide'),
            'tex': ba.gettexture('bombnutsLevelColor'),
            'bottom_tex': ba.gettexture('bombnutsLevelBottomColor'),
            'bgtex': ba.gettexture('hoveringWoodBGColor'),
            'bgmodel': ba.getmodel('onslaughtArenaBG'),
            'bottom_model': ba.getmodel('bombnutsLevelBottom')
        }
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        self.bottom = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bottom_model'],
                'lighting': False,
                'color_texture': self.preloaddata['bottom_tex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.2, 1.1, 0.97)
        gnode.ambient_color = (1.3, 1.2, 1.03)
        gnode.vignette_outer = (0.62, 0.64, 0.69)
        gnode.vignette_inner = (0.97, 0.95, 0.93)

    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        xpos = point.x
        zpos = point.z
        x_adj = xpos * 0.125
        z_adj = (zpos + 3.7) * 0.2
        if running:
            x_adj *= 1.4
            z_adj *= 1.4
        return x_adj * x_adj + z_adj * z_adj > 1.0

class ClayishDonut(ba.Map):
    """Donut shaped map for racing and FFA."""

    from bastd.mapdata import clayish_donut as defs

    name = 'Clay-ish Donut'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return [
            'race',
            'melee',
            'team_flag',
        ]

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'donutPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model_top': ba.getmodel('donutLevel'),
            'collide_model': ba.getcollidemodel('donutLevelCollide'),
            'tex': ba.gettexture('donutLevelColor'),
            'bgtex': ba.gettexture('donutBG'),
            'bgmodel': ba.getmodel('thePadBG')
        }
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'color': (0.7, 0.7, 0.7),
                'model': self.preloaddata['model_top'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.1, 1.2, 1.3)
        gnode.ambient_color = (1.1, 1.2, 1.3)
        gnode.vignette_outer = (0.65, 0.6, 0.55)
        gnode.vignette_inner = (0.9, 0.9, 0.93)
        
##EXPLODINARY CAMPAIGN MAPS
class TheBeginning(ba.Map):
    """The map used for the first level of BSE Campaign."""

    from bastd.mapdata import the_beginning as defs

    name = 'The Beginning'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'thePadPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('theBeginningNature'),
            'house_model': ba.getmodel('theBeginningHouse'),
            'collide_model': ba.getcollidemodel('theBeginningLevelCollide'),
            'wall_model': ba.getcollidemodel('theBeginningWall'),
            'player_wall_collide_model': ba.getcollidemodel('theBeginningPlayerWall'),
            'tex': ba.gettexture('theBeginningLevelColor'),
            'house_tex': ba.gettexture('theBeginningHouseColor'),
            'bgtex': ba.gettexture('panoramaBG'),
            'bgmodel': ba.getmodel('panoramaBG'),
            'vr_fill_mound_model': ba.getmodel('thePadVRFillMound'),
            'vr_fill_mound_tex': ba.gettexture('vrFillMound'),
            'wall_material': ba.Material(),
            'player_wall_material': ba.Material(),
        }
        data['collide_with_wall_material'] = ba.Material()
        data['wall_material'].add_actions(actions=('modify_part_collision', 'friction', 10))
        data['player_wall_material'].add_actions(
            conditions=(
                'they_dont_have_material',
                data['collide_with_wall_material'],
            ),
            actions=('modify_part_collision', 'collide', False)),
        # fixme should chop this into vr/non-vr sections for efficiency
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.house = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['house_model'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['house_tex'],
            },
        )
        self.wall = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['wall_model'],
                'materials': [shared.railing_material, self.preloaddata['wall_material']],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.56, 0.55, 0.47),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.1, 1.1, 1.0)
        gnode.ambient_color = (1.1, 1.1, 1.0)
        gnode.vignette_outer = (0.7, 0.65, 0.75)
        gnode.vignette_inner = (0.95, 0.95, 0.93)

class MysteriousSwamp(ba.Map):
    """The map used for the Swamp level of BSE Campaign."""

    from bastd.mapdata import swamp as defs

    name = 'Mysterious Swamp'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'thePadPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('swampLevel'),
            'collide_model': ba.getcollidemodel('swampLevelCollide'),
            'lily_model': ba.getmodel('swampLilyModel'),
            'water_model': ba.getmodel('swampWaterModel'),
            'water_collide_model': ba.getcollidemodel('swampWaterCollide'),
            'raft_model': ba.getmodel('swampRaftModel'),
            'tex': ba.gettexture('swampLevelColor'),
            'bgtex': ba.gettexture('menuBG'),
            'bgmodel': ba.getmodel('thePadBG'),
            'water_tex': ba.gettexture('swampWaterColor'),
            'raft_tex': ba.gettexture('swampRaftColor'),
            'lily_tex': ba.gettexture('theBeginningLevelColor'),
            'vr_fill_mound_model': ba.getmodel('thePadVRFillMound'),
            'vr_fill_mound_tex': ba.gettexture('vrFillMound'),
        }
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        
        water_material = ba.Material()
        water_emit = ba.Material()
        
        water_material.add_actions(
            actions=(("modify_part_collision", "collide", True),
                     ("modify_part_collision", "physical", False),
                     ("call", "at_connect", self.water_collide)))

        
        water_emit.add_actions(
            actions=(("modify_part_collision", "collide", True),
                     ("modify_part_collision", "physical", False),
                     ("call", "at_connect", self.emit_water)))

        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.raft = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'model': self.preloaddata['raft_model'],
                'color_texture': self.preloaddata['raft_tex'],
                'materials': [shared.footing_material],
            },
        )
        self.water = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['water_model'],
                'collide_model': self.preloaddata['water_collide_model'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['water_tex'],
                'materials': [water_material, water_emit],
            },
        )
        self.lily = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['lily_model'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['lily_tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        swamp_sound = ba.getsound('swampAmbience')
        ba.newnode('sound',owner=self.background,attrs={'sound':swamp_sound,'volume':0.35})
        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.5, 0.5, 0.5)
        gnode.ambient_color = (0.1, 0.35, 0.1)
        gnode.shadow_ortho = True
        gnode.vignette_outer = (0.76, 0.76, 0.76)
        gnode.vignette_inner = (0.95, 0.95, 0.99)
        
    def emit_water(self):
        node = ba.getcollision().opposingnode
        ba.emitfx(
                position=node.position,
                velocity=node.velocity,
                count=10 if not ba.app.config.get("BSE: Reduced Particles", False) else 5,
                spread=0.25,
                scale=1.5,
                chunk_type='sweat',
            );
    
    def water_collide(self):
        node = ba.getcollision().opposingnode
        impact_sound = ba.getsound('waterImpactBig')
        ba.playsound(impact_sound, 0.5, position=node.position)
            
    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5

class Grotto(ba.Map):
    """A dark Grotto..."""

    from bastd.mapdata import grotto as defs

    name = 'Grotto'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'grottoPreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('grottoLevel'),
            'collide_model': ba.getcollidemodel('grottoLevelCollide'),
            'tex': ba.gettexture('grottoLevelColor'),
            'bgtex': ba.gettexture('reflectionSharpest_+x'),
            'bgmodel': ba.getmodel('thePadBG'),
        }
        data['vr_fill_mound_model'] = ba.getmodel('stepRightUpVRFillMound')
        data['vr_fill_mound_tex'] = ba.gettexture('vrFillMound')
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.53, 0.57, 0.5),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        grotto_sound = ba.getsound('grottoAmbience')
        ba.newnode('sound',owner=self.background,attrs={'sound':grotto_sound,'volume':0.65})
        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.41,0.59,0.64)
        gnode.ambient_color  = (0.88, 0.91, 1.2)
        gnode.vignette_outer = (0.39, 0.42, 0.49)
        gnode.vignette_inner = (0.99, 0.98, 0.98)
        
    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5

class AlpineGateway(ba.Map):
    """Entrance to the mountain path."""

    from bastd.mapdata import alpine_gateway as defs

    name = 'Alpine Gateway'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'fuseCruiseSea'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('alpineGateLevel'),
            'collide_model': ba.getcollidemodel('alpineGateLevelCollide'),
            'wall_model': ba.getcollidemodel('alpineGateWall'),
            'tex': ba.gettexture('alpineGateLevelColor'),
            'bgtex': ba.gettexture('alpineBG'),
            'bgmodel': ba.getmodel('thePadBG'),
            'bgmodel2': ba.getmodel('alpineBG'),
            'bgtex2': ba.gettexture('bgTile'),
            'wall_material': ba.Material(),
        }
        data['wall_material'].add_actions(actions=('modify_part_collision', 'friction', 10))
        data['vr_fill_mound_model'] = ba.getmodel('stepRightUpVRFillMound')
        data['vr_fill_mound_tex'] = ba.gettexture('vrFillMound')
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.wall = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['wall_model'],
                'materials': [shared.railing_material, self.preloaddata['wall_material']],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.53, 0.57, 0.5),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        alpine_sound = ba.getsound('alpineAmbience')
        ba.newnode('sound',owner=self.background,attrs={'sound':alpine_sound,'volume':0.25})
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.2, 1.17, 1.1)
        gnode.ambient_color = (1.2, 1.17, 1.1)
        gnode.vignette_outer = (0.6, 0.6, 0.64)
        gnode.vignette_inner = (0.95, 0.95, 0.93)
        
    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5

class MountChill(ba.Map):
    """A mountain. Chills, huh!"""

    from bastd.mapdata import mount_chill as defs

    name = 'Mount Chill'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'fuseCruiseSea'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('mountChillLevel'),
            'collide_model': ba.getcollidemodel('mountChillLevelCollide'),
            'tex': ba.gettexture('mountChillLevelColor'),
            'snowmodel': ba.getmodel('mountChillSnow'),
            'snowtex': ba.gettexture('mountChillSnowColor'),
            'bgtex': ba.gettexture('mountChillBG'),
            'bgmodel': ba.getmodel('thePadBG'),
        }
        data['vr_fill_mound_model'] = ba.getmodel('stepRightUpVRFillMound')
        data['vr_fill_mound_tex'] = ba.gettexture('vrFillMound')
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['snowmodel'],
                'color_texture': self.preloaddata['snowtex'],
                'materials': [shared.footing_material],
            },
        )
        self.mountain = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['model'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['tex'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.53, 0.57, 0.5),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.05, 1.0, 1.12)
        gnode.ambient_color = (1.2, 1.17, 1.1)
        gnode.vignette_outer = (0.6, 0.55, 0.69)
        gnode.vignette_inner = (0.95, 0.95, 0.93)
        
    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5

class HotAirBalloon(ba.Map):
    """A balloon!"""

    from bastd.mapdata import balloon as defs

    name = 'Hot Air Havoc'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'fuseCruiseSea'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('balloonLevel'),
            'collide_model': ba.getcollidemodel('balloonLevelCollide'),
            'collide_border': ba.getcollidemodel('balloonBorderCollide'),
            'tex': ba.gettexture('balloonLevelColor'),
            'balloonmodel': ba.getmodel('balloonModel'),
            'balloontex': ba.gettexture('balloonTile'),
            'bgtex': ba.gettexture('balloonBG'),
            'bgmodel': ba.getmodel('thePadBG'),
        }
        data['vr_fill_mound_model'] = ba.getmodel('stepRightUpVRFillMound')
        data['vr_fill_mound_tex'] = ba.gettexture('vrFillMound')
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()

        balloonmaterial = ba.Material()
        balloonmaterial.add_actions(
            conditions=(
                'they_have_material', shared.object_material,
            ),
            actions=('modify_node_collision', 'collide', False),
        )

        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.border = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_border'],
            },
        )
        self.balloon = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['balloonmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['balloontex'],
                'materials': [balloonmaterial],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.53, 0.57, 0.5),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.41,0.59,0.8)
        gnode.ambient_color  = (0.88, 0.91, 1.2)
        gnode.vignette_outer = (0.45, 0.5, 0.6)
        gnode.vignette_inner = (0.99, 0.98, 0.98)
        
    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5

class Blockland(ba.Map):
    """Blocky platform in Blockland!"""

    from bastd.mapdata import blockland as defs

    name = 'Blockland'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'whereEaglesDarePreview'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('blocklandLevel'),
            'collide_model': ba.getcollidemodel('blocklandLevelCollide'),
            'wall_model': ba.getcollidemodel('blocklandWall'),
            'slippery_model': ba.getcollidemodel('blocklandSlippery'),
            'tex': ba.gettexture('blocklandLevelColor'),
            'bgtex': ba.gettexture('rampageBGColor'),
            'bgtex2': ba.gettexture('rampageBGColor2'),
            'bgmodel': ba.getmodel('rampageBG'),
            'bgmodel2': ba.getmodel('rampageBG2'),
            'vr_fill_model': ba.getmodel('rampageVRFill'),
            'wall_material': ba.Material(),
        }
        data['wall_material'].add_actions(actions=('modify_part_collision', 'friction', 10))
        return data

    def __init__(self) -> None:
        super().__init__(vr_overlay_offset=(0, 0, 2))
        shared = SharedObjects.get()
        
        slip_material = ba.Material()
        slip_material.add_actions(
            conditions=(
                'they_have_material', shared.object_material,
            ),
            actions=('modify_node_collision', 'collide', False),
        )

        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material]
            })
        self.slippery = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['slippery_model'],
                'materials': [slip_material]
            },
        )
        self.wall = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['wall_model'],
                'materials': [shared.railing_material, self.preloaddata['wall_material']],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex']
            })
        self.bg2 = ba.newnode('terrain',
                              attrs={
                                  'model': self.preloaddata['bgmodel2'],
                                  'lighting': False,
                                  'background': True,
                                  'color_texture': self.preloaddata['bgtex2']
                              })
        ba.newnode('terrain',
                   attrs={
                       'model': self.preloaddata['vr_fill_model'],
                       'lighting': False,
                       'vr_only': True,
                       'background': True,
                       'color_texture': self.preloaddata['bgtex2']
                   })
        gnode = ba.getactivity().globalsnode
        gnode.tint = (1.15, 1.10, 0.82)
        gnode.ambient_color = (1.2, 1.3, 1.0)
        gnode.vignette_outer = (1, 1, 1)
        gnode.vignette_inner = (0.99, 0.99, 0.95)
        
    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5

class Confrontation(ba.Map):
    """Overseer's base - a final battle of good and evil!"""

    from bastd.mapdata import confrontation as defs

    name = 'Confrontation'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'fuseCruiseSea'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'model': ba.getmodel('confrontationLevel'),
            'collide_model': ba.getcollidemodel('confrontationLevelCollide'),
            'wall_model': ba.getcollidemodel('confrontationWall'),
            'collide_slippery': ba.getcollidemodel('confrontationLevelSlippery'),
            'tex': ba.gettexture('confrontationLevelColor'),
            'bgtex': ba.gettexture('balloonBG'),
            'bgmodel': ba.getmodel('thePadBG'),
            'wall_material': ba.Material(),
        }
        data['wall_material'].add_actions(actions=('modify_part_collision', 'friction', 10))
        data['vr_fill_mound_model'] = ba.getmodel('stepRightUpVRFillMound')
        data['vr_fill_mound_tex'] = ba.gettexture('vrFillMound')
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.node = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_model'],
                'model': self.preloaddata['model'],
                'color_texture': self.preloaddata['tex'],
                'materials': [shared.footing_material],
            },
        )
        self.wall = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['wall_model'],
                'materials': [shared.railing_material, self.preloaddata['wall_material']],
            },
        )
        self.slippery = ba.newnode(
            'terrain',
            delegate=self,
            attrs={
                'collide_model': self.preloaddata['collide_slippery'],
            },
        )
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.53, 0.57, 0.5),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.41,0.59,0.64)
        gnode.ambient_color  = (0.88, 0.91, 1.2)
        gnode.vignette_outer = (0.39, 0.42, 0.49)
        gnode.vignette_inner = (0.99, 0.98, 0.98)
        
    def is_point_near_edge(self, point: ba.Vec3, running: bool = False) -> bool:
        box_position = self.defs.boxes['edge_box'][0:3]
        box_scale = self.defs.boxes['edge_box'][6:9]
        xpos = (point.x - box_position[0]) / box_scale[0]
        zpos = (point.z - box_position[2]) / box_scale[2]
        return xpos < -0.5 or xpos > 0.5 or zpos < -0.5 or zpos > 0.5

class BombPoem(ba.Map):
    """ ogo """

    from bastd.mapdata import confrontation as defs

    name = 'Bomb Poem'

    @classmethod
    def get_play_types(cls) -> list[str]:
        """Return valid play types for this map."""
        return []

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'fuseCruiseSea'

    @classmethod
    def on_preload(cls) -> Any:
        data: dict[str, Any] = {
            'bgtex': ba.gettexture('panoramaBG'),
            'bgmodel': ba.getmodel('panoramaBG'),
        }
        data['vr_fill_mound_model'] = ba.getmodel('stepRightUpVRFillMound')
        data['vr_fill_mound_tex'] = ba.gettexture('vrFillMound')
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['bgmodel'],
                'lighting': False,
                'background': True,
                'color_texture': self.preloaddata['bgtex'],
            },
        )
        ba.newnode(
            'terrain',
            attrs={
                'model': self.preloaddata['vr_fill_mound_model'],
                'lighting': False,
                'vr_only': True,
                'color': (0.53, 0.57, 0.5),
                'background': True,
                'color_texture': self.preloaddata['vr_fill_mound_tex'],
            },
        )
        gnode = ba.getactivity().globalsnode
        # Overseer Essence fades
        time_cycle = [
            # Tint
            ['tint', {
                0: (0.54, 0.62, 0.95),
                80: (1.14, 1.1, 1.0),
            }],
            # Ambient
            ['ambient_color', {
                0: (1.2, 1.4, 3.9),
                80: (1.06, 1.04, 1.03),
            }],
            # Vignette OUT
            ['vignette_outer', {
                0: (0.62, 0.75, 0.8),
                80: (0.45, 0.55, 0.54),
            }],
            # Vignette IN
            ['vignette_inner', {
                0: (0.9, 0.94, 1),
                80: (0.99, 0.98, 0.98),
            }],
        ]

        self._time_clocks = []

        for x in time_cycle: self._time_clocks.append(ba.animate_array(gnode, x[0], 3, x[1]))