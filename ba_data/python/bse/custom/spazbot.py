""" A list of our custom made bots. """

from __future__ import annotations

import bascenev1 as bs
from bascenev1lib.actor.spaz import Spaz
from bascenev1lib.actor.spazbot import (
    SpazBot,
    DEFAULT_BOT_COLOR,
    DEFAULT_BOT_HIGHLIGHT,
    # LITE_BOT_COLOR, LITE_BOT_HIGHLIGHT,
    PRO_BOT_COLOR,
    PRO_BOT_HIGHLIGHT,
)
import bascenev1lib.actor.spazbot as VanillaBots

import random
import weakref
from enum import Enum

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable
    from bascenev1lib.actor.flag import Flag


class AppearanceGroup(Enum):
    """
    Appearance keys that contain multiple appearances.
    Used by some bots that have several styles to them.
    """

    NINJA = ["Snake Shadow", "Sneaky Snake"]
    PIRATE = ["Jack Morgan", "Ye Olde' Sparrow", "Jackie Panty"]


class BSESpazBot(SpazBot):
    """Our custom SpazBot with a variety of custom qualities."""

    # Powerup pickupability
    accepts_powerups = False

    def __init__(self) -> None:
        # Unpack our Enum if so.
        if isinstance(self.character, AppearanceGroup):
            self.character = self.character.value
        # Select from list.
        if isinstance(self.character, list):
            self.character = random.choice(self.character)

        # accept_powerups fallback as vanilla bots don't like the new __init__.
        try:
            self.accepts_powerups
        except:
            self.accepts_powerups = False

        # Follow standard behavior.
        Spaz.__init__(
            self=self,
            color=self.color,
            highlight=self.highlight,
            character=self.character,
            source_player=None,
            start_invincible=False,
            can_accept_powerups=self.accepts_powerups,
        )

        # If you need to add custom behavior to a bot, set this to a callable
        # which takes one arg (the bot) and returns False if the bot's normal
        # update should be run and True if not.
        self.update_callback: Callable[[SpazBot], Any] | None = None
        activity = self.activity
        assert isinstance(activity, bs.GameActivity)
        self._map = weakref.ref(activity.map)
        self.last_player_attacked_by: bs.Player | None = None
        self.last_attacked_time = 0.0
        self.last_attacked_type: tuple[str, str] | None = None
        self.target_point_default: bs.Vec3 | None = None
        self.held_count = 0
        self.last_player_held_by: bs.Player | None = None
        self.target_flag: Flag | None = None
        self._charge_speed = 0.5 * (
            self.charge_speed_min + self.charge_speed_max
        )
        self._lead_amount = 0.5
        self._mode = "wait"
        self._charge_closing_in = False
        self._last_charge_dist = 0.0
        self._running = False
        self._last_jump_time = 0.0

        self._throw_release_time: float | None = None
        self._have_dropped_throw_bomb: bool | None = None
        self._player_pts: list[tuple[bs.Vec3, bs.Vec3]] | None = None

        # These cooldowns didn't exist when these bots were calibrated,
        # so take them out of the equation.
        self._jump_cooldown = 0
        self._pickup_cooldown = 0
        self._fly_cooldown = 0
        self._bomb_cooldown = 0
        # Wavedash stuff (it blows up unless we add this here.)
        self._wavedash_cooldown = 99999
        self.last_wavedash_time_ms = -99999
        self.grounded = 0
        # It took me ~1 hour to figure that out...
        # Anotha day, anotha victory for the og,,,

        if self.start_cursed:
            self.curse()


class ToxicBot(VanillaBots.BomberBotPro):
    """A variant of BomberBot with Toxic Bombs."""

    character = "Spazzy Toxicant"
    default_bomb_type = "toxic"
    color = (0.49, 0.87, 0.45)
    highlight = (0.1, 0.35, 0.1)
    default_boxing_gloves = False


class NoirBot(VanillaBots.BrawlerBotLite):
    """A slow moving bot that tries to punch you, and occasionally throws impact bombs."""

    character = "Kronk Noir"
    color = (0.13, 0.13, 0.13)
    highlight = (0.4, 0.2, 0.1)
    default_boxing_gloves = True
    default_bomb_type = "impact"
    throwiness = 0.4
    throw_dist_min = 2.0
    throw_dist_max = 5.0
    points_mult = 2


class StickyBotPro(VanillaBots.StickyBot):
    """A stronger StickyBot."""

    color = PRO_BOT_COLOR
    highlight = PRO_BOT_HIGHLIGHT
    default_shields = True
    default_boxing_gloves = True
    points_mult = 3


class MellyBot(SpazBot):
    """A static bot that tries to bomb you."""

    character = "Melly"
    color = (0.4, 0.05, 0.05)
    highlight = (0.2, 0.35, 0.21)
    static = True
    default_boxing_gloves = True
    throw_dist_min = 0.0
    throw_dist_max = 10.0
    default_bomb_type = "sticky"
    points_mult = 2


class WaiterBot(SpazBot):
    """A less crazy bot with tacky bombs."""

    character = "Melvin"
    punchiness = 1
    throwiness = 1
    run = True
    charge_dist_min = 4.0
    charge_dist_max = 10.0
    charge_speed_min = 1.0
    charge_speed_max = 1.0
    throw_rate = 2.0
    throw_dist_min = 0.0
    throw_dist_max = 5.5
    default_bomb_count = 2
    default_bomb_type = "tacky"
    points_mult = 3


class WaiterBotPro(WaiterBot):
    """A stronger WaiterBot."""

    color = PRO_BOT_COLOR
    highlight = PRO_BOT_HIGHLIGHT
    default_bomb_count = 3
    default_boxing_gloves = True
    points_mult = 4


