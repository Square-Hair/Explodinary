""" Replaces the settings menu with our own. """

from __future__ import annotations

import bauiv1lib.settings.allsettings
import bse.ui.settings.allsettings

bauiv1lib.settings.allsettings.AllSettingsWindow = (
    bse.ui.settings.allsettings.AllSettingsWindow
)
