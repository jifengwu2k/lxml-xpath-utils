A collection of utility functions for working with `lxml` and XPath.

Supports Python 2+.

## Functions

*   `inner_text(element: ElementBase) -> str`: Extracts the combined text content of an element and its descendants, like accessing JavaScript's innerText attribute.
*   `find_deepest_elements_containing_target_text(element: ElementBase, target_text: str) -> Iterator[ElementBase]`:  A generator that yields the deepest elements containing target text, starting from leaf nodes.
*   `get_xpath(element: ElementBase, relative_to: Optional[ElementBase] = None) -> str`:  Generates the absolute or relative XPath expression for a given `lxml` element.  If `relative_to` is specified, the XPath will be relative to that element.

## Usage

Here's a brief example of how to use the functions:

```python
from __future__ import print_function

from lxml import etree

from lxml_xpath_utils import inner_text, find_deepest_elements_containing_target_text, get_xpath

html = """<html>
    <body>
        <div id="main">
            <p>This is a paragraph with target text.</p>
            <div class="nested">
                <span>Some text here</span>
                <p>Another paragraph with target text in it.</p>
            </div>
            <p>No match here</p>
        </div>
        <div id="other">
            <p>target text appears again here</p>
        </div>
    </body>
</html>"""

target_text = "target text"

parser = etree.HTMLParser()
root = etree.fromstring(html, parser)

matching_elements = find_deepest_elements_containing_target_text(root, target_text)

print("Elements containing '%s':" % target_text)
for elem in matching_elements:
    absolute_xpath = get_xpath(elem)
    print(absolute_xpath)
    assert elem == root.xpath(absolute_xpath)[0]
    print("  Text: %s\n" % inner_text(elem))

print("Elements containing '%s' in /html/body/div[@id='main']:" % target_text)
new_root = root.xpath('/html/body/div[@id="main"]')[0]
new_matching_elements = find_deepest_elements_containing_target_text(new_root, target_text)

for new_elem in new_matching_elements:
    relative_xpath = get_xpath(new_elem, new_root)
    print(relative_xpath)
    assert new_elem == new_root.xpath(relative_xpath)[0]
    print("  Text: %s\n" % inner_text(new_elem))
```

Output:

```
Elements containing 'target text':
/html/body/div[1]/p[1]
  Text: This is a paragraph with target text.

/html/body/div[1]/div/p
  Text: Another paragraph with target text in it.

/html/body/div[2]/p
  Text: target text appears again here

Elements containing 'target text' in /html/body/div[@id='main']:
./p[1]
  Text: This is a paragraph with target text.

./div/p
  Text: Another paragraph with target text in it.

```

## Contributing

Feel free to contribute to this project by submitting pull requests or opening issues.

## License

This project is licensed under the [MIT License](LICENSE).
