import time
import minecraft_data_api as api

from mcdreforged.api.all import *
from hat.config import *
from hat.utils import *


last_execution_time = {}
@new_thread("Hat")
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
        selected_item_slot = api.get_player_info(player_name, 'SelectedItemSlot')

        for item in inventory:
            if item['Slot'] == selected_item_slot:

                if 'Count' in item:
                    head_slot_count = item.get('Count')

                else:
                    head_slot_count = item.get('count')

                if any(item_id in item.get('id') for item_id in ['shulker_box', 'enchanted_book']) and head_slot_count > 1:
                    src.reply(RText(tr('too_many_items'), RColor.red))
                    return

        server.execute(f'item replace entity {player_name} armor.head from entity {player_name} hotbar.{selected_item_slot}')

        for item in inventory:
            if item['Slot'] == 103:
                head_slot_id = item.get('id')

                if 'Count' in item:
                    head_slot_count = item.get('Count')

                else:
                    head_slot_count = item.get('count')

                if 'tag' in item:
                    head_slot_tag = str(parse_head_slot_data(inventory, 'tag'))

                elif 'components' in item:
                    head_slot_tag = str(parse_head_slot_data(inventory, 'components'))

                else:
                    head_slot_tag = ''

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
        RText(tr('help'))
    )


def on_load(server: ServerInterface, old):
    global config
    config = server.load_config_simple(ConfigFilePath, target_class=Config, in_data_folder=False)

    register_commands_and_help(server)
