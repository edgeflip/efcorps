import json
import re

from django.core.exceptions import ValidationError
from django.db import models
from south.modelsinspector import add_introspection_rules


add_introspection_rules([], ['^' + re.escape(__name__)])


class JSONField(models.Field):

    __metaclass__ = models.SubfieldBase

    def db_type(self, connection):
        return 'json'

    def get_prep_value(self, value):
        return json.dumps(value)

    def to_python(self, value):
        if isinstance(value, basestring):
            try:
                return json.loads(value)
            except ValueError as exc:
                raise ValidationError(exc)

        try:
            self.get_prep_value(value)
        except ValueError as exc:
            raise ValidationError(exc)
        else:
            return value


class BigSerialField(models.AutoField):

    def db_type(self, connection):
        return 'bigserial'

    def get_internal_type(self):
        return 'BigIntegerField'

    def get_related_db_type(self, connection):
        return models.BigIntegerField().db_type(connection)


class FlexibleForeignKey(models.ForeignKey):

    def db_type(self, connection):
        try:
            get_related_db_type = self.related_field.get_related_db_type
        except AttributeError:
            return super(FlexibleForeignKey, self).db_type(connection)
        else:
            return get_related_db_type(connection)
