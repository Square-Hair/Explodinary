""" A module containing all of Explodinary's music. """
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any

from baclassic._music import (
    MusicType,
    MusicPlayMode,
    AssetSoundtrackEntry,
    ASSET_SOUNDTRACK_ENTRIES,
    MusicSubsystem,
)
from enum import Enum

"""
MUSIC DATA
Append all your music here!
"""

# Our custom MusicType enum.
class MusicTypeBSE(Enum):
    # MAIN MENU
    MENU            = 'Menu'
    MENU_NIGHT      = 'MenuNight'
    MENU_ADVENTURE  = 'MenuAdventure'
    MENU_ISLAND     = 'MenuIsland'
    MENU_FOREST     = 'MenuForest'
    MENU_MOUNTAIN   = 'MenuMountain'
    MENU_SPOOKY     = 'MenuSpooky'
    # GAMEMODE
    KABLOOYA        = 'Kablooya'
    RUNAROUND       = 'Runaround'
    SOCCER          = 'Soccer'
    MOUNTAINKING    = 'Mountain King'
    ROULETTE        = 'Roulette'
    HUB             = 'Hub'
    FUSE_CRUISE     = 'Fuse Cruise'
    BOMBNUTS        = 'Bombnuts'
    ARMS_RACE       = 'Arms Race'
    # DEFEAT
    DEFEAT          = 'Defeat'
    DEFEAT_KABLOOYA = 'DefeatKablooya'
    # PATHWAY PANDEMONIUM
    RESTYE          = 'RestYe'
    RESTYE2         = 'RestYe2'
    RESTYE3         = 'RestYe3'
    RESTYE4         = 'RestYe4'
    RESTYEDEFEAT    = 'RestYeDefeat'
    # BSE CAMPAIGN
    BEGINNING       = 'Beginning'
    GROTTO          = 'Grotto'
    SWAMP           = 'Swamp'
    ALPINE          = 'Alpine'
    MOUNT_CHILL     = 'MountChill'
    GOLEM           = 'Golem'
    HOT_AIR         = 'HotAir'
    BLOCKLAND       = 'Blockland'
    PRE_ABYSS       = 'PreAbyss'
    ABYSS           = 'Abyss'
    BOMB_POEM       = 'BombPoem'
    # CHAOS MODE
    CHAOS_SWEET     = 'ChaosSweetRelease'
    CHAOS_SUGARCUBE = 'ChaosSugarcubeHailstorm'
    CHAOS_CHILI     = 'ChaosChiliHailstorm'
    CHAOS_PIZZA     = 'ChaosPizza'
    CHAOS_PINEAPPLE = 'ChaosPineapple'
    CHAOS_OREGANO   = 'ChaosOregano'
    CHAOS_LASAGNA   = 'ChaosLasagna'

