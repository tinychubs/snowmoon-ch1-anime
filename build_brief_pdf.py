# -*- coding: utf-8 -*-
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                PageBreak, Table, TableStyle, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

JP_FONT = os.environ.get('JP_FONT', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
pdfmetrics.registerFont(TTFont('JP', JP_FONT, subfontIndex=0))

INDIGO = colors.HexColor('#2b2350')
PURPLE = colors.HexColor('#4b3a7a')
EMERALD = colors.HexColor('#1f8a70')
LIGHT = colors.HexColor('#f1eef9')
PALE = colors.HexColor('#e8f4f0')
GREY = colors.HexColor('#666666')
LINE = colors.HexColor('#c9c2dd')

OUT = os.environ.get('OUT', 'Snowmoon_Ch1_Anime_Production_Brief.pdf')

# ---------- styles ----------
def S(name, **kw):
    base = dict(fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=colors.HexColor('#1d1b26'))
    base.update(kw)
    return ParagraphStyle(name, **base)

st_title = S('title', fontName='Helvetica-Bold', fontSize=30, leading=34, textColor=colors.white)
st_sub = S('sub', fontSize=13, leading=18, textColor=colors.HexColor('#d9d2f0'))
st_h1 = S('h1', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=INDIGO, spaceBefore=4, spaceAfter=6)
st_h2 = S('h2', fontName='Helvetica-Bold', fontSize=12.5, leading=16, textColor=PURPLE, spaceBefore=8, spaceAfter=3)
st_h3 = S('h3', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=EMERALD, spaceBefore=4, spaceAfter=1)
st_body = S('body')
st_small = S('small', fontSize=8.3, leading=11.5, textColor=GREY)
st_bullet = S('bullet', leftIndent=10, bulletIndent=0)
st_label = S('label', fontName='Helvetica-Bold', fontSize=8.3, leading=11, textColor=INDIGO)
st_cell = S('cell', fontSize=8.8, leading=12.3)
st_beat = S('beat', fontSize=8.8, leading=12.3, leftIndent=0)
st_jp = S('jp', fontName='JP', fontSize=10, leading=15)
st_jp_small = S('jps', fontName='JP', fontSize=9, leading=13.5)
st_en = S('en', fontName='Helvetica-Oblique', fontSize=8.6, leading=11.5, textColor=colors.HexColor('#4a4660'))
st_spk = S('spk', fontName='Helvetica-Bold', fontSize=8.3, leading=11, textColor=EMERALD)
st_prompt = S('prompt', fontName='Courier', fontSize=7.6, leading=10, textColor=colors.HexColor('#23202e'))
st_hdr = S('hdr', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.white)
st_hdr_r = S('hdrr', fontName='Helvetica', fontSize=8.6, leading=13, textColor=colors.HexColor('#d9d2f0'))
st_tbl_h = S('tblh', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.white)
st_tbl = S('tbl', fontSize=8.5, leading=11.5)

def jp(t):
    return '<font name="JP">%s</font>' % t

def P(t, s=st_body):
    return Paragraph(t, s)

def bullets(items, s=st_bullet):
    return [Paragraph(i, s, bulletText='\u2022') for i in items]

def prompt_box(text):
    t = Table([[Paragraph(text, st_prompt)]], colWidths=[174 * mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f6f5fa')),
        ('BOX', (0, 0), (-1, -1), 0.6, LINE),
        ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    return t

def simple_table(header, rows, widths, jp_cols=(), pad=4):
    data = [[Paragraph(h, st_tbl_h) for h in header]]
    for r in rows:
        line = []
        for i, c in enumerate(r):
            if i in jp_cols:
                line.append(Paragraph(c, st_jp_small))
            else:
                line.append(Paragraph(c, st_tbl))
        data.append(line)
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), INDIGO),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT]),
        ('GRID', (0, 0), (-1, -1), 0.4, LINE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), pad), ('BOTTOMPADDING', (0, 0), (-1, -1), pad),
    ]))
    return t

# ---------- page decorations ----------
def cover_page(c, doc):
    w, h = A4
    c.saveState()
    c.setFillColor(INDIGO)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColor(PURPLE)
    c.rect(0, h * 0.30, w, h * 0.34, fill=1, stroke=0)
    c.setFillColor(EMERALD)
    c.rect(0, h * 0.30 - 4, w, 4, fill=1, stroke=0)
    c.restoreState()

def later_pages(c, doc):
    w, h = A4
    c.saveState()
    c.setFillColor(INDIGO)
    c.rect(0, h - 10 * mm, w, 10 * mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(18 * mm, h - 6.4 * mm, 'SNOWMOON  |  CHAPTER 1  |  ANIME PRODUCTION BRIEF')
    c.setFont('Helvetica', 8)
    c.drawRightString(w - 18 * mm, h - 6.4 * mm, '20 scenes x 10 s = 3:20')
    c.setFillColor(GREY)
    c.setFont('Helvetica', 8)
    c.drawCentredString(w / 2, 9 * mm, 'Page %d' % doc.page)
    c.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                      topMargin=18 * mm, bottomMargin=16 * mm,
                      title='Snowmoon Chapter 1 - Anime Production Brief',
                      author='Claude')
frame_cover = Frame(18 * mm, 18 * mm, A4[0] - 36 * mm, A4[1] - 36 * mm, id='c')
frame_main = Frame(18 * mm, 16 * mm, A4[0] - 36 * mm, A4[1] - 34 * mm, id='m')
doc.addPageTemplates([
    PageTemplate(id='Cover', frames=[frame_cover], onPage=cover_page),
    PageTemplate(id='Main', frames=[frame_main], onPage=later_pages),
])

story = []
from reportlab.platypus import NextPageTemplate

# ================= COVER =================
story += [Spacer(1, 60 * mm)]
story += [P('SNOWMOON', S('c1', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor('#9fe0cf'))),
          Spacer(1, 3 * mm),
          P('Chapter 1', st_title),
          P('Anime Production Brief', st_title),
          Spacer(1, 5 * mm),
          P('Scene brief, character reference prompts, city multiview reference, and a full 20-scene shot list with Japanese narration and dialogue (English translation included).', st_sub)]
story += [Spacer(1, 62 * mm)]
cover_tbl = Table([
    [P('<b>Source</b>', S('x', textColor=colors.HexColor('#9fe0cf'), fontSize=9)), P('vitalik.eth.limo/snowmoon, Chapter 1', S('y', textColor=colors.white, fontSize=9))],
    [P('<b>Format</b>', S('x2', textColor=colors.HexColor('#9fe0cf'), fontSize=9)), P('20 scenes, 10 seconds each, total runtime 3:20, 16:9', S('y2', textColor=colors.white, fontSize=9))],
    [P('<b>Audio</b>', S('x3', textColor=colors.HexColor('#9fe0cf'), fontSize=9)), P('Japanese anime voice acting for narrator and characters, English subtitles', S('y3', textColor=colors.white, fontSize=9))],
    [P('<b>Cast</b>', S('x4', textColor=colors.HexColor('#9fe0cf'), fontSize=9)), P('5 main characters, the drone boy, the toy drone, Emerald (AI voice)', S('y4', textColor=colors.white, fontSize=9))],
], colWidths=[28 * mm, 130 * mm])
cover_tbl.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                               ('BOTTOMPADDING', (0, 0), (-1, -1), 3), ('TOPPADDING', (0, 0), (-1, -1), 3),
                               ('LINEABOVE', (0, 0), (-1, 0), 0.6, colors.HexColor('#9fe0cf'))]))
story += [cover_tbl]
story += [NextPageTemplate('Main'), PageBreak()]

