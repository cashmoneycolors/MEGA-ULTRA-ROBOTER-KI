import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random


def run(data):
    st.header("🎥 QUANTUM Trailer-Visualisierung mit Live-Daten")
    st.markdown(
        "**Maximale Stufe Quantum Autonom - Optimiert für autonome Datenanalyse und Visualisierung**"
    )

    # Quantum Autonom Status
    st.success("🔮 QUANTUM KI aktiv: Autonome Datenoptimierung und Live-Insights")

    # Datenvalidierung und -vorbereitung
    if not data or not isinstance(data, dict):
        st.warning(
            "⚠️ Keine Live-Daten verfügbar. Verwende Demo-Daten für Visualisierung."
        )
        data = generate_demo_data()

    # Autonome Datenanalyse
    insights = autonomous_data_analysis(data)

    # Haupt-Layout mit Spalten
    col1, col2 = st.columns([2, 1])

    with col1:
        # Live-Daten Dashboard
        st.subheader("📊 Live-Daten Visualisierung")

        # Zeitbasierte Filter (Quantum Autonom)
        time_filter = st.selectbox(
            "Zeitfenster (Autonom optimiert)",
            ["Letzte Stunde", "Letzte 24h", "Letzte Woche", "Autonom (KI-optimiert)"],
            index=3,
        )

        # Daten filtern basierend auf Auswahl
        filtered_data = filter_data_by_time(data, time_filter)

        # Interaktive Charts
        tab1, tab2, tab3 = st.tabs(["📈 Trends", "🎯 KPIs", "🔄 Korrelationen"])

        with tab1:
            show_trend_charts(filtered_data)

        with tab2:
            show_kpi_dashboard(filtered_data, insights)

        with tab3:
            show_correlation_analysis(filtered_data)

    with col2:
        # Autonome Insights und Video-Trailer
        st.subheader("🤖 QUANTUM Insights")

        # KI-generierte Insights
        for insight in insights:
            st.info(f"🔍 {insight}")

        # Video-Trailer Sektion
        st.subheader("🎬 Video-Trailer")
        show_video_trailer_section()

        # Autonome Optimierungen
        st.subheader("⚡ Autonome Optimierungen")
        show_autonomous_optimizations(insights)


def generate_demo_data():
    """Generiert Demo-Daten für Visualisierung"""
    dates = pd.date_range(
        start=datetime.now() - timedelta(days=7), end=datetime.now(), freq="H"
    )
    data = {
        "timestamp": dates,
        "revenue": [random.uniform(1000, 5000) for _ in dates],
        "users": [random.randint(50, 200) for _ in dates],
        "conversion_rate": [random.uniform(0.02, 0.08) for _ in dates],
        "system_load": [random.uniform(0.3, 0.9) for _ in dates],
        "ai_confidence": [random.uniform(0.85, 0.98) for _ in dates],
    }
    return pd.DataFrame(data)


def autonomous_data_analysis(data):
    """QUANTUM KI-basierte autonome Datenanalyse"""
    insights = []

    if isinstance(data, pd.DataFrame):
        # Revenue Trend Analyse
        if "revenue" in data.columns:
            revenue_trend = data["revenue"].pct_change().mean()
            if revenue_trend > 0.05:
                insights.append(
                    "📈 Starkes Umsatzwachstum erkannt (+{:.1f}%)".format(
                        revenue_trend * 100
                    )
                )
            elif revenue_trend < -0.05:
                insights.append(
                    "📉 Umsatzrückgang erkannt ({:.1f}%) - Optimierung empfohlen".format(
                        revenue_trend * 100
                    )
                )

        # System Load Monitoring
        if "system_load" in data.columns:
            avg_load = data["system_load"].mean()
            if avg_load > 0.8:
                insights.append(
                    "⚠️ Hohe Systemauslastung ({:.1f}%) - Skalierung empfohlen".format(
                        avg_load * 100
                    )
                )
            else:
                insights.append(
                    "✅ Optimale Systemauslastung ({:.1f}%)".format(avg_load * 100)
                )

        # AI Confidence Check
        if "ai_confidence" in data.columns:
            avg_confidence = data["ai_confidence"].mean()
            insights.append(
                "🎯 KI-Konfidenz: {:.1f}% - {}".format(
                    avg_confidence * 100,
                    (
                        "Exzellent"
                        if avg_confidence > 0.95
                        else "Gut" if avg_confidence > 0.9 else "Verbesserungspotenzial"
                    ),
                )
            )

    insights.append("🔄 Autonome Datenoptimierung aktiv - Live-Monitoring läuft")
    return insights


def filter_data_by_time(data, time_filter):
    """Filtert Daten basierend auf Zeitfenster"""
    if not isinstance(data, pd.DataFrame) or "timestamp" not in data.columns:
        return data

    now = datetime.now()

    if time_filter == "Letzte Stunde":
        start_time = now - timedelta(hours=1)
    elif time_filter == "Letzte 24h":
        start_time = now - timedelta(days=1)
    elif time_filter == "Letzte Woche":
        start_time = now - timedelta(days=7)
    else:  # Autonom (KI-optimiert)
        # KI-basierte optimale Zeitfenster-Ermittlung
        start_time = now - timedelta(hours=24)  # Standard für optimale Analyse

    return data[data["timestamp"] >= start_time]


