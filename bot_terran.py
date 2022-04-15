#created 4/15/2022 from sentdex youtube tutorial https://www.youtube.com/watch?v=5U2WdZxJhEE

#import sc2
#from sc2 import run_game, maps, Race, Difficulty
#from sc2.player import Bot, Computer


import random

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.player import Human

class Oli_bot(sc2.BotAI):
    async def on_step(self, iteration):
        await self.distribute_workers()
        await self.build_workers()
    
    async def build_workers(self):
        #for cc in self.units(COMMANDCENTER).ready.noqueue:
        #for cc in self.townhalls.ready.random:
        if self.can_afford(SCV) and self.workers.amount < 22 and cc.noqueue:
            await self.do(cc.train(SCV))
        commandcenter = self.townhalls.ready.random
        if self.can_afford(SCV):
            await self.do(cc.train(SCV))
        
run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Terran, Oli_bot()),
    Computer(Race.Terran, Difficulty.Easy)
    ], realtime=True) 