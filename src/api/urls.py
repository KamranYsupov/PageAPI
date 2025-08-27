from django.urls import path, include

app_name = 'api_v1'

urlpatterns = [
    path('v1/', include('api.v1.urls'))
]