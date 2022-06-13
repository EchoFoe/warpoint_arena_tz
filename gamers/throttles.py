from rest_framework.throttling import AnonRateThrottle


class CustomRateThrottle(AnonRateThrottle):
    scope = 'custom_throttle'

    def get_cache_key(self, request, view):
        return self.get_ident(request)
