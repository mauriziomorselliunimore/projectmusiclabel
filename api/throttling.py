from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class BurstRateThrottle(UserRateThrottle):
    rate = '60/minute'  # 60 richieste al minuto

class SustainedRateThrottle(UserRateThrottle):
    rate = '1000/day'  # 1000 richieste al giorno

class AnonymousThrottle(AnonRateThrottle):
    rate = '30/minute'  # 30 richieste al minuto per utenti anonimi
