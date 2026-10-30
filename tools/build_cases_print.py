"""케이스 5건을 한 문서로 합쳐 인쇄/PDF 저장용 cases-print.html을 만든다.

케이스 원본(case-*.html)을 수정한 뒤 이 스크립트를 다시 실행하면 통합본이 갱신된다.
    python tools/build_cases_print.py
"""
import io
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = [
    ("case-risk.html", "CASE 01", "리스크·감사"),
    ("case-diagnosis.html", "CASE 02", "감사·윤리"),
    ("case-purchase.html", "CASE 03", "구매·PI·데이터"),
    ("case-strategy.html", "CASE 04", "전략·기획"),
    ("case.html", "CASE 05", "자동화·데이터"),
]
STYLE_VERSION = "14"

LOCAL_STYLE = """
.cv-hero { padding: 40px 0 46px; }
.cv-hero h1 { font-size: clamp(22px, 3.2vw, 31px); line-height: 1.42; }
.cv-hero .sub { margin-top: 12px; font-size: 14px; max-width: 640px; text-wrap: balance; }
.case-kicker { font-size: 12px; font-weight: 700; color: var(--amber); letter-spacing: .18em; margin-bottom: 14px; }
.cv-list { list-style: none; }
.cv-list li { position: relative; padding-left: 15px; font-size: 14px; margin-bottom: 9px; line-height: 1.7; }
.cv-list li::before { content: ""; position: absolute; left: 0; top: .62em; width: 5px; height: 5px; border-radius: 50%; background: var(--amber); }
.cv-list strong { color: var(--navy); font-weight: 700; }
.case-stats { grid-template-columns: repeat(3, 1fr); }
.case-steps { margin-top: 0; }
.case-steps + .cv-list { margin-top: 24px; }
.case-note { margin-top: 26px; font-size: 13px; color: var(--muted); }
.case-note a { color: var(--navy); font-weight: 700; text-decoration: none; border-bottom: 1.5px solid var(--amber); padding-bottom: 1px; }
.home-link { color: rgba(255,255,255,.75); font-size: 13.5px; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,.3); padding-bottom: 2px; white-space: nowrap; }
.home-link:hover { color: #fff; }

.doc-toolbar { display: flex; align-items: center; justify-content: space-between; gap: 12px; max-width: 880px; margin: 0 auto; padding: 16px 28px; }
.doc-toolbar a { font-size: 13.5px; font-weight: 700; color: var(--navy); text-decoration: none; border-bottom: 1.5px solid var(--amber); padding-bottom: 2px; }
.doc-toolbar button { padding: 11px 20px; border: none; border-radius: 9px; background: var(--amber); color: var(--navy-deep); font: inherit; font-size: 14px; font-weight: 700; cursor: pointer; }
.doc-toolbar button:hover { background: var(--amber-deep); }
.doc-list { list-style: none; }
.doc-list li { display: grid; grid-template-columns: 74px 1fr; gap: 14px; padding: 11px 0; border-bottom: 1px solid var(--line); }
.doc-list li:first-child { border-top: 1px solid var(--line); }
.doc-list .no { font-size: 12px; font-weight: 800; color: var(--amber-ink); letter-spacing: .1em; padding-top: 2px; }
.doc-list strong { display: block; font-size: 14.5px; font-weight: 700; color: var(--navy); }
.doc-list span.desc { display: block; font-size: 13px; color: var(--muted); }
.case-block-head { border-top: 3px solid var(--navy); }
.doc-title { font-family: 'MaruBuri', 'Noto Serif KR', serif; font-size: clamp(20px, 2.6vw, 26px); line-height: 1.45; color: var(--navy); letter-spacing: -.01em; text-wrap: balance; }
.doc-sub { margin-top: 10px; font-size: 14px; color: var(--body-c); max-width: 640px; text-wrap: pretty; }
@media (max-width: 760px) {
  .doc-toolbar { padding: 14px 22px; }
  .doc-list li { grid-template-columns: 1fr; gap: 2px; }
}
@media print {
  @page { margin: 14mm; }
  .doc-toolbar { display: none; }
  .case-block { break-before: page; }
  .case-block-head { border-top: none; padding-bottom: 6px; }
  .doc-title { font-size: 16pt; color: #16324F; }
  .doc-sub { font-size: 10pt; color: #333; }
  .case-kicker { color: #9A6210; font-size: 9pt; }
  .cv-list li { break-inside: avoid; }
  .doc-list li { break-inside: avoid; }
}
"""

TOC_DESC = {
    "case-risk.html": "각 부서의 사후 대응을 전사 리스크 맵과 상시 모니터링으로 바꾼 3개월",
    "case-diagnosis.html": "한 건의 감사가 전사 예방 자료로 남는 방식",
    "case-purchase.html": "130억 규모 차세대 시스템, 구매 영역 PM",
    "case-strategy.html": "벤치마킹 → 전략 → 프롭테크·모바일 서비스, 누적 매출 50억 원",
    "case.html": "100% 수작업 신용평가 수집을 자동화로, 건당 5분을 3분으로",
}


