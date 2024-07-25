# Released under the MIT License. See LICENSE for details.
#
"""Defines the spaz actor."""
# pylint: disable=too-many-lines

from __future__ import annotations

import random
from typing import TYPE_CHECKING

import ba
from bastd.actor import bomb as stdbomb
from bastd.actor.powerupbox import PowerupBoxFactory
from bastd.actor.spazfactory import SpazFactory
from bastd.gameutils import SharedObjects
from bastd.actor.popuptext import PowerupPopup, PopupText

if TYPE_CHECKING:
    from typing import Any, Sequence, Callable

POWERUP_WEAR_OFF_TIME = 20000
BASE_PUNCH_COOLDOWN = 600
BOXING_PUNCH_COOLDOWN = 850
FLYING_PUNCH_COOLDOWN = 1300
VITAL_PUNCH_COOLDOWN = 150


class PickupMessage:
    """We wanna pick something up."""


class PunchHitMessage:
    """Message saying an object was hit."""


class CurseExplodeMessage:
    """We are cursed and should blow up now."""


class BombDiedMessage:
    """A bomb has died and thus can be recycled."""

class ToxicMessage:
    """We're toxic (is that a public parties reference?!?!?!?)."""

class HealthyMessage:
    """We're not toxic (not a public parties reference)."""

class VitalMessage:
    """We're vital."""

class UnvitalMessage:
    """We stop being vital."""
    
