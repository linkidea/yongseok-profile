#!/usr/bin/env python3
"""
수상 사진 웹용 가공 스크립트
- 원본: 사용자가 제공한 시상식 사진 (PNG)
- 처리: 웹용 리사이즈(최대 1200px) + 오른쪽 시상자 얼굴 은은한 블러
- 출력: 프로젝트 루트 awards-2022.jpg
- 재실행: 원본 경로(SRC) 확인 후 python tools/edit_award_photo.py
- 주의: 원본 사진은 사용자 보관(Desktop/Downloads) — 이 폴더에는 가공본만 둔다.
"""
import os
from PIL import Image, ImageDraw, ImageFilter

SRC = r"C:\Users\CloudK\Downloads\개별사진(코어비전)_편집.png"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "awards-2022.jpg")

img = Image.open(SRC).convert("RGB")
print("original:", img.size)

MAXW = 1200
if img.width > MAXW:
    h = round(img.height * MAXW / img.width)
    img = img.resize((MAXW, h), Image.LANCZOS)
W, H = img.size
print("resized:", img.size)

# 오른쪽 시상자 머리 영역 블러 (비율 기준, 페더 처리)
cx, cy = 0.545 * W, 0.49 * H
rx, ry = 0.055 * W, 0.065 * H
blurred = img.filter(ImageFilter.GaussianBlur(12))
mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(mask).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(10))
img = Image.composite(blurred, img, mask)

img.save(OUT, "JPEG", quality=85, optimize=True)
print("saved:", OUT, os.path.getsize(OUT) // 1024, "KB")
