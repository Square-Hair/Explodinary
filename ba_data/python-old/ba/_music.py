# Released under the MIT License. See LICENSE for details.
#
"""Music related functionality."""
from __future__ import annotations

import copy
from typing import TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

import _ba

if TYPE_CHECKING:
    from typing import Callable, Any
    import ba


class MusicType(Enum):
    """Types of music available to play in-game.

    Category: **Enums**

    These do not correspond to specific pieces of music, but rather to
    'situations'. The actual music played for each type can be overridden
    by the game or by the user.
    """
    #GENERAL
    MENU = 'Menu'
    MENU_NIGHT = 'MenuNight'
    MENU_ADVENTURE = 'MenuAdventure'
    MENU_ISLAND = 'MenuIsland'
    MENU_FOREST = 'MenuForest'
    MENU_MOUNTAIN = 'MenuMountain'
    VICTORY = 'Victory'
    CHAR_SELECT = 'CharSelect'
    RUN_AWAY = 'RunAway'
    ONSLAUGHT = 'Onslaught'
    KEEP_AWAY = 'Keep Away'
    RACE = 'Race'
    EPIC_RACE = 'Epic Race'
    SCORES = 'Scores'
    GRAND_ROMP = 'GrandRomp'
    TO_THE_DEATH = 'ToTheDeath'
    CHOSEN_ONE = 'Chosen One'
    FORWARD_MARCH = 'ForwardMarch'
    FLAG_CATCHER = 'FlagCatcher'
    SURVIVAL = 'Survival'
    EPIC = 'Epic'
    SPORTS = 'Sports'
    HOCKEY = 'Hockey'
    FOOTBALL = 'Football'
    FLYING = 'Flying'
    SCARY = 'Scary'
    MARCHING = 'Marching'
    #BSE
    KABLOOYA = 'Kablooya'
    RUNAROUND = 'Runaround'
    SOCCER = 'Soccer'
    MOUNTAINKING = 'Mountain King'
    ROULETTE = 'Roulette'
    HUB = 'Hub'
    FUSE_CRUISE = 'Fuse Cruise'
    BOMBNUTS = 'Bombnuts'
    ARMS_RACE = 'Arms Race'
    #DEFEAT
    DEFEAT = 'Defeat'
    DEFEAT_KABLOOYA = 'DefeatKablooya'
    #PATHWAY PANDEMONIUM
    RESTYE = 'RestYe'
    RESTYE2 = 'RestYe2'
    RESTYE3 = 'RestYe3'
    RESTYE4 = 'RestYe4'
    RESTYEDEFEAT = 'RestYeDefeat'
    #BSE CAMPAIGN
    BEGINNING = 'Beginning'
    GROTTO = 'Grotto'
    SWAMP = 'Swamp'
    ALPINE = 'Alpine'
    MOUNT_CHILL = 'MountChill'
    GOLEM = 'Golem'
    HOT_AIR = 'HotAir'
    BLOCKLAND = 'Blockland'
    PRE_ABYSS = 'PreAbyss'
    ABYSS = 'Abyss'
    BOMB_POEM = 'BombPoem'
    #CHAOS
    CHAOS_SWEET = 'ChaosSweetRelease'
    CHAOS_SUGARCUBE = 'ChaosSugarcubeHailstorm'
    CHAOS_CHILI = 'ChaosChiliHailstorm'
    CHAOS_PIZZA = 'ChaosPizza'
    CHAOS_PINEAPPLE = 'ChaosPineapple'
    CHAOS_OREGANO = 'ChaosOregano'
    CHAOS_LASAGNA = 'ChaosLasagna'


class MusicPlayMode(Enum):
    """Influences behavior when playing music.

    Category: **Enums**
    """

    REGULAR = 'regular'
    TEST = 'test'


@dataclass
class AssetSoundtrackEntry:
    """A music entry using an internal asset.

    Category: **App Classes**
    """

    assetname: str
    volume: float = 1.0
    loop: bool = True


