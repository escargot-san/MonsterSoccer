#!/usr/bin/env python3
"""紹介サイトとプライバシーポリシーを全言語まとめて作り直す。

  使い方（monster_soccer フォルダで）: python misc/monster_soccer_main/tools/build_privacy.py

元の文章:
  docs/PRIVACY_POLICY.md          プライバシーポリシー（日本語・正）
  docs/privacy/<言語>.md           その翻訳（参考訳。日本語版を直したら翻訳も直す）
  tools/site_text.py              トップページの文章（言語ごと）
作るもの:
  misc/monster_soccer_main/index.html, <言語>.html                  トップ
  misc/monster_soccer_main/privacy.html, privacy-<言語>.html        プライバシーポリシー（Play Console には privacy.html）
  server/src/main/resources/legal/privacy.txt                       サーバーの /legal/privacy（日本語）
  app/src/main/assets/legal/privacy.txt, privacy_<言語>.txt          アプリの「サポート」→「プライバシーポリシー」
"""
import html, re, sys
from pathlib import Path

site = Path(__file__).resolve().parents[1]
root = site.parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_text import LANGS, DEFAULT, T

def page_name(kind, suffix):
    if kind == "index": return f"{suffix}.html" if suffix else "index.html"
    return f"privacy-{suffix}.html" if suffix else "privacy.html"

def link(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"(https://[^\s）)]+)", r'<a href="\1">\1</a>', s)
    return re.sub(r"([\w.]+@[\w.]+\.\w+)", r'<a href="mailto:\1">\1</a>', s)

GLOBE = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'

def head(lang, kind, title, desc=""):
    alts = "\n".join(f'<link rel="alternate" hreflang="{l[3]}" href="{page_name(kind, l[1])}">' for l in LANGS)
    d = next(l for l in LANGS if l[0] == DEFAULT)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{page_name(kind, d[1])}">'
    meta = ""
    if desc:
        t = T[lang[0]]
        meta = (f'<meta name="description" content="{html.escape(desc)}">\n<meta property="og:title" content="{html.escape(t["name"])}">\n'
                f'<meta property="og:description" content="{html.escape(desc)}">\n<meta property="og:image" content="assets/img/banner-ja.webp">\n<meta property="og:type" content="website">\n')
    return f"""<!doctype html>
<html lang="{lang[3]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
{meta}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;800&family=Noto+Sans+KR:wght@400;700&family=Noto+Sans+SC:wght@400;700&family=Noto+Sans+TC:wght@400;700&family=Noto+Sans+Thai:wght@400;700&display=swap" rel="stylesheet">
{alts}
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
"""

def lang_menu(cur, kind):
    current = ' aria-current="page"'
    items = "\n".join(
        f'        <li><a href="{page_name(kind, l[1])}" lang="{l[3]}" hreflang="{l[3]}"{current if l == cur else ""}>{l[2]}</a></li>'
        for l in LANGS)
    return f"""    <details class="lang-menu">
      <summary>{GLOBE} {cur[2]}</summary>
      <ul>
{items}
      </ul>
    </details>"""

def header(cur, kind, nav):
    t = T[cur[0]]
    home = page_name("index", cur[1])
    return f"""<header class="site-header">
  <div class="inner">
    <a class="brand" href="{home if kind != 'index' else '#top'}"><span class="brand-mark">⚽</span>{html.escape(t['name'])}</a>
    <nav class="site-nav">
{nav}
    </nav>
{lang_menu(cur, kind)}
  </div>
</header>
"""

def footer(cur):
    t = T[cur[0]]
    langs = "".join(f'<a href="{page_name("privacy", l[1])}" lang="{l[3]}">{l[2]}</a>' for l in LANGS)
    return f"""<footer class="site-footer">
  <p style="margin:0"><a href="{page_name('index', cur[1])}">{html.escape(t['top'])}</a><a href="{page_name('privacy', cur[1])}">{html.escape(t['privacy'])}</a></p>
  <div class="footer-langs">{''.join(f'<a href="{page_name("index", l[1])}" lang="{l[3]}">{l[2]}</a>' for l in LANGS)}</div>
  <p style="margin:8px 0 0">© 2026 {html.escape(t['name'])}</p>
</footer>
</body>
</html>
"""

def card(title, body):
    b = ("<ul>" + "".join(f"<li>{html.escape(x)}</li>" for x in body) + "</ul>") if isinstance(body, list) else f"<p>{html.escape(body)}</p>"
    return f'      <div class="card"><h3>{html.escape(title)}</h3>{b}</div>'

