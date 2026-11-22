#!/usr/bin/env python3
"""プライバシーポリシーを1か所（docs/PRIVACY_POLICY.md）から作り直す。

  使い方（monster_soccer フォルダで）: python misc/monster_soccer_main/tools/build_privacy.py

作るもの:
  misc/monster_soccer_main/privacy.html              公開サイト（Play Console に登録する URL）
  server/src/main/resources/legal/privacy.txt         サーバーの /legal/privacy
  app/src/main/assets/legal/privacy.txt               アプリの「サポート」→「プライバシーポリシー」
"""
import html, re, sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
md = (root / "docs/PRIVACY_POLICY.md").read_text(encoding="utf-8").splitlines()

def link(s):
    s = html.escape(s)
    s = re.sub(r"(https://[^\s）)]+)", r'<a href="\1">\1</a>', s)
    return re.sub(r"([\w.]+@[\w.]+\.\w+)", r'<a href="mailto:\1">\1</a>', s)

out, txt, in_list, updated = [], [], False, ""
for line in md:
    if line.startswith("制定日："): updated = line
    if not line.startswith("- ") and in_list: out.append("</ul>"); in_list = False
    if line.startswith("# "): continue
    elif line.startswith("## "):
        out.append(f"<h2>{html.escape(line[3:])}</h2>"); txt += ["", line[3:]]
    elif line.startswith("### "):
        out.append(f"<h3>{html.escape(line[4:])}</h3>"); txt.append(f"【{line[4:]}】")
    elif line.startswith("- "):
        if not in_list: out.append("<ul>"); in_list = True
        out.append(f"  <li>{link(line[2:])}</li>"); txt.append("・" + line[2:])
    elif line.strip():
        if line is not updated: out.append(f"<p>{link(line)}</p>")
        txt.append(line)
if in_list: out.append("</ul>")

body = "\n".join(out)
page = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>プライバシーポリシー | 妖怪サッカー</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="site-header">
  <div class="inner">
    <a class="brand" href="index.html"><span class="brand-mark">⚽</span>妖怪サッカー</a>
    <nav class="site-nav" style="display:flex"><a class="keep" href="index.html">トップへ戻る</a></nav>
  </div>
</header>
<main>
<article class="doc">
<h1>プライバシーポリシー</h1>
<p class="updated">{html.escape(updated)}</p>
<!-- tools/build_privacy.py が docs/PRIVACY_POLICY.md から作っています。直接書きかえないでください。 -->
{body}
</article>
</main>
<footer class="site-footer"><p style="margin:0"><a href="index.html">トップ</a><a href="privacy.html">プライバシーポリシー</a></p><p style="margin:8px 0 0">© 2026 妖怪サッカー</p></footer>
</body>
</html>
"""
site = Path(__file__).resolve().parents[1]
(site / "privacy.html").write_text(page, encoding="utf-8")
plain = "\n".join(txt).strip() + "\n"
for p in [root / "server/src/main/resources/legal/privacy.txt", root / "app/src/main/assets/legal/privacy.txt"]:
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(plain, encoding="utf-8")
print("ok")
