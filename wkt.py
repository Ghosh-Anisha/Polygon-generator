import geodaisy.converters as convert
import json

class WKT:
    __wkt = []
    __geojson = {}

    def __init__(self):
        self.__wkt = []
        self.__geojson = {}

    def append(self, obj):
        self.__wkt.append(obj)
        return

    def get_geojson(self, index):
        return convert.wkt_to_geojson(self.__wkt[index].wkt())

    def len(self):
        return len(self.__wkt)

    def write_wkt(self, filename):
        f = open(filename, "w")
        for obj in self.__wkt:
            f.write(obj.wkt())
            f.write("\n")
        f.close()

    def write_geojson(self, filename):
        self.__geojson = {"type": "FeatureCollection", "features":[]}
        for i in range(len(self.__wkt)):
            obj = convert.wkt_to_geojson(self.__wkt[i].wkt())
            geojsonobj = {
                "type": "Feature",
                "geometry": json.loads(obj)
            }
            self.__geojson["features"].append(geojsonobj)
        with open(filename, 'w') as f:
            json.dump(self.__geojson, f)
        return
