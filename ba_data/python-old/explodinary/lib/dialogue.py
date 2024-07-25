from __future__ import annotations
from enum import Enum

import ba
from bastd.actor.spazappearance import Appearance

class DialogueManager:
    """ Handles DialogueMessage, showing them one by one. """
    class ReadingState(Enum):
        """ An enum class for our reading state. """
        IDLE = 0
        READING = 1
        DONE = 2
    
    def __init__(self,
                 finish_call: callable | None = None):
        self.end_call = finish_call
        self._queued_messages, self._active_messages = ([],[])
        
        # Create a reading state
        self.rs = rs = self.ReadingState
        self._reading_state = rs.IDLE
        # Create a continue state that allows the queue messages to be loaded after the active ones finish (set by start())
        self._continue_on_finish = False 
        
    def add_message(self,
                    message: DialogueMessage):
        """ Adds a DialogueMessage to our _queued_messages list. """
        if type(message) is list:
            for msg in message:
                self._queued_messages.append(msg)
        else:
            self._queued_messages.append(message)
        
    def start(self,
              continue_on_finish: bool = False):
        """ Starts reading the current queued messages. """
        if self._reading_state == self.rs.READING:
            raise Exception('We\'re already reading messages!')
        elif len(self._queued_messages) < 1:
            raise Exception('There are no messages to read from.')
        
        # Update our reading variables
        self._reading_state = self.rs.READING
        self._continue_on_finish = continue_on_finish
        
        # Allocate our queued messages to the active list and start reading them
        self._active_messages = self._queued_messages.copy()
        self._queued_messages = []
        
        # Start our reading messages routine
        self.read_message()
        
    def read_message(self):
        """ Reads a message from the _active_messages list. """
        if len(self._active_messages) < 1:
            raise Exception('Trying to read_message from an empty _active_message list?\nThis shouldn\'t happen at all!')
        
        message = self._active_messages.pop(0)
        # Check what type of message we just loaded
        if type(message) is tuple:
            key, val = message
            # Interpret message as:
            if key == 'wait':
                ba.timer(val, self.read_message)
                return
            elif key == 'call':
                val()
            else:
                print(f'Unknown key type for "{message}". Skipping...')
            self.read_message()
            
        elif type(message) is DialogueMessage:
            # Override the end call with a function of ours so we're able to update whenever it ends
            message.end_call = ba.Call(self._finished_reading, message.end_call)
            # Call our message!
            message.start()
            
        else:
            print(f'Message type is invalid: "{message}". Skipping...')
            self.read_message()
        
    def _finished_reading(self, real_end_call: callable | None):
        """ Called when a DialogueMessage finishes. """
        # Call the original end call function if any
        if real_end_call: real_end_call()
        
        # Keep reading messages or mark our routine as finished
        if len(self._active_messages) > 0   : self.read_message()
        else                                : self._finished()
        
        
    def _finished(self):
        """ Tell ourselves we finished reading all queued messages. """
        # Continue reading queued messages!
        if self._continue_on_finish:
            # Don't do so if there are no queued messages.
            if len(self._queued_messages) < 1:
                self._continue_on_finish = False
                return
            self.start(continue_on_finish=True)
        else:
            # Call the end_call function if it exists.
            if self.end_call: self.end_call()
    
