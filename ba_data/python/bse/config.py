"""Config. manager."""

from __future__ import annotations
from typing import TYPE_CHECKING

import bascenev1 as bs

if TYPE_CHECKING:
    from typing import Any


# Courtesy of Claypocalypse!
class ClaypocalypseConfigSubsystem:
    """
    Subsystem in charge of managing config. information.

    Makes writing and saving to the "Claypocalypse" config. dict.
    miles more optimal than using "bs.app.config.*" functions.
    Also stores some local variables used for a variety of things.
    """

    def __init__(self) -> None:
        # Create a config. dict. if it doesn't exist already.
        self.base_dict = "Explodinary"
        self.base_dict_internal = "bse"
        bs.app.config.setdefault(self.base_dict, {})

        # import from 2.4< in case we haven't
        if not self.fetch('has_imported'):
            self._retro_settings()

    def __repr__(self) -> str:
        return repr(bs.app.config.get(self.base_dict, {}))

    def write(self, directory: str, value: Any) -> None:
        """
        Writes to a specific dict. subkey(s) on
        a string, commits & applies when finished.

        Args:
            directory (str): Directory-type subkeys and variable locator.
            value (Any): The value to write to the target variable.

        Example:
            write('training.dummy', True) will write
            bs.app.config[self.base_dict]['training']['dummy'] = True

        Raises:
            KeyError: The provided directory is not a valid path.
                      Usually raised when accessing variables as a directory.
        """
        # Turn our "to" directory to an actual dict. subkey.
        subs = directory.split(".")
        target: dict = bs.app.config[self.base_dict]

        # Enter our subkeys, creating a default subdict if
        # it doesn't exist, omitting the last one to set the value.
        for i, sub in enumerate(subs[:-1]):
            # Create subkey and check.
            target.setdefault(sub, {})
            if not isinstance(target.get(sub, None), dict):
                # Raise an error if the key we're trying
                # to enter is not an actual key.
                # Show the key's value on our way out.
                raise KeyError(
                    f'Config path: "{".".join(list(subs[:i+1]))}"'
                    "is not valid!\n"
                    f"config['{self.base_dict}']"
                    f'{[f"[{key}]" for key in subs[:i+1]]} = {target[sub]}\n\n'
                    f'Caused when trying to access "{sub}".'
                )
            # Move our target.
            target = target[sub]

        # Write to our target.
        target[subs[-1]] = value
        # Apply and commit!
        self._apply_and_commit()

    def fetch(
        self, directory: str, fallback: Any = None, do_set: bool = False
    ) -> Any:
        """
        Looks for and return a key's value.

        Args:
            directory (str): Directory-type subkeys the desired variable is at.
            fallback (Any): The value provided if such variable doesn't exist.
            do_set (bool): Create the value of it previously didn't exist.

        Example:
            fetch('training.dummy', None, True) will get
            bs.app.config[self.base_dict]['training']['dummy'] variable's
            value, or return "None" if it doesn't exist.
            It will also create the value if it didn't exist before.

        Raises:
            KeyError: The provided directory is not a valid path.
                      Usually raised when accessing variables as a directory.

        Returns:
            Any: The value of the provided directory or fallback if None.
        """
        # Turn our "at" directory to an actual dict. subkey.
        subs = directory.split(".")
        target: dict = bs.app.config[self.base_dict]

        # Enter the subkey.
        for i, sub in enumerate(subs[:-1]):
            # Create subkey and check.
            target.setdefault(sub, {})
            if not isinstance(target[sub], dict):
                # Raise an error if we try
                # to enter a non-subkey.
                raise KeyError(
                    f'Config path: "{".".join(list(subs[:i+1]))}"'
                    "is not a valid subkey!\n\n"
                    f'Caused when trying to access "{sub}".'
                )
            target = target[sub]

        # Return the variable's value, or the
        # fallback value if it doesn't exist.
        to_sender = (
            target.setdefault(subs[-1], fallback)
            if do_set
            else target.get(subs[-1], fallback)
        )
        # Save the key if it didn't previously exist.
        if do_set:
            self._apply_and_commit()
        # Parry.
        return to_sender

    def write_internal(self, directory: str, value: Any) -> None:
        """Make a v1 account transaction for a clay-based value.
        Useful for storing data independent of our config.
        """
        bs.app.plus.add_v1_account_transaction(
            {
                "type": "SET_MISC_VAL",
                "name": f"{self.base_dict_internal}.{directory}",
                "value": value,
            }
        )
        bs.app.plus.run_v1_account_transactions()

    def fetch_internal(
        self, directory: str, fallback: Any = None, do_set: bool = False
    ) -> Any:
        """Fetch a v1 account value.

        Useful for getting data independent from our config.
        """
        v = bs.app.plus.get_v1_account_misc_val(
            f"{self.base_dict_internal}.{directory}", fallback
        )
        if do_set:
            self.write_internal(directory, fallback)
        return v

    def nuke_config(self) -> None:
        """
        Resets our Claypocalypse dict.
        Please don't use this unless necessary.
        """
        # Scary!
        bs.app.config[self.base_dict] = {}
        self._apply_and_commit()

    # bs.app.config "forks".
    def _commit(self) -> None:
        bs.app.config.commit()

    def _apply(self) -> None:
        bs.app.config.apply()

    def _apply_and_commit(self) -> None:
        bs.app.config.apply_and_commit()

    def _retro_settings(self) -> None:
        """Import config. settins from <=2.4."""
        one = ( # old settings collection
            ('BSE: Speedrun Mode','speedrun.enabled'),
            ('BSE: Skip Cutscenes','skip_cutscenes'),
            ('BSE: Reduced Particles','particle_redux'),
            ('BSE: TNT Variants','tnt_variants'),
            ('BSE: Powerup Popups','powerup_text'),
            ('BSE: Announce Games','game_announcer'),
            ('BSE: Custom Particles','particle_custom'),
            ('BSE: Quickturn','quickturn'),
            ('BSE: Powerup Distribution','powerup_dist'),
            ('BSE: Chaos Mode','chaos_mode'),
            ('BSE: Menu Theme','menu_theme'),
            ('BSE: Latest Version','data.last_ver'),
            ('BSE: Oversilly Oversillier','unlocks.oversilly'),
            ('BSE: Adios Amigo','unlocks.adiosamigo'),
        )
        two = ( # from BSE-Config.ChaosMode
            ('Enabled','chaos.enabled'),
            ('DoMusic','chaos.music'),
            ('DoSound','chaos.sound'),
            ('DoAnnounce','chaos.announce'),
            ('Event_len','chaos.events.length'),
            ('Event_pos','chaos.events.position'),
            ('Event_show','chaos.events.show'),
            ('Time','chaos.time.value'),
            ('Time_pos','chaos.time.position'),
            ('Time_show','chaos.time.show'),
        )

        # duplicate settings by checking if they exist, then writing to b
        for i, collec in enumerate([one, two]):
            for a,b in collec:
                v = (
                    # standard
                    bs.app.config.get(a, None) if i != 1
                    # from BSE-Config.ChaosMode dict
                    else bs.app.config.get(
                        'BSE-Config', {'ChaosMode':{}}
                    )['ChaosMode'].get(a, None)
                )
                if v:
                    self.write(b, v)
        # prevent further imports
        self.write('has_imported', True)