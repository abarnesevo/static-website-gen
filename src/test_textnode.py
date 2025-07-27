import unittest

from split_node import (
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
)
from extract_markdown import (
    extract_markdown_links,
    extract_markdown_images,
    markdown_to_blocks,
)
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC, "ligma.com")
        node2 = TextNode("This is a different text node", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = ("This is a text node", TextType.LINK, None)
        node2 = ("This is a text node", TextType.LINK, None)
        self.assertEqual(node, node2)

    def test_text_to_html1(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_html2(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_text_to_html3(self):
        node = TextNode("This is a link", TextType.LINK, "http://ligma.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "http://ligma.com"})

    def test_text_to_html4(self):
        node = TextNode("This is an image", TextType.IMAGE, "imageURL")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.props, {"src": "imageURL", "alt": "This is an image"}
        )
        self.assertEqual(html_node.value, "")

    def test_split_delimiter1(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_delimiter2(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_delimiter3(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_raises_value_error(self):
        node = TextNode("This is text with a _italic word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image] (https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link] (https://somewebsite.com$1)"
        )
        self.assertEqual([("link", "https://somewebsite.com$1")], matches)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is an ![image] (https://myimage.com/ijzzk) and ![another image] (https://myotherimage.com/ijzzk)",
            TextType.TEXT,
        )
        splitted_nodes = split_nodes_images([node])
        self.assertEqual(
            splitted_nodes,
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://myimage.com/ijzzk"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "another image", TextType.IMAGE, "https://myotherimage.com/ijzzk"
                ),
            ],
        )

    def test_split_nodes_image2(self):
        node = TextNode(
            "This is an ![image] (https://myimage.com/ijzzk) and ![another image] (https://myotherimage.com/ijzzk) and another one ![3rd image] (https://3rdimage.com/ijzzk)",
            TextType.TEXT,
        )
        splitted_nodes = split_nodes_images([node])
        self.assertEqual(
            splitted_nodes,
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://myimage.com/ijzzk"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "another image", TextType.IMAGE, "https://myotherimage.com/ijzzk"
                ),
                TextNode(" and another one ", TextType.TEXT),
                TextNode("3rd image", TextType.IMAGE, "https://3rdimage.com/ijzzk"),
            ],
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is a [link] (https://mysite.com/ijzzk) and [another link] (https://myothersite.com/ijzzk)",
            TextType.TEXT,
        )
        splitted_nodes = split_nodes_links([node])
        self.assertEqual(
            splitted_nodes,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://mysite.com/ijzzk"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "another link", TextType.LINK, "https://myothersite.com/ijzzk"
                ),
            ],
        )

    def test_split_nodes_link2(self):
        node = TextNode(
            "This is a [link] (https://mysite.com/ijzzk) and [another link] (https://myothersite.com/ijzzk) and another one [3rd link] (https://3rdsite.comijzzk)",
            TextType.TEXT,
        )
        splitted_nodes = split_nodes_links([node])
        self.assertEqual(
            splitted_nodes,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://mysite.com/ijzzk"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "another link", TextType.LINK, "https://myothersite.com/ijzzk"
                ),
                TextNode(" and another one ", TextType.TEXT),
                TextNode("3rd link", TextType.LINK, "https://3rdsite.comijzzk"),
            ],
        )

    def test_split_nodes_no_link(self):
        node = TextNode(
            "This is a link] (https://mysite.com/ijzzk) and another link] (https://myothersite.com/ijzzk)",
            TextType.TEXT,
        )
        splitted_nodes = split_nodes_links([node])
        self.assertEqual(
            splitted_nodes,
            [
                TextNode(
                    "This is a link] (https://mysite.com/ijzzk) and another link] (https://myothersite.com/ijzzk)",
                    TextType.TEXT,
                ),
            ],
        )

    def test_text_to_text_nodes(self):
        text = "This is a **text** with an _italic_ word and a `code block` with an ![image] (https://myimage.com/123) and a [link] (https://somesite.com)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://myimage.com/123"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://somesite.com"),
            ],
        )

    def test_text_to_text_nodes2(self):
        text = "This is a **text** and a `code block` with an ![image] (https://myimage.com/123)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://myimage.com/123"),
            ],
        )

    def test_text_to_text_nodes_error(self):
        node = TextNode(
            "This is text with a __italic word and a `code block`", TextType.TEXT
        )
        with self.assertRaises(Exception):
            text_to_textnodes(node)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks1(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


if __name__ == "__main__":
    unittest.main()
