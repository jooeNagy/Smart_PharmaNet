from drf_spectacular.extensions import OpenApiAuthenticationExtension

class PharmacyJWTAuthentication(OpenApiAuthenticationExtension):
    target_class = 'accouunts.authentication.PharmacyJWTAuthentication'
    name = 'PharmacyJWT'
    
    def get_security_definition(self, auto_schema):
        return {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'JWT Token authentication'
        }