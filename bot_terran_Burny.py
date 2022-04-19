#created 4/15/2022 from sentdex youtube tutorial https://www.youtube.com/watch?v=5U2WdZxJhEE
# on 4/18/2022 realized that DentosalSc2 library was old, 2 years. so uninstalled and started on BurnySc2
#https://github.com/BurnySc2/python-sc2/issues/4 - for major changes
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

import random

from typing import Set

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



class Oli_bot(BotAI):
    def __init__(self):
        self.unit_command_uses_self_do = False
        self.Flag = True
        
    async def on_step(self, iteration):
        
        cc = (self.structures(UnitTypeId.COMMANDCENTER))
        cc = cc.first
        await self.distribute_workers()
        
        if self.workers.amount == 12 and self.can_afford(UnitTypeId.SCV) and cc.is_idle:
            #await self.do(cc.train(UnitTypeId.SCV))
            self.do(cc.train(UnitTypeId.SCV))
        
        if self.workers.amount < 15 and self.already_pending(UnitTypeId.SUPPLYDEPOT) and self.can_afford(UnitTypeId.SCV) and cc.is_idle:
            self.do(cc.train(UnitTypeId.SCV))
                
        if self.units(UnitTypeId.SCV).amount < 21 and self.structures(UnitTypeId.SUPPLYDEPOT).ready.amount > 0 \
            and self.already_pending(UnitTypeId.SUPPLYDEPOT) and self.already_pending(UnitTypeId.BARRACKS) \
            and self.can_afford(UnitTypeId.SCV) and cc.is_idle:
            self.do(cc.train(UnitTypeId.SCV))
                
        # Raise depos when enemies are nearby                
        for depo in self.structures(UnitTypeId.SUPPLYDEPOT).ready:
            for unit in self.enemy_units:
                if unit.distance_to(depo) < 15:
                    break
            else:
                depo(AbilityId.MORPH_SUPPLYDEPOT_LOWER)

        # Lower depos when no enemies are nearby
        for depo in self.structures(UnitTypeId.SUPPLYDEPOTLOWERED).ready:
            for unit in self.enemy_units:
                if unit.distance_to(depo) < 10:
                    depo(AbilityId.MORPH_SUPPLYDEPOT_RAISE)
                    break
        
        #build first refinery
        if self.can_afford(UnitTypeId.REFINERY) and self.already_pending(UnitTypeId.BARRACKS) and self.already_pending(UnitTypeId.REFINERY) == 0:
            vgs: Units = self.vespene_geyser.closer_than(20, cc)
            for vg in vgs:
                if self.gas_buildings.filter(lambda unit: unit.distance_to(vg) < 1):
                    break

                worker: Unit = self.select_build_worker(vg.position)
                if worker is None:
                    break

                worker.build(UnitTypeId.REFINERY, vg)
                print("!!!!! Build Refinery 1")
                break
        
        #build second refinery
        if self.can_afford(UnitTypeId.REFINERY) and self.structures(UnitTypeId.BARRACKS).ready.amount == 0  and self.already_pending(UnitTypeId.REFINERY) == 0:
            vgs: Units = self.vespene_geyser.closer_than(20, cc)
            for vg in vgs:
                if self.gas_buildings.filter(lambda unit: unit.distance_to(vg) < 1):
                    break

                worker: Unit = self.select_build_worker(vg.position)
                if worker is None:
                    break

                worker.build(UnitTypeId.REFINERY, vg)
                print("!!!!! Build Refinery 1")
                break
        ''' #build second refinery
        if self.can_afford(UnitTypeId.REFINERY) and self.structures(UnitTypeId.SUPPLYDEPOT).ready.amount > 1 and self.already_pending(UnitTypeId.BARRACKS):
                    vgs: Units = self.vespene_geyser.closer_than(20, cc)
                    for vg in vgs:
                        if self.gas_buildings.filter(lambda unit: unit.distance_to(vg) < 1):
                            break

                        worker: Unit = self.select_build_worker(vg.position)
                        if worker is None:
                            break

                        worker.build(UnitTypeId.REFINERY, vg)
                        break
         '''            
                
        #Move additional SCVs to new refinery
        if self.structures(UnitTypeId.REFINERY).amount > 0:
            rfs = self.structures(UnitTypeId.REFINERY).closer_than(20.0, cc)
            for rf in rfs:
                if rf.assigned_harvesters < 3:
                    #gasTags = [x.tag for x in self.state.units.vespene_geyser]
                    rfs = self.structures(UnitTypeId.REFINERY).closer_than(20.0, cc)
                    for rf in rfs:
                        worker = self.select_build_worker(rf.position)
                        if worker is None:
                            break
                        self.do(worker.gather(rf))
                        #await self.do(worker.gather(self.units(REFINERY).closer_than(20.0, cc)))
                        break
                    ''' for x in self.workers.closer_than(10, cc):
                        #print(type(x))
                        try: 
                            #x.orders[0].ability.id in [AbilityId.HARVEST_GATHER]
                            if x.orders[0].target in gasTags:
                                count = count + 1
                        except Exception as e:
                            print("Error: "+str(e)) '''
                    
        
        ''' #Build Second Supply Depot 
        if self.can_afford(SUPPLYDEPOT) and self.already_pending(BARRACKS) == 1 and not self.already_pending(SUPPLYDEPOT): 
            await self.build(SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center,8))
            
        #Build First Supply Depot
        if self.supply_left < 3 and self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT): 
            await self.build(SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center,8)) '''
 
        depot_placement_positions: Set[Point2] = self.main_base_ramp.corner_depots
        # Uncomment the following if you want to build 3 supply depots in the wall instead of a barracks in the middle + 2 depots in the corner
        # depot_placement_positions = self.main_base_ramp.corner_depots | {self.main_base_ramp.depot_in_middle}

        barracks_placement_position: Point2 = self.main_base_ramp.barracks_correct_placement
        # If you prefer to have the barracks in the middle without room for addons, use the following instead
        # barracks_placement_position = self.main_base_ramp.barracks_in_middle

        depots: Units = self.structures.of_type({UnitTypeId.SUPPLYDEPOT, UnitTypeId.SUPPLYDEPOTLOWERED})

        # Filter locations close to finished supply depots
        if depots:
            depot_placement_positions: Set[Point2] = {
                d
                for d in depot_placement_positions if depots.closest_distance_to(d) > 1
            }
        if iteration % 50 == 0:
            print(str(iteration))
            print(str(self.minerals))
        
        
        # Get SCV moving towards first depot location
        if self.Flag == True and iteration > 10:
            if self.minerals > 50:
                target_depot_location: Point2 = depot_placement_positions.pop()
                scv_workers = self.units(UnitTypeId.SCV).closer_than(20.0, cc)
                #workers: scv_workers[0]
                if scv_workers:  # if workers were found
                    worker: Unit = scv_workers[0]
                    worker.move(target_depot_location)
                    self.Flag = False
                    #self.do(worker.build(UnitTypeId.SUPPLYDEPOT, target_depot_location))
        
        #Build first Depot with SCV near target build.
        if self.can_afford(UnitTypeId.SUPPLYDEPOT) and self.already_pending(UnitTypeId.SUPPLYDEPOT) == 0 and \
            not self.already_pending(UnitTypeId.BARRACKS):
            ''' if len(depot_placement_positions) < 2:
                return '''
            # Choose any depot location
            target_depot_location: Point2 = depot_placement_positions.pop()
            scv_workers = self.units(UnitTypeId.SCV).closer_than(5.0, target_depot_location)
            workers: Units = scv_workers
            if workers:  # if workers were found
                worker: Unit = workers.random
                self.do(worker.build(UnitTypeId.SUPPLYDEPOT, target_depot_location))
                print("##########DEPOT 1 BUILD")
            
        #Build second Depot with SCV near target build.
        #if self.can_afford(UnitTypeId.SUPPLYDEPOT) and self.structures(UnitTypeId.SUPPLYDEPOT).ready.amount ==1:
        if self.can_afford(UnitTypeId.SUPPLYDEPOT) and self.already_pending(UnitTypeId.BARRACKS) > 0:
            #if self.already_pending(UnitTypeId.BARRACKS) > 0:
            print("Here!!!!!!!!!!")
            if len(depot_placement_positions) == 0:
                #print("Here!!!!2222!!!!!!")
                return
            # Choose any depot location
            target_depot_location: Point2 = depot_placement_positions.pop()
            #workers: Units = self.workers.gathering
            scv_workers = self.units(UnitTypeId.SCV).closer_than(5.0, cc)
            workers: Units = scv_workers
            if workers:  # if workers were found
                worker: Unit = workers.random
                self.do(worker.build(UnitTypeId.SUPPLYDEPOT, target_depot_location))
                print("##########DEPOT 2 BUILD")
                    
        # Build barracks
        if depots.ready and self.can_afford(UnitTypeId.BARRACKS) and self.already_pending(UnitTypeId.BARRACKS) == 0:
            if self.structures(UnitTypeId.BARRACKS).amount + self.already_pending(UnitTypeId.BARRACKS) > 0:
                return
            scv_workers = self.units(UnitTypeId.SCV).closer_than(10.0, barracks_placement_position)
            workers: Units = scv_workers
            if workers:  # if workers were found
                worker: Unit = workers.random
                worker.build(UnitTypeId.BARRACKS, barracks_placement_position)
                print("BARRACKS 1 BUILT!!!")
            else:
                workers: Units = self.workers.gathering
                if workers:  # if workers were found
                    worker: Unit = workers.random
                    worker.build(UnitTypeId.BARRACKS, barracks_placement_position)
                    print("BARRACKS 1a BUILT!!!")
            
            ''' workers = self.workers.gathering
            if workers and barracks_placement_position:  # if workers were found
                worker: Unit = workers.random
                worker.build(UnitTypeId.BARRACKS, barracks_placement_position) '''

        
                
        #Build Reactor
        if self.units(UnitTypeId.BARRACKS).exists:
            for brks_react in self.units(UnitTypeId.BARRACKS).ready:
                brks_react.build(UnitTypeId.BARRACKSREACTOR)
        
                
        if self.structures(UnitTypeId.BARRACKSREACTOR).exists:
            for brks_react2 in self.structures(UnitTypeId.BARRACKS).ready:
                #brks_react2.train(MARINE, 2)
                brks_react2.train(UnitTypeId.MARINE,2)
        ### MARINE MICRO REFERNCE FOR LATER: https://github.com/Dentosal/python-sc2/blob/master/examples/arcade_bot.py
        
    async def on_building_construction_started(self, unit: Unit):
        print(f"Construction of building {unit} started at {unit.position}.")

    async def on_building_construction_complete(self, unit: Unit):
        print(f"Construction of building {unit} completed at {unit.position}.")

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