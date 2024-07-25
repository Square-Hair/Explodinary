# Ported by: Freaku / @[Just] Freak#4999
# Slightly modified for BSE by SoK

# Join BCS:
# https://discord.gg/ucyaesh


# ba_meta require api 7

from __future__ import annotations

from typing import TYPE_CHECKING

import ba
from bastd.actor.playerspaz import PlayerSpaz

if TYPE_CHECKING:
    from typing import Any, Type, List, Dict, Tuple, Union, Sequence, Optional


class State:
    def __init__(self, bomb=None, grab=False, punch=False, curse=False, required=False, final=False, name='', raw_name = ''):
        self.bomb = bomb
        self.grab = grab
        self.punch = punch
        self.pickup = False
        self.curse = curse
        self.required = required or final
        self.final = final
        self.name = name
        self.raw_name = raw_name
        self.next = None
        self.index = None

    def apply(self, player, spaz):

        spaz.disconnect_controls_from_player()
        spaz.connect_controls_to_player(enable_punch=self.punch,
                                        enable_bomb=self.bomb,
                                        enable_pickup=self.grab)
        if self.curse:
            spaz.curse_time = -1
            spaz.curse()
        if self.bomb:
            spaz.bomb_type = self.bomb
        spaz.set_score_text(self.name)

        def set_controls():
            player.actor.node.bomb_pressed = True
            player.actor.on_bomb_release()

        release_input = (ba.InputType.PUNCH_RELEASE, ba.InputType.PICK_UP_RELEASE)
        if not self.bomb is None:
            for release in release_input:
                player.assigninput(
                    release,
                    set_controls
                )

    def get_setting(self):
        return (self.raw_name)


states = [State(bomb='normal',      raw_name = 'Normal Bombs' , name = ba.Lstr(translate=['armsRace', 'Normal Bombs' ])),
          State(bomb='ice',         raw_name = 'Ice Bombs'    , name = ba.Lstr(translate=['armsRace', 'Ice Bombs'    ])),
          State(bomb='sticky',      raw_name = 'Sticky Bombs' , name = ba.Lstr(translate=['armsRace', 'Sticky Bombs' ])),
          State(bomb='impact',      raw_name = 'Impact Bombs' , name = ba.Lstr(translate=['armsRace', 'Impact Bombs' ])),
          State(bomb='tacky',       raw_name = 'Tacky Bombs'  , name = ba.Lstr(translate=['armsRace', 'Tacky Bombs'  ])),
          State(bomb='toxic',       raw_name = 'Toxic Bombs'  , name = ba.Lstr(translate=['armsRace', 'Toxic Bombs'  ])),
          State(bomb='steampunk',   raw_name = 'Steam Bombs'  , name = ba.Lstr(translate=['armsRace', 'Steam Bombs'  ])),
          State(bomb='cluster',     raw_name = 'Cluster Bombs', name = ba.Lstr(translate=['armsRace', 'Cluster Bombs'])),
          State(grab=True,          raw_name = 'Grabbing only', name = ba.Lstr(translate=['armsRace', 'Grabbing only'])),
          State(punch=True,         raw_name = 'Punching only', name = ba.Lstr(translate=['armsRace', 'Punching only'])),
          State(curse=True,         raw_name = 'Cursed'       , name = ba.Lstr(translate=['armsRace', 'Cursed'       ]), final=True)]


class Player(ba.Player['Team']):
    """Our player type for this game."""

    def __init__(self):
        self.state = None


class Team(ba.Team[Player]):
    """Our team type for this game."""

    def __init__(self) -> None:
        self.score = 0


# ba_meta export game
class ArmsRaceGame(ba.TeamGameActivity[Player, Team]):
    """A game type based on acquiring kills."""

    name = 'Arms Race'
    description = 'Upgrade your weapon by eliminating enemies.\nWin the match by being the first player\nto get a kill while cursed.'

    # Print messages when players die since it matters here.
    announce_player_deaths = True

    @classmethod
    def get_available_settings(
            cls, sessiontype: Type[ba.Session]) -> List[ba.Setting]:
        settings = [
            ba.IntChoiceSetting(
                'Time Limit',
                choices=[
                    ('None', 0),
                    ('1 Minute', 60),
                    ('2 Minutes', 120),
                    ('5 Minutes', 300),
                    ('10 Minutes', 600),
                    ('20 Minutes', 1200),
                ],
                default=0,
            ),
            ba.FloatChoiceSetting(
                'Respawn Times',
                choices=[
                    ('Shorter', 0.25),
                    ('Short', 0.5),
                    ('Normal', 1.0),
                    ('Long', 2.0),
                    ('Longer', 4.0),
                ],
                default=1.0,
            ),
            ba.BoolSetting('Epic Mode', default=False)]
        for state in states:
            if not state.required:
                settings.append(ba.BoolSetting(state.get_setting(), default=True))

        return settings

    @classmethod
    def supports_session_type(cls, sessiontype: Type[ba.Session]) -> bool:
        return (issubclass(sessiontype, ba.DualTeamSession)
                or issubclass(sessiontype, ba.FreeForAllSession))

    @classmethod
    def get_supported_maps(cls, sessiontype: Type[ba.Session]) -> List[str]:
        return ba.getmaps('melee')

    def __init__(self, settings: dict):
        super().__init__(settings)
        self.states = [s for s in states if settings.get(s.name, True)]
        for i, state in enumerate(self.states):
            if i < len(self.states) and not state.final:
                state.next = self.states[i + 1]
            state.index = i
        self._dingsound = ba.getsound('dingSmall')
        self._epic_mode = bool(settings['Epic Mode'])
        self._time_limit = float(settings['Time Limit'])

        # Base class overrides.
        self.slow_motion = self._epic_mode
        self.default_music = (ba.MusicType.EPIC if self._epic_mode else
                              ba.MusicType.ARMS_RACE)

    def get_instance_description(self) -> Union[str, Sequence]:
        return 'Upgrade your weapon by eliminating enemies.'

    def get_instance_description_short(self) -> Union[str, Sequence]:
        return 'upgrade until you get a curse kill', len(self.states)

    def on_begin(self) -> None:
        super().on_begin()
        self.setup_standard_time_limit(self._time_limit)
        # self.setup_standard_powerup_drops()

    def on_player_join(self, player):
        if player.state is None:
            player.state = self.states[0]
        self.spawn_player(player)

    # overriding the default character spawning..

    def spawn_player(self, player):
        if player.state is None:
            player.state = self.states[0]
        super().spawn_player(player)
        player.state.apply(player, player.actor)

    def isValidKill(self, m):
        if m.getkillerplayer(Player) is None:
            return False

        if m.getkillerplayer(Player).team is m.getplayer(Player).team:
            return False

        return True

    def handlemessage(self, msg: Any) -> Any:

        if isinstance(msg, ba.PlayerDiedMessage):
            if self.isValidKill(msg):
                self.stats.player_scored(msg.getkillerplayer(Player), 10, kill=True)
                if not msg.getkillerplayer(Player).state.final:
                    msg.getkillerplayer(Player).state = msg.getkillerplayer(Player).state.next
                    msg.getkillerplayer(Player).state.apply(
                        msg.getkillerplayer(Player), msg.getkillerplayer(Player).actor)
                else:
                    msg.getkillerplayer(Player).team.score += 1
                    self.end_game()
            self.respawn_player(msg.getplayer(Player))

        else:
            return super().handlemessage(msg)
        return None

    def end_game(self) -> None:
        results = ba.GameResults()
        for team in self.teams:
            results.set_team_score(team, team.score)
        self.end(results=results)