# Our soundtrack entries.
EXPLODINARY_SOUNDTRACK_ENTRIES: dict[MusicTypeBSE, AssetSoundtrackEntry] = {
    # MENU
    MusicTypeBSE.MENU           : AssetSoundtrackEntry('bse_menuMusic'),                            # BombStory - Sunset | SoK
    MusicTypeBSE.MENU_NIGHT     : AssetSoundtrackEntry('bse_menuMusicNight'),                       # BombSquad Explodinary - Night Theme | SoK
    MusicTypeBSE.MENU_ADVENTURE : AssetSoundtrackEntry('bse_menuAdventureMusic'),                   # Otherside - Epic Orchestra Version | Kalamity Music
    MusicTypeBSE.MENU_ISLAND    : AssetSoundtrackEntry('bse_menuIslandMusic'),                      # Relic - Epic Orchestral Cover | Kalamity Music
    MusicTypeBSE.MENU_FOREST    : AssetSoundtrackEntry('bse_menuForestMusic'),                      # Modulo (Minecraft Fan Music) | Steelman
    MusicTypeBSE.MENU_MOUNTAIN  : AssetSoundtrackEntry('bse_menuMountainMusic', volume=0.9),        # Fading Memories - Fan Made Minecraft Music Disc | Laudividni
    MusicTypeBSE.MENU_SPOOKY    : AssetSoundtrackEntry('bse_menuSpookyMusic', volume=0.5),          # Spooky Scary Skeletons (Medieval Cover) | Middle Ages
    
    # GAMEMODE
    MusicTypeBSE.KABLOOYA       : AssetSoundtrackEntry('bse_kablooyaMusic', volume=0.9),            # Can Can | Offenbach
    MusicTypeBSE.SOCCER         : AssetSoundtrackEntry('bse_soccerMusic', volume=1.0),              # Sabre Dance | Aram Khachaturian
    ### TODO: Weird ass vanilla music override from 1.7.19?? Change that.
    MusicType.MARCHING          : AssetSoundtrackEntry('bse_fastMountainKing', volume=0.8),         # Catch That Yeti (High) | Plants Vs. Zombies: Garden Warfare OST
    MusicTypeBSE.MOUNTAINKING   : AssetSoundtrackEntry('bse_mountainKingMusic', volume=0.7),        # In The Hall Of The Mountain King | Epic Trailer Version
    MusicTypeBSE.ROULETTE       : AssetSoundtrackEntry('bse_rouletteMusic', volume=1),              # Come Along With Me - An Adventure Time Orchestration | Rush Garcia
    MusicTypeBSE.HUB            : AssetSoundtrackEntry('bse_hubMusic', volume=0.8),                 # Peaceful Nature | AI Generated
    MusicTypeBSE.FUSE_CRUISE    : AssetSoundtrackEntry('bse_cruiseMusic', volume=0.92),             # Drunken Sailor - Sea Shanty - Instrumental | Tim Beek Music
    MusicTypeBSE.BOMBNUTS       : AssetSoundtrackEntry('bse_bombnutsMusic', volume=1.1),            # Sticks and Stones - Orchestral X Chiptune Cover | Kāru
    MusicTypeBSE.ARMS_RACE      : AssetSoundtrackEntry('bse_armsRaceMusic', volume=0.8),            # Waltz No. 2 | Dmitri Shostakovich

    # DEFEAT
    MusicTypeBSE.DEFEAT         : AssetSoundtrackEntry('bse_defeatMusic', volume=0.25),             # Calm Luxury Hotel Lobby Jazz | Hotel Jazz Deluxe
    MusicTypeBSE.DEFEAT_KABLOOYA: AssetSoundtrackEntry('bse_defeatKablooyaMusic', volume=0.25),     # Main Menu Theme | Angels vs Devils
    
    # PATHWAY PANDEMONIUM
    MusicTypeBSE.RESTYE         : AssetSoundtrackEntry('bse_restYeMusic1', volume=0.8),             # God Rest Ye Merry Gentlemen | The Avalon Pops Orchestra
    MusicTypeBSE.RESTYE2        : AssetSoundtrackEntry('bse_restYeMusic2', volume=0.65),            # God Rest Ye Merry Gentleman - Epic Version | Epic Christmas Music
    MusicTypeBSE.RESTYE3        : AssetSoundtrackEntry('bse_restYeMusic3', volume=0.75),            # God Rest Ye Merry Gentlemen (Epic Version) | Matt Ebenezer
    MusicTypeBSE.RESTYE4        : AssetSoundtrackEntry('bse_restYeMusic4', volume=0.75),            # God Rest Ye Merry Gentlemen | James Dooley
    MusicTypeBSE.RESTYEDEFEAT   : AssetSoundtrackEntry('bse_restYeDefeatMusic', volume=0.75),       # God Rest Ye Merry Celtishmen | A. Nakarada

    # BSE CAMPAIGN
    MusicTypeBSE.BEGINNING      : AssetSoundtrackEntry('bse_beginningMusic', volume=0.8),           # BSE - The Beginning | ShadowQ
    MusicTypeBSE.GROTTO         : AssetSoundtrackEntry('bse_grottoMusic', volume=0.8),              # BSE - Beyond The Grotto | ShadowQ
    MusicTypeBSE.SWAMP          : AssetSoundtrackEntry('bse_swampMusic', volume=0.8),               # BSE - Mysterious Swamp | ShadowQ
    MusicTypeBSE.ALPINE         : AssetSoundtrackEntry('bse_alpineMusic', volume=0.8),              # BSE - Alpine Gateway | ShadowQ
    MusicTypeBSE.MOUNT_CHILL    : AssetSoundtrackEntry('bse_mountChillMusic', volume=0.2),          # BSE - Mount Chill | ShadowQ
    MusicTypeBSE.GOLEM          : AssetSoundtrackEntry('bse_golemMusic', volume=0.15),              # BSE - GOLEM! | ShadowQ
    MusicTypeBSE.HOT_AIR        : AssetSoundtrackEntry('bse_hotAirMusic', volume=0.8),              # BSE - Balloon | ShadowQ
    MusicTypeBSE.BLOCKLAND      : AssetSoundtrackEntry('bse_blocklandMusic', volume=0.8),           # BSE - Blockland | ShadowQ
    MusicTypeBSE.PRE_ABYSS      : AssetSoundtrackEntry('bse_abyssPreparation', volume=0.8),         # Background Music - Underwater inspired by Taboo | CO.AG Music
    MusicTypeBSE.ABYSS          : AssetSoundtrackEntry('bse_abyssMusic', volume=0.8),               # BSE - Overseer Hailstorm | ShadowQ
    MusicTypeBSE.BOMB_POEM      : AssetSoundtrackEntry('bse_bombPoem', volume=0.85),                # Calm Ambience | Sleep Music/Relaxing Music/Instrumental
        
    # CHAOS MODE
    MusicTypeBSE.CHAOS_SUGARCUBE: AssetSoundtrackEntry('bse_chaosSugarcube', volume=0.8),           # Sugarcube Hailstorm | PaperKitty
    MusicTypeBSE.CHAOS_CHILI    : AssetSoundtrackEntry('bse_chaosChili', volume=1.5),               # Chili Hailstorm | SoK
    MusicTypeBSE.CHAOS_SWEET    : AssetSoundtrackEntry('bse_chaosSweet', volume=0.7),               # Sweet Release of Death | RodMod
    MusicTypeBSE.CHAOS_PIZZA    : AssetSoundtrackEntry('bse_chaosPizza', volume=0.35),              # It's Pizza Time! | Mr. Sauceman
    MusicTypeBSE.CHAOS_PINEAPPLE: AssetSoundtrackEntry('bse_chaosPineapple', volume=0.17),          # Pinapple Rag Techno Remake | Gooseworx
    MusicTypeBSE.CHAOS_OREGANO  : AssetSoundtrackEntry('bse_chaosOregano', volume=0.35),            # Oregano Mirage | ClascyJitto (Frostix)
    MusicTypeBSE.CHAOS_LASAGNA  : AssetSoundtrackEntry('bse_chaosLasagna', volume=0.35),            # Mondaymania II | aytanner
                                                                                                    #   I'll never forget how SoK plugged this song onto my dms 
                                                                                                    #   right after talking about having to go to a funeral LMFAO -Temp
}

