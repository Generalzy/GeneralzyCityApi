from rest_framework.throttling import SimpleRateThrottle


class SmsThrottle(SimpleRateThrottle):
    scope = 'phone'

    def get_cache_key(self, request, view):
        phone = request.data.get('phone')
        return self.cache_format % {'scope': self.scope, 'ident': phone}
