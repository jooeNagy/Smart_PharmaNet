from drf_spectacular.extensions import OpenApiAuthenticationExtension

class PharmacyJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'accounts.authentication.PharmacyJWTAuthentication'
    name = 'jwtAuth'
    
    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }