class Author:
    def __init__(self, json) -> None:
        self.id = json["id"]
        self.username = json["username"]
        self.discriminator = json["discriminator"]

class EmbedField:
    def __init__(self, json) -> None:
        self.name = json["name"]
        self.value = json["value"]

class Embed:
    def __init__(self, json) -> None:
        self.title = json.get("title")
        self.author = json.get("author")
        self.description = json.get("description")
        self.fields = [EmbedField(field) for field in json["fields"]]

class Reference:
    def __init__(self, json) -> None:
        self.message_id = json["message_id"]
        self.message = MessageClass(json["resolved"])

class Button:
    def __init__(self, json) -> None:
        self.custom_id = json["custom_id"]
        self.disabled = json["disabled"]
        self.emoji = json["emoji"]
        self.label = json["label"]

class MessageClass:
    def __init__(self, message_json) -> None:
        self.id = message_json["id"]
        self.content = message_json.get("content")
        self.channel_id = message_json["channel_id"]
        self.guild_id = message_json["guild_id"]
        self.author = Author(message_json["author"])
        self.embed = Embed(message_json["embeds"][0]) if message_json.get("embeds") else None
        self.reference = Reference(message_json["reference"]) if message_json.get("reference") else None
        self.components = [Button(component) for component in message_json["components"][0]]
