from  __future__ import annotations

import random
from typing import Any
from dataclasses import dataclass

import ba
from ba import TimeType
from explodinary import campaign as bsec
from bastd.actor.zoomtext import ZoomText

Music = {
    'VS': [
        ba.MusicType.CHAOS_SWEET,
        ba.MusicType.CHAOS_PIZZA,
        ba.MusicType.CHAOS_PINEAPPLE,
        ba.MusicType.CHAOS_OREGANO,
        ba.MusicType.CHAOS_LASAGNA,
    ],
    'Coop': [
        ba.MusicType.CHAOS_SUGARCUBE,
        ba.MusicType.CHAOS_CHILI,
    ]
}

from explodinary.lib import bseconfig

Events = {
    'normal':   [], # For your average event.
    'special':  [], # Bigger, more intense events. (Unused for now)
    'manager':  [], # Events to switch up ChaosManager.
    'force':    [], # Dev-only: Ignores all other events and runs the ones in this list.
}

GameBlacklist = [
    bsec.the_beginning.TheBeginningGame,
    bsec.mysterious_swamp.MysteriousSwampGame,
    bsec.beyond_the_grotto.GrottoGame,
    bsec.alpine_gateway.AlpineGatewayGame,
    bsec.mount_chill.MountChillGame,
    bsec.hot_air_havoc.HotAirHavocGame,
    bsec.blockland.BlocklandGame,
    bsec.confrontation.ConfrontationGame,
    bsec.bomb_poem.BombPoemGame,
]

from bastd.game.easteregghunt import EasterEggHuntGame

@dataclass
class TickMessage:
    """ Message
        Sent when an in-game tick occurs. """

@dataclass
class UpdateMessage:
    """ Message
        Sent when our manager has a code update. """

class ChaosEvent:
    """ Baseplate class for Chaos events. """
    name = 'Chaos Event Name'
    icon = 'empty'
    event_type = 'normal'
    
    # Event will be dismissed if current activity / session matches an element in the list.
    # (You might want to do some importing beforehand for this.)
    blacklist = []
    
    def __init__(
        self,
        manager: ChaosManager
    ):
        """"""
        self.icon = self._chk_icon(self.icon)
        self.activity = ba.getactivity()
        self.session = ba.getsession()
        self.manager = manager
        
        self._is_coop = type(self.session) is ba.CoopSession

    def _chk_icon(self, t) -> ba.Texture:
        if type(t) is str:
            # Set to empty texture if unspecified or requested.
            if t.lower() in ['','none','null']:
                t = 'empty'
            t = ba.gettexture(t)
        elif not type(t) is ba.Texture:
            print(f'Not a ba.Texture nor string: "{t}". Defaulted to "empty".')
            t = ba.gettexture('empty')
        return t
    
    def _get_players(self) -> list:
        """ Returns a list of players. """
        players = self.activity.players; playerlist: list = []
        
        for x in players:
            if x.actor: playerlist.append(x.actor)
        
        return playerlist
        
    def _get_bots(self) -> list:
        """ Retuns a list of bots. """
        if not self._is_coop: return []
        
        # Modes like meteor shower can be co-op and not have a bot list, be ready for that
        try: self.activity._bots
        except AttributeError: return []
        
        self.activity._bots._update()
        bots = self.activity._bots._bot_lists
        
        if bots:
            botlist: list = []
            for x in bots:
                if x and x[0]: botlist.append(x[0]) # If there's no bots, the bot list is just "[]", prevent adding that
        
        return botlist
    
    def _get_everyone(self) -> list:
        """ Returns a list with both players and bots (if existing). """
        plist, blist, alist = self._get_players(), self._get_bots(), []
        
        for x in plist: alist.append(x)
        for x in blist: alist.append(x)
        
        return alist
    
    def _get_config(self) -> dict:
        """ Retuns a dict with the current chaos settings. """
        return ba.getactivity()._chaos_config
    
    def _get_variable_list(self) -> dict:
        """ Retuns a dict with the current chaos variables. """
        return ba.getactivity()._chaos_variables
    
    def _get_variable(self, var: str, fallback: Any = None) -> Any:
        """ Gets a variable from our chaos variables list.
            Creates it if it doesn't exist. """
        return self._get_variable_list().setdefault(var, fallback)
            
    def _set_variable(self, var: str, val: Any) -> Any:
        """ Sets a chaos list variable. """
        self._get_variable_list()[var] = val
    
    def event(self):
        """ The event itself. """
        