# What gets played by default for our different music types:
ASSET_SOUNDTRACK_ENTRIES: dict[MusicType, AssetSoundtrackEntry] = {

    ### BOMBSQUAD MUSIC [MIGHT CONTAIN BSE REPLACEMENTS]
    MusicType.VICTORY: AssetSoundtrackEntry('victoryMusic', volume=1.2, loop=False),
    MusicType.CHAR_SELECT: AssetSoundtrackEntry('charSelectMusic', volume=0.4),
    MusicType.RUN_AWAY: AssetSoundtrackEntry('runAwayMusic', volume=1.2),
    MusicType.ONSLAUGHT: AssetSoundtrackEntry('onslaughtMusic', volume=0.9),
    MusicType.KEEP_AWAY: AssetSoundtrackEntry('runAwayMusic', volume=1.2),
    MusicType.RACE: AssetSoundtrackEntry('raceMusic', volume=1.2),
    MusicType.EPIC_RACE: AssetSoundtrackEntry('slowEpicMusic', volume=1.2),
    MusicType.SCORES: AssetSoundtrackEntry('scoresEpicMusic', volume=0.6, loop=False),
    MusicType.GRAND_ROMP: AssetSoundtrackEntry('grandRompMusic', volume=1.2),
    MusicType.TO_THE_DEATH: AssetSoundtrackEntry('toTheDeathMusic', volume=0.8),
    MusicType.CHOSEN_ONE: AssetSoundtrackEntry('survivalMusic', volume=0.8),
    MusicType.RUNAROUND: AssetSoundtrackEntry('runaroundMusic', volume=0.8),
    MusicType.FORWARD_MARCH: AssetSoundtrackEntry('forwardMarchMusic', volume=0.8),
    MusicType.FLAG_CATCHER: AssetSoundtrackEntry('flagCatcherMusic', volume=0.8),
    MusicType.SURVIVAL: AssetSoundtrackEntry('survivalMusic', volume=0.8),
    MusicType.EPIC: AssetSoundtrackEntry('slowEpicMusic', volume=1.5),
    MusicType.SPORTS: AssetSoundtrackEntry('sportsMusic', volume=0.8),
    MusicType.HOCKEY: AssetSoundtrackEntry('sportsMusic', volume=0.8),
    MusicType.FOOTBALL: AssetSoundtrackEntry('sportsMusic', volume=0.8),
    MusicType.FLYING: AssetSoundtrackEntry('flyingMusic', volume=0.8),
    MusicType.SCARY: AssetSoundtrackEntry('scaryMusic', volume=0.45),

    ### EXPLODINARY MUSIC
    MusicType.KABLOOYA: AssetSoundtrackEntry('kablooyaMusic', volume=0.9),                  # Can Can | Offenbach
    MusicType.SOCCER: AssetSoundtrackEntry('soccerMusic', volume=1.0),                      # Sabre Dance | Aram Khachaturian
    MusicType.MARCHING: AssetSoundtrackEntry('fastMountainKing', volume=0.8),               # Catch That Yeti (High) | Plants Vs. Zombies: Garden Warfare OST
    MusicType.MOUNTAINKING: AssetSoundtrackEntry('mountainKingMusic', volume=0.7),          # In The Hall Of The Mountain King | Epic Trailer Version
    MusicType.ROULETTE: AssetSoundtrackEntry('rouletteMusic', volume=1),                    # Come Along With Me - An Adventure Time Orchestration | Rush Garcia
    MusicType.HUB: AssetSoundtrackEntry('hubMusic', volume=0.8),                            # Peaceful Nature | AI Generated
    MusicType.FUSE_CRUISE: AssetSoundtrackEntry('cruiseMusic', volume=0.92),                # Drunken Sailor - Sea Shanty - Instrumental | Tim Beek Music
    MusicType.BOMBNUTS: AssetSoundtrackEntry('bombnutsMusic', volume=1.1),                  # Sticks and Stones - Orchestral X Chiptune Cover | Kāru
    MusicType.ARMS_RACE: AssetSoundtrackEntry('armsRaceMusic', volume=0.8),                 # Waltz No. 2 | Dmitri Shostakovich
    
    #MENU
    MusicType.MENU: AssetSoundtrackEntry('menuMusic'),                                      # BombStory - Sunset | SoK
    MusicType.MENU_NIGHT: AssetSoundtrackEntry('menuMusicNight'),                           # BombSquad Explodinary - Night Theme | SoK
    MusicType.MENU_ADVENTURE: AssetSoundtrackEntry('menuAdventureMusic'),                   # Otherside - Epic Orchestra Version | Kalamity Music
    MusicType.MENU_ISLAND: AssetSoundtrackEntry('menuIslandMusic'),                         # Relic - Epic Orchestral Cover | Kalamity Music
    MusicType.MENU_FOREST: AssetSoundtrackEntry('menuForestMusic'),                         # Modulo (Minecraft Fan Music) | Steelman
    MusicType.MENU_MOUNTAIN: AssetSoundtrackEntry('menuMountainMusic', volume=0.9),         # Fading Memories - Fan Made Minecraft Music Disc | Laudividni
    
    #DEFEAT
    MusicType.DEFEAT: AssetSoundtrackEntry('defeatMusic', volume=0.25),                     # Calm Luxury Hotel Lobby Jazz | Hotel Jazz Deluxe
    MusicType.DEFEAT_KABLOOYA: AssetSoundtrackEntry('defeatKablooyaMusic', volume=0.25),    # Main Menu Theme | Angels vs Devils
    
    #PATHWAY PANDEMONIUM
    MusicType.RESTYE: AssetSoundtrackEntry('restYeMusic1', volume=0.8),                     # God Rest Ye Merry Gentlemen | The Avalon Pops Orchestra
    MusicType.RESTYE2: AssetSoundtrackEntry('restYeMusic2', volume=0.65),                   # God Rest Ye Merry Gentleman - Epic Version | Epic Christmas Music
    MusicType.RESTYE3: AssetSoundtrackEntry('restYeMusic3', volume=0.75),                   # God Rest Ye Merry Gentlemen (Epic Version) | Matt Ebenezer
    MusicType.RESTYE4: AssetSoundtrackEntry('restYeMusic4', volume=0.75),                   # God Rest Ye Merry Gentlemen | James Dooley
    MusicType.RESTYEDEFEAT: AssetSoundtrackEntry('restYeDefeatMusic', volume=0.75),         # God Rest Ye Merry Celtishmen | A. Nakarada

    #BSE CAMPAIGN
    MusicType.BEGINNING: AssetSoundtrackEntry('beginningMusic', volume=0.8),                # BSE - The Beginning | ShadowQ
    MusicType.GROTTO: AssetSoundtrackEntry('grottoMusic', volume=0.8),                      # BSE - Beyond The Grotto | ShadowQ
    MusicType.SWAMP: AssetSoundtrackEntry('swampMusic', volume=0.8),                        # BSE - Mysterious Swamp | ShadowQ
    MusicType.ALPINE: AssetSoundtrackEntry('alpineMusic', volume=0.8),                      # BSE - Alpine Gateway | ShadowQ
    MusicType.MOUNT_CHILL: AssetSoundtrackEntry('mountChillMusic', volume=0.2),             # BSE - Mount Chill | ShadowQ
    MusicType.GOLEM: AssetSoundtrackEntry('golemMusic', volume=0.15),                       # BSE - GOLEM! | ShadowQ
    MusicType.HOT_AIR: AssetSoundtrackEntry('hotAirMusic', volume=0.8),                     # BSE - Balloon | ShadowQ
    MusicType.BLOCKLAND: AssetSoundtrackEntry('blocklandMusic', volume=0.8),                # BSE - Blockland | ShadowQ
    MusicType.PRE_ABYSS: AssetSoundtrackEntry('abyssPreparation', volume=0.8),              # Background Music - Underwater inspired by Taboo | CO.AG Music
    MusicType.ABYSS: AssetSoundtrackEntry('abyssMusic', volume=0.8),                        # BSE - Overseer Hailstorm | ShadowQ
    MusicType.BOMB_POEM: AssetSoundtrackEntry('bombPoem', volume=0.85),                     # Calm Ambience | Sleep Music/Relaxing Music/Instrumental
        
    #CHAOS
    MusicType.CHAOS_SUGARCUBE: AssetSoundtrackEntry('chaosSugarcube', volume=0.8),          # Sugarcube Hailstorm | PaperKitty
    MusicType.CHAOS_CHILI: AssetSoundtrackEntry('chaosChili', volume=1.5),                  # Chili Hailstorm | SoK
    MusicType.CHAOS_SWEET: AssetSoundtrackEntry('chaosSweet', volume=0.7),                  # Sweet Release of Death | RodMod
    MusicType.CHAOS_PIZZA: AssetSoundtrackEntry('chaosPizza', volume=0.35),                 # It's Pizza Time! | Mr. Sauceman
    MusicType.CHAOS_PINEAPPLE: AssetSoundtrackEntry('chaosPineapple', volume=0.17),         # Pinapple Rag Techno Remake | Gooseworx
    MusicType.CHAOS_OREGANO: AssetSoundtrackEntry('chaosOregano', volume=0.35),             # Oregano Mirage | ClascyJitto (Frostix)
    MusicType.CHAOS_LASAGNA: AssetSoundtrackEntry('chaosLasagna', volume=0.35),             # Mondaymania II | aytanner
                                                                                            #   I'll never forget how SoK plugged this song onto my dms 
                                                                                            #   right after talking about having to go to a funeral LMFAO -Temp
}


