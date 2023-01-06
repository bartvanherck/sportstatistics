from PIL import Image, ImageDraw, ImageFont

class SportImage(object):
    def __init__(self, statistics, traces, text_color=(0,0,0), track_color=(0,0,0), rotate=0) -> None:
        self.statistics = statistics
        self.traces = traces
        self.font_title = ImageFont.truetype('Ubuntu-R.ttf', 35)
        self.font_text = ImageFont.truetype('Ubuntu-B.ttf', 40)
        self.text_color = text_color
        self.track_color = track_color
        self.width = 1200
        self.height = 900
        self.rotate = rotate
        self.horizontal = True
        self.coords = [20,15]

    def draw(self, infile, outfile, offsets, withmap=False, max_path_size=400):
        image = Image.open(infile)
        image = self.normalize(image)
        self.text_on_image(image)
        if withmap:
            self.draw_path(image, offsets["x"], offsets["y"], max_path_size)
        image.save(outfile, quality=95)
    
    def draw_path(self, image, offset_x=40, offset_y=40, max_size=700):
        draw = ImageDraw.Draw(image)
        shape = self.traces.get_shape(max_height=image.height, offset_x=offset_x, offset_y=offset_y, max_size=max_size)
        draw.line(shape, fill=self.track_color, width=4)

    def place_text(self, img, coord ,titleText, content):
        img.text(tuple(coord), titleText, fill=self.text_color, font=self.font_title)
        coord[1] += 45
        img.text(tuple(coord), content, fill=self.text_color, font=self.font_text)
        coord[1] -= 45
    
    def place_time(self, draw):
        hour, minute, seconds = self.statistics.total_time
        text = f"{hour} h {minute:02} m {seconds:02} s"
        self.place_text(draw, self.coords, "Tijd", text)

    def place_distance(self, draw):
        text = f"{self.statistics.distance:.2f} km".replace(".",",")
        self.place_text(draw, self.coords, "Afstand", text)
    
    def place_tempo(self, draw):
        nbr, komma = self.statistics.tempo
        text = f"{nbr}:{komma:02} / km"
        self.place_text(draw, self.coords, "Tempo", text)
    
    def place_ascent(self, draw):
        text = f"{self.statistics.ascent} m"
        self.place_text(draw, self.coords, "Hoogte", text)

    def text_on_image(self, image):
        draw = ImageDraw.Draw(image)
        self.place_time(draw)
        self.next_coordinate(horizontal=self.horizontal)
        self.place_distance(draw)
        self.next_coordinate(horizontal=self.horizontal)
        self.place_tempo(draw)
        self.next_coordinate(horizontal=self.horizontal)
        self.place_ascent(draw)
    
    def next_coordinate(self, horizontal = True):
        if horizontal:
            self.coords[0] += 330
        else:
            self.coords[1] += 120
        
    def normalize(self, image):
        self.calculate_normalized_image_sizes(image)
        img = image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        if self.rotate != 0:
            print(f"rotate please for {self.rotate} degrees")
            return img.rotate(self.rotate)
        return img
    
    def calculate_normalized_image_sizes(self, image):
        if image.width > image.height:
            self.width = 1200
            self.height = int(1200 * image.height / image.width)
            self.horizontal = True
        elif image.height > image.width:
            self.height = 1200
            self.width = int(1200 * image.width / image.height)
            self.horizontal = False
        else:
            self.height = 1200
            self.width = 1200
            self.horizontal = True
