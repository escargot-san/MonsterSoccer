# monster_soccer_main
妖怪サッカーの紹介サイト（13言語）。Play Console に登録するプライバシーポリシーの URL もここ（privacy.html）。

- index.html（日本語）, en.html, zh-hans.html … トップ
- privacy.html（日本語）, privacy-en.html … プライバシーポリシー
- assets/style.css, assets/img/banner-ja.webp（バナー 1024×338）

## 文章の直し方
ページは直接書きかえず、元の文章を直して作り直します。
- プライバシーポリシー：monster_soccer/docs/PRIVACY_POLICY.md（日本語・正）と docs/privacy/<言語>.md（参考訳）
- トップ：tools/site_text.py
直したら monster_soccer フォルダで `python misc/monster_soccer_main/tools/build_privacy.py` を実行すると、
全言語のページと、アプリ内（app/src/main/assets/legal/）・サーバー（/legal/privacy）の文章がまとめて作り直されます。
