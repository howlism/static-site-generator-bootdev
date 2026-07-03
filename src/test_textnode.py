import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a link text node", TextType.LINK, "link.com")
        node5 = TextNode("This is a link text node", TextType.LINK, "anotherlink.com")
        node6 = TextNode("This is a link text node", TextType.LINK, "anotherlink.com")
        node7 = TextNode("This is a link text node", TextType.LINK, None)
        self.assertEqual(node, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node4, node5)
        self.assertEqual(node5, node6)
        self.assertNotEqual(node6, node7)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        node2 = TextNode("This is a bold text node", TextType.BOLD)
        html_node2 = text_node_to_html_node(node2)
        node3 = TextNode("This is an italicised text node", TextType.ITALIC)
        html_node3 = text_node_to_html_node(node3)
        node4 = TextNode("This is a code node", TextType.CODE)
        html_node4 = text_node_to_html_node(node4)
        node5 = TextNode("This is a link", TextType.LINK, "www.website.com")
        html_node5 = text_node_to_html_node(node5)
        node6 = TextNode(
            "This is an image", TextType.IMAGE, "www.images.com/link/to/image.png"
        )
        html_node6 = text_node_to_html_node(node6)

        # Plain Text
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        # Bold Text
        self.assertEqual(html_node2.tag, "b")
        self.assertEqual(html_node2.value, "This is a bold text node")

        # Italic Text
        self.assertEqual(html_node3.tag, "i")
        self.assertEqual(html_node3.value, "This is an italicised text node")

        # Code Node
        self.assertEqual(html_node4.tag, "code")
        self.assertEqual(html_node4.value, "This is a code node")

        # Link Node
        self.assertEqual(html_node5.tag, "a")
        self.assertEqual(html_node5.value, "This is a link")
        self.assertEqual(html_node5.props_to_html(), ' href="www.website.com"')

        # Image Node
        self.assertEqual(html_node6.tag, "img")
        self.assertEqual(html_node6.value, "")
        self.assertEqual(
            html_node6.props_to_html(),
            ' src="www.images.com/link/to/image.png" alt="This is an image"',
        )


if __name__ == "__main__":
    unittest.main()
