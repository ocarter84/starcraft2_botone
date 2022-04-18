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
        self.need_supply_depot = False

class Oli_bot(sc2.BotAI):
    async def on_step(self, iteration):
        count = 0
        if iteration == 50 or iteration == 100:
            print(str(iteration))
        Early_g = Game(iteration)
        cc = (self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND))
        cc = cc.first
        await self.distribute_workers()
        
        if self.workers.amount == 12 and cc.noqueue and self.can_afford(SCV) and cc.noqueue:
            await self.do(cc.train(SCV))
        
        if self.workers.amount > 12 and self.already_pending(SUPPLYDEPOT) and self.can_afford(SCV) and cc.noqueue:
                await self.do(cc.train(SCV))
                
        if self.units(UnitTypeId.SCV).amount < 18 and self.units(SUPPLYDEPOT).exists and self.can_afford(SCV) and self.units(UnitTypeId.BARRACKS).ready.amount < 1 and cc.noqueue:
                await self.do(cc.train(SCV))
        
        #build first refinery
        if self.units(REFINERY).amount < 1 and self.already_pending(UnitTypeId.BARRACKS) > 0:
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
                
        #Move additional SCVs to new refinery
        if self.units(REFINERY).amount > 0 and self.units(REFINERY).amount < 3:
            gasTags = [x.tag for x in self.state.units.vespene_geyser]
            rfs = self.units(REFINERY).closer_than(20.0, cc)
            for rf in rfs:
                worker = self.select_build_worker(rf.position)
                if worker is None:
                    break
                await self.do(worker.gather(rf))
                #await self.do(worker.gather(self.units(REFINERY).closer_than(20.0, cc)))
                break
            for x in self.workers.closer_than(10, cc):
                #print(type(x))
                try: 
                    #x.orders[0].ability.id in [AbilityId.HARVEST_GATHER]
                    if x.orders[0].target in gasTags:
                        count = count + 1
                except Exception as e:
                    print("Error: "+str(e))
                    
                
            
        #build second refinery after second supply depot has started.
        if self.units(REFINERY).amount > 0:
            ''' for th in self.townhalls:
                vgs = self.state.vespene_geyser.closer_than(10, th)
                for vg in vgs:
                    if await self.can_place(UnitTypeId.REFINERY, vg.position) and self.can_afford(UnitTypeId.REFINERY):
                        ws = self.workers.gathering
                        if ws.exists: # same condition as above
                            w = ws.closest_to(vg)
                            # caution: the target for the refinery has to be the vespene geyser, not its position!
                            w.build(UnitTypeId.REFINERY, vg) '''
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
        
        
        #Build Second Supply Depot 
        if self.can_afford(SUPPLYDEPOT) and self.already_pending(BARRACKS) == 1 and not self.already_pending(SUPPLYDEPOT): 
            await self.build(SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center,8))
            
        #Build First Supply Depot
        if self.supply_left < 3 and self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT): 
            await self.build(SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center,8))
            
        # send workers to mine from gas
        if iteration % 50 == 0:
            rfs = self.units(REFINERY).closer_than(20.0, cc)
            for rf in rfs:
                print("{0} of {1}".format(str(rf),str(len(rfs))))
                print(str(rf.assigned_harvesters))
            #print("SCVs on Gas = "+str(count))
        '''     print("IN Distribute Workers func iteration: "+str(iteration))
            await self.distribute_workers() '''
            
        
                
        ''' 
        if self.supply_left < 3 and self.supply_used > 22 and self.can_afford(SUPPLYDEPOT): 
            await self.build(SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center,8))
         '''
        if self.units(SUPPLYDEPOT).exists:
            if not self.units(BARRACKS).exists:
                if self.can_afford(BARRACKS):
                    await self.build(BARRACKS, near=cc.position.towards(self.game_info.map_center, 8))

            ''' elif self.units(BARRACKS).exists and self.units(REFINERY).amount < 2:
                if self.can_afford(REFINERY):
                    vgs = self.state.vespene_geyser.closer_than(20.0, cc)
                    for vg in vgs:
                        if self.units(REFINERY).closer_than(1.0, vg).exists:
                            break

                        worker = self.select_build_worker(vg.position)
                        if worker is None:
                            break

                        await self.do(worker.build(REFINERY, vg))
                        break '''

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
        
    # distribute workers function rewritten, the default distribute_workers() function did not saturate gas quickly enough
    async def distribute_workers(self, performanceHeavy=True, onlySaturateGas=True):
        # expansion_locations = self.expansion_locations
        #owned_expansions = self.owned_expansions
        mineralTags = [x.tag for x in self.state.units.mineral_field]
        gasTags = [x.tag for x in self.state.units.vespene_geyser]
        geyserTags = [x.tag for x in self.geysers]

        workerPool = self.units & []
        workerPoolTags = set()

        # find all geysers that have surplus or deficit
        deficitGeysers = {}
        surplusGeysers = {}
        for g in self.geysers.filter(lambda x:x.vespene_contents > 0):
            # only loop over geysers that have still gas in them
            deficit = g.ideal_harvesters - g.assigned_harvesters
            if deficit > 0:
                deficitGeysers[g.tag] = {"unit": g, "deficit": deficit}
            elif deficit < 0:
                surplusWorkers = self.workers.closer_than(10, g).filter(lambda w:w not in workerPoolTags and len(w.orders) == 1 and w.orders[0].ability.id in [AbilityId.HARVEST_GATHER] and w.orders[0].target in geyserTags)
                # workerPool.extend(surplusWorkers)
                for i in range(-deficit):
                    if surplusWorkers.amount > 0:
                        w = surplusWorkers.pop()
                        workerPool.append(w)
                        workerPoolTags.add(w.tag)
                surplusGeysers[g.tag] = {"unit": g, "deficit": deficit}

        # find all townhalls that have surplus or deficit
        deficitTownhalls = {}
        surplusTownhalls = {}
        if not onlySaturateGas:
            for th in self.townhalls:
                deficit = th.ideal_harvesters - th.assigned_harvesters
                if deficit > 0:
                    deficitTownhalls[th.tag] = {"unit": th, "deficit": deficit}
                elif deficit < 0:
                    #surplusWorkers = self.workers.closer_than(10, th).filter(lambda w:w.tag not in workerPoolTags and len(w.orders) == 1 and w.orders[0].ability.id in [AbilityId.HARVEST_GATHER] and w.orders[0].target in mineralTags)
                    surplusWorkers = self.workers.closer_than(10, th)
                    # workerPool.extend(surplusWorkers)
                    for i in range(-deficit):
                        if surplusWorkers.amount > 0:
                            w = surplusWorkers.pop()
                            workerPool.append(w)
                            workerPoolTags.add(w.tag)
                    surplusTownhalls[th.tag] = {"unit": th, "deficit": deficit}
            
            #Adding here 4/17/2022 trying to get just 2 addl workers to the first refinery
            surplusWorkers = self.workers.closer_than(10, th)
            w = surplusWorkers.pop()
            workerPool.append(w)
            workerPoolTags.add(w.tag)
            if all([len(deficitGeysers) == 0, len(surplusGeysers) == 0, len(surplusTownhalls) == 0 or deficitTownhalls == 0]):
                # cancel early if there is nothing to balance
                return

        # check if deficit in gas less or equal than what we have in surplus, else grab some more workers from surplus bases
        deficitGasCount = sum(gasInfo["deficit"] for gasTag, gasInfo in deficitGeysers.items() if gasInfo["deficit"] > 0)
        surplusCount = sum(-gasInfo["deficit"] for gasTag, gasInfo in surplusGeysers.items() if gasInfo["deficit"] < 0)
        surplusCount += sum(-thInfo["deficit"] for thTag, thInfo in surplusTownhalls.items() if thInfo["deficit"] < 0)

        if deficitGasCount - surplusCount > 0:
            # grab workers near the gas who are mining minerals
            for gTag, gInfo in deficitGeysers.items():
                if workerPool.amount >= deficitGasCount:
                    break
                workersNearGas = self.workers.closer_than(10, gInfo["unit"]).filter(lambda w:w.tag not in workerPoolTags and len(w.orders) == 1 and w.orders[0].ability.id in [AbilityId.HARVEST_GATHER] and w.orders[0].target in mineralTags)
                while workersNearGas.amount > 0 and workerPool.amount < deficitGasCount:
                    w = workersNearGas.pop()
                    workerPool.append(w)
                    workerPoolTags.add(w.tag)

        # now we should have enough workers in the pool to saturate all gases, and if there are workers left over, make them mine at townhalls that have mineral workers deficit
        for gTag, gInfo in deficitGeysers.items():
            if performanceHeavy:
                # sort furthest away to closest (as the pop() function will take the last element)
                workerPool.sort(key=lambda x:x.distance_to(gInfo["unit"]), reverse=True)
                #print("Worker pool: "+str(workerPool))
            for i in range(gInfo["deficit"]):
                if workerPool.amount > 0:
                    w = workerPool.pop()
                    #print("type of w: "+str(type(w)))
                    if len(w.orders) == 1:
                        #w.gather(gInfo["unit"], queue=True)
                        w.gather(gInfo["unit"])
                    else:
                        w.gather(gInfo["unit"])
                        #testing here
                        w.gather(gInfo["unit"], queue=True)

        if not onlySaturateGas:
            # if we now have left over workers, make them mine at bases with deficit in mineral workers
            for thTag, thInfo in deficitTownhalls.items():
                if performanceHeavy:
                    # sort furthest away to closest (as the pop() function will take the last element)
                    workerPool.sort(key=lambda x:x.distance_to(thInfo["unit"]), reverse=True)
                for i in range(thInfo["deficit"]):
                    if workerPool.amount > 0:
                        w = workerPool.pop()
                        mf = self.state.mineral_field.closer_than(10, thInfo["unit"]).closest_to(w)
                        if len(w.orders) == 1 and w.orders[0].ability.id in [AbilityId.HARVEST_RETURN]:
                            w.gather(mf, queue=True)
                        else:
                            w.gather(mf)


        
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