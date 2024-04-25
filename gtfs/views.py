import uuid
from django.shortcuts import render, redirect
from gtfs.models import Agency, Route, Stop, Zone, Calendar, CalendarDate
from gtfs.models import FareAttribute, FeedInfo, FareRule, Company, Feed
from django.contrib.gis.geos import Point
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseBadRequest
import os
from django.core.files import File
from django.contrib import messages

# Create your views here.


def edition(request):
    return render(request, 'edition.html')


def duplicate_agencies(original_feed, duplicate_feed):

    # Duplicar agencias relacionadas al feed original
    original_agencies = Agency.objects.filter(feed_id=original_feed.feed_id)
    for original_agency in original_agencies:
        Agency.objects.create(
            feed_id=duplicate_feed,
            agency_id=original_agency.agency_id,
            name=original_agency.name,
            url=original_agency.url,
            timezone=original_agency.timezone,
            lang=original_agency.lang,
            phone=original_agency.phone,
            fare_url=original_agency.fare_url,
            email=original_agency.email,
        )

def duplicate_routes(original_feed, duplicate_feed):

    # Duplicar rutas relacionadas al feed original
    original_routes = Route.objects.filter(feed_id=original_feed.feed_id)
    for original_route in original_routes:

        # Obtén la agencia con el mismo agency_id y con un id mayor
        original_agency = original_route.agency
        new_agency = Agency.objects.filter(agency_id=original_agency.agency_id).order_by('-id').first()

        # Crea la nueva ruta y asocia la nueva agencia si se encontró, de lo contrario, agencia será None
        new_route = Route.objects.create(
            feed_id=duplicate_feed,
            route_id=original_route.route_id,
            agency=new_agency,
            short_name=original_route.short_name,
            long_name=original_route.long_name,
            desc=original_route.desc,
            route_type=original_route.route_type,
            url=original_route.url,
            color=original_route.color,
            text_color=original_route.text_color,
        )
        
        # Verifica si se encontró una nueva agencia
        if new_agency:
            new_route.agency = new_agency
            new_route.save()
        else:
            print(f"No se encontró una agencia con id mayor para {original_agency.agency_id}")

def duplicate_stops(original_feed, duplicate_feed):

    # Duplicar paradas relacionadas al feed original
    original_stops = Stop.objects.filter(feed_id=original_feed.feed_id)
    for original_stop in original_stops:

        # Obtén la zona con el mismo zone_id y con un id mayor
        original_zone = original_stop.zone
        new_zone = Zone.objects.filter(zone_id=original_zone.zone_id).order_by('-id').first()

        new_stop = Stop.objects.create(
            feed_id=duplicate_feed,
            stop_id=original_stop.stop_id,
            name=original_stop.name,
            desc=original_stop.desc,
            lat=original_stop.lat,
            lon=original_stop.lon,
            loc=original_stop.loc,
            zone=original_stop.zone,
            url=original_stop.url,
            location_type=original_stop.location_type,
            parent_station=original_stop.parent_station,
            wheelchair_boarding=original_stop.wheelchair_boarding,
        )

        # Verifica si se encontró una nueva agencia
        if new_zone:
            new_stop.zone = new_zone
            new_stop.save()
        else:
            print(f"No se encontró una agencia con id mayor para {original_zone.zone_id}")

def duplicate_calendars(original_feed, duplicate_feed):

    # Duplicar calendarios relacionados al feed original
    original_calendars = Calendar.objects.filter(feed_id=original_feed.feed_id)
    for original_calendar in original_calendars:
        Calendar.objects.create(
            feed_id=duplicate_feed,
            service_id=original_calendar.service_id,
            monday=original_calendar.monday,
            tuesday=original_calendar.tuesday,
            wednesday=original_calendar.wednesday,
            thursday=original_calendar.thursday,
            friday=original_calendar.friday,
            saturday=original_calendar.saturday,
            sunday=original_calendar.sunday,
            start_date=original_calendar.start_date,
            end_date=original_calendar.end_date,
        )

def duplicate_zones(original_feed, duplicate_feed):

    # Duplicar zonas relacionadas al feed original
    original_zones = Zone.objects.filter(feed_id=original_feed.feed_id)
    for original_zone in original_zones:
        Zone.objects.create(
            feed_id=duplicate_feed,
            zone_id=original_zone.zone_id,
        )

def duplicate_fare_attributes(original_feed, duplicate_feed):

    # Duplicar atributos de tarifa relacionados al feed original
    original_fare_attributes = FareAttribute.objects.filter(feed_id=original_feed.feed_id)
    for original_fare_attribute in original_fare_attributes:

        # Obtén la agencia con el mismo agency_id y con un id mayor
        original_agency = original_fare_attribute.agency
        new_agency = Agency.objects.filter(agency_id=original_agency.agency_id).order_by('-id').first()

        new_fare_attribute = FareAttribute.objects.create(
            feed_id=duplicate_feed,
            agency=new_agency, 
            fare_id=original_fare_attribute.fare_id,
            price=original_fare_attribute.price,
            currency_type=original_fare_attribute.currency_type,
            payment_method=original_fare_attribute.payment_method,
            transfers=original_fare_attribute.transfers,
            transfer_duration=original_fare_attribute.transfer_duration,
        )

def duplicate_fare_rules(original_feed, duplicate_feed):

    # Duplicar reglas de tarifa relacionadas al feed original
    original_fare_rules = FareRule.objects.filter(feed_id=original_feed.feed_id)
    for original_fare_rule in original_fare_rules:

        # Obtiene la tarifa con el mismo fare_id y con un id mayor
        original_fare_attribute = original_fare_rule.fare
        new_fare_attribute = FareAttribute.objects.filter(fare_id=original_fare_attribute.fare_id).order_by('-id').first()

        # Obtiene la ruta con el mismo route_id y con un id mayor
        original_route = original_fare_rule.route
        new_route = Route.objects.filter(route_id=original_route.route_id).order_by('-id').first()

        # Obtiene el origen con el mismo zone_id y con un id mayor
        original_origin = original_fare_rule.origin
        new_origin = Zone.objects.filter(zone_id=original_origin.zone_id).order_by('-id').first()

        # Obtiene el destino con el mismo zone_id y con un id mayor
        original_destination = original_fare_rule.destination
        new_destination = Zone.objects.filter(zone_id=original_destination.zone_id).order_by('-id').first()

        FareRule.objects.create(
            feed_id=duplicate_feed,
            fare=new_fare_attribute,
            route=new_route,
            origin=new_origin,
            destination=new_destination,
        )

def duplicate_calendar_dates(original_feed, duplicate_feed):

    # Duplicar fechas del calendario relacionadas al feed original
    original_calendar_dates = CalendarDate.objects.filter(feed_id=original_feed.feed_id)
    for original_calendar_date in original_calendar_dates:

        # Obtén el calendario con el mismo service_id y con un id mayor
        original_calendar = original_calendar_date.service
        new_calendar = Calendar.objects.filter(service_id=original_calendar.service_id).order_by('-id').first()

        new_calendar_date = CalendarDate.objects.create(
            feed_id=duplicate_feed,
            service=original_calendar_date.service,
            date=original_calendar_date.date,
            exception_type=original_calendar_date.exception_type,
            holiday_name=original_calendar_date.holiday_name,
        )

        # Verifica si se encontró una nueva agencia
        if new_calendar:
            new_calendar_date.service = new_calendar
            new_calendar_date.save()
        else:
            print(f"No se encontró una agencia con id mayor para {original_calendar.service_id}")

def duplicate_feed_info(original_feed, duplicate_feed):
    # Obtener la última versión del feed info para este feed
    last_feed_info = FeedInfo.objects.filter(feed_id=original_feed).order_by('-version').first()
    
    if last_feed_info:
        # Si hay una versión anterior, incrementarla en 1
        new_version = str(int(last_feed_info.version) + 1)
    else:
        # Si no hay versiones anteriores, establecer la versión inicial en 1
        new_version = '1'

    # Crear una nueva instancia de FeedInfo
    new_feed_info = FeedInfo.objects.create(
        feed_id=duplicate_feed,
        publisher_name=last_feed_info.publisher_name,
        publisher_url=last_feed_info.publisher_url,
        lang=last_feed_info.lang,
        start_date=last_feed_info.start_date,
        end_date=last_feed_info.end_date,
        version=new_version,
        contact_email=last_feed_info.contact_email
    )

    new_feed_info.save()    


