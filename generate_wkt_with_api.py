import requests
import json
from shapely.geometry import Point, Polygon, LineString
from wkt import WKT
from geodaisy import GeoObject
import pandas as pd
from tqdm import tqdm

URL = "https://developers.google.com/maps/documentation/javascript/examples/json/states.json"
r = requests.get(URL)
gj = json.loads(r.text)

google_dict = {"GEO_ID":[], "STATE":[], "NAME":[], "CENSUSAREA":[], "gx_id":[], "TYPE":[], "COORDINATES":[]}

wkt = WKT()
for i in tqdm(range(len(gj["features"]))):
    google_dict["GEO_ID"].append(gj["features"][i]["properties"]["GEO_ID"])
    google_dict["STATE"].append(gj["features"][i]["properties"]["STATE"])
    google_dict["NAME"].append(gj["features"][i]["properties"]["NAME"])
    google_dict["CENSUSAREA"].append(gj["features"][i]["properties"]["CENSUSAREA"])
    google_dict["gx_id"].append(gj["features"][i]["properties"]["gx_id"])

    google_dict["TYPE"].append(gj["features"][i]["geometry"]["type"])
    google_dict["COORDINATES"].append(gj["features"][i]["geometry"]["coordinates"][0])


    if (gj["features"][i]["geometry"]["type"] == "Polygon"):
        wkt.append(GeoObject(Polygon(gj["features"][i]["geometry"]["coordinates"][0])))
    if (gj["features"][i]["geometry"]["type"] == "LineString"):
        wkt.append(GeoObject(LineString(gj["features"][i]["geometry"]["coordinates"][0])))
    if (gj["features"][i]["geometry"]["type"] == "Point"):
        wkt.append(GeoObject(Point(gj["features"][i]["geometry"]["coordinates"][0])))
wkt.write_wkt("google.wkt")
df = pd.DataFrame(google_dict)
df.to_csv("google.csv")
