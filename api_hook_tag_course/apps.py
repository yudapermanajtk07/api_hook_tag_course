from django.apps import AppConfig

class ApiHookConfig(AppConfig):
    name = 'api_hook_tag_course'
    verbose_name = 'API Hook for Course Tags'

    plugin_app = {}

    def ready(self):
        # Mengimpor signals ketika Django sudah siap agar receiver terdaftar
        import api_hook_tag_course.signals
