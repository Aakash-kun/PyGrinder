import re
import secrets
import Classes


pattern = re.compile("\d+")

def get_headers(instance: Classes.Instance, payload=None):
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