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


# ---------- the task ----------
def task():
    s = ['<svg class="fig" viewBox="0 0 830 200" role="img" aria-label="左边一串英文词 The cat is tired 进入一台翻译机，右边出来一串德文词 Die Katze ist müde。">']
    s.append('<defs><marker id="ar6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker></defs>')
    y = 78
    s.append('<text class="colh" x="141" y="50" text-anchor="middle">一串词进</text>')
    for i, w in enumerate(["The", "cat", "is", "tired"]):
        s.append(f'<rect class="wbox" x="{20+i*62}" y="{y}" width="56" height="44" rx="9"/>')
        s.append(f'<text class="wtxt en" x="{48+i*62}" y="{y+28}" text-anchor="middle">{w}</text>')
    s.append(f'<text class="small" x="141" y="{y+76}" text-anchor="middle">英文</text>')
    s.append(f'<line class="chain" x1="272" y1="{y+22}" x2="322" y2="{y+22}" marker-end="url(#ar6)"/>')
    s.append(f'<rect class="tower" x="330" y="{y-28}" width="140" height="100" rx="16"/>')
    s.append(f'<text class="wtxt big" x="400" y="{y+34}" text-anchor="middle" style="fill:var(--accent)">？</text>')
    s.append(f'<text class="small" x="400" y="{y+100}" text-anchor="middle">翻译机</text>')
    s.append(f'<line class="chain" x1="478" y1="{y+22}" x2="528" y2="{y+22}" marker-end="url(#ar6)"/>')
    s.append('<text class="colh" x="673" y="50" text-anchor="middle">另一串词出</text>')
    for i, w in enumerate(["Die", "Katze", "ist", "müde"]):
        s.append(f'<rect class="wbox" x="{536+i*70}" y="{y}" width="64" height="44" rx="9"/>')
        s.append(f'<text class="wtxt en" x="{568+i*70}" y="{y+28}" text-anchor="middle">{w}</text>')
    s.append(f'<text class="small" x="673" y="{y+76}" text-anchor="middle">德文</text>')
    s.append('</svg>')
    return "\n".join(s)


# ---------- what people used before 2017 ----------
def before():
    items = [("2000 年代", "统计翻译", "按词组查表拼"), ("2014", "Seq2Seq", "LSTM：一个读一个写"),
             ("2015", "Seq2Seq + 注意力", "写时回头看原文"), ("2016", "谷歌翻译 GNMT", "8 层 LSTM 叠起来"),
             ("2017 年 5 月", "ConvS2S", "改用卷积，想少排队")]
    xs = [90 + i * 165 for i in range(5)]
    s = ['<svg class="fig" viewBox="0 0 860 230" role="img" aria-label="2017 年以前的翻译模型：先是统计翻译；2014 到 2016 年是 RNN（LSTM）当家，2015 年给 RNN 加上了注意力；2017 年有人改用卷积。">']
    s.append(f'<path class="brace" d="M{xs[1]-40} 84 V66 H{xs[3]+40} V84"/>')
    s.append(f'<text class="colh" x="{xs[2]}" y="54" text-anchor="middle">RNN 当家：一个词一个词读</text>')
    s.append(f'<line class="spine" x1="40" y1="110" x2="820" y2="110"/>')
    for i, ((yr, name, sub), x) in enumerate(zip(items, xs)):
        hot = i == 2
        s.append(f'<circle class="{"node first" if hot else "node"}" cx="{x}" cy="110" r="{14 if hot else 10}"/>')
        s.append(f'<text class="yr" x="{x}" y="150" text-anchor="middle">{yr}</text>')
        s.append(f'<text class="{"wtxt strong" if hot else "wtxt"}" x="{x}" y="178" text-anchor="middle">{name}</text>')
        s.append(f'<text class="small" x="{x}" y="202" text-anchor="middle">{sub}</text>')
    s.append('</svg>')
    return "\n".join(s)


# ---------- parts vs. assembly ----------
def parts():
    s = ['<svg class="fig" viewBox="0 0 860 414" role="img" aria-label="上半部分：Seq2Seq 架构由编码器和解码器组成，编码器把英文句子读成向量，解码器根据向量逐词写出德文。下半部分：编码器和解码器内部可以用不同的网络实现：用循环网络是经典 Seq2Seq，用卷积网络是 ConvS2S，只用注意力是 Transformer。">']
    s.append('<defs><marker id="ar7" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker></defs>')
    s.append('<text class="colh" x="430" y="26" text-anchor="middle">架构（architecture）：Seq2Seq = 编码器 + 解码器</text>')
    for x, lab, desc in [(100, "编码器（encoder）", "把输入句子读成向量"), (520, "解码器（decoder）", "根据向量逐词写出")]:
        s.append(f'<rect class="tower" x="{x}" y="46" width="240" height="98" rx="14"/>')
        s.append(f'<text class="subt" x="{x+120}" y="74" text-anchor="middle">{lab}</text>')
        s.append(f'<text class="small" x="{x+120}" y="96" text-anchor="middle">{desc}</text>')
        s.append(f'<rect class="slot" x="{x+30}" y="108" width="180" height="26" rx="7"/>')
        s.append(f'<text class="small" x="{x+120}" y="126" text-anchor="middle">内部用什么网络实现？</text>')
    s.append('<line class="chain" x1="342" y1="94" x2="408" y2="94" marker-end="url(#ar7)"/>')
    s.append('<circle class="mix" cx="430" cy="94" r="14"/>')
    s.append('<line class="chain" x1="446" y1="94" x2="514" y2="94" marker-end="url(#ar7)"/>')
    s.append('<text class="small" x="430" y="132" text-anchor="middle">读懂的内容（向量）</text>')
    for cx, ws in [(220, ["The", "cat", "is", "tired"]), (640, ["Die", "Katze", "ist", "müde"])]:
        x0 = cx - (4 * 54 - 6) / 2
        for i, w in enumerate(ws):
            s.append(f'<rect class="wbox" x="{x0+i*54:.0f}" y="172" width="48" height="32" rx="8"/>')
            s.append(f'<text class="wtxt en" x="{x0+i*54+24:.0f}" y="193" text-anchor="middle" style="font-size:13px">{w}</text>')
    s.append('<line class="chain" x1="220" y1="170" x2="220" y2="150" marker-end="url(#ar7)"/>')
    s.append('<line class="chain" x1="640" y1="146" x2="640" y2="166" marker-end="url(#ar7)"/>')
    s.append('<text class="colh" x="430" y="238" text-anchor="middle">编码器、解码器内部，可以用不同的网络来实现：</text>')
    cols = [(150, "循环网络（RNN 类）", ["简单 RNN", "LSTM", "GRU"], "经典 Seq2Seq", "2014–2016 主流", False),
            (430, "卷积网络（CNN）", ["CNN"], "ConvS2S", "2017 年 5 月", False),
            (710, "只用注意力", ["注意力"], "Transformer", "2017 年 6 月 · 本论文", True)]
    for cx, head, chips, name, sub, hot in cols:
        s.append(f'<rect class="{"card hot" if hot else "card"}" x="{cx-128}" y="252" width="256" height="150" rx="14"/>')
        s.append(f'<text class="colh" x="{cx}" y="282" text-anchor="middle">{head}</text>')
        cw, gap = 74, 8
        x0 = cx - (len(chips) * cw + (len(chips) - 1) * gap) / 2
        for i, c in enumerate(chips):
            x = x0 + i * (cw + gap)
            s.append(f'<rect class="{"wbox hl" if hot else "wbox"}" x="{x:.0f}" y="298" width="{cw}" height="36" rx="8"/>')
            s.append(f'<text class="{"small on" if hot else "small"}" x="{x+cw/2:.0f}" y="321" text-anchor="middle" style="font-weight:700">{c}</text>')
        s.append(f'<text class="{"wtxt strong" if hot else "wtxt"}" x="{cx}" y="366" text-anchor="middle">= {name}</text>')
        s.append(f'<text class="small" x="{cx}" y="390" text-anchor="middle">{sub}</text>')
    s.append('</svg>')
    return "\n".join(s)


