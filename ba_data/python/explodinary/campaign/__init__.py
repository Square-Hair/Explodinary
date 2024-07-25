from __future__ import annotations

import math
import random
from enum import Enum, unique
from dataclasses import dataclass
from typing import TYPE_CHECKING

import ba
from ba import _map

from bastd.actor.spaz import Spaz
from bastd.actor.popuptext import PopupText
from bastd.actor.bomb import TNTSpawner
from bastd.actor.playerspaz import PlayerSpazHurtMessage
from bastd.actor.scoreboard import Scoreboard
from bastd.actor.powerupbox import PowerupBox, PowerupBoxFactory

from explodinary.custom.particle import bseVFX

from explodinary.actor.bsespazbot import (
    SpazBotDiedMessage,
    SpazBotSet,
)

if TYPE_CHECKING:
    from typing import Any, Sequence
    from explodinary.actor.bsespazbot import SpazBot
    
from explodinary.lib import dialogue, skipvote

### Main Activity module ###

@dataclass
class Wave:
    """A wave of enemies."""

    entries: list[Spawn | Spacing | Delay | None]
    base_angle: float = 0.0


@dataclass
class Spawn:
    """A bot spawn event in a wave."""

    bottype: type[SpazBot] | str
    point: Point | None = None
    spacing: float = 5.0


@dataclass
class Spacing:
    """Empty space in a wave."""

    spacing: float = 5.0


@dataclass
class Delay:
    """A delay between events in a wave."""

    duration: float


@unique
class Point(Enum):
    """Points on the map we can spawn at."""

    LEFT_UPPER_MORE         =   'bot_spawn_left_upper_more'
    LEFT_UPPER              =   'bot_spawn_left_upper'
    TURRET_TOP_RIGHT        =   'bot_spawn_turret_top_right'
    RIGHT_UPPER             =   'bot_spawn_right_upper'
    TURRET_TOP_MIDDLE_LEFT  =   'bot_spawn_turret_top_middle_left'
    TURRET_TOP_MIDDLE_RIGHT =   'bot_spawn_turret_top_middle_right'
    TURRET_TOP_LEFT         =   'bot_spawn_turret_top_left'
    TOP_RIGHT               =   'bot_spawn_top_right'
    TOP_LEFT                =   'bot_spawn_top_left'
    TOP                     =   'bot_spawn_top'
    BOTTOM                  =   'bot_spawn_bottom'
    LEFT                    =   'bot_spawn_left'
    RIGHT                   =   'bot_spawn_right'
    RIGHT_UPPER_MORE        =   'bot_spawn_right_upper_more'
    RIGHT_LOWER             =   'bot_spawn_right_lower'
    RIGHT_LOWER_MORE        =   'bot_spawn_right_lower_more'
    BOTTOM_RIGHT            =   'bot_spawn_bottom_right'
    BOTTOM_LEFT             =   'bot_spawn_bottom_left'
    TURRET_BOTTOM_RIGHT     =   'bot_spawn_turret_bottom_right'
    TURRET_BOTTOM_LEFT      =   'bot_spawn_turret_bottom_left'
    LEFT_LOWER              =   'bot_spawn_left_lower'
    LEFT_LOWER_MORE         =   'bot_spawn_left_lower_more'
    TURRET_TOP_MIDDLE       =   'bot_spawn_turret_top_middle'
    BOTTOM_HALF_RIGHT       =   'bot_spawn_bottom_half_right'
    BOTTOM_HALF_LEFT        =   'bot_spawn_bottom_half_left'
    TOP_HALF_RIGHT          =   'bot_spawn_top_half_right'
    TOP_HALF_LEFT           =   'bot_spawn_top_half_left'

class badgeColor(Enum):
    """ yea """
    neutral     =   [(0.1,0.33,0.5), (0.7,0.99,1.1)]
    completed   =   [(0.15,0.5,0.25), (0.2,0.9,0.3)]
    failed      =   [(0.5,0.11,0.15), (0.9,0.3,0.22)]

class Player(ba.Player['Team']):
    """Our player type for this game."""

    def __init__(self) -> None:
        self.has_been_hurt = False
        self.respawn_wave = 0
        self.hp_trail = -1
        self.shield_trail = -1

    """ Extra characteristics for our players. """

    def _set_spaz(self, spaz): self._spaz: Spaz = spaz
    def _a(self) -> BSECampaignActivity: return ba.getactivity()

    def vital(self, vitamin:bool = False):
        from bastd.actor.spaz import VITAL_PUNCH_COOLDOWN
        self._spaz._is_vital = True
        self._spaz._punch_cooldown = VITAL_PUNCH_COOLDOWN
        self._spaz.node.hurt = 0
        self._spaz._last_hit_time = None
        self._spaz._num_times_hit = 0

        if vitamin: self._a().handle_player_vitamin()
        else:       self._a().handle_player_vitalize()


class Team(ba.Team[Player]):
    """Our team type for this game."""

devmode = False

