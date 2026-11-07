"""Build dependency-free, standalone HTML. python3 tools/build.py"""
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parent.parent
VERSION='1.1.0'
config=json.loads((ROOT/'src/data.json').read_text())
css=(ROOT/'src/dashboard.css').read_text()
js=(ROOT/'src/dashboard.js').read_text()
for kind,c in config.items():
    data=json.dumps(c['data'],ensure_ascii=False).replace('</','<\\/')
    html=f'''<!doctype html>
<!-- Jane’s Picks · MIT · Copyright (c) 2026 Jane / Dante Labs -->
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{c['title']} · 제인의 픽</title><style>{css}</style></head>
<body><a class="skip" href="#main">본문 바로가기</a>
<header class="topbar"><div class="brand"><span class="brandmark" aria-hidden="true">J.</span><span>JANE’S PICKS<small>INTERACTIVE DASHBOARDS</small></span></div><div class="top-actions"><span class="demo-badge">가상 데이터 · v{VERSION}</span><button id="motion" class="icon-button" aria-pressed="false">모션 끄기</button><button id="help" class="icon-button" aria-label="컴포넌트와 활용법 보기">? <span>활용법</span></button></div></header>
<main id="main"><div class="page-heading"><div><p class="eyebrow">WORKSPACE / {c['en']}</p><h1>{c['title']}<span class="live-dot" aria-hidden="true"></span></h1><p class="intro">{c['intro']}</p></div><div class="edition">BLUE EDITION<span>클릭하며 살펴보는 UI 레퍼런스</span></div></div>
<section class="filterbar" aria-label="대시보드 필터"><div id="filters"></div><button id="reset" class="reset">↺ 필터 초기화</button></section>
<div class="statusline"><p id="status" role="status" aria-live="polite"></p><span>조회용 예제 · 실제 저장 없음</span></div>
<section id="stats" class="stats" aria-label="핵심 지표"></section>
<div id="workspace"></div>
<details class="scope"><summary>데이터 기준과 예제의 범위</summary><p>{c['note']}</p><p>모든 지표·차트·목록에는 같은 필터가 적용됩니다. 실제 데이터 연결·로그인·서버 저장은 포함하지 않습니다. 검색·필터·정렬은 새로고침하면 초기화됩니다.</p><p>단일 HTML에 스타일과 스크립트가 포함되어 있어 외부 설치나 네트워크 없이 열립니다. DATA 배열을 교체할 때 집계 기준도 함께 검토하세요.</p></details>
</main><footer><strong>제인의 픽</strong><span>Jane / Dante Labs · 자체 제작 · MIT</span><span>BLUE EDITION / {VERSION}</span></footer>
<dialog id="detail" aria-labelledby="detail-title"><div class="dialog-head"><span class="eyebrow">DETAIL VIEW</span><button class="close" aria-label="상세 닫기">✕</button></div><div id="detail-body"></div><button class="close bottom-close">확인하고 닫기</button></dialog>
<dialog id="help-dialog" aria-labelledby="help-title"><div class="dialog-head"><span class="eyebrow">DESIGN NOTES</span><button class="close" aria-label="활용법 닫기">✕</button></div><h2 id="help-title">이 화면에서 체험하는 UI</h2><div id="help-body"></div><p class="muted">애니메이션은 상태가 바뀐 위치를 알려주는 용도입니다. 시스템의 ‘움직임 줄이기’를 따르며 상단에서 직접 끌 수도 있습니다.</p><button class="close bottom-close">확인하고 닫기</button></dialog>
<div id="toast" class="toast" role="status" aria-live="polite"></div>
<script>const KIND={json.dumps(kind)};\n// 가상 예시 데이터. 실제 데이터 연결 시 집계 기준을 검토하세요.\nconst DATA={data};\n{js}</script></body></html>'''
    (ROOT/'templates'/f'{kind}.html').write_text(html)
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'templates').glob('*.html'))}
(ROOT/'manifest.json').write_text(json.dumps({'version':VERSION,'sha256':manifest},indent=2)+'\n')
print(json.dumps(manifest,indent=2))
