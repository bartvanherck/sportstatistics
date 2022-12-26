
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

    def get_shape(self, max_height=900, offset_x=40, offset_y=0, max_size=400):
        offset_lat = max_height - max_size - offset_y
        offset_long = offset_x

        max_right = self.max_coord_longitude - self.min_coord_longitude
        longs = (self.__calculate_coord(l, max_right, max_size) for l in self.points_longitude())
        max_right = self.max_coord_latitude - self.min_coord_latitude
        lats = (self.__calculate_coord(l, max_right, max_size) for l in self.points_latitude())
        
        longs_mapped = [l + offset_long for l in longs]
        lats_mapped = [self.reverse_coordinate(c, max_size) + offset_lat for c in lats]
        path = list(zip(longs_mapped,lats_mapped))
        return path
