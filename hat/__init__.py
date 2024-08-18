import minecraft_data_api as api

from mcdreforged.api.all import *
from hat.config import *
from hat.utils import *

@new_thread("Hat")
def hat(server: ServerInterface, src: CommandSource):
    if isinstance(src, PlayerCommandSource):
        if not src.has_permission(config.permission):
           src.reply(RText(tr('required_permission'), RColor.red))
           return

        player_name = src.get_info().player
        inventory = api.get_player_info(player_name, 'Inventory')
        selected_item = api.get_player_info(player_name, 'SelectedItem', timeout=0.2)

        if selected_item is None:
            src.reply(RText(tr('hand_is_empty'), RColor.red))
            return

        selected_item_slot = api.get_player_info(player_name, 'SelectedItemSlot')

        server.execute(f'item replace entity {player_name} armor.head from entity {player_name} hotbar.{selected_item_slot}')

        for item in inventory:
            if item['Slot'] == 103:
                head_slot_id = item.get('id')
                head_slot_count = item.get('Count')

                if 'tag' in item:
                    head_slot_tag = str(parsing_head_slot_data(inventory)) + ' '

                else:
                    head_slot_tag = ' '

                server.execute(f'item replace entity {player_name} hotbar.{selected_item_slot} with {head_slot_id}{head_slot_tag}{head_slot_count}')
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
    