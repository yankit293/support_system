from django.contrib import admin
from .models import RaiseRequest, Issue, Status, ReportUser, Reason, ReportContent


class RaiseRequestAdmin(admin.ModelAdmin):
    list_display = ( 'date','name', 'email', 'phone_number', 'description','issue','status','user',)
    search_fields = ('name', 'email',)
    date_hierarchy = 'date'


admin.site.register(RaiseRequest, RaiseRequestAdmin)
admin.site.register(Issue)
admin.site.register(Status)
admin.site.register(ReportUser)
admin.site.register(ReportContent)
admin.site.register(Reason)

