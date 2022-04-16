#created 4/15/2022 from sentdex youtube tutorial https://www.youtube.com/watch?v=5U2WdZxJhEE

#import sc2
from sc2 import run_game, maps, Race, Difficulty
#from sc2.player import Bot, Computer


import random

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.player import Human

class Supply_depot():
    def __init__(self,time):
        self.time_built = time 

class Game():
    def __init__(self,time):
        self.iteration = time
        self.supply_depots = 0
        self.workers = 0

class Oli_bot(sc2.BotAI):
    async def on_step(self, iteration):
        if iteration == 50 or iteration == 100:
            print(str(iteration))
        Early_g = Game(iteration)
        cc = (self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND))
        cc = cc.first
        await self.distribute_workers()
        
        if self.workers.amount < 22 and cc.noqueue:
            await self.do(cc.train(SCV))
        ''' if self.can_afford(SCV):
            await self.build_workers(cc) '''
            
        #self.supply_left < 3 and 
        if self.supply_used < 15 and self.can_afford(SUPPLYDEPOT): 
            #print("Supply Depots: "+str(Early_g.supply_depots))
            await self.build(SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center,8))
            #await self.build_supply(cc)
        if self.supply_left < 3 and self.can_afford(SUPPLYDEPOT): 
            #print("Supply Depots: "+str(Early_g.supply_depots))
            await self.build(SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center,8))
        
        if self.units(SUPPLYDEPOT).exists:
            if not self.units(BARRACKS).exists:
                if self.can_afford(BARRACKS):
                    await self.build(BARRACKS, near=cc.position.towards(self.game_info.map_center, 8))

            elif self.units(BARRACKS).exists and self.units(REFINERY).amount < 2:
                if self.can_afford(REFINERY):
                    vgs = self.state.vespene_geyser.closer_than(20.0, cc)
                    for vg in vgs:
                        if self.units(REFINERY).closer_than(1.0, vg).exists:
                            break

                        worker = self.select_build_worker(vg.position)
                        if worker is None:
                            break

                        await self.do(worker.build(REFINERY, vg))
                        break

            if self.units(BARRACKS).ready.exists:
                f = self.units(FACTORY)
                if not f.exists:
                    if self.can_afford(FACTORY):
                        await self.build(FACTORY, near=cc.position.towards(self.game_info.map_center, 8))
                elif f.ready.exists and self.units(STARPORT).amount < 2:
                    if self.can_afford(STARPORT):
                        await self.build(STARPORT, near=cc.position.towards(self.game_info.map_center, 30).random_on_distance(8))
        

    #async def build_workers(self,cc):
    #        await self.do(cc.train(SCV))
    
    #async def build_supply(self,cc):
    #    await self.build(SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center,8))
        
        


        
''' run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Terran, Oli_bot()),
    Computer(Race.Terran, Difficulty.Easy)
    ], realtime=True)  '''

def main():
    sc2.run_game(sc2.maps.get("AbyssalReefLE"), [
        # Human(Race.Terran),
        Bot(Race.Terran, Oli_bot()),
        Computer(Race.Zerg, Difficulty.Easy)
    ], realtime=True)

if __name__ == '__main__':
    main()