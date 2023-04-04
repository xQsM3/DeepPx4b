import os
import glob
import sys
import pandas as pd

class Evaluator:
    def __init__(self,bagfile_path,worldfile_path):
        self.bagfiles = glob.glob(os.path.join(bagfile_path,"*.*"))
        self.worldfiles = glob.glob(os.path.join(worldfile_path,"*.*"))


    def generate_numerical_code(self,bag):
        print(f"bag: {bag}")
        if "city" in bag:
            world = self.get_world(bag,"city")
            return self.decode_cities(world)
        elif "simple" in bag:
            world = self.get_world(bag,"simple")
            print(world)
            return self.decode_simple(world)
        elif "natural" in bag:
            world = self.get_world(bag,"natural")
            return self.decode_natural(world)

    def decode_cities(self,world):
        first = 1
        second = self.get_variable(world,"width_street_") # width street
        third = self.get_variable(world,"number_streets_") # amount of streets
        fourth = self.get_variable(world,"building_range_") # building height ?
        fifth = 0 # distance obst / goal
        return [first,second,third,fourth,fifth]
    def decode_simple(self,world):
        first = 2
        second = self.get_variable(world,"#obst_")
        third = self.get_variable(world,"obstwidth_"),self.get_variable(world,"obsthight_")
        third = int( str(third[0])+str(third[1]) )
        fourth = self.get_variable(world,"space_")
        fifth = self.get_variable(world,"elev_")
        sixth = 0 #distance to goal
        return [first,second,third,fourth,fifth,sixth]

    def decode_natural(self,world):
        first = 3
        second = self.get_variable(world,"density_")
        third = self.get_variable(world,"terrain_")
        fourth = 0
        return [first,second,third,fourth]

    def get_variable(self,file,name):
        #print(file)
        file = os.path.basename(file).split(".world")[0].split(".launch")[0]
        #print(file,name)
        return int(float(file.split(name)[-1].split("_")[0] ))

    def get_world(self,bag,maintype):
        print("###")
        index = int(self.get_variable(bag,f"{maintype}_obst_") )
        search = f"{maintype}_obst_" + str(index) # create search string for worlds
        #if not search in self.worldfiles:
        #    raise FileNotFoundError(f"worldfile {search} not found")
        for world in self.worldfiles:
            if str(search) in world:
                break
        return world


    def evaluate(self):
        full_evaluation = {}
        sub_evaluation = {}
        for bag in self.bagfiles:
            # add sim to full evaluation
            num_code = self.generate_numerical_code(bag)
            self.add_sim(bag, str(num_code), full_evaluation)
            # add sim to evaluation categorised in subworldtypes
            subworldtype = self.categories_subtype(num_code)
            self.add_sim(bag, "all", sub_evaluation)
            self.add_sim(bag,subworldtype,sub_evaluation)

        #pd.set_option('max_columns', None)
        pd.set_option('display.max_columns', 100)
        return pd.DataFrame.from_dict(full_evaluation),pd.DataFrame.from_dict(sub_evaluation)

    def categories_subtype(self,num_code):
        if num_code[0] == 3:
            return "natural"
        if num_code[0] == 2:
            return "simple"
        if num_code[0] == 1:
            if num_code[3] == 1:
                return "city_small"
            if num_code[3] == 2:
                return "city_medium"
            if num_code[3] == 3:
                return "city_tall"
    def add_sim(self,bag, row, evaluation):
        if not row in evaluation:
            evaluation[row] = {"total": 0, "failed": 0, "failure_prop": None}

        evaluation[row]["total"] += 1
        error = True if "error" in bag else False
        if error: evaluation[row]["failed"] += 1

        evaluation[row]["failure_prop"] = 100 * evaluation[row]["failed"] / evaluation[row]["total"]

if __name__ == "__main__":
    bagfile_path = sys.argv[1] # path to bagfiles to be evaluated
    worldfile_path = sys.argv[2]

    eval = Evaluator(bagfile_path,worldfile_path)
    print(eval.evaluate()[1] )
