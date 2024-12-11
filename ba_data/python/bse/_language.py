from __future__ import annotations

import os
import logging
import json

import bascenev1 as bs
import _babase
from babase._language import (
    LanguageSubsystem,
    Lstr,
    AttrDict,
    _add_to_attr_dict,
)
import bse

# We're "forking" a class, so we'll have a
# lot of "undefined" vars. from __init__.
# pylint: disable=W0201


class LanguageSubsystemSupport(LanguageSubsystem):
    """Overwrite for our classic LanguageSubsystem."""

    def setlanguage(
        self,
        language: str | None,
        print_change: bool = True,
        store_to_config: bool = True,
        clay_aware: bool = False,  # If we are aware of
        # having a clay lang variant.
    ) -> None:
        """Set the active app language.

        Pass None to use OS default language.
        """
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-branches
        assert _babase.in_logic_thread()
        cfg = _babase.app.config
        cur_language = cfg.get('Lang', None)

        # Store this in the config if its changing.
        if language != cur_language and store_to_config:
            if language is None:
                if 'Lang' in cfg:
                    del cfg['Lang']  # Clear it out for default.
            else:
                cfg['Lang'] = language
            cfg.commit()
            switched = True
        else:
            switched = False

        with open(
            os.path.join(
                _babase.app.env.data_directory,
                'ba_data',
                'data',
                'languages',
                'english.json',
            ),
            encoding='utf-8',
        ) as infile:
            lenglishvalues = json.loads(infile.read())

        # None implies default.
        if language is None:
            language = self.default_language
        try:
            if language == 'English':
                lmodvalues = None
            else:
                lmodfile = os.path.join(
                    _babase.app.env.data_directory,
                    'ba_data',
                    'data',
                    'languages',
                    language.lower() + '.json',
                )
                with open(lmodfile, encoding='utf-8') as infile:
                    lmodvalues = json.loads(infile.read())
        except Exception:
            logging.exception("Error importing language '%s'.", language)
            _babase.screenmessage(
                f"Error setting language to '{language}'; see log for details.",
                color=(1, 0, 0),
            )
            switched = False
            lmodvalues = None

        # Claypocalypse json append
        # English default
        with open(
            os.path.join(
                _babase.app.env.data_directory,
                bse.DATA_DIRECTORY,
                'lang',
                'english.json',
            ),
            encoding='utf-8',
        ) as infile:
            lclayengvalues = json.loads(infile.read())
        # Custom lang.
        try:
            lclayfile = os.path.join(
                bse.DATA_DIRECTORY,
                'lang',
                language.lower() + '.json',
            )
            with open(lclayfile, encoding='utf-8') as infile:
                lclayvalues = json.loads(infile.read())
        except Exception as e:
            # Don't do this if the file simply doesn't exist.
            if not isinstance(e, FileNotFoundError) and clay_aware:
                logging.exception(
                    "Error importing clay language '%s'.", language
                )
                _babase.screenmessage(
                    f"Error loading clay json of '{language}';"
                    "see log for details.",
                    color=(1, 0, 0),
                )
            lclayvalues = None

        self._language = language

        # Create an attrdict of *just* our target language.
        self._language_target = AttrDict()
        langtarget = self._language_target
        assert langtarget is not None
        _add_to_attr_dict(
            langtarget, lmodvalues if lmodvalues is not None else lenglishvalues
        )

        # Create an attrdict of our target language overlaid on our base
        # (english).
        languages = [lenglishvalues]
        if lmodvalues is not None:
            languages.append(lmodvalues)
        # Prioritize Claypocalypse lang.
        languages.append(lclayengvalues)
        if lclayvalues is not None:
            languages.append(lclayvalues)
        lfull = AttrDict()
        for lmod in languages:
            _add_to_attr_dict(lfull, lmod)
        self._language_merged = lfull

        # Pass some keys/values in for low level code to use; start with
        # everything in their 'internal' section.
        internal_vals = [
            v for v in list(lfull['internal'].items()) if isinstance(v[1], str)
        ]

        # Cherry-pick various other values to include.
        # (should probably get rid of the 'internal' section
        # and do everything this way)
        for value in [
            'replayNameDefaultText',
            'replayWriteErrorText',
            'replayVersionErrorText',
            'replayReadErrorText',
        ]:
            internal_vals.append((value, lfull[value]))
        internal_vals.append(
            ('axisText', lfull['configGamepadWindow']['axisText'])
        )
        internal_vals.append(('buttonText', lfull['buttonText']))
        lmerged = self._language_merged
        assert lmerged is not None
        random_names = [
            n.strip() for n in lmerged['randomPlayerNamesText'].split(',')
        ]
        random_names = [n for n in random_names if n != '']
        _babase.set_internal_language_keys(internal_vals, random_names)
        if switched and print_change:
            _babase.screenmessage(
                Lstr(
                    resource='languageSetText',
                    subs=[
                        ('${LANGUAGE}', Lstr(translate=('languages', language)))
                    ],
                ),
                color=(0, 1, 0),
            )


# Overwrite our default setlanguage function!
LanguageSubsystem.setlanguage = LanguageSubsystemSupport.setlanguage
# Refresh our language after getting replaced.
bs.app.lang.setlanguage(
    bs.app.lang.language,
    print_change=False,
    store_to_config=False,
)
