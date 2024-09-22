import os
import glob
import json

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

