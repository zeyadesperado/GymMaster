from django.utils.deprecation import MiddlewareMixin

class ReferrerPolicyMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response