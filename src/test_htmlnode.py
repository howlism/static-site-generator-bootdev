import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq_props_to_hmtl(self):
        html_node1 = HTMLNode(
            None,
            None,
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            html_node1.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )
        self.assertNotEqual(
            html_node1.props_to_html(), 'href="https://www.google.com"target="_blank"'
        )
        self.assertNotEqual(html_node1.props_to_html(), "")

    def test_leaf_to_html_p(self):
        leaf_node1 = LeafNode("p", "Hello, world!")
        leaf_node2 = LeafNode(
            "a",
            "Click Me!",
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(leaf_node1.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(
            leaf_node2.to_html(),
            '<a href="https://www.google.com" target="_blank">Click Me!</a>',
        )
        self.assertNotEqual(leaf_node1.to_html(), leaf_node2.to_html())

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        child_node2 = LeafNode("a", "Click Me!", {"href": "www.apple.com"})
        parent_node2 = ParentNode("div", [child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        self.assertEqual(
            parent_node2.to_html(), '<div><a href="www.apple.com">Click Me!</a></div>'
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        grandchild_node2 = LeafNode("a", "link", {"href": "www.apple.com"})
        child_node2 = ParentNode("span", [grandchild_node2])
        parent_node2 = ParentNode("div", [child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        self.assertEqual(
            parent_node2.to_html(),
            '<div><span><a href="www.apple.com">link</a></span></div>',
        )

    def test_to_html_with_great_grandchildren(self):
        great_grandchild_node = LeafNode("p", "great grandchild")
        grandchild_node = ParentNode("span", [great_grandchild_node])
        child_node = ParentNode("div", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        great_grandchild_node2 = LeafNode("a", "cool link", {"href": "www.apple.com"})
        grandchild_node2 = ParentNode("span", [great_grandchild_node2])
        child_node2 = ParentNode("div", [grandchild_node2])
        parent_node2 = ParentNode("div", [child_node2])

        self.assertEqual(
            parent_node.to_html(),
            "<div><div><span><p>great grandchild</p></span></div></div>",
        )
        self.assertEqual(
            parent_node2.to_html(),
            '<div><div><span><a href="www.apple.com">cool link</a></span></div></div>',
        )


if __name__ == "__main__":
    unittest.main()
