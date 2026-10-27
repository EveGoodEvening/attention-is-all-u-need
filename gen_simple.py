import math, sys

OUT = sys.argv[1]

W9 = ["小狗", "没有", "过", "马路", "因为", "它", "太", "累", "了"]
X9 = [56 + i * 86 for i in range(9)]


def words_row(y, hl=None, small=False, xs=X9, words=W9, bw=72, bh=44):
    s = []
    for i, (x, w) in enumerate(zip(xs, words)):
        cls = "wbox"
        if hl and i in hl:
            cls += " " + hl[i]
        s.append(f'<rect class="{cls}" x="{x-bw/2}" y="{y}" width="{bw}" height="{bh}" rx="10"/>')
        tc = "wtxt on" if hl and hl.get(i) == "hl" else "wtxt"
        s.append(f'<text class="{tc}" x="{x}" y="{y+bh/2+7}" text-anchor="middle">{w}</text>')
    return "\n".join(s)


def arcs(src, weights, y, color_cls, xs=X9, scale=34, hmul=0.42, minw=1.2):
    s = []
    x1 = xs[src]
    for j, w in weights.items():
        x2 = xs[j]
        h = 30 + abs(x2 - x1) * hmul
        mx = (x1 + x2) / 2
        sw = max(minw, w * scale)
        op = 0.25 + 0.75 * min(1, w / max(weights.values()))
        s.append(f'<path class="{color_cls}" d="M{x1} {y} Q{mx} {y-2*h} {x2} {y}" '
                 f'stroke-width="{sw:.1f}" stroke-opacity="{op:.2f}" fill="none" stroke-linecap="round"/>')
    return "\n".join(s)


# ---------- hero heatmap ----------
def hero():
    n = 9
    cell = 40
    ox, oy = 92, 70
    # plausible self-attention weights (rows = who is looking)
    M = [[0.0] * n for _ in range(n)]
    for i in range(n):
        M[i][i] = 0.35
        if i > 0: M[i][i - 1] = 0.15
        if i < n - 1: M[i][i + 1] = 0.15
    M[5] = [0.62, 0.02, 0.02, 0.08, 0.04, 0.08, 0.03, 0.09, 0.02]  # 它 -> 小狗
    M[2][3] = 0.6   # 过 -> 马路
    M[3][2] = 0.45
    M[7][5] = 0.4   # 累 -> 它
    M[7][6] = 0.35
    M[1][2] = 0.5   # 没有 -> 过
    s = [f'<svg class="fig" viewBox="0 0 470 470" role="img" aria-label="一张 9×9 的格子图：每一行是一个词，它在看哪个词，格子就越亮。“它”这一行最亮的格子在“小狗”。">']
    for i in range(n):
        s.append(f'<text class="hm-lab" x="{ox-10}" y="{oy+i*cell+cell/2+5}" text-anchor="end">{W9[i]}</text>')
        s.append(f'<text class="hm-lab" x="{ox+i*cell+cell/2}" y="{oy-12}" text-anchor="middle">{W9[i]}</text>')
        for j in range(n):
            v = M[i][j]
            s.append(f'<rect x="{ox+j*cell+2}" y="{oy+i*cell+2}" width="{cell-4}" height="{cell-4}" rx="6" '
                     f'class="hm" fill-opacity="{0.06+0.94*min(1,v/0.62):.2f}"/>')
    # highlight row 它
    s.append(f'<rect class="hm-ring" x="{ox-2}" y="{oy+5*cell-2}" width="{n*cell+4}" height="{cell+4}" rx="9" fill="none"/>')
    s.append(f'<text class="hm-axis" x="{ox-10}" y="{oy-38}" text-anchor="end">谁在看 ↓</text>')
    s.append(f'<text class="hm-axis" x="{ox}" y="{oy-38}">被看的词 →</text>')
    s.append(f'<text class="hm-note" x="{ox}" y="{oy+n*cell+30}">“它”这一行，最亮的是“小狗”</text>')
    s.append("</svg>")
    return "\n".join(s)


