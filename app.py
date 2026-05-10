import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="India CNS - The Generic Market",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.block-container { padding: 2rem 3rem; max-width: 1300px; }
h1,h2,h3 { font-family: 'DM Serif Display', serif; }

.tag {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 3px;
    margin-bottom: 1rem;
    border: 1px solid rgba(128,128,128,0.4);
    opacity: 0.6;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}
.hero-sub {
    font-size: 1rem;
    font-weight: 300;
    opacity: 0.65;
    margin-bottom: 0;
}
.kpi-card {
    border-radius: 10px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(128,128,128,0.18);
    background: rgba(128,128,128,0.05);
}
.kpi-label {
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    opacity: 0.5;
    font-weight: 600;
    margin-bottom: 0.25rem;
}
.kpi-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    line-height: 1;
}
.kpi-delta { font-size: 0.78rem; opacity: 0.55; margin-top: 0.25rem; }
.kpi-delta.up { color: #2D9B6F; opacity: 1; }

.insight-strip {
    border-radius: 10px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 1rem;
    background: rgba(128,128,128,0.08);
    border-left: 3px solid #C8A84B;
}
.insight-num {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: #C8A84B;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.insight-body { font-size: 0.86rem; line-height: 1.65; opacity: 0.72; }

.lundbeck-card {
    border-radius: 10px;
    padding: 1.6rem 1.8rem;
    border: 1px solid rgba(200,168,75,0.35);
    background: rgba(200,168,75,0.06);
    margin-top: 0.5rem;
}
.lundbeck-head {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem;
    margin-bottom: 0.6rem;
    color: #C8A84B;
}
.lundbeck-body { font-size: 0.88rem; line-height: 1.7; opacity: 0.75; }

.section-title { font-family: 'DM Serif Display', serif; font-size: 1.4rem; margin-bottom: 0.15rem; }
.section-sub { font-size: 0.82rem; opacity: 0.5; margin-bottom: 1rem; }
.source-note { font-size: 0.7rem; opacity: 0.4; margin-top: 0.4rem; }
hr.div { border: none; border-top: 1px solid rgba(128,128,128,0.18); margin: 2rem 0; }

.sw-card {
    border-radius: 10px;
    padding: 1.3rem 1.5rem;
    border: 1px solid rgba(128,128,128,0.18);
    background: rgba(128,128,128,0.04);
}
.sw-num {
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #C8A84B;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.sw-head { font-family: 'DM Serif Display', serif; font-size: 1.05rem; margin-bottom: 0.5rem; }
.sw-body { font-size: 0.84rem; line-height: 1.65; opacity: 0.7; }
</style>
""", unsafe_allow_html=True)

# ── DATA (all verified from Netmeds, Nov 2024) ─────────────────────────────────
generics = pd.DataFrame({
    "Molecule":     ["Clonazepam\n0.5mg", "Escitalopram\n10mg", "Olanzapine\n5mg",
                     "Valproate\n500mg",  "Sertraline\n50mg"],
    "Category":     ["Anxiolytic", "Antidepressant", "Antipsychotic",
                     "Antiepileptic", "Antidepressant"],
    "Brand":        ["Generic", "Nexito (Sun)", "Sun generic",
                     "Generic", "Torrent"],
    "Pack_Price":   [32, 52, 52, 130, 196],
    "Pack_Tabs":    [10, 10, 10, 15,  15],
    "Monthly_Cost": [96, 156, 156, 260, 392],
})

# Cipralex — sole originator reference
cipralex_monthly = 268  # ₹134/15T → ₹8.93/tab → ×30

# Affordability — monthly cost as % of ₹25,000 median income
generics["Afford_Pct"] = (generics["Monthly_Cost"] / 25000 * 100).round(2)

# Market share
share = pd.DataFrame({
    "Player": ["Sun Pharma", "Torrent Pharma", "Alkem", "Abbott India", "Lundbeck India", "Others"],
    "Share":  [18, 14, 11, 9, 7, 41],
    "Type":   ["Generic","Generic","Generic","MNC","MNC","Mixed"],
})

CAT_COLORS = {
    "Antidepressant": "#3A7CA5",
    "Antipsychotic":  "#C8A84B",
    "Antiepileptic":  "#6B9E6E",
    "Anxiolytic":     "#9A7DB8",
}
TYPE_COLORS = {"Generic": "#3A7CA5", "MNC": "#C8A84B", "Mixed": "#aaa"}

def base_layout(**kwargs):
    cfg = dict(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", size=11),
        margin=dict(l=0, r=30, t=10, b=40),
    )
    cfg.update(kwargs)
    return cfg

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="tag"></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">India CNS Pharma —<br><i>The Generic Takeover</i></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">MNC originators have largely exited Indian CNS retail. The market belongs to domestic generics and at these prices, the real barrier isn\'t cost. It\'s access.</div>', unsafe_allow_html=True)
st.markdown('<hr class="div">', unsafe_allow_html=True)

# ── KPIs ───────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown("""<div class="kpi-card">
        <div class="kpi-label">India CNS market size</div>
        <div class="kpi-value">~$800M</div>
        <div class="kpi-delta">Growing at ~7% CAGR · IQVIA 2024</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown("""<div class="kpi-card">
        <div class="kpi-label">Generic share of CNS market</div>
        <div class="kpi-value">~84%</div>
        <div class="kpi-delta">Sun + Torrent + Alkem dominate · AIOCD est.</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown("""<div class="kpi-card">
        <div class="kpi-label">Depression treatment gap</div>
        <div class="kpi-value">85%</div>
        <div class="kpi-delta">56Mn Indians untreated · WHO 2023</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown("""<div class="kpi-card">
        <div class="kpi-label">Cheapest generic monthly cost</div>
        <div class="kpi-value">₹96</div>
        <div class="kpi-delta up">0.38% of median monthly income</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="div">', unsafe_allow_html=True)

# ── SECTION 1: GENERIC PRICING ─────────────────────────────────────────────────
st.markdown('<div class="section-title">Generic CNS Drug Prices — What Patients Actually Pay</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Monthly treatment cost (30-day supply) · verified retail prices · Netmeds 2024</div>', unsafe_allow_html=True)

col_chart, col_ins = st.columns([2.2, 1])

with col_chart:
    bar_colors = [CAT_COLORS.get(c, "#888") for c in generics["Category"]]

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=generics["Molecule"],
        y=generics["Monthly_Cost"],
        marker_color=bar_colors,
        text=["₹"+str(v) for v in generics["Monthly_Cost"]],
        textposition="outside",
        textfont=dict(size=11),
        name="Generic (monthly)",
        width=0.5,
    ))
    # Cipralex reference line
    fig1.add_hline(
        y=cipralex_monthly,
        line_dash="dash",
        line_color="#C8A84B",
        line_width=1.5,
        annotation_text="Cipralex (Lundbeck originator) ₹268/mo",
        annotation_position="top left",
        annotation_font_size=10,
        annotation_font_color="#C8A84B",
    )

    fig1.update_layout(**base_layout(
        height=340,
        showlegend=False,
        xaxis=dict(showgrid=False, tickfont_size=10),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(128,128,128,0.12)",
            title="INR per month",
            tickfont_size=10,
            range=[0, 480],
        ),
    ))
    st.plotly_chart(fig1, use_container_width=True)

    # Legend
    st.markdown("""
    <div style="display:flex; gap:1.5rem; flex-wrap:wrap; font-size:0.75rem; opacity:0.6; margin-top:-0.5rem;">
        <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#3A7CA5;margin-right:4px"></span>Antidepressant</span>
        <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#C8A84B;margin-right:4px"></span>Antipsychotic</span>
        <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#6B9E6E;margin-right:4px"></span>Antiepileptic</span>
        <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#9A7DB8;margin-right:4px"></span>Anxiolytic</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="source-note">Sources: Netmeds verified retail prices · Monthly cost = per-tablet price × 30 standard daily doses</div>', unsafe_allow_html=True)

with col_ins:
    st.markdown("""<div class="insight-strip">
        <div class="insight-num">₹96</div>
        <div class="insight-body">The cheapest CNS generic clonazepam costs ₹96/month. 
        Less than a Netflix subscription. The access barrier in Indian mental healthcare 
        is not price. It is psychiatrist density (0.3 per 100k vs WHO norm of 1), 
        stigma, and last-mile distribution.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="insight-strip">
        <div class="insight-num">1.7×</div>
        <div class="insight-body">The dashed line is Cipralex (Lundbeck's originator escitalopram) at ₹268/month. 
        The generic equivalent (Nexito) costs ₹156. A 1.7× gap, not the 10–15× seen in Western markets. 
        MNCs in India have been forced to price close to generics just to stay on the shelf.</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="div">', unsafe_allow_html=True)

# ── SECTION 2: AFFORDABILITY ───────────────────────────────────────────────────
st.markdown('<div class="section-title">Affordability — Cost as % of Monthly Income</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Monthly generic treatment cost as % of India median monthly income (₹25,000 · PLFS 2023)</div>', unsafe_allow_html=True)

col_afford, col_afford_ins = st.columns([2.2, 1])

with col_afford:
    afford_colors = [CAT_COLORS.get(c, "#888") for c in generics["Category"]]
    fig2 = go.Figure(go.Bar(
        x=generics["Afford_Pct"],
        y=generics["Molecule"],
        orientation="h",
        marker_color=afford_colors,
        text=[f"{v}%" for v in generics["Afford_Pct"]],
        textposition="outside",
        textfont=dict(size=11),
        width=0.5,
    ))
    fig2.update_layout(**base_layout(
        height=280,
        showlegend=False,
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(128,128,128,0.12)",
            title="% of ₹25,000 monthly income",
            tickfont_size=10,
            range=[0, 2.2],
        ),
        yaxis=dict(showgrid=False, tickfont_size=10),
        margin=dict(l=0, r=50, t=10, b=40),
    ))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('<div class="source-note">Median income: PLFS 2023 · Prices: Netmeds verified retail</div>', unsafe_allow_html=True)

with col_afford_ins:
    st.markdown("""<div class="insight-strip">
        <div class="insight-num">&lt;1.6%</div>
        <div class="insight-body">Every generic CNS drug on this list costs less than 1.6% of median monthly income. 
        Even the most expensive sertraline at ₹392/month is affordable for a working urban Indian. 
        Price has been solved. The problem is that most patients never reach a prescriber.</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="div">', unsafe_allow_html=True)

# ── SECTION 3: MARKET SHARE ────────────────────────────────────────────────────
st.markdown('<div class="section-title">Who Owns the Market</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Estimated India CNS market share by company · 2024</div>', unsafe_allow_html=True)

col_pie, col_pie_ins = st.columns([1, 1])

with col_pie:
    pie_colors = [TYPE_COLORS.get(t, "#aaa") for t in share["Type"]]
    fig3 = go.Figure(go.Pie(
        labels=share["Player"],
        values=share["Share"],
        hole=0.52,
        marker=dict(colors=pie_colors, line=dict(color="rgba(0,0,0,0.06)", width=1.5)),
        textfont=dict(size=11, family="DM Sans"),
        sort=False,
    ))
    fig3.update_layout(**base_layout(
        height=300,
        legend=dict(font_size=11, orientation="v"),
        annotations=[dict(
            text="CNS<br>India",
            x=0.5, y=0.5,
            font_size=12,
            font_family="DM Serif Display",
            showarrow=False,
        )],
    ))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('<div class="source-note">Blue = domestic generic · Gold = MNC · Sources: AIOCD AWACS estimates · company reports</div>', unsafe_allow_html=True)

with col_pie_ins:
    st.markdown("""<div class="insight-strip" style="margin-top:0.5rem">
        <div class="insight-num">84%</div>
        <div class="insight-body">Domestic generic players control ~84% of India's CNS market by volume. 
        Sun, Torrent, and Alkem alone account for ~43%. 
        MNCs like Lundbeck and Abbott hold single-digit shares 
        not because they lost, but because they chose not to compete on volume.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="insight-strip">
        <div class="insight-num">7%</div>
        <div class="insight-body">Lundbeck India's estimated CNS share. Tiny by volume 
        but their play is margin, not share. 
        Specialist psychiatrists in Tier 1 cities, insured urban patients, 
        brand equity built through medical education. 
        A deliberately narrow, high-margin niche.</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="div">', unsafe_allow_html=True)

# ── SECTION 4: LUNDBECK EXCEPTION ─────────────────────────────────────────────
st.markdown('<div class="section-title">The Lundbeck Exception</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Why one MNC originator is still standing in Indian CNS retail</div>', unsafe_allow_html=True)

col_l1, col_l2, col_l3 = st.columns(3)
with col_l1:
    st.markdown("""<div class="sw-card">
        <div class="sw-num">The strategy</div>
        <div class="sw-head">Don't fight generics — avoid them</div>
        <div class="sw-body">Lundbeck doesn't try to sell Cipralex at chemist counters. 
        Their sales force targets specialist psychiatrists, not general practitioners. 
        The prescriber recommends the brand by name. 
        The patient typically urban, insured, or upper-income fills it. 
        Generics and originators are selling to completely different patients.</div>
    </div>""", unsafe_allow_html=True)
with col_l2:
    st.markdown("""<div class="sw-card">
        <div class="sw-num">The pricing</div>
        <div class="sw-head">1.7× premium — not 10×</div>
        <div class="sw-body">Cipralex costs ₹268/month vs ₹156 for Nexito. 
        In the US, that same gap is 15–20×. 
        India's NPPA pricing environment and generic competition have compressed 
        Lundbeck's premium to near-parity. They maintain presence through brand trust, 
        not through pricing power.</div>
    </div>""", unsafe_allow_html=True)
with col_l3:
    st.markdown("""<div class="sw-card">
        <div class="sw-num">The question</div>
        <div class="sw-head">Is this model sustainable?</div>
        <div class="sw-body">As India's Tier 2-3 cities develop specialist infrastructure 
        and telemedicine grows, the addressable market for premium CNS brands will expand. 
        The question for Lundbeck and every MNC still in Indian CNS 
        is whether to stay niche or find a way into the mass market 
        without destroying the brand premium that justifies their presence.</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="div">', unsafe_allow_html=True)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:1rem 0 2rem; opacity:0.45;">
    <div style="font-family:'DM Serif Display',serif; font-size:0.95rem; margin-bottom:0.3rem;">
        Built by Ishaan · Analyst, Axtria · IIT BHU
    </div>
    <div style="font-size:0.7rem;">
        Data: Netmeds verified retail prices (2024) · IQVIA India · AIOCD AWACS estimates · WHO Mental Health Atlas 2023 · PLFS 2023 · company reports
    </div>
</div>
""", unsafe_allow_html=True)