def append_chaos_event(event: ChaosEvent):
    """ Adds Chaos Event to the indicated pool list. """
    try:
        Events[str.lower(event.event_type)].append(event)
    except KeyError:
        raise Exception(f'- ChaosAppend | {event.name} -\nEvent type does not exist: "{event.event_type}"\nMake sure it\'s either "Normal", "Special" or "Manager".')

class ChaosManager:
    """ Main handler for all Chaos. """
    def __init__(
        self,
        activity,
    ):
        self.activity = activity
        self.session = ba.getsession()
        
        # Sounds list
        self.orchestra_sounds = [
            'orchestraHit3',
            'orchestraHit2',
            'orchestraHit',
        ]
        
        # Load config. values
        c = ba.app.config
        self.config = activity._chaos_config = {
            'time'      : bseconfig.chaos_get('Time'),
            'timer_show': bseconfig.chaos_get('Time_show'),
            'timer_pos' : bseconfig.chaos_get('Time_pos'),
            'list_show' : bseconfig.chaos_get('Event_show'),
            'list_len'  : bseconfig.chaos_get('Event_len'),
            'list_pos'  : bseconfig.chaos_get('Event_pos'),
            'doAnnounce': bseconfig.chaos_get('DoAnnounce'),
            'doSound'   : bseconfig.chaos_get('DoSound'),
            'doMusic'   : bseconfig.chaos_get('DoMusic'),
        }
        
        activity._chaos_variables = {}
        
        self.base_time = btmr = 1
        self.time_rate = mult = 30                      # Operation time multiplier
        self.chaos = {
            'max'       : self.config['time'] * mult,   # Time of each cycle
            'time'      : self.config['time'] * mult,   # Current cycle's time
            'ldt'       : str(self.config['time']),     # Last Display Time        
            'itr'       : 0,                            # Current Event iteration
            'special'   : 0,                            # Special Event counter
            'manager'   : 0,                            # Manager Event counter
        }
        
        # Load and store display elements if required
        self._dtimer = None if not self.config['timer_show'] else ChaosDisplayTimer(self, self.activity)
        self.update_timer()
        
        self._devent = None if not self.config['list_show'] else ChaosDisplayList(self.activity)
        
        # Change music
        if self.config['doMusic']: self._switch_music()
        
        # Create some timers to keep track of things
        activity._chaos = {}
        activity._chaos['update_time']      = ba.Timer(btmr/mult,
                                                       self._update,
                                                       timetype=TimeType.BASE,
                                                       repeat=True)
        
        activity._chaos['tick_time']        = ba.Timer(0.001,
                                                       self._tick,
                                                       repeat=True)
        
        self._update_time                   = [activity._chaos['update_time']]
        self._tick_time                     = [activity._chaos['tick_time']]

    def _switch_music(self):
        """ Changes the game's music. """
        from explodinary.game import pathwayPandemonium
        
        if type(self.activity) is pathwayPandemonium.PathwayPandemoniumGame: return
        
        key = 'Coop' if (
            type(self.session) is ba.CoopSession
            ) else 'VS'
        
        ba.setmusic( random.choice( Music[key] ) )
        
    def _update(self):
        """ Runs every 1/mult update. """
        # Tick down our internal timer unless the game is paused.
        if not self.activity.globalsnode.paused:
            self.time_down()
        
    def time_down(self):
        """ Handle time passing of our internal timer, along other stuff. """
        t = self.chaos['time']
        
        if not (t-1) <= 0:
            self.chaos['time'] = (t-1)
        else:
            # Run an event whenever our timer reaches 0!
            self.chaos['time'] = self.chaos['max']
            self.pre_do_event()
                    
    def _tick(self):
        """ Runs every in-game tick. """
        # Update the display timer whenever our last display time doesn't match our current display time
        dt = self.get_time()
        
        if self.chaos['ldt'] != dt:
            self.update_timer()
            self.chaos['ldt'] = dt
    
    def get_time(self) -> int:
        """ Returns current countdown time as a readable integer. """
        return int(min(self.chaos['max'] / self.time_rate, (self.chaos['time'] / self.time_rate) + 1))
    
    def update_timer(self):
        """ Updates the timer text and plays sounds if allowed. """
        t = self.get_time()
        # Update our display timer if we have it
        if self._dtimer:
            self._dtimer._trace_timer(t)
        
        if self.config['doSound']: self._play_sounds(t)
        
    def _play_sounds(self, t: int):
        """ Handles playing ticks / orchestra hit sounds on countdown. """
        sct = self.config['time']; v = (1.4/sct) * (sct / t)
        ba.playsound(
            ba.getsound('tick'),
            volume=v
        )
        if t <= 3: ba.playsound(ba.getsound(self.orchestra_sounds[t-1]))
        
    def pre_do_event(self):
        """ Chooses what event should be peformed. """
        # Do standard countdown
        itrn = self.chaos['itr']     = self.chaos['itr']     + 1
        itrs = self.chaos['special'] = self.chaos['special'] + 1
        itrm = self.chaos['manager'] = self.chaos['manager'] + 1
        
        pool = 'normal'
        
        # Force an event if possible
        if len(Events['force']) > 0:
            pool = 'force'
        # Run a manager event from 6 to 12 events
        elif itrm >= random.randint(6,12):
            self.chaos['manager'] = 0
            pool = 'manager'
            
        self.do_event(pool = pool)
        
    def do_event(self,
                 itr = 0,
                 pool = 'normal',
                 data_override = {}):
        """ Gets and runs an event. """
        # Prevent an infinite loop if we've gone through 20 iterations already (Not really necessary as python already prevents this but it generates a lagspike so...)
        if itr > 14:
            raise Exception(f'Found ourselves on an infinite loop and reached iteration "{itr}"\nMake sure you appended your events right, Temp. -Temp')
        
        forced_ev = pool == 'force'
        
        event: ChaosEvent = random.choice(Events[pool])(self)
        bl = event.blacklist
        
        # Reroll event if we're blacklisted
        if type(self.activity) in bl or (type(self.session)) in bl:
            self.do_event(
                itr = itr+1,
                pool = pool,
                data_override = data_override,
            )
            return
        # Do event! if everything runs good, continue. Or else, reroll!
        try: event_output = event.event()
        except Exception as x:
            # If an error occurs, reroll the event to compensate (and print the error afterwards)
            if not forced_ev:
                self.do_event(
                    itr = itr+1,
                    pool = pool,
                    data_override = data_override,
                )
            raise Exception(x)
        
        # Baseplate for output variables
        output = {
            'time': 0,
            'timetype': ba.TimeType.SIM,
            'announce': True,
            'delay': 0
        }
        
        # If the event manually returns as "False", something went wrong and we want to reroll
        if event_output is False:
            self.do_event(
                    itr = itr+1,
                    pool = pool,
                    data_override = data_override,
                )
            return
        
        # If we get a dict, handle variables given
        elif type(event_output) is dict:
            for key in event_output.keys():
                output[key] = event_output[key]
        # If we get a number, it's most likely time, so let's handle it as such
        elif type(event_output) in [float, int]:
            output['time'] = event_output
            
        # If we have a data override (like in the case of an event referencing another event), prioritize those
        for k, v in data_override.items():
            output[k] = v
            
        # If we're allowed to announce and the event allows announcing, annouce! What a shocker
        if output['announce']:
            # Do our visual announcement if allowed
            if self.config['doAnnounce']:
                ba.timer(output['delay']+0.001, ba.Call( self.announce_event, event.name ))
            # Add it to our event list display if visible
            if self.config['list_show'] and self._devent:
                ba.timer(output['delay']+0.001, ba.Call( self._devent.add_event, event.name, event.icon, (output['time'], output['timetype']) ))
        
    def announce_event(self, eventname: str):
        """ Displays a ZoomText showing our event's name. """
        ba.timer(0.25, lambda: ba.playsound(ba.getsound('scoreHit01')))
        
        ZoomText(
            ba.Lstr(translate=('chaosEventNames', eventname)),
            lifespan=1.25,
            jitter=2.0,
            position=(0, -230 - 1 * 20),
            scale=0.5,
            maxwidth=800,
            trail=True,
            color=(0.7,1.1,0.95),
        ).autoretain()
                    
