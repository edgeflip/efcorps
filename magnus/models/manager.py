import enum
import functools
import re

import django.db.models.manager

from magnus.utils import functional


class Types(enum.Enum):
    pass


class TypeObjectManager(django.db.models.manager.Manager):

    Types = Types
    getter_pattern = re.compile(r'^get_([a-z][a-z0-9_]*)$')

    @functional.cached_property
    def types(self):
        for kls in self.model.mro():
            # issubclass demands class so check for EnumMeta first
            defns = [value for value in kls.__dict__.values()
                     if isinstance(value, enum.EnumMeta) and issubclass(value, self.Types)]
            if defns:
                try:
                    (types,) = defns
                except ValueError:
                    raise LookupError("Model defines multiple types")
                return types
        raise LookupError("Model defines no types")

    @property
    def type_field_name(self):
        try:
            field = self.types.__field__
        except AttributeError:
            return self.types.__name__.lower()[:-1]
        else:
            return field if isinstance(field, basestring) else field.name

    def get_type(self, type_):
        return self.get(**{self.type_field_name: type_})

    def __getattr__(self, attr):
        type_match = self.getter_pattern.search(attr)
        if type_match:
            type_name = type_match.group(1)
            try:
                type_member = self.types[type_name.upper()]
            except KeyError:
                pass
            else:
                getter = functools.partial(self.get_type, type_member.value)
                getter.__dict__.update(
                    __name__=attr,
                    __module__=self.get_type.__module__,
                )
                setattr(self, attr, getter)
                return getter

        raise AttributeError("'{}' object has no attribute {!r}"
                             .format(self.__class__.__name__, attr))