# ---------- RNN chain ----------
def rnn():
    s = ['<svg class="fig" viewBox="0 0 800 250" role="img" aria-label="九个词排成一排，记忆一格一格往后传；“小狗”的信息越传越淡，到“它”时几乎看不见了。">']
    s.append('<defs><marker id="ar1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="mk"/></marker></defs>')
    for i, x in enumerate(X9):
        op = max(0.06, 1 - i * 0.17)
        s.append(f'<circle class="mem" cx="{x}" cy="70" r="26"/>')
        s.append(f'<circle class="memdot" cx="{x}" cy="70" r="12" fill-opacity="{op:.2f}"/>')
        s.append(f'<line class="up" x1="{x}" y1="150" x2="{x}" y2="100" marker-end="url(#ar1)"/>')
        if i < 8:
            s.append(f'<line class="chain" x1="{x+28}" y1="70" x2="{X9[i+1]-30}" y2="70" marker-end="url(#ar1)"/>')
    s.append(words_row(152, hl={0: "hl", 5: "hl2"}))
    s.append(f'<text class="cap-in" x="{X9[0]}" y="28" text-anchor="middle">记得很清楚</text>')
    s.append(f'<text class="cap-in" x="{X9[5]}" y="28" text-anchor="middle">“小狗”是谁来着？</text>')
    s.append(f'<text class="step" x="{X9[0]}" y="226" text-anchor="middle">第 1 步</text>')
    s.append(f'<text class="step" x="{X9[8]}" y="226" text-anchor="middle">第 9 步</text>')
    s.append('</svg>')
    return "\n".join(s)


# ---------- attention arcs ----------
def attn():
    w = {0: 0.62, 1: 0.03, 2: 0.03, 3: 0.08, 4: 0.04, 6: 0.03, 7: 0.10, 8: 0.02}
    s = ['<svg class="fig" viewBox="0 -30 800 330" role="img" aria-label="“它”同时连线到所有词，连到“小狗”的线最粗。">']
    s.append(arcs(5, w, 230, "arc-a", scale=26))
    s.append(words_row(232, hl={0: "hl", 5: "hl2"}))
    s.append(f'<text class="pct" x="{(X9[0]+X9[5])/2}" y="{230-(30+430*0.42)-0.62*26/2-8:.1f}" text-anchor="middle">62%</text>')
    s.append('</svg>')
    return "\n".join(s)


# ---------- QKV ----------
def qkv():
    rows = [("小狗", "动物", 0.62), ("累", "状态", 0.10), ("马路", "地点", 0.08), ("其他词", "……", 0.20)]
    ys = [70, 150, 230, 310]
    s = ['<svg class="fig" viewBox="0 0 900 380" role="img" aria-label="“它”拿着一张问题卡片，去和每个词的标签比对；匹配度最高的是“小狗”，于是“它”的新含义大部分来自“小狗”。">']
    s.append('<defs><marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker></defs>')
    heads = [(110, "① 提问", "Query"), (360, "② 标签", "Key"), (535, "③ 匹配度", ""), (700, "④ 内容", "Value"), (830, "⑤ 混合", "")]
    for x, a, b in heads:
        s.append(f'<text class="colh" x="{x}" y="22" text-anchor="middle">{a}</text>')
        if b:
            s.append(f'<text class="colsub" x="{x}" y="40" text-anchor="middle">{b}</text>')
    # Q card
    s.append('<rect class="card q" x="30" y="140" width="160" height="110" rx="14"/>')
    s.append('<text class="wtxt big" x="110" y="182" text-anchor="middle">它</text>')
    s.append('<text class="small" x="110" y="212" text-anchor="middle">“我指的是</text>')
    s.append('<text class="small" x="110" y="232" text-anchor="middle">哪个动物？”</text>')
    for (word, tag, wt), y in zip(rows, ys):
        s.append(f'<path class="link" d="M190 195 C250 195 250 {y} 290 {y}" fill="none" stroke-width="{1+wt*6:.1f}" stroke-opacity="{0.3+0.7*wt/0.62:.2f}"/>')
        s.append(f'<rect class="card k" x="290" y="{y-24}" width="140" height="48" rx="10"/>')
        s.append(f'<text class="wtxt" x="330" y="{y+7}" text-anchor="middle" style="font-size:{17 if len(word)>2 else 19}px">{word}</text>')
        s.append(f'<text class="tag" x="395" y="{y+5}" text-anchor="middle">{tag}</text>')
        # bar
        bw = 120 * wt
        s.append(f'<rect class="barbg" x="470" y="{y-10}" width="120" height="20" rx="5"/>')
        s.append(f'<rect class="bar" x="470" y="{y-10}" width="{bw:.1f}" height="20" rx="5"/>')
        s.append(f'<text class="num" x="600" y="{y+5}">{int(wt*100)}%</text>')
        s.append(f'<rect class="card v" x="660" y="{y-20}" width="80" height="40" rx="8" fill-opacity="{0.15+0.85*wt/0.62:.2f}"/>')
        s.append(f'<text class="{"vt on" if wt > 0.5 else "vt"}" x="700" y="{y+6}" text-anchor="middle">{word}</text>')
        s.append(f'<line class="link" x1="742" y1="{y}" x2="790" y2="190" stroke-width="{1+wt*6:.1f}" stroke-opacity="{0.3+0.7*wt/0.62:.2f}"/>')
    s.append('<circle class="mix" cx="830" cy="190" r="40"/>')
    s.append('<text class="wtxt big" x="830" y="199" text-anchor="middle" style="fill:var(--on-accent)">它</text>')
    s.append('<text class="small" x="830" y="254" text-anchor="middle">≈ 小狗</text>')
    s.append('</svg>')
    return "\n".join(s)


