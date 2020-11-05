from django.contrib import admin
from .models import RaiseRequest, Issue




class RaiseRequestAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'email', 'phone_number', 'description','issue',)
    search_fields = ('name', 'email',)
    date_hierarchy = 'date'





admin.site.register(RaiseRequest, RaiseRequestAdmin)
admin.site.register(Issue)

