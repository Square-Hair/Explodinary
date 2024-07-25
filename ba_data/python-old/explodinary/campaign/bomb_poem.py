from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Sequence

import ba
import random
from bastd.gameutils import SharedObjects

class Player(ba.Player['Team']):
    """Our player type for this game."""

class Team(ba.Team[Player]):
    """Our team type for this game."""

class BombPoem(ba.Actor):
    def __init__(self,text,color,scale,time):
        ba.Actor.__init__(self)
		
        time *= 2

        self.text = ba.NodeActor(ba.newnode('text',
                         attrs={'v_attach':'bottom' ,
                                'h_attach':'center',
                                'text':ba.Lstr(translate=('bombPoem', text)),
                                'h_align':'center',
                                'v_align':'center',
                                'shadow':1.0,
                                'flatness':1.0,
                                'color':color,
                                'scale':1,
                                'position':(0,-100)}))
								
        ba.animate_array(self.text.node,'position',2,{0:self.text.node.position,time:(0,900)})
        ba.timer(time,self.clr)
		
    def clr(self):
        self.text.node.delete()
        
class BombPoemGame(ba.CoopGameActivity[Player, Team]):
    name = ''
    description = ''
    default_music = ba.MusicType.BOMB_POEM
    big_message = False
    
    def get_supported_maps(cls, sessiontype: type[ba.Session]) -> list[str]:
        return ['Bomb Poem']
        
    def _show_info(self) -> None: return

    def on_begin(self) -> None:
        ba.CoopGameActivity.on_begin(self)
        self.play_big_death_sound = False
        self.propertoppers()
		
        self.poem = [
                   ['Brother, I have witnessed a mortal player whose creativity\nin the realm of BombLand transcends the ordinary.\n'
                    'They are an artist of explosive innovation, crafting a symphony of chaos and strategy.',(0.2,1,0.5),4.0,20,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['Ah, the spark of creativity, a flame that ignites the imagination.\n'
                    'Tell me, brother, how does this player manifest their creative prowess within the confines of BombLand?',(0,1,1),4.5,20,1.5],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['They manipulate the game\'s elements like a master sculptor,\n'
                    'fashioning bombs and strategies into breathtaking works of art.\n'
                    'Each explosion is a brushstroke, each move a stroke of genius.\n'
                    'Their canvas is the virtual arena, and their creations leave both allies and adversaries spellbound.',(0.2,1,0.5),4.5,20,1.5],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['A virtuoso of destruction, I see.\n'
                    'But is their creativity limited to mere destruction, or do they also\n'
                    'weave tales of triumph and unexpected beauty amidst the chaos?',(0,1,1),4.5,20,1.5],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['Their creativity knows no bounds, brother.\n'
                    'They engineer elaborate schemes, constructing intricate mazes of bombs\n'
                    'that become intricate puzzles for their opponents to solve.\n'
                    'Their strategies are a tapestry of surprise and intrigue, showcasing\n'
                    'their ability to bend the rules to their will.',(0.2,1,0.5),4.5,20,1.5],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['How fascinating! It is as if they have unlocked the very essence of imagination itself,\n'
                    'infusing the game with their own unique vision. Do they draw inspiration from the world around them,\n'
                    'or do they possess a wellspring of creativity deep within their soul?',(0,1,1),4.5,20,1.5],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['They are a vessel of inspiration, brother, drawing from both the tangible and intangible.\n'
                    'They find inspiration in the chaos of nature, the patterns of the stars, and the whispers of forgotten legends.\n'
                    'They channel these muses into their gameplay, creating moments\n'
                    'of pure brilliance that captivate all who bear witness.',(0.2,1,0.5),4.5,20,1.5],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['To harness creativity in such a way is a gift bestowed upon few.\n'
                    'This mortal player brings forth a symphony of ideas and innovation,\n'
                    'transforming the battlegrounds of BombLand into a living canvas.\n'
                    'Their play transcends the mundane, elevating it to a realm where imagination and skill coalesce.',(0,1,1),4.5,20,1.5],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['\n',(0.2,1,0.5),4.0,15,1],
                   ['Let us celebrate this creative force, brother, for they inspire mortals\n'
                    'to explore the depths of their own imagination. In their wake, they leave a legacy of artistry,\n'
                    'encouraging others to push the boundaries of what is possible. May their inventive spirit\n'
                    'forever burn bright, as a beacon for all who dare to dream within the realm of BombLand.',(0.2,1,0.5),4.5,20,1.5],
                  ]
        ba.timer(5,self.start_credits)
        ba.timer(81, self.end_game)
	
    def propertoppers(self) -> None:
        ba.getsession()._custom_menu_ui = []
        
    def start_credits(self):
       delay = 0
       for c in self.poem:
           ba.timer(delay,ba.Call(BombPoem,text=c[0],color=c[1],scale=c[2],time=c[3]))
           delay += (c[4])

    def spawn_player(self,player): return
    
    def end_game(self) -> None:
        delay = 7.5

        gnode = self.globalsnode
        ba.animate_array(gnode, 'tint', 3, {
            0: gnode.tint,
            delay: (0,0,0),
        })
        ba.timer(delay + 0.1, lambda: ba.app.return_to_main_menu_session_gracefully(reset_ui=False))