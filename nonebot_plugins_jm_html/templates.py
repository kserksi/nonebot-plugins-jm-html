from __future__ import annotations
from typing import List, Optional

BOOTSTRAP_CSS = "https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/5.3.7/css/bootstrap.min.css"
BOOTSTRAP_JS = "https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/5.3.7/js/bootstrap.min.js"


def render_album_html(
    title: str,
    authors: List[str],
    tags: List[str],
    cover: Optional[str],
    images: List[str],
) -> str:
    """
    生成移动端优化的 Bootstrap HTML 页面
    """
    authors_html = ", ".join(authors) if authors else "未知作者"
    tags_html = ", ".join(tags) if tags else "无标签"

    carousel_items = ""
    for idx, img in enumerate(images):
        active_class = "active" if idx == 0 else ""
        carousel_items += f"""
        <div class="carousel-item {active_class}">
            <img src="{img}" class="d-block w-100" alt="Page {idx+1}">
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link href="{BOOTSTRAP_CSS}" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-4">
    <h1 class="mb-2">{title}</h1>
    <p><strong>作者:</strong> {authors_html}</p>
    <p><strong>标签:</strong> {tags_html}</p>
    <div id="carouselExampleIndicators" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">
            {carousel_items}
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">上一页</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">下一页</span>
        </button>
    </div>
</div>
<script src="{BOOTSTRAP_JS}"></script>
</body>
</html>
"""
    return html
