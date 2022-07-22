from django.contrib import admin

# Register your models here.
from pyorc.parties.models import Party, PartyType


class PartyAdmin(admin.ModelAdmin):
    exclude = ("id", "created_at")
    list_filter = ("year", "party_type")
    search_fields = ("name", "scenario_name", "desk_name")


class PartyTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Party, PartyAdmin)
admin.site.register(PartyType, PartyTypeAdmin)