def duplicate_feed(feed_id):
    # Obtener el feed original
    original_feed = Feed.objects.get(feed_id=feed_id)

    # Obtiene la fecha y hora actual
    current_datetime = datetime.now()

    # Crea una cadena de feed_id utilizando el formato: "YYYYMMDDHHMMSS"
    feed_id = "GTFS_" + current_datetime.strftime("%Y%m%d%H%M%S")

    # Crear un nuevo feed con los mismos atributos (excluyendo la clave principal)
    duplicate_feed = Feed(
        feed_id=feed_id,
        company_id=original_feed.company_id,
        created_at=timezone.now(),
        zip_file=original_feed.zip_file,
        is_current=True,  # Establecer is_current en True para el feed duplicado
        in_edition=original_feed.in_edition
    )

    # Guardar el nuevo feed sin comprometerlo en la base de datos
    duplicate_feed.save_base(raw=True)

    # Copiar el archivo zip a una nueva ubicación
    original_path = original_feed.zip_file.path
    new_path = os.path.join("gtfs/feeds/", f"copy_{timezone.now().strftime('%Y%m%d%H%M%S')}.zip")

    with open(original_path, 'rb') as original_file:
        with open(new_path, 'wb') as new_file:
            new_file.write(original_file.read())

    # Establecer el nuevo archivo zip para el feed duplicado
    duplicate_feed.zip_file.name = new_path
    duplicate_feed.zip_file.save(os.path.basename(new_path), File(open(new_path, 'rb')))

    # Establecer is_current en False para el feed original
    original_feed.is_current = False
    original_feed.save()

    # Duplicar agencias
    duplicate_agencies(original_feed, duplicate_feed)

    #Duplicar paradas
    duplicate_stops(original_feed, duplicate_feed)

    # Duplicar rutas
    duplicate_routes(original_feed, duplicate_feed)

    # Duplicar calendarios
    duplicate_calendars(original_feed, duplicate_feed)

    # Duplicar fechas de calendario
    duplicate_calendar_dates(original_feed, duplicate_feed)

    # Duplicar zonas
    duplicate_zones(original_feed, duplicate_feed)

    # Duplicar atributos de tarifa
    duplicate_fare_attributes(original_feed, duplicate_feed)

    # Duplicar reglas de tarifa
    duplicate_fare_rules(original_feed, duplicate_feed)

    # # Duplicar el feed info
    duplicate_feed_info(original_feed, duplicate_feed)

    # Guardar el feed duplicado con la nueva ruta del archivo zip
    duplicate_feed.save()

    return duplicate_feed


# MÉTODOS PARA CREAR 
def create_agency(request, company_id):
    # Verifica si la solicitud es de tipo POST
    if request.method == "POST":

        # Obtener el feed actual para la compañía dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)

        # Duplicar el feed actual
        duplicated_feed = duplicate_feed(current_feed.feed_id)

        # Crea una nueva instancia de la agencia con los datos proporcionados en la solicitud
        new_agency = Agency(
            # id=new_agency_id,
            feed_id=duplicated_feed,
            agency_id=request.POST["agency_id"],
            name=request.POST["agency_name"],
            url=request.POST["agency_url"],
            timezone=request.POST["agency_timezone"],
            lang=request.POST["agency_lang"],
            phone=request.POST["agency_phone"],
            fare_url=request.POST["agency_fare_url"],
            email=request.POST["agency_email"],
        )

        # Guarda la nueva agencia en la base de datos
        new_agency.save()

        duplicated_feed.last_action = f"Se agregó la agencia {new_agency.name}"
        duplicated_feed.save()

        # Redirige a la página "edited" después de la creación exitosa
        return redirect(reverse("company_agency", args=[company_id]))
    else:
        # Si la solicitud no es de tipo POST, renderiza la página "agency.html"
        return render(request, "create/agency.html")

def create_route(request, company_id):
    # Verifica si la solicitud es de tipo POST
    if request.method == "POST":

        # Obtener el feed actual para la compañía dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)
        
        # Duplicar el feed actual
        duplicated_feed = duplicate_feed(current_feed.feed_id)

        # Obtiene la agencia a la que pertenece la ruta, si no se proporciona, será nulo
        agency_id = request.POST.get("route_agency")
        new_agency = None
        if agency_id:
            agency = Agency.objects.get(id=agency_id)
            new_agency = Agency.objects.filter(agency_id=agency.agency_id).order_by('-id').first()

        # Crea una nueva instancia de la ruta con los datos proporcionados en la solicitud
        new_route = Route(
            # id=new_route_id,
            feed_id=duplicated_feed,
            agency=new_agency,
            route_id=request.POST["route_id"],
            short_name=request.POST["route_short_name"],
            long_name=request.POST["route_long_name"],
            desc=request.POST["route_desc"],
            route_type=request.POST["route_type"],
            url=request.POST["route_url"],
            color=request.POST["route_color"][1:7],
            text_color=request.POST["route_text_color"][1:7],
        )

        # Guarda la nueva ruta en la base de datos
        new_route.save()

        duplicated_feed.last_action = f"Se agregó la ruta {new_route.short_name}"
        duplicated_feed.save()

        # Redirige a la página "edited" después de la creación exitosa
        return redirect(reverse("company_route", args=[company_id]))
    else:
        # Si la solicitud no es de tipo POST, obtiene datos adicionales y renderiza la página "routes.html"
        duplicated_feed = Feed.objects.get(company_id=company_id, is_current=True)
        agencies = Agency.objects.filter(feed_id=duplicated_feed.feed_id)
        route_type_choices = Route.ROUTE_TYPE_CHOICES
        # Se pasan la lista de agencias y route type choices debido a que se deben escoger en una parte del formulario
        context = {
            "agencies": agencies,
            "route_type_choices": route_type_choices,
        }
        return render(request, "create/routes.html", context)

def create_stop(request, company_id):
    # Verifica si la solicitud es de tipo POST
    if request.method == 'POST':

        # Obtener el feed actual para la compañía dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)
        
        # Duplicar el feed actual
        duplicated_feed = duplicate_feed(current_feed.feed_id)

        # Obtiene los datos de la parada desde la solicitud
        stop_id = request.POST.get('stop_id')
        stop_name = request.POST.get('stop_name')
        stop_desc = request.POST.get('stop_desc')
        stop_lat = float(request.POST.get('stop_lat'))
        stop_lon = float(request.POST.get('stop_lon'))
        stop_zone_id = request.POST.get('stop_zone') 
        stop_url = request.POST.get('stop_url')
        stop_location_type = request.POST.get('stop_location_type')
        stop_parent_station = request.POST.get('stop_parent_station')
        stop_wheelchair_boarding = request.POST.get('stop_wheelchair_boarding')

        # Crea un objeto Point para la ubicación de la parada
        stop_loc = Point(stop_lon, stop_lat)

        zone = Zone.objects.get(id=stop_zone_id)
        new_zone = Zone.objects.filter(zone_id=zone.zone_id).order_by('-id').first()

        # Crea una nueva instancia de la parada con los datos proporcionados
        new_stop = Stop(
            # id=new_stop_id,
            feed_id=duplicated_feed,
            stop_id=stop_id,
            name=stop_name,
            desc=stop_desc,
            lat=stop_lat,
            lon=stop_lon,
            loc=stop_loc,
            zone=new_zone,
            url=stop_url,
            location_type=stop_location_type,
            parent_station=stop_parent_station,
            wheelchair_boarding=stop_wheelchair_boarding
        )

        # Guarda la nueva parada en la base de datos
        new_stop.save()

        duplicated_feed.last_action = f"Se agregó la parada {new_stop.name}"
        duplicated_feed.save()

        # Redirige a la página "edited" después de la creación exitosa
        return redirect(reverse("company_stop", args=[company_id]))
    else:
        duplicated_feed = Feed.objects.get(company_id=company_id, is_current=True)
        zones = Zone.objects.filter(feed_id=duplicated_feed.feed_id)
        # Se pasa por contexto zone porque se necesita para una parte del formulario
        context = {
            "zones": zones,
        }
        return render(request, "create/stop.html", context)
    
