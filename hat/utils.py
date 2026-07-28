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
        with open(f'{working_directory}/server.properties', 'rt', encoding='utf-8') as props:
            for line in props:
                line = line.strip()
                if not line.startswith('level-name='):
                    continue

                level_name = line.split('=', 1)[1]
                break
            else:
                level_name = 'world'
                server.logger.warning(tr('get_level_name_fail'))

        level = nbtlib.load(f'{working_directory}/{level_name}/level.dat').get('Data')
        data_version = level['DataVersion']
        return int(data_version)
    except Exception as e:
        server.logger.error(e)
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
        components = ', '.join(f'{k}={json.dumps(v, ensure_ascii=False)}' for k, v in data.items())
        head_slot_tag = f'[{components}]'.replace('minecraft:', '')
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


def build_item_replace_cmd(
        target_entity, target_slot, *,
        source_slot = None,
        item_id = None, item_tag = "", count = None) -> str:
    if source_slot is not None:
        return f'item replace entity {target_entity} {target_slot} from entity {target_entity} {source_slot}'

    elif item_id is not None:
        cmd = f'item replace entity {target_entity} {target_slot} with {item_id}{item_tag}'
        if count is not None:
            cmd += f' {count}'
        return cmd

    else:
        raise ValueError("Either source_slot or item_id must be provided")