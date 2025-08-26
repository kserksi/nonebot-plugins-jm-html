from __future__ import annotations

import asyncio
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple
from uuid import uuid4

from nonebot import get_driver

from .fetcher import fetch_album
from .templates import render_album_html
from .routers import build_router
from .config import plugin_config

@dataclass
class CacheEntry:
    uuid: str
    album_id: str
    user_id: str
    root_dir: Path
    expire_at: float

# key = (user_id, album_id)
_CACHE: Dict[Tuple[str, str], CacheEntry] = {}

# 临时资源基础目录
BASE_DIR = Path("./data/jm_temp")
BASE_DIR.mkdir(parents=True, exist_ok=True)

_router_registered = False

def _register_router_once() -> None:
    """在 NoneBot FastAPI 应用中注册路由，只注册一次"""
    global _router_registered
    if _router_registered:
        return
    app = get_driver().server_app  # FastAPI app
    router = build_router(_CACHE)
    app.include_router(router, prefix="/jm", tags=["jm_html"])
    _router_registered = True


def get_existing_link(user_id: str, album_id: str) -> str | None:
    """
    检查缓存中是否存在有效资源链接
    """
    key = (user_id, album_id)
    entry = _CACHE.get(key)
    if not entry:
        return None
    if time.time() >= entry.expire_at:
        # 过期即清理
        try:
            shutil.rmtree(entry.root_dir, ignore_errors=True)
        finally:
            _CACHE.pop(key, None)
        return None
    return f"/jm/{entry.uuid}/index.html"


async def ensure_album_ready(
    user_id: str,
    album_id: str,
    jm_pwd: str | None,
    ttl_seconds: int = 300,
) -> str:
    """
    确保指定用户和本子ID的 HTML 资源已生成
    返回 /jm/{uuid}/index.html 链接
    """
    _register_router_once()

    # 先检查缓存
    existing = get_existing_link(user_id, album_id)
    if existing:
        return existing

    # 1️⃣ 创建临时目录
    uid = uuid4().hex
    root = BASE_DIR / uid
    img_dir = root / "images"
    root.mkdir(parents=True, exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)

    # 2️⃣ 下载漫画
    album, image_rel_paths = fetch_album(album_id, img_dir)

    # 3️⃣ 生成 HTML
    html = render_album_html(
        title=album.title,
        authors=getattr(album, "authors", []),
        tags=getattr(album, "tags", []),
        cover=image_rel_paths[0] if image_rel_paths else None,
        images=image_rel_paths,
    )
    (root / "index.html").write_text(html, encoding="utf-8")

    # 4️⃣ 写入缓存
    expire_at = time.time() + ttl_seconds
    entry = CacheEntry(uuid=uid, album_id=str(album_id), user_id=user_id, root_dir=root, expire_at=expire_at)
    _CACHE[(user_id, str(album_id))] = entry

    # 5️⃣ 异步清理
    asyncio.create_task(_reaper(entry))

    return f"/jm/{uid}/index.html"


async def _reaper(entry: CacheEntry) -> None:
    """
    等待资源到期并自动清理
    """
    now = time.time()
    delay = max(0.0, entry.expire_at - now)
    await asyncio.sleep(delay)

    try:
        shutil.rmtree(entry.root_dir, ignore_errors=True)
    finally:
        _CACHE.pop((entry.user_id, entry.album_id), None)
