from markdown_to_html import markdown_to_html_node
import unittest


class Test_Markdown_to_html(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quotes(self):
        md = """
>This is **bolded** quote
>text 
>tag here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is <b>bolded</b> quote text tag here</blockquote></div>",
        )

    def test_heading(self):
        md = """
### This is triple heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is triple heading</h3></div>",
        )

    def test_ol(self):
        md = """
1. this is an item
2. this is item 2
3. this is item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>this is an item</li><li>this is item 2</li><li>this is item 3</li></ol></div>",
        )

    def test_ul(self):
        md = """
- this is an item
- this is item 2
- this is item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this is an item</li><li>this is item 2</li><li>this is item 3</li></ul></div>",
        )
