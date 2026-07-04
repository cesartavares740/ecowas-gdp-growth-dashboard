# ==============================================
# ECOWAS GDP GROWTH DASHBOARD
# Author: Cesar Tavares
# ==============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ECOWAS GDP Growth Dashboard",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📈 ECOWAS GDP Growth Dashboard")
st.markdown(
    "Interactive analysis of GDP Growth across selected ECOWAS economies (2015–2025)"
)

st.divider()
# ======================================================
# LOAD DATA
# ======================================================

DATA_PATH = "Data/Processed/ecowas_growth_master.csv"

master = pd.read_csv(DATA_PATH)

years = [str(y) for y in range(2015, 2026)]

# ======================================================
# KPI CARDS
# ======================================================

avg_growth = master["2025"].mean()
highest = master["2025"].max()
lowest = master["2025"].min()

top_country = master.loc[master["2025"].idxmax(), "Country Name"]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Average GDP Growth", f"{avg_growth:.2f}%")
col2.metric("Highest Growth", f"{highest:.2f}%")
col3.metric("Lowest Growth", f"{lowest:.2f}%")
col4.metric("Top Performer", top_country)

# ======================================================
# =====================================================
# INTERACTIVE GDP GROWTH CHART
# =====================================================

st.subheader("GDP Growth Trend (2015–2025)")

# Country selector
country = st.selectbox(
    "Select a country",
    ["All"] + sorted(master["Country Name"].tolist())
)

fig = go.Figure()

# -----------------------------------------------------
# Show ALL countries
# -----------------------------------------------------
if country == "All":

    for _, row in master.iterrows():

        # Highlight Côte d'Ivoire
        if row["Country Name"] == "Cote d'Ivoire":

            line_color = "#F4C542"
            line_width = 4
            opacity = 1

        else:

            line_color = "#6B7280"
            line_width = 1.2
            opacity = 0.35

        fig.add_trace(

            go.Scatter(

                x=years,
                y=row[years],

                mode="lines",

                name=row["Country Name"],

                line=dict(
                    color=line_color,
                    width=line_width
                ),

                opacity=opacity,

                hovertemplate=
                "<b>%{fullData.name}</b><br>"
                "Year: %{x}<br>"
                "GDP Growth: %{y:.2f}%<extra></extra>"

            )
        )

    chart_title = "GDP Growth Trend - All ECOWAS Countries"

# -----------------------------------------------------
# Show ONE country
# -----------------------------------------------------
# -------------------------------------------------
# Show ONE country
# -------------------------------------------------
else:

    selected = master[master["Country Name"] == country].iloc[0]

    fig.add_trace(

        go.Scatter(

            x=years,
            y=selected[years],

            mode="lines+markers",

            name=country,

            line=dict(
                color="#4FC3F7",
                width=4
            ),

            marker=dict(
                size=9
            ),

            hovertemplate=
            "<b>%{fullData.name}</b><br>"
            "Year: %{x}<br>"
            "GDP Growth: %{y:.2f}%<extra></extra>"

        )

    )

    chart_title = f"GDP Growth Trend - {country}"

# -----------------------------------------------------
# Layout
# -----------------------------------------------------

fig.update_layout(

    template="plotly_dark",

    title=chart_title,
    title_x=0.5,
    xaxis_title="Year",
    yaxis_title="GDP Growth (%)",
    height=850,
    legend_title="Country",
    hovermode="x unified",
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117"

)
fig.update_layout(

    font=dict(size=18),

    title_font=dict(size=24),

    xaxis=dict(
        title_font=dict(size=18),
        tickfont=dict(size=18)
    ),

    yaxis=dict(
        title_font=dict(size=18),
        tickfont=dict(size=18)
    ),

    legend=dict(
        font=dict(size=18)
    )
)
st.plotly_chart(fig, use_container_width=True)
# =====================================================
# ==========================================================


# GDP GROWTH DISTRIBUTION (BOXPLOT)
# ==========================================================

st.subheader("📊 GDP Growth Distribution Across ECOWAS (2025)")

fig_box = go.Figure()

