from django.db import models
from django.db.models.fields import FieldDoesNotExist

from astrosat import APP_LABEL


class AstrosatModel(models.Model):
    """
    base class for all my models
    includes the get_field fn below
    """
    class Meta:
        app_label = APP_LABEL
        abstract = True

    @classmethod
    def get_field(cls, field_name):
        """
        convenience fn for getting a Django Field
        note that this can take as input a JSON-style name to better work w/ Angular
        :param field_name: a fully-qualified field name (ie: "model.child.field")
        :return:
        """
        try:
            model_class = cls
            for fn in field_name.split("."):
                field = model_class._meta.get_field(fn)
                model_class = field.related_model
            return field
        except (AttributeError, FieldDoesNotExist):
            return None
