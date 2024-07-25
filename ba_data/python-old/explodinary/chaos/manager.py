import ba
from ba import TimeType
from explodinary.chaos import ChaosEvent, append_chaos_event

class ManagerSwitchTime(ChaosEvent):
    change = 0
    durmult = 2
    bounds = [0.00, 1.50]
    
    def event(self):
        """ Makes the Chaos timer go slightly faster. """
        # Don't make it go TOO WILD y'know!
        if self.manager.base_time < self.bounds[0] or self.manager.base_time > self.bounds[1]: return False
        
        duration = self._get_config()['time'] * self.durmult

        # Do and apply
        self.manager.base_time -= self.change        
        self.apply()
        
        ba.timer(duration, self.rewind)
        
        return duration

    def apply(self):
        """ Applies our changes by updating the update time timer. """
        self.activity._chaos['update_time'] = ba.Timer(self.manager.base_time/self.manager.time_rate,
                                                       self.manager._update,
                                                       timetype=TimeType.BASE,
                                                       repeat=True)
        
        self.manager._update_time[0]        = self.activity._chaos['update_time']                
    
    def rewind(self):
        """ Rewinds our changes. """
        self.manager.base_time += self.change
        self.apply()

class ManagerTurnItUp(ManagerSwitchTime):
    name = 'Turn it up!'
    icon = 'chaosTurnItUp'
    event_type = 'manager'
    
    change = 0.12
    durmult = 5
    bounds = [0.6, 999]
    
append_chaos_event(ManagerTurnItUp)
    
class ManagerBackItDown(ManagerSwitchTime):
    name = 'Back it down'
    icon = 'chaosTurnItDown'
    event_type = 'manager'
    
    change = -0.175
    durmult = 2
    bounds = [-999, 1.5]
    
append_chaos_event(ManagerBackItDown)
    
class ManagerTripleroo(ChaosEvent):
    name = 'Triple-roo!'
    icon = 'chaosTripleroo'
    event_type = 'manager'
    
    def event(self):
        """ Runs 3 random events. """
        for _ in range(3):
            self.manager.do_event(
                pool            = 'normal',
                data_override   = {
                    'announce': False
                }
            )
            
append_chaos_event(ManagerTripleroo)
