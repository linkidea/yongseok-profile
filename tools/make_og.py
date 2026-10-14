#!/usr/bin/env python3
"""
OG 공유 이미지 생성 스크립트
- 카카오톡·링크드인 등 링크 공유 시 보이는 썸네일(1200x630)을 만든다.
- 실행: python tools/make_og.py   (Pillow 필요, Windows 기준 malgun 폰트 사용)
- 결과: 같은 폴더 프로젝트 루트에 og-image.png 저장
- 주의: 하단 URL이 바뀌면(커스텀 도메인 연결 등) URL 부분 수정 후 재실행할 것.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
NAVY = (22, 50, 79)
NAVY_DEEP = (15, 36, 57)
AMBER = (232, 163, 61)

FONT_REG = r"C:\Windows\Fonts\malgun.ttf"
FONT_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "og-image.png")


def font(path, size):
    return ImageFont.truetype(path, size)


def gradient():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        c = tuple(int(NAVY[i] + (NAVY_DEEP[i] - NAVY[i]) * t) for i in range(3)) + (255,)
        d.line([(0, y), (W, y)], fill=c)
    return img


def draw_bg_steps(d):
    """오른쪽의 은은한 대형 스텝 모티프 (배경 장식)"""
    steps = [
        (900, 400, (255, 255, 255, 16)),
        (970, 330, (255, 255, 255, 22)),
        (1040, 260, (255, 255, 255, 28)),
        (1110, 190, (232, 163, 61, 40)),
    ]
    for x, top, color in steps:
        d.rectangle([x, top, x + 58, H], fill=color)


def draw_logo(d, x, y, s=3):
    """사이트 로고(5단 스텝 + 앰버 화살표)를 s배 확대해 그린다."""
    bars = [
        (0, 21, 5, 5, 115),
        (7, 16, 5, 10, 153),
        (14, 11, 5, 15, 199),
        (21, 6, 5, 20, 235),
    ]
    for bx, by, bw, bh, op in bars:
        d.rectangle([x + bx * s, y + by * s, x + (bx + bw) * s, y + (by + bh) * s],
                    fill=(255, 255, 255, op))
    d.rectangle([x + 28 * s, y + 6 * s, x + 34 * s, y + 26 * s], fill=AMBER + (255,))
    d.polygon([(x + 28 * s, y + 6 * s), (x + 31 * s, y + 0.8 * s), (x + 34 * s, y + 6 * s)],
              fill=AMBER + (255,))


def main():
    img = gradient()
    d = ImageDraw.Draw(img)

    draw_bg_steps(d)

    # 로고 + 이름
    draw_logo(d, 80, 68)
    d.text((206, 82), "강용석", font=font(FONT_BOLD, 32), fill=(255, 255, 255, 245))
    d.text((206, 126), "KANG YONG-SEOK · 경영지원 & 리스크 17년",
           font=font(FONT_REG, 16), fill=(255, 255, 255, 150))

    # 헤드라인
    d.text((80, 206), "현장부터 감사까지",
           font=font(FONT_BOLD, 30), fill=AMBER + (255,))
    d.text((80, 256), "구매·PI·기획을 거쳐 온",
           font=font(FONT_BOLD, 42), fill=(255, 255, 255, 240))
    d.text((80, 316), "내부감사·리스크 전문가",
           font=font(FONT_BOLD, 58), fill=(255, 255, 255, 255))

    # 앰버 룰 + 핵심 수치
    d.rectangle([80, 420, 200, 424], fill=AMBER + (255,))
    d.text((80, 452), "RPA·AI 자동화 연 7억 절감 · 130억 프로젝트 PM · 전사 ERM 구축",
           font=font(FONT_REG, 24), fill=(255, 255, 255, 190))

    # 하단 URL
    d.text((80, 560), "linkidea.github.io/yongseok-profile",
           font=font(FONT_REG, 19), fill=(255, 255, 255, 130))

    img.convert("RGB").save(OUT, "PNG")
    print("saved:", OUT)


if __name__ == "__main__":
    main()
