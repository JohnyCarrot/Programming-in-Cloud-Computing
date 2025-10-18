"""
URL configuration for lab3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from debts import views as debts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', debts_views.index, name='index'),
    path('create', debts_views.debtor_create, name='create'),
    path("update/<int:pk>/", debts_views.debtor_update, name="update"),
    path("delete/<int:pk>/", debts_views.debtor_delete, name="delete"),
    path("toggle/<int:pk>/", debts_views.debtor_toggle_paid, name="toggle_paid"),
    path("migrate", debts_views.run_migrations, name="run_migrations"),
    path("download_data", debts_views.download_data, name="download_data"),
]
