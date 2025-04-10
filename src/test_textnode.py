import unittest

from textnode import TextNode, TextType

#
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_w_url(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://github.com")
        node2 = TextNode("This is a text node", TextType.IMAGE, "https://github.com")
        self.assertEqual(node, node2)

    def test_uneq_text(self):
        node = TextNode("This is a text node", TextType.LINK, "https://github.com")
        node2 = TextNode("This is another text node", TextType.LINK, "https://github.com")
        self.assertNotEqual(node, node2)

    def test_uneq_url(self):
        node = TextNode("This is a text node", TextType.CODE, "https://github.com")
        node2 = TextNode("This is a text node", TextType.CODE, "https://boot.dev")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
