from django.apps import AppConfig


class DashbordAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Dashbord_admin'



    def ready(self):
        from Dashbord_admin import signals


