'''
config.json schema

{
    "start_command_character" : str,
    "idle_status_options" : [str],
    "allowed_channels" : [long],
    "supported_filetypes" : [str],
    "save_path" : str,
    "bot_token" : str
}

example:
{
    "start_command_character" : "!",
    "idle_status_options" : ["Doing nothing...", "Idle"],
    "allowed_channels" : [4234987239487234],
    "supported_filetypes" : [".jpg", ".png", ".jpeg"],
    "save_path" : "~/bot/images,
    "bot_token" : "< DISCORD BOT TOKEN >"
}
'''

import json

def load_config():
    with open('config.json') as f:
        return json.load(f)

CONFIG = load_config()

def get(key):
    return CONFIG[key]

def format_string(s):
    '''
    Allows you to use config tokens in your strings.
    Example: format_string('Please call {start_command_character}train first') => 'Please call !train first'
    '''
    return s.format(**CONFIG)
