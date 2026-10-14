#!/usr/bin/env python3
"""
프로필 사진 웹용 가공 스크립트
- 원본: 사용자 제공 증명사진 (Desktop/증명사진(프로필).jpg)
- 처리: 웹용 리사이즈 (최대 너비 600px)
- 출력: 프로젝트 루트 profile.jpg
- 재실행: python tools/edit_profile_photo.py
"""
import os
from PIL import Image

SRC = r"C:\Users\CloudK\Desktop\증명사진(프로필).jpg"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "profile.jpg")

img = Image.open(SRC).convert("RGB")
print("original:", img.size)

MAXW = 600
if img.width > MAXW:
    h = round(img.height * MAXW / img.width)
    img = img.resize((MAXW, h), Image.LANCZOS)

img.save(OUT, "JPEG", quality=88, optimize=True)
print("saved:", OUT, os.path.getsize(OUT) // 1024, "KB")
