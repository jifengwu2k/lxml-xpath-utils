import os.path
from typing import Iterator, Optional, List

from lxml.etree import ElementBase


def inner_text(element: ElementBase) -> str:
    """Extracts the combined text content of an element and its descendants."""
    return ''.join(element.itertext())


def find_deepest_elements_containing_target_text(
    element: ElementBase,
    target_text: str,
) -> Iterator[ElementBase]:
    """
    Recursively searches for the deepest elements containing target text, starting from leaf nodes.

    Uses a depth-first, post-order traversal to efficiently locate matching elements.
    """
    children: List[ElementBase] = list(element)

    if not children:  # Base case: leaf node
        if target_text in inner_text(element):
            yield element
        return  # Important: exit the function after processing the leaf

    # Recursive case: iterate over children
    for child in children:
        yield from find_deepest_elements_containing_target_text(child, target_text)


def get_xpath_components(element: ElementBase, relative_to: Optional[ElementBase] = None) -> Iterator[str]:
    """
    Generates XPath components for an element.

    Handles special cases for the root element and relative XPath.
    """
    parent: Optional[ElementBase] = element.getparent()

    if parent is None:  # Root element
        yield '/'
        yield element.tag
    elif relative_to is not None and element == relative_to:  # Element is the relative base
        yield '.'  # Use '.' for the base element itself
    else:
        yield from get_xpath_components(parent, relative_to)  # Recurse to parent

        siblings: List[ElementBase] = [child for child in parent if child.tag == element.tag]
        if len(siblings) == 1:
            yield element.tag  # Unique tag
        else:
            index = siblings.index(element) + 1
            yield f'{element.tag}[{index}]'  # Indexed tag


def get_xpath(element: ElementBase, relative_to: Optional[ElementBase] = None) -> str:
    """
    Constructs the XPath expression for an element.
    """
    xpath_components: Iterator[str] = get_xpath_components(element, relative_to)

    first: str = next(xpath_components)
    remaining: Iterator[str] = xpath_components

    return os.path.join(first, *remaining)