class MusicSubsystem:
    """Subsystem for music playback in the app.

    Category: **App Classes**

    Access the single shared instance of this class at 'ba.app.music'.
    """

    def __init__(self) -> None:
        # pylint: disable=cyclic-import
        self._music_node: _ba.Node | None = None
        self._music_mode: MusicPlayMode = MusicPlayMode.REGULAR
        self._music_player: MusicPlayer | None = None
        self._music_player_type: type[MusicPlayer] | None = None
        self.music_types: dict[MusicPlayMode, MusicType | None] = {
            MusicPlayMode.REGULAR: None,
            MusicPlayMode.TEST: None,
        }

        # Set up custom music players for platforms that support them.
        # FIXME: should generalize this to support arbitrary players per
        # platform (which can be discovered via ba_meta).
        # Our standard asset playback should probably just be one of them
        # instead of a special case.
        if self.supports_soundtrack_entry_type('musicFile'):
            from ba.osmusic import OSMusicPlayer

            self._music_player_type = OSMusicPlayer
        elif self.supports_soundtrack_entry_type('iTunesPlaylist'):
            from ba.macmusicapp import MacMusicAppMusicPlayer

            self._music_player_type = MacMusicAppMusicPlayer

    def on_app_launch(self) -> None:
        """Should be called by app on_app_launch()."""

        # If we're using a non-default playlist, lets go ahead and get our
        # music-player going since it may hitch (better while we're faded
        # out than later).
        try:
            cfg = _ba.app.config
            if 'Soundtrack' in cfg and cfg['Soundtrack'] not in [
                '__default__',
                'Default Soundtrack',
            ]:
                self.get_music_player()
        except Exception:
            from ba import _error

            _error.print_exception('error prepping music-player')

    def on_app_shutdown(self) -> None:
        """Should be called when the app is shutting down."""
        if self._music_player is not None:
            self._music_player.shutdown()

    def have_music_player(self) -> bool:
        """Returns whether a music player is present."""
        return self._music_player_type is not None

    def get_music_player(self) -> MusicPlayer:
        """Returns the system music player, instantiating if necessary."""
        if self._music_player is None:
            if self._music_player_type is None:
                raise TypeError('no music player type set')
            self._music_player = self._music_player_type()
        return self._music_player

    def music_volume_changed(self, val: float) -> None:
        """Should be called when changing the music volume."""
        if self._music_player is not None:
            self._music_player.set_volume(val)

    def set_music_play_mode(
        self, mode: MusicPlayMode, force_restart: bool = False
    ) -> None:
        """Sets music play mode; used for soundtrack testing/etc."""
        old_mode = self._music_mode
        self._music_mode = mode
        if old_mode != self._music_mode or force_restart:

            # If we're switching into test mode we don't
            # actually play anything until its requested.
            # If we're switching *out* of test mode though
            # we want to go back to whatever the normal song was.
            if mode is MusicPlayMode.REGULAR:
                mtype = self.music_types[MusicPlayMode.REGULAR]
                self.do_play_music(None if mtype is None else mtype.value)

    def supports_soundtrack_entry_type(self, entry_type: str) -> bool:
        """Return whether provided soundtrack entry type is supported here."""
        uas = _ba.env()['user_agent_string']
        assert isinstance(uas, str)

        # FIXME: Generalize this.
        if entry_type == 'iTunesPlaylist':
            return 'Mac' in uas
        if entry_type in ('musicFile', 'musicFolder'):
            return (
                'android' in uas
                and _ba.android_get_external_files_dir() is not None
            )
        if entry_type == 'default':
            return True
        return False

    def get_soundtrack_entry_type(self, entry: Any) -> str:
        """Given a soundtrack entry, returns its type, taking into
        account what is supported locally."""
        try:
            if entry is None:
                entry_type = 'default'

            # Simple string denotes iTunesPlaylist (legacy format).
            elif isinstance(entry, str):
                entry_type = 'iTunesPlaylist'

            # For other entries we expect type and name strings in a dict.
            elif (
                isinstance(entry, dict)
                and 'type' in entry
                and isinstance(entry['type'], str)
                and 'name' in entry
                and isinstance(entry['name'], str)
            ):
                entry_type = entry['type']
            else:
                raise TypeError(
                    'invalid soundtrack entry: '
                    + str(entry)
                    + ' (type '
                    + str(type(entry))
                    + ')'
                )
            if self.supports_soundtrack_entry_type(entry_type):
                return entry_type
            raise ValueError('invalid soundtrack entry:' + str(entry))
        except Exception:
            from ba import _error

            _error.print_exception()
            return 'default'

    def get_soundtrack_entry_name(self, entry: Any) -> str:
        """Given a soundtrack entry, returns its name."""
        try:
            if entry is None:
                raise TypeError('entry is None')

            # Simple string denotes an iTunesPlaylist name (legacy entry).
            if isinstance(entry, str):
                return entry

            # For other entries we expect type and name strings in a dict.
            if (
                isinstance(entry, dict)
                and 'type' in entry
                and isinstance(entry['type'], str)
                and 'name' in entry
                and isinstance(entry['name'], str)
            ):
                return entry['name']
            raise ValueError('invalid soundtrack entry:' + str(entry))
        except Exception:
            from ba import _error

            _error.print_exception()
            return 'default'

    def on_app_resume(self) -> None:
        """Should be run when the app resumes from a suspended state."""
        if _ba.is_os_playing_music():
            self.do_play_music(None)

    def do_play_music(
        self,
        musictype: MusicType | str | None,
        continuous: bool = False,
        mode: MusicPlayMode = MusicPlayMode.REGULAR,
        testsoundtrack: dict[str, Any] | None = None,
    ) -> None:
        """Plays the requested music type/mode.

        For most cases, setmusic() is the proper call to use, which itself
        calls this. Certain cases, however, such as soundtrack testing, may
        require calling this directly.
        """

        # We can be passed a MusicType or the string value corresponding
        # to one.
        if musictype is not None:
            try:
                musictype = MusicType(musictype)
            except ValueError:
                print(f"Invalid music type: '{musictype}'")
                musictype = None

        with _ba.Context('ui'):

            # If they don't want to restart music and we're already
            # playing what's requested, we're done.
            if continuous and self.music_types[mode] is musictype:
                return
            self.music_types[mode] = musictype

            # If the OS tells us there's currently music playing,
            # all our operations default to playing nothing.
            if _ba.is_os_playing_music():
                musictype = None

            # If we're not in the mode this music is being set for,
            # don't actually change what's playing.
            if mode != self._music_mode:
                return

            # Some platforms have a special music-player for things like iTunes
            # soundtracks, mp3s, etc. if this is the case, attempt to grab an
            # entry for this music-type, and if we have one, have the
            # music-player play it.  If not, we'll play game music ourself.
            if musictype is not None and self._music_player_type is not None:
                if testsoundtrack is not None:
                    soundtrack = testsoundtrack
                else:
                    soundtrack = self._get_user_soundtrack()
                entry = soundtrack.get(musictype.value)
            else:
                entry = None

            # Go through music-player.
            if entry is not None:
                self._play_music_player_music(entry)

            # Handle via internal music.
            else:
                self._play_internal_music(musictype)

    def _get_user_soundtrack(self) -> dict[str, Any]:
        """Return current user soundtrack or empty dict otherwise."""
        cfg = _ba.app.config
        soundtrack: dict[str, Any] = {}
        soundtrackname = cfg.get('Soundtrack')
        if soundtrackname is not None and soundtrackname != '__default__':
            try:
                soundtrack = cfg.get('Soundtracks', {})[soundtrackname]
            except Exception as exc:
                print(f'Error looking up user soundtrack: {exc}')
                soundtrack = {}
        return soundtrack

    def _play_music_player_music(self, entry: Any) -> None:

        # Stop any existing internal music.
        if self._music_node is not None:
            self._music_node.delete()
            self._music_node = None

        # Do the thing.
        self.get_music_player().play(entry)

    def _play_internal_music(self, musictype: MusicType | None) -> None:

        # Stop any existing music-player playback.
        if self._music_player is not None:
            self._music_player.stop()

        # Stop any existing internal music.
        if self._music_node:
            self._music_node.delete()
            self._music_node = None

        # Start up new internal music.
        if musictype is not None:

            entry = ASSET_SOUNDTRACK_ENTRIES.get(musictype)
            if entry is None:
                print(f"Unknown music: '{musictype}'")
                entry = ASSET_SOUNDTRACK_ENTRIES[MusicType.FLAG_CATCHER]

            self._music_node = _ba.newnode(
                type='sound',
                attrs={
                    'sound': _ba.getsound(entry.assetname),
                    'positional': False,
                    'music': True,
                    'volume': entry.volume * 5.0,
                    'loop': entry.loop,
                },
            )


