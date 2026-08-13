import logging
from django.dispatch import receiver
from openedx_events.content_authoring.signals import CONTENT_OBJECT_ASSOCIATIONS_CHANGED
from api_hook_tag_course.tasks import send_tag_data_to_api

log = logging.getLogger(__name__)

@receiver(CONTENT_OBJECT_ASSOCIATIONS_CHANGED)
def trigger_api_on_tag_update(sender, **kwargs):
    """
    Receiver function that listens to the CONTENT_OBJECT_ASSOCIATIONS_CHANGED event.
    It checks if the changes involve 'tags' and if so, triggers a Celery task.
    """
    event_data = kwargs.get('event_data')
    
    if not event_data:
        return

    # Periksa apakah perubahan yang terjadi melibatkan tag
    if hasattr(event_data, 'changes') and 'tags' in event_data.changes:
        object_id = str(event_data.object_id)
        log.info(f"Detected tag changes for object {object_id}. Triggering API call via Celery.")
        
        # Eksekusi task celery secara asinkron (background)
        send_tag_data_to_api.delay(object_id)
