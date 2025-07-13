import unittest

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
        self.assertEqual(html_node.props, {"src": "imageURL", "alt": "This is an image"})
        self.assertEqual(html_node.value, "")




if __name__ == "__main__":
    unittest.main()

