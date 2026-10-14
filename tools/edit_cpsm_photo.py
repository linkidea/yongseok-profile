#!/usr/bin/env python3
"""
CPSM 자격증 이미지 웹용 가공 스크립트
- 원본: 사용자가 제공한 2019년 발급 CPSM 증서 스크린샷 (Downloads)
- 처리: 하단 좌측 '등록번호/발급일/만료일' 블록을 배경색으로 제거 (만료일 2022 노출 방지)
- 출력: 프로젝트 루트 cpsm-certificate.jpg
- 주의: 2025년 갱신 완료(사용자 확인). 갱신 증서를 입수하면 이 이미지를 교체할 것.
- 재실행: python tools/edit_cpsm_photo.py
"""
import os
from PIL import Image, ImageDraw, ImageStat

SRC = r"C:\Users\CloudK\Downloads\스크린샷_14-10-2026_174512_.jpeg"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "cpsm-certificate.jpg")

img = Image.open(SRC).convert("RGB")
print("original:", img.size)
W, H = img.size

# 배경색 샘플: 날짜 블록 바로 위 여백 (인장/테두리 피해서 좌측 1/3 구간)
strip = img.crop((int(W * 0.08), int(H * 0.74), int(W * 0.38), int(H * 0.78)))
bg = tuple(int(v) for v in ImageStat.Stat(strip).median)
print("bg sampled:", bg)

# 날짜·등록번호 블록 제거 (좌측 하단 — 인장(x≈0.45W~)과 테두리를 침범하지 않도록 범위 제한)
box = (int(W * 0.06), int(H * 0.80), int(W * 0.40), int(H * 0.955))
ImageDraw.Draw(img).rectangle(box, fill=bg)

img.save(OUT, "JPEG", quality=88, optimize=True)
print("saved:", OUT, os.path.getsize(OUT) // 1024, "KB")
