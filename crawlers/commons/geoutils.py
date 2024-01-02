import math


class Coords:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

        # TODO: colocar alguns validações aqui


def distancia(p1: Coords, p2: Coords):
    """
    distância aproximada (em metros) entre 2 coordenadas
    """
    R = 6371e3
    [φ1, φ2, λ1, λ2] = [p1.latitude, p2.latitude, p1.longitude, p2.longitude]
    φ1 = φ1 * math.pi / 180.0
    φ2 = φ2 * math.pi / 180.0
    λ1 = λ1 * math.pi / 180.0
    λ2 = λ2 * math.pi / 180.0
    [Δφ, Δλ] = [φ2 - φ1, λ2 - λ1]
    a = math.sin(Δφ / 2) * math.sin(Δφ / 2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ / 2) * math.sin(Δλ / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d
