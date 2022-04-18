#created 4/15/2022 from sentdex youtube tutorial https://www.youtube.com/watch?v=5U2WdZxJhEE
# on 4/18/2022 realized that DentosalSc2 library was old, 2 years. so uninstalled and started on BurnySc2
#https://github.com/BurnySc2/python-sc2/issues/4 - for major changes
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import random

from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.position import Point2, Point3
from sc2.unit import Unit
from sc2.units import Units



class Supply_depot():
    def __init__(self,time):
        self.time_built = time 

class Game():
    def __init__(self,time):
        self.iteration = time
        self.supply_depots = 0
        self.workers = 0
        self.need_supply_depot = False
    

        

class Oli_bot(BotAI):
    async def on_step(self, iteration):
        count = 0
        if iteration == 50 or iteration == 100:
            print(str(iteration))
        Early_g = Game(iteration)
        cc = (self.structures(UnitTypeId.COMMANDCENTER))
        cc = cc.first
        await self.distribute_workers()
        
        if self.workers.amount == 12 and cc.noqueue and self.can_afford(UnitTypeId.SCV) and cc.is_idle:
            #await self.do(cc.train(UnitTypeId.SCV))
            self.do(cc.train(UnitTypeId.SCV))
        
        if self.workers.amount > 12 and self.already_pending(UnitTypeId.SUPPLYDEPOT) and self.can_afford(UnitTypeId.SCV) and cc.noqueue:
                await self.do(cc.train(UnitTypeId.SCV))
                
        if self.units(UnitTypeId.SCV).amount < 18 and self.structures(UnitTypeId.SUPPLYDEPOT).exists and self.can_afford(UnitTypeId.SCV) and self.structures(UnitTypeId.BARRACKS).ready.amount < 1 and cc.noqueue:
                await self.do(cc.train(UnitTypeId.SCV))
                
        # Raise depos when enemies are nearby
        for depo in self.structures(UnitTypeId.SUPPLYDEPOT).ready:
            for unit in self.known_enemy_units.not_structure:
                if unit.position.to2.distance_to(depo.position.to2) < 15:
                    break
            else:
                await self.do(depo(UnitTypeId.MORPH_SUPPLYDEPOT_LOWER))

        # Lower depos when no enemies are nearby
        for depo in self.structures(UnitTypeId.SUPPLYDEPOTLOWERED).ready:
            for unit in self.known_enemy_units.not_structure:
                if unit.position.to2.distance_to(depo.position.to2) < 10:
                    await self.do(depo(UnitTypeId.MORPH_SUPPLYDEPOT_RAISE))
                    break
        
        #build first refinery
        if self.structures(UnitTypeId.REFINERY).amount < 1 and self.already_pending(UnitTypeId.BARRACKS) > 0:
            if self.can_afford(UnitTypeId.REFINERY):
                vgs = self.state.vespene_geyser.closer_than(20.0, cc)
                for vg in vgs:
                    if self.structures(UnitTypeId.REFINERY).closer_than(1.0, vg).exists:
                        break

                    worker = self.select_build_worker(vg.position)
                    if worker is None:
                        break
                    
                    if self.can_afford(UnitTypeId.REFINERY):
                        await self.do(worker.build(UnitTypeId.REFINERY, vg))
                        break
                
        #Move additional SCVs to new refinery
        if self.structures(UnitTypeId.REFINERY).amount > 0:
            rfs = self.structures(UnitTypeId.REFINERY).closer_than(20.0, cc)
            for rf in rfs:
                if rf.assigned_harvesters < 3:
                    gasTags = [x.tag for x in self.state.units.vespene_geyser]
                    rfs = self.structures(UnitTypeId.REFINERY).closer_than(20.0, cc)
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
        if self.structures(UnitTypeId.REFINERY).amount > 0:
            ''' for th in self.townhalls:
                vgs = self.state.vespene_geyser.closer_than(10, th)
                for vg in vgs:
                    if await self.can_place(UnitTypeId.REFINERY, vg.position) and self.can_afford(UnitTypeId.REFINERY):
                        ws = self.workers.gathering
                        if ws.exists: # same condition as above
                            w = ws.closest_to(vg)
                            # caution: the target for the refinery has to be the vespene geyser, not its position!
                            w.build(UnitTypeId.REFINERY, vg) '''
            if self.can_afford(UnitTypeId.REFINERY):
                vgs = self.state.vespene_geyser.closer_than(20.0, cc)
                for vg in vgs:
                    if self.structures(UnitTypeId.REFINERY).closer_than(1.0, vg).exists:
                        break

                    worker = self.select_build_worker(vg.position)
                    if worker is None:
                        break
                    
                    if self.can_afford(UnitTypeId.REFINERY):
                        await self.do(worker.build(UnitTypeId.REFINERY, vg))
                        break
        
        
        ''' #Build Second Supply Depot 
        if self.can_afford(SUPPLYDEPOT) and self.already_pending(BARRACKS) == 1 and not self.already_pending(SUPPLYDEPOT): 
            await self.build(SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center,8))
            
        #Build First Supply Depot
        if self.supply_left < 3 and self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT): 
            await self.build(SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center,8)) '''
        
        depot_placement_positions = self.main_base_ramp.corner_depots
        # Uncomment the following if you want to build 3 supplydepots in the wall instead of a barracks in the middle + 2 depots in the corner
        # depot_placement_positions = self.main_base_ramp.corner_depots | {self.main_base_ramp.depot_in_middle}

        barracks_placement_position = None
        barracks_placement_position = self.main_base_ramp.barracks_correct_placement
        # If you prefer to have the barracks in the middle without room for addons, use the following instead
        # barracks_placement_position = self.main_base_ramp.barracks_in_middle

        depots = self.structures(UnitTypeId.SUPPLYDEPOT) | self.structures(UnitTypeId.SUPPLYDEPOTLOWERED)

        # Filter locations close to finished supply depots
        if depots:
            depot_placement_positions = {d for d in depot_placement_positions if depots.closest_distance_to(d) > 1}

        # Build depots
        if self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
            if len(depot_placement_positions) == 0:
                return
            # Choose any depot location
            target_depot_location = depot_placement_positions.pop()
            ws = self.workers.gathering
            if ws: # if workers were found
                w = ws.random
                #await self.do(w.build(UnitTypeId.SUPPLYDEPOT, target_depot_location))
                self.do(cc.build(UnitTypeId.SUPPLYDEPOT, target_depot_location))

        # Build barracks
        if depots.ready.exists and self.can_afford(UnitTypeId.BARRACKS) and not self.already_pending(UnitTypeId.BARRACKS):
            if self.structures(UnitTypeId.BARRACKS).amount + self.already_pending(UnitTypeId.BARRACKS) > 0:
                return
            ws = self.workers.gathering
            if ws and barracks_placement_position: # if workers were found
                w = ws.random
                await self.do(w.build(UnitTypeId.BARRACKS, barracks_placement_position))

        #Build Reactor
        if self.units(UnitTypeId.BARRACKS).exists:
            for brks_react in self.units(UnitTypeId.BARRACKS).ready:
                await self.do(brks_react.build(UnitTypeId.BARRACKSREACTOR))
        
                
        if self.structures(UnitTypeId.BARRACKSREACTOR).exists:
            for brks_react2 in self.structures(UnitTypeId.BARRACKS).ready:
                brks_react2.train(MARINE, 2)
        ### MARINE MICRO REFERNCE FOR LATER: https://github.com/Dentosal/python-sc2/blob/master/examples/arcade_bot.py
        
        if self.structures(UnitTypeId.BARRACKSTECHLAB).ready.exists and self.structures(UnitTypeId.BARRACKS).amount < 2:
            for react in self.structures(UnitTypeId.BARRACKS).ready:
                abilities = await self.get_available_abilities(UnitTypeId.lab)
                if AbilityId.RESEARCH_COMBATSHIELD in abilities and \
                    self.can_afford(AbilityId.RESEARCH_COMBATSHIELD):
                    await self.do(UnitTypeId.lab(AbilityId.RESEARCH_COMBATSHIELD))

            
        # send workers to mine from gas
        ''' if iteration % 500 == 0:
            print(str(self.units(REFINERY).amount)) '''
            
            #print("SCVs on Gas = "+str(count))
        '''     print("IN Distribute Workers func iteration: "+str(iteration))
            await self.distribute_workers() '''
            
        
                
        ''' 
        if self.supply_left < 3 and self.supply_used > 22 and self.can_afford(SUPPLYDEPOT): 
            await self.build(SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center,8))
         '''
        #original build baracks 
        ''' if self.units(SUPPLYDEPOT).exists:
            if not self.units(BARRACKS).exists:
                if self.can_afford(BARRACKS):
                    await self.build(BARRACKS, near=cc.position.towards(self.game_info.map_center, 8)) '''



        if self.structures(UnitTypeId.BARRACKS).ready.exists and not self.already_pending(UnitTypeId.FACTORY):
            f = self.structures(UnitTypeId.FACTORY)
            if not f.exists:
                if self.can_afford(UnitTypeId.FACTORY):
                    await self.build(UnitTypeId.FACTORY, near=cc.position.towards(self.game_info.map_center, 3))
            elif f.ready.exists and self.units(UnitTypeId.STARPORT).amount < 2:
                if self.can_afford(UnitTypeId.STARPORT):
                    await self.build(UnitTypeId.STARPORT, near=cc.position.towards(self.game_info.map_center, 30).random_on_distance(3))
        

    #async def build_workers(self,cc):
    #        await self.do(cc.train(SCV))
    
    #async def build_supply(self,cc):
    #    await self.build(SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center,8))
        
    ''' # distribute workers function rewritten, the default distribute_workers() function did not saturate gas quickly enough
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
 '''

        
