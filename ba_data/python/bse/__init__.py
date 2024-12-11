"""Explodinary's main module; loads any needed scripts on startup."""

from . import (
    _music,
    wrappers,
    mainmenu,
    config,
)

from .custom import (
    announcer,
    appearance,
    particle,
    quickturn,
    spazbot,
)

# Subsystems
cfg = config.ClaypocalypseConfigSubsystem()