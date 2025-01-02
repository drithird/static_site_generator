import unittest

from markdown_to_html import markdown_to_html_node

text = """# Test Markdown Document

## Header Level 2

This is **bold text** and this is *italicized text* **bolded  2 **.


### Links Section

Here's a [link to OpenAI](https://www.openai.com) for testing purposes.

### Images Section

Below is an image placeholder for testing:

![Placeholder Image](https://via.placeholder.com/150)


#### Spacing Test

This paragraph is followed by multiple new lines to test formatting robustness.




This paragraph should appear after several blank lines.


### Mixed Content

Here is a bullet point list with formatting:

- **Bolded item**
- *Italicized item*

Here is a numbered list with a link:

1. Visit [OpenAI](https://www.openai.com).
2. See the image above.
3. Test **mixed styles** here.

> This is a wise quote

> This is another quote

```
print("Hello World!") 
print("Hello")
```
"""


class Test_markdown_to_html_node(unittest.TestCase):
    def test_markdown_to_html_node(self):
        test_answer = """ParentNode(div, None, [ParentNode(h1, None, [LeafNode(None, Test Markdown Document, None, None)], None), ParentNode(h2, None, [LeafNode(None, Header Level 2, None, None)], None), ParentNode(p, None, [LeafNode(None, This is , None, None), LeafNode(b, bold text, None, None), LeafNode(None,  and this is , None, None), LeafNode(i, italicized text, None, None), LeafNode(None,  , None, None), LeafNode(b, bolded  2 , None, None), LeafNode(None, ., None, None)], None), ParentNode(h3, None, [LeafNode(None, Links Section, None, None)], None), ParentNode(p, None, [LeafNode(None, Here's a , None, None), LeafNode(a, link to OpenAI, None, {'href': 'https://www.openai.com'}), LeafNode(None,  for testing purposes., None, None)], None), ParentNode(h3, None, [LeafNode(None, Images Section, None, None)], None), ParentNode(p, None, [LeafNode(None, Below is an image placeholder for testing:, None, None)], None), ParentNode(p, None, [LeafNode(None, , None, None), LeafNode(img, , None, {'src': 'https://via.placeholder.com/150', 'alt': 'Placeholder Image'})], None), ParentNode(h4, None, [LeafNode(None, Spacing Test, None, None)], None), ParentNode(p, None, [LeafNode(None, This paragraph is followed by multiple new lines to test formatting robustness., None, None)], None), ParentNode(p, None, [LeafNode(None, This paragraph should appear after several blank lines., None, None)], None), ParentNode(h3, None, [LeafNode(None, Mixed Content, None, None)], None), ParentNode(p, None, [LeafNode(None, Here is a bullet point list with formatting:, None, None)], None), ParentNode(ul, None, [ParentNode(li, None, [LeafNode(b, Bolded item, None, None)], None), ParentNode(li, None, [LeafNode(i, Italicized item, None, None)], None)], None), ParentNode(p, None, [LeafNode(None, Here is a numbered list with a link:, None, None)], None), ParentNode(ol, None, [ParentNode(li, None, [LeafNode(None, Visit , None, None), LeafNode(a, OpenAI, None, {'href': 'https://www.openai.com'}), LeafNode(None, ., None, None)], None), ParentNode(li, None, [LeafNode(None, See the image above., None, None)], None), ParentNode(li, None, [LeafNode(None, Test , None, None), LeafNode(b, mixed styles, None, None), LeafNode(None,  here., None, None)], None)], None), ParentNode(blockquote, None, [LeafNode(None, This is a wise quote, None, None)], None), ParentNode(blockquote, None, [LeafNode(None, This is another quote, None, None)], None), ParentNode(pre, None, [LeafNode(code, \nprint("Hello World!")\nprint("Hello")\n, None, None)], None)], None)"""
        parent_node = markdown_to_html_node(text)
        self.assertEqual(str(parent_node), test_answer)


if __name__ == "__main__":
    unittest.main()