def create_zone(request, company_id):
    # Verifica si la solicitud es de tipo POST
    if request.method == "POST":

        # Obtener el feed actual para la compañía dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)
        
        # Duplicar el feed actual
        duplicated_feed = duplicate_feed(current_feed.feed_id)

        # Obtiene la opción seleccionada del formulario
        selected_zone_id = request.POST["zone_id"]

        # Si la opción no ha sido seleccionada anteriormente, crea y guarda la nueva zona
        new_zone = Zone(
            # id=new_zone_id,
            feed_id=duplicated_feed,   
            zone_id=selected_zone_id,
        )
        new_zone.save()

        duplicated_feed.last_action = f"Se agregó la zona {new_zone.zone_id}"
        duplicated_feed.save()

        # Redirige a la página "edited" después de la creación exitosa
        return redirect(reverse("company_zone", args=[company_id]))
    else:
        # Si la solicitud no es de tipo POST, obtiene datos adicionales y renderiza la página "zone.html"
        # Filtra las opciones disponibles excluyendo las que ya han sido utilizadas
        available_zones = [choice for choice in Zone._meta.get_field("zone_id").choices
                           if not Zone.objects.filter(zone_id=choice[0]).exists()]
        
        # Se pasa por contexto las opciones disponibles
        context = {
            'zone_id_choices': available_zones,
        }
        return render(request, "create/zone.html", context)