class ChaosDisplayTimer:
    """ Countdown timer for Chaos events.
        Purely visual; handled by ChaosManager. """
    def __init__(
        self,
        manager,
        activity,
    ):
        self.activity = activity
        self.config = activity._chaos_config
        
        self.defaults = {
            'color'     : (1,1,1,1),
            'opacity'   : 0.5,
            'scale'     : 1.5,
        }
        
        y = 90 if self.config['timer_pos'] == 'bottom' else -90
        self.activity._chaos_dtimer = (
            ba.newnode(
                'text',
                attrs={
                    'text': '0',
                    'maxwidth': 300,
                    'position': (0, y),
                    'vr_depth': 10,
                    'h_attach': 'center',
                    'h_align': 'center',
                    'v_attach': self.config['timer_pos'],
                    'v_align': 'center',
                    'color': (1.0, 1.0, 1.0, 1.0),
                    'shadow': 1,
                    'flatness': 1,
                    'scale': 1.5,
                    'opacity': 0.5,
                },
            )
        )
        
    def _trace_timer(self,
                     time: int):
        """ Sets the display timer's text to the provided time. """
        self.activity._chaos_dtimer.text = str(int(time))
        
        # Animate our text
        self.do_animation(time)
            
    def do_animation(self, n: int):
        """ Animates our text. """
        dop = self.defaults['opacity']
        dsc = self.defaults['scale']
        
        # Animate depending on the current number counting down
        # Last 3
        if n <= 3:
            nlist = [3,2,1]
            ba.animate(self.activity._chaos_dtimer, 'scale', {
                0: (dsc + ((dsc%3/3) * nlist[n-1])),
                1: dsc
            })
            ba.animate(self.activity._chaos_dtimer, 'opacity', {
                0: (dop + (((1-dop)/3) * nlist[n-1])),
                1: dop
            })
            
        # Halfway (> 50% of our timer)
        elif n <= int((self.config['time']+0.5)/2):
            ba.animate(self.activity._chaos_dtimer, 'opacity', {
                0: (dop + 0.15),
                1: dop
            })
        