# ---------- multi-head ----------
def heads():
    xs = [50 + i * 80 for i in range(9)]
    panels = [
        ("head1", "1 号头：“它”是谁？", 5, {0: 0.8, 3: 0.08, 7: 0.06}),
        ("head2", "2 号头：“它”怎么了？", 5, {7: 0.7, 6: 0.2, 0: 0.06}),
        ("head3", "3 号头：“过”什么？", 2, {3: 0.8, 1: 0.12}),
    ]
    out = []
    for cls, title, src, w in panels:
        hl = {src: "hl-" + cls}
        s = [f'<svg class="fig head" viewBox="0 0 740 190" role="img" aria-label="{title}">']
        s.append(f'<text class="colh" x="10" y="26">{title}</text>')
        s.append(arcs(src, w, 136, "arc-" + cls, xs=xs, scale=12, hmul=0.16, minw=1.5))
        s.append(words_row(138, hl=hl, xs=xs, bw=64, bh=40))
        s.append('</svg>')
        out.append("\n".join(s))
    return out


# ---------- position ----------
def position():
    s = ['<svg class="fig" viewBox="0 0 800 380" role="img" aria-label="“狗咬人”和“人咬狗”倒进同一个袋子，看起来一模一样；给每个字贴上座位号后就能分清。座位号像一只有几根指针的钟，每个座位上几根指针的角度组合都不一样。">']
    s.append('<defs><marker id="ar3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker></defs>')
    def word(x, y, w, badge=None):
        hl = w == "狗"
        r = [f'<rect class="wbox{" hl" if hl else ""}" x="{x}" y="{y}" width="52" height="44" rx="10"/>',
             f'<text class="wtxt{" on" if hl else ""}" x="{x+26}" y="{y+29}" text-anchor="middle">{w}</text>']
        if badge:
            r.append(f'<circle class="seat2" cx="{x+48}" cy="{y+4}" r="12"/>')
            r.append(f'<text class="seatn2" x="{x+48}" y="{y+9}" text-anchor="middle">{badge}</text>')
        return "\n".join(r)
    s.append('<text class="colh" x="40" y="26">不贴座位号</text>')
    for k, ws in enumerate([["狗", "咬", "人"], ["人", "咬", "狗"]]):
        for i, w in enumerate(ws):
            s.append(word(40 + i * 62, 50 + k * 80, w))
    s.append('<line class="chain" x1="230" y1="72" x2="288" y2="108" marker-end="url(#ar3)"/>')
    s.append('<line class="chain" x1="230" y1="152" x2="288" y2="124" marker-end="url(#ar3)"/>')
    s.append('<ellipse class="bag" cx="345" cy="116" rx="52" ry="44"/>')
    s.append('<text class="wtxt" x="345" y="110" text-anchor="middle">狗 咬 人</text>')
    s.append('<text class="small" x="345" y="134" text-anchor="middle">分不清！</text>')
    s.append('<text class="colh" x="460" y="26">贴上座位号</text>')
    for k, ws in enumerate([["狗", "咬", "人"], ["人", "咬", "狗"]]):
        y = 50 + k * 80
        for i, w in enumerate(ws):
            s.append(word(460 + i * 62, y, w, badge=str(i + 1)))
        s.append(f'<text class="small" x="660" y="{y+29}">{"狗在 1 号 → 狗咬人" if k==0 else "狗在 3 号 → 人咬狗"}</text>')
    # clocks: one hand per speed; each hand's angle is one sin/cos pair
    s.append('<text class="colh" x="40" y="222">座位号怎么来？像一只有几根指针的钟</text>')
    hands = [(1.0, 40, 3, "wave1", "秒针 转得快"), (0.35, 31, 4, "wave2", "分针"), (0.1, 22, 6, "wave3", "时针 转得慢")]
    for k, (_, _, w, cls, lab) in enumerate(hands):
        y = 268 + k * 30
        s.append(f'<line class="{cls}" x1="40" y1="{y}" x2="66" y2="{y}" style="stroke-width:{w};stroke-linecap:round"/>')
        s.append(f'<text class="small" x="76" y="{y+5}">{lab}</text>')
    seats = [(320, 1), (500, 2), (680, 3)]
    cy = 300
    for x, p in seats:
        s.append(f'<circle class="grid" cx="{x}" cy="{cy}" r="46" fill="none" style="stroke-width:2"/>')
        for t in range(12):
            a = t * math.pi / 6
            r0 = 40 if t % 3 else 36
            s.append(f'<line class="grid" x1="{x + r0*math.sin(a):.1f}" y1="{cy - r0*math.cos(a):.1f}" x2="{x + 46*math.sin(a):.1f}" y2="{cy - 46*math.cos(a):.1f}"/>')
        for om, L, w, cls, _ in reversed(hands):
            a = om * p
            s.append(f'<line class="{cls}" x1="{x}" y1="{cy}" x2="{x + L*math.sin(a):.1f}" y2="{cy - L*math.cos(a):.1f}" style="stroke-width:{w};stroke-linecap:round"/>')
        s.append(f'<circle class="seat2" cx="{x}" cy="{cy}" r="4"/>')
        s.append(f'<circle class="seat2" cx="{x}" cy="364" r="12"/>')
        s.append(f'<text class="seatn2" x="{x}" y="369" text-anchor="middle">{p}</text>')
    s.append('</svg>')
    return "\n".join(s)


