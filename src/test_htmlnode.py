import unittest

from htmlnode import *
# 
class TestHTMLNode(unittest.TestCase):
    def test_empty_node(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode("a", "Click me!", None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multi(self):
        node = HTMLNode("h1", "Test Value",["item_1", "item_2"],{"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(),' href="https://www.google.com" target="_blank"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)

    def test_leaf_to_html_no_tag_no_props(self):
        node = LeafNode(None, "No tag here!")
        self.assertEqual(node.to_html(), "No tag here!")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "No tag here!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "No tag here!")

    def test_leaf_to_html_tag_no_props(self):
        node = LeafNode("b", "This is bold!")
        self.assertEqual(node.to_html(), "<b>This is bold!</b>")

    def test_leaf_to_html_tag_props(self):
        node = LeafNode("a", "Click it! Click it Good!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click it! Click it Good!</a>')

class TestParentNode(unittest.TestCase):
    def test_parent_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", None)

    def test_parent_no_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [
                LeafNode(None, "No tag here!"),
                LeafNode("a", "Click it! Click it Good!", {"href": "https://www.google.com"})
                ])

    def test_parent_4_leafnodes(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "This is bold!"),
                LeafNode(None, "No tag here!"),
                LeafNode(None, "No tag here!", {"href": "https://www.google.com"}),
                LeafNode("a", "Click it! Click it Good!", {"href": "https://www.google.com"})
            ]
        )
        self.assertEqual(node.to_html(), '<p><b>This is bold!</b>No tag here!No tag here!<a href="https://www.google.com">Click it! Click it Good!</a></p>')

    def test_parent_2_sub_parents(self):
        parent_b1 = ParentNode(
            "p",
            [
                LeafNode("b", "This is bold!"),
                LeafNode(None, "No tag here!")
            ]
        )
        parent_b2 = ParentNode(
            "p",
            [
                LeafNode("b", "This is bold!"),
                LeafNode(None, "No tag here!")
            ]
        )
        parent_a = ParentNode(
            "p",
            [
                parent_b1,
                parent_b2
            ]
        )
        self.assertEqual(parent_a.to_html(), '<p><p><b>This is bold!</b>No tag here!</p><p><b>This is bold!</b>No tag here!</p></p>')

if __name__ == "__main__":
    unittest.main()
