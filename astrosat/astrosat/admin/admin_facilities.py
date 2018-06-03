
from django.contrib import admin

from django.forms import ModelForm

from astrosat.models.models_facilities import Facility


class FacilityAdminForm(ModelForm):
    class Meta:
        model = Facility
        fields = (
            'id',
            'center',
            'center_search_status',
            'facility',
            'facilityurl',
            'occupied',
            'status',
            'url_link',
            'record_date',
            'last_update',
            'country',
            'contact',
            'phone',
            # 'location',
            'city',
            'state',
            'zipcode',
        )


class FacilityAdmin(admin.ModelAdmin):
    form = FacilityAdminForm

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(FacilityAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(Facility, FacilityAdmin)

