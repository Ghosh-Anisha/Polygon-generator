import random
from math import atan2

class Generate:
    __factor = 1
    def __init__(self, factor):
        self.__factor = factor
        return
    def __to_random_boolean(self):
        return random.getrandbits(1)

    def __to_vectors_coordinates(self, coordinates, min_coordinate, max_coordinate):
        last_min = last_max = min_coordinate
        result = []
        for coordinate in coordinates:
            if self.__to_random_boolean():
                result.append(coordinate - last_min)
                last_min = coordinate
            else:
                result.append(last_max - coordinate)
                last_max = coordinate
        result.extend((max_coordinate - last_min,
                       last_max - max_coordinate))
        return result

    def generate_polygon(self, vertices_count=10,
                      x_generator=random.random,
                      y_generator=random.random):
        xs = [x_generator() for _ in range(vertices_count)]
        ys = [y_generator() for _ in range(vertices_count)]
        xs = sorted(xs)
        ys = sorted(ys)
        min_x, *xs, max_x = xs
        min_y, *ys, max_y = ys
        vectors_xs = self.__to_vectors_coordinates(xs, min_x, max_x)
        vectors_ys = self.__to_vectors_coordinates(ys, min_y, max_y)
        random.shuffle(vectors_ys)
        def __to_vector_angle(vector):
            x, y = vector
            return atan2(y, x)
        vectors = sorted(zip(vectors_xs, vectors_ys),
                         key=__to_vector_angle)
        point_x = point_y = 0
        min_polygon_x = min_polygon_y = 0
        points = []
        for vector_x, vector_y in vectors:
            points.append((point_x, point_y))
            point_x += vector_x
            point_y += vector_y
            min_polygon_x = min(min_polygon_x, point_x)
            min_polygon_y = min(min_polygon_y, point_y)
        shift_x, shift_y = min_x - min_polygon_x, min_y - min_polygon_y
        result = [((point_x + shift_x)*self.__factor, (point_y + shift_y)*self.__factor)
                for point_x, point_y in points]
        result.append(result[0])
        return result

    def generate_point(self,
                      x_generator=random.random,
                      y_generator=random.random):
        return [x_generator()*self.__factor, y_generator()*self.__factor]

    def generate_linestring(self,
                            vertices_count = 10):
        result = []
        for i in range(vertices_count):
            result.append(tuple(self.generate_point()))
        result.sort(key = lambda a: a[0])
        return result
