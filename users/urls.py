from django.urls import path, include
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # path("login/", view=views.user_login_view, name="user_login"),
    # path("logout/", view=views.user_logout_view, name="user_logout"),
    path("list/", view=views.user_list_view, name="user_list"),

    path(
        "<uuid:guid>/detail/",
        views.user_detail_api_view,
        name="user_detail",
    ),
    path(
        "<uuid:guid>/update/",
        views.user_update_api_view,
        name="user_update",
    ),

    path('register/', views.user_registration_api_view, name='register'),

    path('user-login/', views.MyObtainTokenPairView.as_view(), name='user-login'),

    path("logout/", view=views.user_logout_view, name="user_logout"),


]