class MusicPlayer:
    """Wrangles soundtrack music playback.

    Category: **App Classes**

    Music can be played either through the game itself
    or via a platform-specific external player.
    """

    def __init__(self) -> None:
        self._have_set_initial_volume = False
        self._entry_to_play: Any = None
        self._volume = 1.0
        self._actually_playing = False

    def select_entry(
        self,
        callback: Callable[[Any], None],
        current_entry: Any,
        selection_target_name: str,
    ) -> Any:
        """Summons a UI to select a new soundtrack entry."""
        return self.on_select_entry(
            callback, current_entry, selection_target_name
        )

    def set_volume(self, volume: float) -> None:
        """Set player volume (value should be between 0 and 1)."""
        self._volume = volume
        self.on_set_volume(volume)
        self._update_play_state()

    def play(self, entry: Any) -> None:
        """Play provided entry."""
        if not self._have_set_initial_volume:
            self._volume = _ba.app.config.resolve('Music Volume')
            self.on_set_volume(self._volume)
            self._have_set_initial_volume = True
        self._entry_to_play = copy.deepcopy(entry)

        # If we're currently *actually* playing something,
        # switch to the new thing.
        # Otherwise update state which will start us playing *only*
        # if proper (volume > 0, etc).
        if self._actually_playing:
            self.on_play(self._entry_to_play)
        else:
            self._update_play_state()

    def stop(self) -> None:
        """Stop any playback that is occurring."""
        self._entry_to_play = None
        self._update_play_state()

    def shutdown(self) -> None:
        """Shutdown music playback completely."""
        self.on_app_shutdown()

    def on_select_entry(
        self,
        callback: Callable[[Any], None],
        current_entry: Any,
        selection_target_name: str,
    ) -> Any:
        """Present a GUI to select an entry.

        The callback should be called with a valid entry or None to
        signify that the default soundtrack should be used.."""

    # Subclasses should override the following:

    def on_set_volume(self, volume: float) -> None:
        """Called when the volume should be changed."""

    def on_play(self, entry: Any) -> None:
        """Called when a new song/playlist/etc should be played."""

    def on_stop(self) -> None:
        """Called when the music should stop."""

    def on_app_shutdown(self) -> None:
        """Called on final app shutdown."""

    def _update_play_state(self) -> None:

        # If we aren't playing, should be, and have positive volume, do so.
        if not self._actually_playing:
            if self._entry_to_play is not None and self._volume > 0.0:
                self.on_play(self._entry_to_play)
                self._actually_playing = True
        else:
            if self._actually_playing and (
                self._entry_to_play is None or self._volume <= 0.0
            ):
                self.on_stop()
                self._actually_playing = False


def setmusic(musictype: ba.MusicType | None, continuous: bool = False) -> None:
    """Set the app to play (or stop playing) a certain type of music.

    category: **Gameplay Functions**

    This function will handle loading and playing sound assets as necessary,
    and also supports custom user soundtracks on specific platforms so the
    user can override particular game music with their own.

    Pass None to stop music.

    if 'continuous' is True and musictype is the same as what is already
    playing, the playing track will not be restarted.
    """

    # All we do here now is set a few music attrs on the current globals
    # node. The foreground globals' current playing music then gets fed to
    # the do_play_music call in our music controller. This way we can
    # seamlessly support custom soundtracks in replays/etc since we're being
    # driven purely by node data.
    gnode = _ba.getactivity().globalsnode
    gnode.music_continuous = continuous
    gnode.music = '' if musictype is None else musictype.value
    gnode.music_count += 1


def do_play_music(*args: Any, **keywds: Any) -> None:
    """A passthrough used by the C++ layer."""
    _ba.app.music.do_play_music(*args, **keywds)
