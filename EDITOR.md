# Editor GTFS Schedule

Este documento reúne las tablas con los datos que serán implementados y la secuencia de edición en la aplicación.

## GTFS Schedule v2.0 

Revisión: 16 de noviembre de 2023

### Tablas

> En **negrita** las tablas para editar. En *cursiva* las tablas no consideradas. En ***negrita y cursiva*** las de implementación no prioritaria.

- :white_check_mark: **agency.txt** (requerida)
- :white_check_mark: **stops.txt** (requerida)
- :white_check_mark: **routes.txt** (requerida)
- :white_check_mark: **trips.txt** (requerida)
- :white_check_mark: **stop_times.txt** (requerida)
- :white_check_mark: **calendar.txt** (requerida condicionalmente con calendar_dates.txt)
- :white_check_mark: **calendar_dates.txt** (requerida condicionalmente con calendar.txt)
- :white_check_mark: **fare_attributes.txt** (opcional)
- :white_check_mark: **fare_rules.txt** (opcional)
- :x: *timeframes.txt* (opcional)
- :x: *fare_media.txt* (opcional)
- :x: *fare_products.txt* (opcional)
- :x: *fare_leg_rules.txt* (opcional)
- :x: *fare_transfer_rules.txt* (opcional)
- :x: *areas.txt* (opcional)
- :x: *stop_areas.txt* (opcional)
- :x: *networks.txt* (prohibida condicionalmente)
- :x: *route_networks.txt* (prohibida condicionalmente)
- :white_check_mark: **shapes.txt** (opcional)
- :white_check_mark: ***frequencies.txt*** (opcional)
- :x: *transfers.txt* (opcional)
- :x: *pathways.txt* (opcional)
- :x: *levels.txt* (opcional)
- :x: *location_groups.txt* (opcional)
- :x: *location_group_stops.txt* (opcional)
- :x: *locations.geojson* (opcional)
- :x: *booking_rules.txt* (opcional)
- :x: *translations.txt* (opcional)
- :white_check_mark: **feed_info.txt** (opcional)
- :white_check_mark: ***attributions.txt*** (opcional)

En total son **trece (13) tablas** de GTFS Schedule utilizadas en el editor, de las cuales **once (11)** son de implementación inmediata y **dos (2)** (frequencies.txt, attributions.txt) son de implementación no prioritaria.

Además, hay varias tablas auxiliares:

- :white_check_mark: **feeds**: histórico de *feeds* GTFS Schedule creados en el editor, incluyendo los vencidos, el actual publicado y el que está en edición
- :white_check_mark: **geoshapes**: trayectorias guardadas como geometrías en la base de datos geoespacial
- :white_check_mark: **route_stops**: secuencia de paradas para cada combinación de ruta (`route_id`) y trayectoria (`shape_id`)
- :white_check_mark: **trip_durations**: aproximación de la duración de un viaje en un intervalo del día para cada combinación de ruta (`route_id`), trayectoria (`shape_id`) y calendario (`service_id`)
- :white_check_mark: **trip_times**: tiempos de salida de cada viaje
- :eight_spoked_asterisk: **stop_times_measurements**
- :eight_spoked_asterisk: **estimation_models**

Las tablas *stop_times_measurements* y *estimation_models* son generadas de forma independiente y periódica a partir de los datos regitrados en *stop_times_estimations*. 

El editor edita en total **dieciocho (18)** tablas.

## Orden de edición

Asumiendo una aplicación "de una página" (**SPA**, *Single-Page Application*), la creación de un suministro (*feed*) de GTFS sucede en **ocho pasos**:

1. :page_facing_up: **Inicio** :house:
   - Descripción general
1. :page_facing_up: **Agencias** :key:
   - agency.txt
2. :page_facing_up: **Paradas** :busstop:
   - stops.txt
3. :page_facing_up: **Calendario** :calendar:
   - calendar.txt
   - calendar_dates.txt
4. :page_facing_up: **Rutas** :oncoming_bus:
   - routes.txt
   - shapes.txt (una ruta puede tener más de una trayectoria)
   - geoshapes
   - route_stops
   - route_durations
5. :page_facing_up: **Viajes** :clock130:
   - trips.txt
   - *frequencies.txt*
   - trip_times
   - stop_times.txt
6. :page_facing_up: **Tarifas** :dollar:
   - fare_attributes.txt
   - fare_rules.txt
7. :page_facing_up: **Información** :information_source:
   - feed_info.txt
   - *attributions.txt*
8. :page_facing_up: **Revisión y exportación** :ok:
   - feeds

### Esbozo de cada sitio de edición

- Colección de *componentes* que estarían en cada sitio de edición.
- Operaciones CRUD requeridas del API

#### Agencias

Información sobre las "agencias" que operan el servicio. En Costa Rica, podría ser una sola agencia (el CTP, por ejemplo) o cientos de concesionarios, dependiendo de quién publica el suministro.

##### Componentes

- Tabla con registros
- Botón de creación de nuevo registro
- 

##### Solicitudes API

```bash
GET /api/agency
```

## Comentarios sobre la implementación

Motivos para tener un servidor y base de datos separado del servidor en tiempo real Databús:

- Posibilidad de interactuar con otras bases de datos (por ejemplo, para recopilar información oficial de paradas, rutas, etc.). Este también es un motivo para justificar la separación del _backend_ del _frontend_ en React JS y no utilizar soluciones alternativas como Django _full stack_ con HTMX.
- Las demandas de desempeño de Databús y el editor son diferentes. Databús es más "sucio" porque está en tiempo real procesando una "alta" cantidad de datos, y sería imaginable un colapso más fácilmente. Mientras que el editor es más "limpio" y su uso más "pausado", gestionado por personas.

## Algunos modelos especiales

```python
class Feed(models.Model):
   (...)
   is_draft = models.BooleanField()
   is_complete = models.BooleanField()
   is_valid = models.BooleanField()
   is_current = models.BooleanField()
   zip_file = models.FileField(upload_to="feeds")
   (...)
```

```python
class StopTimeEstimation(models.Model):
   (...)
   estimation_id =
   route_id =
   shape_id =
   has_measurements = models.BooleanField()
   
```

```python
class StopTimeMeasurements(models.Model):
   """They should be usable for any route or segment"""
   begins_at_stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
   begins_at = models.DateTimeField()
   ends_at_stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
   ends_at = models.DateTimeField()
   shape = models.LineStringField()
   duration = models.DurationField()
```

```python
class TripTime(models.Model):
   trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
   stop_id = models.ForeignKey(Stop, on_delete=models.CASCADE)
   trip_time = models.TimeField()
```

```python
class EstimationModel(models.Model):
   MODEL_TYPE_CHOICES = [
      ("poly", "Polynomial"),
      ("exp", "Exponential"),
   ]   
   estimation_id = models.ForeignKey(StopTimeEstimation, on_delete=models.CASCADE)
   model_type = models.CharField(choices=MODEL_TYPE_CHOICES)
   parameters = models.JSONField()
```

## Propuesta de implementación

Contexto:

- Software B2b
- Panel de administración
- CRUD intensivo
- Múltiples validaciones

Entonces:

- `[dominio].cr`
  - Información general
  - Datos de los *feeds*
  - Registro de usuarios
- `editor.[dominio].cr` (*single-page application*)
  - Edición de un nuevo *feed*
