from ..attributes.base import attrs_to_str
from ..attributes.core import Attributes


class Element[Attrs: Attributes]:
  element: str

  def __init__(self, attrs: Attrs | None = None, children: list['Element | str'] | None = None):
    self.attrs = attrs or Attributes()
    self.children = children or []

  def __iter__(self):
    yield from self.children

  def __str__(self):
    element = self.element
    element_attrs = ' '.join((
        element,
        attrs_to_str(self.attrs),
    ))
    children = '\n'.join((
        f'\t{subchild}'
        for child in self.children
        for subchild in str(child).split('\n')
    ))
    if not children:
      return f'<{element_attrs}/>'

    return f'<{element_attrs}>\n{children}\n</{element}>'
