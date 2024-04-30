from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_companies, name='compañías'),
    path('listo/', views.edited, name='edited'),

    # METODOS DE CREAR
    path('agencia/crear/<company_id>/', views.create_agency, name='create_agency'),
    path('ruta/crear/<company_id>/', views.create_route, name='create_route'),
    path('parada/crear/<company_id>/', views.create_stop, name='create_stop'),
    path('zonas/crear/<company_id>/', views.create_zone, name='create_zone'),
    path('calendario/crear/<company_id>/', views.create_calendar, name='create_calendar'),
    path('fecha_de_calendario/crear/<id>/<company_id>/', views.create_calendar_date, name='create_calendar_date'),
    path('tarifa/crear/<company_id>/', views.create_fare_attribute, name='create_fare_attribute'),

    path('regla_de_tarifa/crear/<company_id>/', views.create_fare_rule, name='create_fare_rule'),
    path('compañía/crear', views.create_company, name='create_company'),
    path('feed/crear', views.create_feed, name='create_feed'),


    # METODOS DE LISTAR
    path('compañía/lista', views.list_company, name='list_company'),
    path('feed/lista/<company_id>/', views.list_feed, name='list_feed'),


    # METODOS DE ELIMINAR
    path('agencia/eliminar/<id>/', views.delete_agency, name='delete_agency'),
    path('ruta/eliminar/<id>/<str:company_id>/', views.delete_route, name='delete_route'),
    path('zona/eliminar/<id>/<str:company_id>/', views.delete_zone, name='delete_zone'),
    path('parada/eliminar/<id>/<str:company_id>/', views.delete_stop, name='delete_stop'),
    path('calendario/eliminar/<id>/<str:company_id>/', views.delete_calendar, name='delete_calendar'),
    path('fecha_de_calendario/eliminar/<id>/<company_id>/<calendar_id>', views.delete_calendar_dates, name='delete_calendar_dates'),
    path('tarifa/eliminar/<id>/<str:company_id>/', views.delete_fare_attribute, name='delete_fare_attribute'),

    path('regla_de_tarifa/eliminar/<id>/<str:company_id>/', views.delete_fare_rule, name='delete_fare_rule'),
    path('compañía/eliminar/<company_id>/', views.delete_company, name='delete_company'),
    path('feed/eliminar/<id>/<str:company_id>/', views.delete_feed, name='delete_feed'),

    # METODOS DE EDITAR
    path('agencia/editar/<int:id>/<str:company_id>/', views.edit_agency, name='edit_agency'),
    path('ruta/editar/<int:id>/<str:company_id>/', views.edit_route, name='edit_route'),
    path('zona/editar/<id>/<str:company_id>/', views.edit_zone, name='edit_zone'),
    path('parada/editar/<id>/<str:company_id>/', views.edit_stop, name='edit_stop'),
    path('calendario/editar/<id>/<str:company_id>/', views.edit_calendar, name='edit_calendar'),
    path('fecha_de_calendario/editar/<id>/<company_id>/<calendar_id>', views.edit_calendar_dates, name='edit_calendar_dates'),
    path('tarifa/editar/<id>/<str:company_id>/', views.edit_fare_attribute, name='edit_fare_attribute'),
    path('información_del_feed/editar/<id>/<company_id>/', views.edit_feed_info, name='edit_feed_info'),
    path('regla_de_tarifa/editar/<id>/<str:company_id>/', views.edit_fare_rule, name='edit_fare_rule'),
    path('compañía/editar/<company_id>/', views.edit_company, name='edit_company'),
    path('feed/editar/<feed_id>/<str:company_id>/', views.edit_feed, name='edit_feed'),

    # PÁGINAS DE COMPAÑÍA
    path('compañías/lista', views.list_companies, name='list_companies'),
    path('compañías/agencias/<str:company_id>/', views.company_agency, name='company_agency'),
    path('compañías/rutas/<str:company_id>/', views.company_route, name='company_route'),
    path('compañías/paradas/<str:company_id>/', views.company_stop, name='company_stop'),
    path('compañías/zonas/<str:company_id>/', views.company_zone, name='company_zone'),
    path('compañías/calendario/<str:company_id>/', views.company_calendar, name='company_calendar'),
    path('compañías/tarifa/<str:company_id>/', views.company_fare_attribute, name='company_fare_attribute'),
    path('compañías/reglas_de_tarifa/<str:company_id>/', views.company_fare_rule, name='company_fare_rule'),
    path('compañías/fechas_de_calendario/<str:id>/<str:company_id>/', views.company_calendar_date, name='company_calendar_date'),
    path('compañías/información_del_feed/<str:company_id>/', views.company_feed_info, name='company_feed_info'),


    # MÉTODOS PARA ASIGNAR O ELIMINAR LAS RUTAS DE UNA AGENCIA 
    # QUE VA A SER ELIMINADA
    path('ver_rutas_de_agencia/<str:id>/', views.view_agency_routes, name='view_agency_routes'),
    path('agencia/eliminar_todas_las_rutas/<str:id>/', views.delete_all_routes, name='delete_all_routes'),
    path('actualizar_rutas_de_agencia/<str:id>/', views.update_all_routes_agency, name='update_all_routes_agency'),
    path('actualizar_ruta_de_agencia/<str:id>/<str:route_id>/', views.update_route, name='update_route'),
    path('eliminar_ruta_de_agencia/<str:id>/<str:route_id>/', views.delete_agency_route, name='delete_agency_route'),

    # MÉTODOS PARA ASIGNAR O ELIMINAR LAS PARADAS DE UNA ZONA 
    # QUE VA A SER ELIMINADA
    path('ver_paradas_de_zona/<str:id>/', views.view_zone_stops, name='view_zone_stops'),
    path('agencia/eliminar_todas_las_paradas/<str:id>/', views.delete_all_stops, name='delete_all_stops'),
    path('actualizar_paradas_de_zona/<str:id>/', views.update_all_stops_zone, name='update_all_stops_zone'),
    path('actualizar_parada_de_zona/<str:id>/<str:stop_id>/', views.update_stop, name='update_stop'),
    path('eliminar_parada_de_zona/<str:id>/<str:stop_id>/', views.delete_zone_stop, name='delete_zone_stop'),



    path('cargar_contenido/', views.cargar_contenido, name='cargar_contenido'),
    path('seleccionar_feed/<str:feed_id>/<str:company_id>/', views.select_feed, name='select_feed'),
]