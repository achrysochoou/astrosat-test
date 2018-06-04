from django.conf import settings

# simple context processors that allow me to reference settings variables in templates
# be sure to add these to "settings.py"


def astrosat_debug(context):
    """
    simple context processor that allows me to use a "debug" template tag
    without requiring me to explicitly provide "INTERNAL_IPS" in settings.py
    (as per http://stackoverflow.com/a/13609888/1060339)
    :param context:
    :return:
    """
    return {
        "debug": settings.DEBUG
    }


def astrosat_cdn(context):
    """
    simple context processor that allows me to access the CDN setting from a template
    :param context:
    :return:
    """
    return {
        "cdn": settings.CDN
    }
