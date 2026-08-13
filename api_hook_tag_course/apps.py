from django.apps import AppConfig

class ApiHookConfig(AppConfig):
    name = 'api_hook_tag_course'
    verbose_name = 'API Hook for Course Tags'

    plugin_app = {
        'url_config': {
            'lms.djangoapp': {},
            'cms.djangoapp': {},
        },
        'settings_config': {
            'lms.djangoapp': {},
            'cms.djangoapp': {},
        },
    }

    def ready(self):
        # Mengimpor signals ketika Django sudah siap agar receiver terdaftar
        import api_hook_tag_course.signals
