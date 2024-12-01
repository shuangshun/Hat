import json

from mcdreforged.api.all import *
from collections import OrderedDict

PLUGIN_METADATA = ServerInterface.get_instance().as_plugin_server_interface().get_self_metadata()

def tr(key, *args) -> str:
    return ServerInterface.get_instance().tr(f"{PLUGIN_METADATA.id}.{key}", *args)

def convert_ordered_dict_to_dict(data):
    if isinstance(data, OrderedDict):
        return {key: convert_ordered_dict_to_dict(value) for key, value in data.items()}

    elif isinstance(data, list):
        return [convert_ordered_dict_to_dict(item) for item in data]

    else:
        return data

def parsing_components(data):
    def transform(obj, is_top_level=True):
        if isinstance(obj, dict):
            items = []
            for key, value in obj.items():
                new_value = transform(value, False)

                if is_top_level:
                   items.append(f"{key}={new_value}")

                else:
                    items.append(f"{key}:{new_value}")

            return '{' + ', '.join(items) + '}'

        elif isinstance(obj, list):
            elements = [transform(item, False) for item in obj]
            return '[' + ', '.join(elements) + ']'

        else:
            return str(obj)

    transformed_data = transform(data)
    head_slot_data = f'[{transformed_data[1:-1]}]'.replace('minecraft:', '')
    head_slot_tag = json.dumps(head_slot_data, ensure_ascii=False)[1:-1]

    return head_slot_tag

def parsing_head_slot_data(data, type):
    for item in data:
        if item.get('Slot') == 103:
            try:
                if type == 'tag':
                   head_slot_tag = convert_ordered_dict_to_dict(item.get(type))

                elif type == 'components':
                   head_slot_dict = convert_ordered_dict_to_dict(item.get(type))
                   head_slot_tag = parsing_components(item.get(type))
                   return head_slot_tag

            except Exception as e:
                raise RuntimeError(f"Error in parsing process: {e}") from e
                return None

    return None
