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

def parsing_head_slot_data(data):
    for item in data:
        if item.get('Slot') == 103:
            try:
                tag = item.get('tag')

                if tag is not None:
                    head_slot_tag = convert_ordered_dict_to_dict(tag)
                    return head_slot_tag

                else:
                    print("No 'tag' found in the item.")
                    return None

            except Exception as e:
                print(f"Error during conversion: {e}")
                return None

    return None