# ================= 1. OVERVIEW =================
story += [P('1. Project overview', st_h1)]
story += [P('This brief turns Chapter 1 of Snowmoon into a 3 minute 20 second anime built from twenty 10-second clips. '
            'Every clip has visual guidance, the assets it needs, narration and dialogue in Japanese with an English translation, '
            'audio notes, and a copy-paste video generation prompt.')]
story += [Spacer(1, 2 * mm)]
story += [P('Story in one paragraph', st_h2),
          P('Gladias, a calm and thoughtful apprentice of the Order of Steering, walks through the beautifully green city of Meldan in the '
            'country of Veridia. Along the way he casts a random citizen vote on a building, attends a heavy metal concert to audit it for a '
            'social impact tax, gets exposed as an Order member, escapes with a mischievous trick, rides home, and shares a warm family '
            'dinner before an anonymous message reveals that someone knows his secret.')]
story += [P('Important notes', st_h2)]
story += bullets([
    '<b>Adapted wording.</b> All narration and dialogue here is adapted in original wording to fit 10-second pacing. It follows the story beats of the chapter but is not a word-for-word copy. Check the source if you need exact lines.',
    '<b>Original lyrics.</b> The concert lyric line in Scene 8 is a new placeholder line, not the lyrics from the chapter. Replace it with your own if you like.',
    '<b>Rights.</b> If you plan to publish or monetise the anime, confirm that you have the story author\'s permission first.',
    '<b>Design choices.</b> The source text does not give ages or faces for most characters. Ages, hairstyles and colours in the reference prompts are suggested designs you can change.',
    '<b>Robe continuity.</b> Gladias wears the purple privacy robe with the hood down in the early scenes (so his face reads), hood up at the concert, hood down again on the bus and at home.',
])
story += [Spacer(1, 3 * mm)]

# ---- scene map ----
scene_map = [
    ('01', '0:00', 'Meldan establishing shot', 'Yes', '-'),
    ('02', '0:10', 'Gladias walks, Emerald audio plays', '-', 'Emerald'),
    ('03', '0:20', 'Drone flyover, watch safety check', 'Yes', '-'),
    ('04', '0:30', 'Boy catches drone, bench kindness', '-', 'Boy, Grandmother'),
    ('05', '0:40', 'Sky bridge, whispered Pause', 'Yes', 'Gladias'),
    ('06', '0:50', 'Vote request, Badra St #1103', 'Yes', '-'),
    ('07', '1:00', 'Slider vote, concert gate', '-', 'Gladias, Gate'),
    ('08', '1:10', 'Concert field, Dreadknot on stage', '-', 'Singer'),
    ('09', '1:20', 'Tax rubric and the debate', 'Yes', 'Gladias'),
    ('10', '1:30', 'Prediction score, votes Tier 3', '-', 'Gladias'),
    ('11', '1:40', '"It\'s an Order member!"', 'Yes', 'Heckler'),
    ('12', '1:50', 'Burly man and the Arctic Emperor trick', 'Yes', 'Gladias'),
    ('13', '2:00', 'Snatch, delete, throw', '-', 'Gladias, Device'),
    ('14', '2:10', 'Run in heels, hop on the bus', '-', '-'),
    ('15', '2:20', 'Bus ads and a smile', '-', 'Gladias'),
    ('16', '2:30', 'Home arrival, Zven hug', 'Yes', 'Gladias, Seila, Zven'),
    ('17', '2:40', 'Food truck order', '-', 'Seila, Febric, Zven, Gladias'),
    ('18', '2:50', 'Lily and the history exam', 'Yes', 'Lily, Seila'),
    ('19', '3:00', 'Family dinner, plans', '-', 'Seila, Gladias, Zven, Febric'),
    ('20', '3:10', 'The anonymous message', 'Yes', 'On-screen text'),
]
story += [P('Scene map at a glance', st_h2)]
story += [simple_table(['#', 'Start', 'Scene', 'Narration', 'Dialogue'],
                       [list(r) for r in scene_map],
                       [10 * mm, 14 * mm, 76 * mm, 22 * mm, 52 * mm], pad=2)]
story += [PageBreak()]

# ================= 2. STYLE & VOICE =================
story += [P('2. Style lock and voice direction', st_h1)]
story += [P('Style lock (paste into every image and video prompt)', st_h2)]
story += [prompt_box('Modern Japanese anime film style, clean line art, soft cel shading, painterly nature backgrounds, luminous natural daylight, '
                     'gentle color grading, lush green and warm stone palette with deep purple accents, high detail, cinematic 16:9 framing, '
                     'consistent character design across shots, no grime, no dust, no text artifacts.')]
story += [Spacer(1, 2 * mm)]
story += [P('Palette', st_h2)]
pal = Table([[
    P('<b>Forest green</b><br/>#2f6b4f', st_small), P('<b>Warm stone</b><br/>#c9b79c', st_small),
    P('<b>Robe purple</b><br/>#3c2a63', st_small), P('<b>Sky blue-grey</b><br/>#7a95b0', st_small),
    P('<b>Stage red</b><br/>#c4361f', st_small), P('<b>Emerald AI</b><br/>#1fbf8f', st_small)]],
    colWidths=[29 * mm] * 6, rowHeights=[16 * mm])
pal.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#a9d3bd')), ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#e8dcc8')),
    ('BACKGROUND', (2, 0), (2, 0), colors.HexColor('#b9a9dd')), ('BACKGROUND', (3, 0), (3, 0), colors.HexColor('#c6d3e0')),
    ('BACKGROUND', (4, 0), (4, 0), colors.HexColor('#efb3a6')), ('BACKGROUND', (5, 0), (5, 0), colors.HexColor('#a6ead2')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('BOX', (0, 0), (-1, -1), 0.5, LINE),
    ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.white)]))
story += [pal]
story += [P('Voice and audio direction (Japanese anime voice acting)', st_h2)]
voice_rows = [
    ['Narrator', jp('ナレーター'), 'Calm, warm, slightly formal adult voice. Steady pace, gentle pauses. Sounds like a documentary-style anime narrator.'],
    ['Gladias', jp('グラディアス'), 'Mid-low adult male. Thoughtful and soft, with dry humor. Whispers in Scene 5. Voice becomes quick and playful in Scene 12.'],
    ['Seila', jp('セイラ'), 'Warm mature female voice. Kind, relaxed, a little teasing.'],
    ['Zven', jp('ズヴェン'), 'High, bright, energetic young boy. Shouts a lot.'],
    ['Febric', jp('フェブリック'), 'Relaxed teenage boy. Slightly sleepy, dry, affectionate.'],
    ['Lily', jp('リリー'), 'Low-energy tween girl. Flat, muffled, hides feelings.'],
    ['Drone boy', jp('少年'), 'Loud, proud, sporty young boy. One line only.'],
    ['Emerald (AI)', jp('エメラルド'), 'Soft neutral synthetic-sounding female voice, friendly, no vibrato.'],
    ['Gate and device', jp('ゲート／端末'), 'Clean flat machine voice, short confirmations.'],
    ['Dreadknot singer', jp('ボーカル'), 'Growled metal vocal, aggressive delivery, heavily reverbed.'],
]
story += [simple_table(['Role', 'Japanese', 'Voice direction'], voice_rows, [30 * mm, 30 * mm, 114 * mm], jp_cols=(1,))]
story += [P('Timing budget', st_h2)]
story += [P('A 10-second clip comfortably holds about 55 to 70 Japanese characters of speech at anime pace, with a natural breath between lines. '
            'Scenes that carry both narration and dialogue are kept under that budget. If a generated clip runs long, trim the narration first and keep the character lines.')]
