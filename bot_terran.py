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
        if Early_g.supply_depots == 0:
            if self.workers.amount < 22 and cc.noqueue:
                await self.do(cc.train(SCV))
        if self.supply_left < 3 and self.can_afford(SUPPLYDEPOT): 
            print("Supply Depots: "+str(self.supply_depots))
            await self.build_supply(cc,Early_g)
        if self.can_afford(SCV):
            await self.build_workers(cc)
                
            
    
    async def build_workers(self,cc):
        if self.workers.amount < 22 and cc.noqueue:
            await self.do(cc.train(SCV))
    
    async def build_supply(self,cc,Early_g):
        await self.build(SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center,8))
        Early_g.supply_depots += 1


        
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