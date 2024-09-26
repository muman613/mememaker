import json

from PIL import Image, ImageDraw, ImageFont

from .page import GraphicalPage
from .utils import load_template, draw_centered_text


class GraphicalTemplate:
    def __init__(self, name, page, areas):
        self.name = name
        self.page = GraphicalPage.load_from_name(page)
        self.areas = areas

    @classmethod
    def load_from_json(cls, json_data):
        template_data = json_data['template']
        name = template_data['name']
        page = template_data['page']
        areas = template_data['areas']
        return cls(name, page, areas)

    @classmethod
    def load_from_name(cls, template_name):
        # Load the JSON from a file
        json_data = load_template(template_name)
        # Create a GraphicalTemplate object from the loaded JSON data
        return cls.load_from_json(json_data)

    @classmethod
    def load_from_filename(cls, file_path):
        # Load the JSON from a file
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        # Create a GraphicalPage object from the loaded JSON data
        return cls.load_from_json(json_data)

    @staticmethod
    def dimensions_to_rectangle(w, h, dimensions):
        x1 = w * (dimensions['left'] / 100)
        y1 = h * (dimensions['top'] / 100)
        x2 = w * (dimensions['right'] / 100)
        y2 = h * (dimensions['bottom'] / 100)
        return [(x1, y1), (x2, y2)]

    def render_template(self):
        image = self.page.create_image()

        image_width, image_height = self.page.width_px, self.page.height_px

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('FreeSansBold.ttf', size=128)

        for area in self.areas:
            rectangle = self.dimensions_to_rectangle(image_width, image_height, area['dimensions'])

            draw.rectangle(rectangle, outline='darkblue', width=2)
            draw_centered_text(image, rectangle, area['name'], font=font, fill=(0, 0, 0))

        return image
