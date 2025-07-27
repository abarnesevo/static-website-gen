from textnode import TextNode, TextType
import os
import shutil


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


def main():
    move_to_public()


if __name__ == "__main__":
    main()
