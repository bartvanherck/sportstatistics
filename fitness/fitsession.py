from enum import Enum

class FitDataType(Enum):
    SESSION = 1
    RECORD = 2

class FitSession(object):
    def __init__(self, frame):
        self.sport = frame.get_value('sport')
        self.elapsed_time = frame.get_value('total_elapsed_time')
        self.distance = frame.get_value('total_distance')
        self.ascent = frame.get_value('total_ascent')
        self.descent = frame.get_value('total_descent')
        self.average_speed = frame.get_value('avg_speed')
        self.start_time = frame.get_value('start_time')

    @property
    def start_day(self):
        return (self.start_time.year, self.start_time.month, self.start_time.day)

    @property
    def distance_in_km(self):
        return self.distance / 1000

    def __str__(self):
        lst = list()
        lst.append(f"Sport:{self.sport}")
        lst.append(f"Time:{self.elapsed_time}")
        lst.append(f"Distance:{self.distance}")
        lst.append(f"Ascent:{self.ascent}")
        lst.append(f"Descent:{self.descent}")
        lst.append(f"Speed:{self.average_speed}")
        lst.append(f"Start time:{self.start_time}")
        return " - ".join(lst)
