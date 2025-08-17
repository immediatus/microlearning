import json
from sqlalchemy.types import TypeDecorator, TEXT

class JSONArray(TypeDecorator):
    """Stores and retrieves a list as a JSON-encoded string."""
    impl = TEXT
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
