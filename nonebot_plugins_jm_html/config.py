from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, Extra


class Config(BaseSettings,extra=Extra.ignore):
    """
    NoneBot 插件配置
    """

    # 可选网页访问密码
    jm_pwd: str | None = Field(default=None, env="JM_PWD")

    # 临时缓存存活时间，单位秒，默认 300 秒（5 分钟）
    jm_ttl_seconds: int = Field(default=300, env="JM_TTL_SECONDS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 全局实例，其他模块可直接导入使用
plugin_config: Config = Config()
