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
    
    payload = {
        "object_id": object_id_str,
        "event_type": "tags_changed"
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        log.info(f"Successfully sent tag change for {object_id_str} to API.")
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to send tag change for {object_id_str} to API: {e}")
