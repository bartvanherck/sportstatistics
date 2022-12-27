
class Traces(object):
    def __init__(self):
        self.points = list()
        self.min_coord_longitude = None
        self.max_coord_longitude = None
        self.min_coord_latitude = None
        self.max_coord_latitude = None
    
    def insert(self, item):
        if item.value is not None:
            self.points.append(item)
            self.initialize_min_max(item.value)
            self.set_max_min_values(item.value)
    
    def __calculate_coord(self, c, m, l):
        return int(c / m * l)

    def initialize_min_max(self, item):
        if self.min_coord_latitude is None:
            self.min_coord_latitude = item["latitude"]
        if self.max_coord_latitude is None:
            self.max_coord_latitude = item["latitude"]
        if self.min_coord_longitude is None:
            self.min_coord_longitude = item["longitude"]
        if self.max_coord_longitude is None:
            self.max_coord_longitude = item["longitude"]

    def set_max_min_values(self,item):
        if item["latitude"] < self.min_coord_latitude:
            self.min_coord_latitude = item["latitude"]
        if item["latitude"] > self.max_coord_latitude:
            self.max_coord_latitude = item["latitude"]
        if item["longitude"] < self.min_coord_longitude:
            self.min_coord_longitude = item["longitude"]
        if item["longitude"] > self.max_coord_longitude:
            self.max_coord_longitude = item["longitude"]

    def points_longitude(self):
        points = [p.value for p in self.points]
        return [p["longitude"]-self.min_coord_longitude for p in points if p is not None]

    def points_latitude(self):
        points = [p.value for p in self.points]
        return [p["latitude"]-self.min_coord_latitude for p in points if p is not None]

    def reverse_coordinate(self, c, max_coord):
        mapper = list(range(max_coord,-1,-1))
        return mapper[c]

    def get_max_coordinate_from_trace(self):
        points_long = self.points_longitude()
        points_lat = self.points_latitude()
        if max(points_lat) > max(points_long):
            return self.max_coord_latitude - self.min_coord_latitude
        else:
            return self.max_coord_longitude - self.min_coord_longitude

    def get_shape(self, max_height=900, offset_x=40, offset_y=0, max_size=500):
        offset = dict(lat=max_height - max_size -offset_y, long=offset_x)
        max_coord = self.get_max_coordinate_from_trace()
        all_coord_long = (self.__calculate_coord(l, max_coord, max_size) for l in self.points_longitude())
        all_coord_lat = (self.__calculate_coord(l, max_coord, max_size) for l in self.points_latitude())

        shifted_coord_long = (l + offset["long"] for l in all_coord_long)
        shifted_coord_lat = (self.reverse_coordinate(l, max_size) + offset["lat"] for l in all_coord_lat)

        return list(zip(shifted_coord_long, shifted_coord_lat))