# Merge them with our base asset soundtrack entries.
ASSET_SOUNDTRACK_ENTRIES.update(EXPLODINARY_SOUNDTRACK_ENTRIES)

#
#
#
#
#
#
#
#
#
#
#
#
#
#


"""
Internal overriding
Function replacing beyond this point.
"""
def patched_do_play_music(
    self,
    musictype: MusicType | str | None,
    continuous: bool = False,
    mode: MusicPlayMode = MusicPlayMode.REGULAR,
    testsoundtrack: dict[str, Any] | None = None,
) -> None:
    """
    Function override for MusicSubsystem.do_play_music.
    The original function only checks for MusicType and ignores
    any extra enums. This modded function fixes that.
    """
    # We can be passed a MusicType or the string value corresponding
    # to one.
    import babase
    from baclassic._music import MusicType
    
    ### PCP MUSICTYPE PATCH
    # NOTE: If we can replace this segment without replacing
    #       the whole function, that would be really cool.
    if musictype is not None:
        # Check all MusicType enums.
        MusicTypes = [
            MusicType,
            MusicTypeBSE,
        ]
        done = False
        for mt in MusicTypes:
            try:
                # Fetch! (from our selected MusicType enum.)
                musictype = mt(musictype)
                # If we go thru, mark as done and dip.
                done = True
                break
            except ValueError:
                continue
        # If we didn't find anything, print our error thing.
        if not done:
            from traceback import print_stack
            print_stack(f"Invalid music type: '{musictype}'")
            musictype = None
    ### PCP MUSICTYPE PATCH
            
    with babase.ContextRef.empty():
        # If they don't want to restart music and we're already
        # playing what's requested, we're done.
        if continuous and self.music_types[mode] is musictype:
            return
        self.music_types[mode] = musictype
        # If the OS tells us there's currently music playing,
        # all our operations default to playing nothing.
        if babase.is_os_playing_music():
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
            
# Override our MusicSubsystem's do_play_music function with our patched one.
MusicSubsystem.do_play_music = patched_do_play_music

# Squeeze our MusicTypeBSE class into bascenev1.
import bascenev1 as bs
bs.MusicTypeBSE = MusicTypeBSE