from markdown_to_html import markdown_to_html_node
from extract_markdown import extract_markdown_title
from htmlnode import HTMLNode
import os
import shutil

starting_dest = "/home/abarnes/abarnes/workspace/github.com/static-website-gen/public"
starting_content = (
    "/home/abarnes/abarnes/workspace/github.com/static-website-gen/content"
)
starting_template = (
    "/home/abarnes/abarnes/workspace/github.com/static-website-gen/template.html"
)


def copy_static_to_public(current_file_path=None):
    if current_file_path == None:
        static = "/home/abarnes/abarnes/workspace/github.com/static-website-gen/static"
        public = "/home/abarnes/abarnes/workspace/github.com/static-website-gen/public"

    else:
        static = os.path.join(
            "/home/abarnes/abarnes/workspace/github.com/static-website-gen/static",
            current_file_path,
        )
        print(f"current static: {static}")
        public = os.path.join(
            "/home/abarnes/abarnes/workspace/github.com/static-website-gen/public",
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
    if os.path.exists(
        "/home/abarnes/abarnes/workspace/github.com/static-website-gen/public"
    ):
        shutil.rmtree(
            "/home/abarnes/abarnes/workspace/github.com/static-website-gen/public"
        )
    os.mkdir("/home/abarnes/abarnes/workspace/github.com/static-website-gen/public")
    copy_static_to_public()


def generate_page(from_path, template_path, dest_path):
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
    path = os.path.dirname(dest_path)

    if not os.path.exists(path):
        os.makedirs(path)

    with open(dest_path, "w") as f:
        f.write(template)
        f.close()


def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    for object in contents:
        object_path = os.path.join(dir_path_content, object)
        if os.path.isfile(object_path):
            if object.endswith(".md"):
                new_dest = os.path.join(dest_dir_path, object.replace(".md", ".html"))
                generate_page(object_path, template_path, new_dest)
        else:
            new_dest = os.path.join(dest_dir_path, object)
            os.mkdir(new_dest)
            generate_pages_recursively(object_path, template_path, new_dest)


def main():
    move_to_public()
    generate_pages_recursively(starting_content, starting_template, starting_dest)


if __name__ == "__main__":
    main()
