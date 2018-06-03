from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.sites.models import Site
from django.db.models import Q
from django.forms import ModelForm

from astrosat.models.models_sites import AstrosatSite

__author__ = 'allyn.treshansky'


class SiteAdminForm(ModelForm):
    class Meta:
        model = Site
        fields = ("name", "domain")

    def clean(self):
        """
        prevents duplicate sites
        :return:
        """
        cleaned_data = super(SiteAdminForm, self).clean()
        site = self.instance
        existing_sites = Site.objects.filter(
            Q(name=cleaned_data["name"]) |
            Q(domain=cleaned_data["domain"]))\
            .exclude(pk=site.pk)
        if existing_sites:
            msg = "Sites must have unique names and domains."
            raise ValidationError(msg)
        return cleaned_data


class AstrosatSiteInline(admin.StackedInline):
    model = AstrosatSite
    can_delete = False
    verbose_name = "Astrosat Site Type"
    verbose_name_plural = "Astrosat Site Types"


class AstrosatSiteAdmin(admin.ModelAdmin):
    inlines = (AstrosatSiteInline, )
    form = SiteAdminForm

# when db is 1st setup, built-in Site may be registered before Q classes
try:
    admin.site.register(Site, AstrosatSiteAdmin)
except AlreadyRegistered:
    admin.site.unregister(Site)
    admin.site.register(Site, AstrosatSiteAdmin)