EN4 = ["The", "cat", "is", "tired"]
DE4 = ["Die", "Katze", "ist", "müde"]
W_KATZE = [0.10, 0.80, 0.05, 0.05]   # attention while writing "Katze"; shared by both add-on figures
SUB = "₁₂₃₄₅₆₇₈₉"


# ---------- attention add-on: before vs after ----------
def addon():
    hx = [60, 150, 240, 330]
    sx = [530, 620, 710, 800]
    s = ['<svg class="fig" viewBox="0 0 860 410" role="img" aria-label="上：2014 年原版 Seq2Seq，编码器读完整句后，只把最后一步的记忆 h₄ 交给解码器。下：2015 年加了注意力，解码器写 Katze 时，回头看原文全部 4 个词的记忆，其中 80% 看 cat。">']
    s.append('<defs><marker id="ar10" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker></defs>')

    def chains(yc, hot_s=None):
        r = []
        for xs, letter, words in [(hx, "h", EN4), (sx, "s", DE4)]:
            for i, x in enumerate(xs):
                cls = "mem hot" if (letter == "s" and i == hot_s) else "mem"
                r.append(f'<circle class="{cls}" cx="{x}" cy="{yc}" r="22"/>')
                r.append(f'<text class="wtxt en" x="{x}" y="{yc+6}" text-anchor="middle">{letter}{SUB[i]}</text>')
                hl = letter == "s" and i == hot_s
                r.append(f'<rect class="{"wbox hl" if hl else "wbox"}" x="{x-28}" y="{yc+32}" width="56" height="28" rx="7"/>')
                r.append(f'<text class="{"wtxt en on" if hl else "wtxt en"}" x="{x}" y="{yc+51}" text-anchor="middle" style="font-size:13px">{words[i]}</text>')
                if i < 3:
                    r.append(f'<line class="chain" x1="{x+24}" y1="{yc}" x2="{xs[i+1]-26}" y2="{yc}" marker-end="url(#ar10)"/>')
        r.append(f'<line class="chain" x1="{hx[3]+24}" y1="{yc}" x2="{sx[0]-26}" y2="{yc}" marker-end="url(#ar10)"/>')
        return "\n".join(r)

    # top: original
    yc = 100
    s.append('<text class="colh" x="20" y="34">2014 原版：读完整句，只交出最后一步的记忆</text>')
    s.append(chains(yc))
    s.append(f'<text class="small" x="430" y="{yc-12}" text-anchor="middle">整句压成 1 个向量</text>')
    s.append(f'<text class="small" x="195" y="{yc+84}" text-anchor="middle">编码器</text>')
    s.append(f'<text class="small" x="665" y="{yc+84}" text-anchor="middle">解码器</text>')
    # bottom: with attention
    yc = 320
    s.append('<text class="colh" x="20" y="210">2015 加注意力：每写一个词，都回头看原文的每个词</text>')
    for x, w in zip(hx, W_KATZE):
        h = 30 + abs(sx[1] - x) * 0.07  # keep arc peaks below the row title
        mx = (x + sx[1]) / 2
        s.append(f'<path class="arc-a" d="M{x} {yc-24} Q{mx} {yc-24-2*h:.0f} {sx[1]} {yc-24}" stroke-width="{max(1.5, w*14):.1f}" stroke-opacity="{0.3+0.7*w/max(W_KATZE):.2f}" fill="none" stroke-linecap="round"/>')
    s.append(chains(yc, hot_s=1))
    for x, w in zip(hx, W_KATZE):
        s.append(f'<text class="{"num strong" if w == max(W_KATZE) else "num"}" x="{x}" y="{yc+82}" text-anchor="middle">{int(round(w*100))}%</text>')
    s.append(f'<text class="small" x="{sx[1]}" y="{yc+82}" text-anchor="middle">正在写这个词</text>')
    s.append('</svg>')
    return "\n".join(s)


