"""Generate the original, editable illustrations for the GPU decision report."""

from html import escape
from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SCALE = 2
FONT_DIR = Path('C:/Windows/Fonts')
BG = '#F4F7FA'
INK = '#172C3D'
MUTED = '#526677'
BLUE = '#215F9B'
TEAL = '#167B71'
BORDER = '#D7E1E8'


class Drawing:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.im = Image.new('RGB', (width * SCALE, height * SCALE), BG)
        self.draw = ImageDraw.Draw(self.im)
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', f'<rect width="{width}" height="{height}" fill="{BG}"/>']

    def rect(self, x, y, w, h, fill, radius=0, outline=None, line_width=1):
        coords = tuple(round(v * SCALE) for v in (x, y, x + w, y + h))
        self.draw.rounded_rectangle(coords, radius=round(radius * SCALE), fill=fill, outline=outline, width=round(line_width * SCALE))
        stroke = f' stroke="{outline}" stroke-width="{line_width}"' if outline else ''
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"{stroke}/>')

    def text(self, x, y, text, size=28, color=INK, bold=False, align='left'):
        font = ImageFont.truetype(str(FONT_DIR / ('segoeuib.ttf' if bold else 'segoeui.ttf')), size * SCALE)
        anchor = {'left': 'lt', 'center': 'mt', 'right': 'rt'}[align]
        self.draw.text((x * SCALE, y * SCALE), text, font=font, fill=color, anchor=anchor)
        svg_anchor = {'left': 'start', 'center': 'middle', 'right': 'end'}[align]
        weight = 700 if bold else 400
        self.svg.append(f'<text x="{x}" y="{y}" dominant-baseline="text-before-edge" text-anchor="{svg_anchor}" font-family="Segoe UI, Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(text)}</text>')

    def line(self, pts, color=MUTED, width=3):
        self.draw.line([(round(x * SCALE), round(y * SCALE)) for x, y in pts], fill=color, width=width * SCALE, joint='curve')
        self.svg.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')

    def ellipse(self, x, y, w, h, fill, outline=None, width=1):
        self.draw.ellipse(tuple(round(v * SCALE) for v in (x, y, x + w, y + h)), fill=fill, outline=outline, width=width * SCALE)
        stroke = f' stroke="{outline}" stroke-width="{width}"' if outline else ''
        self.svg.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{fill}"{stroke}/>')

    def arrow(self, x1, x2, y, color=BLUE):
        self.line([(x1, y), (x2, y)], color, 4)
        self.line([(x2 - 14, y - 10), (x2, y), (x2 - 14, y + 10)], color, 4)

    def save(self, stem):
        self.im.resize((self.width, self.height), Image.Resampling.LANCZOS).save(HERE / f'{stem}.png')
        (HERE / f'{stem}.svg').write_text('\n'.join(self.svg + ['</svg>']), encoding='utf-8')


def memory():
    d = Drawing(1600, 980)
    d.text(64, 49, 'Deux mémoires, deux rôles différents', 46, bold=True)
    d.text(64, 118, 'La VRAM appartient à la carte graphique ; la RAM appartient au serveur ou au PC.', 28, MUTED)
    card_y, card_w, card_h = 196, 712, 594
    for x, label, gpu, vram, ram, color, fraction in [
        (64, 'PC ACTUEL', 'RTX 4070 Laptop', '≈ 8 Go', '32 Go', BLUE, .25),
        (824, 'SERVEUR ENVISAGÉ', 'RTX 5090', '32 Go', '32–64 Go', TEAL, 1),
    ]:
        d.rect(x, card_y, card_w, card_h, '#FFFFFF', 18, BORDER)
        d.text(x + 36, card_y + 30, label, 22, color, True)
        d.text(x + 36, card_y + 70, gpu, 38, bold=True)
        d.line([(x + 36, card_y + 136), (x + card_w - 36, card_y + 136)], BORDER, 2)
        d.text(x + 36, card_y + 168, 'VRAM · mémoire graphique', 27, bold=True)
        d.text(x + 36, card_y + 214, vram, 51, color, True)
        d.rect(x + 36, card_y + 291, 640, 28, '#E6EDF2', 6)
        d.rect(x + 36, card_y + 291, 640 * fraction, 28, color, 6)
        d.text(x + 36, card_y + 342, 'Modèles IA, images et calculs sur le GPU', 25, MUTED)
        d.line([(x + 36, card_y + 400), (x + card_w - 36, card_y + 400)], BORDER, 2)
        d.text(x + 36, card_y + 432, 'RAM · mémoire du système', 27, bold=True)
        d.text(x + 36, card_y + 478, ram, 40, bold=True)
        d.text(x + 250, card_y + 490, 'Système et applications', 23, MUTED)
    d.text(64, 827, 'Les barres comparent uniquement la capacité de VRAM : environ 4 fois plus.', 26, MUTED)
    d.rect(64, 885, 1472, 60, '#E8EEF4', 10)
    d.text(800, 898, 'Capacité mémoire ≠ qualité ou FPS garantis', 28, INK, True, 'center')
    d.save('memoire-gpu')


