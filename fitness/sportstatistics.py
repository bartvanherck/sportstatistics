from .utils import name_of_month
from collections import Counter, OrderedDict, defaultdict


class SportStatistics(object):
    def __init__(self):
        self.__sports = list()
        self.sessions = list()

    def insert(self, session):
        self.add_session(session)
        self.__sports = list(set([sport for sport,_ in self.sessions]))
        self.__sports.sort()
    
    def add_session(self, session):
        dates = [s.start_day for _,s in self.sessions]
        if session.start_day not in dates:
            self.sessions.append((session.sport,session))

    def number_days(self, sessions):
        return len(sessions)
    
    def numbers_per_month(self, sessions):
        count = Counter((y,m) for y,m,_ in (s.start_day for s in sessions))
        return OrderedDict(sorted(count.items()))

    def distances_per_month(self, sessions):
        dist = defaultdict(int)
        for session in sessions:
            y,m,_ = session.start_day
            dist[(y,m)] += session.distance_in_km
        return OrderedDict(sorted(dist.items()))

    def heights_per_month(self, sessions):
        ascents = defaultdict(int)
        for session in sessions:
            y,m,_ = session.start_day
            ascents[(y,m)] += session.ascent
        return OrderedDict(sorted(ascents.items()))

    def distance(self, sessions):
        return sum([s.distance_in_km for s in sessions])
    
    def ascent(self, sessions):
        return sum([s.ascent for s in sessions])
    
    def __detailed_overview(self, sessions):
        s = list()
        s.append("++++++++++++++++++++++++++++++++++++")
        numbers = self.numbers_per_month(sessions)
        for month in numbers:
                s.append(f"    => Days in {month[0]} {name_of_month(month[1])} : {numbers[month]}")
        s.append("++++++++++++++++++++++++++++++++++++")
        distances = self.distances_per_month(sessions)
        for month in distances:
                s.append(f"    => Distance in {month[0]} {name_of_month(month[1])} : {distances[month]:.2f}")
        s.append("++++++++++++++++++++++++++++++++++++")
        heights = self.heights_per_month(sessions)
        for month in heights:
                s.append(f"    => Height in {month[0]} {name_of_month(month[1])} : {heights[month]}")
        return s

    def __overview(self, sport, sessions):
        s = list()
        s.append("====================================")
        s.append(f"=== {sport.upper()}")
        s.append("====================================")
        s.append(f"Days:     {self.number_days(sessions)}")
        s.append(f"Distance: {self.distance(sessions):.2f}")
        s.append(f"Height:   {self.ascent(sessions)}")
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
