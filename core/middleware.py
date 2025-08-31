from django.middleware.security import SecurityMiddleware

class CustomSecurityMiddleware(SecurityMiddleware):
    def process_response(self, request, response):
        response = super().process_response(request, response)
        
        # Aggiunge headers di sicurezza
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Se in produzione, aggiunge HSTS
        if not request.is_secure():
            return response
            
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
