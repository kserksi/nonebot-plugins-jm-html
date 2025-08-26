<div align="center">
  <a href="https://nonebot.dev/store/plugins">
    <img src="./image/NoneBotPlugin.svg" width="300" alt="logo">
  </a>
</div>
<div align="center">

# nonebot_plugin_jm_html

</div>

## 📖 介绍

下载禁漫漫画，整理后合成本地链接，方便在线阅读。

## 💿 安装

使用 nb-cli 安装插件

```shell
nb plugin install nonebot_plugins_jm_html
```

使用 pip 安装插件

```shell
pip install nonebot_plugins_jm_html
```

## 🕹️ 使用

**/jm [禁漫号]** : 获得对应禁漫号的本地链接

## ⚙️ 配置

| 配置项       | 默认值  | 说明                            |
| ----------- |------|-------------------------------|
|jm_pwd       | None | 访问密码，默认不设置。如需防止腾讯风控可设置字符串作为密码 |
|jm_ttl_seconds | 300  | 默认链接超时链接，默认300秒。              |

