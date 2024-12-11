"""Plugin fix for older versions of Explodinary."""
import bascenev1 as bs
def do():
    did_a_thing = False
    new_plugin_list = bs.app.config['Plugins'].copy()
    for i,v in enumerate(bs.app.config['Plugins']):
        if v in [
                'bastd.actor.quickturn.MikiWavedashTest',
                'bastd.game.timeyBombnuts.TimeyBombnutsLevel',
                'bastd.game.explodinaryOnslaught.ExplodinaryOnslaughtLevel',
                'bastd.game.explodinaryRunaround.ExplodinaryInfiniteRunaroundLevel',
                'bastd.game.routeRoulette.RouteRouletteLevel',
                'bastd.game.kablooyaOnslaught.KablooyaOnslaughtLevel',
                'bastd.game.kablooyaRunaround.KablooyaRunaroundLevel',
                'explodinary.game.pathwayPandemonium.PathwayPandemoniumLevel',
                'bastd.game.arms_race.ArmsRaceGame',
                'bastd.ui.quick_game.QuickGamePlugin'
                ]:
            del new_plugin_list[v]
            did_a_thing = True
    if did_a_thing:
        bs.app.config['Plugins'] = new_plugin_list
        bs.app.config.commit()