# ---------- attention add-on: one decoding step ----------
def addon_step():
    ys = [90, 150, 210, 270]
    s = ['<svg class="fig" viewBox="0 0 860 310" role="img" aria-label="解码器写第 2 个词的一步：拿当前状态 s₁ 和原文 4 个词的记忆 h₁ 到 h₄ 逐个比对，得到合计 100% 的匹配度（cat 80%），按比例混合成上下文向量 c₂，再写出 Katze。">']
    s.append('<defs><marker id="ar11" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker></defs>')
    for x, a, b in [(110, "① 解码器现在", "s₁"), (340, "② 原文的记忆", "h₁ … h₄"), (510, "③ 匹配度", "合计 100%"), (690, "④ 混合", "上下文向量 c₂"), (808, "⑤ 写出", "")]:
        s.append(f'<text class="colh" x="{x}" y="24" text-anchor="middle">{a}</text>')
        if b:
            s.append(f'<text class="colsub" x="{x}" y="44" text-anchor="middle">{b}</text>')
    s.append('<rect class="card q" x="30" y="128" width="160" height="104" rx="14"/>')
    s.append('<text class="wtxt big" x="110" y="172" text-anchor="middle" style="font-family:var(--mono)">s₁</text>')
    s.append('<text class="small" x="110" y="198" text-anchor="middle">刚写完 Die</text>')
    s.append('<text class="small" x="110" y="218" text-anchor="middle">下一个写什么？</text>')
    top = max(W_KATZE)
    for i, (y, w) in enumerate(zip(ys, W_KATZE)):
        k = 0.3 + 0.7 * w / top
        s.append(f'<path class="link" d="M190 180 C240 180 240 {y} 290 {y}" fill="none" stroke-width="{1+w*6:.1f}" stroke-opacity="{k:.2f}"/>')
        s.append(f'<rect class="card k" x="290" y="{y-22}" width="100" height="44" rx="10"/>')
        s.append(f'<text class="wtxt en" x="340" y="{y+5}" text-anchor="middle">h{SUB[i]} {EN4[i]}</text>')
        s.append(f'<rect class="barbg" x="440" y="{y-9}" width="120" height="18" rx="5"/>')
        s.append(f'<rect class="bar" x="440" y="{y-9}" width="{120*w:.1f}" height="18" rx="5"/>')
        s.append(f'<text class="num" x="568" y="{y+5}">{int(round(w*100))}%</text>')
        s.append(f'<line class="link" x1="608" y1="{y}" x2="656" y2="180" stroke-width="{1+w*6:.1f}" stroke-opacity="{k:.2f}"/>')
    s.append('<circle class="mix" cx="690" cy="180" r="34"/>')
    s.append('<text class="wtxt en" x="690" y="187" text-anchor="middle" style="fill:var(--on-accent);font-size:20px">c₂</text>')
    s.append('<line class="chain" x1="726" y1="180" x2="766" y2="180" marker-end="url(#ar11)"/>')
    s.append('<rect class="wbox hl" x="770" y="160" width="76" height="40" rx="9"/>')
    s.append('<text class="wtxt en on" x="808" y="186" text-anchor="middle">Katze</text>')
    s.append('</svg>')
    return "\n".join(s)


# ---------- LSTM / GRU gates ----------
def gates():
    panels = [("简单 RNN", "1980 年代末", [], 1),
              ("LSTM", "1997", [("g1", "忘记门", "旧笔记擦掉多少"), ("g2", "输入门", "新内容记多少"), ("g3", "输出门", "这一步拿出多少用")], 4),
              ("GRU", "2014", [("g1", "更新门", "旧的留多少、新的换多少"), ("g2", "重置门", "想新内容时参考多少旧的")], 4)]
    s = ['<svg class="fig" viewBox="0 0 860 340" role="img" aria-label="三本记忆笔记本对比：简单 RNN 没有门，每读一个词整页重写，记性差；LSTM 有忘记门、输入门、输出门三道门，记性好；GRU 把门合并成更新门和重置门两道，记性也好。">']
    for i, (name, yr, gs, mem) in enumerate(panels):
        cx = 145 + i * 285
        s.append(f'<rect class="card" x="{cx-135}" y="8" width="270" height="324" rx="14"/>')
        s.append(f'<text class="{"wtxt strong" if gs else "wtxt"}" x="{cx}" y="42" text-anchor="middle">{name}</text>')
        s.append(f'<text class="yr" x="{cx}" y="62" text-anchor="middle">{yr}</text>')
        # the notebook = memory
        s.append(f'<rect class="mem" x="{cx-56}" y="78" width="112" height="70" rx="8"/>')
        for k in range(3):
            s.append(f'<line class="grid" x1="{cx-40}" y1="{98+k*16}" x2="{cx+40}" y2="{98+k*16}"/>')
        s.append(f'<text class="small" x="{cx}" y="166" text-anchor="middle">记忆笔记本</text>')
        if not gs:
            s.append(f'<rect class="gate none" x="{cx-120}" y="184" width="240" height="34" rx="17"/>')
            s.append(f'<text class="gtxt" x="{cx}" y="206" text-anchor="middle">没有门</text>')
            s.append(f'<text class="small" x="{cx}" y="244" text-anchor="middle">每读一个词，整页重写</text>')
            s.append(f'<text class="small" x="{cx}" y="266" text-anchor="middle">旧内容很快被冲掉</text>')
        for k, (c, g, d) in enumerate(gs):
            y = 184 + k * 42
            s.append(f'<rect class="gate {c}" x="{cx-125}" y="{y}" width="250" height="34" rx="17"/>')
            s.append(f'<text class="gtxt" x="{cx-112}" y="{y+22}"><tspan class="gname">{g}</tspan> · {d}</text>')
        s.append(f'<text class="small" x="{cx-50}" y="314" text-anchor="end">记性</text>')
        for k in range(5):
            s.append(f'<circle class="{"memdot" if k < mem else "dotoff"}" cx="{cx-34+k*20}" cy="309" r="7"/>')
    s.append('</svg>')
    return "\n".join(s)


# ---------- RNN flaw 1: no parallelism ----------
def queue():
    s = ['<svg class="fig" viewBox="0 0 800 320" role="img" aria-label="记忆 h₁ 到 h₉ 排成一条链，后一个必须等前一个算完。下方是显卡的计算单元，每一步只有一格在干活，其余都闲着。">']
    s.append('<defs><marker id="ar8" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker></defs>')
    sub = "₁₂₃₄₅₆₇₈₉"
    for i, x in enumerate(X9):
        s.append(f'<circle class="mem" cx="{x}" cy="46" r="22"/>')
        s.append(f'<text class="wtxt en" x="{x}" y="52" text-anchor="middle">h{sub[i]}</text>')
        s.append(f'<text class="small" x="{x}" y="92" text-anchor="middle">{W9[i]}</text>')
        if i < 8:
            s.append(f'<line class="chain" x1="{x+24}" y1="46" x2="{X9[i+1]-26}" y2="46" marker-end="url(#ar8)"/>')
    rows = 8
    for r in range(rows):
        for i, x in enumerate(X9):
            on = r == 0
            s.append(f'<rect class="{"tick on" if on else "tick"}" x="{x-30}" y="{112+r*20}" width="60" height="14" rx="4"/>')
    s.append(f'<text class="step" x="{X9[0]}" y="290" text-anchor="middle">第 1 步</text>')
    s.append(f'<text class="step" x="{X9[8]}" y="290" text-anchor="middle">第 9 步</text>')
    s.append(f'<text class="small" x="{X9[1]-30}" y="290">↑ 显卡的计算单元（真实有几千个）：每一步只有一格在干活</text>')
    s.append('</svg>')
    return "\n".join(s)


