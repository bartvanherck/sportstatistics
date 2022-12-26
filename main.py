import argparse
import glob
from fitness.sportstatistics import SportStatistics
from fitness.fitfilereader import FitFileReader
from fitness.fitsession import FitDataType


class Application(object):
    def __init__(self) -> None:
        self.parser=argparse.ArgumentParser(
                    prog = 'fitnes',
                    description = 'Prints overview of my runs')
    
    def arguments(self):
        self.parser.add_argument('-d', '--directory', default='/home/bart/Downloads/fit')
    
    def parse_args(self):
        self.arguments()
        return self.parser.parse_args()
    
    def display_statistics(self, args):
        statistic = SportStatistics()
        # for fitfile in glob.glob(f"{args['directory']}/20221215.fit"):
        for fitfile in glob.glob(f"{args['directory']}/*.fit"):
            reader = FitFileReader()
            for session_type, session in reader.parse(fitfile):
                if session_type is FitDataType.SESSION:
                    statistic.insert(session)
        print(statistic)

if __name__ == '__main__':
    app = Application()
    args = app.parse_args()
    app.display_statistics(dict(directory=args.directory))
