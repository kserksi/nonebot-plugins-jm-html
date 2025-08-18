from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from nonebot import get_driver

from .config import Config

security = HTTPBasic()


def build_router(cache: Dict[Tuple[str, str], object]) -> APIRouter:
    """
    构建 FastAPI 路由，用于访问临时生成的 HTML 页面和图片
    """
    router = APIRouter()
    cfg = Config.parse_obj(get_driver().config)

    def _check_pwd(credentials: HTTPBasicCredentials = Depends(security)):
        """
        HTTP Basic 验证，如果未设置 jm_pwd，则放行
        """
        if not cfg.jm_pwd:
            return True
        if credentials.password != cfg.jm_pwd:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return True

    @router.get("/{uuid}/", response_class=HTMLResponse)
    async def entry(uuid: str):
        """
        根路径跳转到 index.html
        """
        return HTMLResponse('<meta http-equiv="refresh" content="0; url=./index.html"/>')

    @router.get("/{uuid}/{path:path}")
    async def serve(uuid: str, path: str, ok: bool = Depends(_check_pwd)):
        """
        访问临时资源文件（HTML 或图片）
        """
        root = Path(f"./data/jm_temp/{uuid}")
        file_path = root / (path or "index.html")
        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(status_code=404, detail="Not Found")
        return FileResponse(file_path)

    return router
