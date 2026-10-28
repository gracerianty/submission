from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# 1. KONFIGURASI DASHBOARD
st.set_page_config(
    page_title="Bike Sharing Analysis",
    page_icon="🚲",
    layout="wide"
)

st.title("Bike Sharing Analysis Dashboard")
st.write(
    "Dashboard untuk menganalisis pola penyewaan sepeda "
    "berdasarkan waktu, musim, dan kondisi cuaca."
)

# 2. MEMUAT DATASET
DATA_PATH = Path(__file__).parent / "main_data.csv"

REQUIRED_COLUMNS = [
    "dteday",
    "season",
    "weathersit",
    "casual",
    "registered",
    "cnt"
]


@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)

    data["dteday"] = pd.to_datetime(
        data["dteday"],
        errors="coerce"
    )

    # Pemetaan kode musim pada Bike Sharing Dataset
    season_map = {
        1: "Winter",
        2: "Spring",
        3: "Summer",
        4: "Fall"
    }

    weather_map = {
        1: "Clear / Few Clouds",
        2: "Mist / Cloudy",
        3: "Light Rain / Snow",
        4: "Heavy Rain / Other"
    }

    data["season_name"] = data["season"].map(season_map)
    data["weather_name"] = data["weathersit"].map(weather_map)

    data = data.dropna(subset=["dteday"])

    return data


if not DATA_PATH.exists():
    st.error(
        "File main_data.csv tidak ditemukan. "
        "Letakkan file tersebut di folder yang sama dengan dashboard.py."
    )
    st.stop()

try:
    df = load_data(str(DATA_PATH))
except (ValueError, KeyError, pd.errors.ParserError) as error:
    st.error(f"Dataset gagal dibaca: {error}")
    st.stop()

missing_columns = [
    column for column in REQUIRED_COLUMNS
    if column not in df.columns
]

if missing_columns:
    st.error(
        "Kolom berikut tidak ditemukan dalam dataset: "
        + ", ".join(missing_columns)
    )
    st.stop()

if df.empty:
    st.error("Dataset tidak memiliki baris dengan tanggal yang valid.")
    st.stop()


# 3. FILTER RENTANG TANGGAL
st.sidebar.header("Filter Data")

min_date = df["dteday"].min().date()
max_date = df["dteday"].max().date()

date_range = st.sidebar.date_input(
    "Pilih rentang tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range

    filtered = df[
        (df["dteday"].dt.date >= start_date)
        & (df["dteday"].dt.date <= end_date)
    ].copy()
elif isinstance(date_range, (tuple, list)) and len(date_range) == 1:
    selected_date = date_range[0]

    filtered = df[
        df["dteday"].dt.date == selected_date
    ].copy()
else:
    filtered = df[
        df["dteday"].dt.date == date_range
    ].copy()

if filtered.empty:
    st.warning("Tidak ada data pada rentang tanggal tersebut.")
    st.stop()


# 4. RINGKASAN METRIK
total_rentals = int(filtered["cnt"].sum())
average_daily = filtered["cnt"].mean()
registered_total = int(filtered["registered"].sum())
casual_total = int(filtered["casual"].sum())

st.subheader("Ringkasan Penyewaan")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Penyewaan",
    f"{total_rentals:,.0f}"
)

col2.metric(
    "Rata-rata Harian",
    f"{average_daily:,.0f} sepeda"
)

col3.metric(
    "Penyewaan Terdaftar",
    f"{registered_total:,.0f}"
)

col4.metric(
    "Penyewaan Kasual",
    f"{casual_total:,.0f}"
)

st.caption(
    "Total dan rata-rata dihitung berdasarkan rentang tanggal yang dipilih."
)

st.divider()


# 5. TREN PENYEWAAN HARIAN
st.subheader("1. Tren Penyewaan Sepeda Harian")

daily_data = (
    filtered.groupby("dteday", as_index=False)["cnt"]
    .sum()
    .sort_values("dteday")
)

fig_trend = px.line(
    daily_data,
    x="dteday",
    y="cnt",
    labels={
        "dteday": "Tanggal",
        "cnt": "Jumlah penyewaan (sepeda)"
    },
    template="simple_white"
)

fig_trend.update_traces(
    line=dict(width=2),
    hovertemplate=(
        "Tanggal: %{x|%d %b %Y}<br>"
        "Penyewaan: %{y:,.0f} sepeda"
        "<extra></extra>"
    )
)

fig_trend.update_layout(
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20),
    hovermode="x unified"
)

fig_trend.update_xaxes(
    title_text="Tanggal",
    showgrid=False
)

fig_trend.update_yaxes(
    rangemode="tozero",
    title_text="Jumlah penyewaan (sepeda)",
    gridcolor="lightgray"
)

st.plotly_chart(
    fig_trend,
    width="stretch"
)

st.caption(
    "Grafik menunjukkan perubahan jumlah penyewaan harian. "
    "Pola yang terlihat bersifat deskriptif."
)

# 6. RATA-RATA PENYEWAAN BERDASARKAN MUSIM
st.subheader("2. Rata-rata Penyewaan Berdasarkan Musim")

season_order = [
    "Winter",
    "Spring",
    "Summer",
    "Fall"
]

season_data = (
    filtered.groupby("season_name", observed=True, as_index=False)["cnt"]
    .mean()
    .rename(columns={"cnt": "average_rentals"})
)

