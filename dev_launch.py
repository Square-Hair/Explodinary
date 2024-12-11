"""Launch script for Claypocalypse.
Updates and replaces important files that can't be changed on runtime."""
from __future__ import annotations

import os
import sys
import shutil
import subprocess

import json
import random
import string

ROOT_DIRECTORY = os.path.dirname(
    __file__ if not __file__.startswith(os.environ.get('TEMP')) else
    sys.executable
)
class ReplaceFunction:
    """The!"""
    def __init__(self) -> None:
        # Check if we're running this from an executable or script.
        # (if running from an .exe, __file__ should return a temp directory)
        root = ROOT_DIRECTORY
        # Set our directories.
        self.where: str = os.path.abspath(
            f'{root}/ba_data/python/bse/'
        )
        self.py_dir: str = os.path.abspath(
            f'{root}/ba_data/python/'
        )

    def _download_and_install(self) -> None:
        # TODO: Create an installer that fetches from GitHub.
        raise RuntimeError('Not implemented.')

    def do_replace(self) -> None:
        """
        Move files from bse/installer/replacement
        to their respective locations.
        """
        replacement_dir = f'{self.where}/.basereplace'
        subdirs = [
            d for d in os.listdir(replacement_dir)
            if os.path.isdir(os.path.join(replacement_dir, d))
            ]
        for subdir in subdirs:
            source: str         = f'{replacement_dir}/{subdir}'
            destination: str    = f'{self.py_dir}/{subdir}'
            # Create the destination path in case it doesn't exist.
            if not os.path.exists(destination):
                os.makedirs(destination)
            # Copy our subfolder into the target folder.
            shutil.copytree(
                source,
                destination,
                dirs_exist_ok=True
                )

class GenerateGibberish:
    """Generate the gibberish lang. file for Claypocalypse."""
    def __init__(self) -> None:
        self.langpath = os.path.join(
            ROOT_DIRECTORY,
            'ba_data',
            'python',
            'bse',
            '_data',
            'lang'
        )
        self.langfile = 'english.json'

    def do_generate(self) -> None:
        """Load our base langfile and scramble it around."""
        # Read and import the base lang. file.
        jsonfile: dict
        with open(
            os.path.join(self.langpath, self.langfile),
            'r', encoding='UTF-8'
        ) as file:
            jsonfile = json.loads(file.read())

        # Scramble each line.
        def scramble_line(line: str) -> str:
            """Scramble a string."""
            finalstr: str = ''
            # Use the string as our seed.
            random.seed(line)
            def randoltr() -> str:
                """Returns a random letter
                (or punctuation in rare occasions)."""
                return random.choice(
                    ((' ' + string.ascii_lowercase) * 6)
                    + '.,'
                )

            for letter in line:
                out: str = ''
                choich = random.choice(
                    [1] * 8 +
                    [2] * 5 +
                    [3] * 7 +
                    [4] * 2 +
                    [5] * 1
                )
                # Did you know? All capital letters in any string do
                # not get scrambled at all! Look it up!
                if not (
                    letter.isupper()
                    or letter.isspace()
                    or letter.isnumeric()
                    or letter.isdecimal()
                    or (letter.isascii() and not letter.isalpha())
                ):
                    match choich:
                        case 1: # Leave alone
                            out = letter
                        case 2: # Delete
                            pass
                        case 3: # Replace solo
                            out = randoltr()
                        case 4: # Replace add
                            out = (
                                randoltr() +
                                ''.join(randoltr() for _
                                 in range(random.randint(1, 2)))
                            )
                        case _: # Add
                            out = (
                                letter +
                                ''.join(randoltr() for _
                                 in range(random.randint(1, 2)))
                            )
                # Ignore capitalization.
                else:
                    out = letter
                finalstr += out

            return finalstr

        def walk_scramble(walk_to: dict) -> None:
            """Walk and scramble each entry."""
            ourwalk = walk_to.copy()
            for key, item in ourwalk.items():
                # Scramble every line on a list.
                if isinstance(item, list):
                    newlist: list = []
                    for s in [s for s in item if isinstance(s, str)]:
                        newlist.append(scramble_line(s))
                    ourwalk[key] = newlist
                # Scramble a singular line.
                elif isinstance(item, str):
                    ourwalk[key] = scramble_line(item)
                # If we end up with a null, generate and scramble a string.
                elif item is None:
                    ourwalk[key] = scramble_line(str(key))
                # Scramble a new dict.
                elif isinstance(item, dict):
                    ourwalk[key] = walk_scramble(item)
            return ourwalk

        jsonfile = walk_scramble(jsonfile)

        # Write the scrambled file into "gibberish.json".
        with open(
            os.path.join(self.langpath, 'gibberish.json'), 'w',
        ) as gibberishfile:
            json.dump(jsonfile, gibberishfile, indent=4)

print('Running replacement process before launching...')
ReplaceFunction().do_replace()
print('Generating gibberish file...')
GenerateGibberish().do_generate()

# Launch Claypocalypse.
print('Done.')
subprocess.Popen('Explodinary.exe')
