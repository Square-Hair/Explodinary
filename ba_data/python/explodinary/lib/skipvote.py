from __future__ import annotations
import ba
import random

class SkipVoteModule:
    """ A class in charge of handling player inputs,
        count votes and reset the session if enough players voted. """
    def __init__(self,
                 percent: float = 100.0,
                 skiptext: ba.Lstr | str | None = None,
                 on_vote_end: callable | None = None):
        """"""
        self.activity   = ba.getactivity() # _ba.get_foreground_host_activity()
        self.percent    = percent
        if not skiptext:
            skiptext = ba.Lstr(resource='explodinary.skipVotes')
        self.skiptext   = skiptext
        self.call       = on_vote_end
        
        self.votes          = 0
        self.votes_max      = 0
        self.players        = []
        self.voted_players  = []
        
        self._on_warning    = False
        # Dying unwires our players from voting, so we need to keep 'em hooked
        self._rewire_clock          = ba.Timer(0.1, self.wire_players_to_vote, repeat=True)
                
        # Nodes
        self._skip_count_text = ba.newnode(
            'text', attrs={
                'position': (0, -80),
                'h_attach': 'center',
                'v_attach': 'top',
                'h_align': 'center',
                'v_align': 'center',
                'scale': 1.15,
                'color': (1,1,1,1),
                'text': self._get_count_text(),
                'opacity': 0,
            }
        )
        self._skip_confirm_text = ba.newnode(
            'text', attrs={
                'position': (0, -120),
                'h_attach': 'center',
                'v_attach': 'top',
                'h_align': 'center',
                'v_align': 'center',
                'scale': 0.75,
                'color': (1,0.3,0.3,0.75),
                'opacity': 0,
                'text': ba.Lstr(resource='explodinary.skipConfirm'),
            }
        )
        
        self._update_votings()
        self.wire_players_to_vote()
        self._fade_vote_count()
        
    def _animate_vote_count(self, player: ba.Player | None = None):
        """ Animates the vote count.
            Called whenever someone votes. """
        ba.animate(self._skip_count_text, 'scale', {
            0: 1.3,
            0.15: 1.22,
            0.33: 1.15,
        })
        color = player.color if player else (1, 0.9, 0.2)
        ba.animate_array(self._skip_count_text, 'color', 3, {
            0: color,
            0.33: (1,1,1),
        })
        self._fade_vote_count()
        
    def _fade_vote_count(self):
        """ Makes the vote count visible for 4 seconds before fading away. """
        ba.animate(self._skip_count_text, 'opacity', {
            0   : self._skip_count_text.opacity,
            0.1 : 1,
            4   : 1,
            6   : 0,
        })
        
    def _get_count_text(self):
        """ Returns the count text. """
        return ba.Lstr(value='${SKIP}: ${COUNT}/${COUNTMAX}', subs=[
                       ('${SKIP}',      self.skiptext),
                       ('${COUNT}',     str(self.votes)),
                       ('${COUNTMAX}',  str(self.votes_max)),
                       ])
        
    def _update_votings(self):
        """ Updates how many people are there, how many votes we have and how many are needed to skip. """
        self.players = [p for p in self.activity.players]
        self.votes = sum(1 for player in self.voted_players if player in self.players)
        self.votes_max = max(1, int(len(self.players)/100*self.percent))
        
        self._skip_count_text.text = self._get_count_text()
        
        # Check if we met the vote quota
        if self.votes >= self.votes_max: self.vote_ended()
        
    def wire_players_to_vote(self):
        """ Wires player's button to vote! """
        player: ba.Player
        for player in self.players:
            
            player.assigninput(
                (
                    ba.InputType.JUMP_PRESS,
                    ba.InputType.PUNCH_PRESS,
                    ba.InputType.BOMB_PRESS,
                    ba.InputType.PICK_UP_PRESS,
                ),
                ba.Call(self.player_voted, player),
            )
            
    def player_voted(self, player: ba.Player):
        """ Tells our voting system someone voted!
            Give 'em a sick stamp and a pat on the back :3 """
        if player in self.voted_players:
            self._update_votings()
            return
        
        if len(self.players) == 1 and not self._on_warning: self.solo_warning(True)
        else: self.add_vote(player)
        
    def add_vote(self, player: ba.Player):
        """ Adds a vote from our player. """
        if player in self.voted_players:
            raise Exception(f'This player has already voted: "{player}"\nShouldn\'t reach this logic point.')
        
        # Add this player's vote into the votelist
        self.voted_players.append(player)
        
        # Play a cool sound and update our votes
        try: sound = random.choice(ba.app.spaz_appearances.get(player.character).jump_sounds)
        except: sound = 'corkPop'
        
        ba.playsound(ba.getsound(sound), volume = 0.66)
        self._animate_vote_count(player)
        self._update_votings()
        
    def solo_warning(self, yes: bool):
        """ Warn our lonely players that pressing Jump again will skip the cutscene. """
        self._on_warning = yes
        if yes:
            # Fade in and animate our skip confirm text
            # I'd use a loop here but there's no way to kill animates after they're made
            # So yea, very cool. -Temp
            ba.animate(self._skip_confirm_text, 'opacity', {
                0.0: 0, 0.2: 1.25, 0.4: 0.75, 0.6: 1.25, 0.8: 0.75, 1.0: 1.25, 1.2: 0.75, 1.4: 1.25,
                1.6: 0.75, 1.8: 1.25, 2.0: 0.75, 2.2: 1.25, 2.4: 0.75, 2.6: 1.25, 2.8: 0.75,
                3.0: 1.25, 3.2: 0.75, 3.4: 1.25, 3.6: 0.75, 3.8: 1.25, 4.0: 0.75, 4.2: 1.25, 4.4: 0.75,
                4.6: 1.25, 4.8: 0.75, 5.0: 1.25, 5.2: 0.75, 5.4: 1.25, 5.6: 0.75, 5.8: 1.25, 6.0: 0,
            })
            
            # Animate our skip count text
            self._fade_vote_count()
            # Wait 6 seconds before fading out 
            ba.timer(6.0, ba.Call(self.solo_warning, False))
        else:
            # Fade out our skip confirm text
            ba.animate(self._skip_confirm_text, 'opacity', {
                0: self._skip_confirm_text.opacity,
                0.2: 0,
            }, loop=True)
        
        
    def vote_ended(self):
        """ Called when a vote ends positively. """
        # Play a cool sound
        ba.playsound(ba.getsound('swish'))
        # Call the provided function and kill this process
        if self.call: self.call()
        self.delete()
        
    def end(self):
        """ Ends the voting abruptly. """
        self.vote_halted()
        
    def vote_halted(self):
        """ Called when a vote ends abruptly. """
        self.delete()
        
    def delete(self):
        """ Unlinks our player's inputs and deletes all our nodes. """
        player: ba.Player
        for player in self.players: player.resetinput()
        if player.actor: player.actor.connect_controls_to_player()
        
        for node in [
            self._skip_count_text,
            self._skip_confirm_text,
        ]:
            node.delete()
            
        self._rewire_clock = None