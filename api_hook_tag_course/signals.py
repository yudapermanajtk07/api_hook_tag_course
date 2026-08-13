import logging
from django.dispatch import receiver
from openedx_events.content_authoring.signals import CONTENT_OBJECT_ASSOCIATIONS_CHANGED
from api_hook_tag_course.tasks import send_tag_data_to_api

log = logging.getLogger(__name__)

@receiver(CONTENT_OBJECT_ASSOCIATIONS_CHANGED)
def trigger_api_on_tag_update(sender, **kwargs):
    event_data = kwargs.get('event_data')
    if not event_data:
        return
    # 1. TAMBAHKAN DUA BARIS INI UNTUK DEBUGGING
    log.info(f"--- DEBUG EVENT DATA ---")
    log.info(f"Isi event_data.changes: {getattr(event_data, 'changes', 'TIDAK ADA')}")
    
    # 2. Hapus (atau comment) pengecekan 'tags' sementara waktu agar task PASTI dieksekusi
    # if hasattr(event_data, 'changes') and 'tags' in event_data.changes:
    
    object_id = str(event_data.object_id)
    log.info(f"Detected tag changes for object {object_id}. Triggering API call via Celery.")
    send_tag_data_to_api.delay(object_id)