season_data["season_name"] = pd.Categorical(
    season_data["season_name"],
    categories=season_order,
    ordered=True
)

season_data = season_data.sort_values("season_name")

fig_season = px.bar(
    season_data,
    x="season_name",
    y="average_rentals",
    labels={
        "season_name": "Musim",
        "average_rentals": "Rata-rata penyewaan (sepeda/hari)"
    },
    template="simple_white"
)

fig_season.update_traces(
    hovertemplate=(
        "Musim: %{x}<br>"
        "Rata-rata: %{y:,.0f} sepeda/hari"
        "<extra></extra>"
    )
)

fig_season.update_layout(
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20)
)

fig_season.update_xaxes(
    title_text="Musim",
    showgrid=False
)

fig_season.update_yaxes(
    rangemode="tozero",
    title_text="Rata-rata penyewaan (sepeda/hari)",
    gridcolor="lightgray"
)

st.plotly_chart(
    fig_season,
    width="stretch"
)

st.caption(
    "Grafik membandingkan rata-rata penyewaan harian pada setiap musim, "
    "bukan total penyewaan selama musim tersebut."
)

# 7. RATA-RATA PENYEWAAN BERDASARKAN CUACA
st.subheader("3. Rata-rata Penyewaan Berdasarkan Cuaca")

weather_data = (
    filtered.groupby("weather_name", as_index=False)["cnt"]
    .mean()
    .rename(columns={"cnt": "average_rentals"})
    .sort_values("average_rentals", ascending=False)
)

fig_weather = px.bar(
    weather_data,
    x="weather_name",
    y="average_rentals",
    labels={
        "weather_name": "Kondisi cuaca",
        "average_rentals": "Rata-rata penyewaan (sepeda/hari)"
    },
    template="simple_white"
)

fig_weather.update_traces(
    hovertemplate=(
        "Cuaca: %{x}<br>"
        "Rata-rata: %{y:,.0f} sepeda/hari"
        "<extra></extra>"
    )
)

fig_weather.update_layout(
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20)
)

fig_weather.update_xaxes(
    title_text="Kondisi cuaca",
    showgrid=False,
    tickangle=-15
)

fig_weather.update_yaxes(
    rangemode="tozero",
    title_text="Rata-rata penyewaan (sepeda/hari)",
    gridcolor="lightgray"
)

st.plotly_chart(
    fig_weather,
    width="stretch"
)

st.caption(
    "Semua kategori cuaca yang tersedia dalam data ditampilkan. "
    "Perbedaan rata-rata tidak membuktikan hubungan sebab-akibat."
)

# 8. PERBANDINGAN JENIS PENYEWA
st.subheader("4. Komposisi Penyewaan")

rental_type_data = pd.DataFrame({
    "Jenis penyewa": [
        "Terdaftar",
        "Kasual"
    ],
    "Jumlah penyewaan": [
        registered_total,
        casual_total
    ]
})

fig_rental_type = px.bar(
    rental_type_data,
    x="Jenis penyewa",
    y="Jumlah penyewaan",
    labels={
        "Jenis penyewa": "Jenis penyewa",
        "Jumlah penyewaan": "Total penyewaan (sepeda)"
    },
    template="simple_white"
)

fig_rental_type.update_traces(
    hovertemplate=(
        "Jenis: %{x}<br>"
        "Total: %{y:,.0f} penyewaan"
        "<extra></extra>"
    )
)

fig_rental_type.update_layout(
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20)
)

fig_rental_type.update_xaxes(
    title_text="Jenis penyewa",
    showgrid=False
)

fig_rental_type.update_yaxes(
    rangemode="tozero",
    title_text="Total penyewaan (sepeda)",
    gridcolor="lightgray"
)

st.plotly_chart(
    fig_rental_type,
    width="stretch"
)

# 9. TABEL DATA
with st.expander("Lihat data yang digunakan"):
    display_columns = [
        "dteday",
        "season_name",
        "weather_name",
        "casual",
        "registered",
        "cnt"
    ]

    display_data = filtered[display_columns].rename(
        columns={
            "dteday": "Tanggal",
            "season_name": "Musim",
            "weather_name": "Kondisi Cuaca",
            "casual": "Penyewaan Kasual",
            "registered": "Penyewaan Terdaftar",
            "cnt": "Total Penyewaan"
        }
    )

    st.write(f"Jumlah baris: {len(filtered):,}")

    st.dataframe(
        display_data,
        width="stretch",
        hide_index=True
    )

# 10. CATATAN INTERPRETASI
st.divider()

st.subheader("Catatan Interpretasi")

st.markdown(
    """
    - **Sumber data:** Bike Sharing Dataset.
    - **Satuan:** jumlah penyewaan sepeda.
    - **Tren harian:** menunjukkan perubahan penyewaan dari waktu ke waktu.
    - **Perbandingan musim dan cuaca:** menggunakan rata-rata penyewaan
      harian agar nilai kategori dapat dibandingkan.
    - **Filter tanggal:** memengaruhi metrik, grafik, dan tabel data.
    - **Batasan analisis:** pola yang ditampilkan bersifat deskriptif.
      Grafik tidak dengan sendirinya membuktikan hubungan sebab-akibat.
    """
)

st.caption(
    "Visualisasi dirancang untuk menampilkan data secara jelas, "
    "menghindari dekorasi yang tidak diperlukan, dan menjaga interpretasi."
)