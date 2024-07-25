import ba
from bastd.game import (
    assault, capturetheflag, chosenone,
    conquest, deathmatch, elimination,
    football, hockey, keepaway,
    kingofthehill, onslaught, race, runaround,
    ninjafight, easteregghunt, targetpractice, meteorshower,
    arms_race, soccer, rockethell, arms_race
    )
from explodinary.game import (
    kablooyaOnslaught, explodinaryOnslaught,
    kablooyaRunaround, explodinaryRunaround,
    pathwayPandemonium, routeRoulette, #arms_race, soccer, rockethell
    )

announce_l = {
    assault.AssaultGame:'Assault',
    capturetheflag.CaptureTheFlagGame:'CaptureTheFlag',
    chosenone.ChosenOneGame:'ChosenOne',
    conquest.ConquestGame:'Conquest',
    deathmatch.DeathMatchGame:'DeathMatch',
    elimination.EliminationGame:'Elimination',
    football.FootballCoopGame:'Football',
    football.FootballTeamGame:'Football',
    hockey.HockeyGame:'Hockey',
    keepaway.KeepAwayGame:'KeepAway',
    kingofthehill.KingOfTheHillGame:'KingOfTheHill',
    onslaught.OnslaughtGame:'Onslaught',
    race.RaceGame:'Race',
    runaround.RunaroundGame:'Runaround',
    ninjafight.NinjaFightGame:'NinjaFight',
    easteregghunt.EasterEggHuntGame:'EasterEggHunt',
    meteorshower.MeteorShowerGame:'MeteorShower',
    targetpractice.TargetPracticeGame:'TargetPractice',
    ### BSE
    kablooyaOnslaught.KablooyaOnslaughtGame:'Onslaught',
    explodinaryOnslaught.ExplodinaryOnslaughtGame:'Onslaught',
    kablooyaRunaround.KablooyaRunaroundGame:'Runaround',
    explodinaryRunaround.ExplodinaryInfiniteRunaroundGame:'Runaround',
    pathwayPandemonium.PathwayPandemoniumGame:'Pandemonium',
    routeRoulette.RouteRouletteGame:'RouteRoulette',
    rockethell.RocketHellGame:'RocketHell',
    soccer.SoccerGame:'Soccer',
    arms_race.ArmsRaceGame:'ArmsRace',
}

def _slomo() -> None: return(ba.getactivity().slow_motion)

def _do_game_announce(game) -> None:
    vc = None
    if not _slomo():
        # Get voiceline
        cfg = ba.app.config
        do = cfg.get("BSE: Announce Games", False)
        
        vc = f'announce{announce_l.get(type(game), "None")}'
        if vc == 'announceNone' or not do: vc = None

    # Play thing
    if vc: ba.playsound(ba.getsound(vc))
    ba.playsound(ba.getsound('gong'), 0.3 if vc else 1)