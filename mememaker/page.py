import json
from PIL import Image, ImageDraw
from .utils import load_page


class GraphicalPage:
    def __init__(self, width_in, height_in, dpi, bg_color, border_width, border_color):
        # Convert dimensions from inches to pixels using DPI
        self.width_px = int(width_in * dpi[0])
        self.height_px = int(height_in * dpi[1])
        self.dpi = dpi
        self.bg_color = bg_color
        self.border_width = border_width
        self.border_color = border_color

    @classmethod
    def from_json(cls, json_data):
        # Parse the JSON data
        page_data = json_data['page']
        dimensions = page_data['dimensions']
        dpi = page_data['dpi']
        bg_color = page_data['bg']
        border_data = page_data['border']
        border_width = border_data['width']
        border_color = border_data['color']

        return cls(
            width_in=dimensions['width'],
            height_in=dimensions['height'],
            dpi=dpi,
            bg_color=bg_color,
            border_width=border_width,
            border_color=border_color
        )

    @classmethod
    def load_from_name(cls, page_name):
        # Load the JSON from a file
        json_data = load_page(page_name)
        # Create a GraphicalPage object from the loaded JSON data
        return cls.from_json(json_data)

    @classmethod
    def load_from_filename(cls, file_path):
        # Load the JSON from a file
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        # Create a GraphicalPage object from the loaded JSON data
        return cls.from_json(json_data)

    def create_image(self):
        # Create a blank image with the background color
        image = Image.new("RGB", (self.width_px, self.height_px), self.bg_color)
        draw = ImageDraw.Draw(image)

        # Draw the border if border width is greater than 0
        if self.border_width > 0:
            # Calculate the border dimensions and draw the rectangle
            draw.rectangle(
                [(self.border_width // 2, self.border_width // 2),
                 (self.width_px - self.border_width // 2, self.height_px - self.border_width // 2)],
                outline=self.border_color,
                width=self.border_width
            )

        return image