''' run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Terran, Oli_bot()),
    Computer(Race.Terran, Difficulty.Easy)
    ], realtime=True)  '''

''' def main():
    sc2.run_game(sc2.maps.get("AbyssalReefLE"), [
        # Human(Race.Terran),
        Bot(Race.Terran, Oli_bot()),
        Computer(Race.Zerg, Difficulty.Easy)
    ], realtime=False)

if __name__ == '__main__':
    main() '''

def main():
    map = random.choice(
        [
            # Most maps have 2 upper points at the ramp (len(self.main_base_ramp.upper) == 2)
            "AutomatonLE",
            "BlueshiftLE",
            "CeruleanFallLE",
            "KairosJunctionLE",
            "ParaSiteLE",
            "PortAleksanderLE",
            "StasisLE",
            "DarknessSanctuaryLE",
            "ParaSiteLE",  # Has 5 upper points at the main ramp
            "AcolyteLE",  # Has 4 upper points at the ramp to the in-base natural and 2 upper points at the small ramp
            "HonorgroundsLE",  # Has 4 or 9 upper points at the large main base ramp
        ]
    )
    map = "PillarsofGoldLE"
    run_game(
        maps.get("Abyssal Reef LE"),
        [Bot(Race.Terran, Oli_bot()), Computer(Race.Zerg, Difficulty.Easy)],
        realtime=True,
        # sc2_version="4.10.1",
    )


if __name__ == "__main__":
    main()