def index_page(cur):
    t = T[cur[0]]; e = lambda s: html.escape(s)
    colon = "：" if cur[0] in ("ja", "zh-Hans", "zh-Hant") else ": "
    priv = page_name("privacy", cur[1])
    ids = ["about", "features", "purchase", "creator", "support"]
    nav = "\n".join(f'      <a href="#{i}">{e(n)}</a>' for i, n in zip(ids, t["nav"])) + f'\n      <a class="keep" href="{priv}">{e(t["nav"][5])}</a>'
    creator2 = e(t["creator"][1]).replace("{privacy}", f'<a href="{priv}">{e(t["privacy"])}</a>')
    return head(cur, "index", f'{t["name"]} | {t["tagline"]}', t["desc"]) + header(cur, "index", nav) + f"""
<div class="hero" id="top">
  <img src="assets/img/banner-ja.webp" width="1024" height="338" alt="{e(t['alt'])}">
</div>

<main>
  <section id="about">
    <span class="eyebrow">ABOUT</span>
    <h2>{e(t['about_h'])}</h2>
    <div class="lead">
      <p><strong>{e(t['about'][0])}</strong></p>
      <p style="margin:0">{e(t['about'][1])}</p>
    </div>
  </section>

  <section id="features">
    <span class="eyebrow">FEATURES</span>
    <h2>{e(t['features_h'])}</h2>
    <div class="cards">
{chr(10).join(card(a, b) for a, b in t['features'])}
    </div>
  </section>

  <section id="purchase">
    <span class="eyebrow">PURCHASE</span>
    <h2>{e(t['purchase_h'])}</h2>
    <div class="cards">
{chr(10).join(card(a, b) for a, b in t['purchase'])}
    </div>
    <p class="note">{e(t['purchase_note'])}</p>
  </section>

  <section id="creator">
    <span class="eyebrow">CREATOR</span>
    <h2>{e(t['creator_h'])}</h2>
    <div class="lead">
      <p>{e(t['creator'][0])}</p>
      <p style="margin:0">{creator2}</p>
    </div>
  </section>

  <section id="support">
    <span class="eyebrow">SUPPORT</span>
    <h2>{e(t['support_h'])}</h2>
    <div class="lead">
      <p>{e(t['support'])}</p>
      <p style="margin:0">{e(t['dev'])}{colon}@さん<br>{e(t['mail'])}{colon}<a href="mailto:escargot.san@gmail.com">escargot.san@gmail.com</a></p>
    </div>
  </section>
</main>

""" + footer(cur)

def read_policy(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    title = next(l[2:] for l in lines if l.startswith("# "))
    updated = [l for l in lines if l.strip()][-1]
    out, txt, in_list = [], [], False
    for line in lines:
        if not line.startswith("- ") and in_list: out.append("</ul>"); in_list = False
        if line.startswith("# ") or line == updated: continue
        if line.startswith("## "):
            out.append(f"<h2>{html.escape(line[3:])}</h2>"); txt += ["", line[3:]]
        elif line.startswith("### "):
            out.append(f"<h3>{html.escape(line[4:])}</h3>"); txt.append(f"【{line[4:]}】")
        elif line.startswith("- "):
            if not in_list: out.append("<ul>"); in_list = True
            out.append(f"  <li>{link(line[2:])}</li>"); txt.append("・" + line[2:])
        elif line.strip():
            out.append(f"<p>{link(line)}</p>"); txt.append(line)
    if in_list: out.append("</ul>")
    txt += ["", updated]
    return title, updated, "\n".join(out), "\n".join(txt).strip() + "\n"

def privacy_page(cur, title, updated, body):
    t = T[cur[0]]
    nav = f'      <a class="keep" href="{page_name("index", cur[1])}">{html.escape(t["back"])}</a>'
    return head(cur, "privacy", f'{title} | {t["name"]}') + header(cur, "privacy", nav) + f"""<main>
<article class="doc">
<h1>{html.escape(title)}</h1>
<p class="updated">{html.escape(updated)}</p>
<!-- tools/build_privacy.py が docs/PRIVACY_POLICY.md と docs/privacy/ から作っています。直接書きかえないでください。 -->
{body}
</article>
</main>
""" + footer(cur)

for cur in LANGS:
    code = cur[0]
    src = root / "docs/PRIVACY_POLICY.md" if code == "ja" else root / f"docs/privacy/{code}.md"
    title, updated, body, plain = read_policy(src)
    (site / page_name("privacy", cur[1])).write_text(privacy_page(cur, title, updated, body), encoding="utf-8")
    (site / page_name("index", cur[1])).write_text(index_page(cur), encoding="utf-8")
    app = root / "app/src/main/assets/legal" / ("privacy.txt" if code == "ja" else f"privacy_{code}.txt")
    app.parent.mkdir(parents=True, exist_ok=True); app.write_text(plain, encoding="utf-8")
    if code == "ja":
        p = root / "server/src/main/resources/legal/privacy.txt"; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(plain, encoding="utf-8")
print("ok", len(LANGS))