fig_box.add_trace(
    go.Box(
        x=master["2025"],
        orientation="h",
        width=0.8,
        marker_color="#7B68EE"
    )
)

fig_box.update_layout(
    template="plotly_dark",
    title="ECOWAS GDP Growth Distribution (2025)",
    title_x=0.5,
    xaxis_title="GDP Growth (%)",
    height=700,

    font=dict(size=18),

title_font=dict(size=24),

xaxis=dict(
    title_font=dict(size=18),
    tickfont=dict(size=18)
),

yaxis=dict(
    tickfont=dict(size=18)
)
)

st.plotly_chart(fig_box, use_container_width=True)

# ==========================================================


# TOP 5 VS BOTTOM 5 GDP GROWTH (2025)
st.subheader("🏆 Top Five and Bottom Five GDP Growth Performers (2025)")
# Top 5 countries
top5 = (
    master[["Country Name", "2025"]]
    .sort_values("2025", ascending=False)
    .head(5)
)

# Bottom 5 countries
bottom5 = (
    master[["Country Name", "2025"]]
    .sort_values("2025", ascending=True)
    .head(5)
)
# Create two columns
col1, col2 = st.columns([1, 1], gap="large")


# -----------------------------
with col1:

    fig_top = go.Figure()

    fig_top.add_trace(
    go.Bar(
        x=top5["2025"],
        y=top5["Country Name"],
        orientation="h",
        width=0.8,
        marker_color="#D4AF37",
        text=top5["2025"].map(lambda x: f"{x:.2f}"),
        textposition="outside",
        textfont=dict(size=18),
    )
)

    fig_top.update_layout(
    template="plotly_dark",
    title="",
    xaxis_title="GDP Growth (%)",
    yaxis_title="",
    height=650,

    font=dict(size=18),

    xaxis=dict(
        title_font=dict(size=18),
        tickfont=dict(size=18)
    ),

    yaxis=dict(
        tickfont=dict(size=18)
    ),

    margin=dict(l=60, r=20, t=20, b=40),
)

    fig_top.update_yaxes(autorange="reversed")

    st.plotly_chart(fig_top, use_container_width=True)


# -----------------------------
with col2:

    fig_bottom = go.Figure()

    fig_bottom.add_trace(
        go.Bar(
            x=bottom5["2025"],
            y=bottom5["Country Name"],
            orientation="h",
            width=0.8,
            marker_color="#C0392B",
            text=bottom5["2025"].map(lambda x: f"{x:.2f}"),
            textposition="outside",
            textfont=dict(size=18)
        )
    )

    fig_bottom.update_layout(
    template="plotly_dark",
    title="",
    xaxis_title="GDP Growth (%)",
    yaxis_title="",
    height=650,

    font=dict(size=18),

    xaxis=dict(
        title_font=dict(size=18),
        tickfont=dict(size=18)
    ),

    yaxis=dict(
        tickfont=dict(size=18)
    ),

    margin=dict(l=60, r=20, t=20, b=40),
)

    fig_bottom.update_yaxes(autorange="reversed")

    st.plotly_chart(fig_bottom, use_container_width=True)
# ==========================================================



# GDP RANKING (2025)
# =====================================================

st.subheader("🏆 ECOWAS GDP Growth Ranking (2025)")

ranking = (
    master[["Country Name", "2025"]]
    .rename(columns={"2025": "GDP Growth (%)"})
    .sort_values("GDP Growth (%)", ascending=False)
    .reset_index(drop=True)
)

ranking.insert(0, "Rank", range(1, len(ranking) + 1))

import plotly.graph_objects as go

fig_table = go.Figure(data=[go.Table(columnwidth=[60, 280, 140],

    header=dict(
        values=["<b>Rank</b>", "<b>Country</b>", "<b>GDP Growth (%)</b>"],
        fill_color="#D4AF37",
        font=dict(color="black", size=18),
        align="center",
        height=50
    ),

    cells=dict(
        values=[
            ranking["Rank"],
            ranking["Country Name"],
            ranking["GDP Growth (%)"].map(lambda x: f"{x:.2f}")
        ],

        fill_color="#0E1117",

        font=dict(
            color="white",
            size=16
        ),

        align=["center","left","center"],
        height=45
    )

)])