class ChaosDisplayList:
    """ Event list for performed Chaos events.
        Purely visual; handled by ChaosManager. """
    def __init__(
        self,
        activity,
    ): 
        self.activity = activity
        self.config = activity._chaos_config
        
        self.evnodes = []
        
        self.evlen = self.config['list_len']
        
        # Alignment values
        self.alignx :str    = self.config['list_pos']
        # Alignment positions
        self.icosize        = 30
        self.glob_x         = (-30 if self.alignx == 'right' else 30)
        self.text_x         = self.glob_x - (self.icosize if self.alignx == 'right' else -self.icosize)
        self.glob_y = (
            (self.icosize * 1.1)*self.evlen / 2
        )
        
        # Time used to calculate remaining event time
        self.time_global = 0
        self.time_last = 0
        
        ba.timer(0.001, self.handle_timers, timetype=TimeType.BASE, repeat=True)
        
    def add_event(self,
                    name  : ba.Lstr | str,
                    icon  : ba.Texture,
                    time_l: list[float, TimeType] = (0.0, ba.TimeType.SIM)):
        """ Adds an event to the event list. """
        # Slide all the previous events down
        self.slide_events()
        
        time, timetype = time_l
        # We only handle BASE and SIM timetypes!
        if not timetype in [
            ba.TimeType.BASE,
            ba.TimeType.SIM,
        ]:
            raise Exception(f'TimeType not supported: "{timetype}"')
        
        # Add a name, icon and timer nodes
        self.evnodes.insert(0, [
            # Text
            ba.newnode(
                'text',
                attrs={
                    'text': name,
                    'maxwidth': 200,
                    'position': (
                        self.text_x,
                        self.glob_y
                        ),
                    'vr_depth': 5,
                    'h_attach': self.alignx,
                    'h_align': self.alignx,
                    'v_attach':'center',
                    'v_align': 'center',
                    'color': (1.0, 1.0, 1.0, 1.0),
                    'shadow': 1,
                    'flatness': 1,
                    'scale': 0.8,
                    'opacity': 0,
                },
            ),
            # Image
            ba.newnode(
                'image',
                attrs={
                    'texture': icon,
                    'absolute_scale': True,
                    'vr_depth': 5,
                    'position': (
                        self.glob_x,
                        self.glob_y
                        ),
                    'scale': (self.icosize,self.icosize),
                    'color': (1,1,1) if not time else (0,0,0),
                    'opacity': 0,
                    'attach': f'center{self.alignx.capitalize()}',
                },
            ),
            # Timer
            ba.newnode(
                'text',
                attrs={
                    'text': str(time),
                    'maxwidth': self.icosize * 0.9,
                    'position': (
                        self.glob_x,
                        self.glob_y
                        ),
                    'vr_depth': 5,
                    'h_attach': 'right',
                    'h_align': 'center',
                    'v_attach': 'center',
                    'v_align': 'center',
                    'color': (1.0, 1.0, 1.0, 1.0),
                    'shadow': 1,
                    'flatness': 1,
                    'scale': 0.85,
                    'opacity': 0,
                },
            ) if time else None,
            # Starting time (in ms)
            self.time_global if timetype is ba.TimeType.BASE else ba.time( timetype = ba.TimeType.SIM, timeformat=ba.TimeFormat.MILLISECONDS ),
            # Event time (in ms)
            time*1000 if time else None,
            # Timetype used
            timetype
        ])
        # Fade in every node
        ftime = min(0.5, self.config['time']*0.15)
        for i, ev in enumerate(self.evnodes[0]):
            if not type(ev) is ba.Node: continue
            maxop = 1 if i != 2 else 0.75
            ba.animate(ev, 'opacity', {
                0       : 0,
                ftime   : maxop,
            })
            # Color our icon pitch black if we have a timer (we'll handle this later)
            if i == 1 and time: ev.color = (0,0,0)
                
        # Clean up events if we start to overflow
        if len(self.evnodes) > self.evlen: self.clean_up()
    
    def slide_events(self):
        """ Slides all already existing displayed events a slot down. """
        time = min(0.5, self.config['time']*0.15)
        for group in self.evnodes:
            for node in group:
                if (
                    not type(node) is ba.Node or
                    not node.exists()
                ): continue
                ba.animate_array(node, 'position', 2, {
                    0   : node.position,
                    time: (node.position[0], node.position[1] - (self.icosize * 1.1)),
                })
        
    def clean_up(self):
        """ Removes the last element from the list. """
        # Fade all nodes out
        time = min(0.5, self.config['time']*0.15)
        for i, node in enumerate(self.evnodes[-1]):
            if (
                type(node) is ba.Node and
                node.exists()
            ):
                ba.animate(node, 'opacity', {
                    0: node.opacity,
                    time: 0,
                })
                ba.timer(time + 0.1, node.delete)
            else:
                self.evnodes[-1][i] = None
        # Wipe them from the list
        self.evnodes.pop(-1)
        
    def handle_timers(self):
        """ Gets the current time and handles the active events' time node. """
        t_ms = ba.time( timetype=ba.TimeType.BASE, timeformat=ba.TimeFormat.MILLISECONDS )
        
        diff = t_ms - self.time_last
        self.time_last = t_ms
        
        # We don't want to count the time we spend on a paused game
        if not self.activity.globalsnode.paused:
            self.time_global += diff
            
        # Do this for every event with a timer
        for event in self.evnodes:
            if (
                event[2] == None or
                event[4] == None
            ): continue
            # If we fail to do our job, we probably disappeared from the list
            if event[5] is ba.TimeType.BASE: self._handle_event_timer_base(event)
            elif event[5] is ba.TimeType.SIM: self._handle_event_timer_sim(event)
            else: raise Exception(f'TimeType not supported: "{event[5]}"')
            
    def _handle_event_timer_base(self, event: list):
        """ Handles the displayed time for an event.
            This function uses TimeType.BASE time. """
        # Assign variables
        _, _, _, stime, etime, _ = event
        # Calculate time left using given variables
        time_cur    = etime - (self.time_global - stime)
        
        # Modify our visuals accordingly
        self._handle_event_timer_post(event, time_cur, etime)
            
    def _handle_event_timer_sim(self, event: list):
        """ Handles the displayed time for an event.
            This function uses TimeType.SIM time. """
        # Assign variables
        _, _, _, stime, etime, _ = event
        # Calculate time left using given variables
        t_ms        = ba.time( timetype = ba.TimeType.SIM, timeformat=ba.TimeFormat.MILLISECONDS )
        time_cur    = etime - (t_ms - stime)
        
        # Modify our visuals accordingly
        self._handle_event_timer_post(event, time_cur, etime)
        
    def _handle_event_timer_post(self, event: list, current_time: int, end_time: int):
        """ Handles the displayed time and icon for an event. """
        _, image, timer, _, _, _ = event
        # Modify our visuals accordingly
        if not current_time <= 0:
            timer.text  = str(round(current_time/1000, 1))
            
            color_img   = 1 - (1 * (current_time / end_time))
            image.color = [color_img for _ in range(3)]
        else:
            timer.delete()
            image.color = (1,1,1)
    
class InitChaosMode:
    """ Initiates Chaos mode. """
    def __init__(
        self,
        activity: ba.Activity
    ):
        with ba.Context(activity): ChaosManager(activity)
        
from explodinary.chaos import (
    sok, temp, era, # Hehe, that's us!
    manager
    )

if False: print(len(Events['normal']))
