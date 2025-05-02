# Hat

[![](https://img.shields.io/github/v/release/shuangshun/Hat)](https://github.com/shuangshun/Hat/releases)
[![](https://shields.io/github/downloads/shuangshun/Hat/total)](https://github.com/MrXiaoM/shuangshun/Hat)
[![](https://img.shields.io/github/stars/shuangshun/Hat)](https://github.com/shuangshun/Hat)

**English** | [中文](README_zh_cn.md)

Provides a command `!!hat`, allowing players to wear items on their heads.

---

## Usage

- Install the plugin and all required dependencies.
- Hold any item in your hand and enter the `!!hat` command in the game.

## Configuration Explanation

- `permission` sets the minimum permission level required to use the `!!hat` command.
> Only integer values are allowed. For details, please refer to [Permission Overview](https://docs.mcdreforged.com/en/latest/permission.html#overview).

- `cooldown` sets the cooldown time for using the `!!hat` command (unit: seconds).

```json5
{
    "permission": 1, // Default is 1, regular player
    "cooldown": 3 // Default is 3 seconds
}
```

------

> [!Note]
> Notice! This plugin is only applicable for [1.17+](https://minecraft.wiki/w/Commands/item#History)
