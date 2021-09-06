from shapely.geometry import Point, Polygon, LineString
from generate import Generate
from wkt import WKT
from geodaisy import GeoObject
import random
from tqdm import tqdm
import argparse
import time

parser = argparse.ArgumentParser()

parser.add_argument("-v", "--vertices", help="choose number of vertices",
                    type=int, default=500)
parser.add_argument("-f", "--factor", help="choose multiplication factor",
                    type=int, default=100)
parser.add_argument("-s", "--shapes", help="choose number of shapes in wkt",
                    type=int, default=500)
args = parser.parse_args()

generate = Generate(args.factor)
wkt = WKT()

options = ["Point", "Polygon", "LineString"]
# print(random.choice(options))

start_time = time.time()
for i in tqdm(range(args.shapes)):
    option = random.choice(options)
    if (option == "Point"):
        wkt.append(GeoObject(Point(generate.generate_point())))
    elif (option == "LineString"):
        wkt.append(GeoObject(LineString(generate.generate_linestring(args.vertices))))
    else:
        wkt.append(GeoObject(Polygon(generate.generate_polygon(args.vertices))))
print("--- Execution: %s seconds ---" % (time.time() - start_time))

wkt.write_wkt("file.wkt")
wkt.write_geojson("file.geojson")
