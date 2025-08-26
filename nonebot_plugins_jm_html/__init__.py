from __future__ import annotations

from nonebot import get_driver, on_command
from nonebot.adapters import Event, Bot
from nonebot.typing import T_State
from nonebot.params import ArgPlainText
from nonebot.plugin import PluginMetadata
from nonebot.exception import FinishedException
from nonebot.matcher import current_bot, current_event

from .config import Config
from .handlers import handle_jm

__plugin_meta__ = PluginMetadata(
    name="jm_html",
    description="Download JM album and generate a mobile-first Bootstrap HTML gallery with temp cache & password",
    usage="/jm <album_id>",
    type="application",
    homepage="https://github.com/yourname/nonebot-plugin-jm-html",
)

# 从 Driver 配置读取插件配置
plugin_config: Config = Config.parse_obj(get_driver().config)

# 注册 /jm 命令
cmd_jm = on_command("jm", priority=5, block=True)

@cmd_jm.handle()
async def _(state: T_State, event: Event):
    """
    命令入口：如果用户直接跟在 /jm 后面发送本子ID，则直接放入 state
    """
    text = str(event.get_message()).strip()
    if text:
        state["album_id"] = text

@cmd_jm.got("album_id", prompt="请发送要获取的 JM album_id（数字）")
async def _(album_id: str = ArgPlainText("album_id")):
    """
    获取 album_id 后委托给 handlers 处理
    """
    try:
        await handle_jm(album_id=album_id)
    except FinishedException:
        # 已处理完成，不再抛出
        pass
