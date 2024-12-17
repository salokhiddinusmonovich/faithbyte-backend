from drf_yasg import openapi

def get_token():
    token = openapi.Parameter('token', openapi.IN_QUERY, description="register api token", 
                              type=openapi.TYPE_STRING)
    return [token]