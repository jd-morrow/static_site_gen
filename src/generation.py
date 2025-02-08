import os
import shutil
from markdown_blocks import *
from htmlnode import *

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    
    if not os.path.exists(from_path):
        raise Exception("No file found in from_path")
   
    with open(from_path, "r") as file:
        markdown_file = file.read()
    with open(template_path, "r") as template:
        template_file = template.read()
    
    html = markdown_to_html_node(markdown_file).to_html()
    title = extract_title(markdown_file)
    full_html_page = template_file.replace("{{ Title }}", title).replace("{{ Content }}", html)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(full_html_page)
    
    return True

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception("Invalid content path")
    
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for content in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, content)

        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                dest_path = os.path.splitext(os.path.join(dest_dir_path, content))[0] + ".html"
                generate_page(from_path, template_path, dest_path)

        else:
            dest_path = os.path.join(dest_dir_path, content)
            generate_pages_recursive(from_path, template_path, dest_path)