import uuid
from django.shortcuts import render, redirect
from gtfs.models import Agency, Route, Stop, Zone, Calendar, CalendarDate
from gtfs.models import FareAttribute, FeedInfo, FareRule, Company, Feed
from django.contrib.gis.geos import Point
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse


# Create your views here.


def edition(request):
    return render(request, 'edition.html')

def companies(request):
    # Recupera la lista de instancias de Company
    companies = Company.objects.all()

    # Renderiza el template de lista de Company con la lista obtenida
    return render(request, "list/list_companies.html", {"companies": companies})


# MÉTODOS PARA CREAR 
def create_agency(request, company_id):
    # Verifica si la solicitud es de tipo POST
    if request.method == "POST":

        # Obtiene la última agencia existente
        last_agency = Agency.objects.order_by('-id').first()

        # Calcula el nuevo ID para la agencia en base al id de la última agencia 
        if last_agency:
            new_agency_id = int(last_agency.id) + 1
        else:
            new_agency_id = 1

        # Obtener el feed actual para la compañía dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)

        # Crea una nueva instancia de la agencia con los datos proporcionados en la solicitud
        new_agency = Agency(
            id=new_agency_id,
            feed_id=current_feed,
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

        # Redirige a la página "edited" después de la creación exitosa
        return redirect(reverse("company_agency", args=[company_id]))
    else:
        # Si la solicitud no es de tipo POST, renderiza la página "agency.html"
        return render(request, "create/agency.html")

def create_route(request, company_id):
    # Verifica si la solicitud es de tipo POST
    if request.method == "POST":
        # Obtiene la última ruta existente
        last_route = Route.objects.order_by('-id').first()

        # Calcula el nuevo ID para la ruta en base al id de la última ruta
        if last_route:
            new_route_id = int(last_route.id) + 1
        else:
            new_route_id = 1

        # Obtiene la agencia a la que pertenece la ruta
        agency = Agency.objects.get(agency_id=request.POST["route_agency"])

        # Obtener el feed actual para la ruta dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)

        # Crea una nueva instancia de la ruta con los datos proporcionados en la solicitud
        new_route = Route(
            id=new_route_id,
            feed_id=current_feed,
            agency=agency,
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

        # Redirige a la página "edited" después de la creación exitosa
        return redirect(reverse("company_route", args=[company_id]))
    else:
        # Si la solicitud no es de tipo POST, obtiene datos adicionales y renderiza la página "routes.html"
        agencies = Agency.objects.all()
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
        # Obtiene la última parada existente
        last_stop = Stop.objects.order_by('-id').first()

        # Calcula el nuevo ID para la parada en base a al id de la parada pasada
        if last_stop:
            new_stop_id = int(last_stop.id) + 1
        else:
            new_stop_id = 1

        # Obtener el feed actual para la ruta dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)

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

        # Crea una nueva instancia de la parada con los datos proporcionados
        new_stop = Stop(
            id=new_stop_id,
            feed_id=current_feed,
            stop_id=stop_id,
            name=stop_name,
            desc=stop_desc,
            lat=stop_lat,
            lon=stop_lon,
            loc=stop_loc,
            zone=Zone.objects.get(zone_id=stop_zone_id),
            url=stop_url,
            location_type=stop_location_type,
            parent_station=stop_parent_station,
            wheelchair_boarding=stop_wheelchair_boarding
        )

        # Guarda la nueva parada en la base de datos
        new_stop.save()

        # Redirige a la página "edited" después de la creación exitosa
        return redirect(reverse("company_stop", args=[company_id]))
    else:
        # Si la solicitud no es de tipo POST, obtiene datos adicionales y renderiza la página "stop.html"
        zones = Zone.objects.all()
        # Se pasa por contexto zone porque se necesita para una parte del formulario
        context = {
            "zones": zones,
        }
        return render(request, "create/stop.html", context)
    
def create_zone(request, company_id):
    # Verifica si la solicitud es de tipo POST
    if request.method == "POST":

        # Obtener el feed actual para la ruta dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)

        # Obtiene la opción seleccionada del formulario
        selected_zone_id = request.POST["zone_id"]

        # Si la opción no ha sido seleccionada anteriormente, crea y guarda la nueva zona
        new_zone = Zone(
            feed_id=current_feed,   
            zone_id=selected_zone_id,
        )
        new_zone.save()

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
        # Obtiene la última entrada de calendario
        last_calendar = Calendar.objects.order_by('-id').first()

        # Calcula el nuevo ID para el calendario en base a al id del último calendario
        if last_calendar:
            new_calendar_id = int(last_calendar.id) + 1
        else:
            new_calendar_id = 1

        # Obtener el feed actual para la ruta dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)

        # Crea una nueva instancia de Calendar con los datos proporcionados en la solicitud
        new_calendar = Calendar(
            id=new_calendar_id,
            feed_id=current_feed,
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

        # Redirige a la página "edited" después de la creación exitosa
        return redirect(reverse("company_calendar", args=[company_id]))
    else:
        # Si la solicitud no es de tipo POST, renderiza la página "calendar.html" con la información existente
        return render(request, "create/calendar.html")

def create_calendar_date(request, id, company_id):
    # Verifica si la solicitud es de tipo POST
    if request.method == "POST":
        # Obtiene el calendario correspondiente a través de una llave foránea proporcionada en la solicitud
        calendar = Calendar.objects.get(id=id)

        # Obtiene la última entrada de calendario
        last_calendar = CalendarDate.objects.order_by('-id').first()

        # Calcula el nuevo ID para el calendario en base a al id del último calendario
        if last_calendar:
            new_calendar_id = int(last_calendar.id) + 1
        else:
            new_calendar_id = 1

        # Obtener el feed actual para la ruta dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)

        # Crea una nueva instancia de CalendarDate con los datos proporcionados en la solicitud
        new_calendar_date = CalendarDate(
            service=calendar,
            id=new_calendar_id,
            feed_id=current_feed,
            date=request.POST.get("date"),
            exception_type=request.POST.get("exception_type"),
            holiday_name=request.POST.get("holiday_name"),
        )

        # Guarda la nueva fecha del calendario en la base de datos
        new_calendar_date.save()

        # Redirige a la página "edited" después de la creación exitosa
        return redirect(reverse("company_calendar_date", args=[calendar.id, company_id]))
    else:
        return render(request, "create/calendar_date.html")

def create_fare_attribute(request, company_id):
    # Verifica si la solicitud es de tipo POST
    if request.method == "POST":
        
        # Obtiene la última tarifa existente
        last_fare = FareAttribute.objects.order_by('-id').first()

        # Calcula el nuevo ID para la tarifa en base al id de la última tarifa 
        if last_fare:
            new_fare_id = int(last_fare.id) + 1
        else:
            new_fare_id = 1

        # Obtiene la agencia asociada a la tarifa
        agency_id = request.POST["agency_id"]
        agency = Agency.objects.get(agency_id=agency_id)

        # Obtener el feed actual para la ruta dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)

        # Crea una nueva instancia de la tarifa con los datos proporcionados en la solicitud
        new_fare = FareAttribute(
            id=new_fare_id,
            feed_id = current_feed,
            fare_id=request.POST["fare_id"],
            price=request.POST["price"],
            currency_type=request.POST["currency_type"],
            payment_method=request.POST["payment_method"],
            transfers=request.POST.get("transfers"),
            agency=agency,
            transfer_duration=request.POST.get("transfer_duration"),
        )

        # Guarda la nueva tarifa en la base de datos
        new_fare.save()

        # Redirige a la página "edited" después de la creación exitosa
        return redirect(reverse("company_fare_attribute", args=[company_id]))
    else:
        # Si la solicitud no es de tipo POST, obtiene las agencias disponibles y renderiza la página "fare_attribute.html"
        agencies = Agency.objects.all()
        context = {'agencies': agencies}
        return render(request, "create/fare_attribute.html", context)

def create_feed_info(request):
    # Verifica si la solicitud es de tipo POST
    if request.method == "POST":
        # Obtiene la última instancia de FeedInfo existente
        last_feed_info = FeedInfo.objects.order_by('-id').first()

        # Calcula el nuevo ID para FeedInfo en base al id de la última instancia
        if last_feed_info:
            new_feed_info_id = last_feed_info.id + 1
        else:
            new_feed_info_id = 1

        # Crea una nueva instancia de FeedInfo con los datos proporcionados en la solicitud
        new_feed_info = FeedInfo(
            id=new_feed_info_id,
            publisher_name=request.POST["publisher_name"],
            publisher_url=request.POST["publisher_url"],
            lang=request.POST["lang"],
            start_date=request.POST["start_date"],
            end_date=request.POST["end_date"],
            version=request.POST["version"],
            contact_email=request.POST["contact_email"],
        )

        # Guarda la nueva instancia de FeedInfo en la base de datos
        new_feed_info.save()

        # Redirige a la página "edition" después de la creación exitosa
        return redirect("edition")
    else:
        # Si la solicitud no es de tipo POST, renderiza la página de creación con el formulario
        return render(request, "create/feed_info.html")   

def create_fare_rule(request, company_id):
    # Verifica si la solicitud es de tipo POST
    if request.method == "POST":

        # Obtiene las instancias de FareAttribute, Route y Zone correspondientes
        fare = FareAttribute.objects.get(id=request.POST["fare"])
        route = Route.objects.get(id=request.POST["route"])
        origin = Zone.objects.get(id=request.POST["origin"])
        destination = Zone.objects.get(id=request.POST["destination"])

        # Obtener el feed actual para la compañía dada
        current_feed = Feed.objects.get(company_id=company_id, is_current=True)

        # Crea una nueva instancia de FareRule con los datos proporcionados en la solicitud
        new_fare_rule = FareRule(
            feed_id = current_feed,
            fare=fare,
            route=route,
            origin=origin,
            destination=destination,
        )

        # Guarda la nueva regla de tarifa en la base de datos
        new_fare_rule.save()

        # Redirige a la página "edited" después de la creación exitosa
        return redirect(reverse("company_fare_rule", args=[company_id])) 
    else:
        # Si la solicitud no es de tipo POST, obtiene las instancias existentes necesarias y renderiza la página correspondiente
        fares = FareAttribute.objects.all()
        routes = Route.objects.all()
        zones = Zone.objects.all()

        # Se pasa por contexto las instancias necesarias
        context = {
            "fares": fares,
            "routes": routes,
            "zones": zones,
        }

        return render(request, "create/fare_rule.html", context)

def create_company(request):
    if request.method == "POST":
        # Obtiene la última compañía existente
        last_company = Company.objects.order_by('-company_id').first()

        # Calcula el nuevo ID para la compañía en base al id de la última compañía 
        if last_company:
            new_company_id = int(last_company.company_id) + 1
        else:
            new_company_id = 1

        # Crea una nueva instancia de la compañía con los datos proporcionados en la solicitud
        new_company = Company(
            company_id=new_company_id,
            name=request.POST["company_name"],
            address=request.POST["company_address"],
            phone=request.POST["company_phone"],
            email=request.POST["company_email"],
            website=request.POST["company_website"],
            logo=request.POST["company_logo"],
        )

        # Guarda la nueva compañía en la base de datos
        new_company.save()

        # Crea un nuevo feed enlazado a la compañía y con un feed_id relacionado a la fecha de creación
        new_feed_id = f"GTFS_{timezone.now().strftime('%Y%m%d%H%M%S')}"
        new_feed = Feed(
            feed_id=new_feed_id,
            company_id=new_company,
        )

        # Guarda el nuevo feed en la base de datos
        new_feed.save()

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
    feeds = Feed.objects.filter(company_id=company)

    # Renderiza el template de lista de feeds relacionados a una compañía
    return render(request, "list/list_feed.html", {"company": company, "feeds": feeds})

def list_companies(request):
    # Recupera la lista de instancias de Company
    companies = Company.objects.all()

    # Renderiza el template de lista de Company con la lista obtenida
    return render(request, "list/list_companies.html", {"companies": companies})




#MÉTODOS PARA ELIMINAR
def delete_agency(request, id, company_id):
    # Obtiene la agencia con el ID proporcionado
    agency = Agency.objects.get(id=id)

    # Elimina la agencia de la base de datos
    agency.delete()

    # Redirige a la lista de agencias después de eliminar
    return redirect(reverse("company_agency", args=[company_id]))

def delete_stop(request, id, company_id):
    # Obtiene la parada con el ID proporcionado
    stop = Stop.objects.get(id=id)

    # Elimina la parada de la base de datos
    stop.delete()

    # Redirige a la lista de paradas después de eliminar
    return redirect(reverse("company_stop", args=[company_id]))
 
def delete_route(request, id, company_id):
    # Obtiene la ruta con el ID proporcionado
    route = Route.objects.get(id=id)

    # Elimina la ruta de la base de datos
    route.delete()

    # Redirige a la lista de rutas después de eliminar
    return redirect(reverse("company_route", args=[company_id]))

def delete_zone(request, id, company_id):
    # Obtiene la zona con el ID proporcionado
    zone = Zone.objects.get(id=id)

    # Elimina la zona de la base de datos
    zone.delete()

    # Redirige a la lista de zonas después de eliminar
    return redirect(reverse("company_zone", args=[company_id]))

def delete_calendar(request, id, company_id):
    # Obtiene el calendario con el ID proporcionado
    calendar = Calendar.objects.get(id=id)

    # Elimina el calendario de la base de datos
    calendar.delete()

    # Redirige a la lista de calendarios después de eliminar
    return redirect(reverse("company_calendar", args=[company_id]))

def delete_calendar_dates(request, id, company_id, calendar_id):
    # Obtiene la fecha de calendario con el ID del servicio proporcionado
    calendar_date = CalendarDate.objects.get(id=id)

    # Elimina la fecha de calendario de la base de datos
    calendar_date.delete()

    # Redirige a la lista de fechas de calendario después de eliminar
    return redirect(reverse("company_calendar_date", args=[calendar_id, company_id]))

def delete_fare_attribute(request, id ,company_id):
    # Obtiene la tarifa con el ID proporcionado
    fare_attribute = FareAttribute.objects.get(id=id)

    # Elimina la tarifa de la base de datos
    fare_attribute.delete()

    # Redirige a la lista de tarifas después de eliminar
    return redirect(reverse("company_fare_attribute", args=[company_id]))

def delete_feed_info(request, feed_info_id):
    # Obtiene la instancia de FeedInfo con el ID proporcionado o devuelve un error 404 si no existe
    feed_info = FeedInfo.objects.get(id=feed_info_id)

    # Elimina la instancia de FeedInfo de la base de datos
    feed_info.delete()

    # Redirige a la lista de FeedInfo después de eliminar
    return redirect("list_feed_info")

def delete_fare_rule(request, id, company_id):
    # Obtiene la instancia de FareRule con el ID proporcionado o devuelve un error 404 si no existe
    fare_rule = FareRule.objects.get(id=id)

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

    feed = Feed.objects.get(feed_id=id)

    # Elimina la instancia de Feed de la base de datos
    feed.delete()

    # Recupera la lista de feeds relacionados a la compañía
    feeds = Feed.objects.filter(company_id=company)

    # Renderiza el template de lista de feeds relacionados a una compañía
    return render(request, "list/list_feed.html", {"company": company, "feeds": feeds})



# MÉTODOS PARA EDITAR
def edit_agency(request, id, company_id):
    # Obtiene la agencia con el ID proporcionado
    agency = Agency.objects.get(id=id)

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
    # Obtiene la parada con el ID proporcionado
    stop = Stop.objects.get(id=id)

    if request.method == "POST":
        # Actualiza la información de la parada con los datos proporcionados en el formulario
        stop.name = request.POST["stop_name"]
        stop.desc = request.POST["stop_desc"]
        stop.lat = float(request.POST["stop_lat"].replace(',', '.'))
        stop.lon = float(request.POST["stop_lon"].replace(',', '.'))
        stop.zone_id = request.POST["stop_zone"]  
        stop.url = request.POST["stop_url"]
        stop.location_type = request.POST["stop_location_type"]
        stop.parent_station = request.POST["stop_parent_station"]
        stop.wheelchair_boarding = request.POST["stop_wheelchair_boarding"]

        # En caso de tener la latitud y la longitud se van a utilizar para crear lo localización que es de tipo Point
        if "stop_lat" in request.POST and "stop_lon" in request.POST:
            stop.loc = Point(float(request.POST["stop_lon"].replace(',', '.')), float(request.POST["stop_lat"].replace(',', '.')))

        stop.save()

        # Redirige a la lista de paradas después de editar
        return redirect(reverse("company_stop", args=[company_id]))
    else:
        # Muestra el formulario de edición con la información actual de la parada y las zonas disponibles
        zones = Zone.objects.all()
        context = {"stop": stop, "zones": zones}
        return render(request, "edit/edit_stop.html", context)

def edit_route(request, id, company_id):
    # Obtiene la ruta con el ID proporcionado
    route = Route.objects.get(id=id)
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
        agency = Agency.objects.get(agency_id=agency_id)
        route.agency = agency

        route.save()

        # Redirige a la lista de rutas después de editar
        return redirect(reverse("company_route", args=[company_id]))
    else:
        # Muestra el formulario de edición con la información actual de la ruta y las agencias disponibles
        context = {"route": route, "agencies": agencies, "route_type_choices": route_type_choices}
        return render(request, "edit/edit_route.html", context)
  
def edit_zone(request, id, company_id):
    # Obtiene la zona con el ID proporcionado
    zone = Zone.objects.get(id=id)

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
    # Obtiene el calendario con el ID proporcionado
    calendar = Calendar.objects.get(id=id)

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
    # Obtiene la fecha del calendario con el ID proporcionado
    calendar_dates = CalendarDate.objects.get(id=id)

    if request.method == "POST":
        # Actualiza la información de la fecha del calendario con los datos proporcionados en el formulario
        calendar_dates.date = request.POST["date"]
        calendar_dates.exception_type = request.POST["exception_type"]
        calendar_dates.holiday_name = request.POST["holiday_name"]
        calendar_dates.save()
    
        # Redirige a la lista de fechas de calendario después de editar
        return redirect(reverse("company_calendar_date", args=[calendar_id, company_id]))
    else:
        # Muestra el formulario de edición con la información actual de la fecha del calendario
        context = {
            "calendar_dates": calendar_dates,
        }
        return render(request, "edit/edit_calendar_dates.html", context)

def edit_fare_attribute(request, id, company_id):
    # Obtiene la clase de tarifa con el ID proporcionado
    fare_attribute = FareAttribute.objects.get(id=id)
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
        # Muestra el formulario de edición con la información actual de la clase de tarifa y las agencias disponibles
        context = {"fare_attribute": fare_attribute, "agencies": agencies}
        return render(request, "edit/edit_fare_attribute.html", context)

def edit_feed_info(request, id, company_id):
    # Obtiene la instancia de FeedInfo con el ID proporcionado o devuelve un error 404 si no existe
    feed_info = FeedInfo.objects.get(id=id)

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
    # Obtiene la regla de tarifa con el ID proporcionado
    fare_rule = FareRule.objects.get(id=id)

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
        context = {
            "fare_rule": fare_rule,
            "zones": Zone.objects.all(),  # Puedes necesitar ajustar esto según tu implementación
            "fares": FareAttribute.objects.all(),
            "routes": Route.objects.all(),
        }
        return render(request, "edit/edit_fare_rule.html", context)

def edit_company(request, company_id):
    # Obtiene la compañía con el ID proporcionado
    company = Company.objects.get(company_id=company_id)

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
            id=str(current_feed.created_at),
            start_date=current_feed.created_at.date(),
            end_date=None,  # Replace with your default value
            publisher_name="Default Publisher",  # Replace with your default value
            publisher_url="http://default-publisher-url.com",  # Replace with your default value
            lang="en",  # Replace with your default value
            version="1.0",  # Replace with your default value
            contact_email="default@example.com"  # Replace with your default value
        )
        new_feed_info.save()
        feed_info = new_feed_info

    # Renderiza el template de detalle_company con la compañía y feed_info obtenidos
    return render(request, "company_screens/feed_info.html", {"company": company, 'feed_info': feed_info})




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
    return render(request, "agency_delete/view_agency_routes.html", context)

def delete_all_routes(request, agency_id):
        # Obtiene la agencia con el ID proporcionado
        agency = Agency.objects.get(agency_id=agency_id)

        # Obtiene todas las rutas asociadas a la agencia
        routes_to_delete = Route.objects.filter(agency=agency)

        # Elimina cada ruta de la base de datos
        for route in routes_to_delete:
            route.delete()
        
        # Redirige a la lista de rutas de la agencia correspondiente
        return redirect("view_agency_routes", agency_id=agency_id)

def update_all_routes_agency(request, agency_id):
    # Obtiene la nueva agencia

    if request.method == 'POST':
            
        new_agency_id = request.POST["new_agency_id"]
        new_agency = Agency.objects.get(agency_id=new_agency_id)

        # Actualiza la agencia de todas las rutas asociadas
        routes_to_update = Route.objects.filter(agency=agency_id)
        routes_to_update.update(agency=new_agency)

        # Redirige a la página "view_agency_routes" después de la actualización
        return redirect("view_agency_routes", agency_id=agency_id)
    else:
        return redirect("view_agency_routes", agency_id=agency_id)

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