story += [PageBreak()]

# ================= 3. NARRATION =================
story += [P('3. Narration script (Japanese with English translation)', st_h1)]
story += [P('Ten narration sentences, spread across the film. The narrator is a separate audio track from the character dialogue, recorded in Japanese.')]
narr = [
    ('N1', 'Scene 1', '三七二四年、雪月の三日。ヴェリディアの首都メルダンは、森のように静かに息づいていた。',
     'Year 3724, the third day of Snowmoon. Meldan, the capital of Veridia, breathed as quietly as a forest.'),
    ('N2', 'Scene 3', 'この街では、おもちゃのドローンでさえ、無害であることを証明する。そして、それ以外は何も明かさない。',
     'In this city even a toy drone proves that it is harmless, and reveals nothing else.'),
    ('N3', 'Scene 5', '今日、グラディアスに求められているのは、人間の世界について意見を述べることだった。',
     'Today, Gladias was asked to give his opinion on the human world.'),
    ('N4', 'Scene 6', '市民はくじで選ばれ、建物の美しさに投票する。その評価が、建物の税を決めるのだ。',
     'Citizens are chosen by lot to vote on how beautiful a building is, and that score decides its tax.'),
    ('N5', 'Scene 9', 'グラディアスは舵取り会の見習い。彼の判断は、今まさに採点されている。',
     'Gladias is an apprentice of the Order of Steering, and his judgment was being scored right at that moment.'),
    ('N6', 'Scene 11', 'だが会の者は、正体を隠さねばならない。見破った者には、賞金が支払われる。',
     'But members of the Order must stay hidden, and whoever unmasks one collects a bounty.'),
    ('N7', 'Scene 12', '思慮深い哲学者の仮面が外れ、いたずら好きの少年が顔を出した。',
     'The thoughtful philosopher\'s mask slipped, and a mischievous boy showed his face.'),
    ('N8', 'Scene 16', '家では家族が待っていた。二人は自分たちの子、あとの二人は共同家族の子だ。',
     'At home his family was waiting: two children of his own, and two from their co-family.'),
    ('N9', 'Scene 18', 'あと四日で、子どもたちは半年間、もうひとつの家族のもとへ行く。',
     'In four days the children would go to live with the other family for half a year.'),
    ('N10', 'Scene 20', 'そのとき、彼の秘密を知る誰かが、静かに連絡をよこした。',
     'And then someone who knew his secret quietly reached out.'),
]
rows = []
for n, sc, j, e in narr:
    rows.append([n + '<br/>' + sc, j, e])
story += [simple_table(['Line', 'Japanese (narrator)', 'English translation'], rows,
                       [22 * mm, 88 * mm, 64 * mm], jp_cols=(1,))]
story += [Spacer(1, 3 * mm)]
story += [P('Name and term glossary (Japanese)', st_h2)]
gl = [
    ['Gladias', jp('グラディアス'), 'Meldan', jp('メルダン')],
    ['Seila', jp('セイラ'), 'Veridia', jp('ヴェリディア')],
    ['Zven', jp('ズヴェン'), 'Kalimar district', jp('カリマル地区')],
    ['Febric', jp('フェブリック'), 'Order of Steering', jp('舵取り会')],
    ['Lily', jp('リリー'), 'Acolyte', jp('見習い')],
    ['Emerald (AI)', jp('エメラルド'), 'Privacy Robe', jp('プライバシー・ローブ')],
    ['Dreadknot (band)', jp('ドレッドノット'), 'Arctic Emperor', jp('北極皇帝')],
]
story += [simple_table(['English', 'Japanese', 'English', 'Japanese'], gl,
                       [38 * mm, 42 * mm, 42 * mm, 52 * mm], jp_cols=(1, 3))]
story += [PageBreak()]

# ================= 4. CHARACTER SHEETS =================
story += [P('4. Character reference sheet prompts', st_h1)]
story += [P('Generate each sheet as one image, then use it as the reference image for every video clip that features the character. '
            'Keep the same sheet, outfit and seed for the whole film to avoid drift.')]
story += [P('Shared layout block (add to the start of every character prompt)', st_h2)]
story += [prompt_box('Character reference sheet, modern Japanese anime film style, clean line art, soft cel shading, plain light grey background, 16:9. '
                     'Layout: full-body turnaround on the left (front, three-quarter, side, back), five head-and-shoulder expressions on the right '
                     '(neutral, smiling, surprised, worried, mischievous), color palette swatches along the bottom, small labelled prop callouts.')]

chars = [
    ('4.1 Gladias (main, Acolyte of the Order)', jp('グラディアス'),
     'Adult man in his early forties. Slim, average height. Calm, thoughtful, gentle humor. Two outfits: everyday and the Veridian Privacy Robe.',
     'CHARACTER: Gladias, adult man in his early forties, slim build, short dark tousled hair, calm thoughtful dark eyes, gentle half-smile. '
     'OUTFIT A (everyday): soft muted green linen tunic, dark trousers, simple brown shoes. A thin silken cloth band wrapped tightly around his neck '
     '(a silent throat microphone), a small wireless earpiece in one ear, a smartwatch on his left wrist, a palm-sized hand device. '
     'OUTFIT B (Veridian Privacy Robe): loose-fitting dark purple robe covering the whole body from hood to ankles, matching dark purple shoes with '
     'high heels and deliberately uneven soles, a strap-belt face cover that tightens across the face just below the nose. Show the robe with hood up '
     'and hood down. Expression set includes a quiet contented smile and a mischievous grin.'),
    ('4.2 Seila (Gladias\'s wife, blogger)', jp('セイラ'),
     'Adult woman in her late thirties. Warm, curious, practical. Writes a blog and travels.',
     'CHARACTER: Seila, adult woman in her late thirties, warm brown eyes, shoulder-length wavy dark hair tied loosely at the back, slight smile lines, '
     'kind relaxed expression. OUTFIT: deep green knit cardigan over a cream top, comfortable dark trousers, soft indoor shoes. Holds a palm-sized '
     'hand device. Expressions include gentle concern, soft laughter, and a caring hug pose.'),
    ('4.3 Zven (their younger son)', jp('ズヴェン'),
     'Boy around 8. Small and bouncy, always cheerful, shouts when excited.',
     'CHARACTER: Zven, boy around 8 years old, small and energetic, messy short brown hair, big bright eyes, wide gap-toothed grin. '
     'OUTFIT: soft orange hoodie with a small star patch, khaki shorts, white sneakers. Add extra poses: jumping down stairs three steps at a time, '
     'running into a hug, cheering with both arms up.'),
    ('4.4 Febric (co-family teenage boy)', jp('フェブリック'),
     'Boy around 15. Tall, relaxed, dry sense of humor. Always carries a device on a cable.',
     'CHARACTER: Febric, teenage boy around 15, tall and lanky, dark curly hair, slightly sleepy calm eyes, relaxed posture. '
     'OUTFIT: grey hoodie with sleeves pushed up, dark jeans, worn sneakers. PROP: a hand device connected by a thin cable to a larger rugged '
     'compute box carried in the other hand. Expressions: laid-back, quietly amused, fondly serious.'),
    ('4.5 Lily (Gladias and Seila\'s daughter)', jp('リリー'),
     'Girl around 12 or 13. Quiet, withdrawn after a bad exam, absorbed in a mobile game.',
     'CHARACTER: Lily, girl around 12 to 13 years old, slim, straight dark-brown hair partly covering her face, tired downcast eyes. '
     'OUTFIT: oversized lavender hoodie, grey leggings, socks. PROP: hand device held close to her chest. Expressions: withdrawn, '
     'intensely focused on a game, a tiny softened smile, turning her face away.'),
    ('4.6 The drone boy (catches the drone)', jp('ドローンを捕まえる少年'),
     'Boy around 9 or 10. Athletic, proud, part of a family with four children. Must look clearly different from Zven.',
     'CHARACTER: sporty boy around 9 to 10 years old, athletic build, short spiky light-brown hair, a small confident smirk. '
     'OUTFIT: blue and white sports jersey with the number 5, knee-length blue shorts, red sneakers, a yellow wristband. Add a mid-jump pose '
     'catching a ball-shaped drone with one hand, and a triumphant pose holding it up. Add small secondary references of two younger siblings '
     'riding tricycles (a little sister in pink, a little brother in green).'),
    ('4.7 The toy drone', jp('おもちゃのドローン'),
     'Small ball-shaped toy drone with feather-like rotors on three sides. Harmless, friendly, safe-looking.',
     'PROP SHEET: toy drone, small ball-shaped body about the size of a grapefruit, smooth matte pastel mint shell, three feather-like soft rotors '
     'arranged around three sides, tiny soft green status light on the front, rounded friendly design. Views: front, side, top, bottom, rotor detail '
     'close-up, size comparison next to a boy\'s hand, in-flight pose with soft rotor motion blur, and a "caught in hand" pose.'),
]
for title, jname, desc, prompt in chars:
    block = [P('%s  <font name="JP" size="10">%s</font>' % (title, jname), st_h2),
             P(desc, st_body), Spacer(1, 1.5 * mm),
             prompt_box(prompt), Spacer(1, 2 * mm)]
    story += [KeepTogether(block)]