# ---------- RNN flaw 2: long distance, English example ----------
def far():
    words = ["The", "cat", "which", "I", "found", "in", "the", "garden", "last", "summer", "after", "the", "storm", "was", "hungry"]
    src, dst = 1, 13
    xs, x = [], 10
    for w in words:
        bw = len(w) * 9 + 16
        xs.append((x, bw))
        x += bw + 6
    W = x + 4
    s = [f'<svg class="fig" viewBox="0 0 {W} 190" role="img" aria-label="英文句子 The cat which I found in the garden last summer after the storm was hungry：cat 的信息要一格一格传 12 次才到 was，越传越淡。">']
    s.append('<defs><marker id="ar9" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker></defs>')
    y = 96
    for i, ((bx, bw), w) in enumerate(zip(xs, words)):
        cls = "wbox hl" if i == src else ("wbox hl2" if i == dst else "wbox")
        s.append(f'<rect class="{cls}" x="{bx}" y="{y}" width="{bw}" height="38" rx="8"/>')
        s.append(f'<text class="{"wtxt en on" if i == src else "wtxt en"}" x="{bx+bw/2:.0f}" y="{y+25}" text-anchor="middle">{w}</text>')
        if src <= i <= dst:
            k = i - src
            s.append(f'<circle class="memdot" cx="{bx+bw/2:.0f}" cy="{y-14}" r="7" fill-opacity="{max(0.08, 1 - k*0.08):.2f}"/>')
        if src <= i < dst:
            nx, nw = xs[i + 1]
            s.append(f'<path class="chain" d="M{bx+bw/2+8:.0f} {y-18} Q{(bx+bw/2+nx+nw/2)/2:.0f} {y-34} {nx+nw/2-9:.0f} {y-18}" fill="none" marker-end="url(#ar9)"/>')
    cx0 = xs[src][0] + xs[src][1] / 2
    cx1 = xs[dst][0] + xs[dst][1] / 2
    s.append(f'<text class="cap-in" x="{(cx0+cx1)/2:.0f}" y="36" text-anchor="middle">cat 的信息要传 12 次才到 was，每次都被冲淡一点</text>')
    s.append(f'<text class="small" x="{cx1:.0f}" y="164" text-anchor="middle">用 was 还是 were？</text>')
    s.append(f'<text class="small" x="{cx1:.0f}" y="182" text-anchor="middle">得记得前面是 cat</text>')
    s.append('</svg>')
    return "\n".join(s)


# ---------- RNN flaw 2, backward: the learning signal fades ----------
def grad():
    words = ["cat", "which", "…", "the", "storm", "were"]
    xs = [90 + i * 136 for i in range(6)]
    s = ['<svg class="fig" viewBox="0 0 860 362" role="img" aria-label="模型把 was 错猜成 were，老师纠正后，纠错信号从 were 一步步倒着传回 cat，每传一步乘 0.9。下方条形图：隔 1 步还剩 0.90，隔 10 步剩 0.35，隔 50 步只剩 0.005。">']
    s.append('<defs><marker id="ar13" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" class="mk2"/></marker></defs>')
    s.append('<text class="colh" x="20" y="30">猜错了：纠错信号沿原路倒着传回 cat</text>')
    y = 82
    for i, (x, w) in enumerate(zip(xs, words)):
        cls = "wbox hl" if i == 0 else ("wbox hl2" if i == 5 else "wbox")
        s.append(f'<rect class="{cls}" x="{x-44}" y="{y}" width="88" height="38" rx="8"/>')
        s.append(f'<text class="{"wtxt en on" if i == 0 else "wtxt en"}" x="{x}" y="{y+25}" text-anchor="middle">{w}</text>')
        if i < 5:
            s.append(f'<line class="back" x1="{xs[i+1]-48}" y1="{y+19}" x2="{x+50}" y2="{y+19}" marker-end="url(#ar13)"/>')
            s.append(f'<text class="num" x="{(x+xs[i+1])/2:.0f}" y="{y-8}" text-anchor="middle">×0.9</text>')
    s.append(f'<text class="small" x="{xs[5]}" y="{y+62}" text-anchor="middle">✘ 老师：应该是 was</text>')
    s.append(f'<text class="small" x="{xs[0]}" y="{y+62}" text-anchor="middle">“当时该把 cat 记牢”</text>')
    s.append('<text class="colh" x="20" y="200">每往回传一步，信号大约 ×0.9。还剩多少？</text>')
    x0, bw = 250, 400
    for i, (lab, v, txt) in enumerate([("隔 1 步（Transformer）", 0.9, "0.90"), ("隔 10 步", 0.9 ** 10, "0.35"), ("隔 50 步", 0.9 ** 50, "0.005 几乎没了")]):
        yy = 222 + i * 42
        s.append(f'<text class="blab{" strong" if i == 0 else ""}" x="{x0-12}" y="{yy+20}" text-anchor="end">{lab}</text>')
        s.append(f'<rect class="bar dim" x="{x0}" y="{yy}" width="{bw}" height="28" rx="6"/>')
        s.append(f'<rect class="bar" x="{x0}" y="{yy}" width="{max(2, bw*v):.1f}" height="28" rx="6"/>')
        s.append(f'<text class="{"num strong" if i == 0 else "num"}" x="{x0+bw+12}" y="{yy+20}">{txt}</text>')
    s.append(f'<text class="axis" x="{x0+bw}" y="{222+3*42+4}" text-anchor="end">整条 = 刚出发时的信号（1）</text>')
    s.append('</svg>')
    return "\n".join(s)


