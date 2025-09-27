import io
import json
import nbtlib

from mcdreforged.api.all import *
from collections import OrderedDict

PLUGIN_METADATA = ServerInterface.get_instance().as_plugin_server_interface().get_self_metadata()


def tr(key, *args) -> str:
    return ServerInterface.get_instance().tr(f"{PLUGIN_METADATA.id}.{key}", *args)


def get_data_ver(server: PluginServerInterface) -> int:
    try:
        working_directory = server.get_mcdr_config()['working_directory']
        with io.open(f"{working_directory}/server.properties", "rt") as prop_file:
            while True:
                line = prop_file.readline()
                if line == "":
                    raise KeyError("level-name not found")

                if line.startswith('#'):
                    continue

                key, val = line.split('=')
                if key.strip() != "level-name":
                    continue

                level_name = val.strip()
                break
        level = nbtlib.load(f'{working_directory}/{level_name}/level.dat').get('Data')
        data_version = level['DataVersion']
        return int(data_version)
    except Exception:
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
    try:
        components = []
        for k, v in data.items():
            components.append(f'{k}={json.dumps(v, ensure_ascii=False)}')

        transformed_data = '{' + ', '.join(components) + '}'
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
