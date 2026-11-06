"""영문 케이스 5건을 한 문서로 합쳐 en-cases-print.html을 만든다.

영문 케이스 원본(en-case-*.html)을 수정한 뒤 이 스크립트를 다시 실행한다.
    python tools/build_cases_print_en.py
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_cases_print import BASE, LOCAL_STYLE, extract  # noqa: E402

STYLE_VERSION = "16"

CASES = [
    ("en-case-risk.html", "CASE 01", "Risk · Audit"),
    ("en-case-diagnosis.html", "CASE 02", "Audit · Ethics"),
    ("en-case-purchase.html", "CASE 03", "Purchasing · PI · Data"),
    ("en-case-strategy.html", "CASE 04", "Strategy"),
    ("en-case.html", "CASE 05", "Automation · Data"),
]

TOC_DESC = {
    "en-case-risk.html": "Turning after-the-fact response into an enterprise risk map and always-on monitoring, in three months",
    "en-case-diagnosis.html": "How one audit becomes prevention material for every division",
    "en-case-purchase.html": "KRW 13B next-generation system, purchasing workstream PM",
    "en-case-strategy.html": "Benchmarking → strategy → proptech and mobile services, KRW 5B cumulative revenue",
    "en-case.html": "100% manual credit data collection automated, five minutes to three per case",
}

DOC = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#16324F">
<title>Case studies — 5 cases | Yong-seok Kang</title>
<meta name="description" content="Five case studies by Yong-seok Kang in one document — preventive risk framework, audit case analysis, enterprise purchasing system, strategy planning, credit assessment automation. For print and PDF.">
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="https://linkidea.github.io/yongseok-profile/en-cases-print.html">
<link rel="alternate" hreflang="ko" href="https://linkidea.github.io/yongseok-profile/cases-print.html">
<link rel="alternate" hreflang="en" href="https://linkidea.github.io/yongseok-profile/en-cases-print.html">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='7' fill='%2316324F'/><rect x='6' y='22' width='4' height='4' fill='%23ffffff' opacity='.5'/><rect x='12' y='17' width='4' height='9' fill='%23ffffff' opacity='.7'/><rect x='18' y='12' width='4' height='14' fill='%23ffffff' opacity='.85'/><rect x='24' y='7' width='4' height='19' fill='%23E8A33D'/></svg>">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="style.css?v=__V__">
<style>__STYLE__</style>
</head>
<body>

<div class="doc-toolbar">
  <a href="en-cases.html">← Back to case studies</a>
  <button type="button" onclick="window.print()">Print / Save as PDF</button>
</div>

<header class="hero cv-hero">
  <div class="wrap">
    <div class="brand">
      <div class="brand-left">
        <svg width="34" height="26" viewBox="0 0 34 26" aria-hidden="true">
          <rect x="0" y="21" width="5" height="5" fill="rgba(255,255,255,.45)"/>
          <rect x="7" y="16" width="5" height="10" fill="rgba(255,255,255,.6)"/>
          <rect x="14" y="11" width="5" height="15" fill="rgba(255,255,255,.78)"/>
          <rect x="21" y="6" width="5" height="20" fill="rgba(255,255,255,.92)"/>
          <path d="M28 6 L31 .8 L34 6 Z" fill="#E8A33D"/>
          <rect x="28" y="6" width="6" height="20" fill="#E8A33D"/>
        </svg>
        <div class="brand-text">
          <strong>Yong-seok Kang</strong>
          <span>강용석</span>
        </div>
      </div>
      <div class="hero-links">
        <a class="home-link" href="en.html">← Home</a>
        <a class="home-link" href="en-career.html">← Career</a>
        <a class="home-link" href="en-cases.html">← All cases</a>
      </div>
    </div>
    <p class="case-kicker">CASE STUDIES · 5</p>
    <h1>Case studies</h1>
    <p class="sub">Yong-seok Kang — Part Leader, Diagnosis &amp; Audit. Problem → approach → result → takeaway.</p>
    <p class="print-contact">fwipace@naver.com · linkedin.com/in/yongseok-kang · linkidea.github.io/yongseok-profile</p>
  </div>
</header>

<section class="section">
  <div class="wrap">
    <h2 class="label"><span class="no">CONTENTS</span><span class="tx">FIVE CASES</span></h2>
    <ol class="doc-list">
__TOC__
    </ol>
    <p class="case-note">Each case starts on a new page. This document is for printing or saving as PDF; the on-screen index is <a href="en-cases.html">here</a>.</p>
  </div>
</section>

__BLOCKS__

<footer class="footer">
  <div class="wrap">Yong-seok Kang · Internal Audit &amp; Risk · 2026 · <a href="en-cases.html">All cases</a> · <a href="en-career.html">Career</a></div>
</footer>

</body>
</html>
"""


def main():
    toc, blocks = [], []
    for filename, no, tag in CASES:
        _kicker, title, sub, sections = extract(filename)
        flat = re.sub(r"<br\s*/?>", " ", title)
        flat = re.sub(r"\s+", " ", flat).strip()
        toc.append(
            '      <li><span class="no">%s</span><div><strong>%s</strong>'
            '<span class="desc">%s</span></div></li>' % (no, flat, TOC_DESC[filename])
        )
        head = (
            '  <section class="section case-block-head">\n'
            '    <div class="wrap">\n'
            '      <p class="case-kicker">%s · %s</p>\n'
            '      <h2 class="doc-title">%s</h2>\n'
            '      <p class="doc-sub">%s</p>\n'
            "    </div>\n"
            "  </section>\n" % (no, tag, title, sub)
        )
        blocks.append('<div class="case-block">\n' + head + "\n".join(sections) + "\n</div>")

    html = (DOC.replace("__V__", STYLE_VERSION)
               .replace("__STYLE__", LOCAL_STYLE)
               .replace("__TOC__", "\n".join(toc))
               .replace("__BLOCKS__", "\n\n".join(blocks)))
    out = os.path.join(BASE, "en-cases-print.html")
    io.open(out, "w", encoding="utf-8", newline="\n").write(html)
    print("written:", out, "cases:", len(blocks))


if __name__ == "__main__":
    main()