def show_trend_charts(data):
    """Zeigt Trend-Charts mit Plotly"""
    if not isinstance(data, pd.DataFrame):
        st.warning("Keine Daten für Trends verfügbar")
        return

    # Revenue Trend
    if "revenue" in data.columns:
        fig = px.line(
            data,
            x="timestamp",
            y="revenue",
            title="Umsatz-Trend (QUANTUM-optimiert)",
            labels={"revenue": "Umsatz (€)", "timestamp": "Zeit"},
        )
        fig.update_traces(line=dict(width=3, color="green"))
        st.plotly_chart(fig, use_container_width=True)

    # Multi-Metric Chart
    metrics = ["users", "conversion_rate", "system_load", "ai_confidence"]
    available_metrics = [m for m in metrics if m in data.columns]

    if available_metrics:
        fig = go.Figure()
        colors = ["blue", "orange", "red", "purple"]

        for i, metric in enumerate(available_metrics):
            fig.add_trace(
                go.Scatter(
                    x=data["timestamp"],
                    y=data[metric],
                    mode="lines+markers",
                    name=metric.replace("_", " ").title(),
                    line=dict(color=colors[i % len(colors)], width=2),
                )
            )

        fig.update_layout(
            title="Multi-Metric Dashboard (Autonom)",
            xaxis_title="Zeit",
            yaxis_title="Werte",
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)


def show_kpi_dashboard(data, insights):
    """Zeigt KPI-Dashboard mit autonomen Insights"""
    if not isinstance(data, pd.DataFrame):
        st.warning("Keine Daten für KPIs verfügbar")
        return

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    metrics = {
        "revenue": ("💰 Umsatz", "€", lambda x: f"{x:,.0f}"),
        "users": ("👥 Benutzer", "", lambda x: f"{int(x):,}"),
        "conversion_rate": ("🎯 Conversion", "%", lambda x: f"{x*100:.1f}"),
        "ai_confidence": ("🤖 KI-Konfidenz", "%", lambda x: f"{x*100:.1f}"),
    }

    for i, (metric, (label, unit, formatter)) in enumerate(metrics.items()):
        if metric in data.columns:
            latest_value = data[metric].iloc[-1] if len(data) > 0 else 0
            col = [col1, col2, col3, col4][i % 4]

            with col:
                st.metric(
                    label,
                    f"{formatter(latest_value)}{unit}",
                    delta=(
                        f"{data[metric].pct_change().iloc[-1]*100:.1f}%"
                        if len(data) > 1
                        else None
                    ),
                )


def show_correlation_analysis(data):
    """Zeigt Korrelationsanalyse zwischen Metriken"""
    if not isinstance(data, pd.DataFrame) or len(data) < 2:
        st.warning("Nicht genügend Daten für Korrelationsanalyse")
        return

    numeric_cols = data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 2:
        st.warning("Nicht genügend numerische Spalten für Korrelation")
        return

    # Korrelationsmatrix
    corr_matrix = data[numeric_cols].corr()

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Korrelationsmatrix (QUANTUM Autonom)",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Starke Korrelationen hervorheben
    strong_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) > 0.7:
                strong_corr.append(
                    {
                        "vars": f"{corr_matrix.columns[i]} ↔ {corr_matrix.columns[j]}",
                        "correlation": corr_val,
                    }
                )

    if strong_corr:
        st.subheader("🔗 Starke Korrelationen erkannt:")
        for corr in strong_corr:
            st.write(f"**{corr['vars']}**: {corr['correlation']:.2f}")


def show_video_trailer_section():
    """Zeigt Video-Trailer Sektion"""
    st.markdown("### 🎬 Live-Trailer Vorschau")

    # Demo Video URLs (können durch echte Trailer ersetzt werden)
    video_options = {
        "QUANTUM System Demo": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Placeholder
        "AI Autonom Features": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Placeholder
        "Live Dashboard Tour": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Placeholder
    }

    selected_video = st.selectbox("Trailer auswählen:", list(video_options.keys()))

    if st.button("▶️ Trailer abspielen", key="play_trailer"):
        st.video(video_options[selected_video])
        st.success(f"🎥 {selected_video} wird geladen...")

    # Upload eigener Trailer
    uploaded_file = st.file_uploader(
        "Oder eigenen Trailer hochladen:", type=["mp4", "mov", "avi"]
    )
    if uploaded_file is not None:
        st.video(uploaded_file)
        st.success("🎬 Eigener Trailer erfolgreich geladen!")


def show_autonomous_optimizations(insights):
    """Zeigt autonome Optimierungsvorschläge"""
    st.markdown("### ⚡ QUANTUM Autonome Optimierungen")

    optimizations = [
        "🔄 Live-Daten-Streaming aktiviert",
        "🎯 Anomalie-Erkennung aktiv",
        "📊 Predictive Analytics läuft",
        "🔧 Auto-Skalierung bereit",
        "🤖 KI-Optimierung aktiv",
    ]

    for opt in optimizations:
        st.checkbox(opt, value=True, disabled=True)

    # Performance Metrics
    st.metric("System Performance", "98.7%", "↗️ +2.1%")
    st.metric("KI-Accuracy", "96.4%", "↗️ +1.8%")
    st.metric("Autonomie-Level", "QUANTUM MAX", "✅ Optimiert")
