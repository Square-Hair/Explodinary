from __future__ import annotations
import ba, bastd

from explodinary import _versiondata

from typing import Any

def _create_bse_config():
    """ Creates a BSE key in the config file if there isn't any. """
    ba.app.config.setdefault(_versiondata.configsub, {})
    ba.app.config.commit()
fgmc = _create_bse_config; fgmc() # For Good Measure Check

exconfig: dict = ba.app.config[_versiondata.configsub]
chaossub: str = "ChaosMode"

def _create_bse_config_subdir(key: str) -> None:
    """ Creates a subdirectory on our config directory. """
    exconfig.setdefault(key, {})
    ba.app.config.commit()

# General (Unused for now)

def get(key: str, fallback: Any | None = None) -> Any:
    """ Gets a value from our config database. """
    return exconfig.get(key, fallback)

def set(key: str, val: Any) -> None:
    """ Writes a value to our config. """
    exconfig[key] = val
    ba.app.config.commit()

def stablish(key: str, fallback: Any | None = None) -> Any:
    """ Tries to get a value from our config,
        if failed, creates a fallback value and returns it. """
    v = exconfig.setdefault(key, fallback)
    ba.app.config.commit()
    return v

# Chaos

def _build_chaos_settings() -> None:
    """ Creates all Chaos Mode config directories.
        This is called only in explodinary/loader.py """
    _create_bse_config_subdir(chaossub)
    chaosc: dict = exconfig[chaossub]
    
    settings = [
        ('Enabled',     False),
        ('Time',        12),
        ('Time_show',   True),
        ('Time_pos',    'bottom'),
        ('Event_show',  True),
        ('Event_len',   7),
        ('Event_pos',  'right'),
        ('DoAnnounce',  True),
        ('DoSound',     True),
        ('DoMusic',     True)
    ]
    
    for setting in settings:
        chaosc.setdefault(setting[0], setting[1])
        
    ba.app.config.commit()
    
def chaos_get(key: str) -> Any:
    """ Gets a value from our Chaos config key. """
    # Try getting our chaos setting
    try: return exconfig[chaossub].get(key)
    except Exception as e:
        if e is KeyError: raise Exception(f'Chaos config key not found: "{key}"')
        else            : raise Exception(e)
        
def chaos_set(key: str, val: Any) -> None:
    """ Writes a value to our Chaos config. """
    exconfig[chaossub][key] = val
    ba.app.config.commit()