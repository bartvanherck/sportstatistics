
class FitTrackPoint(object):
    def __init__(self, frame):
        self.value = self.get_single_point_data(frame)

    def get_single_point_data(self, frame):
        data = dict()
        if not(frame.has_field('position_lat') and frame.has_field('position_long')):
            return None
        latitude = frame.get_value('position_lat')
        longitude = frame.get_value('position_long')
        if (latitude is None) or (longitude is None):
            return None
        data["latitude"] = latitude
        data["longitude"] = longitude
        return data