story += [P('Supporting props', st_h2)]
props = [
    ('Hand device and watch',
     'PROP SHEET: sleek palm-sized hand device with a soft-glow screen and a slim smartwatch, both in matte graphite with thin emerald edge lights. '
     'Show UI states: green check confirmation, vote slider from -5 to 5 with a Select button, rubric table screen, prediction score gauge, incoming message card.'),
    ('Emerald AI icon',
     'ICON SHEET: small circular emerald-green glowing orb icon with a soft ripple animation, shown on the hand device screen and as a small floating '
     'holographic mark near Gladias\'s ear. Calm, friendly, non-humanoid.'),
]
for t, p in props:
    story += [KeepTogether([P(t, st_h3), prompt_box(p), Spacer(1, 2 * mm)])]
story += [PageBreak()]

# ================= 5. CITY MULTIVIEW =================
story += [P('5. City multiview reference: Meldan, Kalimar district', st_h1)]
story += [P('Meldan looks like a medieval town without the grime, fully woven into nature: stone-brick houses, tall trees everywhere, quiet foot paths, and a '
            'clean modern transport network. Generate the master sheet first, then the panel views, and reuse them as reference images for every environment shot.')]
story += [P('Master multiview prompt', st_h2)]
story += [prompt_box(
    'Environment reference sheet, multiview of the same city district, modern Japanese anime film style, painterly backgrounds, luminous daylight, '
    '16:9. The district is Kalimar in Meldan, capital of Veridia: medieval-style large stone-brick houses that are perfectly clean (no dust, no dirt, no '
    'decay), each house melded seamlessly into surrounding leaves, plants and tall trees, small hanging signs for clothing, flowers and food, '
    'quiet foot paths shaded by trees, five-storey modern apartment buildings interspersed with walking paths and tiny shops, a tall soundproof '
    'barrier painted in green and blue behind a row of trees, a curving sky bridge over a busy road with cars, autobuses and small autonomous delivery vehicles, '
    'and a forested mountain in the distance with fifteen-storey apartment towers shaped like oversized medieval castle towers with many windows. '
    'Show 8 labelled panels (A to H) of consistent architecture, materials and color: A aerial establishing, B forest footpath, C sky bridge, '
    'D apartment street with barrier, E mountain view, F concert field, G autobus interior, H family house exterior and interior. '
    'Consistent color palette: forest green, warm stone, blue-grey, deep purple accents.')]
story += [Spacer(1, 2 * mm)]
story += [P('Panel prompts (generate individually for higher detail)', st_h2)]
panels = [
    ('A. Aerial establishing (used in Scene 1)',
     'High angle wide shot over the tree canopy of Kalimar district, Meldan. Stone-brick houses hidden among trees, curling foot paths, distant mountain with tall castle-tower apartments, '
     'a sky bridge crossing a road in the mid distance. Soft morning haze, drifting leaves. Anime film style.'),
    ('B. Forest footpath (Scenes 1 to 4)',
     'Eye-level view down a foot path with tall trees on both sides. Large clean stone-brick medieval-style houses behind the trees, small signs for clothing, flowers and food. '
     'Side sidewalks branching left and right with a bench on the right side. Dappled sunlight.'),
    ('C. Sky bridge (Scene 5)',
     'Smooth sky bridge rising from a green foot path, crossing over a busy road with cars, autobuses and delivery vehicles. Cool breeze feeling. '
     'View along the road for about two kilometers that turns right, and a forested mountain with castle-tower apartments beyond.'),
    ('D. Apartment street with soundproof barrier (Scenes 6 to 7)',
     'Street with a row of five-storey blue-grey apartment buildings on the left, walking paths and small shops between them, tall trees shading the sidewalk. '
     'On the right, a tall soundproof barrier painted green and blue, partly hidden behind a thick row of trees. Distant aeroplane-shaped corporate headquarters visible between the trees.'),
    ('E. Concert entrance and field (Scenes 7 to 14)',
     'Opening in the green-blue soundproof barrier with a glowing green circle scanner on the gate. Beyond it, a large open grass field enclosed by the barrier, a stage with red and orange lights, '
     'a crowd of dancers and chatters wearing band shirts, with a few people in dark purple hooded robes. Fire exit door on the right side.'),
    ('F. Autobus interior (Scenes 14 to 15)',
     'Interior of a clean, nearly empty local autobus, natural light through big windows, two seats on the left with robed passengers, a teenager with a backpack on the right. '
     'Two advertisement posters on the walls: one about lifelong learning showing a child, a middle-aged woman and an elderly man reading textbooks together; '
     'one for a drink brand with a yellow-and-green bottle.'),
    ('G. Family house exterior and interior (Scenes 16 to 20)',
     'Warm evening exterior of a modest stone-and-wood family home with trees, then interior: stairs, a large dining table, a couch, a bathroom door, cozy lamp light. '
     'Clean lived-in feel with personal items: shoes by the door, tablets, a compute box on the table.'),
    ('H. Signature details (insert references)',
     'Detail sheet: stone brick texture, moss and leaves growing into walls, hanging shop signs, barrier paint pattern in green and blue, the glowing green gate scanner, '
     'the autobus body with rounded front, small delivery vehicle, the sky bridge railing.'),
]
for t, p in panels:
    story += [KeepTogether([P(t, st_h3), prompt_box(p), Spacer(1, 1.5 * mm)])]
story += [PageBreak()]

# ================= 6. SCENES =================
story += [P('6. Scene-by-scene brief (20 scenes, 10 seconds each)', st_h1)]
story += [P('Each card lists timecode, location, assets needed, beat-by-beat visual guidance, narration, dialogue (Japanese and English), audio notes, and a copy-paste video prompt. '
            'Prompts assume you attach the character and environment reference images from sections 4 and 5. Append the style lock from section 2 if your tool does not carry it forward.')]

STYLE_TAIL = ' Modern Japanese anime film style, soft cel shading, painterly backgrounds, 16:9, 10 seconds.'