def create_calendar(request, company_id):
    # Verifica si la solicitud es de tipo POST
    if request.method == "POST":

        # Obtener el feed actual para la compañía dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)
        
        # Duplicar el feed actual
        duplicated_feed = duplicate_feed(current_feed.feed_id)

        # Crea una nueva instancia de Calendar con los datos proporcionados en la solicitud
        new_calendar = Calendar(
            # id=new_calendar_id,
            feed_id=duplicated_feed,
            service_id=request.POST.get("service_id"),
            monday=request.POST.get("monday"),
            tuesday=request.POST.get("tuesday"),
            wednesday=request.POST.get("wednesday"),
            thursday=request.POST.get("thursday"),
            friday=request.POST.get("friday"),
            saturday=request.POST.get("saturday"),
            sunday=request.POST.get("sunday"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date"),
        )

        # Guarda el nuevo calendario en la base de datos
        new_calendar.save()

        duplicated_feed.last_action = f"Se agregó el calendario {new_calendar.service_id}"
        duplicated_feed.save()

        # Redirige a la página "edited" después de la creación exitosa
        return redirect(reverse("company_calendar", args=[company_id]))
    else:
        # Si la solicitud no es de tipo POST, renderiza la página "calendar.html" con la información existente
        return render(request, "create/calendar.html")

def create_calendar_date(request, id, company_id):
    # Verifica si la solicitud es de tipo POST
    if request.method == "POST":

        # Obtener el feed actual para la compañía dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)
        
        # Duplicar el feed actual
        duplicated_feed = duplicate_feed(current_feed.feed_id)

        # Obtener la fecha ingresada en el formulario y convertirla a objeto datetime.date
        new_calendar_date_date_str = request.POST.get("date")
        new_calendar_date_date = datetime.strptime(new_calendar_date_date_str, '%Y-%m-%d').date()

        # Obtiene el calendario correspondiente a través de una llave foránea proporcionada en la solicitud
        calendar = Calendar.objects.get(id=id)
        new_calendar = Calendar.objects.filter(service_id=calendar.service_id).order_by('-id').first()

        # Verificar que la fecha esté dentro del rango permitido por el Calendar
        if not (calendar.start_date <= new_calendar_date_date <= calendar.end_date):
            return HttpResponseBadRequest("La fecha está fuera del rango permitido por el calendario.")

        # Crea una nueva instancia de CalendarDate con los datos proporcionados en la solicitud
        new_calendar_date = CalendarDate(
            service=new_calendar,
            # id=new_calendar_id,
            feed_id=duplicated_feed,
            date=new_calendar_date_date,
            exception_type=request.POST.get("exception_type"),
            holiday_name=request.POST.get("holiday_name"),
        )

        # Guarda la nueva fecha del calendario en la base de datos
        new_calendar_date.save()
        new_calendar = Calendar.objects.filter(service_id=calendar.service_id).order_by('-id').first()

        duplicated_feed.last_action = f"Se agregó la fecha de calendario {new_calendar_date.holiday_name}"
        duplicated_feed.save()

        # Redirige a la página "edited" después de la creación exitosa
        return redirect(reverse("company_calendar_date", args=[new_calendar.id, company_id]))
    else:
        # Obtén el calendario correspondiente para mostrar en el contexto
        calendar = Calendar.objects.get(id=id)
        context = {
            'calendar': calendar,
        }   
        return render(request, "create/calendar_date.html", context)

def create_fare_attribute(request, company_id):
    # Verifica si la solicitud es de tipo POST
    if request.method == "POST":
        
        # Obtener el feed actual para la compañía dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)
        
        # Duplicar el feed actual
        duplicated_feed = duplicate_feed(current_feed.feed_id)

        # Obtiene la agencia a la que pertenece la ruta, si no se proporciona, será nulo
        agency_id = request.POST.get("agency_id")
        new_agency = None
        if agency_id:
            agency = Agency.objects.get(id=agency_id)
            new_agency = Agency.objects.filter(agency_id=agency.agency_id).order_by('-id').first()

        # Crea una nueva instancia de la tarifa con los datos proporcionados en la solicitud
        new_fare = FareAttribute(
            # id=new_fare_id,
            feed_id = duplicated_feed,
            fare_id=request.POST["fare_id"],
            price=request.POST["price"],
            currency_type=request.POST["currency_type"],
            payment_method=request.POST["payment_method"],
            transfers=request.POST.get("transfers"),
            agency=new_agency,
            transfer_duration=request.POST.get("transfer_duration"),
        )

        # Guarda la nueva tarifa en la base de datos
        new_fare.save()

        duplicated_feed.last_action = f"Se agregó la tarifa {new_fare.fare_id}"
        duplicated_feed.save()

        # Redirige a la página "edited" después de la creación exitosa
        return redirect(reverse("company_fare_attribute", args=[company_id]))
    else:
        # Si la solicitud no es de tipo POST, obtiene las agencias disponibles y renderiza la página "fare_attribute.html"
        duplicated_feed = Feed.objects.get(company_id=company_id, is_current=True)
        agencies = Agency.objects.filter(feed_id=duplicated_feed.feed_id)
        context = {'agencies': agencies}
        return render(request, "create/fare_attribute.html", context)  

def create_fare_rule(request, company_id):
    # Verifica si la solicitud es de tipo POST
    if request.method == "POST":

        # Obtener el feed actual para la compañía dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)
        
        # Duplicar el feed actual
        duplicated_feed = duplicate_feed(current_feed.feed_id)

        # Obtiene las instancias de FareAttribute, Route y Zone correspondientes
        fare_id = request.POST.get("fare")
        fare = FareAttribute.objects.get(id=fare_id)
        new_fare = FareAttribute.objects.filter(fare_id=fare.fare_id).order_by('-id').first()

        route_id = request.POST.get("route")
        route = Route.objects.get(id=route_id)
        new_route = Route.objects.filter(route_id=route.route_id).order_by('-id').first()

        origin_id = request.POST.get("origin")
        origin = Zone.objects.get(id=origin_id)
        new_origin = Zone.objects.filter(zone_id=origin.zone_id).order_by('-id').first()

        destination_id = request.POST.get("destination")
        destination = Zone.objects.get(id=destination_id)
        new_destination = Zone.objects.filter(zone_id=destination.zone_id).order_by('-id').first()

        # Crea una nueva instancia de FareRule con los datos proporcionados en la solicitud
        new_fare_rule = FareRule(
            feed_id = duplicated_feed,
            fare=new_fare,
            route=new_route,
            origin=new_origin,
            destination=new_destination,
        )

        # Guarda la nueva regla de tarifa en la base de datos
        new_fare_rule.save()

        duplicated_feed.last_action = f"Se agregó una regla de tarifa"
        duplicated_feed.save()

        # Redirige a la página "edited" después de la creación exitosa
        return redirect(reverse("company_fare_rule", args=[company_id])) 
    else:
        # Si la solicitud no es de tipo POST, obtiene las instancias existentes necesarias y renderiza la página correspondiente
        duplicated_feed = Feed.objects.get(company_id=company_id, is_current=True)
        fares = FareAttribute.objects.filter(feed_id=duplicated_feed.feed_id)
        routes = Route.objects.filter(feed_id=duplicated_feed.feed_id)
        zones = Zone.objects.filter(feed_id__company_id=company_id, feed_id__is_current=True)

        # Se pasa por contexto las instancias necesarias
        context = {
            "fares": fares,
            "routes": routes,
            "zones": zones,
        }

        return render(request, "create/fare_rule.html", context)

def create_company(request):
    if request.method == "POST":

        # Crea una nueva instancia de la compañía con los datos proporcionados en la solicitud
        new_company = Company(
            name=request.POST["company_name"],
            address=request.POST["company_address"],
            phone=request.POST["company_phone"],
            email=request.POST["company_email"],
            website=request.POST["company_website"],
            logo=request.FILES["company_logo"],
        )

        # Guarda la nueva compañía en la base de datos
        new_company.save()

        # Crea un nuevo feed enlazado a la compañía y con un feed_id relacionado a la fecha de creación
        new_feed_id = f"GTFS_{timezone.now().strftime('%Y%m%d%H%M%S')}"
        new_feed = Feed(
            feed_id=new_feed_id,
            company_id=new_company,
            zip_file=request.FILES["gtfs_file"],
            last_action = "Se creó el feed"
        )

        # Guarda el nuevo feed en la base de datos
        new_feed.save()

        # Crea un nuevo FeedInfo
        new_feed_info = FeedInfo(
            feed_id=new_feed,
            start_date=new_feed.created_at.date(),
            end_date=None,  # Replace with your default value
            publisher_name="Default Publisher",  # Replace with your default value
            publisher_url="http://default-publisher-url.com",  # Replace with your default value
            lang="en",  # Replace with your default value
            version="1",  # Replace with your default value
            contact_email="default@example.com"  # Replace with your default value
        )

        # Guarda el nuevo FeedInfo en la base de datos
        new_feed_info.save()

        # Recupera la lista de instancias de Company
        companies = Company.objects.all()

        # Renderiza el template de lista de Company con la lista obtenida
        return render(request, "list/list_companies.html", {"companies": companies})
    else:
        # Si la solicitud no es de tipo POST, renderiza la página "company.html"
        return render(request, "create/company.html")

def create_feed(request):
    # Verifica si la solicitud es de tipo POST
    if request.method == "POST":

        # Obtiene la fecha y hora actual
        current_datetime = datetime.now()

        # Crea una cadena de feed_id utilizando el formato: "YYYYMMDDHHMMSS"
        feed_id = current_datetime.strftime("%Y%m%d%H%M%S")

        # Crea una nueva instancia del feed con los datos proporcionados en la solicitud
        new_feed = Feed(
            feed_id=feed_id,
            company_id=request.POST["company_id"], 
            zip_file=request.FILES["zip_file"], 
            is_current=request.POST.get("is_current", False),
            in_edition=request.POST.get("in_edition", False),
        )

        # Guarda el nuevo feed en la base de datos
        new_feed.save()

        # Redirige a la página "edition" después de la creación exitosa
        return redirect("edition")
    else:
        # Si la solicitud no es de tipo POST, renderiza la página "feed.html" (o el nombre que uses)
        return render(request, "create/feed.html")



# MÉTODOS PARA LISTAR
def list_company(request):
    # Recupera la lista de instancias de Company
    companies = Company.objects.all()

    # Renderiza el template de lista de Company con la lista obtenida
    return render(request, "list/list_companies.html", {"companies": companies})

def list_feed(request, company_id):
    # Recupera la compañía específica
    company = Company.objects.get(company_id=company_id)

    # Recupera la lista de feeds relacionados a la compañía
    feeds = Feed.objects.filter(company_id=company).order_by('created_at')

    # Renderiza el template de lista de feeds relacionados a una compañía
    return render(request, "list/list_feed.html", {"company": company, "feeds": feeds})

def list_companies(request):
    # Recupera la lista de instancias de Company
    companies = Company.objects.all()

    # Renderiza el template de lista de Company con la lista obtenida
    return render(request, "list/list_companies.html", {"companies": companies})




#MÉTODOS PARA ELIMINAR
def delete_agency(request, id):

    # Obtiene la agencia con el ID proporcionado
    original_agency = Agency.objects.get(id=id)

    # Obtiene el company_id asociado a la agencia
    company_id = original_agency.feed_id.company_id.company_id

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    duplicated_feed = duplicate_feed(current_feed.feed_id)

    agency = Agency.objects.filter(agency_id=original_agency.agency_id).order_by('-id').first()

    name = agency.name

    # Elimina la agencia de la base de datos
    agency.delete()

    duplicated_feed.last_action = f"Se eliminó la agencia: {name}"
    duplicated_feed.save()

    # Redirige a la lista de agencias después de eliminar
    return redirect(reverse("company_agency", args=[company_id]))

def delete_stop(request, id, company_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    duplicated_feed = duplicate_feed(current_feed.feed_id)

    # Obtiene la parada con el ID proporcionado
    original_stop = Stop.objects.get(id=id)

    stop = Stop.objects.filter(stop_id=original_stop.stop_id).order_by('-id').first()

    name = stop.name

    # Elimina la parada de la base de datos
    stop.delete()

    duplicated_feed.last_action = f"Se eliminó la parada: {name}"
    duplicated_feed.save()

    # Redirige a la lista de paradas después de eliminar
    return redirect(reverse("company_stop", args=[company_id]))
 
def delete_route(request, id, company_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    duplicated_feed = duplicate_feed(current_feed.feed_id)

    # Obtiene la ruta con el ID proporcionado
    original_route = Route.objects.get(id=id)

    route = Route.objects.filter(route_id=original_route.route_id).order_by('-id').first()

    name = route.short_name

    # Elimina la ruta de la base de datos
    route.delete()

    duplicated_feed.last_action = f"Se eliminó la ruta: {name}"
    duplicated_feed.save()

    # Redirige a la lista de rutas después de eliminar
    return redirect(reverse("company_route", args=[company_id]))

def delete_zone(request, id, company_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    duplicated_feed = duplicate_feed(current_feed.feed_id)

    # Obtiene la zona con el ID proporcionado
    original_zone = Zone.objects.get(id=id)

    zone = Zone.objects.filter(zone_id=original_zone.zone_id).order_by('-id').first()

    name = zone.zone_id

    # Elimina la zona de la base de datos
    zone.delete()

    duplicated_feed.last_action = f"Se eliminó la zona: {name}"
    duplicated_feed.save()

    # Redirige a la lista de zonas después de eliminar
    return redirect(reverse("company_zone", args=[company_id]))

def delete_calendar(request, id, company_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    duplicated_feed = duplicate_feed(current_feed.feed_id)

    # Obtiene el calendario con el ID proporcionado
    original_calendar = Calendar.objects.get(id=id)

    calendar = Calendar.objects.filter(service_id=original_calendar.service_id).order_by('-id').first()

    name = calendar.service_id

    # Elimina el calendario de la base de datos
    calendar.delete()

    duplicated_feed.last_action = f"Se eliminó el calendario: {name}"
    duplicated_feed.save()

    # Redirige a la lista de calendarios después de eliminar
    return redirect(reverse("company_calendar", args=[company_id]))

def delete_calendar_dates(request, id, company_id, calendar_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    duplicated_feed = duplicate_feed(current_feed.feed_id)

    # Obtiene la fecha de calendario con el ID del servicio proporcionado
    original_calendar_date = CalendarDate.objects.get(id=id)

    calendar_date = CalendarDate.objects.filter(holiday_name=original_calendar_date.holiday_name).order_by('-id').first()

    name = calendar_date.holiday_name

    duplicated_feed.last_action = f"Se eliminó la fecha de calendario: {name}"
    duplicated_feed.save()

    # Elimina la fecha de calendario de la base de datos
    calendar_date.delete()

    calendar = Calendar.objects.get(id=calendar_id)
    new_calendar = Calendar.objects.filter(service_id=calendar.service_id).order_by('-id').first()

    # Redirige a la lista de fechas de calendario después de eliminar
    return redirect(reverse("company_calendar_date", args=[new_calendar.id, company_id]))

def delete_fare_attribute(request, id ,company_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    duplicated_feed = duplicate_feed(current_feed.feed_id)

    # Obtiene la tarifa con el ID proporcionado
    original_fare_attribute = FareAttribute.objects.get(id=id)

    fare_attribute = FareAttribute.objects.filter(fare_id=original_fare_attribute.fare_id).order_by('-id').first()

    name = fare_attribute.fare_id

    # Elimina la tarifa de la base de datos
    fare_attribute.delete()

    duplicated_feed.last_action = f"Se eliminó la tarifa: {name}"
    duplicated_feed.save()

    # Redirige a la lista de tarifas después de eliminar
    return redirect(reverse("company_fare_attribute", args=[company_id]))

def delete_fare_rule(request, id, company_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    duplicated_feed = duplicate_feed(current_feed.feed_id)

    # Obtiene la instancia de FareRule con el ID proporcionado o devuelve un error 404 si no existe
    original_fare_rule = FareRule.objects.get(id=id)

    fare_rule = FareRule.objects.filter(
        origin__zone_id=original_fare_rule.origin.zone_id,
        destination__zone_id=original_fare_rule.destination.zone_id
    ).order_by('-id').first()

    duplicated_feed.last_action = f"Se eliminó una regla de tarifa"
    duplicated_feed.save()

    # Elimina la instancia de FareRule de la base de datos
    fare_rule.delete()

    # Redirige a la lista de FareRule después de eliminar
    return redirect(reverse("company_fare_rule", args=[company_id]))

def delete_company(request, company_id):
    # Obtiene la instancia de Company con el ID proporcionado 
    company = Company.objects.get(company_id=company_id)

    # Elimina la instancia de Company de la base de datos
    company.delete()

    # Redirige a la lista de Company después de eliminar
    return redirect("list_company")

def delete_feed(request, id, company_id):
    # Recupera la compañía específica
    company = Company.objects.get(company_id=company_id)

    # Recupera el feed específico
    feed = Feed.objects.get(feed_id=id)

    # Verifica cuántos feeds quedan para esta compañía
    remaining_feeds_count = Feed.objects.filter(company_id=company_id).count()

    # Si solo queda un feed, no permitir eliminarlo y mostrar un mensaje
    if remaining_feeds_count == 1:
        messages.error(request, 'No se puede eliminar el último feed.')
    else:
        # Elimina la instancia de Feed de la base de datos
        feed.delete()
        messages.success(request, 'Feed eliminado correctamente.')

    # Recupera la lista de feeds relacionados a la compañía
    feeds = Feed.objects.filter(company_id=company_id)

    # Renderiza el template de lista de feeds relacionados a una compañía
    return render(request, "list/list_feed.html", {"company": company, "feeds": feeds})



# MÉTODOS PARA EDITAR
def edit_agency(request, id, company_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    # Obtiene la agencia con el ID proporcionado
    original_agency = Agency.objects.get(id=id)

    if request.method == "GET":
        duplicated_feed = duplicate_feed(current_feed.feed_id)
        duplicated_feed.last_action = f"Se editó la agencia {original_agency.name}"
        duplicated_feed.save()

    agency = Agency.objects.filter(agency_id=original_agency.agency_id).order_by('-id').first()

    if request.method == "POST":
        # Actualiza la información de la agencia con los datos proporcionados en el formulario
        agency.agency_id = request.POST["agency_id"]
        agency.name = request.POST["agency_name"]
        agency.url = request.POST["agency_url"]
        agency.timezone = request.POST["agency_timezone"]
        agency.lang = request.POST["agency_lang"]
        agency.phone = request.POST["agency_phone"]
        agency.fare_url = request.POST["agency_fare_url"]
        agency.email = request.POST["agency_email"]
        agency.save()



        # Redirige a la lista de agencias después de editar
        return redirect(reverse("company_agency", args=[company_id]))
    else:
        # Muestra el formulario de edición con la información actual de la agencia
        context = {"agency": agency}
        return render(request, "edit/edit_agency.html", context)

def edit_stop(request, id, company_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    # Obtiene la parada con el ID proporcionado
    original_stop = Stop.objects.get(id=id)

    if request.method == "GET":
        duplicated_feed = duplicate_feed(current_feed.feed_id)
        duplicated_feed.last_action = f"Se editó la parada {original_stop.name}"
        duplicated_feed.save()

    stop = Stop.objects.filter(stop_id=original_stop.stop_id).order_by('-id').first()

    if request.method == "POST":
        # Actualiza la información de la parada con los datos proporcionados en el formulario
        stop.name = request.POST["stop_name"]
        stop.desc = request.POST["stop_desc"]
        stop.lat = float(request.POST["stop_lat"].replace(',', '.'))
        stop.lon = float(request.POST["stop_lon"].replace(',', '.'))

        # Verifica si se seleccionó una zona
        zone_id = request.POST.get("stop_zone")
        if zone_id:
            stop.zone = Zone.objects.get(id=zone_id)
        else:
            stop.zone = None

        stop.url = request.POST["stop_url"]
        stop.location_type = request.POST["stop_location_type"]
        stop.parent_station = request.POST["stop_parent_station"]
        stop.wheelchair_boarding = request.POST["stop_wheelchair_boarding"]

        # En caso de tener la latitud y la longitud se van a utilizar para crear la localización que es de tipo Point
        if "stop_lat" in request.POST and "stop_lon" in request.POST:
            stop.loc = Point(float(request.POST["stop_lon"].replace(',', '.')), float(request.POST["stop_lat"].replace(',', '.')))

        stop.save()

        # Redirige a la lista de paradas después de editar
        return redirect(reverse("company_stop", args=[company_id]))
    else:
        # Muestra el formulario de edición con la información actual de la parada y las zonas disponibles
        duplicated_feed = Feed.objects.get(company_id=company_id, is_current=True)
        zones = Zone.objects.filter(feed_id=duplicated_feed.feed_id)
        context = {"stop": stop, "zones": zones}
        return render(request, "edit/edit_stop.html", context)

def edit_route(request, id, company_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    original_route = Route.objects.get(id=id)

    if request.method == "GET":
        duplicated_feed = duplicate_feed(current_feed.feed_id)
        duplicated_feed.last_action = f"Se editó la ruta {original_route.short_name}"
        duplicated_feed.save()

    # Obtiene la ruta con el ID proporcionado
    route = Route.objects.filter(route_id=original_route.route_id).order_by('-id').first()
    agencies = Agency.objects.all()
    route_type_choices = Route.ROUTE_TYPE_CHOICES 

    if request.method == "POST":
        # Actualiza la información de la ruta con los datos proporcionados en el formulario
        route.route_id = request.POST["route_id"]
        route.short_name = request.POST["route_short_name"]
        route.long_name = request.POST["route_long_name"]
        route.desc = request.POST["route_desc"]
        route.route_type = request.POST["route_type"]
        route.url = request.POST["route_url"]
        route.color = request.POST["route_color"][1:7]
        route.text_color = request.POST["route_text_color"][1:7]

        agency_id = request.POST["route_agency"]
        agency = Agency.objects.get(id=agency_id)
        route.agency = agency

        route.save()

        # Redirige a la lista de rutas después de editar
        return redirect(reverse("company_route", args=[company_id]))
    else:
        duplicated_feed = Feed.objects.get(company_id=company_id, is_current=True)
        agencies = Agency.objects.filter(feed_id=duplicated_feed.feed_id)
        # Muestra el formulario de edición con la información actual de la ruta y las agencias disponibles
        context = {"route": route, "agencies": agencies, "route_type_choices": route_type_choices}
        return render(request, "edit/edit_route.html", context)
  
def edit_zone(request, id, company_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    # Obtiene la zona con el ID proporcionado
    original_zone = Zone.objects.get(id=id)

    if request.method == "GET":
        duplicated_feed = duplicate_feed(current_feed.feed_id)
        duplicated_feed.last_action = f"Se editó la zona {original_zone.zone_id}"
        duplicated_feed.save()

    zone = Zone.objects.filter(zone_id=original_zone.zone_id).order_by('-id').first()

    if request.method == "POST":
        # Obtiene el nuevo ID de zona proporcionado en el formulario
        new_zone_id = request.POST.get("new_zone_id")  

        # Verifica si el nuevo ID es diferente al actual y si no ha sido utilizado
        if new_zone_id != zone.zone_id and new_zone_id not in Zone.objects.values_list('zone_id', flat=True):
            # Actualiza la zona existente con el nuevo ID

            # Asigna el nuevo ID a la zona
            zone.zone_id = new_zone_id
            zone.save()

            # Redirige a la lista de zonas después de editar
            return redirect(reverse("company_zone", args=[company_id]))
        else:
            # Aquí puedes manejar la lógica si el nuevo ID ya ha sido utilizado
            # Por ejemplo, podrías mostrar un mensaje de error o redirigir a otra página
            pass
    else:
        # Obtiene las opciones de ID de zona disponibles en el modelo
        zone_id_choices = Zone._meta.get_field("zone_id").choices

        # Excluye las zonas que ya han sido utilizadas
        unused_zone_id_choices = [choice for choice in zone_id_choices if choice[0] not in Zone.objects.values_list('zone_id', flat=True)]

        # Muestra el formulario de edición con la información actual de la zona y las opciones de ID disponibles
        context = {
            "zone": zone,
            'zone_id_choices': unused_zone_id_choices,
        }
        return render(request, "edit/edit_zone.html", context)

def edit_calendar(request, id, company_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    # Obtiene el calendario con el ID proporcionado
    original_calendar = Calendar.objects.get(id=id)

    if request.method == "GET":
        duplicated_feed = duplicate_feed(current_feed.feed_id)
        duplicated_feed.last_action = f"Se editó el calendario {original_calendar.service_id}"
        duplicated_feed.save()

    calendar = Calendar.objects.filter(service_id=original_calendar.service_id).order_by('-id').first()

    # Obtiene la lista de CalendarDate asociados al calendario
    calendar_dates = CalendarDate.objects.filter(service=calendar)

    if request.method == "POST":
        # Actualiza la información del calendario con los datos proporcionados en el formulario
        calendar.service_id = request.POST["service_id"]
        calendar.monday = request.POST["monday"]
        calendar.tuesday = request.POST["tuesday"]
        calendar.wednesday = request.POST["wednesday"]
        calendar.thursday = request.POST["thursday"]
        calendar.friday = request.POST["friday"]
        calendar.saturday = request.POST["saturday"]
        calendar.sunday = request.POST["sunday"]
        
        # Obtiene las fechas del formulario
        new_start_date = request.POST.get("new_start_date")
        new_end_date = request.POST.get("new_end_date")
        
        # Si se proporcionan nuevas fechas, se actualizan; de lo contrario, se conservan las antiguas
        if new_start_date:
            calendar.start_date = new_start_date
        if new_end_date:
            calendar.end_date = new_end_date
        
        calendar.save()

        # Redirige a la lista de calendarios después de editar
        return redirect(reverse("company_calendar", args=[company_id]))
    else:
        # Muestra el formulario de edición con la información actual del calendario
        context = {"calendar": calendar, "calendar_dates": calendar_dates}
        return render(request, "edit/edit_calendar.html", context)

def edit_calendar_dates(request, id, company_id, calendar_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    # Obtiene la fecha del calendario con el ID proporcionado
    original_calendar_dates = CalendarDate.objects.get(id=id)

    if request.method == "GET":
        duplicated_feed = duplicate_feed(current_feed.feed_id)
        duplicated_feed.last_action = f"Se editó la fecha de calendario {original_calendar_dates.holiday_name}"
        duplicated_feed.save()

    calendar_dates = CalendarDate.objects.filter(holiday_name=original_calendar_dates.holiday_name).order_by('-id').first()

    if request.method == "POST":
        # Actualiza la información de la fecha del calendario con los datos proporcionados en el formulario
        calendar_dates.date = request.POST["date"]
        calendar_dates.exception_type = request.POST["exception_type"]
        calendar_dates.holiday_name = request.POST["holiday_name"]
        calendar_dates.save()

        calendar = Calendar.objects.get(id=calendar_id)
        new_calendar = Calendar.objects.filter(service_id=calendar.service_id).order_by('-id').first()
    
        # Redirige a la lista de fechas de calendario después de editar
        return redirect(reverse("company_calendar_date", args=[new_calendar.id, company_id]))
    else:
        # Muestra el formulario de edición con la información actual de la fecha del calendario
        context = {
            "calendar_dates": calendar_dates,
        }
        return render(request, "edit/edit_calendar_dates.html", context)

def edit_fare_attribute(request, id, company_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    # Obtiene la clase de tarifa con el ID proporcionado
    original_fare_attribute = FareAttribute.objects.get(id=id)

    if request.method == "GET":
        duplicated_feed = duplicate_feed(current_feed.feed_id)
        duplicated_feed.last_action = f"Se editó la tarifa {original_fare_attribute.fare_id}"
        duplicated_feed.save()

    fare_attribute = FareAttribute.objects.filter(fare_id=original_fare_attribute.fare_id).order_by('-id').first()

    agencies = Agency.objects.all()

    if request.method == "POST":
        # Actualiza la información de la clase de tarifa con los datos proporcionados en el formulario
        fare_attribute.fare_id = request.POST["fare_id"]
        fare_attribute.price = request.POST["fare_price"]
        fare_attribute.currency_type = request.POST["fare_currency_type"]
        fare_attribute.payment_method = request.POST["fare_payment_method"]
        fare_attribute.transfers = request.POST["fare_transfers"]
        fare_attribute.transfer_duration = request.POST["fare_transfer_duration"]

        agency_id = request.POST["fare_agency"]
        agency = Agency.objects.get(id=agency_id)
        fare_attribute.agency = agency

        fare_attribute.save()

        # Redirige a la lista de clases de tarifas después de editar
        return redirect(reverse("company_fare_attribute", args=[company_id]))
    else:
        duplicated_feed = Feed.objects.get(company_id=company_id, is_current=True)
        agencies = Agency.objects.filter(feed_id=duplicated_feed.feed_id)
        # Muestra el formulario de edición con la información actual de la clase de tarifa y las agencias disponibles
        context = {"fare_attribute": fare_attribute, "agencies": agencies}
        return render(request, "edit/edit_fare_attribute.html", context)

def edit_feed_info(request, id, company_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    if request.method == "GET":
        duplicated_feed = duplicate_feed(current_feed.feed_id)
        duplicated_feed.last_action = f"Se editó feed info"
        duplicated_feed.save()

    # Obtiene la instancia de FeedInfo con el ID proporcionado 
    original_feed_info = FeedInfo.objects.get(id=id)
    feed_info = FeedInfo.objects.filter(start_date=original_feed_info.start_date).order_by('-id').first()

    if request.method == "POST":
        # Actualiza la información de FeedInfo con los datos proporcionados en el formulario
        feed_info.publisher_name = request.POST["publisher_name"]
        feed_info.publisher_url = request.POST["publisher_url"]
        feed_info.lang = request.POST["lang"]
        feed_info.start_date = request.POST["start_date"]
        feed_info.end_date = request.POST["end_date"]
        feed_info.version = request.POST["version"]
        feed_info.contact_email = request.POST["contact_email"]
        feed_info.save()

        # Redirige a la lista de FeedInfo después de editar
        return redirect(reverse("company_feed_info", args=[company_id]))
    else:
        # Muestra el formulario de edición con la información actual de FeedInfo
        context = {"feed_info": feed_info}
        return render(request, "edit/edit_feed_info.html", context)

def edit_fare_rule(request, id, company_id):

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    # Obtiene la regla de tarifa con el ID proporcionado
    original_fare_rule = FareRule.objects.get(id=id)

    if request.method == "GET":
        duplicated_feed = duplicate_feed(current_feed.feed_id)
        duplicated_feed.last_action = f"Se editó una regla de tarifa"
        duplicated_feed.save()

    fare_rule = FareRule.objects.filter(
        origin__zone_id=original_fare_rule.origin.zone_id,
        destination__zone_id=original_fare_rule.destination.zone_id
    ).order_by('-id').first()


    if request.method == "POST":
        # Actualiza la información de la regla de tarifa con los datos proporcionados en el formulario
        fare_rule.origin = Zone.objects.get(pk=request.POST["origin"])
        fare_rule.destination = Zone.objects.get(pk=request.POST["destination"])
        fare_rule.fare = FareAttribute.objects.get(pk=request.POST["fare"])
        fare_rule.route = Route.objects.get(pk=request.POST["route"])
        fare_rule.save()

        # Redirige a la lista de reglas de tarifas después de editar
        return redirect(reverse("company_fare_rule", args=[company_id]))
    else:
        # Muestra el formulario de edición con la información actual de la regla de tarifa
        duplicated_feed = Feed.objects.get(company_id=company_id, is_current=True)
        fares = FareAttribute.objects.filter(feed_id=duplicated_feed.feed_id)
        routes = Route.objects.filter(feed_id=duplicated_feed.feed_id)
        zones = Zone.objects.filter(feed_id__company_id=company_id, feed_id__is_current=True)
        context = {
            "fare_rule": fare_rule,
            "fares": fares,
            "routes": routes,
            "zones": zones,
        }
        return render(request, "edit/edit_fare_rule.html", context)

def edit_company(request, company_id):
    # Obtiene la compañía con el ID proporcionado
    company = Company.objects.get(company_id=company_id)

    # Obtener el feed actual para la compañía dada
    current_feed = Feed.objects.get(company_id=company_id, is_current=True)

    duplicated_feed = duplicate_feed(current_feed.feed_id)
    duplicated_feed.last_action = f"Se editó la compañía"
    duplicated_feed.save()

    if request.method == "POST":
        # Actualiza la información de la compañía con los datos proporcionados en el formulario
        company.name = request.POST.get("company_name")
        company.address = request.POST.get("company_address")
        company.phone = request.POST.get("company_phone")
        company.email = request.POST.get("company_email")
        company.website = request.POST.get("company_website")
        company.logo = request.POST.get("company_logo")
        company.save()

        # Redirige a la lista de compañías después de editar
        return redirect("list_company")
    else:
        # Muestra el formulario de edición con la información actual de la compañía
        context = {"company": company}
        return render(request, "edit/edit_company.html", context)

def edit_feed(request, feed_id, company_id):

    # Recupera la compañía específica
    company = Company.objects.get(company_id=company_id)

    # Recupera la lista de feeds relacionados a la compañía
    feeds = Feed.objects.filter(company_id=company)

    # Obtiene el feed con el ID proporcionado
    feed = Feed.objects.get(feed_id=feed_id)

    # Recupera la lista de instancias de Company
    companies = Company.objects.all()

    if request.method == "POST":
        # Actualiza la información del feed con los datos proporcionados en el formulario
        feed.zip_file = request.FILES["zip_file"]
        feed.is_current = request.POST.get("is_current", False)
        feed.in_edition = request.POST.get("in_edition", False)
        feed.save()

        # Renderiza el template de lista de feeds relacionados a una compañía
        return render(request, "list/list_feed.html", {"company": company, "feeds": feeds})
    else:
        # Muestra el formulario de edición con la información actual del feed
        context = {"feed": feed, "companies": companies}
        return render(request, "edit/edit_feed.html", context)



# MÉTODOS PARA MOSTRAR LA PÁGINA DE COMPAÑÍAS 
def company_agency(request, company_id):
    # Obtén la instancia de Company usando el company_id
    company = Company.objects.get(company_id=company_id)
    agencies = Agency.objects.filter(feed_id__company_id=company_id, feed_id__is_current=True)

    # Renderiza el template de detalle_company con la compañía obtenida
    return render(request, "company_screens/agency.html", {"company": company, 'agencies': agencies})

def company_route(request, company_id):
    # Obtén la instancia de Company usando el company_id
    company = Company.objects.get(company_id=company_id)
    routes = Route.objects.filter(feed_id__company_id=company_id, feed_id__is_current=True)

    # Renderiza el template de detalle_company con la compañía obtenida
    return render(request, "company_screens/route.html", {"company": company, 'routes': routes})

def company_stop(request, company_id):
    # Obtén la instancia de Company usando el company_id
    company = Company.objects.get(company_id=company_id)
    stops = Stop.objects.filter(feed_id__company_id=company_id, feed_id__is_current=True)

    # Renderiza el template de detalle_company con la compañía obtenida
    return render(request, "company_screens/stop.html", {"company": company, 'stops': stops})

def company_zone(request, company_id):
    # Obtén la instancia de Company usando el company_id
    company = Company.objects.get(company_id=company_id)
    zones = Zone.objects.filter(feed_id__company_id=company_id, feed_id__is_current=True)

    # Renderiza el template de detalle_company con la compañía obtenida
    return render(request, "company_screens/zone.html", {"company": company, 'zones': zones})

def company_calendar(request, company_id):
    # Obtén la instancia de Company usando el company_id
    company = Company.objects.get(company_id=company_id)
    calendars = Calendar.objects.filter(feed_id__company_id=company_id, feed_id__is_current=True)

    # Renderiza el template de detalle_company con la compañía obtenida
    return render(request, "company_screens/calendar.html", {"company": company, 'calendars': calendars})

def company_calendar_date(request, id, company_id):
    # Obtén la instancia de Calendar usando el calendar_id
    company = Company.objects.get(company_id=company_id)
    calendar = Calendar.objects.get(id=id)
    calendar_dates = CalendarDate.objects.filter(service=calendar)

    # Renderiza el template de detalle_company con el calendario obtenido y los calendar_dates relacionados
    return render(request, "company_screens/calendar_date.html", {"company": company, "calendar": calendar, 'calendar_dates': calendar_dates})

def company_fare_attribute(request, company_id):
    # Obtén la instancia de Company usando el company_id
    company = Company.objects.get(company_id=company_id)
    fare_attributes = FareAttribute.objects.filter(feed_id__company_id=company_id, feed_id__is_current=True)

    # Renderiza el template de detalle_company con la compañía obtenida
    return render(request, "company_screens/fare_attribute.html", {"company": company, 'fare_attributes': fare_attributes})

def company_fare_rule(request, company_id):
    # Obtén la instancia de Company usando el company_id
    company = Company.objects.get(company_id=company_id)
    fare_rules = FareRule.objects.filter(feed_id__company_id=company_id, feed_id__is_current=True)

    # Renderiza el template de detalle_company con la compañía obtenida
    return render(request, "company_screens/fare_rule.html", {"company": company, 'fare_rules': fare_rules})

def company_feed_info(request, company_id):
    # Obtén la instancia de Company usando el company_id
    company = Company.objects.get(company_id=company_id)

    # Obtén el feed actual de la compañía
    current_feed = Feed.objects.filter(company_id=company, is_current=True).first()

    # Verifica si existe un FeedInfo asociado a este Feed
    feed_info = FeedInfo.objects.filter(feed_id=current_feed).first()

    # Si no existe, crea uno nuevo con campos en null excepto la fecha
    if not feed_info:
        new_feed_info = FeedInfo(
            feed_id=current_feed,
            start_date=current_feed.created_at.date(),
            end_date=None,  # Replace with your default value
            publisher_name="Default Publisher",  # Replace with your default value
            publisher_url="http://default-publisher-url.com",  # Replace with your default value
            lang="en",  # Replace with your default value
            version="1",  # Replace with your default value
            contact_email="default@example.com"  # Replace with your default value
        )
        new_feed_info.save()
        feed_info = new_feed_info

    # Renderiza el template de detalle_company con la compañía y feed_info obtenidos
    return render(request, "company_screens/feed_info.html", {"company": company, 'feed_info': feed_info})



# MÉTODOS PARA ASIGNAR O ELIMINAR LAS RUTAS DE UNA AGENCIA 
# QUE VA A SER ELIMINADA
def view_agency_routes(request, id):
    # Obtén la agencia con el ID proporcionado
    agency = Agency.objects.get(id=id)

    if request.method == "POST":
        action = request.POST.get("action")

    # Obtén todas las agencias disponibles para asignar a las rutas
    all_agencies = Agency.objects.exclude(id=id)

    # Obtén todas las rutas asociadas a la agencia
    routes = Route.objects.filter(agency=agency)

    # Renderiza la página con la información necesaria
    context = {
        "agency": agency,
        "all_agencies": all_agencies,
        "routes": routes,  # Agrega las rutas al contexto
    }
    return render(request, "assign_before_delete/view_agency_routes.html", context)

def delete_all_routes(request, id):
        # Obtiene la agencia con el ID proporcionado
        agency = Agency.objects.get(id=id)

        # Obtiene todas las rutas asociadas a la agencia
        routes_to_delete = Route.objects.filter(agency=agency)

        # Elimina cada ruta de la base de datos
        for route in routes_to_delete:
            route.delete()
        
        # Redirige a la lista de rutas de la agencia correspondiente
        return redirect("view_agency_routes", id=id)

def update_all_routes_agency(request, id):
    # Obtiene la nueva agencia

    if request.method == 'POST':
            
        new_agency_id = request.POST["new_agency_id"]
        new_agency = Agency.objects.get(id=new_agency_id)

        # Actualiza la agencia de todas las rutas asociadas
        routes_to_update = Route.objects.filter(agency=id)
        routes_to_update.update(agency=new_agency)

        # Redirige a la página "view_agency_routes" después de la actualización
        return redirect("view_agency_routes", id=id)
    else:
        return redirect("view_agency_routes", id=id)
    
def update_route(request, id, route_id):
    if request.method == 'POST':
        new_agency_id = request.POST.get("new_agency_id")

        try:
            new_agency = Agency.objects.get(id=new_agency_id)
            route_to_update = Route.objects.get(id=route_id)

            # Actualiza la agencia de la ruta específica
            route_to_update.agency = new_agency
            route_to_update.save()

            # Redirige a la página "view_agency_routes" después de la actualización
            return redirect("view_agency_routes", id=id)
        except:
            # Redirige a la página "view_agency_routes" si ocurre algún error
            return redirect("view_agency_routes", id=id)

    else:
        # Redirige a la página "view_agency_routes" si la solicitud no es POST
        return redirect("view_agency_routes", id=id)

def delete_agency_route(request, id, route_id):
    # Obtiene la ruta con el ID proporcionado
    route = Route.objects.get(id=route_id)

    # Elimina la ruta de la base de datos
    route.delete()

    # Redirige a la lista de rutas después de eliminar
    return redirect("view_agency_routes", id=id)


# MÉTODOS PARA ASIGNAR O ELIMINAR LAS PARADAS DE UNA ZONA 
# QUE VA A SER ELIMINADA
def view_zone_stops(request, id):
    # Obtén la zona con el ID proporcionado
    zone = Zone.objects.get(id=id)

    if request.method == "POST":
        action = request.POST.get("action")

    # Obtén todas las zonas disponibles para asignar a las paradas
    zones = Zone.objects.exclude(id=id)

    # Obtén todas las paradas asociadas a la zona
    stops = Stop.objects.filter(zone=zone)

    # Renderiza la página con la información necesaria
    context = {
        "zone": zone,
        "zones": zones,
        "stops": stops,  
    }
    return render(request, "assign_before_delete/view_zone_stops.html", context)

def delete_all_stops(request, id):
        # Obtiene la zona con el ID proporcionado
        zone = Zone.objects.get(id=id)

        # Obtiene todas las paradas asociadas a la zona
        stops_to_delete = Stop.objects.filter(zone=zone)

        # Elimina cada ruta de la base de datos
        for stop in stops_to_delete:
            stop.delete()
        
        # Redirige a la lista de rutas de la agencia correspondiente
        return redirect("view_zone_stops", id=id)

def update_all_stops_zone(request, id):
    if request.method == 'POST':

        new_zone_id = request.POST["new_zone_id"]
        new_zone = Zone.objects.get(id=new_zone_id)

        # Actualiza la agencia de todas las rutas asociadas
        stops_to_update = Stop.objects.filter(zone=id)
        stops_to_update.update(zone=new_zone)

        # Redirige a la página "view_agency_routes" después de la actualización
        return redirect("view_zone_stops", id=id)
    else:
        return redirect("view_zone_stops", id=id)
  
def update_stop(request, id, stop_id):
    if request.method == 'POST':
        new_zone_id = request.POST.get("new_zone_id")

        try:
            new_zone = Zone.objects.get(id=new_zone_id)
            stop_to_update = Stop.objects.get(id=stop_id)

            # Actualiza la agencia de la ruta específica
            stop_to_update.zone = new_zone
            stop_to_update.save()

            # Redirige a la página "view_zone_stops" después de la actualización
            return redirect("view_zone_stops", id=id)
        except:
            # Redirige a la página "view_zone_stops" si ocurre algún error
            return redirect("view_zone_stops", id=id)

    else:
        # Redirige a la página "view_zone_stops" si la solicitud no es POST
        return redirect("view_zone_stops", id=id)

def delete_zone_stop(request, id, stop_id):
    # Obtiene la parada con el ID proporcionado
    stop = Stop.objects.get(id=stop_id)

    # Elimina la parada de la base de datos
    stop.delete()

    # Redirige a la lista de rutas después de eliminar
    return redirect("view_zone_stops", id=id)




def cargar_contenido(request):
    enlace = request.GET.get('enlace', '')

    # Lógica para obtener el contenido según el enlace
    # Aquí puedes realizar consultas a la base de datos u otras operaciones según tu necesidad

    # En este ejemplo, simplemente devolvemos un mensaje de prueba
    contenido = f'Contenido para el enlace: {enlace}'

    return JsonResponse({'contenido': contenido})

def select_feed(request, feed_id, company_id):
    # Obtener el feed seleccionado
    feed_seleccionado = Feed.objects.get(feed_id=feed_id)

    # Actualizar los feeds
    Feed.objects.filter(company_id=company_id).update(is_current=False)
    feed_seleccionado.is_current = True
    feed_seleccionado.save()

    # Recupera la compañía específica
    company = Company.objects.get(company_id=company_id)

    # Recupera la lista de feeds relacionados a la compañía
    feeds = Feed.objects.filter(company_id=company)

    return render(request, "list/list_feed.html", {"company": company, "feeds": feeds})



def edited(request):
    return render(request, "edited.html")
