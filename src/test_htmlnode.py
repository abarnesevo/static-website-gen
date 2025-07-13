import unittest

from textnode import TextNode, TextType 

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        node = HTMLNode("tag", "value", ["children"], {"props":"props"})
        node2 = HTMLNode("tag", "value", ["children"], {"props":"props"})
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("Tag")
        node2 = HTMLNode("Tag", "Value", ["children"])
        self.assertNotEqual(node, node2)

    def test_none(self):
        node = HTMLNode("Tag")
        node2 = HTMLNode("Tag")
        self.assertEqual(node, node2)

    def test_leaf(self):
        node = LeafNode("p","Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_props(self):
        node = LeafNode("a", "Click", {"href": "http://ligma.com"})
        self.assertEqual(node.to_html(), '<a href="http://ligma.com">Click</a>')

    def test_raises_value_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
                "<div><span><b>grandchild</b></span></div>",
        )

    def test_children_value_error(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_tag_value_error(self):
        node = ParentNode(None, ["child"])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_with_multiple_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child2</span></div>")

