import unittest

from enum import Enum
from htmlnode import HTMLNode, LeafNode
from textnode import TextType, TextNode
from convertnodes import *
# 
class Test_Convert_Nodes(unittest.TestCase):
    def test_convert_text(self):
        test_text_node = TextNode("Regular text", TextType.TEXT)
        test_leaf_node = text_node_to_html_node(test_text_node)
        self.assertEqual(test_leaf_node.to_html(), "Regular text")

    def test_convert_bold(self):
        test_text_node = TextNode("Bold text", TextType.BOLD)
        test_leaf_node = text_node_to_html_node(test_text_node)
        self.assertEqual(test_leaf_node.to_html(), "<b>Bold text</b>")

    def test_convert_italic(self):
        test_text_node = TextNode("Italic text", TextType.ITALIC)
        test_leaf_node = text_node_to_html_node(test_text_node)
        self.assertEqual(test_leaf_node.to_html(), "<i>Italic text</i>")

    def test_convert_code(self):
        test_text_node = TextNode("Code text", TextType.CODE)
        test_leaf_node = text_node_to_html_node(test_text_node)
        self.assertEqual(test_leaf_node.to_html(), "<code>Code text</code>")

    def test_convert_link(self):
        test_text_node = TextNode("Link text", TextType.LINK, "https://www.google.com")
        test_leaf_node = text_node_to_html_node(test_text_node)
        self.assertEqual(test_leaf_node.to_html(), '<a href="https://www.google.com">Link text</a>')
        
    def test_convert_image(self):
        test_text_node = TextNode("Google Logo", TextType.IMAGE, "https://www.google.com/logo.jpg")
        test_leaf_node = text_node_to_html_node(test_text_node)
        self.assertEqual(test_leaf_node.to_html(), '<img src="https://www.google.com/logo.jpg" alt="Google Logo"></img>')

    def test_convert_unknown_type(self):
        with self.assertRaises(Exception):
            test_text_node = TextNode("This should raise an exception", TextType.UNDERLINE)
            test_leaf_node = text_node_to_html_node(test_text_node)

class Test_Split_Nodes(unittest.TestCase):
    def test_single_TEXT_no_markdown_to_BOLD(self):
        old_nodes = [TextNode("Turn regular text to bold", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Turn regular text to bold")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_single_BOLD_with_markdown(self):
        old_nodes = [TextNode("This is already *BOLD*", TextType.BOLD)]
        result = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is already *BOLD*")
        self.assertEqual(result[0].text_type, TextType.BOLD)

    def test_single_TEXT_middle_markdown(self):
        old_nodes = [TextNode("This text has **BOLD** inside!", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(result[i].text_type == TextType.TEXT
                            for i in range(0, len(result), 2)))
        self.assertTrue(all(result[i].text_type == TextType.BOLD
                            for i in range(1, len(result), 2)))
        self.assertEqual(result[0].text, "This text has ")
        self.assertEqual(result[1].text, "BOLD")
        self.assertEqual(result[2].text, " inside!")

    def test_single_TEXT_start_markdown(self):
        old_nodes = [TextNode("-I- shall have vengeance!", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "-", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(result[i].text_type == TextType.TEXT
                            for i in range(0, len(result), 2)))
        self.assertTrue(all(result[i].text_type == TextType.ITALIC
                            for i in range(1, len(result), 2)))
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[1].text, "I")
        self.assertEqual(result[2].text, " shall have vengeance!")

    def test_single_TEXT_multi_markdown(self):
        old_nodes = [TextNode("A *British Tar* is a *soaring* soul, as *free* as a mountain *bird*!", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        self.assertEqual(len(result), 9)
        self.assertTrue(all(result[i].text_type == TextType.TEXT
                            for i in range(0, len(result), 2)))
        self.assertTrue(all(result[i].text_type == TextType.BOLD
                            for i in range(1, len(result), 2)))
        
    def test_single_TEXT_bad_markdown(self):
        old_nodes = [TextNode("I'm going to *break your function", TextType.TEXT)]
        with self.assertRaises(ValueError):
            result = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)

    def test_multi_mixed_markdown(self):
        old_nodes = [
            TextNode("I want *this* to be bold!", TextType.TEXT),
            TextNode("I -don't- want to be bold!", TextType.TEXT),
            TextNode("I'm italic!", TextType.ITALIC),
            TextNode("I want *that* to be bold!", TextType.TEXT)
        ]
        result = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        self.assertEqual(len(result), 8)
        self.assertEqual(result[0].text, "I want ")
        self.assertEqual(result[1].text, "this")
        self.assertEqual(result[2].text, " to be bold!")
        self.assertEqual(result[3].text, "I -don't- want to be bold!")
        self.assertEqual(result[4].text, "I'm italic!")
        self.assertEqual(result[5].text, "I want ")
        self.assertEqual(result[6].text, "that")
        self.assertEqual(result[7].text, " to be bold!")
        text_indices = [0, 2, 3, 5, 7]
        bold_indices = [1, 6]
        self.assertTrue(all(result[i].text_type == TextType.TEXT
                            for i in text_indices))
        self.assertTrue(all(result[i].text_type == TextType.BOLD
                            for i in bold_indices))
        self.assertEqual(result[4].text_type, TextType.ITALIC)

    def test_empty_delim_section(self):
        old_nodes = [TextNode("I am getting ** ** very tired of writing tests!", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(result[i].text_type == TextType.TEXT
                            for i in range(0, len(result), 2)))
        self.assertTrue(all(result[i].text_type == TextType.CODE
                            for i in range(1, len(result), 2)))
        self.assertEqual(result[0].text, "I am getting ")
        self.assertEqual(result[1].text, " ")
        self.assertEqual(result[2].text, " very tired of writing tests!")

class Test_Image_Extract(unittest.TestCase):
    def test_image(self):
        input = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(input)
        self.assertEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_no_image(self):
        input = "There is no image markdown in this text!"
        result = extract_markdown_images(input)
        self.assertEqual(result, [])

class Test_Link_Extract(unittest.TestCase):
    def test_link(self):
        input = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(input)
        self.assertEqual(result, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_no_link(self):
        input = "This text has no link markdown!"
        result = extract_markdown_links(input)
        self.assertEqual(result, [])

class Text_Split_Image(unittest.TestCase):
    def test_split_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes
        )

    def test_split_image_single(self):
        node = TextNode("![image](https://www.example.COM/IMAGE.PNG)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG")],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()