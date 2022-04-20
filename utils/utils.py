import re
import secrets
import time
import traceback
import json
from typing import Optional
from . import Instance
pattern = re.compile("\d+")

def get_headers(instance, payload=None):
    headers = {
        "Authorization": instance.token,
        "Content-Type": "application/json"
    }
    if payload:
        headers["Content-Length"] = str(len(payload))
    return headers

def get_payload(response, custom_id):
    payload = {
        "type":3,
        "guild_id": response.guild_id,
        "channel_id": response.channel_id,
        "message_flags":0,
        "message_id": response.id,
        "application_id": "270904126974590976",
        "session_id": secrets.token_urlsafe(),
        "data": {
            "component_type":2,
            "custom_id": custom_id,
        }
    }

    return response.json()


get_digits = lambda x: re.findall(pattern, x) or None

async def send_response_eh(instance: Instance.Instance, send_message):
    # send message response error handling
    send_message_json = None
    traceback_id = f"{instance.id}.{str(time.time())[:14]}"
    try:
        send_message_json: Optional[dict[str, str]] = await send_message.json()
    except json.decoder.JSONDecodeError:
        instance.logger.warning(f"Command send response was not json-parsable. Traceback ID: {traceback_id}", extra={"token": instance.token, "username": instance.name, "status_code": 412})
        instance.traceback_logger.warning(traceback.format_exc())
        return 412, "NotJson"
    except Exception:
        instance.logger.error(f"beg send response - Unhandled Exception. Traceback ID: {traceback_id})", extra={"token": instance.token, "username": instance.name, "status_code": 422})
        instance.traceback_logger.critical(traceback.format_exc())
        return 422, "NotHandled"

    # Send message error handling
    if send_message.status_code not in (200, 204):
        instance.logger.warning("Command was not sent.", extra={"token": instance.token, "username": instance.name, "status_code": 417})
        return 417, "NotSent"
    return 200 if send_message.status_code == 200 else 204, send_message_json