# ---------- path length: RNN vs CNN vs attention ----------
def paths():
    n = 8
    xs = [110 + i * 90 for i in range(n)]
    s = ['<svg class="fig" viewBox="0 0 860 490" role="img" aria-label="同一句 8 个词，第 1 个词的信息怎么到第 8 个词。RNN：一格一格传，7 步。CNN：每层只看相邻 3 个，一层层往上叠，4 层才连上。注意力：一条线直连，1 步。">']
    s.append('<defs><marker id="ar12" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker></defs>')

    def words(y):
        r = []
        for i, x in enumerate(xs):
            hl = i in (0, n - 1)
            r.append(f'<rect class="{"wbox hl" if hl else "wbox"}" x="{x-32}" y="{y}" width="64" height="32" rx="8"/>')
            r.append(f'<text class="{"small on" if hl else "small"}" x="{x}" y="{y+21}" text-anchor="middle" style="font-weight:700">词 {i+1}</text>')
        return "\n".join(r)

    # RNN
    s.append('<text class="colh" x="20" y="24">RNN：一格一格往后传</text>')
    y = 64
    for i in range(n - 1):
        s.append(f'<path class="arc-a" d="M{xs[i]+10} {y-2} Q{(xs[i]+xs[i+1])/2:.0f} {y-26} {xs[i+1]-12} {y-2}" stroke-width="2.5" fill="none" marker-end="url(#ar12)"/>')
    s.append(words(y))
    s.append(f'<text class="num strong" x="840" y="{y+21}" text-anchor="end">7 步</text>')

    # CNN: kernel 3, stacked layers; highlight the two paths that meet at the top
    s.append('<text class="colh" x="20" y="134">CNN（卷积）：每层只看相邻 3 个，一层层往上叠</text>')
    wy = 286
    ly = [wy - 30, wy - 62, wy - 94, wy - 126]   # layer 1..4 dot rows
    for L in range(4):
        below = wy if L == 0 else ly[L - 1]
        for i, x in enumerate(xs):
            for d in (-1, 0, 1):
                j = i + d
                if 0 <= j < n:
                    s.append(f'<line class="grid" x1="{x}" y1="{ly[L]}" x2="{xs[j]}" y2="{below}"/>')
    up_left = [0, 1, 2, 3, 4]
    up_right = [7, 6, 5, 4, 4]
    for path in (up_left, up_right):
        pts = [(xs[path[0]], wy)] + [(xs[path[L + 1]], ly[L]) for L in range(4)]
        s.append('<polyline class="arc-a" points="' + " ".join(f"{a},{b}" for a, b in pts) + '" stroke-width="3" fill="none" stroke-linejoin="round"/>')
    for L in range(4):
        for i, x in enumerate(xs):
            on = (i == up_left[L + 1]) or (i == up_right[L + 1])
            s.append(f'<circle class="{"memdot" if on else "dotoff"}" cx="{x}" cy="{ly[L]}" r="{6 if on else 4}"/>')
        s.append(f'<text class="step" x="40" y="{ly[L]+5}">第 {L+1} 层</text>')
    s.append(words(wy))
    s.append(f'<text class="num strong" x="840" y="{ly[1]+5}" text-anchor="end">4 层</text>')

    # attention
    s.append('<text class="colh" x="20" y="364">只用注意力：任意两个词直接连线</text>')
    y = 440
    s.append(f'<path class="arc-a" d="M{xs[0]} {y-2} Q{(xs[0]+xs[-1])/2:.0f} {y-110} {xs[-1]} {y-2}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    s.append(words(y))
    s.append(f'<text class="num strong" x="840" y="{y-30}" text-anchor="end">1 步</text>')
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


# ---------- why divide by sqrt(d_k) ----------
def scale():
    raw = [24, 16, 8, 0]   # dot products for d_k = 64: spread ~ sqrt(64) = 8
    cases = [("不除", 1, "赢家通吃", False), ("除以 √64 = 8", 8, "有重点，也能学", True), ("除以 64", 64, "太平均，没重点", False)]

    def pct(p):
        if p >= 0.995: return "≈100%"
        if p >= 0.01: return f"{round(p*100)}%"
        if p >= 0.0001: return f"{p*100:.2f}%"
        return "≈0%"

    s = ['<svg class="fig" viewBox="0 0 860 300" role="img" aria-label="同一组注意力分数 24、16、8、0 的三种处理。不除：第一个词拿走约 100%，学习信号约 0.0003。除以 8：64%、24%、9%、3%，学习信号约 0.23。除以 64：30%、26%、23%、21%，几乎平均。">']
    for c, (title, div, verdict, hot) in enumerate(cases):
        x = 10 + c * 285
        sc = [r / div for r in raw]
        e = [math.exp(v - max(sc)) for v in sc]
        w = [v / sum(e) for v in e]
        s.append(f'<rect class="{"card hot" if hot else "card"}" x="{x}" y="8" width="270" height="284" rx="14"/>')
        s.append(f'<text class="colh" x="{x+135}" y="38" text-anchor="middle">{title}</text>')
        nums = ", ".join(f"{v:g}" if v == int(v) else f"{v:.2f}" for v in sc)
        s.append(f'<text class="colsub" x="{x+135}" y="62" text-anchor="middle">分数 {nums}</text>')
        for i, wi in enumerate(w):
            y = 82 + i * 36
            s.append(f'<text class="small" x="{x+20}" y="{y+17}">词 {"ABCD"[i]}</text>')
            s.append(f'<rect class="bar dim" x="{x+62}" y="{y}" width="130" height="22" rx="5"/>')
            s.append(f'<rect class="bar" x="{x+62}" y="{y}" width="{max(2, 130*wi):.1f}" height="22" rx="5"/>')
            s.append(f'<text class="num" x="{x+202}" y="{y+17}">{pct(wi)}</text>')
        s.append(f'<text class="{"wtxt strong" if hot else "wtxt"}" x="{x+135}" y="248" text-anchor="middle">{verdict}</text>')
        g = w[0] * (1 - w[0])
        s.append(f'<text class="small" x="{x+135}" y="274" text-anchor="middle">学习信号 ≈ {g:.4f}</text>' if g < 0.01 else f'<text class="small" x="{x+135}" y="274" text-anchor="middle">学习信号 ≈ {g:.2f}</text>')
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


# ---------- multi-head: why one head is not enough ----------
def headmix():
    s = ['<svg class="fig" viewBox="0 0 860 270" role="img" aria-label="左：只有 1 个头时，“它”的权重合计 100%：小狗 62%、累 10%、其他 28%，混成一个向量，“累”的信息被冲淡。右：多个头时，1 号头 80% 看小狗，2 号头 70% 看累，各自算完再拼起来，两条信息都清楚。">']
    s.append('<defs><marker id="ar14" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker></defs>')

    def stack(x, y, w, segs):
        r, cx = [], x
        for cls, frac, lab in segs:
            sw = w * frac
            r.append(f'<rect class="{cls}" x="{cx:.1f}" y="{y}" width="{sw:.1f}" height="30"/>')
            if lab:
                r.append(f'<text class="segt" x="{cx+sw/2:.1f}" y="{y+20}" text-anchor="middle">{lab}</text>')
            cx += sw
        return r

    # left: one head
    s.append('<text class="colh" x="20" y="30">1 个头：合计 100%，混成一个向量</text>')
    s.append('<text class="small" x="20" y="62">“它”</text>')
    s += stack(60, 42, 340, [("seg1", 0.62, "小狗 62%"), ("seg2", 0.10, ""), ("seg0", 0.28, "")])
    s.append(f'<text class="small" x="{60+340*0.67:.0f}" y="92" text-anchor="middle">累 10%</text>')
    s.append(f'<text class="small" x="{60+340*0.86:.0f}" y="92" text-anchor="middle">其他 28%</text>')
    s.append('<line class="chain" x1="230" y1="102" x2="230" y2="136" marker-end="url(#ar14)"/>')
    s.append('<rect class="wbox" x="110" y="142" width="240" height="44" rx="10"/>')
    s.append('<text class="wtxt" x="230" y="170" text-anchor="middle" style="font-size:16px">1 个向量，小狗为主</text>')
    s.append('<text class="small" x="230" y="218" text-anchor="middle">“它怎么了（累）”只占一成，被冲淡</text>')
    # right: several heads
    s.append('<text class="colh" x="450" y="30">多个头：每个头各自合计 100%</text>')
    for k, (cls, frac, lab) in enumerate([("seg1", 0.80, "小狗 80%"), ("seg2", 0.70, "累 70%")]):
        y = 42 + k * 44
        s.append(f'<text class="small" x="450" y="{y+20}">{k+1} 号头</text>')
        s += stack(510, y, 300, [(cls, frac, lab), ("seg0", 1 - frac, "")])
    s.append('<text class="small" x="510" y="146">……一共 8 个头，同时算</text>')
    s.append('<line class="chain" x1="660" y1="154" x2="660" y2="168" marker-end="url(#ar14)"/>')
    for k, (cls, lab) in enumerate([("wbox hl-head1", "小狗"), ("wbox hl-head2", "累"), ("wbox", "……")]):
        s.append(f'<rect class="{cls}" x="{560+k*70}" y="174" width="64" height="36" rx="8"/>')
        s.append(f'<text class="wtxt" x="{592+k*70}" y="198" text-anchor="middle" style="font-size:15px">{lab}</text>')
    s.append('<text class="small" x="660" y="236" text-anchor="middle">拼起来：两条信息都清清楚楚</text>')
    s.append('</svg>')
    return "\n".join(s)


# ---------- multi-head: 512 = 8 x 64 ----------
def headsplit():
    rows = [("wbox hl-head1", "头 1：自己的一套 Q、K、V，64 维"), ("wbox hl-head2", "头 2：另一套 Q、K、V，64 维"), ("wbox hl-head3", "头 3")] + [("wbox", "")] * 4 + [("wbox", "头 8")]
    segs = ["seg1", "seg2", "seg3"] + ["seg0"] * 5
    y0, rh, gap = 50, 20, 4
    top, bot = y0, y0 + 8 * (rh + gap) - gap
    mid = (top + bot) / 2
    s = [f'<svg class="fig" viewBox="0 0 860 {bot+40}" role="img" aria-label="“它”的 512 维向量交给 8 个头，每个头用自己的一套 Q、K、V 变换压成 64 维，各做一遍注意力；8 份 64 维拼回 512 维，再乘 W_O 混合，输出 512 维。">']
    s.append('<defs><marker id="ar15" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker></defs>')
    s.append('<text class="colh" x="58" y="34" text-anchor="middle">“它”的向量</text>')
    s.append(f'<rect class="wbox hl" x="30" y="{top}" width="56" height="{bot-top}" rx="8"/>')
    s.append(f'<text class="wtxt en on" x="58" y="{mid+6:.0f}" text-anchor="middle" style="font-size:15px">512</text>')
    s.append('<text class="colh" x="290" y="34" text-anchor="middle">8 个头，各算各的注意力</text>')
    for i, ((cls, lab), sg) in enumerate(zip(rows, segs)):
        y = y0 + i * (rh + gap)
        s.append(f'<path class="chain" d="M86 {mid:.0f} C120 {mid:.0f} 116 {y+rh/2} 150 {y+rh/2}" fill="none"/>')
        s.append(f'<rect class="{cls}" x="150" y="{y}" width="280" height="{rh}" rx="5"/>')
        if lab:
            s.append(f'<text class="small" x="162" y="{y+15}" style="font-size:13px">{lab}</text>')
        s.append(f'<line class="chain" x1="430" y1="{y+rh/2}" x2="560" y2="{y+rh/2}"/>')
        s.append(f'<rect class="{sg}" x="560" y="{y}" width="56" height="{rh+gap if i < 7 else rh}"/>')
    s.append('<text class="colh" x="588" y="34" text-anchor="middle">拼回 512</text>')
    s.append(f'<line class="chain" x1="620" y1="{mid:.0f}" x2="664" y2="{mid:.0f}" marker-end="url(#ar15)"/>')
    s.append(f'<rect class="card q" x="670" y="{mid-24:.0f}" width="84" height="48" rx="10"/>')
    s.append(f'<text class="wtxt en" x="712" y="{mid+7:.0f}" text-anchor="middle" style="font-family:var(--mono);font-size:17px">× W_O</text>')
    s.append(f'<line class="chain" x1="756" y1="{mid:.0f}" x2="784" y2="{mid:.0f}" marker-end="url(#ar15)"/>')
    s.append('<text class="colh" x="818" y="34" text-anchor="middle">输出</text>')
    s.append(f'<rect class="wbox hl" x="790" y="{top}" width="56" height="{bot-top}" rx="8"/>')
    s.append(f'<text class="wtxt en on" x="818" y="{mid+6:.0f}" text-anchor="middle" style="font-size:15px">512</text>')
    s.append(f'<text class="small" x="290" y="{bot+26}" text-anchor="middle">8 × 64 = 512，总计算量和 1 个 512 维的头差不多</text>')
    s.append('</svg>')
    return "\n".join(s)


# ---------- position ----------
def position():
    s = ['<svg class="fig" viewBox="0 0 800 380" role="img" aria-label="“狗咬人”和“人咬狗”倒进同一个袋子，看起来一模一样；给每个字贴上座位号后就能分清。座位号是在几条快慢不同的波上，各取一个读数。">']
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
    # waves, stacked
    s.append('<text class="colh" x="40" y="222">座位号怎么来？在几条快慢不同的波上各读一个数</text>')
    seats = [(160, "1"), (400, "2"), (640, "3")]
    for x, lab in seats:
        s.append(f'<line class="seatline" x1="{x}" y1="240" x2="{x}" y2="352"/>')
        s.append(f'<circle class="seat2" cx="{x}" cy="364" r="12"/>')
        s.append(f'<text class="seatn2" x="{x}" y="369" text-anchor="middle">{lab}</text>')
    waves = [(0.05, "wave1"), (0.022, "wave2"), (0.009, "wave3")]
    for k, (freq, cls) in enumerate(waves):
        yc = 260 + k * 36
        s.append(f'<line class="grid" x1="40" y1="{yc}" x2="760" y2="{yc}"/>')
        pts = [f"{px},{yc - 13*math.sin(freq*(px-40) + k):.1f}" for px in range(40, 761, 4)]
        s.append(f'<polyline class="{cls}" points="{" ".join(pts)}" fill="none"/>')
        for x, _ in seats:
            s.append(f'<circle class="dot-{cls}" cx="{x}" cy="{yc - 13*math.sin(freq*(x-40) + k):.1f}" r="5"/>')
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
    # 2x2: training vs generation, RNN vs Transformer, on the German answer sentence
    s = ['<svg class="fig" viewBox="0 0 860 424" role="img" aria-label="2 乘 2 对比。训练时答案已知：RNN 仍要 4 步，因为 hₜ 必须等 hₜ₋₁；Transformer 把整句答案一起喂进去，加上遮挡，1 步算完。生成时答案未知：RNN 和 Transformer 都要一个词一个词地出，各 4 步。">']
    cols = [(170, "训练：答案已经知道"), (515, "生成：答案还不知道")]
    rows = [(64, "RNN"), (244, "Transformer")]
    for cx, lab in cols:
        s.append(f'<text class="colh" x="{cx+167}" y="40" text-anchor="middle">{lab}</text>')
    cells = {
        (0, 0): (False, "⏱ 4 步", "答案已知，hₜ 还得等 hₜ₋₁"),
        (1, 0): (True, "⏱ 1 步", "整句答案一起喂，加遮挡"),
        (0, 1): (False, "⏱ 4 步", "下一个词要等上一个写出"),
        (1, 1): (False, "⏱ 4 步", "这点和 RNN 一样"),
    }
    for r, (y, name) in enumerate(rows):
        s.append(f'<text class="{"wtxt strong" if r else "wtxt"}" x="90" y="{y+90}" text-anchor="middle" style="font-family:var(--mono);font-size:16px">{name}</text>')
        for c, (x, _) in enumerate(cols):
            par, steps, why = cells[(r, c)]
            s.append(f'<rect class="{"card hot" if par else "card"}" x="{x}" y="{y}" width="335" height="170" rx="14"/>')
            gx = x + 100
            for k in range(4):
                s.append(f'<text class="step" x="{gx+k*52+21}" y="{y+24}" text-anchor="middle" style="font-size:12px">第 {k+1} 步</text>')
            for i, w in enumerate(DE4):
                yy = y + 34 + i * 24
                s.append(f'<text class="wtxt en" x="{gx-12}" y="{yy+14}" text-anchor="end" style="font-size:13px">{w}</text>')
                for k in range(4):
                    on = (k == 0) if par else (k == i)
                    s.append(f'<rect class="{"tick on" if on else "tick"}" x="{gx+k*52}" y="{yy}" width="42" height="18" rx="4"/>')
            s.append(f'<text class="{"num strong" if par else "num"}" x="{x+20}" y="{y+154}">{steps}</text>')
            s.append(f'<text class="small" x="{x+100}" y="{y+154}">{why}</text>')
    s.append('</svg>')
    return "\n".join(s)


def mask():
    toks = ["〈开始〉", "Die", "Katze", "ist"]
    nxt = DE4
    x0, y0, cw, ch = 170, 72, 70, 50
    s = ['<svg class="fig" viewBox="0 0 760 310" role="img" aria-label="遮挡示意：4 乘 4 的格子，每一行只能看到自己和前面的词，右上方的格子被遮住。〈开始〉只看自己，猜 Die；看到 Die 猜 Katze；看到 Die Katze 猜 ist；看到 Die Katze ist 猜 müde。">']
    s.append(f'<text class="hm-axis" x="{x0-14}" y="30" text-anchor="end">谁在算 ↓</text>')
    s.append(f'<text class="hm-axis" x="{x0}" y="30">能看到的词 →</text>')
    for j, t in enumerate(toks):
        s.append(f'<text class="wtxt en" x="{x0+j*cw+30}" y="58" text-anchor="middle" style="font-size:13px">{t}</text>')
    for i, t in enumerate(toks):
        y = y0 + i * ch
        s.append(f'<text class="wtxt en" x="{x0-14}" y="{y+26}" text-anchor="end" style="font-size:13px">{t}</text>')
        for j in range(4):
            if j <= i:
                s.append(f'<rect class="hm" x="{x0+j*cw}" y="{y}" width="60" height="40" rx="7"/>')
            else:
                s.append(f'<rect class="slot" x="{x0+j*cw}" y="{y}" width="60" height="40" rx="7"/>')
                s.append(f'<text class="small" x="{x0+j*cw+30}" y="{y+26}" text-anchor="middle">遮住</text>')
        s.append(f'<text class="small" x="{x0+4*cw+16}" y="{y+26}">→ 猜下一个词：</text>')
        s.append(f'<rect class="wbox hl" x="{x0+4*cw+120}" y="{y+5}" width="70" height="30" rx="7"/>')
        s.append(f'<text class="wtxt en on" x="{x0+4*cw+155}" y="{y+25}" text-anchor="middle" style="font-size:13px">{nxt[i]}</text>')
    s.append(f'<text class="small" x="{x0}" y="{y0+4*ch+22}">4 行同时算，但每行都看不到自己后面的答案</text>')
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


def split():
    # BERT keeps the encoder (fill in a blank, sees both sides); GPT keeps the decoder (guess the next word, sees only the left)
    s = ['<svg class="fig" viewBox="0 0 860 444" role="img" aria-label="Transformer 拆成两半。BERT 只留编码器，练习填空：遮掉“马路”，用前后的词一起猜。GPT 只留解码器，练习猜下一个词：只看前面的“小狗没有过马路因为它太”，猜出“累”。">']
    s.append('<defs><marker id="ar15" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker></defs>')
    s.append('<text class="colh" x="430" y="26" text-anchor="middle">Transformer（本论文）</text>')
    s.append('<rect class="tower" x="250" y="40" width="360" height="64" rx="14"/>')
    s.append('<rect class="sub sa" x="264" y="52" width="158" height="40" rx="9"/>')
    s.append('<text class="subt" x="343" y="78" text-anchor="middle">编码器</text>')
    s.append('<rect class="sub sa" x="438" y="52" width="158" height="40" rx="9"/>')
    s.append('<text class="subt" x="517" y="78" text-anchor="middle">解码器</text>')
    s.append('<line class="chain" x1="343" y1="104" x2="230" y2="146" marker-end="url(#ar15)"/>')
    s.append('<line class="chain" x1="517" y1="104" x2="630" y2="146" marker-end="url(#ar15)"/>')
    cards = [
        (20, "BERT：只留编码器", "练习：遮掉一个词，用前后文猜", 3, range(9), "前后都能看，擅长读懂一句话"),
        (440, "GPT：只留解码器", "练习：猜下一个词", 7, range(7), "只看前面（遮挡），猜完接着猜，能一直写下去"),
    ]
    cy = 150
    for cx, title, sub, hole, seen, note in cards:
        s.append(f'<rect class="card" x="{cx}" y="{cy}" width="400" height="280" rx="14"/>')
        s.append(f'<text class="colh" x="{cx+20}" y="{cy+32}">{title}</text>')
        s.append(f'<text class="small" x="{cx+20}" y="{cy+56}">{sub}</text>')
        xs = [cx + 32 + i * 42 for i in range(9)]
        wy = cy + 136
        s.append(arcs(hole, {j: 0.1 for j in seen if j != hole}, wy - 4, "arc-a", xs=xs, scale=20, hmul=0.08))
        for i in seen:
            if i == hole:
                continue
            s.append(f'<rect class="wbox" x="{xs[i]-19}" y="{wy}" width="38" height="36" rx="8"/>')
            s.append(f'<text class="wtxt" x="{xs[i]}" y="{wy+23}" text-anchor="middle" style="font-size:14px">{W9[i]}</text>')
        hx = xs[hole]
        s.append(f'<rect class="slot" x="{hx-19}" y="{wy}" width="38" height="36" rx="8"/>')
        s.append(f'<text class="wtxt" x="{hx}" y="{wy+24}" text-anchor="middle" style="font-size:16px">?</text>')
        s.append(f'<line class="chain" x1="{hx}" y1="{wy+40}" x2="{hx}" y2="{wy+68}" marker-end="url(#ar15)"/>')
        s.append(f'<rect class="wbox hl" x="{hx-26}" y="{wy+74}" width="52" height="34" rx="8"/>')
        s.append(f'<text class="wtxt on" x="{hx}" y="{wy+97}" text-anchor="middle" style="font-size:15px">{W9[hole]}</text>')
        s.append(f'<text class="small" x="{hx-34}" y="{wy+96}" text-anchor="end">猜出</text>')
        s.append(f'<text class="small" x="{cx+20}" y="{cy+262}">{note}</text>')
    s.append('</svg>')
    return "\n".join(s)


def legacy():
    items = [(2017, "Transformer", "本论文", "翻译"), (2018, "GPT", "只用解码器", "猜下一个词"),
             (2018, "BERT", "只用编码器", "做填空"), (2020, "GPT-3", "结构没大改", "只是大得多"),
             (2022, "ChatGPT", "在 GPT 上", "再教它对话"), (2023, "Claude", "也是 Transformer", "你正在用的")]
    s = ['<svg class="fig" viewBox="0 0 860 256" role="img" aria-label="时间线：2017 Transformer（本论文，翻译）；2018 GPT（只用解码器，猜下一个词）；2018 BERT（只用编码器，做填空）；2020 GPT-3（结构没大改，只是大得多）；2022 ChatGPT（在 GPT 上再教它对话）；2023 Claude（也是 Transformer）。">']
    s.append('<line class="spine" x1="60" y1="120" x2="820" y2="120"/>')
    for i, (yr, name, sub, sub2) in enumerate(items):
        x = 80 + i * 145
        up = i % 2 == 0
        first = i == 0
        r = 16 if first else 10
        s.append(f'<circle class="{"node first" if first else "node"}" cx="{x}" cy="120" r="{r}"/>')
        ty = 46 if up else 172
        s.append(f'<line class="grid" x1="{x}" y1="{120-r if up else 120+r}" x2="{x}" y2="{ty+48 if up else ty-22}"/>')
        s.append(f'<text class="yr" x="{x}" y="{ty-20 if up else ty+4}" text-anchor="middle">{yr}</text>')
        s.append(f'<text class="{"wtxt strong" if first else "wtxt"}" x="{x}" y="{ty+2 if up else ty+28}" text-anchor="middle">{name}</text>')
        s.append(f'<text class="small" x="{x}" y="{ty+22 if up else ty+48}" text-anchor="middle">{sub}</text>')
        s.append(f'<text class="small" x="{x}" y="{ty+40 if up else ty+66}" text-anchor="middle">{sub2}</text>')
    s.append('</svg>')
    return "\n".join(s)


tpl = open(sys.argv[2], encoding="utf-8").read()
h1, h2, h3 = heads()
rep = {
    "{{HERO}}": hero(), "{{TASK}}": task(), "{{BEFORE}}": before(), "{{PARTS}}": parts(), "{{QUEUE}}": queue(), "{{FAR}}": far(), "{{GRAD}}": grad(), "{{GATES}}": gates(), "{{ADDON}}": addon(), "{{ADDON_STEP}}": addon_step(), "{{PATHS}}": paths(), "{{ATTN}}": attn(), "{{QKV}}": qkv(), "{{SCALE}}": scale(),
    "{{HEADMIX}}": headmix(), "{{HEADSPLIT}}": headsplit(), "{{HEAD1}}": h1, "{{HEAD2}}": h2, "{{HEAD3}}": h3, "{{POS}}": position(),
    "{{ARCH}}": arch(), "{{SPEED}}": speed(), "{{MASK}}": mask(), "{{BLEU}}": bleu(), "{{SPLIT}}": split(), "{{LEGACY}}": legacy(),
}
for k, v in rep.items():
    tpl = tpl.replace(k, v)
open(OUT, "w", encoding="utf-8").write(tpl)
print("ok", len(tpl))