def arch():
    s = ['<svg class="fig" viewBox="0 0 960 520" role="img" aria-label="左边是编码器，一次读懂整句英文；右边是解码器，看着已写好的德文词和读懂的内容，写出下一个词。两边各叠 6 层。">']
    s.append('<defs><marker id="ar4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker>'
             '<marker id="ar5" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="mk2"/></marker></defs>')
    top = 96
    def tower(x, title, sub, layers):
        h = 60 + len(layers) * 56
        r = [f'<text class="colh" x="{x+130}" y="24" text-anchor="middle">{title}</text>',
             f'<text class="colsub" x="{x+130}" y="44" text-anchor="middle">{sub}</text>']
        for k in range(5, 0, -1):
            r.append(f'<rect class="plate" x="{x+k*6}" y="{top-k*6}" width="260" height="{h}" rx="14"/>')
        r.append(f'<rect class="tower" x="{x}" y="{top}" width="260" height="{h}" rx="14"/>')
        for i, (lab, c) in enumerate(layers):
            yy = top + 20 + i * 56
            r.append(f'<rect class="sub {c}" x="{x+20}" y="{yy}" width="220" height="42" rx="9"/>')
            r.append(f'<text class="subt" x="{x+130}" y="{yy+27}" text-anchor="middle">{lab}</text>')
        r.append(f'<text class="times" x="{x+250}" y="{top+h-12}" text-anchor="end">× 6 层</text>')
        return "\n".join(r), top + h
    enc, enc_bot = tower(40, "编码器", "负责读懂", [("词和词互相看", "sa"), ("再消化一下", "ff")])
    dec, dec_bot = tower(520, "解码器", "负责写出", [("看已写好的词", "sa"), ("回头看原文", "ca"), ("再消化一下", "ff")])
    s.append(enc); s.append(dec)
    ca_y = top + 20 + 56 + 21
    s.append(f'<path class="cross" d="M300 {top+40} C410 {top+40} 410 {ca_y} 536 {ca_y}" fill="none" marker-end="url(#ar5)"/>')
    s.append(f'<text class="crosst" x="410" y="{top+30}" text-anchor="middle">读懂的内容</text>')
    # encoder input
    s.append(f'<line class="chain" x1="170" y1="420" x2="170" y2="{enc_bot+6}" marker-end="url(#ar4)"/>')
    for i, w in enumerate(["The", "cat", "is", "tired"]):
        s.append(f'<rect class="wbox" x="{48+i*62}" y="428" width="56" height="38" rx="9"/>')
        s.append(f'<text class="wtxt en" x="{76+i*62}" y="453" text-anchor="middle">{w}</text>')
    s.append('<text class="small" x="170" y="496" text-anchor="middle">英文原句（一次全部读入）</text>')
    # decoder input: words already written
    s.append(f'<line class="chain" x1="650" y1="420" x2="650" y2="{dec_bot+6}" marker-end="url(#ar4)"/>')
    for i, w in enumerate(["Die", "Katze", "ist"]):
        s.append(f'<rect class="wbox" x="{548+i*70}" y="428" width="64" height="38" rx="9"/>')
        s.append(f'<text class="wtxt en" x="{580+i*70}" y="453" text-anchor="middle">{w}</text>')
    s.append('<text class="small" x="650" y="496" text-anchor="middle">已经写好的德文词</text>')
    # output: next word
    oy = top + 100
    s.append(f'<line class="chain" x1="812" y1="{oy}" x2="846" y2="{oy}" marker-end="url(#ar4)"/>')
    s.append(f'<rect class="wbox hl" x="852" y="{oy-20}" width="80" height="40" rx="9"/>')
    s.append(f'<text class="wtxt en on" x="892" y="{oy+6}" text-anchor="middle">müde</text>')
    s.append(f'<text class="small" x="892" y="{oy-32}" text-anchor="middle">下一个词</text>')
    s.append(f'<path class="loop" d="M932 {oy+10} C955 {oy+120} 900 410 758 447" fill="none" marker-end="url(#ar4)"/>')
    s.append('<text class="small" x="790" y="482">写完放回去，接着写</text>')
    s.append('</svg>')
    return "\n".join(s)


