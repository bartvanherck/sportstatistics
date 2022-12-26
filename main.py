import argparse
import glob
from fitness.sportstatistics import SportStatistics
from fitness.fitfilereader import FitFileReader
from fitness.fitsession import FitDataType
from fitness.traces import Traces
from fitness.sportImage import SportImage

def tuple_type(strings):
    strings = strings.replace("(", "").replace(")", "")
    mapped = map(int, strings.split(","))
    return tuple(mapped)

class Application(object):
    def __init__(self) -> None:
        self.parser=argparse.ArgumentParser(
                    prog = 'fitnes',
                    description = 'Prints overview of my runs')
        self.statistics = SportStatistics()
        self.traces = Traces()
    
    def arguments(self):
        self.parser.add_argument('-d', '--directory', default='/home/bart/Downloads/fit')
        self.parser.add_argument('-s', '--statistics', action='store_true')
        self.parser.add_argument('-gi', '--generate_image', action='store_true')
        self.parser.add_argument('-f', '--fitfile', default='/home/bart/Downloads/fit/20221225_Lopen.fit')
        self.parser.add_argument('-i', '--input_image', default='/home/bart/Downloads/fotos/1.JPG')
        self.parser.add_argument('-o', '--output_image', default='/home/bart/Downloads/fotos/result.JPG')
        self.parser.add_argument('-rt', '--rgb_text', type=tuple_type, default='(255,255,0')
        self.parser.add_argument('-m', '--generate_map', action='store_true')

    def parse_args(self):
        self.arguments()
        return self.parser.parse_args()
    
    def append_statistic_from_fit_file(self, fit_file):
        reader = FitFileReader()
        for record_type, record in reader.parse(fit_file):
            if record_type is FitDataType.SESSION:
                self.statistics.insert(record)
            if record_type is FitDataType.RECORD:
                self.traces.insert(record)

    def display_statistics(self, args):
        # for fitfile in glob.glob(f"{args['directory']}/20221215.fit"):
        for fitfile in glob.glob(f"{args['directory']}/*.fit"):
            self.append_statistic_from_fit_file(fitfile)
                
        print(self.statistics)
    
    def draw_on_image(self, args):
        for fitfile in glob.glob(f"{args['fitfile']}"):
            self.append_statistic_from_fit_file(fitfile)
        
        image = SportImage(self.statistics, self.traces, text_color=args['text_color'])
        image.draw(args['input'], args['output'], args['map'])

if __name__ == '__main__':
    app = Application()
    args = app.parse_args()
    if args.statistics:
        app.display_statistics(dict(directory=args.directory))
    if args.generate_image:
        app.draw_on_image(dict(fitfile=args.fitfile,
                    input=args.input_image,
                    output=args.output_image,
                    map=args.generate_map,
                    text_color=args.rgb_text
                ))