def extract(filename):
    html = io.open(os.path.join(BASE, filename), encoding="utf-8").read()
    kicker = re.search(r'<p class="case-kicker">(.*?)</p>', html, re.S).group(1).strip()
    title = re.search(r"<h1>(.*?)</h1>", html, re.S).group(1).strip()
    sub = re.search(r'<p class="sub">(.*?)</p>', html, re.S).group(1).strip()
    sections = re.findall(r'<section class="section[^"]*">.*?</section>', html, re.S)
    cleaned = []
    for sec in sections:
        sec = re.sub(r'\s*<nav class="case-nav".*?</nav>', "", sec, flags=re.S)
        sec = re.sub(r'\s*<p class="case-note">.*?</p>', "", sec, flags=re.S)
        cleaned.append(sec)
    return kicker, title, sub, cleaned


def main():
    blocks = []
    toc = []
    for i, (filename, no, tag) in enumerate(CASES):
        kicker, title, sub, sections = extract(filename)
        flat_title = re.sub(r"<br\s*/?>", " ", title)
        flat_title = re.sub(r"\s+", " ", flat_title).strip()
        toc.append(
            '      <li><span class="no">%s</span><div><strong>%s</strong>'
            '<span class="desc">%s</span></div></li>' % (no, flat_title, TOC_DESC[filename])
        )
        head = (
            '  <section class="section case-block-head">\n'
            "    <div class=\"wrap\">\n"
            '      <p class="case-kicker">%s · %s</p>\n'
            '      <h2 class="doc-title">%s</h2>\n'
            '      <p class="doc-sub">%s</p>\n'
            "    </div>\n"
            "  </section>\n" % (no, tag, title, sub)
        )
        blocks.append('<div class="case-block">\n' + head + "\n".join(sections) + "\n</div>")

    html = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#16324F">
<title>케이스 스터디 5건 — 강용석</title>
<meta name="description" content="강용석 케이스 스터디 5건 통합본 — 예방형 리스크 체계, 감사 사례 분석, 전사 구매 시스템, 전략기획, 신용평가 자동화. 인쇄/PDF 저장용 문서.">
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="https://linkidea.github.io/yongseok-profile/cases-print.html">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='7' fill='%2316324F'/><rect x='6' y='22' width='4' height='4' fill='%23ffffff' opacity='.5'/><rect x='12' y='17' width='4' height='9' fill='%23ffffff' opacity='.7'/><rect x='18' y='12' width='4' height='14' fill='%23ffffff' opacity='.85'/><rect x='24' y='7' width='4' height='19' fill='%23E8A33D'/></svg>">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="style.css?v=__V__">
<style>__STYLE__</style>
</head>
<body>

<div class="doc-toolbar">
  <a href="cases.html">← 케이스 목록으로</a>
  <button type="button" onclick="window.print()">인쇄 / PDF 저장</button>
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
          <strong>강용석</strong>
          <span>KANG YONG-SEOK</span>
        </div>
      </div>
      <div class="hero-links">
        <a class="home-link" href="index.html">← 프로필 홈</a>
        <a class="home-link" href="career.html">← 경력 상세</a>
        <a class="home-link" href="cases.html">← 케이스 전체</a>
      </div>
    </div>
    <p class="case-kicker">CASE STUDIES · 5건</p>
    <h1>케이스 스터디 5건</h1>
    <p class="sub">강용석 — 내부감사·리스크 관리 파트리더. 문제 → 접근 → 결과 → 시사점 순서로 정리했습니다.</p>
    <p class="print-contact">fwipace@naver.com · linkedin.com/in/yongseok-kang · linkidea.github.io/yongseok-profile</p>
  </div>
</header>

<section class="section">
  <div class="wrap">
    <h2 class="label"><span class="no">목차</span><span class="tx">CASE STUDIES</span></h2>
    <ol class="doc-list">
__TOC__
    </ol>
    <p class="case-note">각 케이스는 새 페이지에서 시작합니다. 이 문서는 인쇄/PDF 저장용이며, 화면용 목록은 <a href="cases.html">케이스 스터디</a>에서 볼 수 있습니다.</p>
  </div>
</section>

__BLOCKS__

<footer class="footer">
  <div class="wrap">강용석 · 내부감사·리스크 · 2026 · <a href="cases.html">케이스 전체</a> · <a href="career.html">경력 상세</a></div>
</footer>

</body>
</html>
"""
    html = (html.replace("__V__", STYLE_VERSION)
                 .replace("__STYLE__", LOCAL_STYLE)
                 .replace("__TOC__", "\n".join(toc))
                 .replace("__BLOCKS__", "\n\n".join(blocks)))

    out = os.path.join(BASE, "cases-print.html")
    io.open(out, "w", encoding="utf-8", newline="\n").write(html)
    print("written:", out, "cases:", len(blocks))


if __name__ == "__main__":
    main()
