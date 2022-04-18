#created 4/15/2022 from sentdex youtube tutorial https://www.youtube.com/watch?v=5U2WdZxJhEE

import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer

class Oli_bot(sc2.BotAI):
    async def on_step(self, iteration):
        await self.distribute_workers()
        
run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Terran, Oli_bot()),
    Computer(Race.Terran, Difficulty.Easy)
    ], realtime=True) 