class WaiterBotProShielded(WaiterBotPro):
    """A stronger version of ba.WaiterBot who starts with shields."""

    default_shields = True
    points_mult = 5


class FrostyBot(SpazBot):
    """A snowman bot who throws Ice Bombs."""

    character = "Frosty"
    points_mult = 3
    color = (0.5, 0.5, 1)
    highlight = (1, 0.5, 0)
    default_bomb_type = "ice"
    default_bomb_count = 3
    punchiness = 0.7
    throw_rate = 1.3
    run = True
    run_dist_min = 6.0


class ExplodeyBotNoTimeLimitSlow(VanillaBots.BrawlerBotLite):
    """A cursed bot who starts with shield and does not explode on his own. Vey slow, though."""

    character = AppearanceGroup.PIRATE
    start_cursed = True
    default_shields = True
    curse_time = None
    color = PRO_BOT_COLOR
    highlight = PRO_BOT_HIGHLIGHT


class SantaBot(SpazBot):
    """A running bot with Unwanted Present.

    category: Bot Classes
    """

    character = "Santa Claus"
    punchiness = 0.9
    throwiness = 1.0
    color = (1, 0, 0)
    highlight = (1, 1, 1)
    run = True
    charge_dist_min = 4.0
    charge_dist_max = 10.0
    charge_speed_min = 1.0
    charge_speed_max = 1.0
    throw_dist_min = 0.0
    throw_dist_max = 4.0
    throw_rate = 2.0
    default_bomb_type = "present"
    default_bomb_count = 1
    points_mult = 4


class SantaBotPro(SantaBot):
    """A stronger ba.SantaBot.

    category: Bot Classes
    """

    color = PRO_BOT_COLOR
    highlight = PRO_BOT_HIGHLIGHT
    default_shields = True
    default_boxing_gloves = True
    points_mult = 5


class MicBot(SpazBot):
    """
    category: Bot Classes

    A slow moving bot that ocasionally throws sky mines.
    """

    character = "Mictlan"
    punchiness = 0.5
    throwiness = 1.0
    color = (0.1, 0.1, 1)
    highlight = (0.1, 0.1, 0.5)
    charge_dist_max = 4
    throw_rate = 1.5
    charge_speed_min = 1
    charge_speed_max = 1
    throw_dist_min = 3
    throw_dist_max = 9999
    default_bomb_count = 6
    default_bomb_type = "lite_mine"
    points_mult = 2


class MicBotPro(MicBot):
    """A stronger ba.MicBot.

    category: Bot Classes
    """

    color = PRO_BOT_COLOR
    highlight = PRO_BOT_HIGHLIGHT
    default_shields = True
    default_boxing_gloves = True
    points_mult = 3


class SplashBot(SpazBot):
    """
    category: Bot Classes

    A bot that can accept powerups.
    """

    character = "Splash"
    punchiness = 0.5
    throwiness = 1.0
    color = (0.2, 1, 0.2)
    highlight = (1, 1, 0)
    charge_dist_max = 4
    throw_rate = 1.5
    run = True
    charge_speed_min = 1
    charge_speed_max = 1
    throwDistMin = 3
    throwDistMax = 9999
    default_bomb_count = 6
    default_bomb_type = "normal"
    can_accept_powerups = True
    points_mult = 2


class SoldatBot(SpazBot):
    """A little Soldier Boy with Flutter Bombs!

    category: Bot Classes
    """

    character = "Soldier Boy"
    default_bomb_type = "clouder"
    points_mult = 2
    color = (0.9, 0.5, 0.5)
    highlight = (1, 0.3, 0.5)
    default_bomb_count = 2
    punchiness = 0.7
    throw_rate = 0.8


"""
VANILLA OVERRIDES:
Replaces some vanilla appearances (mainly for Stolt over hard bots, purely cosmetic.)
"""


class BomberBotPro(VanillaBots.BomberBotPro):
    character = "Stolt"


class BomberBotProShielded(VanillaBots.BomberBotProShielded):
    character = "Stolt"


class BomberBotProStatic(VanillaBots.BomberBotProStatic):
    character = "Stolt"


class BomberBotProStaticShielded(VanillaBots.BomberBotProStaticShielded):
    character = "Stolt"


class ChargerBot(VanillaBots.ChargerBot):
    character = AppearanceGroup.NINJA


class ChargerBotPro(VanillaBots.ChargerBotPro):
    character = "Master Serpent"


class ChargerBotProShielded(VanillaBots.ChargerBotProShielded):
    character = "Master Serpent"


class TriggerBotPro(VanillaBots.TriggerBotPro):
    character = "Z03 3000"


class ExplodeyBot(VanillaBots.ExplodeyBot):
    character = AppearanceGroup.PIRATE


class ExplodeyBotNoTimeLimit(VanillaBots.ExplodeyBotNoTimeLimit):
    character = AppearanceGroup.PIRATE


class ExplodeyBotShielded(VanillaBots.ExplodeyBotShielded):
    character = "Ye Olde' Sparrow"


SpazBot.__init__ = BSESpazBot.__init__

VanillaBots.BomberBotPro = BomberBotPro
VanillaBots.BomberBotProShielded = BomberBotProShielded
VanillaBots.BomberBotProStatic = BomberBotProStatic
VanillaBots.BomberBotProStaticShielded = BomberBotProStaticShielded
VanillaBots.ChargerBot = ChargerBot
VanillaBots.ChargerBotPro = ChargerBotPro
VanillaBots.ChargerBotProShielded = ChargerBotProShielded
VanillaBots.TriggerBotPro = TriggerBotPro
VanillaBots.ExplodeyBot = ExplodeyBot
VanillaBots.ExplodeyBotNoTimeLimit = ExplodeyBotNoTimeLimit
VanillaBots.ExplodeyBotShielded = ExplodeyBotShielded
