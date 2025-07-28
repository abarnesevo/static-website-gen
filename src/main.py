from markdown_to_html import markdown_to_html_node
from extract_markdown import extract_markdown_title
from htmlnode import HTMLNode
import os
import sys
import shutil

starting_dest = "./docs"
starting_content = "./content"
starting_template = "./template.html"
basepath = "./"
if len(sys.argv) > 1:
    basepath = sys.argv[1]


def copy_static_to_public(current_file_path=None):
    if current_file_path == None:
        static = "./static"
        public = "./docs"

    else:
        static = os.path.join(
            "./docs",
            current_file_path,
        )
        print(f"current static: {static}")
        public = os.path.join(
            "./docs",
            current_file_path,
        )

    contents = os.listdir(static)
    for object in contents:
        path = os.path.join(static, object)
        if os.path.isfile(path):
            shutil.copy(path, public)
        else:
            if current_file_path != None:
                new_current = os.path.join(current_file_path, object)
            else:
                new_current = object
            new_dir = os.path.join(public, new_current)
            os.mkdir(new_dir)
            copy_static_to_public(new_current)


def move_to_public():
    if os.path.exists("./docs") == True:
        shutil.rmtree("./docs")
    os.mkdir("./docs")
    copy_static_to_public()


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating a page from {from_path} to {dest_path}")
    with open(from_path) as f:
        md = f.read()
        f.close()

    with open(template_path) as f:
        template = f.read()
        f.close()

    content = markdown_to_html_node(md)
    content = content.to_html()
    title = extract_markdown_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')
    path = os.path.dirname(dest_path)

    if not os.path.exists(path):
        os.makedirs(path)

    with open(dest_path, "w") as f:
        f.write(template)
        f.close()


def generate_pages_recursively(
    dir_path_content, template_path, dest_dir_path, base_path
):
    contents = os.listdir(dir_path_content)
    for object in contents:
        object_path = os.path.join(dir_path_content, object)
        if os.path.isfile(object_path):
            if object.endswith(".md"):
                new_dest = os.path.join(dest_dir_path, object.replace(".md", ".html"))
                generate_page(object_path, template_path, new_dest, base_path)
        else:
            new_dest = os.path.join(dest_dir_path, object)
            os.mkdir(new_dest)
            generate_pages_recursively(object_path, template_path, new_dest, base_path)


def main():
    move_to_public()
    generate_pages_recursively(
        starting_content, starting_template, starting_dest, basepath
    )


if __name__ == "__main__":
    main()
