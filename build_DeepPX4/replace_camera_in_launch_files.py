#!/usr/bin/env python

## SMALL SCRIPT TO ADJUST WORLD FILES AUTOMATICALLY

import os
import glob
import xml.etree.ElementTree as ET

workdir = "/home/xqsme/DeepPX4/build_DeepPX4/launch/HANNASSCAPES"

worlds = glob.glob(os.path.join(workdir,"*.launch"))

for world in worlds:
    try:
        tree = ET.parse(world)
        root = tree.getroot()
    
    
        for elem in root.iter():
            print(elem.tag)
            if elem.tag == "arg":
                try:
                    new = elem.get("value").replace("iris_triple_depth_camera","HANNAS_iris_triple_depth_camera")
                    elem.set("value",new)
                except:
                    pass
        
        tree.write(world)
    except:
        pass

