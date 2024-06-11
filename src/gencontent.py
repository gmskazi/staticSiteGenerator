import os
from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if "# " in line:
            return line
    raise Exception("All pages need a single h1 header")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        contents = file.read()

    with open(template_path, "r") as temp_file:
        template_file = temp_file.read()

    html = markdown_to_html_node(contents).to_html()
    title = extract_title(contents)
    # print(title)

    new_template = template_file.replace("{{ Title }}", title)
    new_template = new_template.replace("{{ Content }}", html)
    # print(new_template)
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as html_file:
        html_file.write(new_template)


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            from_path = os.path.join(root, file)
            html_file = file.replace("md", "html")
            dest_file_path = os.path.join(root, html_file)
            relative_path = os.path.relpath(dest_file_path, dir_path_content)
            dest_path = os.path.join(dest_dir_path, relative_path)

            generate_page(from_path, template_path, dest_path)
