from PIL import Image, ImageDraw, ImageFont

class SportImage(object):
    def __init__(self, statistics, points, text_color=(0,0,0)) -> None:
        self.statistics = statistics
        self.font_title = ImageFont.truetype('Ubuntu-R.ttf', 35)
        self.font_text = ImageFont.truetype('Ubuntu-B.ttf', 40)
        self.text_color = text_color
        self.width = 1200
        self.height = 800
        self.horizontal = True
        self.coords = [20,15]

    def draw(self, infile, outfile, withmap=False):
        image = Image.open(infile)
        image = self.normalize(image)
        self.text_on_image(image)
        image.save(outfile, quality=95)
    
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
        
    def normalize(self, image, rotate=False):
        self.calculate_normalized_image_sizes(image)
        img = image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        if rotate:
            return img.rotate(180)
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
