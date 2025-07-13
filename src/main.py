from textnode import TextNode, TextType

def main():
    node = TextNode("here is some text", TextType.LINK, "http://ligma.com")
    print(node)

if __name__ == "__main__":
    main()
