from celery import shared_task
import requests
import logging
from django.conf import settings

log = logging.getLogger(__name__)

@shared_task
def send_tag_data_to_api(object_id_str):
    """
    Celery task untuk mengirim data perubahan tag ke API eksternal.
    """
    # Mengambil URL dan Token dari konfigurasi Tutor (openedx-common-settings)
    api_url = getattr(settings, 'SYC_API_URL', 'https://api-syc.com/api/sync')
    api_token = getattr(settings, 'SYC_API_TOKEN', '')
    
    # [DEBUG] Menampilkan URL dan Token ke log celery
    log.info(f"--- DEBUG SETTINGS ---")
    log.info(f"Menggunakan URL: {api_url}")
    log.info(f"Menggunakan Token: {api_token}")
    
    headers = {
        "Content-Type": "application/json"
    }
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"
    
    # --- Tambahan untuk mengambil End Date ---
    end_date_str = None
    try:
        from opaque_keys.edx.keys import CourseKey, UsageKey
        from opaque_keys import InvalidKeyError
        from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
        
        try:
            course_key = CourseKey.from_string(object_id_str)
        except InvalidKeyError:
            # Jika yang dikirim adalah ID modul/video (UsageKey), ambil ID Course-nya
            course_key = UsageKey.from_string(object_id_str).course_key
            
        course = CourseOverview.get_from_id(course_key)
        if course.end:
            end_date_str = course.end.isoformat()
    except Exception as e:
        log.error(f"Failed to fetch course end date for {object_id_str}: {e}")
    # ----------------------------------------
    
    payload = {
        "course_id": object_id_str,
        "end_date": end_date_str
    }
    
    log.info(f"--- DEBUG API REQUEST ---")
    log.info(f"API Request Payload: {payload}")
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        log.info(f"Successfully sent tag change for {object_id_str} to API.")
        log.info(f"API Success Response: [{response.status_code}] {response.text}")
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to send tag change for {object_id_str} to API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            log.error(f"API Error Response: [{e.response.status_code}] {e.response.text}")