class Spaz(ba.Actor):
    """
    Base class for various Spazzes.

    Category: **Gameplay Classes**

    A Spaz is the standard little humanoid character in the game.
    It can be controlled by a player or by AI, and can have
    various different appearances.  The name 'Spaz' is not to be
    confused with the 'Spaz' character in the game, which is just
    one of the skins available for instances of this class.
    """

    # pylint: disable=too-many-public-methods
    # pylint: disable=too-many-locals

    node: ba.Node
    """The 'spaz' ba.Node."""

    points_mult = 1
    curse_time: float | None = 8.0
    impact_scale = 1.0
    hitpoints = 1000
    default_bomb_count = 1
    default_bomb_type = 'normal'
    default_boxing_gloves = False
    default_flying_gloves = False
    default_shields = False

    can_freeze = True
    can_pickup = True 
    can_be_poisoned = True

    def __init__(
        self,
        color: Sequence[float] = (1.0, 1.0, 1.0),
        highlight: Sequence[float] = (0.5, 0.5, 0.5),
        character: str = 'Mel',
        source_player: ba.Player | None = None,
        start_invincible: bool = True,
        can_accept_powerups: bool = True,
        powerups_expire: bool = False,
        demo_mode: bool = False,
    ):
        """Create a spaz with the requested color, character, etc."""
        # pylint: disable=too-many-statements

        super().__init__()
        shared = SharedObjects.get()
        activity = self.activity

        factory = SpazFactory.get()

        # We need to behave slightly different in the tutorial.
        self._demo_mode = demo_mode

        self.play_big_death_sound = False

        # Scales how much impacts affect us (most damage calcs)
        self.impact_scale = self.impact_scale
        self.impact_scale *= 1.0

        self.source_player = source_player
        self._dead = False
        self.footing = False
        if self._demo_mode:  # Preserve old behavior
            self._punch_power_scale = 1.3
        else:
            self._punch_power_scale = factory.punch_power_scale
        self.fly = ba.getactivity().globalsnode.happy_thoughts_mode
        if isinstance(activity, ba.GameActivity):
            self._hockey = activity.map.is_hockey
        else:
            self._hockey = False
        self._punched_nodes: set[ba.Node] = set()
        self._cursed = False
        self._toxic_timer = None
        self._vital_scorch_timer = None
        self._is_toxic = False
        self._is_vital = False
        self._vital_timer = None
        self._boost_timer = None
        self._boosted = False
        self._vital_light: ba.Node | None = None
        self.glove_node: ba.Node | None = None
        self._connected_to_player: ba.Player | None = None
        materials = [
            factory.spaz_material,
            shared.object_material,
            shared.player_material,
        ]
        
        roller_materials = [factory.roller_material, shared.player_material]
        extras_material = []

        if can_accept_powerups:
            pam = PowerupBoxFactory.get().powerup_accept_material
            materials.append(pam)
            roller_materials.append(pam)
            extras_material.append(pam)

        media = factory.get_media(character)
        punchmats = (factory.punch_material, shared.attack_material)
        pickupmats = (factory.pickup_material, shared.pickup_material)
        self.node: ba.Node = ba.newnode(
            type='spaz',
            delegate=self,
            attrs={
                'color': color,
                'behavior_version': 0 if demo_mode else 1,
                'demo_mode': demo_mode,
                'highlight': highlight,
                'jump_sounds': media['jump_sounds'],
                'attack_sounds': media['attack_sounds'],
                'impact_sounds': media['impact_sounds'],
                'death_sounds': [factory.delin_sound] if random.randint(0, 75) == 0 else media['death_sounds'],
                'pickup_sounds': media['pickup_sounds'],
                'fall_sounds': media['fall_sounds'],
                'color_texture': media['color_texture'],
                'color_mask_texture': media['color_mask_texture'],
                'head_model': media['head_model'],
                'torso_model': media['torso_model'],
                'pelvis_model': media['pelvis_model'],
                'upper_arm_model': media['upper_arm_model'],
                'forearm_model': media['forearm_model'],
                'hand_model': media['hand_model'],
                'upper_leg_model': media['upper_leg_model'],
                'lower_leg_model': media['lower_leg_model'],
                'toes_model': media['toes_model'],
                'style': factory.get_style(character),
                'fly': self.fly,
                'hockey': self._hockey,
                'materials': materials,
                'roller_materials': roller_materials,
                'extras_material': extras_material,
                'punch_materials': punchmats,
                'pickup_materials': pickupmats,
                'invincible': start_invincible,
                'source_player': source_player,
            },
        )
        self.shield: ba.Node | None = None
        self.character = character

        if start_invincible:

            def _safesetattr(node: ba.Node | None, attr: str, val: Any) -> None:
                if node:
                    setattr(node, attr, val)

            ba.timer(1.0, ba.Call(_safesetattr, self.node, 'invincible', False))
        self.hitpoints = self.hitpoints
        self.hitpoints_max = 1000
        self.shield_hitpoints: int | None = None
        self.shield_hitpoints_max = 600
        self.shield_decay_rate = 0
        self.shield_decay_timer: ba.Timer | None = None
        self._boxing_gloves_wear_off_timer: ba.Timer | None = None
        self._boxing_gloves_wear_off_flash_timer: ba.Timer | None = None
        self._flying_gloves_wear_off_timer: ba.Timer | None = None
        self._bomb_wear_off_timer: ba.Timer | None = None
        self._bomb_wear_off_flash_timer: ba.Timer | None = None
        self._multi_bomb_wear_off_timer: ba.Timer | None = None
        self._multi_bomb_wear_off_flash_timer: ba.Timer | None = None
        self._curse_timer: ba.Timer | None = None
        self.bomb_count = self.default_bomb_count
        self._max_bomb_count = self.default_bomb_count
        self.bomb_type_default = self.default_bomb_type
        self.bomb_type = self.bomb_type_default
        self.dash_count = 0
        self.land_mine_count = 0
        self.lite_mine_count = 0
        self.present_count = 0
        self.flutter_mine_count = 0
        self.glue_mine_count = 0
        self.blast_radius = 2.0
        self.powerups_expire = powerups_expire
        if self._demo_mode:  # Preserve old behavior
            self._punch_cooldown = BASE_PUNCH_COOLDOWN
        else:
            self._punch_cooldown = factory.punch_cooldown
        self._jump_cooldown = 150
        self._pickup_cooldown = 350
        self._bomb_cooldown = 0
        self._has_boxing_gloves = False
        self._has_flying_gloves = False
        if self.default_boxing_gloves:
            self.equip_boxing_gloves()
        if self.default_flying_gloves:
            self.equip_flying_gloves()
        self.last_punch_time_ms = -9999
        self.last_pickup_time_ms = -9999
        self.last_jump_time_ms = -9999
        self.last_run_time_ms = -9999
        self._last_run_value = 0.0
        self.last_bomb_time_ms = -9999
        self._turbo_filter_times: dict[str, int] = {}
        self._turbo_filter_time_bucket = 0
        self._turbo_filter_counts: dict[str, int] = {}
        self.frozen = False
        self.shattered = False
        self._last_hit_time: int | None = None
        self._num_times_hit = 0
        self._bomb_held = False
        self._pColor = self.node.color
        if self.default_shields:
            self.equip_shields()
        self._dropped_bomb_callbacks: list[Callable[[Spaz, ba.Actor], Any]] = []

        self._score_text: ba.Node | None = None
        self._score_text_hide_timer: ba.Timer | None = None
        self._last_stand_pos: Sequence[float] | None = None
        
        # Deprecated stuff.. should make these into lists.
        self.punch_callback: Callable[[Spaz], Any] | None = None
        self.pick_up_powerup_callback: Callable[[Spaz], Any] | None = None

    def exists(self) -> bool:
        return bool(self.node)

    def on_expire(self) -> None:
        super().on_expire()

    def reset_powerup_count(self, exceptions: list = []) -> None:
        """ Sets all powerup "counters" to 0 to prevent overlapping.
            Should be called each time a "counter powerup" is picked up! """
        # NOTE: This code sucks.
        if not 'dash' in exceptions: self.dash_count = 0
        if not 'land_mines' in exceptions: self.land_mine_count = 0
        if not 'lite_mines' in exceptions: self.lite_mine_count = 0
        if not 'present' in exceptions: self.present_count = 0
        if not 'flutter_mines' in exceptions: self.flutter_mine_count = 0
        if not 'glue_mines' in exceptions: self.glue_mine_count = 0
        
        # Release callbacks/refs so we don't wind up with dependency loops.
        self._dropped_bomb_callbacks = []
        self.punch_callback = None
        self.pick_up_powerup_callback = None
        self.node.counter_texture = ba.gettexture('empty')
        self.node.counter_text = ''

    def add_dropped_bomb_callback(
        self, call: Callable[[Spaz, ba.Actor], Any]
    ) -> None:
        """
        Add a call to be run whenever this Spaz drops a bomb.
        The spaz and the newly-dropped bomb are passed as arguments.
        """
        assert not self.expired
        self._dropped_bomb_callbacks.append(call)

    def is_alive(self) -> bool:
        """
        Method override; returns whether ol' spaz is still kickin'.
        """
        return not self._dead

    def _hide_score_text(self) -> None:
        if self._score_text:
            assert isinstance(self._score_text.scale, float)
            ba.animate(
                self._score_text,
                'scale',
                {0.0: self._score_text.scale, 0.2: 0.0},
            )

    def _turbo_filter_add_press(self, source: str) -> None:
        """
        Can pass all button presses through here; if we see an obscene number
        of them in a short time let's shame/pushish this guy for using turbo.
        """
        t_ms = ba.time(
            timetype=ba.TimeType.BASE, timeformat=ba.TimeFormat.MILLISECONDS
        )
        assert isinstance(t_ms, int)
        t_bucket = int(t_ms / 1000)
        if t_bucket == self._turbo_filter_time_bucket:
            # Add only once per timestep (filter out buttons triggering
            # multiple actions).
            if t_ms != self._turbo_filter_times.get(source, 0):
                self._turbo_filter_counts[source] = (
                    self._turbo_filter_counts.get(source, 0) + 1
                )
                self._turbo_filter_times[source] = t_ms
                # (uncomment to debug; prints what this count is at)
                # ba.screenmessage( str(source) + " "
                #                   + str(self._turbo_filter_counts[source]))
                if self._turbo_filter_counts[source] == 15:
                    # Knock 'em out.  That'll learn 'em.
                    assert self.node
                    self.node.handlemessage('knockout', 500.0)

        else:
            self._turbo_filter_times = {}
            self._turbo_filter_time_bucket = t_bucket
            self._turbo_filter_counts = {source: 1}

    def set_score_text(
        self,
        text: str | ba.Lstr,
        color: Sequence[float] = (1.0, 1.0, 0.4),
        flash: bool = False,
    ) -> None:
        """
        Utility func to show a message momentarily over our spaz that follows
        him around; Handy for score updates and things.
        """
        color_fin = ba.safecolor(color)[:3]
        if not self.node:
            return
        if not self._score_text:
            start_scale = 0.0
            mnode = ba.newnode(
                'math',
                owner=self.node,
                attrs={'input1': (0, 1.4, 0), 'operation': 'add'},
            )
            self.node.connectattr('torso_position', mnode, 'input2')
            self._score_text = ba.newnode(
                'text',
                owner=self.node,
                attrs={
                    'text': text,
                    'in_world': True,
                    'shadow': 1.0,
                    'flatness': 1.0,
                    'color': color_fin,
                    'scale': 0.02,
                    'h_align': 'center',
                },
            )
            mnode.connectattr('output', self._score_text, 'position')
        else:
            self._score_text.color = color_fin
            assert isinstance(self._score_text.scale, float)
            start_scale = self._score_text.scale
            self._score_text.text = text
        if flash:
            combine = ba.newnode(
                'combine', owner=self._score_text, attrs={'size': 3}
            )
            scl = 1.8
            offs = 0.5
            tval = 0.300
            for i in range(3):
                cl1 = offs + scl * color_fin[i]
                cl2 = color_fin[i]
                ba.animate(
                    combine,
                    'input' + str(i),
                    {0.5 * tval: cl2, 0.75 * tval: cl1, 1.0 * tval: cl2},
                )
            combine.connectattr('output', self._score_text, 'color')

        ba.animate(self._score_text, 'scale', {0.0: start_scale, 0.2: 0.02})
        self._score_text_hide_timer = ba.Timer(
            1.0, ba.WeakCall(self._hide_score_text)
        )

    def on_jump_press(self) -> None:
        """
        Called to 'press jump' on this spaz;
        used by player or AI connections.
        """
        if not self.node:
            return
        t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
        assert isinstance(t_ms, int)
        # Dashing ignores jump cooldown
        self.on_jump_dash()
        if t_ms - self.last_jump_time_ms >= self._jump_cooldown:
            self.node.jump_pressed = True
            self.last_jump_time_ms = t_ms
        self._turbo_filter_add_press('jump')
        
        
    def on_jump_dash(self):
        """ Routine for dashing. """
        if self.dash_count > 0:
            if self.node.exists() and not self.frozen and not self.shattered and self.is_alive():
                self.set_dash_count(self.dash_count - 1)
                xforce = 55
                yforce = 2
                for _ in range(50):
                    v = self.node.velocity
                    self.node.handlemessage('impulse', self.node.position[0], self.node.position[1], self.node.position[2],
                                            0, 25, 0,
                                            yforce, 0.05, 0, 0,
                                            0, 20*400, 0)
                    
                    self.node.handlemessage('impulse', self.node.position[0], self.node.position[1], self.node.position[2],
                                            0, 25, 0,
                                            xforce, 0.05, 0, 0,
                                            v[0]*15*2, 0, v[2]*15*2)
                def sparkies():
                            if self.node.exists():
                                ba.emitfx(position=self.node.position,
                                    chunk_type='sweat',
                                    count=5,
                                    scale=1,
                                    spread=0.6)
                                ba.emitfx(position=self.node.position,
                                    chunk_type='spark',
                                    count=5,
                                    scale=1.0,
                                    spread=0.1)
                ba.timer(0.01,ba.Call(sparkies))
                ba.timer(0.1,ba.Call(sparkies))
                ba.timer(0.2,ba.Call(sparkies))
                ba.playsound(SpazFactory.get().dash_sound, position=self.node.position)
                self.dash_light = ba.newnode('light',
                          owner=self.node,
                          attrs={'position':self.node.position,
                                  'radius':0.0,
                                  'intensity':0.0,
                                  'color': (1, 0.5, 0),
                                  'volume_intensity_scale': 1.0}) 
                self.node.connectattr('position',self.dash_light,'position')
                ba.animate(self.dash_light,'intensity',{0: 0.75, 1: 0.0},loop=False)
                ba.animate(self.dash_light,'radius',{0: 0.2, 1: 0.0},loop=False)

    def on_jump_release(self) -> None:
        """
        Called to 'release jump' on this spaz;
        used by player or AI connections.
        """
        if not self.node:
            return
        self.node.jump_pressed = False

    def on_pickup_press(self) -> None:
        """
        Called to 'press pick-up' on this spaz;
        used by player or AI connections.
        """
        if not self.node:
            return
        t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
        assert isinstance(t_ms, int)
        if t_ms - self.last_pickup_time_ms >= self._pickup_cooldown:
            self.node.pickup_pressed = True
            self.last_pickup_time_ms = t_ms
        self._turbo_filter_add_press('pickup')

    def on_pickup_release(self) -> None:
        """
        Called to 'release pick-up' on this spaz;
        used by player or AI connections.
        """
        if not self.node:
            return
        self.node.pickup_pressed = False

    def on_hold_position_press(self) -> None:
        """
        Called to 'press hold-position' on this spaz;
        used for player or AI connections.
        """
        if not self.node:
            return
        self.node.hold_position_pressed = True
        self._turbo_filter_add_press('holdposition')

    def on_hold_position_release(self) -> None:
        """
        Called to 'release hold-position' on this spaz;
        used for player or AI connections.
        """
        if not self.node:
            return
        self.node.hold_position_pressed = False

    def on_punch_press(self) -> None:
        """
        Called to 'press punch' on this spaz;
        used for player or AI connections.
        """
        if not self.node or self.frozen or self.node.knockout > 0.0:
            return
        t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
        assert isinstance(t_ms, int)
        if t_ms - self.last_punch_time_ms >= self._punch_cooldown:
            if self.punch_callback is not None:
                self.punch_callback(self)
            self._punched_nodes = set()  # Reset this.
            self.last_punch_time_ms = t_ms
            self.node.punch_pressed = True
            if not self.node.hold_node:
                if self._has_boxing_gloves == False:
                    ba.timer(
                        0.1,
                        ba.WeakCall(
                            self._safe_play_sound,
                            SpazFactory.get().swish_sound,
                            0.8,
                        ),
                    )
                else:
                    ba.timer(
                        0.1,
                        ba.WeakCall(
                            self._safe_play_sound,
                            SpazFactory.get().swish_boxing_sound,
                            0.53,
                        ),
                    )
            if self._has_flying_gloves == True:
                self.shoot_glove()
                ba.timer(
                        0.1,
                        ba.WeakCall(
                            self._safe_play_sound,
                            SpazFactory.get().swish_flying_sound,
                            0.53,
                        ),
                    )
            
        self._turbo_filter_add_press('punch')

    def _safe_play_sound(self, sound: ba.Sound, volume: float) -> None:
        """Plays a sound at our position if we exist."""
        if self.node:
            ba.playsound(sound, volume, self.node.position)

    def on_punch_release(self) -> None:
        """
        Called to 'release punch' on this spaz;
        used for player or AI connections.
        """
        if not self.node:
            return
        self.node.punch_pressed = False

    def on_bomb_press(self) -> None:
        """
        Called to 'press bomb' on this spaz;
        used for player or AI connections.
        """
        if not self.node:
            return

        if self._dead or self.frozen:
            return
        if self.node.knockout > 0.0:
            return
        t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
        assert isinstance(t_ms, int)
        if t_ms - self.last_bomb_time_ms >= self._bomb_cooldown:
            self.last_bomb_time_ms = t_ms
            self.node.bomb_pressed = True
            if not self.node.hold_node:
                self.drop_bomb()
        self._turbo_filter_add_press('bomb')

    def on_bomb_release(self) -> None:
        """
        Called to 'release bomb' on this spaz;
        used for player or AI connections.
        """
        if not self.node:
            return
        self.node.bomb_pressed = False

    def on_run(self, value: float) -> None:
        """
        Called to 'press run' on this spaz;
        used for player or AI connections.
        """
        if not self.node:
            return

        t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
        assert isinstance(t_ms, int)
        self.last_run_time_ms = t_ms
        self.node.run = value

        # filtering these events would be tough since its an analog
        # value, but lets still pass full 0-to-1 presses along to
        # the turbo filter to punish players if it looks like they're turbo-ing
        if self._last_run_value < 0.01 and value > 0.99:
            self._turbo_filter_add_press('run')

        self._last_run_value = value

    def on_fly_press(self) -> None:
        """
        Called to 'press fly' on this spaz;
        used for player or AI connections.
        """
        if not self.node:
            return
        # not adding a cooldown time here for now; slightly worried
        # input events get clustered up during net-games and we'd wind up
        # killing a lot and making it hard to fly.. should look into this.
        self.node.fly_pressed = True
        self._turbo_filter_add_press('fly')

    def on_fly_release(self) -> None:
        """
        Called to 'release fly' on this spaz;
        used for player or AI connections.
        """
        if not self.node:
            return
        self.node.fly_pressed = False

    def on_move(self, x: float, y: float) -> None:
        """
        Called to set the joystick amount for this spaz;
        used for player or AI connections.
        """
        if not self.node:
            return
        self.node.handlemessage('move', x, y)

    def on_move_up_down(self, value: float) -> None:
        """
        Called to set the up/down joystick amount on this spaz;
        used for player or AI connections.
        value will be between -32768 to 32767
        WARNING: deprecated; use on_move instead.
        """
        if not self.node:
            return
        self.node.move_up_down = value

    def on_move_left_right(self, value: float) -> None:
        """
        Called to set the left/right joystick amount on this spaz;
        used for player or AI connections.
        value will be between -32768 to 32767
        WARNING: deprecated; use on_move instead.
        """
        if not self.node:
            return
        self.node.move_left_right = value

    def on_punched(self, damage: int) -> None:
        """Called when this spaz gets punched."""

    def get_death_points(self, how: ba.DeathType) -> tuple[int, int]:
        """Get the points awarded for killing this spaz."""
        del how  # Unused.
        num_hits = float(max(1, self._num_times_hit))

        # Base points is simply 10 for 1-hit-kills and 5 otherwise.
        importance = 2 if num_hits < 2 else 1
        return (10 if num_hits < 2 else 5) * self.points_mult, importance

    def vital(self, vitamin:bool = False):
        self._is_vital = True
        self._punch_cooldown = VITAL_PUNCH_COOLDOWN
        self.node.hurt = 0
        self._last_hit_time = None
        self._num_times_hit = 0
    
    def vital_scorch(self):
        if self.node.exists():
            self._vital_scorch = ba.newnode(
                        'scorch',
                        attrs={
                            'position': self.node.position,
                            'big': True,
                            'color': (0.88, 1, 0.0)})
            ba.animate(self._vital_scorch, 'size', {0: 0.4, 1.5: 0})
            ba.timer(1.5, self._vital_scorch.delete)
        
    def unvital(self):
        self._is_vital = False
        self._vital_timer = None
        self._vital_scorch_timer = None
        if self._has_boxing_gloves:
            self._punch_cooldown = BOXING_PUNCH_COOLDOWN
        elif self._has_flying_gloves:
            self._punch_cooldown = 1000
        else:
            self._punch_cooldown = BASE_PUNCH_COOLDOWN

    def poisoned(self):
            if self.is_alive() and self.shield is None:
                if self._is_toxic:
                    self.handlemessage(
                ba.HitMessage(
                pos=self.node.position,
                force_direction=self.node.velocity,
            ))
                    self.hitpoints -= 20
                    ba.animate_array(self.node,'color',3,{0:(0.65,1,0.2),0.5:self.node.color,1:(0.06,0.32,0.14)})
                    ba.emitfx(
                    position=self.node.position,
                    velocity=self.node.velocity,
                    count=10 if not ba.app.config.get("BSE: Reduced Particles", False) else 5,
                    spread=0.25,
                    scale=0.45,
                    chunk_type='slime',
                );
                    self.impact_scale = 1.35
                    ba.playsound(ba.getsound('toxicAcid'), position=self.node.position)
                    if self.hitpoints <= 0:
                        self.handlemessage(ba.DieMessage())
            if self.is_alive() and self.shield:
                self.node.color = self._pColor
                self._toxic_timer = None
                self._is_toxic = False
                self.impact_scale = 1.0
                
    def curse(self) -> None:
        """
        Give this poor spaz a curse;
        he will explode in 8 seconds.
        """
        if not self._cursed:
            factory = SpazFactory.get()
            self._cursed = True

            # Add the curse material.
            for attr in ['materials', 'roller_materials']:
                materials = getattr(self.node, attr)
                if factory.curse_material not in materials:
                    setattr(
                        self.node, attr, materials + (factory.curse_material,)
                    )

            # None specifies no time limit
            assert self.node
            if self.curse_time is None:
                self.node.curse_death_time = -1
            else:
                # Note: curse-death-time takes milliseconds.
                tval = ba.time()
                assert isinstance(tval, (float, int))
                self.node.curse_death_time = int(
                    1000.0 * (tval + self.curse_time)
                )
                self._curse_timer = ba.Timer(
                    8.0, ba.WeakCall(self.curse_explode)
                )

    def equip_boxing_gloves(self) -> None:
        """
        Give this spaz some boxing gloves.
        """
        assert self.node
        if self._has_flying_gloves == True:
            self._flying_gloves_wear_off()
            self._flying_gloves_wear_off_timer = None
            self._flying_gloves_wear_off_flash_timer = None
        self.node.boxing_gloves = True
        self._has_boxing_gloves = True
        if self._demo_mode:  # Preserve old behavior.
            self._punch_power_scale = 1.8
            self._punch_cooldown = BOXING_PUNCH_COOLDOWN
        else:
            factory = SpazFactory.get()
            self._punch_power_scale = 1.8
            if self._is_vital == True:
                self._punch_cooldown = VITAL_PUNCH_COOLDOWN
            else: self._punch_cooldown = BOXING_PUNCH_COOLDOWN
    
    def equip_flying_gloves(self) -> None:
        """
        Give this spaz some flying gloves.
        """
        assert self.node
        if self._has_boxing_gloves == True:
            self._gloves_wear_off()
            self.node.boxing_gloves = False
            self._boxing_gloves_wear_off_timer = None
            self._boxing_gloves_wear_off_flash_timer = None
        if self._has_flying_gloves == True:
            self._flying_gloves_wear_off_flash_timer = None
            if self.glove_node:
                ba.animate(self.glove_node, 'model_scale', {
                    0: 0,
                    0.2: 1.4,
                    0.4: 1,
                })
            
        self._has_flying_gloves = True
        factory = SpazFactory.get()
        shared = SharedObjects.get()
        if self._is_vital == True:
            self._punch_cooldown = VITAL_PUNCH_COOLDOWN
        else:
            self._punch_cooldown = FLYING_PUNCH_COOLDOWN
        self.fly_glove_model = ba.getmodel('boxingGlove')
        self.fly_glove_tex = ba.gettexture('boxingGlovesColor')
        materials = [factory.glove_material]
        if not self.glove_node:
            self.glove_node = ba.newnode(
                'prop',
                owner=self.node,
                attrs={
                    'model': ba.getmodel('flyingGlovesModel'),
                    'light_model': ba.getmodel('flyingGlovesModel'),
                    'body': 'sphere',
                    'body_scale': 0.1,
                    'shadow_size': 0.44,
                    'color_texture': ba.gettexture('flyingGlovesColor'),
                    'reflection': 'soft',
                    'reflection_scale': [0.5],
                    'materials': materials,
                    'gravity_scale': 0.2,
                })
            ba.animate(self.glove_node, 'model_scale', {
                0: 0,
                0.2: 1.4,
                0.4: 1,
            })
    
    
            if self.node.exists():
                # Math node for offset
                math = ba.newnode(
                    'math',
                    owner=self.node,
                    attrs={
                        'input1': (0.5, 1.25, 0),
                        'operation': 'add',
                    },
                )
                self.node.connectattr(
                    'torso_position', math, 'input2'
                )
                math.connectattr('output', self.glove_node, 'position')
    
    def shoot_glove(self):
        import math
        from bastd.actor.bomb import Bomb
        p_center = self.node.position_center
        p_forw = self.node.position_forward
        angle = 180 if p_forw[0]-p_center[0] > 0 else 0
        pos = (p_center[0]+math.sin(angle)*0.1,p_center[1],p_center[2]+math.cos(angle)*0.1)
        cen = self.node.position_center
        frw = self.node.position_forward
        direction = [cen[0]-frw[0],frw[1]-cen[1],cen[2]-frw[2]]
        direction[1] *= .03 
        vel = [v * 20 for v in direction]
        glove = Bomb(position=pos,
                velocity=vel,
                bomb_type='flying_glove',
                source_player=self.source_player).autoretain()
        
    def equip_shields(self, decay: bool = False) -> None:
        """
        Give this spaz a nice energy shield.
        """

        if not self.node:
            ba.print_error('Can\'t equip shields; no node.')
            return

        factory = SpazFactory.get()
        if self.shield is None:
        
            neon_power = 1.0
            shield_color = (max(1.0, self.node.color[0] * 2),
                            max(1.0,self.node.color[1] * 2),
                            max(1.0,self.node.color[2] * 2))
            
            # Tone down neon colors
            if (self.node.color[0] + self.node.color[1] + self.node.color[2]) > 3.0:
                neon_power = max(self.node.color[0], self.node.color[1], self.node.color[2])
                
        
            self.shield = ba.newnode(
                'shield',
                owner=self.node,
                attrs={'color': (shield_color[0] / neon_power,
                                 shield_color[1] / neon_power,
                                 shield_color[2] / neon_power),
                       'radius': 1.15},
            )
            self.node.connectattr('position_center', self.shield, 'position')
        self.shield_hitpoints = self.shield_hitpoints_max = 575
        self.shield_decay_rate = factory.shield_decay_rate if decay else 0
        self.shield.hurt = 0
        ba.playsound(factory.shield_up_sound, 1.0, position=self.node.position)

        if self.shield_decay_rate > 0:
            self.shield_decay_timer = ba.Timer(
                0.5, ba.WeakCall(self.shield_decay), repeat=True
            )
            # So user can see the decay.
            self.shield.always_show_health_bar = True

    def shield_decay(self) -> None:
        """Called repeatedly to decay shield HP over time."""
        if self.shield:
            assert self.shield_hitpoints is not None
            self.shield_hitpoints = max(
                0, self.shield_hitpoints - self.shield_decay_rate
            )
            assert self.shield_hitpoints is not None
            self.shield.hurt = (
                1.0 - float(self.shield_hitpoints) / self.shield_hitpoints_max
            )
            if self.shield_hitpoints <= 0:
                self.shield.delete()
                self.shield = None
                self.shield_decay_timer = None
                assert self.node
                ba.playsound(
                    SpazFactory.get().shield_down_sound,
                    1.0,
                    position=self.node.position,
                )
        else:
            self.shield_decay_timer = None
        
    def handlemessage(self, msg: Any) -> Any:
        # pylint: disable=too-many-return-statements
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-branches
        assert not self.expired

        if isinstance(msg, ba.PickedUpMessage):
            if self.node:
                self.node.handlemessage('hurt_sound')
                self.node.handlemessage('picked_up')

            # This counts as a hit.
            self._num_times_hit += 1

        elif isinstance(msg, ba.ShouldShatterMessage):
            # Eww; seems we have to do this in a timer or it wont work right.
            # (since we're getting called from within update() perhaps?..)
            # NOTE: should test to see if that's still the case.
            ba.timer(0.001, ba.WeakCall(self.shatter))

        elif isinstance(msg, ba.ImpactDamageMessage):
            # Eww; seems we have to do this in a timer or it wont work right.
            # (since we're getting called from within update() perhaps?..)
            ba.timer(0.001, ba.WeakCall(self._hit_self, msg.intensity))
        
        elif isinstance(msg, ba.JumpyMessage):
            xforce = 15
            yforce = 70
            for x in range(15):
                v = self.node.velocity
                self.node.handlemessage('impulse', self.node.position[0], self.node.position[1], self.node.position[2],
                                        0, 25, 0,
                                        yforce, 0.05, 0, 0,
                                        0, 20*400, 0)
                
                self.node.handlemessage('impulse', self.node.position[0], self.node.position[1], self.node.position[2],
                                        0, 25, 0,
                                        xforce, 0.05, 0, 0,
                                        v[0]*15*2, 0, v[2]*15*2)
        
        elif isinstance(msg, ba.SlingMessage):
            xforce = 120
            yforce = 30
            for x in range(50):
                v = self.node.velocity
                self.node.handlemessage('impulse', self.node.position[0], self.node.position[1], self.node.position[2],
                                        0, 25, 0,
                                        yforce, 0.05, 0, 0,
                                        0, 20*400, 0)
                
                self.node.handlemessage('impulse', self.node.position[0], self.node.position[1], self.node.position[2],
                                        0, 25, 0,
                                        xforce, 0.05, 0, 0,
                                        v[0]*15*2, 0, v[2]*15*2)
        
        elif isinstance(msg, ba.PowerupMessage):
            if self._dead or not self.node:
                return True
            if self.pick_up_powerup_callback is not None:
                self.pick_up_powerup_callback(self)
            if msg.poweruptype == 'triple_bombs':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupBombNameText'),
                                 position=self.node.position,
                                 color=(1, 0.88, 0),
                                 scale=1.4,
                                 ).autoretain()
                tex = PowerupBoxFactory.get().tex_bomb
                self._flash_billboard(tex)
                self.set_bomb_count(3)
                if self.powerups_expire:
                    self.node.mini_billboard_1_texture = tex
                    t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_1_start_time = t_ms
                    self.node.mini_billboard_1_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._multi_bomb_wear_off_flash_timer = ba.Timer(
                        (POWERUP_WEAR_OFF_TIME - 2000),
                        ba.WeakCall(self._multi_bomb_wear_off_flash),
                        timeformat=ba.TimeFormat.MILLISECONDS,
                    )
                    self._multi_bomb_wear_off_timer = ba.Timer(
                        POWERUP_WEAR_OFF_TIME,
                        ba.WeakCall(self._multi_bomb_wear_off),
                        timeformat=ba.TimeFormat.MILLISECONDS,
                    )

            elif msg.poweruptype in ['land_mines', 'dash', 'lite_mines',
                                     'present', 'flutter_mines', 'glue_mines']:
                ### NOTE:
                # Next time you add a "counted powerup" (AKA. any powerup with a limited amount of uses), add it
                # to the "in []" list and to the "reset_powerup_count" function so everything loads and resets properly.
                exceptions = msg.poweruptype
                self.reset_powerup_count(exceptions)

                if msg.poweruptype == 'land_mines':
                    self._r = 'helpWindow'
                    if msg.showtooltip:
                        PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupLandMinesNameText'),
                                     position=self.node.position,
                                     color=(0.2, 0.75, 0.53),
                                     scale=1.4,
                                     ).autoretain()
                    self.set_land_mine_count(min(self.land_mine_count + 3, 3))

                elif msg.poweruptype == 'dash':
                    self._r = 'helpWindow'
                    if msg.showtooltip:
                        PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupDashNameText'),
                                     position=self.node.position,
                                     color=(1, 0.35, 0.35),
                                     scale=1.4,
                                     ).autoretain()
                    self.set_dash_count(min(self.dash_count + 3, 6))

                elif msg.poweruptype == 'lite_mines':
                    self._r = 'helpWindow'
                    if msg.showtooltip:
                        PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupSkyMinesNameText'),
                                     position=self.node.position,
                                     color=(0.2, 0.8, 1),
                                     scale=1.4,
                                     ).autoretain()
                    self.set_lite_mine_count(min(self.lite_mine_count + 4, 4))

                elif msg.poweruptype == 'present':
                    self._r = 'helpWindow'
                    if msg.showtooltip:
                        PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupPresentNameText'),
                                     position=self.node.position,
                                     color=(1, 0.5, 0),
                                     scale=1.4,
                                     ).autoretain()
                    self.set_present_count(min(self.lite_mine_count + 1, 1))

                elif msg.poweruptype == 'flutter_mines':
                    self._r = 'helpWindow'
                    if msg.showtooltip:
                        PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupFlutterMinesNameText'),
                                     position=self.node.position,
                                     color=(1, 0.45, 0.5),
                                     scale=1.4,
                                     ).autoretain()
                    self.set_flutter_mine_count(min(self.flutter_mine_count + 3, 6))

                elif msg.poweruptype == 'glue_mines':
                    self._r = 'helpWindow'
                    if msg.showtooltip:
                        PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupGlueMinesNameText'),
                                     position=self.node.position,
                                     color=(1, 0.8, 0.5),
                                     scale=1.4,
                                     ).autoretain()
                    self.set_glue_mine_count(min(self.glue_mine_count + 1, 2))

            elif msg.poweruptype == 'impact_bombs':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupImpactBombsNameText'),
                                 position=self.node.position,
                                 color=(0.5, 0.5, 0.5),
                                 scale=1.4,
                                 ).autoretain()
                self.bomb_type = 'impact'
                tex = self._get_bomb_type_tex()
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._bomb_wear_off_flash_timer = ba.Timer(
                        POWERUP_WEAR_OFF_TIME - 2000,
                        ba.WeakCall(self._bomb_wear_off_flash),
                        timeformat=ba.TimeFormat.MILLISECONDS,
                    )
                    self._bomb_wear_off_timer = ba.Timer(
                        POWERUP_WEAR_OFF_TIME,
                        ba.WeakCall(self._bomb_wear_off),
                        timeformat=ba.TimeFormat.MILLISECONDS,
                    )
            elif msg.poweruptype == 'sticky_bombs':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupStickyBombsNameText'),
                                 position=self.node.position,
                                 color=(0.2, 1, 0.2),
                                 scale=1.4,
                                 ).autoretain()
                self.bomb_type = 'sticky'
                tex = self._get_bomb_type_tex()
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._bomb_wear_off_flash_timer = ba.Timer(
                        POWERUP_WEAR_OFF_TIME - 2000,
                        ba.WeakCall(self._bomb_wear_off_flash),
                        timeformat=ba.TimeFormat.MILLISECONDS,
                    )
                    self._bomb_wear_off_timer = ba.Timer(
                        POWERUP_WEAR_OFF_TIME,
                        ba.WeakCall(self._bomb_wear_off),
                        timeformat=ba.TimeFormat.MILLISECONDS,)
            elif msg.poweruptype == 'cluster_bombs':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupClusterBombsNameText'),
                                 position=self.node.position,
                                 color=(1, 0.15, 0.15),
                                 scale=1.4,
                                 ).autoretain()
                self.bomb_type = 'cluster'
                tex = ba.gettexture('powerupClusterBombs')
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME)
                    self._bomb_wear_off_flash_timer = (ba.Timer(
                        POWERUP_WEAR_OFF_TIME - 2000,
                        ba.WeakCall(self._bomb_wear_off_flash),
                        timeformat=ba.TimeFormat.MILLISECONDS))
                     
                    self._bomb_wear_off_timer = (ba.Timer(
                        POWERUP_WEAR_OFF_TIME,
                        ba.WeakCall(self._bomb_wear_off),
                        timeformat=ba.TimeFormat.MILLISECONDS))
                        
            elif msg.poweruptype == 'tacky_bombs':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupTackyBombsNameText'),
                                 position=self.node.position,
                                 color=(0.4, 1, 0.25),
                                 scale=1.4,
                                 ).autoretain()
                self.bomb_type = 'tacky'
                tex = ba.gettexture('powerupTackyBombs')
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME)
                    self._bomb_wear_off_flash_timer = (ba.Timer(
                        POWERUP_WEAR_OFF_TIME - 2000,
                        ba.WeakCall(self._bomb_wear_off_flash),
                        timeformat=ba.TimeFormat.MILLISECONDS))
                     
                    self._bomb_wear_off_timer = (ba.Timer(
                        POWERUP_WEAR_OFF_TIME,
                        ba.WeakCall(self._bomb_wear_off),
                        timeformat=ba.TimeFormat.MILLISECONDS))
                        
            elif msg.poweruptype == 'clouder_bombs':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupClouderNameText'),
                                 position=self.node.position,
                                 color=(1, 0.3, 0.5),
                                 scale=1.4,
                                 ).autoretain()
                self.bomb_type = 'clouder'
                tex = ba.gettexture('powerupClouder')
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME)
                    self._bomb_wear_off_flash_timer = (ba.Timer(
                        POWERUP_WEAR_OFF_TIME - 2000,
                        ba.WeakCall(self._bomb_wear_off_flash),
                        timeformat=ba.TimeFormat.MILLISECONDS))
                     
                    self._bomb_wear_off_timer = (ba.Timer(
                        POWERUP_WEAR_OFF_TIME,
                        ba.WeakCall(self._bomb_wear_off),
                        timeformat=ba.TimeFormat.MILLISECONDS))
            
            elif msg.poweruptype == 'steampunk_bombs':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupSteampunkNameText'),
                                 position=self.node.position,
                                 color=(0.55, 0.33, 0.25),
                                 scale=1.4,
                                 ).autoretain()
                self.bomb_type = 'steampunk'
                tex = ba.gettexture('powerupSteampunk')
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME)
                    self._bomb_wear_off_flash_timer = (ba.Timer(
                        POWERUP_WEAR_OFF_TIME - 2000,
                        ba.WeakCall(self._bomb_wear_off_flash),
                        timeformat=ba.TimeFormat.MILLISECONDS))
                     
                    self._bomb_wear_off_timer = (ba.Timer(
                        POWERUP_WEAR_OFF_TIME,
                        ba.WeakCall(self._bomb_wear_off),
                        timeformat=ba.TimeFormat.MILLISECONDS))
            
            elif msg.poweruptype == 'toxic_bombs':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupToxicBombsNameText'),
                                 position=self.node.position,
                                 color=(0.49, 0.87, 0.45),
                                 scale=1.4,
                                 ).autoretain()
                self.bomb_type = 'toxic'
                tex = ba.gettexture('powerupToxicBombs')
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME)
                    self._bomb_wear_off_flash_timer = (ba.Timer(
                        POWERUP_WEAR_OFF_TIME - 2000,
                        ba.WeakCall(self._bomb_wear_off_flash),
                        timeformat=ba.TimeFormat.MILLISECONDS))
                     
                    self._bomb_wear_off_timer = (ba.Timer(
                        POWERUP_WEAR_OFF_TIME,
                        ba.WeakCall(self._bomb_wear_off),
                        timeformat=ba.TimeFormat.MILLISECONDS))
            
            elif msg.poweruptype == 'vital_bombs':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupVitalBombsNameText'),
                                 position=self.node.position,
                                 color=(0.9, 1, 0.25),
                                 scale=1.4,
                                 ).autoretain()
                self.bomb_type = 'vital'
                tex = ba.gettexture('powerupVitalBombs')
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME)
                    self._bomb_wear_off_flash_timer = (ba.Timer(
                        POWERUP_WEAR_OFF_TIME - 2000,
                        ba.WeakCall(self._bomb_wear_off_flash),
                        timeformat=ba.TimeFormat.MILLISECONDS))
                     
                    self._bomb_wear_off_timer = (ba.Timer(
                        POWERUP_WEAR_OFF_TIME,
                        ba.WeakCall(self._bomb_wear_off),
                        timeformat=ba.TimeFormat.MILLISECONDS))
                        
            elif msg.poweruptype == 'punch':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupPunchNameText'),
                                 position=self.node.position,
                                 color=(1, 0.2, 0.2),
                                 scale=1.4,
                                 ).autoretain()
                tex = PowerupBoxFactory.get().tex_punch
                self._flash_billboard(tex)
                self.equip_boxing_gloves()
                if self.powerups_expire and not self.default_boxing_gloves:
                    self.node.boxing_gloves_flashing = False
                    self.node.mini_billboard_3_texture = tex
                    t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_3_start_time = t_ms
                    self.node.mini_billboard_3_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._boxing_gloves_wear_off_flash_timer = ba.Timer(
                        POWERUP_WEAR_OFF_TIME - 2000,
                        ba.WeakCall(self._gloves_wear_off_flash),
                        timeformat=ba.TimeFormat.MILLISECONDS,
                    )
                    self._boxing_gloves_wear_off_timer = ba.Timer(
                        POWERUP_WEAR_OFF_TIME,
                        ba.WeakCall(self._gloves_wear_off),
                        timeformat=ba.TimeFormat.MILLISECONDS,
                    )
            elif msg.poweruptype == 'fly_punch':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupFlyingPunchNameText'),
                                 position=self.node.position,
                                 color=(0.2, 0.8, 1),
                                 scale=1.4,
                                 ).autoretain()
                tex = ba.gettexture('powerupFlyingPunch')
                self._flash_billboard(tex)
                self.equip_flying_gloves()
                if self.powerups_expire and not self.default_flying_gloves:
                    self.node.mini_billboard_3_texture = tex
                    t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_3_start_time = t_ms
                    self.node.mini_billboard_3_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._flying_gloves_wear_off_flash_timer = ba.Timer(
                        POWERUP_WEAR_OFF_TIME - 2000,
                        ba.WeakCall(self._flying_gloves_wear_off_flash),
                        timeformat=ba.TimeFormat.MILLISECONDS,
                    )
                    self._flying_gloves_wear_off_timer = ba.Timer(
                        POWERUP_WEAR_OFF_TIME,
                        ba.WeakCall(self._flying_gloves_wear_off),
                        timeformat=ba.TimeFormat.MILLISECONDS,
                    )
            elif msg.poweruptype == 'shield':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupShieldNameText'),
                                 position=self.node.position,
                                 color=(0.5, 0.5, 1),
                                 scale=1.4,
                                 ).autoretain()
                factory = SpazFactory.get()

                # Let's allow powerup-equipped shields to lose hp over time.
                self.equip_shields(decay=factory.shield_decay_rate > 0)
            elif msg.poweruptype == 'curse':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.cursedText'),
                                 position=self.node.position,
                                 color=(0.3, 0, 0.45),
                                 scale=1.4,
                                 ).autoretain()
                self.curse()
            elif msg.poweruptype == 'ice_bombs':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=f'explodinary.append.{self._r}.powerupIceBombsNameText'),
                                 position=self.node.position,
                                 color=(0.2, 1, 1),
                                 scale=1.4,
                                 ).autoretain()
                self.bomb_type = 'ice'
                tex = self._get_bomb_type_tex()
                self._flash_billboard(tex)
                if self.powerups_expire:
                    self.node.mini_billboard_2_texture = tex
                    t_ms = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
                    assert isinstance(t_ms, int)
                    self.node.mini_billboard_2_start_time = t_ms
                    self.node.mini_billboard_2_end_time = (
                        t_ms + POWERUP_WEAR_OFF_TIME
                    )
                    self._bomb_wear_off_flash_timer = ba.Timer(
                        POWERUP_WEAR_OFF_TIME - 2000,
                        ba.WeakCall(self._bomb_wear_off_flash),
                        timeformat=ba.TimeFormat.MILLISECONDS,
                    )
                    self._bomb_wear_off_timer = ba.Timer(
                        POWERUP_WEAR_OFF_TIME,
                        ba.WeakCall(self._bomb_wear_off),
                        timeformat=ba.TimeFormat.MILLISECONDS,
                    )
            elif msg.poweruptype == 'health':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=self._r + '.powerupHealthNameText'),
                                 position=self.node.position,
                                 color=(1, 1, 1),
                                 scale=1.4,
                                 ).autoretain()
                if self._cursed:
                    self._cursed = False
                    ba.playsound(
                    SpazFactory.get().curse_heal_sound,
                    0.4,
                    position=self.node.position,
                )

                    # Remove cursed material.
                    factory = SpazFactory.get()
                    for attr in ['materials', 'roller_materials']:
                        materials = getattr(self.node, attr)
                        if factory.curse_material in materials:
                            setattr(
                                self.node,
                                attr,
                                tuple(
                                    m
                                    for m in materials
                                    if m != factory.curse_material
                                ),
                            )
                    self.node.curse_death_time = 0
                if self._is_toxic:
                    self.node.color = self._pColor
                    self._toxic_timer = None
                    self._is_toxic = False
                if self.hitpoints <= self.hitpoints_max:       
                    self.hitpoints = self.hitpoints_max
                else: self.hitpoints += 20
                self._flash_billboard(PowerupBoxFactory.get().tex_health)
                self.node.hurt = 0
                self._last_hit_time = None
                self._num_times_hit = 0

            elif msg.poweruptype == 'vitamin':
                self._r = 'helpWindow'
                if msg.showtooltip:
                    PowerupPopup(ba.Lstr(resource=self._r + '.powerupVitaminNameText'),
                                 position=self.node.position,
                                 color=(0.9, 1, 0.25),
                                 scale=1.4,
                                 ).autoretain()
                self.node.handlemessage(ba.VitaminMessage())
                self._flash_billboard(PowerupBoxFactory.get().tex_vitamin)
                self.node.hurt = 0
                self._last_hit_time = None
                self._num_times_hit = 0

            self.node.handlemessage('flash')
            if msg.sourcenode:
                msg.sourcenode.handlemessage(ba.PowerupAcceptMessage())
            return True

        elif isinstance(msg, ba.FreezeMessage):
            if not self.node:
                return None
            if not self.can_freeze:
                ba.playsound(
                    ba.getsound('hiss'),
                    1.5,
                    position=self.node.position,
                )
                return None
            if self.node.invincible:
                ba.playsound(
                    SpazFactory.get().block_sound,
                    1.0,
                    position=self.node.position,
                )
                return None
            if self.shield:
                return None
            if not self.frozen:
                self.frozen = True
                self.node.frozen = True
                ba.timer(5.0, ba.WeakCall(self.handlemessage, ba.ThawMessage()))
                # Instantly shatter if we're already dead.
                # (otherwise its hard to tell we're dead)
                if self.hitpoints <= 0:
                    self.shatter()
        
        elif isinstance(msg, ba.TNTFreezeMessage):
            if not self.node:
                return None
            if not self.can_freeze:
                ba.playsound(
                    ba.getsound('hiss'),
                    1.5,
                    position=self.node.position,
                )
                return None
            if self.node.invincible:
                ba.playsound(
                    SpazFactory.get().block_sound,
                    1.0,
                    position=self.node.position,
                )
                return None
            if self.shield:
                return None
            if not self.frozen:
                self.frozen = True
                self.node.frozen = True
                ba.timer(6.0, ba.WeakCall(self.handlemessage, ba.ThawMessage()))
                # Instantly shatter if we're already dead.
                # (otherwise its hard to tell we're dead)
                if self.hitpoints <= 0:
                    self.shatter()
                    
        elif isinstance(msg, ba.ThawMessage):
            if self.frozen and not self.shattered and self.node:
                self.frozen = False
                self.node.frozen = False
        
        elif isinstance(msg, ba.VitaminMessage):
            from ba._gameutils import animate
            
            self.vital(True)
            self.hitpoints == self.hitpoints_max
    
            def _safesetattr(node: ba.Node | None, attr: str, val: Any) -> None:
                if node:
                    setattr(node, attr, val)
            ba.timer(0.0, ba.Call(_safesetattr, self.node, 'invincible', True))
            ba.timer(1, ba.Call(_safesetattr, self.node, 'invincible', False))
            
            if self.frozen and not self.shattered and self.node.exists():
                    self.vital()
                    self.frozen = False
                    self.node.frozen = 0
                
            if self._is_toxic and not self.shattered and self.node.exists():
                self.vital()
                self.hitpoints
                self._is_toxic = False
                self.node.color = self._pColor
                
            if self._cursed:
                    self._cursed = False
                    ba.playsound(
                    SpazFactory.get().curse_heal_sound,
                    0.4,
                    position=self.node.position,
                    )
    
                    # Remove cursed material.
                    factory = SpazFactory.get()
                    for attr in ['materials', 'roller_materials']:
                        materials = getattr(self.node, attr)
                        if factory.curse_material in materials:
                            setattr(
                                self.node,
                                attr,
                                tuple(
                                    m
                                    for m in materials
                                    if m != factory.curse_material
                                ),
                            )
                    self.node.curse_death_time = 0
                
            self.unvital_timer = ba.Timer(8.0, ba.WeakCall(self.handlemessage, ba.UnvitalMessage()))
                
        elif isinstance(msg, ba.VitalMessage):
            from ba._gameutils import animate

            sourceplayer = msg.get_source_player(ba.Player)
            
            try: myteam = sourceplayer.team == self.source_player.team
            except AttributeError: myteam = False
            
            ### ENEMY HIT
            if not myteam:
                self.node.handlemessage("hurt_sound")
                self.handlemessage(
                    ba.HitMessage(
                        flat_damage=400.0,
                        pos=msg.pos,
                        force_direction=msg.force_direction,
                        hit_type='impact',
                    )
                )
            ### ALLY HIT
            else:
                self.vital()
                self.hitpoints = self.hitpoints_max
                ba.playsound(
                    SpazFactory.get().vitalup_sound,
                    position=self.node.position,
                )
                
                if self.shield:
                   self.shield_hitpoints = self.shield_hitpoints_max

                def _safesetattr(node: ba.Node | None, attr: str, val: Any) -> None:
                    if node:
                        setattr(node, attr, val)
                ba.timer(0.0, ba.Call(_safesetattr, self.node, 'invincible', True))
                ba.timer(2, ba.Call(_safesetattr, self.node, 'invincible', False))

                if self._cursed:
                        self.vital()
                        self._cursed = False
                        ba.playsound(
                        SpazFactory.get().curse_heal_sound,
                        0.4,
                        position=self.node.position,
                        )

                        # Remove cursed material.
                        factory = SpazFactory.get()
                        for attr in ['materials', 'roller_materials']:
                            materials = getattr(self.node, attr)
                            if factory.curse_material in materials:
                                setattr(
                                    self.node,
                                    attr,
                                    tuple(
                                        m
                                        for m in materials
                                        if m != factory.curse_material
                                    ),
                                )
                        self.node.curse_death_time = 0
                
                if self.frozen and not self.shattered and self.node.exists():
                    self.vital()
                    self.frozen = False
                    self.node.frozen = 0
                
                if self._is_toxic and not self.shattered and self.node.exists():
                    self.vital()
                    self.hitpoints = self.hitpoints_max
                    self._is_toxic = False
                    self.node.color = self._pColor
                
                if self.dash_count > 0:
                    self.set_dash_count(min(self.dash_count + 1, 6))
        
                if not self._vital_light:
                    self._vital_light = ba.newnode(
                        'light',
                        attrs={
                            'position': self.node.position,
                            'volume_intensity_scale': 0.1,
                            'intensity':0.65,
                            'color': (1.0, 1, 0.45),
                            'radius': 0.1,
                        },
                    )
                    animate(self._vital_light, 'intensity', {5: 0.65, 6: 0})
                    animate(self._vital_light, 'radius', {5: 0.1, 6: 0})
                    self.node.connectattr('position', self._vital_light, 'position')
                    
                   
                self._vital_scorch_timer = ba.Timer(0.1, ba.WeakCall(self.vital_scorch), repeat=True)

                self.unvital_timer = ba.Timer(8.0, ba.WeakCall(self.handlemessage, ba.UnvitalMessage()))
        
        elif isinstance(msg, ba.UnvitalMessage):
            if self._vital_light: self._vital_light.delete()
            if not self._is_vital: return
            if self.is_alive():
                self.unvital()
                ba.playsound(
                    SpazFactory.get().vitaldown_sound,
                    position=self.node.position,
                )
                
        elif isinstance(msg, ba.ToxicMessage):
            if self._is_toxic: return
            if not self.can_be_poisoned:
                return None
            self._is_toxic = True
            self._toxic_timer = ba.timer(0.5,ba.Call(self.poisoned),repeat=True)
            ba.timer(10.0, ba.WeakCall(self.handlemessage, ba.HealthyMessage()))
        
        elif isinstance(msg, ba.HealthyMessage):
            if self._is_toxic and not self.shattered and self.node:
                self._toxic_timer = None
                self._is_toxic = False
                self.node.color = self._pColor
                self.impact_scale = 1.0
            
        elif isinstance(msg, ba.HitMessage):
            if not self.node:
                return None
            if self.node.invincible:
                ba.playsound(
                    SpazFactory.get().block_sound,
                    1.0,
                    position=self.node.position,
                )
                return True

            # If we were recently hit, don't count this as another.
            # (so punch flurries and bomb pileups essentially count as 1 hit)
            local_time = ba.time(timeformat=ba.TimeFormat.MILLISECONDS)
            assert isinstance(local_time, int)
            if (
                self._last_hit_time is None
                or local_time - self._last_hit_time > 1000
            ):
                self._num_times_hit += 1
                self._last_hit_time = local_time

            mag = msg.magnitude * self.impact_scale
            velocity_mag = msg.velocity_magnitude * self.impact_scale
            damage_scale = 0.22

            # If they've got a shield, deliver it to that instead.
            if self.shield:
                if msg.flat_damage:
                    damage = msg.flat_damage * self.impact_scale
                if msg.hit_subtype == 'flutter':
                   damage = 0.1
                if msg.hit_subtype == 'little_cluster':
                   damage = 400 * self.impact_scale
                if msg.hit_subtype == 'lite':
                   damage = 400 * self.impact_scale
                   self.node.handlemessage('knockout', 4000.0)
                   npos = self.node.position
                   ba.emitfx(
                       position=(npos[0], npos[1] + 0.9, npos[2]),
                       velocity=self.node.velocity,
                       count=random.randrange(20, 30),
                       scale=0.5,
                       spread=0.3,
                       chunk_type='ice',
                   )
                   ba.playsound(
                    SpazFactory.get().electrip_sound,
                    1,
                    position=self.node.position,)
                   PopupText(
                       'Electripped!',
                       position=self.node.position,
                       color=(0.25, 0.75, 1),
                       scale=1,
                   ).autoretain()
                else:
                    # Hit our spaz with an impulse but tell it to only return
                    # theoretical damage; not apply the impulse.
                    assert msg.force_direction is not None
                    self.node.handlemessage(
                        'impulse',
                        msg.pos[0],
                        msg.pos[1],
                        msg.pos[2],
                        msg.velocity[0],
                        msg.velocity[1],
                        msg.velocity[2],
                        mag,
                        velocity_mag,
                        msg.radius,
                        1,
                        msg.force_direction[0],
                        msg.force_direction[1],
                        msg.force_direction[2],
                    )
                    damage = msg.flat_damage if msg.flat_damage else (damage_scale * self.node.damage)

                assert self.shield_hitpoints is not None
                self.shield_hitpoints -= int(damage)
                self.shield.hurt = (
                    1.0
                    - float(self.shield_hitpoints) / self.shield_hitpoints_max
                )

                # Its a cleaner event if a hit just kills the shield
                # without damaging the player.
                # However, massive damage events should still be able to
                # damage the player. This hopefully gives us a happy medium.
                max_spillover = SpazFactory.get().max_shield_spillover_damage
                if self.shield_hitpoints <= 0:

                    # FIXME: Transition out perhaps?
                    self.shield.delete()
                    self.shield = None
                    ba.playsound(
                        SpazFactory.get().shield_down_sound,
                        1.0,
                        position=self.node.position,
                    )

                    # Emit some cool looking sparks when the shield dies.
                    npos = self.node.position
                    ba.emitfx(
                        position=(npos[0], npos[1] + 0.9, npos[2]),
                        velocity=self.node.velocity,
                        count=random.randrange(20, 30),
                        scale=1.0,
                        spread=0.6,
                        chunk_type='spark',
                    )

                else:
                    ba.playsound(
                        SpazFactory.get().shield_hit_sound,
                        0.5,
                        position=self.node.position,
                    )

                # Emit some cool looking sparks on shield hit.
                assert msg.force_direction is not None
                ba.emitfx(
                    position=msg.pos,
                    velocity=(
                        msg.force_direction[0] * 1.0,
                        msg.force_direction[1] * 1.0,
                        msg.force_direction[2] * 1.0,
                    ),
                    count=min(30, 5 + int(damage * 0.005)),
                    scale=0.5,
                    spread=0.3,
                    chunk_type='spark',
                )

                # If they passed our spillover threshold,
                # pass damage along to spaz.
                if self.shield_hitpoints <= -max_spillover:
                    leftover_damage = -max_spillover - self.shield_hitpoints
                    shield_leftover_ratio = leftover_damage / damage

                    # Scale down the magnitudes applied to spaz accordingly.
                    mag *= shield_leftover_ratio
                    velocity_mag *= shield_leftover_ratio
                else:
                    return True  # Good job shield!
            else:
                shield_leftover_ratio = 1.0

            if msg.flat_damage:
                damage = int(
                    msg.flat_damage * self.impact_scale * shield_leftover_ratio
                )
            else:
                # Hit it with an impulse and get the resulting damage.
                dst = 1; magmult = 1
                if msg.hit_subtype in ['cloudy','flutter']:
                    st = msg.hit_subtype
                    # If we get hit by a clouder/flutter, recalculate the magnitude
                    magmult = 6
                    mag = 2000.0 * ( magmult / 2 ) * self.impact_scale
                    # We need to do some epic math for the flutters to work as intended
                    if st == 'cloudy':
                        spos = self.node.position; bpos = msg.pos; epos = (0,0,0),

                        import math
                        dst = math.sqrt( ( (bpos[0]-spos[0]) * (bpos[0]-spos[0]) ) +
                                         ( (bpos[1]-spos[1]) * (bpos[1]-spos[1]) ) +
                                         ( (bpos[2]-spos[2]) * (bpos[2]-spos[2]) ) ) * ( magmult / 2 * (1 if st == 'cloudy' else 4) )
                        
                        mag *= min(2.8, dst)

                assert msg.force_direction is not None
                self.node.handlemessage(
                    'impulse',
                    msg.pos[0],
                    msg.pos[1],
                    msg.pos[2],
                    msg.velocity[0],
                    msg.velocity[1],
                    msg.velocity[2],
                    mag,
                    velocity_mag,
                    msg.radius,
                    0,
                    msg.force_direction[0] * magmult,
                    msg.force_direction[1] * magmult,
                    msg.force_direction[2] * magmult,
                )

                damage = int(damage_scale * self.node.damage)
            self.node.handlemessage('hurt_sound')

            # Play punch impact sound based on damage if it was a punch.
            if msg.hit_type == 'punch':
                self.on_punched(damage)

                # If damage was significant, lets show it.
                if damage >= 350:
                    assert msg.force_direction is not None
                    ba.show_damage_count(
                        '-' + str(int(damage / 10)) + '%',
                        msg.pos,
                        msg.force_direction,
                        (0.2, 1, 0.2, 1) if self._is_toxic else (1, 0.25, 0.25, 1),
                    )
                    
                # Let's always add in a super-punch sound with boxing
                # gloves just to differentiate them.
                if msg.hit_subtype == 'super_punch':
                    ba.playsound(
                        SpazFactory.get().punch_sound_stronger,
                        1.0,
                        position=self.node.position,
                    )
                if damage > 1000 and msg.hit_subtype == 'super_punch': 
                    sound = SpazFactory.get().punch_sound_ultra
                    ba.playsound(sound, 1.9, position=self.node.position)
                    ba.emitfx(
                    position=msg.pos,
                    chunk_type='spark',
                    velocity=(
                        msg.force_direction[0] * 1.3,
                        msg.force_direction[1] * 1.3 + 5.0,
                        msg.force_direction[2] * 1.3,
                    ),
                    count=15,
                    scale=0.9,
                    spread=0.28,
                    )
                if damage >= 500:
                    sounds = SpazFactory.get().punch_sound_strong
                    sound = sounds[random.randrange(len(sounds))]
                elif damage >= 100:
                    sound = SpazFactory.get().punch_sound
                else:
                    sound = SpazFactory.get().punch_sound_weak
                ba.playsound(sound, 1.0, position=self.node.position)

                # Throw up some chunks.
                assert msg.force_direction is not None
                ba.emitfx(
                    position=msg.pos,
                    velocity=(
                        msg.force_direction[0] * 0.5,
                        msg.force_direction[1] * 0.5,
                        msg.force_direction[2] * 0.5,
                    ),
                    count=min(10, 1 + int(damage * 0.0025)),
                    scale=0.3,
                    spread=0.03,
                )
                if self.node.style == 'cyborg':
                    ba.emitfx(
                    position=msg.pos,
                    chunk_type='spark',
                    velocity=(
                        msg.force_direction[0] * 1.3,
                        msg.force_direction[1] * 1.3 + 5.0,
                        msg.force_direction[2] * 1.3,
                    ),
                    count=min(30, 1 + int(damage * 0.04)) if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                    scale=0.9,
                    spread=0.28,
                )
                    ba.emitfx(
                    position=msg.pos,
                    chunk_type='metal',
                    velocity=(
                        msg.force_direction[0] * 0.6,
                        msg.force_direction[1] * 0.6 + 2,
                        msg.force_direction[2] * 0.6,
                    ),
                    count=min(3, 1 + int(damage * 0.04)),
                    scale=0.7,
                    spread=0.28,
                )
                elif self.character == 'Splash':
                    self._juicehit = ba.newnode(
                                'scorch',
                                attrs={
                                    'position': self.node.position,
                                    'big': True,
                                    'color': self.node.highlight})
                    ba.animate(self._juicehit, 'size', {0: 0, 0.1: 0.5, 1: 0.5, 1.8: 0})
                    ba.timer(1.8, self._juicehit.delete)
                elif self.character in ['Frosty', 'Snow Golem']:
                    ba.emitfx(
                    position=msg.pos,
                    chunk_type='ice',
                    velocity=self.node.velocity,
                    count=min(3, 1 + int(damage * 0.04)),
                    scale=0.6,
                    spread=0.15,
                )
                elif self.character == 'Spazzy Toxicant' or self._is_toxic:
                    ba.emitfx(
                    position=msg.pos,
                    chunk_type='slime',
                    velocity=self.node.velocity,
                    count=5,
                    scale=0.6,
                    spread=0.15,
                )
                else:
                    ba.emitfx(
                        position=msg.pos,
                        chunk_type='sweat',
                        velocity=(
                            msg.force_direction[0] * 1.3,
                            msg.force_direction[1] * 1.3 + 5.0,
                            msg.force_direction[2] * 1.3,
                        ),
                        count=min(30, 1 + int(damage * 0.04)) if not ba.app.config.get("BSE: Reduced Particles", False) else 10,
                        scale=0.9,
                        spread=0.28,
                    )

                # Momentary flash.
                hurtiness = damage * 0.003
                punchpos = (
                    msg.pos[0] + msg.force_direction[0] * 0.02,
                    msg.pos[1] + msg.force_direction[1] * 0.02,
                    msg.pos[2] + msg.force_direction[2] * 0.02,
                )
                flash_color = (1.0, 0.8, 0.4)
                light = ba.newnode(
                    'light',
                    attrs={
                        'position': punchpos,
                        'radius': 0.12 + hurtiness * 0.12,
                        'intensity': 0.3 * (1.0 + 1.0 * hurtiness),
                        'height_attenuated': False,
                        'color': flash_color,
                    },
                )
                ba.timer(0.06, light.delete)

                flash = ba.newnode(
                    'flash',
                    attrs={
                        'position': punchpos,
                        'size': 0.17 + 0.17 * hurtiness,
                        'color': flash_color,
                    },
                )
                ba.timer(0.06, flash.delete)

            if msg.hit_type == 'impact':
                assert msg.force_direction is not None
                ba.emitfx(
                    position=msg.pos,
                    velocity=(
                        msg.force_direction[0] * 2.0,
                        msg.force_direction[1] * 2.0,
                        msg.force_direction[2] * 2.0,
                    ),
                    count=min(10, 1 + int(damage * 0.01)) if not ba.app.config.get("BSE: Reduced Particles", False) else 5,
                    scale=0.4,
                    spread=0.1,
                )
                
            if msg.hit_subtype == 'cloudy':
                damage = 25
            if msg.hit_subtype == 'vital':
                damage = 0
            if msg.hit_subtype == 'flutter':
                damage = 0.1
            if msg.hit_subtype == 'little_cluster':
                if self._is_toxic:
                    damage = 550 * self.impact_scale
                else: damage = 450 * self.impact_scale
            if msg.hit_subtype == 'lite':
                if self._is_toxic:
                    damage = 500 * self.impact_scale
                    self.node.handlemessage('knockout', 5000.0)
                    PopupText(
                       'Toxitripped!',
                       position=self.node.position,
                       color=(0.49, 0.87, 0.45),
                       scale=1,
                   ).autoretain()
                else:
                    damage = 400 * self.impact_scale
                    self.node.handlemessage('knockout', 3000.0)
            if self.hitpoints > 0:

                # It's kinda crappy to die from impacts, so lets reduce
                # impact damage by a reasonable amount *if* it'll keep us alive
                if msg.hit_type == 'impact' and damage > self.hitpoints:
                    # Drop damage to whatever puts us at 10 hit points,
                    # or 200 less than it used to be whichever is greater
                    # (so it *can* still kill us if its high enough)
                    newdamage = max(damage - 200, self.hitpoints - 10)
                    damage = newdamage
                self.node.handlemessage('flash')

                # If we're holding something, drop it.
                if damage > 0.0 and self.node.hold_node:
                    self.node.hold_node = None
                self.hitpoints -= damage
                self.node.hurt = (
                    1.0 - float(self.hitpoints) / self.hitpoints_max
                )

                # If we're cursed, *any* damage blows us up.
                if self._cursed and damage > 0:
                    ba.timer(
                        0.05,
                        ba.WeakCall(
                            self.curse_explode, msg.get_source_player(ba.Player)
                        ),
                    )

                # If we're frozen, shatter.. otherwise die if we hit zero
                if self.frozen and (damage > 200 or self.hitpoints <= 0):
                    self.shatter()
                elif self.hitpoints <= 0:
                    self.node.handlemessage(
                        ba.DieMessage(how=ba.DeathType.IMPACT)
                    )

            # If we're dead, take a look at the smoothed damage value
            # (which gives us a smoothed average of recent damage) and shatter
            # us if its grown high enough.
            if self.hitpoints <= 0:
                damage_avg = self.node.damage_smoothed * damage_scale
                if damage_avg >= 1000:
                    self.shatter()

        elif isinstance(msg, BombDiedMessage):
            self.bomb_count += 1

        elif isinstance(msg, ba.DieMessage):
            wasdead = self._dead
            self._dead = True
            self.hitpoints = 0
            if not wasdead: self.handlemessage(ba.UnvitalMessage())
            if msg.immediate:
                if self.node:
                    self.node.delete()
            elif self.node:
                self.node.hurt = 1.0
                if self.play_big_death_sound and not wasdead:
                    ba.playsound(SpazFactory.get().single_player_death_sound)
                self.node.dead = True
                ba.timer(2.0, self.node.delete)
            if self.glove_node:
                self.glove_node.delete()
            if self._is_toxic:
                self.node.style = 'ali'
                self.node.color_texture = ba.gettexture('green')
                self.node.color_mask_texture = ba.gettexture('black')
                ba.emitfx(
                    position=self.node.position,
                    velocity=self.node.velocity,
                    count=10 if not ba.app.config.get("BSE: Reduced Particles", False) else 5,
                    spread=0.25,
                    scale=0.45,
                    chunk_type='slime',
                );
            
            # Make sure we still have a node for the funny easter.
            if not self.node.exists(): return

            egg_death_messages = {
                # Snake Family
                'Sneaky Snake':     'snek',
                'Snake Shadow':     'snek',
                'Master Serpent':   'snek',
                # Spaz Family
                'Spaz':             'Powerless Ranger..',
                'Stolt':            'Powerless Ranger..',
                'Soldier Boy':      'Powerless Ranger..',
                # Kronk Family
                'Kronk':            'That was brutal',
                'Kronk Noir':       'That was brutal',
                # Robot Family
                'B-9000':           'ERROR: HEAD MISSING.\nSHUTTING DOWN...',
                'Z03 3000':         'ERROR: HEAD MISSING.\nSHUTTING DOWN...',
                'H4ZE':             'ERROR: HEAD MISSING.\nSHUTTING DOWN...',
                # Mel Family
                'Mel':              'AI HI HI!!!',
                'Melly':            'AI HI HI!!!',
                'Melvin':           'AI HI HI!!!',
                # Other
                'Spencer':          'ROADMAP!!!',
                'Spazzy Toxicant':  'INTOXICATING!!',
                'Agent Johnson':    'but.. i am so pro.. :(',
                'Helpy':            'Can\'t help it!',
                'Mictlan':          'We\'ll meet again!',
            }

            # Fetch a message and attempt an easter egg (1 in 275 chance to appear)
            pmsg = egg_death_messages.get(self.character, None)
            if pmsg and not wasdead: self.secret_funny_death(pmsg, 275)
            
            if self.character == 'Crispin':
                if self.node.exists():
                    self.shatter()

        elif isinstance(msg, ba.OutOfBoundsMessage):
            # By default we just die here.
            self.handlemessage(ba.DieMessage(how=ba.DeathType.FALL))
            if self.glove_node == True:
                self.glove_node.delete()

        elif isinstance(msg, ba.StandMessage):
            self._last_stand_pos = (
                msg.position[0],
                msg.position[1],
                msg.position[2],
            )
            if self.node:
                self.node.handlemessage(
                    'stand',
                    msg.position[0],
                    msg.position[1],
                    msg.position[2],
                    msg.angle,
                )

        elif isinstance(msg, CurseExplodeMessage):
            self.curse_explode()

        elif isinstance(msg, PunchHitMessage):
            if not self.node:
                return None
            node = ba.getcollision().opposingnode

            # Only allow one hit per node per punch.
            if node and (node not in self._punched_nodes):

                punch_momentum_angular = (
                    self.node.punch_momentum_angular * self._punch_power_scale
                )
                punch_power = self.node.punch_power * self._punch_power_scale

                # Ok here's the deal:  we pass along our base velocity for use
                # in the impulse damage calculations since that is a more
                # predictable value than our fist velocity, which is rather
                # erratic. However, we want to actually apply force in the
                # direction our fist is moving so it looks better. So we still
                # pass that along as a direction. Perhaps a time-averaged
                # fist-velocity would work too?.. perhaps should try that.

                # If its something besides another spaz, just do a muffled
                # punch sound.
                if node.getnodetype() != 'spaz':
                    if self.character == 'Splash':
                            sounds = SpazFactory.get().impact_cardboard_sounds_medium
                    elif self.node.style == 'cyborg':
                        sounds = SpazFactory.get().impact_metal_sounds_medium
                    else:
                        sounds = SpazFactory.get().impact_sounds_medium
                    sound = sounds[random.randrange(len(sounds))]
                    ba.playsound(sound, 1.0, position=self.node.position)

                ppos = self.node.punch_position
                punchdir = self.node.punch_velocity
                vel = self.node.punch_momentum_linear

                self._punched_nodes.add(node)
                node.handlemessage(
                    ba.HitMessage(
                        pos=ppos,
                        velocity=vel,
                        magnitude=punch_power * punch_momentum_angular * 110.0,
                        velocity_magnitude=punch_power * 40,
                        radius=0,
                        srcnode=self.node,
                        source_player=self.source_player,
                        force_direction=punchdir,
                        hit_type='punch',
                        hit_subtype=(
                            'super_punch'
                            if self._has_boxing_gloves
                            else 'default'
                        ),
                    )
                )

                # Also apply opposite to ourself for the first punch only.
                # This is given as a constant force so that it is more
                # noticeable for slower punches where it matters. For fast
                # awesome looking punches its ok if we punch 'through'
                # the target.
                mag = -400.0
                if self._hockey:
                    mag *= 0.5
                if len(self._punched_nodes) == 1:
                    self.node.handlemessage(
                        'kick_back',
                        ppos[0],
                        ppos[1],
                        ppos[2],
                        punchdir[0],
                        punchdir[1],
                        punchdir[2],
                        mag,
                    )
        elif isinstance(msg, PickupMessage):
            if not self.node:
                return None

            try:
                collision = ba.getcollision()
                opposingnode = collision.opposingnode
                opposingbody = collision.opposingbody
            except ba.NotFoundError:
                return True

            # Don't allow picking up of invincible dudes.
            try:
                if opposingnode.invincible:
                    return True
            except Exception:
                pass

            try:
                if not opposingnode.getdelegate(ba.Actor, None).can_pickup:
                    return True
            except Exception:
                pass

            # If we're grabbing the pelvis of a non-shattered spaz, we wanna
            # grab the torso instead.
            if (
                opposingnode.getnodetype() == 'spaz'
                and not opposingnode.shattered
                and opposingbody == 4
            ):
                opposingbody = 1

            # Special case - if we're holding a flag, don't replace it
            # (hmm - should make this customizable or more low level).
            held = self.node.hold_node
            if held and held.getnodetype() == 'flag':
                return True

            # Note: hold_body needs to be set before hold_node.
            self.node.hold_body = opposingbody
            self.node.hold_node = opposingnode
        elif isinstance(msg, ba.CelebrateMessage):
            if self.node:
                self.node.handlemessage('celebrate', int(msg.duration * 1000))

        else:
            return super().handlemessage(msg)
        return None

    def secret_funny_death(self,
                           popup_msg: str,
                           one_in: int = 275) -> None:
        """ A dedicated function for our funny death explosions. """
        if self.node.exists() and random.randint(1, one_in) == 1:
            from bastd.actor.bomb import Blast
            PopupText(
            popup_msg,
            position=self.node.position,
            color=self.node.color,
            scale=1,
            ).autoretain()
            self.shatter()
            Blast(self.node.position,
                (0,0,0),
                0.33,
                'normal',
                self.source_player)
            xforce = 15
            yforce = 70
            for x in range(15):
                v = self.node.velocity
                self.node.handlemessage('impulse', self.node.position[0], self.node.position[1], self.node.position[2],
                                        0, 25, 0,
                                        yforce, 0.05, 0, 0,
                                        0, 20*400, 0)
                
                self.node.handlemessage('impulse', self.node.position[0], self.node.position[1], self.node.position[2],
                                        0, 25, 0,
                                        xforce, 0.05, 0, 0,
                                        v[0]*15*2, 0, v[2]*15*2)

    def drop_bomb(self) -> stdbomb.Bomb | None:
        """
        Tell the spaz to drop one of his bombs, and returns
        the resulting bomb object.
        If the spaz has no bombs or is otherwise unable to
        drop a bomb, returns None.
        """

        if ((self.land_mine_count or self.lite_mine_count or self.present_count or self.flutter_mine_count or self.glue_mine_count) <= 0 and self.bomb_count <= 0) or self.frozen:
            return None
        assert self.node
        pos = self.node.position_forward
        vel = self.node.velocity

        if self.land_mine_count > 0:
            dropping_bomb = False
            self.set_land_mine_count(self.land_mine_count - 1)
            bomb_type = 'land_mine'
        elif self.lite_mine_count > 0:
            dropping_bomb = False
            self.set_lite_mine_count(self.lite_mine_count - 1)
            bomb_type = 'lite_mine'
        elif self.present_count > 0:
            dropping_bomb = False
            self.set_present_count(self.present_count - 1)
            bomb_type = 'present'
        elif self.flutter_mine_count > 0:
            dropping_bomb = False
            self.set_flutter_mine_count(self.flutter_mine_count - 1)
            bomb_type = 'flutter_mine'
        elif self.glue_mine_count > 0:
            dropping_bomb = False
            self.set_glue_mine_count(self.glue_mine_count - 1)
            bomb_type = 'glue_mine'
        else:
            dropping_bomb = True
            bomb_type = self.bomb_type

        bomb = stdbomb.Bomb(
            position=(pos[0], pos[1] - 0.0, pos[2]),
            velocity=(vel[0], vel[1], vel[2]),
            bomb_type=bomb_type,
            blast_radius=self.blast_radius,
            source_player=self.source_player,
            owner=self.node,
        ).autoretain()

        assert bomb.node
        if dropping_bomb:
            self.bomb_count -= 1
            bomb.node.add_death_action(
                ba.WeakCall(self.handlemessage, BombDiedMessage())
            )
        self._pick_up(bomb.node)

        for clb in self._dropped_bomb_callbacks:
            clb(self, bomb)

        return bomb

    def _pick_up(self, node: ba.Node) -> None:
        if self.node:
            # Note: hold_body needs to be set before hold_node.
            self.node.hold_body = 0
            self.node.hold_node = node
      
    def set_dash_count(self, count: int) -> None:
        """Set the number of dashes this spaz has."""
        self.dash_count = count
        if self.node:
            if self.dash_count != 0:
                self.node.counter_text = 'x' + str(self.dash_count)
                self.node.counter_texture = (
                    PowerupBoxFactory.get().tex_dash
                )
            else:
                self.node.counter_text = ''
                
    def set_land_mine_count(self, count: int) -> None:
        """Set the number of land-mines this spaz is carrying."""
        self.land_mine_count = count
        if self.node:
            if self.land_mine_count != 0:
                self.node.counter_text = 'x' + str(self.land_mine_count)
                self.node.counter_texture = (
                    PowerupBoxFactory.get().tex_land_mines
                )
            else:
                self.node.counter_text = ''

    def set_lite_mine_count(self, count: int) -> None:
        """Set the number of sky-mines this spaz is carrying."""
        self.lite_mine_count = count
        if self.node:
            if self.lite_mine_count != 0:
                self.node.counter_text = 'x' + str(self.lite_mine_count)
                self.node.counter_texture = (
                    PowerupBoxFactory.get().tex_lite_mines)
            else:
                self.node.counter_text = ''
                
    def set_present_count(self, count: int) -> None:
        """Add one Unwanted Present this spaz is carrying."""
        self.present_count = count
        if self.node:
            if self.present_count != 0:
                self.node.counter_text = 'x' + str(self.present_count)
                self.node.counter_texture = (
                    PowerupBoxFactory.get().tex_present)
                 
            else:
                self.node.counter_text = ''
    
    def set_flutter_mine_count(self, count: int) -> None:
        """Set the number of flutter mines this spaz is carrying."""
        self.flutter_mine_count = count
        if self.node:
            if self.flutter_mine_count != 0:
                self.node.counter_text = 'x' + str(self.flutter_mine_count)
                self.node.counter_texture = (
                    PowerupBoxFactory.get().tex_flutter_mines)
                 
            else:
                self.node.counter_text = ''
    
    def set_glue_mine_count(self, count: int) -> None:
        """Set the number of glue mines this spaz is carrying."""
        self.glue_mine_count = count
        if self.node:
            if self.glue_mine_count != 0:
                self.node.counter_text = 'x' + str(self.glue_mine_count)
                self.node.counter_texture = (
                    PowerupBoxFactory.get().tex_glue_mines)
                 
            else:
                self.node.counter_text = ''
    
    def curse_explode(self, source_player: ba.Player | None = None) -> None:
        """Explode the poor spaz spectacularly."""
        if self._cursed and self.node:
            self.shatter(extreme=True)
            self.handlemessage(ba.DieMessage())
            activity = self._activity()
            if activity:
                stdbomb.Blast(
                    position=self.node.position,
                    velocity=self.node.velocity,
                    blast_radius=3.35,
                    blast_type='normal',
                    source_player=(
                        source_player if source_player else self.source_player
                    ),
                ).autoretain()
            self._cursed = False
            if self._is_toxic and not self.frozen:
                stdbomb.Blast(
                    position=self.node.position,
                    velocity=self.node.velocity,
                    blast_radius=3.5,
                    blast_type='toxic',
                    source_player=(
                        source_player if source_player else self.source_player
                    ),
                ).autoretain()
            self._cursed = False
            if self.frozen:
                stdbomb.Blast(
                    position=self.node.position,
                    velocity=self.node.velocity,
                    blast_radius=3.1,
                    blast_type='ice',
                    source_player=(
                        source_player if source_player else self.source_player
                    ),
                ).autoretain()
            self._cursed = False            
    def shatter(self, extreme: bool = False) -> None:
        """Break the poor spaz into little bits."""
        if self.shattered:
            return
        self.shattered = True
        assert self.node
        if self.frozen:
            # Momentary flash of light.
            light = ba.newnode(
                'light',
                attrs={
                    'position': self.node.position,
                    'radius': 0.4,
                    'height_attenuated': False,
                    'color': (0.2, 1.0, 0.65),
                },
            )

            ba.animate(
                light, 'intensity', {0.0: 3.0, 0.04: 0.5, 0.08: 0.07, 0.3: 0}
            )
            ba.timer(0.1, light.delete)

            # Emit ice chunks.
            ba.emitfx(
                position=self.node.position,
                velocity=self.node.velocity,
                count=int(random.random() * 10.0 + 10.0),
                scale=0.6,
                spread=0.4,
                chunk_type='ice',
            )
            ba.emitfx(
                position=self.node.position,
                velocity=self.node.velocity,
                count=int(random.random() * 10.0 + 10.0),
                scale=0.3,
                spread=0.2,
                chunk_type='ice',
            )
            ba.playsound(
                SpazFactory.get().shatter_sound,
                1.0,
                position=self.node.position,
            )
        else:
            if extreme:
                ba.playsound(
                    SpazFactory.get().splatter_extreme_sound,
                    4.0,
                    position=self.node.position,
                )
            else:
                ba.playsound(
                    SpazFactory.get().splatter_sound,
                    1.0,
                    position=self.node.position,
                )
        self.handlemessage(ba.DieMessage())
        self.node.shattered = 2 if extreme else 1

    def _hit_self(self, intensity: float) -> None:
        if not self.node:
            return
        pos = self.node.position
        self.handlemessage(
            ba.HitMessage(
                flat_damage=50.0 * intensity,
                pos=pos,
                force_direction=self.node.velocity,
                hit_type='impact',
            )
        )
        if self.node.style == 'cyborg':
            ba.emitfx(
                    position=self.node.position,
                    chunk_type='spark',
                    velocity=self.node.velocity,
                    count=6,
                    scale=0.9,
                    spread=0.28,
                )
            ba.emitfx(
                    position=self.node.position,
                    chunk_type='metal',
                    velocity=self.node.velocity,
                    count=3,
                    scale=0.7,
                    spread=0.28,
                )
        if self.character == 'Splash':
            self._juice = ba.newnode(
                        'scorch',
                        attrs={
                            'position': self.node.position,
                            'big': True,
                            'color': self.node.highlight})
            ba.animate(self._juice, 'size', {0: 0, 0.1: 0.6, 1: 0.6, 1.8: 0})
            ba.timer(1.8, self._juice.delete)
        elif self.character in ['Frosty', 'Snow Golem']:
            ba.emitfx(
            position=self.node.position,
            chunk_type='ice',
            velocity=self.node.velocity,
            count=3,
            scale=0.6,
            spread=0.15,
        )  
        elif self.character == 'Spazzy Toxicant':
            ba.emitfx(
            position=self.node.position,
            chunk_type='slime',
            velocity=self.node.velocity,
            count=5,
            scale=0.6,
            spread=0.15,
        )
        self.node.handlemessage('knockout', max(0.0, 50.0 * intensity))
        sounds: Sequence[ba.Sound]
        if intensity >= 5.0:
            if self.character == 'Splash':
                sounds = SpazFactory.get().impact_cardboard_sounds_hard
            elif self.node.style == 'cyborg':
                sounds = SpazFactory.get().impact_metal_sounds_hard
            else:
                sounds = SpazFactory.get().impact_sounds_harder
        elif intensity >= 3.0: 
            if self.character == 'Splash':
                sounds = SpazFactory.get().impact_cardboard_sounds_medium
            elif self.node.style == 'cyborg':
                sounds = SpazFactory.get().impact_metal_sounds_medium
            else:
                sounds = SpazFactory.get().impact_sounds_hard
        else: 
            if self.character == 'Splash':
                sounds = SpazFactory.get().impact_cardboard_sounds_medium
            elif self.node.style == 'cyborg':
                sounds = SpazFactory.get().impact_metal_sounds_medium
            else:
                sounds = SpazFactory.get().impact_sounds_medium
        sound = sounds[random.randrange(len(sounds))]
        ba.playsound(sound, position=pos, volume=4.0)

    def _get_bomb_type_tex(self) -> ba.Texture:
        factory = PowerupBoxFactory.get()
        if self.bomb_type == 'sticky':
            return factory.tex_sticky_bombs
        if self.bomb_type == 'tacky':
            return factory.tex_tacky_bombs
        if self.bomb_type == 'ice':
            return factory.tex_ice_bombs
        if self.bomb_type == 'impact':
            return factory.tex_impact_bombs
        if self.bomb_type == 'clouder':
            return factory.tex_clouder_bombs
        if self.bomb_type == 'steampunk':
            return factory.tex_steampunk_bombs
        if self.bomb_type == 'toxic':
            return factory.tex_toxic_bombs
        if self.bomb_type == 'vital':
            return factory.tex_vital_bombs
        if self.bomb_type == 'cluster':
            return factory.tex_cluster_bombs
        raise ValueError('invalid bomb type')

    def _flash_billboard(self, tex: ba.Texture) -> None:
        assert self.node
        self.node.billboard_texture = tex
        self.node.billboard_cross_out = False
        ba.animate(
            self.node,
            'billboard_opacity',
            {0.0: 0.0, 0.1: 1.0, 0.4: 1.0, 0.5: 0.0},
        )

    def set_bomb_count(self, count: int) -> None:
        """Sets the number of bombs this Spaz has."""
        # We can't just set bomb_count because some bombs may be laid currently
        # so we have to do a relative diff based on max.
        diff = count - self._max_bomb_count
        self._max_bomb_count += diff
        self.bomb_count += diff

    def _gloves_wear_off_flash(self) -> None:
        if self.node:
            self.node.boxing_gloves_flashing = True
            self.node.billboard_texture = PowerupBoxFactory.get().tex_punch
            self.node.billboard_opacity = 1.0
            self.node.billboard_cross_out = True

    def _gloves_wear_off(self) -> None:
        if self._demo_mode:  # Preserve old behavior.
            self._punch_power_scale = 1.35
            self._punch_cooldown = BASE_PUNCH_COOLDOWN
        else:
            factory = SpazFactory.get()
            if self._is_vital == False:
                self._punch_cooldown = factory.punch_cooldown
            else:
                self._punch_cooldown = VITAL_PUNCH_COOLDOWN
            self._punch_power_scale = factory.punch_power_scale
        self._has_boxing_gloves = False
        if self.node:
            ba.playsound(
                PowerupBoxFactory.get().powerdown_sound,
                position=self.node.position,
            )
            self.node.boxing_gloves = False
            self.node.billboard_opacity = 0.0
    
    def _flying_gloves_wear_off_flash(self) -> None:
        if self.node:
            self.node.billboard_texture = ba.gettexture('powerupFlyingPunch')
            self.node.billboard_opacity = 1.0
            self.node.billboard_cross_out = True
        if self.glove_node:
                ba.animate(self.glove_node, 'model_scale', {
                    0: 1,
                    2: 0,
                })
            
    def _flying_gloves_wear_off(self) -> None:
        if self.glove_node:
            self.glove_node.delete()
        
        factory = SpazFactory.get()
        if self._is_vital == False:
            self._punch_cooldown = factory.punch_cooldown
        else:
            self._punch_cooldown = VITAL_PUNCH_COOLDOWN
        self._has_flying_gloves = False
        if self.node:
            ba.playsound(
                PowerupBoxFactory.get().powerdown_sound,
                position=self.node.position,
            )
            self.node.billboard_opacity = 0.0
            
    def _multi_bomb_wear_off_flash(self) -> None:
        if self.node:
            self.node.billboard_texture = PowerupBoxFactory.get().tex_bomb
            self.node.billboard_opacity = 1.0
            self.node.billboard_cross_out = True

    def _multi_bomb_wear_off(self) -> None:
        self.set_bomb_count(self.default_bomb_count)
        if self.node:
            ba.playsound(
                PowerupBoxFactory.get().powerdown_sound,
                position=self.node.position,
            )
            self.node.billboard_opacity = 0.0

    def _bomb_wear_off_flash(self) -> None:
        if self.node:
            self.node.billboard_texture = self._get_bomb_type_tex()
            self.node.billboard_opacity = 1.0
            self.node.billboard_cross_out = True

    def _bomb_wear_off(self) -> None:
        self.bomb_type = self.bomb_type_default
        if self.node:
            ba.playsound(
                PowerupBoxFactory.get().powerdown_sound,
                position=self.node.position,
            )
            self.node.billboard_opacity = 0.0