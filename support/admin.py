from django.contrib import admin
from .models import RaiseRequest, Issue, Status


class RaiseRequestAdmin(admin.ModelAdmin):
    list_display = ( 'date','name', 'email', 'phone_number', 'description','issue','status',)
    search_fields = ('name', 'email',)
    date_hierarchy = 'date'


admin.site.register(RaiseRequest, RaiseRequestAdmin)
admin.site.register(Issue)
admin.site.register(Status)

