from celery import shared_task
import requests
import logging

log = logging.getLogger(__name__)

@shared_task
def send_tag_data_to_api(object_id_str):
    """
    Celery task untuk mengirim data perubahan tag ke API eksternal.
    """
    # Ganti URL ini dengan URL API Anda sebenarnya
    api_url = "https://api.example.com/webhook/tags"
    
    payload = {
        "object_id": object_id_str,
        "event_type": "tags_changed"
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()
        log.info(f"Successfully sent tag change for {object_id_str} to API.")
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to send tag change for {object_id_str} to API: {e}")
