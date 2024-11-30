from mcdreforged.api.all import *

class Config(Serializable):
	permission: int = 1,
	cooldown: int = 3

config: Config
ConfigFilePath = 'config/hat.json'