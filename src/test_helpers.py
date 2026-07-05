import unittest
from textnode import TextNode, TextType
from helpers import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
)


class TestSplitNodes(unittest.TestCase):
    def test_split_node(self):
        # Regular
        text_node = TextNode("This is a **bold** word.", TextType.PLAIN)
        text_node_split = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" word.", TextType.PLAIN),
        ]
        text_node2 = TextNode("This is a `code` block.", TextType.PLAIN)
        text_node_split2 = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" block.", TextType.PLAIN),
        ]
        text_node3 = TextNode("This is an *italicised* block.", TextType.PLAIN)
        text_node_split3 = [
            TextNode("This is an ", TextType.PLAIN),
            TextNode("italicised", TextType.ITALIC),
            TextNode(" block.", TextType.PLAIN),
        ]

        self.assertEqual(
            split_nodes_delimiter([text_node], "**", TextType.BOLD), text_node_split
        )
        self.assertEqual(
            split_nodes_delimiter([text_node2], "`", TextType.CODE), text_node_split2
        )
        self.assertEqual(
            split_nodes_delimiter([text_node3], "*", TextType.ITALIC), text_node_split3
        )


class TestImageLinkFuncs(unittest.TestCase):
    def test_extract_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        img_string = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            img_string,
        )

        img_string2 = extract_markdown_images(
            "This text has ![an image of an orange](https://www.orange.com/pics) and one of ![an image of an apple](https://www.fruit.apple.com/pics)"
        )
        self.assertEqual(
            [
                ("an image of an orange", "https://www.orange.com/pics"),
                ("an image of an apple", "https://www.fruit.apple.com/pics"),
            ],
            img_string2,
        )

    def test_extract_links(self):
        link_text = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertEqual([("link", "https://www.google.com")], link_text)

        link_text2 = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            link_text2,
        )

        link_text3 = extract_markdown_links(
            "This is text with two links. One to [google](https://www.google.com) and one to [wikipedia](https://www.wikipedia.com)"
        )
        self.assertEqual(
            [
                ("google", "https://www.google.com"),
                ("wikipedia", "https://www.wikipedia.com"),
            ],
            link_text3,
        )

    def test_split_images(self):
        img_node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        out_nodes = split_nodes_image([img_node])

        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            out_nodes,
        )

        img_node2 = TextNode(
            "This is some more text with an ![image](https://picture.com) and then some text behind it.",
            TextType.PLAIN,
        )
        out_nodes2 = split_nodes_image([img_node2])

        self.assertEqual(
            [
                TextNode("This is some more text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://picture.com"),
                TextNode(" and then some text behind it.", TextType.PLAIN),
            ],
            out_nodes2,
        )

    def test_split_links(self):
        link_node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN,
        )

        out_nodes = split_nodes_link([link_node])

        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.PLAIN),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            out_nodes,
        )

    def test_text_to_textnodes(self):
        input_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(input_text),
        )


class TestMarkdownBlockSplits(unittest.TestCase):
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
        md2 = """
# This is a heading with a **bolded** word!

This is just a regular paragraph maybe it'll have a [link](https://www.google.com)
Maybe it might have an image of a cat ![cat image](https://www.cat.com/picture)

\n\n\n\n\n\n\n\n

Then we'll have a final paragraph down here
"""

        blocks2 = markdown_to_blocks(md2)
        self.assertEqual(
            blocks2,
            [
                "# This is a heading with a **bolded** word!",
                "This is just a regular paragraph maybe it'll have a [link](https://www.google.com)\nMaybe it might have an image of a cat ![cat image](https://www.cat.com/picture)",
                "Then we'll have a final paragraph down here",
            ],
        )


if __name__ == "__main__":
    unittest.main()
