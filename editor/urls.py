from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.edition, name='edition'),
    path('listo/', views.edited, name='edited'),

    path('agencia/crear', views.create_agency, name='create_agency'),
    path('rutas/crear', views.create_route, name='create_route'),
    path('stop/crear', views.create_stop, name='create_stop'),
    path('zone/crear', views.create_zone, name='create_zone'),
    path('calendar/crear', views.create_calendar, name='create_calendar'),
    path('calendar_date/crear', views.create_calendar_date, name='create_calendar_date'),
    path('fare_attribute/crear', views.create_fare_attribute, name='create_fare_attribute'),
    path('feed_info/crear', views.create_feed_info, name='create_feed_info'),
    path('fare_rule/crear', views.create_fare_rule, name='create_fare_rule'),


    path('agencia/lista', views.list_agency, name='list_agency'),
    path('ruta/lista', views.list_route, name='list_route'),
    path('stop/lista', views.list_stop, name='list_stop'),
    path('zone/lista', views.list_zone, name='list_zone'),
    path('calendar/lista', views.list_calendar, name='list_calendar'),
    path('calendar_dates/lista', views.list_calendar_dates, name='list_calendar_dates'),
    path('fare_attribute/lista', views.list_fare_attribute, name='list_fare_attribute'),
    path('feed_info/lista', views.list_feed_info, name='list_feed_info'),
    path('fare_rule/lista', views.list_fare_rule, name='list_fare_rule'),


    path('agencia/eliminar/<agency_id>/', views.delete_agency, name='delete_agency'),
    path('ruta/eliminar/<route_id>/', views.delete_route, name='delete_route'),
    path('zone/eliminar/<zone_id>/', views.delete_zone, name='delete_zone'),
    path('stop/eliminar/<stop_id>/', views.delete_stop, name='delete_stop'),
    path('calendar/eliminar/<service_id>/', views.delete_calendar, name='delete_calendar'),
    path('calendar_date/eliminar/<service_id>/', views.delete_calendar_dates, name='delete_calendar_dates'),
    path('fare_attribute/eliminar/<fare_id>/', views.delete_fare_attribute, name='delete_fare_attribute'),
    path('feed_info/eliminar/<feed_info_id>/', views.delete_feed_info, name='delete_feed_info'),
    path('fare_rule/eliminar/<fare_rule_id>/', views.delete_fare_rule, name='delete_fare_rule'),


    path('agencia/editar/<int:agency_id>/', views.edit_agency, name='edit_agency'),
    path('ruta/editar/<int:route_id>/', views.edit_route, name='edit_route'),
    path('zone/editar/<zone_id>/', views.edit_zone, name='edit_zone'),
    path('stop/editar/<stop_id>/', views.edit_stop, name='edit_stop'),
    path('calendar/editar/<service_id>/', views.edit_calendar, name='edit_calendar'),
    path('calendar_dates/editar/<service_id>/', views.edit_calendar_dates, name='edit_calendar_dates'),
    path('fare_attribute/editar/<fare_id>/', views.edit_fare_attribute, name='edit_fare_attribute'),
    path('feed_info/editar/<feed_info_id>/', views.edit_feed_info, name='edit_feed_info'),
    path('fare_rule/editar/<fare_rule_id>/', views.edit_fare_rule, name='edit_fare_rule'),

]