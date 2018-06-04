"""
.. module:: astrosat_tags

defines custom template tags
"""

from django import template
from django.conf import settings
from django.db.models.query import QuerySet
from django.core.serializers import serialize
import json

from astrosat import get_version
from astrosat.models.models_sites import AstrosatSite
from astrosat.constants import *

register = template.Library()

#####################
# get static things #
#####################


@register.simple_tag
def astrosat_version():
    return get_version()


@register.simple_tag
def astrosat_url():
    return settings.ASTROSAT_CODE_URL


@register.simple_tag
def astrosat_email():
    return settings.ASTROSAT_EMAIL

# @register.simple_tag
# def bad_chars():
#     BAD_CHARS_LIST = BAD_CHARS.split(' ')
#     return mark_safe(BAD_CHARS_LIST)


#################
# dynamic sites #
#################

@register.filter
def site_type(site):
    """
    Tells me what type of site this is
    See "astrosat.middleware.dynamic_sites" for more information
    :param site:
    :return:
    """
    try:
        astrosat_site = site.astrosat_site
        return astrosat_site.type
    except AstrosatSite.DoesNotExist:
        return None

################
# utility tags #
################


@register.filter
def index(sequence, i):
    """
    returns the ith element in the sequence, otherwise returns an empty string
    inexplicably, Django doesn't have a nice way to do this
    :param sequence:
    :param i:
    :return:
    """
    try:
        return sequence[i]
    except IndexError:
        return u""


@register.filter
def jsonify(object):
    """
    returns a JSON representation of [a set of] object[s]
    :param object:
    :return:
    """
    # note: ng provides a "json" filter that can do this too
    # note: but Django doesn't [https://code.djangoproject.com/ticket/17419]
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return json.dumps(object)

@register.filter
def format(value, arg):
    """
    Alters default filter "stringformat" to not add the % at the front,
    so the variable can be placed anywhere in the string - more pythonic that way
    """
    try:
        if value is not None:
            # return (str(arg)) % value
            return (str(value)) % arg
        else:
            return ""
    except (ValueError, TypeError):
        return ""
