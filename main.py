import argparse
import glob
from pathlib import Path
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
        self.parser.add_argument('-d', '--directory', default='~/Downloads')
        self.parser.add_argument('-gs', '--statistics', action='store_true')
        self.parser.add_argument('-gi', '--generate_image', action='store_true')
        self.parser.add_argument('-f', '--fitfile', default='lopen.fit')
        self.parser.add_argument('-i', '--input_image', default='input.jpg')
        self.parser.add_argument('-o', '--output_image', default='output.jpg')
        self.parser.add_argument('-te', '--rgb_text', type=tuple_type, default='(255,255,0')
        self.parser.add_argument('-tr', '--rgb_track', type=tuple_type, default='(255,255,0')
        self.parser.add_argument('-fx', '--offset_x', default=30, type=int)
        self.parser.add_argument('-fy', '--offset_y', default=30, type=int)
        self.parser.add_argument('-st', '--max_trace_size', default=400, type=int)
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
        self.statistics.reset()
        for fitfile in glob.glob(f"{args['directory']}/*.fit"):
            self.append_statistic_from_fit_file(fitfile)
                
        print(self.statistics)
    
    def draw_on_image(self, args):
        self.statistics.reset()
        self.traces.reset()
        for fitfile in glob.glob(f"{args['fitfile']}"):
            self.append_statistic_from_fit_file(fitfile)
        
        image = SportImage(self.statistics, self.traces, 
                            text_color=args['text_color'],
                            track_color=args['track_color'])
        image.draw(args['input'], args['output'],
                    args['offsets'], args['map'],
                    args['max_trace_size'])

def create_file_path(directory, filename, check=True):
    p = Path(f"{directory}/{filename}")
    if not check:
        return p.absolute()

    if p.is_file():
            return p.absolute()
    return None
    
if __name__ == '__main__':
    app = Application()
    args = app.parse_args()
    if args.statistics:
        app.display_statistics(dict(directory=args.directory))
    if args.generate_image:
        fitfile = create_file_path(args.directory,args.fitfile)
        input_image = create_file_path(args.directory,args.input_image)
        output_image = create_file_path(args.directory,args.output_image, check=False)
        if (output_image is not None) and (input_image is not None) and (fitfile is not None):
            app.draw_on_image(dict(fitfile=fitfile,
                        input=input_image,
                        output=output_image,
                        map=args.generate_map,
                        text_color=args.rgb_text,
                        track_color=args.rgb_track,
                        offsets=dict(x=args.offset_x, y=args.offset_y),
                        max_trace_size=args.max_trace_size
                    ))
        else:
            print("One of the following files does not exist")
            print(f"directory: {args.directory}")
            print(f"fitfile = {args.fitfile} => {fitfile}")
            print(f"input_image = {args.input_image} => {input_image}")
            print(f"output_image = {args.output_image} => {output_image}")