def speed():
    X = 224
    s = ['<svg class="fig" viewBox="0 0 800 230" role="img" aria-label="旧方法要排队算 9 步；Transformer 9 个词一起算，一步完成。">']
    s.append('<text class="colh" x="20" y="36">旧方法：排队</text>')
    for i in range(9):
        x = X + i * 62
        s.append(f'<rect class="tick" x="{x}" y="14" width="52" height="34" rx="7"/>')
        s.append(f'<text class="small" x="{x+26}" y="37" text-anchor="middle">{W9[i]}</text>')
    s.append(f'<text class="num" x="{X}" y="74">⏱ 9 步</text>')
    s.append('<text class="colh" x="20" y="142">新方法：一起上</text>')
    for i in range(9):
        x = X + i * 62
        s.append(f'<rect class="tick on" x="{x}" y="120" width="52" height="34" rx="7"/>')
        s.append(f'<text class="small on" x="{x+26}" y="143" text-anchor="middle">{W9[i]}</text>')
    s.append(f'<rect class="bracket" x="{X-4}" y="114" width="562" height="46" rx="10" fill="none"/>')
    s.append(f'<text class="num" x="{X}" y="186">⏱ 1 步（显卡最擅长同时干很多事）</text>')
    s.append('</svg>')
    return "\n".join(s)


