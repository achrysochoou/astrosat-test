"""
.. module:: astrosat_tags

defines custom template tags
"""

from django import template
from django.conf import settings
from django.db.models.query import QuerySet
from django.core.serializers import serialize
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
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
# def profanities():
#     return mark_safe(PROFANITIES_LIST)
#
#
# @register.simple_tag
# def reserved_words():
#     return mark_safe(RESERVED_WORDS)
#
#
# @register.simple_tag
# def bad_chars():
#     BAD_CHARS_LIST = BAD_CHARS.split(' ')
#     return mark_safe(BAD_CHARS_LIST)

#######################
# authentication tags #
#######################


#################
# dynamic sites #
#################

@register.filter
def site_type(site):
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
def a_or_an(value):
    """
    filter to return "a" or "an" depending on whether string starts with a vowel sound
    """
    # TODO: handle confusing things like "an hour" or "a unicycle"
    vowel_sounds = ["a", "e", "i", "o", "u"]
    if value[0].lower() in vowel_sounds:
        return "an"
    else:
        return "a"


@register.filter
def format(value, arg):
    """
    Alters default filter "stringformat" to not add the % at the front,
    so the variable can be placed anywhere in the string.
    """
    try:
        if value is not None:
            # return (str(arg)) % value
            return (str(value)) % arg
        else:
            return ""
    except (ValueError, TypeError):
        return ""
