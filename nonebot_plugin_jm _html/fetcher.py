from __future__ import annotations

from pathlib import Path
from typing import List

from jmcomic import JMComic  # 确保安装 jmcomic>=3.6


@dataclass
class Album:
    title: str
    authors: list[str]
    tags: list[str]


def fetch_album(album_id: str, dest_dir: Path) -> tuple[Album, List[str]]:
    """
    下载 JM album，并保存图片到 dest_dir

    返回:
        Album: 漫画元信息
        List[str]: 图片相对路径列表
    """
    dest_dir.mkdir(parents=True, exist_ok=True)

    client = JMComic()
    comic = client.get_album(album_id)  # 获取漫画信息

    # 下载所有页到 dest_dir
    image_paths: list[str] = []
    for idx, page in enumerate(comic.pages, start=1):
        img_path = dest_dir / f"{idx:03d}.{page.ext or 'jpg'}"
        if not img_path.exists():
            page.save(img_path)
        image_paths.append(f"images/{img_path.name}")  # 相对路径，用于 HTML

    album = Album(
        title=comic.title,
        authors=comic.authors or [],
        tags=comic.tags or [],
    )
    return album, image_paths
