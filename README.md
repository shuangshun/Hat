# Hat

[![Issues](https://img.shields.io/github/issues/shuangshun/Hat?style=flat-square)](https://github.com/shuangshun/Hat/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/shuangshun/Hat?style=flat-square)](https://github.com/shuangshun/Hat/pulls)
[![Release](https://img.shields.io/github/v/release/shuangshun/Hat?include_prereleases&style=flat-square)](https://github.com/shuangshun/Hat/releases)
[![Downloads](https://img.shields.io/github/downloads/shuangshun/Hat/total?label=Github%20Release%20Downloads&style=flat-square)](https://github.com/shuangshun/Hat/releases)

提供一个命令 `!!here` , 允许玩家将手上的物品戴到头上

------

## 使用

- 安装前置 [Minecraft Data API](https://github.com/Fallen-Breath/MinecraftDataAPI)

- 安装 [Releases](https://github.com/shuangshun/Hat/releases/) 中的最新发布版

- 重启服务器或使用 `!!MCDR plugin reloadall` 命令重载所有插件

- 在游戏内拿着任意物品输入 `!!here` 命令

## 配置说明

- `permission` 能够使用 `!!here` 命令的最低权限等级
> 仅允许输入一个整数值, 详细请看 [权限概览](https://docs.mcdreforged.com/zh-cn/latest/permission.html#overview)

```json5
{
    "permission": 1 // 默认为 1 , 即普通玩家
}
```
