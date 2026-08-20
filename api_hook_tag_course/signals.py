import logging
from django.dispatch import receiver
from openedx_events.content_authoring.signals import CONTENT_OBJECT_ASSOCIATIONS_CHANGED
from api_hook_tag_course.tasks import send_tag_data_to_api

log = logging.getLogger(__name__)

@receiver(CONTENT_OBJECT_ASSOCIATIONS_CHANGED)
def trigger_api_on_tag_update(sender, **kwargs):
    # Cetak semua parameter yang diterima untuk melihat nama variabel aslinya
    log.info(f"--- DEBUG KWARGS ---")
    log.info(f"Kwargs keys: {list(kwargs.keys())}")
    
    # Ambil object_data (umumnya di OEP-50 namanya bukan 'event_data')
    # Kita asumsikan namanya 'object_data' atau sejenisnya.
    # Untuk sementara, mari kita temukan nilainya dulu:
    event_data = None
    for key, value in kwargs.items():
        if key != 'signal':
            event_data = value
            break
            
    if not event_data:
        log.warning("No data found in kwargs!")
        return
    
    # 2. Hapus (atau comment) pengecekan 'tags' sementara waktu agar task PASTI dieksekusi
    # if hasattr(event_data, 'changes') and 'tags' in event_data.changes:
    
    object_id = str(event_data.object_id)
    log.info(f"Detected tag changes for object {object_id}. Triggering API call via Celery.")
    send_tag_data_to_api.delay(object_id)


from openedx_events.content_authoring.signals import COURSE_CATALOG_INFO_CHANGED

@receiver(COURSE_CATALOG_INFO_CHANGED)
def trigger_api_on_course_publish(sender, **kwargs):
    """
    Menangkap sinyal ketika course di-publish (termasuk saat settings disimpan).
    """
    log.info(f"--- DEBUG COURSE_CATALOG_INFO_CHANGED KWARGS ---")
    log.info(f"Kwargs keys: {list(kwargs.keys())}")
    
    # Umumnya event data ada di 'catalog_info'
    catalog_data = kwargs.get('catalog_info')
    
    if not catalog_data:
        for key, value in kwargs.items():
            if key != 'signal':
                catalog_data = value
                break
                
    if not catalog_data:
        log.warning("No data found in COURSE_CATALOG_INFO_CHANGED kwargs!")
        return

    # Ekstrak ID Course yang sebenarnya
    if hasattr(catalog_data, 'course_key'):
        object_id = str(catalog_data.course_key)
    else:
        object_id = str(catalog_data)

    log.info(f"Detected course publish/settings change for {object_id}. Triggering API call via Celery.")
    send_tag_data_to_api.delay(object_id)
