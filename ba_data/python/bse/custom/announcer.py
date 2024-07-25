import bascenev1 as bs
from bascenev1lib.game import (
    assault, capturetheflag, chosenone,
    conquest, deathmatch, elimination,
    football, hockey, keepaway,
    kingofthehill, onslaught, race, runaround,
    ninjafight, easteregghunt, targetpractice, meteorshower,
    )
#from bse.game import (
#    kablooyaOnslaught, explodinaryOnslaught,
#    kablooyaRunaround, explodinaryRunaround,
#    pathwayPandemonium, routeRoulette, arms_race, soccer, rockethell
#    )

game_names = {
    assault.AssaultGame                 :'Assault',
    capturetheflag.CaptureTheFlagGame   :'CaptureTheFlag',
    chosenone.ChosenOneGame             :'ChosenOne',
    conquest.ConquestGame               :'Conquest',
    deathmatch.DeathMatchGame           :'DeathMatch',
    elimination.EliminationGame         :'Elimination',
    football.FootballCoopGame           :'Football',
    football.FootballTeamGame           :'Football',
    hockey.HockeyGame                   :'Hockey',
    keepaway.KeepAwayGame               :'KeepAway',
    kingofthehill.KingOfTheHillGame     :'KingOfTheHill',
    onslaught.OnslaughtGame             :'Onslaught',
    race.RaceGame                       :'Race',
    runaround.RunaroundGame             :'Runaround',
    ninjafight.NinjaFightGame           :'NinjaFight',
    easteregghunt.EasterEggHuntGame     :'EasterEggHunt',
    meteorshower.MeteorShowerGame       :'MeteorShower',
    targetpractice.TargetPracticeGame   :'TargetPractice',
    ### BSE
    #kablooyaOnslaught.KablooyaOnslaughtGame                 :'Onslaught',
    #explodinaryOnslaught.ExplodinaryOnslaughtGame           :'Onslaught',
    #kablooyaRunaround.KablooyaRunaroundGame                 :'Runaround',
    #explodinaryRunaround.ExplodinaryInfiniteRunaroundGame   :'Runaround',
    #pathwayPandemonium.PathwayPandemoniumGame               :'Pandemonium',
    #routeRoulette.RouteRouletteGame                         :'RouteRoulette',
    #rockethell.RocketHellGame                               :'RocketHell',
    #soccer.SoccerGame                                       :'Soccer',
    #arms_race.ArmsRaceGame                                  :'ArmsRace',
}

def _slomo() -> None: return(bs.getactivity().slow_motion)

def _do_game_announce(game) -> None:
    vc = None
    if not _slomo():
        # Get voiceline
        cfg = bs.app.config
        do = cfg.get("BSE: Announce Games", False)
        
        vc = f'bse_announce{game_names.get(type(game), "None")}'
        if vc == 'announceNone' or not do: vc = None

    # Play thing
    if vc: bs.getsound(vc).play()
    bs.getsound('gong').play(volume = 0.3 if vc else 1)
    
""" Code insertion. """ 
from bascenev1._gameactivity import GameActivity
def new_show_info(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        bs.timer(0.2, bs.Call(_do_game_announce, bs.getactivity()))
    return wrapper

GameActivity._show_info = new_show_info(GameActivity._show_info)