class BSECampaignActivity(ba.CoopGameActivity[Player, Team]):
    """ Template activity for our BSE Campaign levels. """

    name = 'BSE Campaign Level'
    description = ''

    tips: list[str | ba.GameTip] = []

    # Show messages when players die since it matters here.
    announce_player_deaths = True

    def __init__(self, settings: dict):

        # Fallbacks
        settings['map'] = settings.get('map', 'Blockland')
        settings['json'] = settings.get('json', False)

        super().__init__(settings)

        # Set our map defs in a fancier way
        get_from_json = settings.get('json', False)
        self._set_map_defs(map = settings['map'],
                           json = get_from_json)

        # Standard, shared stuff

        self._new_wave_sound = ba.getsound('scoreHit01')
        self._winsound = ba.getsound('score')
        self._cashregistersound = ba.getsound('cashRegister')
        self._a_player_has_been_hurt = False
        self._player_has_dropped_bomb = False

        self._scoreboard: Scoreboard | None = None
        self._game_over = False
        self._won = False
        self._wavenum = 0
        self._can_end_wave = True
        self._score = 0
        self._time_bonus = 0
        self._spawn_info_text: ba.NodeActor | None = None
        self._dingsound = ba.getsound('dingSmall')
        self._dingsoundhigh = ba.getsound('dingSmallHigh')
        self._have_tnt = False
        self._excluded_powerups: list[str] | None = None
        self._waves: list[Wave] = []
        self._tntspawner: TNTSpawner | None = None
        self._bots: SpazBotSet | None = None
        self._powerup_drop_timer: ba.Timer | None = None
        self._time_bonus_timer: ba.Timer | None = None
        self._time_bonus_text: ba.NodeActor | None = None
        self._flawless_bonus: int | None = None
        self._wave_text: ba.NodeActor | None = None
        self._wave_update_timer: ba.Timer | None = None
        self._throw_off_kills = 0
        self._land_mine_kills = 0
        self._tnt_kills = 0

        self._is_showing_tip: bool = False
        self._args: dict = {}
        self._track_damage: str | None = None

        self._badges: dict = {}
        self._badge_define()

        # Cutscene variables
        self._has_cutscene: bool = False
        self._end_game_after_waves: bool = True
        self._is_speedrunning: bool = False # ba.app.config.get('BSE: Speedrun Mode', False)
        
        # Extra level variables
        self._music = ba.MusicType.BEGINNING

        self._devmode = devmode

    def _badge_define(self):
        """ Empty function, vessel for badge appending. """

    def _set_map_defs(self,
                      map:str,
                      json:bool
                      ):
        defs: dict = {}
        if json:
            # Les go; get the current map and it's definitions
            mapdefs = _map.get_map_class(map).defs

            sspawn, espawn = [(mapdefs.points['ffa_spawn1'][0], mapdefs.points['ffa_spawn1'][1], mapdefs.points['ffa_spawn1'][2]),
                              (mapdefs.points['ffa_spawn1'][3], mapdefs.points['ffa_spawn1'][4], mapdefs.points['ffa_spawn1'][5]),
            ]
            spawn_center = (( sspawn[0] + espawn[0] ) / 2, ( sspawn[1] + espawn[1] ) / 2, ( sspawn[2] + espawn[2] ) / 2 )
            defs = {
                'spawn_center': spawn_center,
                'tntspawnpos': (0.0, 3.0, 2.1),
                'powerup_center': (0, 4, -1),
                'powerup_spread': (3, 2),
            }
        else:
            # If we don't use jsons, be lame and use static, clingy map defs
            defs = self._map_defs()

        self._spawn_center =    defs['spawn_center']
        self._tntspawnpos =     defs['tntspawnpos']
        self._powerup_center =  defs['powerup_center']
        self._powerup_spread =  defs['powerup_spread']
    
    def _map_defs(self) -> dict:
        """ Map defs in case we opt-out of getting defs from our json file. """
        """ NOTE: This should get 100% get replaced by the instancing activity if we don't opt in! """
        return {
            'spawn_center':     (-6, 2, -2),
            'tntspawnpos':      (0.0, 3.0, 2.1),
            'powerup_center':   (0, 4, -1),
            'powerup_spread':   (3, 2),
        }
    
    def on_transition_in(self) -> None:
        super().on_transition_in()
        customdata = ba.getsession().customdata

        self._spawn_info_text = ba.NodeActor(
            ba.newnode(
                'text',
                attrs={
                    'position': (15, -130),
                    'h_attach': 'left',
                    'v_attach': 'top',
                    'scale': 0.55,
                    'color': (0.3, 0.8, 0.3, 1.0),
                    'text': '',
                },
            )
        )

        self._scoreboard = Scoreboard(
            label=ba.Lstr(resource='scoreText'), score_split=0.5
        )

        self._cutscene_helpy: ba.Actor | None = None

    def on_begin(self, args: dict) -> None:
        self._args = args
        super().on_begin()

        # Arg. dependant variables.
        self._radial_spawn_y = args.get('radial_spawn_y', 2.3)
        self._level_goal_time = args.get('goal_time', '2m30s')

        # More general stuff.
        self.setup_low_life_warning_sound()
        self._update_scores()
        self._bots = SpazBotSet()

        self._level_timer: int = 0
        self._level_final_time: int = 0

        self._level_timer_freq: float = 0.001
        
        self._badge_nodes: dict = {}

        if self._badges.get('timetrial', None):
            k = 'explodinary.campaignBadge.speed.'
            strtime = self._args.get("goal_time", ba.Lstr(resource=f'{k}na'))
            
            self._badge_text('timetrial',
                             desc       = ba.Lstr(resource=f'{k}desc', subs=[('${TIME}', strtime)]),
                             short_desc = ba.Lstr(resource=f'{k}s_desc', subs=[('${TIME}', strtime)]),
                             )
            
        if self._track_damage:
            self._damage_received: int = 0
            self._damage_threshold = dmg = 300
            self._damage_threshold:int = int(((dmg*1.1)*len(self.players)) + (dmg*0.2))

            self._damage_tracking_timer = ba.Timer(0.001,
                                            lambda: self._track_player_hp(self._track_damage),
                                            repeat=True)
            
        # Extras
        self._bot_gaslight_timer: ba.Timer | None = None

        # Start up the level if there's not a cutscene in level.
        if not self._has_cutscene:
            self._start_spawning_stuff()
            self._render_badges()

    def _start_spawning_stuff(self,
                              initial_powerups: float = 0,
                              general_powerups: float = 4,
                              tnt: float = 0,
                              bots: float = 4,
                              force: bool = False):
        """ Starts up the level powerups, tnts and bots. 
            Not called when a cutscene is taking place. """
        args = self._args

        _do_powerups = args.get('powerups', True) or force
        _do_tnt = args.get('tnt', False) or force

        def v(var):
            return not type(var) == bool

        if _do_powerups:
            # Drop some powerups with the provided list by the referencing class
            if v(initial_powerups):
                ba.timer(initial_powerups, lambda: self._drop_powerups(standard_points  =  True,
                                                                       poweruptype      =  random.choice( args.get('first_spawn_type', [None]) )
                                                                       )
                )

            # Start dropping powerups after 4 seconds
            if v(general_powerups):
                ba.timer(general_powerups, self._start_powerup_drops)

        if _do_tnt and v(tnt): # Our TNT spawner (if applicable).
            ba.timer(tnt, self._spawn_tnt)
           
        if v(bots):
            ba.timer(bots, self._start_updating_waves)

    def _spawn_tnt(self):
        self._tntspawner = TNTSpawner(position=self._tntspawnpos)

    def _track_player_hp(self, badge: str = 'nodamage') -> None:
        from explodinary.campaign import Player
        from bastd.actor.spaz import Spaz

        if self._game_over:
            self._damage_tracking_timer = None
            if self._won and self._badge_status(badge):
                self._badge_update(badge, True)
            return
        
        for player in self.players:
            # Set our variables
            spaz: Spaz = player.actor

            # Add the asbolute difference between the last recorded hp with our current one
            self._damage_received += (abs(min(0, spaz.hitpoints - player.hp_trail))) # +
                                      # abs(min(0, spaz.shield_hitpoints or 0 - player.shield_trail)))
            
            if self._damage_received >= self._damage_threshold:
                # Oh no! Too much damage!
                if self._badge_status(badge):
                    self._badge_update(badge, False)
                
            # Save our current hp
            player.hp_trail = spaz.hitpoints

    def _badge_append(self,
                      iname     : ba.Lstr | str,
                      name      : ba.Lstr | str,
                      desc      : ba.Lstr | str,
                      short_desc: ba.Lstr | str,
                      icon      : str | ba.Texture,
                      default   : bool = False,
                      bonus     : int = 400) -> None:
        
        # Turn our icon string into a ba.Texture
        if type(icon) is str:
            icon = ba.gettexture(icon)
        
        self.__unused__ = [short_desc]
        
        self._badges[iname] = {
            'name': name,
            'desc': desc,
            'icon': icon,
            'success': default,
            'failure': False,
            'default': default,
            'bonus': bonus,
            'color': badgeColor.neutral.value,
        }

    def _render_badges(self) -> None:
        btotal = len(self._badges)
        bsx, bsy, padding = [444, 65, 5]
        icosize, txtscale = [(bsy * 0.85), (48.75/bsy)]
        bx, by = [0, (bsy+padding) * ((btotal-1)/2)]
        bym = lambda: (by - (bsy+padding))

        achOutTex = ba.gettexture('achievementOutline')
        achOutMod = ba.getmodel('achievementOutline')

        for i, badge in enumerate(self._badges):
            # Dict's values
            bval = self._badges[badge]

            bgc, bdc = bval['color']

            # Node stuff
            self._badge_nodes[badge] = {
                'bg': ba.newnode(
                    'image',
                    attrs={
                        'texture': ba.gettexture('badgeBack'),
                        'absolute_scale': True,
                        'vr_depth': 5,
                        'position': (bx, by),
                        'scale': (bsx, bsy),
                        'color': bgc,
                        'opacity': 0.6,
                        'attach': 'centerLeft',
                    },
                ),
                'badge': ba.newnode(
                    'image',
                    attrs={
                        'texture': bval['icon'],
                        'absolute_scale': True,
                        'vr_depth': 5,
                        'position': (bx + (bsy * 0.5), by),
                        'scale': (icosize, icosize),
                        'color': (1,1,1),
                        'opacity': 1,
                        'attach': 'centerLeft',
                    },
                ),
                'badge_outline': ba.newnode(
                    'image',
                    attrs={
                        'texture': achOutTex,
                        'model_transparent': achOutMod,
                        'absolute_scale': True,
                        'vr_depth': 5,
                        'position': (bx + (bsy * 0.5), by),
                        'scale': (icosize, icosize),
                        'color': bdc,
                        'opacity': 1,
                        'attach': 'centerLeft',
                    },
                ),
                'title': ba.newnode(
                    'text',
                    attrs={
                        'text': bval['name'],
                        'maxwidth': bsx * 0.6,
                        'position': (bx + (bsy * 1.025) , by + (bsy*0.72) -(bsy/2)),
                        'h_attach': 'left',
                        'h_align': 'left',
                        'v_attach': 'center',
                        'v_align': 'center',
                        'vr_depth': 10,
                        'color': (1.4,1.4,1.4),
                        'scale': txtscale,
                    }
                ),
                'desc': ba.newnode(
                    'text',
                    attrs={
                        'text': bval['desc'],
                        'maxwidth': bsx * 0.7,
                        'position': (bx + (bsy * 1.025) , by + (bsy*0.33) -(bsy/2)),
                        'h_attach': 'left',
                        'h_align': 'left',
                        'v_attach': 'center',
                        'v_align': 'center',
                        'vr_depth': 10,
                        'color': (1,1,1),
                        'scale': txtscale*0.65,
                    }
                ),
            }
            if bval['failure']:
                self._badge_nodes[badge]['badge'].color = (1,0.45,0.4)
            
            by = bym()

            self._badge_visibility(badge, 2 + (0.15*i))
            for key in self._badge_nodes[badge]:
                node = self._badge_nodes[badge][key]
                x, y = [node.position[0], node.position[1]]
                delay = 0.44 * i
                ba.animate_array(node, 'position', 2, {
                    0:                      (-bsy*4, y),
                    delay:                  (-bsy*4, y),
                    (1*0.66)+delay:         (x-bsy*1, y),
                    (1*0.77)+delay:         (x-bsy*0.5, y),
                    (1*0.9) +delay:         (x-bsy*0.212, y),
                    (1)     +delay:         (x, y),
                })

    def _badge_visibility(self,
                          badge: str,
                          time: float,
                          t_in: float = 0.5,
                          t_out: float = 0.5,
                          fopacity: float = 0.5) -> None:
        """ Changes the opacity of our badge display for a while. """
        # If we have no display, return
        try: self._badge_nodes[badge]
        except KeyError: return
        # Do this for each individual badge display piece
        for key in self._badge_nodes[badge]:
            node = self._badge_nodes[badge][key]
            ba.animate(node, 'opacity', {
                0:                  node.opacity,
                t_in:               1,
                t_in+time:          1,
                t_in+t_out+time:    fopacity,
            })
            
    def _badge_update(self,
                      badge: str,
                      status: bool = True,
                      passive: bool = False,
                      award: bool = True) -> None:
        """ Visually updates our badge status. """
        # This should succeed if this badge does exist.
        try:
            self._badges[badge]['success'] = status
            # Set our status failure if we are setting our status as False while not passively
            if not status and not passive:
                self._badges[badge]['failure'] = True
        except KeyError:
            raise Exception(f'This badge does not exist: {badge}')
        
        bgc, bdc = (badgeColor.neutral.value if passive else
                    badgeColor.completed.value if status else
                    badgeColor.failed.value)
                    
        try: 
            # Try doing this
            # If it fails, it means we have no display, and that's okay.
            self._badge_nodes[badge]
            ba.animate_array(self._badge_nodes[badge]['bg'], 'color', 3, {
                0: (1,1,1),
                0.77: bgc,
            })

            ba.animate_array(self._badge_nodes[badge]['badge_outline'], 'color', 3, {
                0: (1,1,1),
                0.77: bdc,
            })

            if not status:
                ba.animate_array(self._badge_nodes[badge]['badge'], 'color', 3, {
                    0: (1,1,1),
                    0.77: (1,0.45,0.4),
                })
        except KeyError: pass

        # Update our new color internally in case we don't have a display
        self._badges[badge]['color'] = (bgc, bdc)

        self._badge_visibility(badge, 1.75, 0.1, 1)
        if status and award: self._badge_award_bonus(badge)

    def _badge_award_bonus(self,
                           badge: str) -> None:
        try:
            bonus = self._badges[badge]
        except:
            raise Exception(f'This badge does not exist: {badge}')
        self._score += self._badges[badge]['bonus']
        self._update_scores()

    def _badge_text(self,
                    badge: str,
                    title: str | None = None,
                    desc: str | None = None,
                    short_desc: str | None = None,
                    update_internal: bool = True,
                    ) -> None:
        ''' Updates the badge's text display '''
        if not self._badges.get(badge, None):
            raise Exception(f'No badge found: "{badge}"')
        
        can_update = self._badge_nodes.get(badge, False)
        if title:
            if update_internal: self._badges[badge]['name']         = title  
            if can_update: self._badge_nodes[badge]['title'].text   = title  
        if desc:
            if update_internal: self._badges[badge]['desc']         = desc
            if can_update: self._badge_nodes[badge]['desc'].text    = desc
        #if short_desc and update_internal:
        #    self._badges[badge]['desc'] = short_desc

    def _badge_status(self,
                      badge: str) -> bool:
        if not self._badges.get(badge, None): return False
        return self._badges[badge].get('success', False)

    def _timer_compare(self) -> bool:
        """ Compares our goal time with the final time.
            Returns success depending of whether we beat the time or not.
        """
        g_time: str = self._level_goal_time
        mm,ss = g_time.split('m')
        ss = ss.replace('s','')

        mm,ss = [int(mm),int(ss)]
        final = int( ((mm*60) + ss)*(1/self._level_timer_freq) )

        won = self._level_final_time <= final

        if devmode: ba.screenmessage(f'DEVMESSAGE: {"Beat the time!" if won else "Took too long..."}\n{self._level_final_time} : {final}')
        return won

    def _timer_tick(self) -> None:
        """ Timer used for badges. """
        if ba.getactivity().globalsnode.paused: # Halt the timer when paused
            return
        
        elif self._game_over: # Stop timer when game ends
            self._level_timer_timer = None
            return 
        
        self._level_timer += 1
        t = self._level_timer
        m = 1 / self._level_timer_freq

        txt = (f'{"{:02d}:".format(int( (t//(m*60))%60 ))}'
               f'{"{:02d}:".format(int( (t//m)%60 ))     }'
               f'{"{:02d}".format(int( (t*(99/m)%99) ))  }')
        
        try: self._debug_timer_os.delete()
        except: pass
        
        self._debug_timer_os = ba.newnode(
            'text',
            attrs={
                'text': txt,
                'maxwidth': 200,
                'position': (0,75),
                'h_attach': 'center',
                'h_align': 'center',
                'v_attach': 'bottom',
                'vr_depth': 10,
                'color': (0.3,1.4,0.425,1.15),
                'shadow': 1.0,
                'flatness': 1.0,
                'scale': 1.1,
                'opacity':0.75,
            }
        )

    def _timer_win(self) -> None:
        ''' Called when game ends in victory. '''
        self._level_timer_timer = None
        self._level_final_time = self._level_timer
        self._badge_update('timetrial', self._timer_compare())
        self._respawn_players_for_wave()

    def _show_info(self) -> None:
        """ Custom info rendering. """
        showInfo = self._args.get('showInfo', False)

        if showInfo:
            super()._show_info()
        
        else: return

    def _show_scoreboard_info(self) -> None:
        """ Custom scoreboard text rendering. """
        showScoreboard = self._args.get('showScoreboard', True)

        if showScoreboard:
            title = self.get_instance_scoreboard_display_string()
            vrmode = ba.app.vr_mode

            from ba._nodeactor import NodeActor
            self._game_scoreboard_name_text = NodeActor(
                ba.newnode(
                    'text',
                    attrs={
                        'text': title,
                        'maxwidth': 300,
                        'position': (0,15),
                        'h_attach': 'center',
                        'h_align': 'center',
                        'v_attach': 'bottom',
                        'vr_depth': 10,
                        'color': (1.0, 1.0, 1.0, 1.0),
                        'shadow': 1.0 if vrmode else 0.6,
                        'flatness': 1.0 if vrmode else 0.5,
                        'scale': 1.1,
                    },
                )
            )
            ba.animate(self._game_scoreboard_name_text.node, 'opacity', {
                0:0,
                0.77:1,
            })

    def _show_tip(self) -> None:
        if not self.tips: return
        super()._show_tip()
        
        showScoreboard = self._args.get('showScoreboard', True)
        
        if showScoreboard:
            self._showing_tip(True)
            ba.timer(4.5, lambda: self._showing_tip(False))

    def _showing_tip(self, status: bool = True) -> None:
        self._is_showing_tip = status
        toedit: list = [self._game_scoreboard_name_text,
                        self._time_bonus_text,]
        for the in toedit:
            if the:
                ba.animate(the.node, 'opacity', {
                    0:the.node.opacity,
                    0.5:0.22 if status else 1,
                })


    def spawn_player(self, player: Player) -> ba.Actor:

        # We keep track of who got hurt each wave for score purposes.
        player.has_been_hurt = False
        pos = (
            self._spawn_center[0] + random.uniform(-0.5, 0.5),
            self._spawn_center[1],
            self._spawn_center[2] + random.uniform(-0.5, 0.5),
        )
        spaz = self.spawn_player_spaz(player, position=pos)
        spaz.add_dropped_bomb_callback(self._handle_player_dropped_bomb)
        return spaz

    def _handle_player_dropped_bomb(
        self, player: ba.Actor, bomb: ba.Actor
    ) -> None:
        del player, bomb  # Unused.
        self._player_has_dropped_bomb = True

    def _drop_powerup(self, index: int, poweruptype: str | None = None) -> None:
        poweruptype = PowerupBoxFactory.get().get_random_powerup_type(
            forcetype=poweruptype, excludetypes=self._excluded_powerups
        )
        PowerupBox(
            position=self.map.powerup_spawn_points[index],
            poweruptype=poweruptype,
        ).autoretain()

    def _start_powerup_drops(self) -> None:
        self._powerup_drop_timer = ba.Timer(
            3.0, ba.WeakCall(self._drop_powerups), repeat=True
        )

    def _drop_powerups(
        self, standard_points: bool = False, poweruptype: str | None = None
    ) -> None:
        """Generic powerup drop."""
        if standard_points:
            points = self.map.powerup_spawn_points
            for i in range(len(points)):
                ba.timer(
                    1.0 + i * 0.5,
                    ba.WeakCall(
                        self._drop_powerup, i, poweruptype if i == 0 else None
                    ),
                )
        else:
            point = (
                self._powerup_center[0]
                + random.uniform(
                    -1.0 * self._powerup_spread[0],
                    1.0 * self._powerup_spread[0],
                ),
                self._powerup_center[1],
                self._powerup_center[2]
                + random.uniform(
                    -self._powerup_spread[1], self._powerup_spread[1]
                ),
            )

            # Drop one random one somewhere.
            PowerupBox(
                position=point,
                poweruptype=PowerupBoxFactory.get().get_random_powerup_type(
                    excludetypes=self._excluded_powerups
                ),
            ).autoretain()

    def do_end(self, outcome: str, delay: float = 0.0) -> None:
        """End the game with the specified outcome."""
        if outcome == 'defeat':
            self.fade_to_red()
        score: int | None
        if self._wavenum >= 2:
            score = self._score
            fail_message = None
        else:
            score = None
            fail_message = ba.Lstr(resource='reachWave2Text')
        self.end(
            {
                'outcome': outcome,
                'score': score,
                'fail_message': fail_message,
                'playerinfos': self.initialplayerinfos,
            },
            delay=delay,
        )

    def _award_completion_achievements(self) -> None:
        return 'unset'

    def _update_waves(self) -> None:

        # If we have no living bots, go to the next wave.
        assert self._bots is not None
        if (
            self._can_end_wave
            and not self._bots.have_living_bots()
            and not self._game_over
        ):
            self._can_end_wave = False
            self._time_bonus_timer = None
            self._time_bonus_text = None
            won = self._wavenum == len(self._waves)

            base_delay = 2.0 if (won and self._end_game_after_waves) else 0.0

            # Reward time bonus.
            if self._time_bonus > 0:
                ba.timer(0, lambda: ba.playsound(self._cashregistersound))
                ba.timer(
                    base_delay,
                    ba.WeakCall(self._award_time_bonus, self._time_bonus),
                )
                base_delay += 1.0

            # Reward flawless bonus.
            if self._wavenum > 0:
                have_flawless = False
                for player in self.players:
                    if player.is_alive() and not player.has_been_hurt:
                        have_flawless = True
                        ba.timer(
                            base_delay,
                            ba.WeakCall(self._award_flawless_bonus, player),
                        )
                    player.has_been_hurt = False  # reset
                if have_flawless:
                    base_delay += 1.0

            if won:
                if self._end_game_after_waves:
                    self._timer_win() # Timer check!! Yippie!
                    self.show_zoom_message(
                        ba.Lstr(resource='victoryText'), scale=1.0, duration=4.0
                    )
                    self.celebrate(20.0)
                    self._award_completion_achievements()
                    ba.timer(base_delay, ba.WeakCall(self._award_completion_bonus))
                    base_delay += 0.85
                    ba.playsound(self._winsound)

                    ba.cameraflash()
                    ba.setmusic(ba.MusicType.VICTORY)

                    self._do_all_respawn()

                    self._game_over = self._won = True

                    # Can't just pass delay to do_end because our extra bonuses
                    # haven't been added yet (once we call do_end the score
                    # gets locked in).
                    ba.timer(base_delay, ba.WeakCall(self.do_end, 'victory'))
                else:
                    ba.timer(base_delay, self._alternate_end)
                return

            self._wavenum += 1

            # Short celebration after waves.
            if self._wavenum > 1:
                self.celebrate(0.5)
            ba.timer(base_delay, ba.WeakCall(self._start_next_wave))

    def _alternate_end(self):
        """ Alternate end if we don't end our game after waves. """
        ba.screenmessage('Alternate end remains untouched!', (1,0.2,0.2))
        ba.playsound(ba.getsound('error'))

    def _award_completion_bonus(self) -> None:
        ba.playsound(self._cashregistersound)
        for player in self.players:
            try:
                if player.is_alive():
                    assert self.initialplayerinfos is not None
                    self.stats.player_scored(
                        player,
                        int(100 / len(self.initialplayerinfos)),
                        scale=1.4,
                        color=(0.6, 0.6, 1.0, 1.0),
                        title=ba.Lstr(resource='completionBonusText'),
                        screenmessage=False,
                    )
            except Exception:
                ba.print_exception()

    def _award_time_bonus(self, bonus: int) -> None:
        ba.playsound(self._cashregistersound)
        PopupText(
            ba.Lstr(
                value='+${A} ${B}',
                subs=[
                    ('${A}', str(bonus)),
                    ('${B}', ba.Lstr(resource='timeBonusText')),
                ],
            ),
            color=(1, 1, 0.5, 1),
            scale=1.0,
            position=(0, 3, -1),
        ).autoretain()
        self._score += self._time_bonus
        self._update_scores()

    def _award_flawless_bonus(self, player: Player) -> None:
        ba.playsound(self._cashregistersound)
        try:
            if player.is_alive():
                assert self._flawless_bonus is not None
                self.stats.player_scored(
                    player,
                    self._flawless_bonus,
                    scale=1.2,
                    color=(0.6, 1.0, 0.6, 1.0),
                    title=ba.Lstr(resource='flawlessWaveText'),
                    screenmessage=False,
                )
        except Exception:
            ba.print_exception()

    def _start_time_bonus_timer(self) -> None:
        self._time_bonus_timer = ba.Timer(
            1.0, ba.WeakCall(self._update_time_bonus), repeat=True
        )

    def _update_player_spawn_info(self) -> None:

        # If we have no living players lets just blank this.
        assert self._spawn_info_text is not None
        assert self._spawn_info_text.node
        if not any(player.is_alive() for player in self.teams[0].players):
            self._spawn_info_text.node.text = ''
        else:
            text: str | ba.Lstr = ''
            for player in self.players:
                if not player.is_alive() and player.respawn_wave <= len(self._waves):
                    rtxt = ba.Lstr(
                        resource='explodinary.onslaughtRespawnNextText',
                        subs=[
                            ('${PLAYER}', player.getname()),
                        ],
                    )
                    text = ba.Lstr(
                        value='${A}${B}\n',
                        subs=[
                            ('${A}', text),
                            ('${B}', rtxt),
                        ],
                    )
            self._spawn_info_text.node.text = text

    def _respawn_players_for_wave(self) -> None:
        # Respawn applicable players.
        if self._wavenum > 1 and not self.is_waiting_for_continue():
            for player in self.players:
                if (
                    not player.is_alive()
                    and player.respawn_wave == self._wavenum
                ):
                    self.spawn_player(player)
        self._update_player_spawn_info()

    def _do_all_respawn(self) -> None:
        for player in self.players:
            if not player.is_alive():
                self.spawn_player(player)

    def _setup_wave_spawns(self, wave: Wave) -> None:
        tval = 0.0
        dtime = 0.2
        if self._wavenum == 1:
            spawn_time = 3.973
            tval += 0.5
        else:
            spawn_time = 2.648

        bot_angle = wave.base_angle
        self._time_bonus = 0
        self._flawless_bonus = 0
        for info in wave.entries:
            if info is None:
                continue
            if isinstance(info, Delay):
                spawn_time += info.duration
                continue
            if isinstance(info, Spacing):
                bot_angle += info.spacing
                continue
            bot_type_2 = info.bottype
            if bot_type_2 is not None:
                assert not isinstance(bot_type_2, str)
                self._time_bonus += bot_type_2.points_mult * 20
                self._flawless_bonus += bot_type_2.points_mult * 5

            # If its got a position, use that.
            point = info.point
            if point is not None:
                assert bot_type_2 is not None
                spcall = ba.WeakCall(
                    self.add_bot_at_point, point, bot_type_2, spawn_time
                )
                ba.timer(tval, spcall)
                tval += dtime
            else:
                spacing = info.spacing
                bot_angle += spacing * 0.5
                if bot_type_2 is not None:
                    tcall = ba.WeakCall(
                        self.add_bot_at_angle, bot_angle, bot_type_2, spawn_time
                    )
                    ba.timer(tval, tcall)
                    tval += dtime
                bot_angle += spacing * 0.5

        # We can end the wave after all the spawning happens.
        ba.timer(
            tval + spawn_time - dtime + 0.01,
            ba.WeakCall(self._set_can_end_wave),
        )

    def _start_next_wave(self) -> None:

        # This can happen if we beat a wave as we die.
        # We don't wanna respawn players and whatnot if this happens.
        if self._game_over:
            return

        self._respawn_players_for_wave()
        wave = self._waves[self._wavenum - 1]
        self._setup_wave_spawns(wave)
        self._update_wave_ui_and_bonuses()

    def _update_wave_ui_and_bonuses(self) -> None:

        # Reset our time bonus.
        tbtcolor = (0.3, 1.1, 0.4, 1)
        tbttxt = ba.Lstr(
            value='${A}: ${B}',
            subs=[
                ('${A}', ba.Lstr(resource='timeBonusText')),
                ('${B}', str(self._time_bonus)),
            ],
        )
        self._time_bonus_text = ba.NodeActor(
            ba.newnode(
                'text',
                attrs={
                    'v_attach': 'bottom',
                    'h_attach': 'center',
                    'h_align': 'center',
                    'vr_depth': -30,
                    'color': tbtcolor,
                    'shadow': 1.0,
                    'flatness': 1.0,
                    'position': (0, 45),
                    'scale': 0.8,
                    'text': tbttxt,
                    'opacity': 0.22 if self._is_showing_tip else 1,
                },
            )
        )

        ba.timer(5.0, ba.WeakCall(self._start_time_bonus_timer))

    def add_bot_at_point(
        self, point: Point, spaz_type: type[SpazBot], spawn_time: float = 1.0
    ) -> None:
        """Add a new bot at a specified named point."""
        if self._game_over:
            return
        assert isinstance(point.value, str)
        pointpos = self.map.defs.points[point.value]
        assert self._bots is not None
        self._bots.spawn_bot(spaz_type, pos=pointpos, spawn_time=spawn_time)

    def add_bot_at_angle(
        self, angle: float, spaz_type: type[SpazBot], spawn_time: float = 1.0
    ) -> None:
        """Add a new bot at a specified angle (for circular maps)."""
        if self._game_over:
            return
        angle_radians = angle / 57.2957795
        xval = math.sin(angle_radians) * 1.06
        zval = math.cos(angle_radians) * 1.06
        point = (xval / 0.125, self._radial_spawn_y, (zval / 0.2) - 3.7)
        assert self._bots is not None
        self._bots.spawn_bot(spaz_type, pos=point, spawn_time=spawn_time)

    def _update_time_bonus(self) -> None:
        self._time_bonus = int(self._time_bonus * 0.93)
        if self._time_bonus > 0 and self._time_bonus_text is not None:
            assert self._time_bonus_text.node
            self._time_bonus_text.node.text = ba.Lstr(
                value='${A}: ${B}',
                subs=[
                    ('${A}', ba.Lstr(resource='timeBonusText')),
                    ('${B}', str(self._time_bonus)),
                ],
            )
        else:
            self._time_bonus_text = None

    def _start_updating_waves(self) -> None:
        self._wave_update_timer = ba.Timer(
            0.22, ba.WeakCall(self._update_waves), repeat=True
        )

        if not self._has_cutscene:
            ba.timer(4.5, self._start_badge_timer)
            
    def _start_badge_timer(self) -> None:
        self._level_timer_timer: ba.Timer | None = ba.Timer(self._level_timer_freq,
                                                            self._timer_tick,
                                                            repeat=True,
                                                            timetype=ba.TimeType.BASE)

    def _update_scores(self) -> None:
        score = self._score
        assert self._scoreboard is not None
        self._scoreboard.set_team_value(self.teams[0], score, max_score=None)

    def handlemessage(self, msg: Any) -> Any:

        if isinstance(msg, PlayerSpazHurtMessage):
            msg.spaz.getplayer(Player, True).has_been_hurt = True
            self._a_player_has_been_hurt = True

        elif isinstance(msg, ba.PlayerScoredMessage):
            self._score += msg.score
            self._update_scores()

        elif isinstance(msg, ba.PlayerDiedMessage):
            super().handlemessage(msg)  # Augment standard behavior.
            player = msg.getplayer(Player)
            if self._won: # Respawn immediately if we already won!
                self.spawn_player(player)
            else:
                self._a_player_has_been_hurt = True

                # Make note with the player when they can respawn:
                player.respawn_wave = max(2, self._wavenum + 1)

                ba.timer(0.1, self._update_player_spawn_info)
                ba.timer(0.1, self._checkroundover)

        elif isinstance(msg, SpazBotDiedMessage):
            pts, importance = msg.spazbot.get_death_points(msg.how)
            self._handle_kill_achievements(msg)
            if msg.killerplayer is not None:
                target: Sequence[float] | None
                if msg.spazbot.node:
                    target = msg.spazbot.node.position
                else:
                    target = None

                killerplayer = msg.killerplayer
                self.stats.player_scored(
                    killerplayer,
                    pts,
                    target=target,
                    kill=True,
                    screenmessage=False,
                    importance=importance,
                )
                ba.playsound(
                    self._dingsound if importance == 1 else self._dingsoundhigh,
                    volume=0.6,
                )

            # Normally we pull scores from the score-set, but if there's
            # no player lets be explicit.
            else:
                self._score += pts
            self._update_scores()
        else:
            super().handlemessage(msg)

    def _handle_kill_achievements(self, msg: SpazBotDiedMessage): return

    def _set_can_end_wave(self) -> None: self._can_end_wave = True

    def end_game(self) -> None:
        # Tell our bots to celebrate just to rub it in.
        assert self._bots is not None
        self._bots.final_celebrate()
        self._game_over = True
        self.do_end('defeat', delay=2.0)
        ba.setmusic(None)

    def on_continue(self) -> None:
        for player in self.players:
            if not player.is_alive():
                self.spawn_player(player)

    def _checkroundover(self) -> None:
        """Potentially end the round based on the state of the game."""
        if self.has_ended():
            return
        if not any(player.is_alive() for player in self.teams[0].players):
            # Allow continuing after wave 1.
            if self._wavenum > 1:
                self.continue_or_end_game()
            else:
                self.end_game()

    def handle_player_vitalize(self): return 'unset'    # Should be overwritten
    def handle_player_vitamin(self): return 'unset'     # Should be overwritten

    def fade_to_red(self) -> None:
        """ We ain't fading to red anymore! """
        from ba import _gameutils

        c_existing = self.globalsnode.tint
        cnode = ba.newnode(
            'combine',
            attrs={
                'input0': c_existing[0],
                'input1': c_existing[1],
                'input2': c_existing[2],
                'size': 3,
            },
        )
        _gameutils.animate(cnode, 'input0', {0: c_existing[0], 2.0: 0.45})
        _gameutils.animate(cnode, 'input1', {0: c_existing[1], 2.0: 0.45})
        _gameutils.animate(cnode, 'input2', {0: c_existing[2], 2.0: 1.25})
        cnode.connectattr('output', self.globalsnode, 'tint')
        
    ### Cool explo. stuff
    
    def _do_intro_cutscene(self):
        """ Does our level intro.
            Should get overwritten by our level instance. """
    def _do_end_cutscene(self, outcome: str):
        """ Does our end level cutscene.
            Should get overwritten by our level instance. """
    def alt_do_end(self, outcome: str): BSECampaignActivity.do_end(self, outcome)
            
    def _dumb_bot_spawn(self, delay: float = 0):
        """ Delays and spawns bot with their AI disabled. """
        self._dumbify()
        self._start_spawning_stuff(False, False, False, delay)
        
    def _dumbify(self, enable = False):
        """ Disables bots' AI temporarily. """
        self._time_bonus_timer = None
        # Are we *enabling* their AI?
        if enable: self._bots.start_moving()
        else: self._bots.stop_moving()
            
    def _intro_cutscene_end(self,
                            instant = False):
        """ Wraps up our intro cutscene """
        # De-focus Helpy in case we can
        try: self._cutscene_helpy.node.is_area_of_interest = False
        except: pass
        # Stop bot AI gaslighting
        self._bot_gaslight_timer = None
        self._bots.start_moving()
        # Handle stuff spawning and badge timer if instant (aka. not playing a cutscene.)
        if instant:
            self._start_spawning_stuff()
            ba.timer(8.5, self._start_badge_timer)
        else:
            self._start_badge_timer()
            
        # Re-enable player's controllers
        self._handle_controllers(True)
        
        # Set our music!
        ba.setmusic(self._music)
        # Some other stuff
        ba.timer(0.22, ba.Call(self._dumbify, True))
        ba.timer(0.77, self._end_wrapup)
        
    def _end_wrapup(self):
        """ Does a post-end intro tip / timer management. """
        # Show once per session only.
        # cd = ba.getsession().customdata
        # if not cd.get('tip_tm', False):
            # cd['tip_tb'] = True
            # self.tips = [
                # ba.GameTip(
                    # 'Use Cluster Bombs to cover a large area\n'
                    # 'with clusters quickly.',
                    # icon=ba.gettexture('powerupClusterBombs'),
                    # sound=ba.getsound('ding'),
                # )
            # ]
        ba.timer(3, ba.WeakCall(self._start_time_bonus_timer))
        ba.timer(0.8, self._show_tip)
        ba.timer(0.2, self._render_badges)


    def has_done_cutscene(self, key: str = 'default', check: bool = True) -> bool:
        """ Checks if we've already shown this cutscene.
            Mark as True if we haven't. """
        cd = ba.getsession().customdata

        cutscene_key = f'{key}_cutscene'
        if (
            not self._is_speedrunning and
            not cd.get(cutscene_key, False) and
            not ba.app.config.get('BSE: Skip Cutscenes', False)
            ):
            if check: cd[cutscene_key] = True
            return False
        
        return True

    def _handle_controllers(self, connect: bool):
        """ Connects / disconnects every player's controllers. """
        for player in self.players:
            if player.actor is not None:
                try:
                    if connect: player.actor.connect_controls_to_player()
                    else: player.actor.disconnect_controls_from_player()
                except: raise Exception(f'Can\'t handle controllers for "{str(player)}". (connect: {connect})')

    def spawn_helpy(self,
                    pos: tuple,
                    particle: bool = False):
        """ Spawns Helpy. """
        from bastd.actor.spaz import Spaz
        from bastd.actor.spazappearance import Appearance
        helpy_a: Appearance = ba.app.spaz_appearances.get('Helpy')

        helpy = self._cutscene_helpy = Spaz(helpy_a.default_color,
                                            helpy_a.default_highlight,
                                            'Helpy', None, False, False, False, True)
        helpy.handlemessage(ba.StandMessage(pos))
        if particle: bseVFX('gone_puff', self._cutscene_helpy.node.position, self._cutscene_helpy.node.velocity)
        helpy.impact_scale = 0
        helpy.can_freeze = False
        helpy.can_pickup = False
        helpy.can_be_poisoned = False

    def badoink_helpy(self):
        """ Helpy DIES. """
        try:
            bseVFX('gone_puff', self._cutscene_helpy.node.position, self._cutscene_helpy.node.velocity)
            self._cutscene_helpy.node.handlemessage(ba.DieMessage(how=ba.DeathType.GENERIC))
            self._cutscene_helpy.node.delete()
            self._helpy_stand = None
        except: pass

    def hold_pos_helpy(self):
        """ Teleports Helpy to the location he's in the moment this function is called """
        self._helpy_stand = ba.Timer(0.05, ba.Call(self._stand_helpy, self._cutscene_helpy.node.position), repeat=True)

    def release_pos_helpy(self): self._helpy_stand = None

    def _stand_helpy(self, pos):
        try:
            h,p,s = (self._cutscene_helpy, self._cutscene_helpy.node.position, pos)
            for i,x in enumerate(p):
                if p[i] < s[i]-0.25 or p[i] > s[i]+0.25:
                    h.handlemessage(ba.StandMessage((s[0], s[1]-1, s[2])))
        except: return None

    def helpy_move(self,
                  x: float = 0.0,
                  y: float = 0.0,
                  run: bool = False,
                  jump: bool = False):
        """ Moves helpy. """
        self._cutscene_helpy.on_move_left_right(x)
        self._cutscene_helpy.on_move_up_down(y)
        self._cutscene_helpy.on_run(1.5 if run else 1)
        if jump:
            self._cutscene_helpy.on_jump_press()
            self._cutscene_helpy.on_jump_release()
            
    def reset(self):
        """ Resets the activity. """
        self.end({'outcome':'restart'})