class DialogueMessage:
    """ Display a message including an icon, nickname and text.
        Mainly used in Campaign Mode's story. """
    def __init__(self,
                 speaker    : SpeakerLib._speaker_template,
                 text       : str,
                 time       : float = 1.5,
                 idle       : float = 3.0,
                 fade       : float = 1.5,
                 scale      : float = 1.0,
                 offset     : tuple = (0,0),
                 end_call   : callable | None = None):
        self.speaker    = speaker
        self.text       = text
        # Evaluate our text if it's type is ba.Lstr (Sadly we can't show different languages while keeping the dialogue writing animations ´n´)
        if type(text) is ba.Lstr: self.text = text = text.evaluate()
        # Replace all ⛔s with a zero-width character for further dialogue reading
        self.text = text = text.replace("⛔","\u200b")
        
        self.time       = time
        self.idle       = idle
        self.fade       = fade
        
        self.scale      = scale
        self.offset     = offset
        
        self.end_call   = end_call
        
        # Internal variables
        self._text_start_time: int | None = None
        self._text_update_clock: ba.Timer | None = None
        self._last_text_percentage: int | None = None
        
        self._sound_dialogue = ba.getsound('dialogueType')
        
    def start(self):
        """ Displays this DialogueMessage. """
        # General variables
        s           = self.speaker
        scl         = self.scale
        goff        = self.offset
        start_line  = 166
        # Icon variables
        icoscl      = 56
        masktex     = ba.gettexture('characterIconMask')
                
        self.icon = ba.newnode(
            'image',
            attrs={
                'texture':          s['icon']['texture'],
                'tint_texture':     s['icon']['tint_texture'],
                'tint_color':       s['color'],
                'tint2_color':      s['highlight'],
                'mask_texture':     masktex,
                'absolute_scale':   True,
                'position':         (goff[0], goff[1] + start_line + (((icoscl/2)+12.5)*scl)),
                'scale':            [icoscl * scl for _ in range(2)],
                'attach':           'bottomCenter',
            },
        )
        self.name = ba.newnode(
            'text',
            attrs={
                'text':             s['name'],
                'maxwidth':         160,
                'position':         (goff[0], goff[1] + start_line),
                'h_attach':         'center',
                'v_attach':         'bottom',
                'h_align':          'center',
                'v_align':          'center',
                'color':            s['color'],
                'scale':            1.077 * scl,
                'shadow':           0.65,
                'flatness':         1.0,
            }
        )
        self.msg = ba.newnode(
            'text',
            attrs={
                'text':             '',
                'maxwidth':         450,
                'position':         (goff[0], goff[1] + start_line - (15*scl)),
                'h_attach':         'center',
                'v_attach':         'bottom',
                'h_align':          'center',
                'v_align':          'top',
                'color':            (1,1,1),
                'scale':            0.9 * scl,
                'shadow':           0.45,
                'flatness':         0.75,
            }
        )
        # Play one of our speaker's sounds
        import random
        if self.speaker['sounds']:
            ba.playsound(
                ba.getsound( random.choice(self.speaker['sounds']) ),
                volume = 0.77 * self.scale,
                )
            
        # Add a one-frame timer to update our text
        if self.time:
            # Do our text updating routine if we actually provided a time
            self._text_update_clock = ba.Timer(0.001, self.text_update, repeat=True)
        else:
            # Else, show the text immediately and go to the idling / fading section
            self.msg.text = self.text
            self.do_idle()
        
    def text_update(self):
        """ Renders our text, plays sound bites and checks if we've finished
            displaying all of it using the time provided. """
        t_ms, ourt, last, ltp = ba.time(timeformat=ba.TimeFormat.MILLISECONDS), self.time*1000, self._text_start_time, self._last_text_percentage
        # If we just started, mark this millisecond to our start time so we can
        # calculate how much text we reveal according to current and ending time
        if not last: last = self._text_start_time = t_ms
        # Get the percentage of how close we are to our target time
        p = ( (t_ms - last) / ourt ) * 100; tp = len(self.text) if t_ms >= last + ourt else max(1, int( len(self.text)/100 *p ))
        text_segment = self.text[:tp]
        # Record that our last character isn't a non-width character, space, line break or... nothing!
        # (IndexError is thrown for some reason with the non-width character so we add that as a fallback.)
        no_last_char = text_segment[-1] in ['\u200b',' ','\n','']
        # Play a typing sound whenever our ltp does not match our new tp
        if not ltp == tp and not no_last_char:
            ba.playsound(
                self._sound_dialogue,
                volume = 0.44 * self.scale,
            )
            self._last_text_percentage = tp
        
        # Draw the percentage of our text into the message box
        self.msg.text = text_segment
        
        # End our cycle once our time is beyond our type time
        if t_ms >= last + ourt:
            self._text_update_clock = None
            self.do_idle()
        
    def do_idle(self):
        """ Idles our message on screen during the provided time and then fades out. """
        # Fallback: if both display time and fadeout time add up to no more than 0, skip this step
        if not self.idle + self.fade > 0:
            self.end()
            return
        self.idle += 0.001; self.fade += 0.001 # Small fallbacks to prevent the animation from breaking
        
        # Animate the entire idle!
        for node in [
            self.icon,
            self.name,
            self.msg,
        ]:
            ba.animate(node, 'opacity', {
                0                       : 1,
                self.idle               : 1,
                self.idle + self.fade   : 0,
            })
        ba.timer(self.idle + self.fade, self.end)
        
    def end(self):
        """ Marks the end of our message.
            Called after our text fades out. """
        if self.end_call: self.end_call()
        self.die()
        
    def die(self):
        """ Deletes all our nodes. """
        for node in [
            self.icon,
            self.name,
            self.msg,
        ]:
            node.delete()
    
def get_player_speaker(player: ba.Player) -> dict:
    """ Returns a player's speaking dict. """
    return {
        'name'      : player.getname(),
        'icon'      : player.get_icon(),
        'color'     : player.color,
        'highlight' : player.highlight,
        'sounds'    : ba.app.spaz_appearances.get(player.character).attack_sounds,
    }

def get_appearance_speaker(appearance: Appearance) -> dict:
    """ Returns a speaker dict from a spazappearance class. """
    return {
        'name'      : appearance.name,
        'icon'      : {
            'texture'       : ba.gettexture(appearance.icon_texture),
            'tint_texture'  : ba.gettexture(appearance.icon_mask_texture),
        },
        'color'     : appearance.default_color,
        'highlight' : appearance.default_highlight,
        'sounds'    : appearance.attack_sounds,
        }
    
class SpeakerLib:
    """ A class with template speakers. """
    def __init__(self):
        self.helpy = get_appearance_speaker(ba.app.spaz_appearances.get('Helpy'))
        
    def _speaker_template(self) -> dict:
        """ Returns a template for a speaker. """
        _dap = ba.app.spaz_appearances.get('Spaz')
        return {
            'name'      : 'character_name',
            'icon'      : {
                'texture'       : _dap.icon_texture,
                'tint_texture'  : _dap.icon_mask_texture
            },
            'color'     : (0.7, 0.7, 0.7),
            'highlight' : (0.3, 0.3, 0.3),
            'sounds'    : _dap.attack_sounds,
        }