def tc(n):
    a, b = (n - 1) * 10, n * 10
    return '%d:%02d - %d:%02d' % (a // 60, a % 60, b // 60, b % 60)

def dl(speaker, kind, jline, eline):
    return [P('%s  <font color="#888888">(%s)</font>' % (speaker, kind), st_spk),
            P(jp(jline), st_jp_small),
            P(eline, st_en), Spacer(1, 1.5 * mm)]

scenes = [
 dict(n=1, title='Meldan establishing shot', loc='Forest footpath, Kalimar district, Meldan',
      assets='City panels A and B. Gladias (tiny, distant, hood down) in the last beat.',
      beats=[('0-4s', 'Slow crane-down from above the tree canopy to reveal clean stone-brick houses merged into trees and plants. Drifting leaves. Title card fades in and out: Meldan, Veridia - 3724 Snowmoon 3.'),
             ('4-8s', 'Gentle push-in along the foot path. Small signs for clothing, flowers and food. Nature and buildings feel like one thing.'),
             ('8-10s', 'A tiny figure in a dark purple robe walks into frame under the trees, hood down. Hold.')],
      narr=('N1', narr[0][2], narr[0][3]), dial=[],
      audio='Soft forest ambience, distant birdsong, light wind. Gentle acoustic guitar and piano theme starts quietly.',
      prompt='Slow crane-down from above the tree canopy to a peaceful district of large clean medieval-style stone-brick houses melded into trees and plants, shop signs for clothing, flowers and food, '
             'drifting leaves, a small figure in a dark purple robe walking along the foot path at the end.' + STYLE_TAIL),
 dict(n=2, title='Gladias walks, Emerald audio plays', loc='Forest footpath',
      assets='Gladias (everyday outfit + purple robe, hood down), neck band, earpiece, hand device. City panel B.',
      beats=[('0-3s', 'Side tracking shot of Gladias walking calmly between tall trees, robe swaying.'),
             ('3-6s', 'Close-up: he breathes in, eyes closing briefly, lips curving slightly. Earpiece and silk neck band visible.'),
             ('6-10s', 'Insert on the hand device in his palm: soft emerald orb pulses with an audio waveform. Behind him, houses dissolve into plants in soft focus.')],
      narr=None,
      dial=[('Emerald (AI)', 'voice over, faint', '…空気感染の仕組みと、換気や密度が街全体の感染者数に与える影響の計算法をご説明します',
             '...Let me explain how airborne infection spreads, and how to calculate what ventilation and density do to citywide case counts.')],
      audio='Birdsong, footsteps on soft ground. Emerald voice sits softly in the mix like a podcast in one earpiece.',
      prompt='Gladias, a calm man in a dark purple hooded robe with hood down and a thin silk band around his neck, walks along a shaded foot path between tall trees, breathes in with closed eyes, '
             'then a close-up of a glowing emerald orb icon pulsing on a palm-sized device in his hand.' + STYLE_TAIL),
 dict(n=3, title='Drone flyover and watch safety check', loc='Forest footpath',
      assets='Gladias, the toy drone (prop sheet), watch UI. City panel B.',
      beats=[('0-2s', 'Small toy drone glides fast over his head from behind, its shadow crossing him. He looks up, startled.'),
             ('2-5s', 'Macro close-up on his wrist watch: a green check lights up. Three short UI lines slide in: Toy drone verified / Keeps a safe distance from people / Nothing else shared.'),
             ('5-8s', 'Follow the drone as it curves off along a left sidewalk. Clear look at its ball shape with feather-like rotors on three sides.'),
             ('8-10s', 'Back to Gladias, relaxed and smiling, lowering his wrist.')],
      narr=('N2', narr[1][2], narr[1][3]), dial=[],
      audio='Soft rotor whirr with a whoosh, gentle confirmation chime for the watch, light ambience continues.',
      prompt='A small ball-shaped toy drone with soft feather-like rotors on three sides flies quickly over a man walking on a forest foot path, close-up of his smartwatch lighting a green check with small UI lines, '
             'then the drone flying away down a side sidewalk.' + STYLE_TAIL),
 dict(n=4, title='Boy catches the drone, bench kindness', loc='Side sidewalks off the footpath',
      assets='Drone boy, two small siblings on tricycles, grandmother + small child, seated couple, the toy drone. City panel B.',
      beats=[('0-3s', 'Low angle: the drone zips overhead and the boy jumps and snatches it out of the air with one hand. Two younger siblings on tricycles behind him.'),
             ('3-5s', 'He holds it up and shouts in triumph.'),
             ('5-10s', 'Pan right to another sidewalk. A grandmother with a small child approaches a bench. A seated couple stands up and offers their seats. The grandmother bows her thanks and sits down.')],
      narr=None,
      dial=[('Drone boy', 'shouting', 'よっしゃー！ぼくの五ポイント！', 'Yes! Five points for me!'),
            ('Grandmother', 'warm', 'ありがとうねえ、ご親切に', 'Thank you, dear, how kind.')],
      audio='Kids laughing, tricycle bells, a happy woodwind motif for the boy, soft warm strings for the bench moment.',
      prompt='A sporty boy in a blue and white number 5 jersey leaps and catches a small ball-shaped drone out of the air, two small kids on tricycles behind him; '
             'pan to a grandmother and a small child arriving at a bench where a young couple stands up to offer their seats.' + STYLE_TAIL),
 dict(n=5, title='Sky bridge and the whispered Pause', loc='Sky bridge over a busy road',
      assets='Gladias, neck band, city panel C.',
      beats=[('0-3s', 'The foot path curves upward and smoothly becomes a sky bridge over a busy road with cars, autobuses and delivery vehicles.'),
             ('3-6s', 'Gladias steps to the middle; a chilly breeze blows hair and robe into his face.'),
             ('6-8s', 'Extreme close-up of his neck band and throat: his lips barely move, only the throat, as he whispers.'),
             ('8-10s', 'Reverse wide: the road runs two kilometers then turns right; a forested mountain with castle-tower apartments beyond.')],
      narr=('N3', narr[2][2], narr[2][3]),
      dial=[('Gladias', 'whisper, silent-speech', '一時停止。この景色を、少し味わいたいんだ', 'Pause. I want to take in this view for a moment.')],
      audio='Wind rush, traffic hum from below, Emerald audio cuts out on the whisper. Music opens up with a wide orchestral swell.',
      prompt='A smooth green footpath rises into a sky bridge over a busy road with cars and autobuses, a man in a dark purple robe stops in the middle in a chilly breeze, close-up of his silk neck band as he silently whispers, '
             'then a wide reveal of the long road and a forested mountain with castle-tower apartment buildings.' + STYLE_TAIL),
 dict(n=6, title='The vote request: Badra St #1103', loc='Street beside the soundproof barrier',
      assets='Gladias, hand device UI (vote screen), city panel D.',
      beats=[('0-3s', 'Gladias walks beside a tall green-and-blue soundproof barrier hidden behind trees. His device buzzes; he pulls it out.'),
             ('3-6s', 'UI insert: Vote on Badra St #1103 / Five-storey apartment building, blue-grey / slider from -5 to 5 with a Select button.'),
             ('6-8s', 'Reverse: the blue-grey five-storey building with tree-lined foot paths, in soft afternoon light.'),
             ('8-10s', 'Tax card slides in: Total land tax 1.51%. Quick cut to a tiny aeroplane-shaped headquarters in the far distance, its tax card reading 1.89%.')],
      narr=('N4', narr[3][2], narr[3][3]), dial=[],
      audio='Device buzz, soft UI clicks, city hum. Light curious pizzicato motif.',
      prompt='A man walks beside a tall green and blue painted soundproof barrier hidden by trees, checks a buzzing hand device showing a vote slider for a five-storey blue-grey apartment building, '
             'then a shot of the tree-lined building and a small tax card, and a distant aeroplane-shaped office building between the trees.' + STYLE_TAIL),
 dict(n=7, title='Slider vote and the concert gate', loc='Street to the concert entrance',
      assets='Gladias (robe, hood up at the end), device UI, gate scanner, city panel E.',
      beats=[('0-3s', 'Gladias zooms his device at the aeroplane building, smirks, and shakes his head with amusement.'),
             ('3-5s', 'Slider close-up: his thumb nudges it only slightly to the right, then taps Select.'),
             ('5-8s', 'He arrives at an opening in the barrier and holds his device to a glowing green circle on the gate.'),
             ('8-10s', 'Gate lights turn green; he pulls his hood up and walks through as music pours from inside.')],
      narr=None,
      dial=[('Gladias', 'thought', 'あの飛行機ビルの税は…まあ、妥当だな', 'That aeroplane building\'s tax... well, it\'s fair enough.'),
            ('Gate machine', 'flat voice', '認証しました。ようこそ', 'Verified. Welcome.')],
      audio='Muffled bass from the concert growing louder, gate confirmation beep, soft crowd noise.',
      prompt='A man zooms his hand device toward a far-away aeroplane-shaped building and smirks, thumb nudges a slider slightly to the right, then he scans the device at a glowing green circle on a gate in a tall green and blue barrier, '
             'the gate turns green and he pulls up his purple hood and walks through.' + STYLE_TAIL),
 dict(n=8, title='Concert field, Dreadknot on stage', loc='Concert field inside the soundproof barrier',
      assets='Gladias in the robe (hood up), crowd extras, stage, singer (Dreadknot). City panel E.',
      beats=[('0-3s', 'Close-up of Gladias tightening the strap on his face cover just below the nose, hood up.'),
             ('3-6s', 'Wide of the large enclosed field: dancers, chatters, a few robed figures, calm watchers.'),
             ('6-10s', 'Stage with a growling lead singer under red and orange lights, fists in the air. Gladias pushes through the crowd toward the front.')],
      narr=None,
      dial=[('Dreadknot singer', 'growl, original placeholder lyric', '夜を裂け、鉄の嵐となれ！', 'Tear the night, become a storm of iron!')],
      audio='Full heavy metal band: distorted guitars, double bass drum, growled vocal, crowd roar. Cut all other music.',
      prompt='A robed man with his hood up tightens a face-cover strap, wide shot of a large open concert field enclosed by a tall barrier with dancing crowds and a few people in purple robes, '
             'a metal singer growling on stage under red and orange lights while the man pushes toward the front.' + STYLE_TAIL),
 dict(n=9, title='Tax rubric and the debate', loc='Front of the concert crowd',
      assets='Gladias, rubric UI (Tiers 1 to 5), crowd, stage.',
      beats=[('0-3s', 'Device screen: a simplified rubric table of Tiers 1 to 5 with tax rates from 0% to 40%.'),
             ('3-7s', 'Cross-cut: cheering, dancing crowd, then the stage. Floating words appear over the scene: Advocating vs Showcasing.'),
             ('7-10s', 'Gladias looks uneasy: a brief flash of stern authority figures (silhouetted Sentinels) preferring a softer society, then back to his face.')],
      narr=('N5', narr[4][2], narr[4][3]),
      dial=[('Gladias', 'thought', '暴力を煽っているのか、それとも見せ物にしているだけなのか…', 'Are they inciting violence, or just putting it on as a show...?')],
      audio='Concert muffled slightly as Gladias concentrates, his thought line and narrator sit above the mix.',
      prompt='Close-up of a palm-sized device showing a five-tier tax rubric, cross-cut with a joyful cheering metal concert crowd, floating text reading advocating versus showcasing, '
             'and a worried man in a purple hood weighing his decision.' + STYLE_TAIL),
 dict(n=10, title='Prediction score and the Tier 3 vote', loc='Front of the concert crowd',
      assets='Gladias, device UI (score gauge, Acolyte chat, tier buttons).',
      beats=[('0-3s', 'Score gauge fills to 92 with a bold line at 90: the deadline for becoming a Sentinel.'),
             ('3-6s', 'Chat panel: two Acolytes argue, one for Tier 3 and one for Tier 4. Small floating numbers and fractions orbit Gladias\'s head as he computes his odds.'),
             ('6-8s', 'The band finishes a song; the crowd roars. He looks at the joyful faces and steels himself.'),
             ('8-10s', 'His thumb taps Tier 3. A brief, proud smile.')],
      narr=None,
      dial=[('Gladias', 'thought', 'よし、賭けてみよう。ティア3だ', 'Alright, I\'ll take the gamble. Tier 3.')],
      audio='Heartbeat-like bass pulse under the crowd, a cymbal swell, and a quiet UI click on the vote.',
      prompt='A device shows a prediction score of 92 with a marker at 90 and a small chat between two apprentices, small floating math symbols swirl around a man in a purple hood, '
             'the band ends a song with a roaring crowd, his thumb taps a Tier 3 button and he smiles proudly.' + STYLE_TAIL),
 dict(n=11, title='"It\'s an Order member!"', loc='Concert crowd',
      assets='Gladias, heckler (voice + hand in frame), crowd, decoy in purple robe. City panel E.',
      beats=[('0-2s', 'Hard cut from the proud smile to frozen shock.'),
             ('2-5s', 'A voice from behind yells. The crowd turns their heads toward him one by one.'),
             ('5-8s', 'Fast POV: Gladias scans the field and locks on the nearest exit.'),
             ('8-10s', 'A robed man bolts for the fire exit on the right. Dozens of hand devices point at him.')],
      narr=('N6', narr[5][2], narr[5][3]),
      dial=[('Heckler (off-screen)', 'shouting', 'おい、みんな！会の人間がいるぞ！', 'Hey, everyone! There\'s an Order member here!')],
      audio='Music drops to muffled reverb, a sharp sting, then crowd murmur and phone shutter sounds.',
      prompt='A man in a purple hood freezes in shock as a shout rings out behind him and the crowd turns, fast POV scanning for an exit, another robed man sprints toward a fire exit on the right '
             'while many people raise hand devices to film him.' + STYLE_TAIL),
 dict(n=12, title='Burly man and the Arctic Emperor trick', loc='Concert crowd',
      assets='Gladias, burly man, crowd.',
      beats=[('0-3s', 'Gladias turns to run and finds a large burly man pointing a hand device straight at his face.'),
             ('3-6s', 'Slow push-in on Gladias\'s eyes. His expression shifts from panic to a schoolboy\'s mischievous glint.'),
             ('6-8s', 'He snaps his head and points off-screen with fake excitement.'),
             ('8-10s', 'The man turns to look, confused.')],
      narr=('N7', narr[6][2], narr[6][3]),
      dial=[('Gladias', 'excited, fake', '見ろ！北極皇帝の新しい声明じゃないか？', 'Look! Isn\'t that a new statement from the Arctic Emperor?')],
      audio='Music hard-cuts to silence for the push-in, then a small comic sting on the trick.',
      prompt='A robed man turns and faces a huge burly man aiming a hand device at his face, slow push-in as the robed man\'s frightened eyes turn mischievous, '
             'he points excitedly off-screen and the burly man looks away in confusion.' + STYLE_TAIL),
 dict(n=13, title='Snatch, delete, throw', loc='Concert crowd',
      assets='Gladias, burly man, snatched hand device, device UI.',
      beats=[('0-2s', 'Gladias\'s hand snatches the device from the man\'s arm.'),
             ('2-5s', 'He spins away and barks a command at the stolen device.'),
             ('5-7s', 'Device screen: it deletes files and briefly shows thumbnails, one of them is Gladias\'s face at bottom right. Screen goes black.'),
             ('7-10s', 'He throws the device high in the air. The burly man\'s eyes and hands follow it upward.')],
      narr=None,
      dial=[('Gladias', 'quick, commanding', '直近一時間の音声・画像・動画をすべて削除。再起動', 'Delete all audio, images and video from the last hour. Reboot.'),
            ('Stolen device', 'flat voice', '四件のファイルを削除しました', 'Four files deleted.')],
      audio='Fast percussion hits, device blip, a rising whoosh for the throw.',
      prompt='A robed man snatches a hand device from a burly man\'s arm, spins away and speaks a command, the screen flashes thumbnails including his face then goes black, '
             'he throws the device high into the air while the burly man watches it fly.' + STYLE_TAIL),
 dict(n=14, title='Run in heels, hop on the bus', loc='Concert field, exit, street, bus stop',
      assets='Gladias (purple robe, high-heeled uneven-soled shoes), crowd, autobus. City panels E and F.',
      beats=[('0-4s', 'Low tracking shot of his purple heeled shoes with uneven soles wobbling as he runs, robe flapping, crowd distracted by the fire exit chase.'),
             ('4-7s', 'He reaches the barrier exit and slips out while heads are still turned.'),
             ('7-10s', 'He jumps onto a local autobus just as the doors close.')],
      narr=None, dial=[],
      audio='Fast driving music, crowd fading away, a bus chime and door hiss to end.',
      prompt='Low tracking shot of dark purple high-heeled shoes with uneven soles running, a robed man weaves through a distracted crowd, slips through a gate in a tall barrier and jumps onto a local autobus '
             'as the doors close.' + STYLE_TAIL),
 dict(n=15, title='Bus ads and a smile', loc='Autobus interior',
      assets='Gladias (hood down), two robed passengers, teenager with backpack, two ad posters. City panel F.',
      beats=[('0-3s', 'Nearly empty bus: two robed passengers on the left (faces hidden), a teenager with a backpack on the right. Gladias sits and lowers his hood.'),
             ('3-6s', 'Poster 1: a classroom with a child, a middle-aged woman and an elderly man reading together. Text: Learning is a lifelong duty. School ends at 20, education never does.'),
             ('6-8s', 'Poster 2: a yellow-and-green drink bottle. Text: Free of over 2,000 known poisons.'),
             ('8-10s', 'Close-up of Gladias smiling at the poster.')],
      narr=None,
      dial=[('Gladias', 'thought', '世の中には、もっと楽しさが必要だよな', 'The world could use a bit more fun.')],
      audio='Quiet bus hum, soft warm music returns, a tiny sparkle sound on his smile. Poster text is on-screen only, no voice.',
      prompt='A nearly empty clean autobus with two hooded passengers and a teenager with a backpack, a man in a purple robe lowers his hood and looks at two wall posters: a family-of-generations learning scene '
             'and a yellow-and-green drink bottle ad, then smiles warmly.' + STYLE_TAIL),
 dict(n=16, title='Home arrival, Zven hug', loc='Family house, evening',
      assets='Gladias, Seila, Zven, Febric, house exterior/interior. City panel G.',
      beats=[('0-3s', 'Warm evening exterior of the family house. Gladias opens the door.'),
             ('3-6s', 'He calls out. Seila steps out of her room.'),
             ('6-8s', 'Zven leaps down the stairs three steps at a time and runs into Gladias for a hug.'),
             ('8-10s', 'Febric follows slowly, his hand device attached by a cable to a compute box in the other hand.')],
      narr=('N8', narr[7][2], narr[7][3]),
      dial=[('Gladias', 'calling', 'セイラ、いるかい？', 'Seila, are you home?'),
            ('Seila', 'from her room', 'ちょうどブログを書き終えたところよ', 'I just finished writing my blog post.'),
            ('Zven', 'shouting', 'パパが帰ってきたー！', 'Dad\'s home!')],
      audio='Door creak, warm home ambience, footsteps on stairs, a soft warm theme.',
      prompt='Evening exterior of a cozy stone-and-wood house, a man opens the front door and calls inside, a woman steps out of a room, a small boy jumps down stairs three steps at a time and hugs the man, '
             'a tall teenager follows carrying a hand device on a cable to a compute box.' + STYLE_TAIL),
 dict(n=17, title='Food truck order', loc='Family dining area',
      assets='Gladias, Seila, Febric, Zven, hand device UI (order screen).',
      beats=[('0-3s', 'Seila holds up her device and suggests the food truck arriving in seven minutes.'),
             ('3-6s', 'Febric calls out his number, Zven shouts his number and does a victory fist.'),
             ('6-8s', 'Gladias picks his own number with a shrug.'),
             ('8-10s', 'Seila taps the order button; a cute confirmation icon.')],
      narr=None,
      dial=[('Seila', 'friendly', '夕飯は、七分後に来るジェゴのフードトラックにしない？', 'How about dinner from the Dzego food truck? It arrives in seven minutes.'),
            ('Febric', 'casual', 'ぼく、四番！', 'Number four for me!'),
            ('Zven', 'excited', '五番！ぼくの勝ち！', 'Number five, I win!'),
            ('Gladias', 'relaxed', 'じゃあ、僕は十三番にしよう', 'Then I\'ll have number thirteen.')],
      audio='Cozy kitchen ambience, light comedic music.',
      prompt='A warm dining area where a woman holds up a hand device and smiles, a tall teen and a small boy call out numbers with the boy pumping his fist, the father shrugs and picks his number, '
             'the woman taps an order button with a cheerful confirmation icon.' + STYLE_TAIL),
 dict(n=18, title='Lily and the history exam', loc='Family living room',
      assets='Lily, Seila, Gladias, couch, bathroom door, hand device (game screen).',
      beats=[('0-3s', 'The bathroom door opens and Lily walks out, eyes on the floor.'),
             ('3-6s', 'Seila asks what happened; Lily answers with a flat voice.'),
             ('6-8s', 'Seila hugs her; Lily turns her face away.'),
             ('8-10s', 'Lily runs to the couch and dives into a game on her device while Gladias and Seila exchange a worried glance.')],
      narr=('N9', narr[8][2], narr[8][3]),
      dial=[('Lily', 'flat, muffled', '歴史のテスト、六十点。…まあ、いいけど', 'Sixty percent on the history test. ...Whatever.'),
            ('Seila', 'gentle', '全部が得意じゃなくてもいいのよ', 'You don\'t have to be good at everything.')],
      audio='Bathroom door click, a soft sad piano motif, faint game sounds from the device.',
      prompt='A quiet tween girl in a lavender hoodie walks out of a bathroom looking at the floor, her mother gently hugs her but she turns her face away, '
             'she sits on the couch and disappears into a game on her device as her parents share a worried look.' + STYLE_TAIL),
 dict(n=19, title='Family dinner and plans', loc='Family dining table',
      assets='All five family members, food truck bag, food boxes with numbers, city panel G.',
      beats=[('0-3s', 'The doorbell rings. Gladias opens the door and carries a bag of food boxes to the table.'),
             ('3-6s', 'He hands each person the box with their number. Zven happily tears his open.'),
             ('6-8s', 'Lily quietly joins the table. Everyone eats, warm light overhead.'),
             ('8-10s', 'A close two-shot of Zven and Febric as they talk about Uncle Vil, then a soft laugh.')],
      narr=None,
      dial=[('Seila', 'thoughtful', '私はフリータウンに行こうかな', 'I think I\'ll go to Freetown.'),
            ('Gladias', 'relaxed', '僕は森を歩くよ', 'I\'ll go walk in the forest.'),
            ('Zven', 'bright', 'ヴィルおじさん、大好き！', 'I love Uncle Vil!'),
            ('Febric', 'insisting', 'ぼくにとっては“パパ”だよ！', 'To me he\'s Dad!')],
      audio='Cutlery, chatter, warm acoustic guitar.',
      prompt='A cozy dinner table where a father hands numbered food boxes to his family, a quiet girl joins, the family eats under warm light, '
             'a small boy and a tall teen banter with bright smiles.' + STYLE_TAIL),
 dict(n=20, title='The anonymous message', loc='Family dining table',
      assets='Gladias, hand device (message card), family in the background.',
      beats=[('0-3s', 'Warm shot of the family eating together. Soft laughter.'),
             ('3-6s', 'Gladias\'s device buzzes on the table. He picks it up and the smile fades.'),
             ('6-8s', 'Extreme close-up on the screen: a message card appears from Anonymous with a verified reputation badge, followed by a second message.'),
             ('8-10s', 'Zoom into his stunned eyes as the music cuts out. Hard cut to black.')],
      narr=('N10', narr[9][2], narr[9][3]),
      dial=[('On-screen message 1', 'text only', 'コンサートで見かけました。あなたが会の人間だと知っています', 'I saw you at the concert. I know you are in the Order.'),
            ('On-screen message 2', 'text only', '通報して賞金を得るつもりはありません。ただ、お願いがあります', 'I will not report you for the bounty. But I have a request.')],
      audio='Warm music slowly thins, device buzz, a low drone, then silence at the cut to black.',
      prompt='A father at a warm family dinner table looks down as his hand device buzzes, close-up of two anonymous message cards with a verified badge, '
             'extreme close-up of his stunned eyes, the sounds fade to silence and the screen cuts to black.' + STYLE_TAIL),
]

def scene_card(s):
    n = s['n']
    hdr = Table([[P('SCENE %02d' % n, st_hdr), P(s['title'], st_hdr), P(tc(n), S('tcr', fontName='Helvetica-Bold', fontSize=9, leading=13, textColor=colors.HexColor('#9fe0cf'), alignment=2))]],
                colWidths=[22 * mm, 108 * mm, 44 * mm])
    hdr.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), INDIGO),
                             ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
                             ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
    rows = []
    rows.append([P('LOCATION', st_label), P(s['loc'], st_cell)])
    rows.append([P('ASSETS', st_label), P(s['assets'], st_cell)])
    rows.append([P('VISUAL GUIDANCE', st_label),
                 [P('<b>%s</b>  %s' % (a, b), st_beat) for a, b in s['beats']]])
    if s['narr']:
        nid, nj, ne = s['narr']
        rows.append([P('NARRATION', st_label),
                     [P('%s  <font color="#888888">(narrator, calm)</font>' % nid, st_spk), P(jp(nj), st_jp_small), P(ne, st_en)]])
    else:
        rows.append([P('NARRATION', st_label), P('None in this scene.', st_cell)])
    if s['dial']:
        cell = []
        for sp, kind, j, e in s['dial']:
            cell += dl(sp, kind, j, e)
        rows.append([P('DIALOGUE', st_label), cell])
    else:
        rows.append([P('DIALOGUE', st_label), P('None in this scene.', st_cell)])
    rows.append([P('AUDIO / SFX', st_label), P(s['audio'], st_cell)])
    rows.append([P('VIDEO PROMPT', st_label), P(s['prompt'], st_prompt)])
    t = Table(rows, colWidths=[28 * mm, 146 * mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), LIGHT),
        ('BACKGROUND', (1, len(rows) - 1), (1, len(rows) - 1), colors.HexColor('#f6f5fa')),
        ('GRID', (0, 0), (-1, -1), 0.4, LINE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return [hdr, t, Spacer(1, 5 * mm)]

for s in scenes:
    story += [KeepTogether(scene_card(s))]

story += [PageBreak()]

# ================= 7. COVERAGE =================
story += [P('7. Dialogue coverage checklist', st_h1)]
story += [P('Every spoken or on-screen line in Chapter 1, and what happened to it in the 20-scene adaptation.')]
cov = [
    ['Emerald audio lesson while Gladias walks', 'Scene 2', 'Used, adapted and shortened'],
    ['Drone boy shouts about points', 'Scene 4', 'Used, adapted'],
    ['Grandmother thanks the couple', 'Scene 4', 'Used (a short spoken thank you added)'],
    ['Gladias whispers a pause to Emerald', 'Scene 5', 'Used, adapted'],
    ['Vote screen and building details', 'Scene 6', 'On-screen text only'],
    ['Gladias weighs the aeroplane building tax', 'Scene 7', 'Compressed to one thought line'],
    ['Gate machine confirms entry', 'Scene 7', 'Used, adapted'],
    ['Dreadknot song lines', 'Scene 8', 'Replaced by a new placeholder lyric'],
    ['Rubric tiers and precedent search', 'Scene 9', 'On-screen text; long reading cut'],
    ['Gladias debates advocating vs showcasing violence', 'Scene 9', 'Compressed to one thought line'],
    ['Chat between two Acolytes; probability reasoning', 'Scene 10', 'On-screen text and floating numbers, no voice'],
    ['Gladias picks Tier 3', 'Scene 10', 'Used as a thought line'],
    ['Heckler exposes the Order member', 'Scene 11', 'Used, adapted'],
    ['Gladias tricks the burly man with the Arctic Emperor line', 'Scene 12', 'Used, adapted'],
    ['Gladias orders the device to delete everything and reboot', 'Scene 13', 'Used, adapted'],
    ['Device replies that four files were deleted', 'Scene 13', 'Used, adapted'],
    ['Bus ad text (lifelong learning; drink brand)', 'Scene 15', 'On-screen text only'],
    ['Gladias wishes there were more fun', 'Scene 15', 'Used as a thought line'],
    ['Gladias calls for Seila; Seila answers; Zven announces Dad', 'Scene 16', 'Used, adapted'],
    ['Food truck plan and number orders', 'Scene 17', 'Compressed (four lines); Hreda and Lily\'s number cut'],
    ['Lily reports her exam mark; Seila comforts her', 'Scene 18', 'Used, adapted'],
    ['Uncle Vil and Aunt Daia pickup plan', 'Scene 18', 'Conveyed by narrator line N9'],
    ['Seila\'s Freetown plan and Gladias\'s forest plan', 'Scene 19', 'Compressed to short lines'],
    ['Zven and Febric on Uncle Vil', 'Scene 19', 'Used, adapted'],
    ['Anonymous messages to Gladias', 'Scene 20', 'On-screen text (both messages)'],
]
story += [simple_table(['Source moment', 'Where', 'Status'], cov, [90 * mm, 22 * mm, 62 * mm])]
story += [Spacer(1, 4 * mm)]
story += [P('Production tips', st_h2)]
story += bullets([
    'Lock the character sheets first, then the city sheet, then generate scenes in order so you can carry visual continuity forward.',
    'Record the Japanese narration and dialogue first, then trim each clip to the audio, not the other way around.',
    'Scenes 11 to 13 form one continuous action sequence. Generate them with the same reference images and keep the crowd lighting identical.',
    'If a clip cannot fit all dialogue, drop the narration in that scene first (the story still reads through the visuals).',
    'Keep the hood-down and hood-up rule for Gladias\'s robe consistent across scenes.',
])

doc.build(story)
print('built', OUT)
