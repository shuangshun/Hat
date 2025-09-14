import time
import minecraft_data_api as api

from mcdreforged.api.all import *
from hat.config import *
from hat.utils import *


last_execution_time = {}
@new_thread("hat")
def hat(server: ServerInterface, src: CommandSource):
    if isinstance(src, PlayerCommandSource):
        if not src.has_permission(config.permission):
            src.reply(RText(tr('required_permission'), RColor.red))
            return

        player_name = src.get_info().player

        current_time = time.time()
        if player_name in last_execution_time and (current_time - last_execution_time[player_name]) < config.cooldown:
            remaining_time = int(config.cooldown - (current_time - last_execution_time[player_name]))
            src.reply(RText(tr('on_cooldown', remaining_time), RColor.red))
            return

        last_execution_time[player_name] = current_time

        selected_item = api.get_player_info(player_name, 'SelectedItem', timeout=0.2)

        if selected_item is None:
            src.reply(RText(tr('hand_is_empty'), RColor.red))
            return

        inventory = api.get_player_info(player_name, 'Inventory')
        if data_ver >= 4063:
            equipment = api.get_player_info(player_name, 'equipment.head', timeout=0.2)
            if equipment is not None:
                equipment['Slot'] = 103
                inventory.append(equipment)

        selected_item_slot = api.get_player_info(player_name, 'SelectedItemSlot')

        selected_slot_count = selected_item.get('Count') or selected_item.get('count')
        if any(item_id in selected_item.get('id') for item_id in ['shulker_box', 'enchanted_book']) and selected_slot_count > 1:
            src.reply(RText(tr('too_many_items'), RColor.red))
            return

        server.execute(f'item replace entity {player_name} armor.head from entity {player_name} hotbar.{selected_item_slot}')

        for item in inventory:
            if item['Slot'] == 103:
                head_slot_id = item.get('id')

                head_slot_count = item.get('Count') or item.get('count')

                head_slot_tag = ''
                if 'tag' in item or 'components' in item:
                    key = 'tag' if 'tag' in item else 'components'
                    head_slot_tag = str(parse_head_slot_data(item, key))

                server.execute(f'item replace entity {player_name} hotbar.{selected_item_slot} with {head_slot_id}{head_slot_tag} {head_slot_count}')
                break
        else:
            server.execute(f'item replace entity {player_name} hotbar.{selected_item_slot} with air')

        src.reply(RText(tr('success'), RColor.green))

    else:
        src.reply(RText(tr('use_in_player'), RColor.red))


def register_commands_and_help(server: PluginServerInterface):
    server.register_command(
        Literal("!!hat")
        .runs(lambda src: hat(server, src))
    )

    server.register_help_message(
        '!!hat',
        tr('help')
    )


def on_load(server: PluginServerInterface, old):
    global config, data_ver
    config = server.load_config_simple(ConfigFilePath, target_class=Config, in_data_folder=False)
    data_ver = get_data_ver(server)

    if data_ver < 2714:
        if data_ver == -1:
            server.logger.warning(tr('get_ver_fail'))
        else:
            server.logger.warning(tr('unsupported_ver'))
        server.unload_plugin('hat')
        return

    register_commands_and_help(server)
