# Hat

[![](https://img.shields.io/github/v/release/shuangshun/Hat)](https://github.com/shuangshun/Hat/releases)
[![](https://shields.io/github/downloads/shuangshun/Hat/total)](https://github.com/MrXiaoM/shuangshun/Hat)
[![](https://img.shields.io/github/stars/shuangshun/Hat)](https://github.com/shuangshun/Hat)

[English](README.md) | **中文**

提供一个命令 `!!hat` , 允许玩家将手上的物品戴到头上

------

## 使用

- 安装好插件及所需的全部依赖

- 在游戏内拿着任意物品输入 `!!hat` 命令

## 配置说明

- `permission` 设置能够使用 `!!hat` 命令的最低权限等级
> 仅允许输入一个整数值, 详细请看 [权限概览](https://docs.mcdreforged.com/zh-cn/latest/permission.html#overview)

- `cooldown` 设置使用 `!!hat` 命令的冷却时间(单位: 秒)

```json5
{
    "permission": 1, // 默认为 1, 即普通玩家
    "cooldown": 3 // 默认为 3 秒
}
```

------

> [!Warning]
> 注意! 本插件仅适用于 [1.17+](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4/item#%E5%8E%86%E5%8F%B2)
