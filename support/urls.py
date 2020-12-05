from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('paymentissue/', views.paymentissue, name='payment'),
    path('paymentissue/status/', views.paymentallissuestatus, name='paymentissueallstatus'),
    path('paymentissue/status/<int:id>/',views.paymentissuestatus, name='paymentissuestatus'),
    path('paymentissue/delete/<str:pk>/', views.deletepaymentissue, name='deletepaymentissue'),
    #Get usernames
    path('get_usernames/', views.get_usernames, name='get_usernames'),
    #Report User
    path('reportuser/', views.reportuser, name='reportuser'),
    path('reportuser/status/', views.reportalluserstatus, name='reportuserallstatus'),
    path('reportuser/status/<int:id>/',views.reportuserstatus, name='reportuserstatus'),
    path('delete/reportuser/<str:pk>/', views.delete_report_user, name='delete_report_user'),
    #Report Content
    path('reportcontent/', views.reportcontent, name='reportcontent'),
    path('reportcontent/status/', views.reportallcontentstatus, name='reportcontentallstatus'),
    path('reportcontent/status/<int:id>/',views.reportcontentstatus, name='reportcontentstatus'),
    path('delete/reportcontent/<str:pk>/', views.delete_report_content, name='delete_report_content'),
]