fig_table.update_layout(
    template="plotly_dark",
    height=700,
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig_table, use_container_width=True)
# ============================================================
# AVERAGE GDP GROWTH (2015-2025)
# ============================================================

st.subheader("📊 Average GDP Growth (2015–2025)")
# Calculate average GDP growth (2015–2025)

average_growth = (
    master[["Country Name"] + years]
    .copy()
)

average_growth["Average Growth (%)"] = average_growth[years].mean(axis=1)

average_growth = (
    average_growth[["Country Name", "Average Growth (%)"]]
    .sort_values("Average Growth (%)", ascending=False)
)
# ============================================================
# AVERAGE GDP GROWTH BAR CHART
# ============================================================

fig_avg = go.Figure()
colors = []

for i in range(len(average_growth)):

    if i < 3:
        colors.append("#D4AF37")      # Gold (Top 3)
    elif i >= len(average_growth)-2:
        colors.append("#D64545")      # Red (Bottom 2)
    else:
        colors.append("#4F6FAF")      # Blue (Middle)

fig_avg.add_trace(
    go.Bar(
        x=average_growth["Average Growth (%)"],
        y=average_growth["Country Name"],
        orientation="h",
        width=0.8,
        marker_color=colors,
        marker_line_color="white",
        marker_line_width=0.5,
        text=average_growth["Average Growth (%)"].map(lambda x: f"{x:.2f}"),
        textposition="outside",
        textfont=dict(size=18)
    )
)

fig_avg.update_layout(
    template="plotly_dark",
    title="",
    title_x=0.5,

    xaxis_title="Average GDP Growth (%)",
    yaxis_title="",

    height=720,

    font=dict(size=18),

    xaxis=dict(
        title_font=dict(size=18),
        tickfont=dict(size=18)
    ),

    yaxis=dict(
        tickfont=dict(size=18)
    ),

    margin=dict(l=90, r=30, t=20, b=40)
)

fig_avg.update_yaxes(autorange="reversed")

st.plotly_chart(fig_avg, use_container_width=True)


# =====================================================
# EXECUTIVE INSIGHTS
# =====================================================

st.subheader("📝 Executive Insights")

st.markdown("""
### Key Findings

- 🟨 **Guinea** recorded the highest average GDP growth during 2015–2025, closely followed by **Côte d'Ivoire**.
- 📈 Most ECOWAS economies maintained average annual GDP growth between **4% and 6%**, demonstrating regional resilience despite the COVID-19 shock.
- 🟥 **Nigeria** recorded the weakest average growth over the period, reflecting persistent macroeconomic challenges.
- 🌍 The distribution of growth rates indicates considerable differences in economic performance across ECOWAS member states.
- 💡 Sustained structural reforms and economic diversification remain essential for improving long-term growth performance across the region.

---

**Source:** World Bank Open Data (GDP Growth, annual %). Author calculations and visualization.
""")


st.expander("ℹ️ About this Dashboard").markdown("""
### Dashboard Overview

This interactive dashboard presents GDP growth performance across selected ECOWAS economies between **2015 and 2025**.

### Features

• Interactive country trend analysis

• GDP Growth Ranking (2025)

• GDP Growth Distribution (Box Plot)

• Best & Worst Performing Economies (2025)

• Average GDP Growth (2015–2025)

• Executive Insights

### Data Source

World Bank Open Data (Annual GDP Growth, %)

### Purpose

To support evidence-based economic analysis and regional policy discussions through interactive data visualisation.

### Author

**Cesar Carvalho Tavares**
""")

st.markdown("---")

st.markdown(
    """
<div style='text-align:center; color:#B8B8B8; font-size:14px;'>

<b>ECOWAS Intelligence Hub</b><br>

Interactive GDP Growth Dashboard (2015–2025)<br>

Version 1.0 | World Bank Open Data | © 2026 Cesar Carvalho Tavares

</div>
""",
unsafe_allow_html=True
)
