from glob import glob
import argparse
import os
import time

def main(args):
    assert args.worldtype in ["city","simple","natural","all"],"worldtype must be either city,simple,nature"
    bags = glob(os.path.join(args.filepath,"*.bag"))
    total_errors, total_simulations = 0,0
    for bag in bags:
        if (args.worldtype in bag) or args.worldtype == "all":
            total_simulations +=1
            if "error" in bag:
                total_errors +=1


    error_rate = (float(total_errors) / total_simulations) * 100
    print("#################################################################")
    print("error rate %       total errors            total simulations")
    print("    {0}                 {1}                       {2}".format(error_rate,total_errors,total_simulations))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='failure propability monitoring')
    parser.add_argument("--filepath",type=str,default="/home/linux123/bagfiles_all_worlds")
    parser.add_argument("--worldtype",type=str)
    args = parser.parse_args()

    while True:
        
        main(args)
	time.sleep(60)
