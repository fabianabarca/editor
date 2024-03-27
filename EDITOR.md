# Editor GTFS Schedule

Este documento reúne las tablas con los datos que serán implementaros y la secuencia de edición en la aplicación.

## GTFS Schedule v2.0 

Revisión: 16 de noviembre de 2023

### Tablas

> En **negrita** las tablas para editar. En *cursiva* las tablas no consideradas. En ***negrita y cursiva*** de implementación no prioritaria.

- **agency.txt** (requerida)
- **stops.txt** (requerida)
- **routes.txt** (requerida)
- **trips.txt** (requerida)
- **stop_times.txt** (requerida)
- **calendar.txt** (requerida condicionalmente con calendar_dates.txt)
- **calendar_dates.txt** (requerida condicionalmente con calendar.txt)
- **fare_attributes.txt** (opcional)
- **fare_rules.txt** (opcional)
- *timeframes.txt* (opcional)
- *fare_media.txt* (opcional)
- *fare_products.txt* (opcional)
- *fare_leg_rules.txt* (opcional)
- *fare_transfer_rules.txt* (opcional)
- *areas.txt* (opcional)
- *stop_areas.txt* (opcional)
- *networks.txt* (prohibida condicionalmente)
- *route_networks.txt* (prohibida condicionalmente)
- **shapes.txt** (opcional)
- ***frequencies.txt*** (opcional)
- *transfers.txt* (opcional)
- *pathways.txt* (opcional)
- *levels.txt* (opcional)
- *location_groups.txt* (opcional)
- *location_group_stops.txt* (opcional)
- *locations.geojson* (opcional)
- *booking_rules.txt* (opcional)
- *translations.txt* (opcional)
- **feed_info.txt** (opcional)
- ***attributions.txt*** (opcional)

En total son **trece (13) tablas** de GTFS Schedule utilizadas en el editor, de las cuales **once (11)** son de implementación inmediata y **dos (2)** (frequencies.txt, attributions.txt) son de implementación no prioritaria.

Además, hay varias tablas auxiliares:

- **geoshapes**
- **route_stops**
- **trip_times**
- **estimation_models**

El editor edita en total **diecisiete (17)** tablas.

## Orden de edición

Asumiendo una aplicación "de una página" (**SPA**, *Single-Page Application*), la creación de un suministro (*feed*) de GTFS sucede en **ocho pasos**:

1. AGENCIA
   - agency.txt
2. PARADAS
   - stops.txt
3. RUTAS
   - routes.txt
4. TRAYECTORIAS
   - shapes.txt
   - geoshapes
   - route_stops
   - estimation_models
5. CALENDARIO
   - calendar.txt
   - calendar_dates.txt
6. VIAJES
   - trips.txt
   - *frequencies.txt*
   - trip_times
   - stop_times.txt
7. TARIFAS
   - fare_attributes.txt
   - fare_rules.txt
8. INFORMACIÓN
   - feed_info.txt
   - *attributions.txt*
