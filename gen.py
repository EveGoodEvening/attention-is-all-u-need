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
    s = ['<svg class="fig" viewBox="0 0 860 370" role="img" aria-label="Seq2Seq 是一种组装方式：一个编码器读、一个解码器写。里面插什么零件都行：插 RNN 类（简单 RNN、LSTM、GRU）是 2014 到 2016 年的主流；插卷积就是 ConvS2S；只用注意力就是 Transformer。">']
    s.append('<defs><marker id="ar7" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="mk"/></marker></defs>')
    s.append('<text class="colh" x="430" y="28" text-anchor="middle">组装方式：Seq2Seq（一个读，一个写）</text>')
    for x, lab in [(180, "编码器 · 读"), (480, "解码器 · 写")]:
        s.append(f'<rect class="tower" x="{x}" y="46" width="200" height="80" rx="14"/>')
        s.append(f'<text class="subt" x="{x+100}" y="74" text-anchor="middle">{lab}</text>')
        s.append(f'<rect class="slot" x="{x+40}" y="86" width="120" height="28" rx="7"/>')
        s.append(f'<text class="small" x="{x+100}" y="105" text-anchor="middle">插零件</text>')
    s.append('<line class="chain" x1="382" y1="86" x2="474" y2="86" marker-end="url(#ar7)"/>')
    cols = [(150, "零件：RNN 类", ["简单 RNN", "LSTM", "GRU"], "Seq2Seq", "2014–2016 主流，2015 年起加注意力", False),
            (430, "零件：卷积", ["CNN"], "ConvS2S", "2017 年 5 月", False),
            (710, "零件：只用注意力", ["注意力"], "Transformer", "2017 年 6 月 · 本论文", True)]
    for cx, head, chips, name, sub, hot in cols:
        s.append(f'<path class="chain" d="M{cx} 198 C{cx} 160 430 170 430 132" fill="none" marker-end="url(#ar7)"/>')
        s.append(f'<rect class="{"card hot" if hot else "card"}" x="{cx-128}" y="200" width="256" height="156" rx="14"/>')
        s.append(f'<text class="colh" x="{cx}" y="230" text-anchor="middle">{head}</text>')
        cw, gap = 74, 8
        x0 = cx - (len(chips) * cw + (len(chips) - 1) * gap) / 2
        for i, c in enumerate(chips):
            x = x0 + i * (cw + gap)
            cls = "wbox hl" if hot else "wbox"
            s.append(f'<rect class="{cls}" x="{x:.0f}" y="246" width="{cw}" height="36" rx="8"/>')
            s.append(f'<text class="{"small on" if hot else "small"}" x="{x+cw/2:.0f}" y="269" text-anchor="middle" style="font-weight:700">{c}</text>')
        s.append(f'<text class="{"wtxt strong" if hot else "wtxt"}" x="{cx}" y="316" text-anchor="middle">= {name}</text>')
        s.append(f'<text class="small" x="{cx}" y="340" text-anchor="middle">{sub}</text>')
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
    "{{HERO}}": hero(), "{{TASK}}": task(), "{{BEFORE}}": before(), "{{PARTS}}": parts(), "{{QUEUE}}": queue(), "{{RNN}}": rnn(), "{{FAR}}": far(), "{{GATES}}": gates(), "{{ATTN}}": attn(), "{{QKV}}": qkv(),
    "{{HEAD1}}": h1, "{{HEAD2}}": h2, "{{HEAD3}}": h3, "{{POS}}": position(),
    "{{ARCH}}": arch(), "{{SPEED}}": speed(), "{{BLEU}}": bleu(), "{{LEGACY}}": legacy(),
}
for k, v in rep.items():
    tpl = tpl.replace(k, v)
open(OUT, "w", encoding="utf-8").write(tpl)
print("ok", len(tpl))