def bleu():
    data = [("以前最好的", 26.36), ("Transformer", 28.4)]
    W, x0, x1 = 760, 160, 700
    sc = (x1 - x0) / 30
    s = [f'<svg class="fig" viewBox="0 0 {W} 190" role="img" aria-label="英译德翻译得分：以前最好的 26.36，Transformer 28.4。">']
    for t in range(0, 31, 10):
        x = x0 + t * sc
        s.append(f'<line class="grid" x1="{x}" y1="14" x2="{x}" y2="140"/>')
        s.append(f'<text class="axis" x="{x}" y="160" text-anchor="middle">{t}</text>')
    for i, (lab, v) in enumerate(data):
        y = 24 + i * 58
        last = i == len(data) - 1
        s.append(f'<text class="blab{" strong" if last else ""}" x="{x0-12}" y="{y+27}" text-anchor="end">{lab}</text>')
        s.append(f'<rect class="{"bar" if last else "bar dim"}" x="{x0}" y="{y+6}" width="{v*sc:.1f}" height="32" rx="6"/>')
        s.append(f'<text class="num{" strong" if last else ""}" x="{x0+v*sc+10:.1f}" y="{y+28}">{v}</text>')
    s.append(f'<text class="axis" x="{x1}" y="182" text-anchor="end">翻译得分（BLEU：和人工翻译有多像，越高越好）</text>')
    s.append('</svg>')
    return "\n".join(s)


def legacy():
    items = [(2017, "Transformer", "本论文"), (2018, "GPT", "会写文字"), (2018, "BERT", "会读懂文字"),
             (2020, "GPT-3", "大很多"), (2022, "ChatGPT", "会聊天"), (2023, "Claude 等", "你正在用的")]
    s = ['<svg class="fig" viewBox="0 0 860 240" role="img" aria-label="从 2017 年的 Transformer 出发，长出了 GPT、BERT、ChatGPT、Claude 等一大家子。">']
    s.append('<line class="spine" x1="60" y1="120" x2="820" y2="120"/>')
    for i, (yr, name, sub) in enumerate(items):
        x = 80 + i * 145
        up = i % 2 == 0
        first = i == 0
        r = 16 if first else 10
        s.append(f'<circle class="{"node first" if first else "node"}" cx="{x}" cy="120" r="{r}"/>')
        ty = 58 if up else 172
        s.append(f'<line class="grid" x1="{x}" y1="{120-r if up else 120+r}" x2="{x}" y2="{ty+28 if up else ty-22}"/>')
        s.append(f'<text class="yr" x="{x}" y="{ty-20 if up else ty+4}" text-anchor="middle">{yr}</text>')
        s.append(f'<text class="{"wtxt strong" if first else "wtxt"}" x="{x}" y="{ty+2 if up else ty+28}" text-anchor="middle">{name}</text>')
        s.append(f'<text class="small" x="{x}" y="{ty+22 if up else ty+48}" text-anchor="middle">{sub}</text>')
    s.append('</svg>')
    return "\n".join(s)


tpl = open(sys.argv[2], encoding="utf-8").read()
h1, h2, h3 = heads()
rep = {
    "{{HERO}}": hero(), "{{RNN}}": rnn(), "{{ATTN}}": attn(), "{{QKV}}": qkv(),
    "{{HEAD1}}": h1, "{{HEAD2}}": h2, "{{HEAD3}}": h3, "{{POS}}": position(),
    "{{ARCH}}": arch(), "{{SPEED}}": speed(), "{{BLEU}}": bleu(), "{{LEGACY}}": legacy(),
}
for k, v in rep.items():
    tpl = tpl.replace(k, v)
open(OUT, "w", encoding="utf-8").write(tpl)
print("ok", len(tpl))
