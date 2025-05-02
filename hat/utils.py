import json
import nbtlib

from mcdreforged.api.all import *
from collections import OrderedDict

PLUGIN_METADATA = ServerInterface.get_instance().as_plugin_server_interface().get_self_metadata()


def tr(key, *args) -> str:
    return ServerInterface.get_instance().tr(f"{PLUGIN_METADATA.id}.{key}", *args)


def get_data_ver() -> int:
    try:
        level = nbtlib.load('server/world/level.dat').get('Data')
        data_version = level['DataVersion']
        return int(data_version)
    except KeyError:
        return -1


def convert_ordered_dict_to_dict(data):
    try:
        if isinstance(data, OrderedDict):
            return {key: convert_ordered_dict_to_dict(value) for key, value in data.items()}

        elif isinstance(data, list):
            return [convert_ordered_dict_to_dict(item) for item in data]

        else:
            return data
    except Exception as e:
        raise ValueError(f"Error converting data: {e}") from e


def parse_components(data):
    def transform(data, is_top_level=True, is_top_level_key=False):
        if isinstance(data, dict):

            components = []
            for k, v in data.items():
                if is_top_level and not is_top_level_key:
                    components.append(f'{k}={json.dumps(v, ensure_ascii=False)}')

                else:
                    components.append(f'"{k}": {json.dumps(v, ensure_ascii=False)}')
            return '{' + ', '.join(components) + '}'

        elif isinstance(data, list):
            return '[' + ', '.join(json.dumps(item, ensure_ascii=False) for item in data) + ']'

        else:
            if isinstance(data, (int, float)):
                return f'{data}'

            return json.dumps(data, ensure_ascii=False)

    try:
        transformed_data = transform(data)
        head_slot_tag = f'[{transformed_data[1:-1]}]'.replace('minecraft:', '')
        return head_slot_tag
    except Exception as e:
        raise ValueError(f"Error converting data: {e}") from e


def parse_head_slot_data(item, type):
    try:
        value = item.get(type)

        if type == 'tag':
            return convert_ordered_dict_to_dict(value)

        elif type == 'components':
            return parse_components(value)

    except KeyError as e:
        raise KeyError(f'Error in parsing process: {e}') from e

    except TypeError as e:
        raise TypeError(f'Error in parsing process: {e}') from e
