"""SPA 静态托管的缓存策略（入口 no-cache / 哈希资产 immutable）。

修复"改版后浏览器一直用旧前端"：入口 index.html 无 Cache-Control 时浏览器
走启发式缓存，旧标签页/普通刷新继续拿旧入口（服务器已发新构建、浏览器仍
显示旧 UI）。哈希资产文件名即指纹，可 immutable 长缓存。
"""

from __future__ import annotations

from starlette.testclient import TestClient

from cloudra.services.api_v2.app import _SpaStaticFiles


def test_spa_static_cache_headers(tmp_path):
    (tmp_path / "assets").mkdir()
    (tmp_path / "index.html").write_text("<html>hi</html>", encoding="utf-8")
    (tmp_path / "assets" / "app-abc123.js").write_text("console.log(1)", encoding="utf-8")

    client = TestClient(_SpaStaticFiles(directory=str(tmp_path), html=True))

    r_index = client.get("/")
    assert r_index.status_code == 200
    assert r_index.headers["cache-control"] == "no-cache"

    r_asset = client.get("/assets/app-abc123.js")
    assert r_asset.status_code == 200
    assert "max-age=31536000" in r_asset.headers["cache-control"]
    assert "immutable" in r_asset.headers["cache-control"]
