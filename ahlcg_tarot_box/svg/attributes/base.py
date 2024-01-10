from dataclasses import dataclass


def value_to_str(value):
  if isinstance(value, list | tuple | set):
    return ' '.join((
        str(v)
        for v in value
    ))

  return str(value)


def attrs_to_str(attrs: 'Attributes', namespace: str | None = None):
  return ' '.join((
      attr_to_str(k, v, namespace)
      for k, v in attrs.__dict__.items()
      if v is not None
  ))


def attr_to_str(key: str, value, namespace: str | None = None) -> str:
  if isinstance(value, XmlNamespace):
    return attrs_to_str(value, key)

  key = key.replace('_', '-')
  if namespace:
    return f'{namespace}:{key}="{value_to_str(value)}"'

  return f'{key}="{value_to_str(value)}"'


class Attribute[T]():
  def __init__(self, value: T):
    self.value = value

  def __str__(self):
    return str(self.value)


@dataclass
class Attributes():
  pass


@dataclass
class XmlNamespace(Attributes):
  base: str | None = None
  lang: Attribute | None = None
  space: Attribute | None = None