def webcam_icon(d, x, y):
    d.rect(x, y, 98, 58, '#EAF1F8', 12, BLUE, 3)
    d.ellipse(x + 31, y + 11, 36, 36, '#FFFFFF', BLUE, 3)
    d.ellipse(x + 42, y + 22, 14, 14, BLUE)
    d.line([(x + 49, y + 61), (x + 49, y + 76)], BLUE, 3)
    d.line([(x + 20, y + 78), (x + 78, y + 78)], BLUE, 3)


def gpu_icon(d, x, y):
    d.rect(x + 16, y + 8, 64, 64, '#E8F4F1', 8, TEAL, 3)
    d.rect(x + 32, y + 24, 32, 32, '#FFFFFF', 3, TEAL, 2)
    for i in range(4):
        n = 26 + i * 14
        d.line([(x + n, y), (x + n, y + 8)], TEAL, 3)
        d.line([(x + n, y + 72), (x + n, y + 80)], TEAL, 3)
        d.line([(x + 8, y + n - 8), (x + 16, y + n - 8)], TEAL, 3)
        d.line([(x + 80, y + n - 8), (x + 88, y + n - 8)], TEAL, 3)


def screen_icon(d, x, y):
    d.rect(x, y, 100, 64, '#EAF1F8', 7, BLUE, 3)
    d.line([(x + 50, y + 66), (x + 50, y + 81)], BLUE, 3)
    d.line([(x + 24, y + 82), (x + 76, y + 82)], BLUE, 3)
    d.ellipse(x + 40, y + 12, 20, 20, '#FFFFFF', BLUE, 2)
    d.rect(x + 31, y + 37, 38, 13, '#FFFFFF', 6, BLUE, 2)


def pipeline():
    d = Drawing(1600, 980)
    d.text(64, 49, 'Une webcam locale, un calcul distant', 46, bold=True)
    d.text(64, 118, 'Architecture envisagée : le même PC assure la capture et l’affichage.', 28, MUTED)
    y, h = 238, 440
    for x, w, number, title, color in [
        (64, 350, '1', 'PC de l’école', BLUE),
        (570, 460, '2', 'Serveur distant', TEAL),
        (1186, 350, '3', 'PC de l’école', BLUE),
    ]:
        d.rect(x, y, w, h, '#FFFFFF', 18, BORDER)
        d.ellipse(x + 28, y + 28, 36, 36, color)
        d.text(x + 46, y + 29, number, 25, '#FFFFFF', True, 'center')
        d.text(x + 82, y + 29, title, 28, bold=True)
    webcam_icon(d, 190, 343)
    gpu_icon(d, 752, 343)
    screen_icon(d, 1311, 343)
    d.text(239, 465, 'Capture webcam', 29, BLUE, True, 'center')
    d.text(239, 518, 'Envoi des images', 26, MUTED, False, 'center')
    d.text(239, 558, 'via Internet', 26, MUTED, False, 'center')
    d.text(800, 465, 'Traitement sur le GPU', 29, TEAL, True, 'center')
    d.text(800, 518, 'Détection · échange de visage', 25, MUTED, False, 'center')
    d.text(800, 558, 'Amélioration facultative', 25, MUTED, False, 'center')
    d.text(800, 598, 'Encodage du flux de retour', 25, MUTED, False, 'center')
    d.text(1361, 465, 'Images transformées', 27, BLUE, True, 'center')
    d.text(1361, 518, 'Affichage ou sortie', 25, MUTED, False, 'center')
    d.text(1361, 558, 'en webcam virtuelle', 25, MUTED, False, 'center')
    d.text(491, 352, 'Flux', 24, BLUE, False, 'center')
    d.text(491, 386, 'montant', 24, BLUE, False, 'center')
    d.arrow(436, 548, 443)
    d.text(1108, 352, 'Flux', 24, BLUE, False, 'center')
    d.text(1108, 386, 'retour', 24, BLUE, False, 'center')
    d.arrow(1052, 1164, 443)
    d.rect(64, 725, 1472, 76, '#E8EEF4', 10)
    d.text(800, 747, 'Transport vidéo et retour local à intégrer et à tester', 29, INK, True, 'center')
    d.text(64, 844, 'Délai total = capture + envoi + calcul + retour + affichage', 31, bold=True)
    d.text(64, 900, 'La puissance du GPU ne supprime pas la latence ni les contraintes du réseau.', 27, MUTED)
    d.save('chaine-webcam')


if __name__ == '__main__':
    memory()
    pipeline()
    print('Generated memoire-gpu and chaine-webcam in SVG and PNG.')
