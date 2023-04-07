from core.models import Mercado
from functools import partial
from commons.geoutils import Coords, distancia


MAX_DISTANCE_PER_LATITUDE_DEGREE = 111.699
MAX_DISTANCE_PER_LONGITUDE_DEGREE = 111.321


def mercados_proximos(latitude: float, longitude: float, radius_in_km=10):
    delta_lat = radius_in_km / MAX_DISTANCE_PER_LATITUDE_DEGREE
    delta_long = radius_in_km / MAX_DISTANCE_PER_LONGITUDE_DEGREE
    latitude_range = [latitude - delta_lat, latitude + delta_lat]
    longitude_range = [longitude - delta_long, longitude + delta_long]
    mercado_qs = Mercado.objects.filter(
        latitude__range=latitude_range, longitude__range=longitude_range
    )
    mercados = []
    coordenadas = Coords(latitude=latitude, longitude=longitude)
    for mercado in mercado_qs:
        dist = distancia(mercado.coordenadas, coordenadas)
        if dist > radius_in_km:
            continue
        mercados.append((mercado, distancia))
    return sorted(mercados, key=lambda m: m[1])
