from .utils import name_of_month, speed_to_min_km
from collections import Counter, OrderedDict, defaultdict
import datetime

class SportStatistics(object):
    def __init__(self) -> None:
        self.reset()

    def insert(self, session) -> None:
        self.add_session(session)
        self.__sports = list(set([sport for sport,_ in self.sessions]))
        self.__sports.sort()
    
    def reset(self) -> None:
        self.__sports = list()
        self.sessions = list()

    def add_session(self, session) -> None:
        self.sessions.append((session.sport,session))

    def get_number_days(self, sessions) -> int:
        days = set([s.start_day for s in sessions])
        return len(days)
    
    def get_numbers_per_month(self, sessions):
        count = Counter((y,m) for y,m,_ in (s.start_day for s in sessions))
        return OrderedDict(sorted(count.items()))

    def get_distances_per_month(self, sessions):
        dist = defaultdict(int)
        for session in sessions:
            y,m,_ = session.start_day
            dist[(y,m)] += session.distance_in_km
        return OrderedDict(sorted(dist.items()))

    def get_heights_per_month(self, sessions):
        ascents = defaultdict(int)
        for session in sessions:
            y,m,_ = session.start_day
            ascents[(y,m)] += session.ascent
        return OrderedDict(sorted(ascents.items()))

    def get_distance(self, sessions) -> int:
        return sum([s.distance_in_km for s in sessions])
    
    def get_ascent(self, sessions) -> int:
        return sum([s.ascent for s in sessions])
    
    @property
    def total_time(self):
        mysum = datetime.timedelta()
        for h,m,s in [s.total_time for _,s in self.sessions]:
            d = datetime.timedelta(hours=int(h), minutes=m, seconds=s)
            mysum += d
        
        days = mysum.days
        hours = mysum.seconds//3600 + days * 24
        minutes = (mysum.seconds//60)%60
        seconds = mysum.seconds - hours*3600 - minutes*60
        return hours, minutes, seconds
    
    @property
    def distance(self):
        return sum(s.distance_in_km for _,s in self.sessions)
    
    @property
    def tempo(self):
        som = sum(s.average_speed for _,s in self.sessions)
        length = len(self.sessions)
        return speed_to_min_km(som/length)
    
    @property
    def ascent(self):
        return sum(s.ascent for _,s in self.sessions)

    def __detailed_overview(self, sessions) -> list:
        s = list()
        s.append("++++++++++++++++++++++++++++++++++++")
        numbers = self.get_numbers_per_month(sessions)
        for month in numbers:
                s.append(f"    => Days in {month[0]} {name_of_month(month[1])} : {numbers[month]}")
        s.append("++++++++++++++++++++++++++++++++++++")
        distances = self.get_distances_per_month(sessions)
        for month in distances:
                s.append(f"    => Distance in {month[0]} {name_of_month(month[1])} : {distances[month]:.2f}")
        s.append("++++++++++++++++++++++++++++++++++++")
        heights = self.get_heights_per_month(sessions)
        for month in heights:
                s.append(f"    => Height in {month[0]} {name_of_month(month[1])} : {heights[month]}")
        return s

    def __overview(self, sport, sessions) -> list:
        s = list()
        s.append("====================================")
        s.append(f"=== {sport.upper()}")
        s.append("====================================")
        s.append(f"Days:     {self.get_number_days(sessions)}")
        s.append(f"Distance: {self.get_distance(sessions):.2f}")
        s.append(f"Height:   {self.get_ascent(sessions)}")
        s += self.__detailed_overview(sessions)
        s.append("====================================")
        return s

    def __str__(self):
        str = list()
        for sport in self.__sports:
            all_sessions = list()
            for session in [ses for sp, ses in self.sessions if sp == sport]:
                all_sessions.append(session)
            str += self.__overview(sport, all_sessions)
        
        return "\n".join(str)
