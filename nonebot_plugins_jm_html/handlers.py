from __future__ import annotations

import asyncio
from nonebot import get_driver
from nonebot.adapters import Bot, Event
from nonebot.exception import FinishedException
from nonebot.matcher import current_bot, current_event

from .service import get_existing_link, ensure_album_ready
from .config import plugin_config

# 读取全局配置
_cfg: Config = Config.parse_obj(get_driver().config)


async def handle_jm(album_id: str) -> None:
    """
    核心处理函数：
    1. 检查缓存，看是否已有可用链接
    2. 如果没有，下载漫画并生成 HTML 页面
    3. 发送给用户最终链接
    """
    # 获取当前 bot 和 event
    bot: Bot = current_bot.get()
    event: Event = current_event.get()
    user_id = event.get_user_id()

    # 1️⃣ 缓存命中
    link = get_existing_link(user_id=user_id, album_id=album_id)
    if link:
        await bot.send(event, f"已存在可用链接：{link}")
        raise FinishedException

    # 2️⃣ 生成资源
    try:
        link = await ensure_album_ready(
            user_id=user_id,
            album_id=album_id,
            jm_pwd=_cfg.jm_pwd,
            ttl_seconds=_cfg.jm_ttl_seconds,
        )
        await bot.send(event, f"生成成功：{link}")
    except Exception as e:
        await bot.send(event, f"处理失败：{e}")
        raise FinishedException
