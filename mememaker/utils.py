import os
import glob
import json
from typing import List
from PIL import Image, ImageDraw, ImageFont

PAGES_PATH = 'resources/pages'
TEMPLATES_PATH = 'resources/templates'


def scan_directory_for_json(directory):
    # Use glob to find all .json files in the specified directory
    json_files = glob.glob(os.path.join(directory, '*.json'))

    # If no .json files are found, raise a FileNotFoundError
    if not json_files:
        raise FileNotFoundError(f"No JSON files found in directory: {directory}")

    # Return a list of all the .json file paths
    return json_files


def load_json_file(json_filename: str) -> dict:
    if os.path.exists(json_filename):
        with open(json_filename, 'r') as f:
            return json.load(f)
    return {}


def load_page(page_name: str) -> dict:
    page_list = scan_directory_for_json(PAGES_PATH)
    for page in page_list:
        page_json = load_json_file(page)
        if 'page' in page_json and 'name' in page_json['page']:
            if page_name == page_json['page']['name']:
                return page_json

    # If no matching page is found, raise an exception
    raise FileNotFoundError(f"No page found with the name '{page_name}' in {PAGES_PATH}")



def load_template(template_name: str) -> dict:
    template_list = scan_directory_for_json(TEMPLATES_PATH)
    for template in template_list:
        template_json = load_json_file(template)
        if 'template' in template_json and 'name' in template_json['template']:
            if template_name == template_json['template']['name']:
                return template_json

    # If no matching template is found, raise an exception
    raise FileNotFoundError(f"No template found with the name '{template_name}' in {TEMPLATES_PATH}")


def get_template_names() -> List[str]:
    template_names = []
    template_list = scan_directory_for_json(TEMPLATES_PATH)
    for template in template_list:
        template_json = load_json_file(template)
        if 'template' in template_json and 'name' in template_json['template']:
            template_names.append(template_json['template']['name'])

    return template_names


def get_page_names() -> List[str]:
    page_names = []
    page_list = scan_directory_for_json(PAGES_PATH)
    for page in page_list:
        page_json = load_json_file(page)
        if 'page' in page_json and 'name' in page_json['page']:
            page_names.append(page_json['page']['name'])

    return page_names


def draw_centered_text(image, rectangle, text, font, fill=(255, 255, 255)):
    draw = ImageDraw.Draw(image)

    # Extract the rectangle coordinates
    (x0, y0), (x1, y1) = rectangle

    # Calculate the center of the rectangle
    center_x = (x0 + x1) // 2
    center_y = (y0 + y1) // 2

    # Get the size of the text to calculate the position for centering
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calculate the position for the text to be centered
    text_x = center_x - text_width // 2
    text_y = center_y - text_height // 2

    # Draw the text
    draw.text((text_x, text_y), text, font=font, fill=fill)