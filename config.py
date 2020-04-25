'''
config.json schema

{
    "enable_auto_class_add" : bool,
    "auto_class_add_threshold" : float,
    "start_command_character" : str,
    "idle_status_options" : [str],
    "allowed_channels" : [long],
    "supported_filetypes" : [str],
    "save_path" : str,
    "bot_token" : str,
    "redis_host" : str,
    "redis_port" : int
}

example:
{
    "enable_auto_class_add" : true,
    "auto_class_add_threshold" : 0.90,
    "start_command_character" : "!",
    "idle_status_options" : ["Doing nothing...", "Idle"],
    "allowed_channels" : [4234987239487234],
    "supported_filetypes" : [".jpg", ".png", ".jpeg"],
    "save_path" : "~/bot/images",
    "bot_token" : "< DISCORD BOT TOKEN >",
    "redis_host" : "localhost",
    "redis_port" : 6379
}
'''

import json

def load_config():
    with open('config.json') as f:
        return json.load(f)

CONFIG = load_config()

def get(key):
    return CONFIG[key]

def format_string(s, **kwargs):
    '''
    Allows you to use config tokens in your strings.
    Example: format_string('Please call {start_command_character}train first') => 'Please call !train first'

    Optionally, you may use pass extra options in the form of kwargs.
    Example: format_string('Please call {start_command_character}train before {cmd_used}', cmd_used='!predict')
                => 'Please call !train before !predict'
    '''
    return s.format(**{**CONFIG, **kwargs}) # {**CONFIG, **kwargs} merges the dictionaries CONFIG and kwargs
