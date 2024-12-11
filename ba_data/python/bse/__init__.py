"""Explodinary's main module; loads any needed scripts on startup."""

import bascenev1 as bs
import os

CLAY_DIRECTORY: str = os.path.join(bs.app.env.python_directory_app, 'bse')
DATA_DIRECTORY: str = os.path.join(CLAY_DIRECTORY, '_data')

from . import (
    _pluginfix,
    _music,
    _language,
    wrappers,
    mainmenu,
    config,
    #ui,
)
_pluginfix.do() # run our plugin list fix from older versions

from .custom import (
    announcer,
    appearance,
    particle,
    quickturn,
    spazbot,
)

# Subsystems
cfg = config.ClaypocalypseConfigSubsystem()