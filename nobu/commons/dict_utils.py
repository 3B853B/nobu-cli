from typing import Any


class DictUtils:
    @classmethod
    def get_key(cls, data: dict[str, Any], target_key: str) -> Any | None:
        if isinstance(data, dict):
            for key, value in data.items():
                if key == target_key:
                    return value
                if isinstance(value, (dict, list)):
                    result = DictUtils.get_key(value, target_key)
                    if result is not None:
                        return result

        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    result = DictUtils.get_key(item, target_key)
                    if result is not None:
                        return result

        return None
