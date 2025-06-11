import posixpath

from lxml.etree import ElementBase


def inner_text(element):
    """Extracts the combined text content of an element and its descendants."""
    return ''.join(element.itertext())


def find_deepest_elements_containing_target_text(element, target_text):
    """
    Recursively searches for the deepest elements containing target text, starting from leaf nodes.

    Uses a depth-first, post-order traversal to efficiently locate matching elements.
    """
    children = list(element)

    if not children:  # Base case: leaf node
        if target_text in inner_text(element):
            yield element
        return  # Important: exit the function after processing the leaf

    # Recursive case: iterate over children
    for child in children:
        for _ in find_deepest_elements_containing_target_text(child, target_text):
            yield _


def get_xpath_components(element, relative_to=None):
    """
    Generates XPath components for an element.

    Handles special cases for the root element and relative XPath.
    """
    parent = element.getparent()

    if parent is None:  # Root element
        yield '/'
        yield element.tag
    elif relative_to is not None and element == relative_to:  # Element is the relative base
        yield '.'  # Use '.' for the base element itself
    else:
        for _ in get_xpath_components(parent, relative_to):  # Recurse to parent
            yield _

        siblings = [child for child in parent if child.tag == element.tag]
        if len(siblings) == 1:
            yield element.tag  # Unique tag
        else:
            index = siblings.index(element) + 1
            yield '%s[%d]' % (element.tag, index)  # Indexed tag


def get_xpath(element, relative_to=None):
    """
    Constructs the XPath expression for an element.
    """
    xpath_components = get_xpath_components(element, relative_to)

    first = next(xpath_components)
    remaining = xpath_components

    return posixpath.join(first, *remaining)
