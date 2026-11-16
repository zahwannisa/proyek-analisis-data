import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="E-Commerce Public Dataset Dashboard",
    page_icon="🛒",
    layout="wide"
)

sns.set(style="whitegrid")


@st.cache_data
def load_data():
    # Mengatasi perbedaan working directory saat dijalankan lokal maupun di Streamlit Cloud
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    df = pd.read_csv(file_path)

    # Konversi kolom tanggal
    datetime_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in datetime_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Hitung lama pengiriman (hari) jika belum tersedia
    if "delivery_days" not in df.columns:
        df["delivery_days"] = (
            df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
        ).dt.total_seconds() / 86400.0

    # Pastikan kolom nama kategori bahasa Inggris terisi
    if "product_category_name_english" not in df.columns and "product_category_name" in df.columns:
        df["product_category_name_english"] = df["product_category_name"]
    else:
        df["product_category_name_english"] = df["product_category_name_english"].fillna(
            df.get("product_category_name", "unknown")
        )

    return df


all_df = load_data()

# ==================== SIDEBAR FILTER ====================
with st.sidebar:
    st.title("🛒 Olist E-Commerce")
    st.markdown("Filter data untuk mengeksplorasi performa penjualan dan kepuasan pelanggan.")

    valid_dates = all_df["order_purchase_timestamp"].dropna()
    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    date_range = st.date_input(
        label="Rentang Tanggal Pembelian",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    # Filter opsional berdasarkan kategori
    all_categories = sorted(all_df["product_category_name_english"].dropna().unique().tolist())
    selected_categories = st.multiselect(
        label="Filter Kategori Produk (Opsional)",
        options=all_categories,
        default=[],
        help="Kosongkan untuk menampilkan seluruh kategori produk.",
    )

# Terapkan filter tanggal dan kategori
main_df = all_df[
    (all_df["order_purchase_timestamp"].dt.date >= start_date)
    & (all_df["order_purchase_timestamp"].dt.date <= end_date)
].copy()

if selected_categories:
    main_df = main_df[main_df["product_category_name_english"].isin(selected_categories)]

# ==================== HEADER & KPI METRICS ====================
st.title("📊 E-Commerce Public Dataset Dashboard")
st.markdown(
    f"Menampilkan ringkasan transaksi dari **{start_date.strftime('%d %b %Y')}** hingga **{end_date.strftime('%d %b %Y')}**."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_orders = main_df["order_id"].nunique()
    st.metric("Total Pesanan", f"{total_orders:,}")

with col2:
    total_revenue = main_df["price"].sum() if "price" in main_df.columns else 0
    st.metric("Total Revenue (BRL)", f"R$ {total_revenue:,.2f}")

with col3:
    avg_review = main_df["review_score"].mean() if "review_score" in main_df.columns else 0
    st.metric("Rata-rata Review Score", f"{avg_review:.2f} / 5.00")

with col4:
    avg_delivery = main_df["delivery_days"].dropna().mean()
    st.metric("Rata-rata Lama Pengiriman", f"{avg_delivery:.1f} Hari")

st.divider()

# ==================== PERTANYAAN 1: PERFORMA KATEGORI PRODUK ====================
st.subheader("1. Performa Kategori Produk Berdasarkan Jumlah Pesanan & Total Pendapatan")

delivered_df = main_df[main_df["order_status"] == "delivered"] if "order_status" in main_df.columns else main_df

if delivered_df.empty:
    st.warning("Tidak ada data pesanan berstatus 'delivered' pada rentang filter yang dipilih.")
else:
    cat_perf = (
        delivered_df.groupby("product_category_name_english", as_index=False)
        .agg(
            total_orders=("order_id", "nunique"),
            total_revenue=("price", "sum"),
        )
    )

    tab1, tab2 = st.tabs(["Berdasarkan Jumlah Pesanan", "Berdasarkan Total Revenue"])

    with tab1:
        col_left, col_right = st.columns(2)

        with col_left:
            top_orders = cat_perf.sort_values(by="total_orders", ascending=False).head(5)
            fig, ax = plt.subplots(figsize=(8, 4.5))
            colors_top = ["#1f4e78"] + ["#9dc3e6"] * (len(top_orders) - 1)
            sns.barplot(
                data=top_orders,
                x="total_orders",
                y="product_category_name_english",
                palette=colors_top,
                ax=ax,
            )
            ax.set_title("Top 5 Kategori Produk Terlaris", fontsize=12, fontweight="bold")
            ax.set_xlabel("Jumlah Pesanan")
            ax.set_ylabel("")
            for container in ax.containers:
                ax.bar_label(container, fmt="%d", padding=4, fontsize=9)
            ax.set_xlim(0, top_orders["total_orders"].max() * 1.15)
            st.pyplot(fig)

        with col_right:
            bottom_orders = cat_perf.sort_values(by="total_orders", ascending=True).head(5)
            fig, ax = plt.subplots(figsize=(8, 4.5))
            colors_bot = ["#d95f02"] + ["#f4b183"] * (len(bottom_orders) - 1)
            sns.barplot(
                data=bottom_orders,
                x="total_orders",
                y="product_category_name_english",
                palette=colors_bot,
                ax=ax,
            )
            ax.set_title("5 Kategori Produk dengan Pesanan Terendah", fontsize=12, fontweight="bold")
            ax.set_xlabel("Jumlah Pesanan")
            ax.set_ylabel("")
            for container in ax.containers:
                ax.bar_label(container, fmt="%d", padding=4, fontsize=9)
            ax.set_xlim(0, max(bottom_orders["total_orders"].max() * 1.25, 5))
            st.pyplot(fig)

    with tab2:
        col_left, col_right = st.columns(2)

        with col_left:
            top_rev = cat_perf.sort_values(by="total_revenue", ascending=False).head(5)
            fig, ax = plt.subplots(figsize=(8, 4.5))
            colors_top = ["#1f4e78"] + ["#9dc3e6"] * (len(top_rev) - 1)
            sns.barplot(
                data=top_rev,
                x="total_revenue",
                y="product_category_name_english",
                palette=colors_top,
                ax=ax,
            )
            ax.set_title("Top 5 Kategori Berdasarkan Revenue (BRL)", fontsize=12, fontweight="bold")
            ax.set_xlabel("Total Pendapatan (BRL)")
            ax.set_ylabel("")
            for container in ax.containers:
                ax.bar_label(container, fmt="%.0f", padding=4, fontsize=9)
            ax.set_xlim(0, top_rev["total_revenue"].max() * 1.18)
            st.pyplot(fig)

        with col_right:
            bottom_rev = cat_perf.sort_values(by="total_revenue", ascending=True).head(5)
            fig, ax = plt.subplots(figsize=(8, 4.5))
            colors_bot = ["#d95f02"] + ["#f4b183"] * (len(bottom_rev) - 1)
            sns.barplot(
                data=bottom_rev,
                x="total_revenue",
                y="product_category_name_english",
                palette=colors_bot,
                ax=ax,
            )
            ax.set_title("5 Kategori dengan Revenue Terendah (BRL)", fontsize=12, fontweight="bold")
            ax.set_xlabel("Total Pendapatan (BRL)")
            ax.set_ylabel("")
            for container in ax.containers:
                ax.bar_label(container, fmt="%.0f", padding=4, fontsize=9)
            ax.set_xlim(0, max(bottom_rev["total_revenue"].max() * 1.25, 100))
            st.pyplot(fig)

st.divider()

# ==================== PERTANYAAN 2 & ANALISIS LANJUTAN: PENGIRIMAN VS REVIEW ====================
st.subheader("2. Hubungan Lama Pengiriman terhadap Tingkat Kepuasan Pelanggan (Review Score)")

review_delivery_df = main_df.dropna(subset=["review_score", "delivery_days"]).copy()
review_delivery_df = review_delivery_df[review_delivery_df["delivery_days"] >= 0]

if review_delivery_df.empty:
    st.warning("Data review dan lama pengiriman tidak mencukupi untuk filter yang dipilih.")
else:
    col_q2_1, col_q2_2 = st.columns(2)

    with col_q2_1:
        avg_days_by_score = (
            review_delivery_df.groupby("review_score", as_index=False)["delivery_days"]
            .mean()
            .sort_values(by="review_score")
        )
        fig, ax = plt.subplots(figsize=(8, 4.5))
        bar_colors = [
            "#d95f02" if score == 1 else "#1f4e78" if score == 5 else "#9dc3e6"
            for score in avg_days_by_score["review_score"]
        ]
        sns.barplot(
            data=avg_days_by_score,
            x="review_score",
            y="delivery_days",
            palette=bar_colors,
            ax=ax,
        )
        ax.set_title("Rata-rata Lama Pengiriman per Review Score", fontsize=12, fontweight="bold")
        ax.set_xlabel("Review Score (1 - 5)")
        ax.set_ylabel("Rata-rata Lama Pengiriman (Hari)")
        for container in ax.containers:
            ax.bar_label(container, fmt="%.1f hr", padding=4, fontsize=9)
        ax.set_ylim(0, avg_days_by_score["delivery_days"].max() * 1.18)
        st.pyplot(fig)

    with col_q2_2:
        # Binning kategori durasi pengiriman (Analisis Lanjutan)
        bins = [-1, 7, 14, 21, float("inf")]
        labels = [
            "Cepat (≤ 7 Hari)",
            "Normal (8 - 14 Hari)",
            "Lambat (15 - 21 Hari)",
            "Sangat Lambat (> 21 Hari)",
        ]
        review_delivery_df["delivery_category"] = pd.cut(
            review_delivery_df["delivery_days"], bins=bins, labels=labels
        )

        bin_summary = (
            review_delivery_df.groupby("delivery_category", observed=False, as_index=False)
            .agg(
                avg_review=("review_score", "mean"),
                total_orders=("order_id", "nunique"),
            )
        )

        fig, ax = plt.subplots(figsize=(8, 4.5))
        bin_colors = ["#1f4e78", "#5b9bd5", "#f4b183", "#d95f02"]
        sns.barplot(
            data=bin_summary,
            x="delivery_category",
            y="avg_review",
            palette=bin_colors,
            ax=ax,
        )
        ax.set_title("Rata-rata Review Score Berdasarkan Kecepatan Pengiriman", fontsize=12, fontweight="bold")
        ax.set_xlabel("Kategori Durasi Pengiriman")
        ax.set_ylabel("Rata-rata Review Score")
        ax.set_ylim(0, 5.5)
        plt.xticks(rotation=12)
        for container in ax.containers:
            ax.bar_label(container, fmt="%.2f", padding=4, fontsize=9)
        st.pyplot(fig)

st.caption("Submission Proyek Analisis Data • E-Commerce Public Dataset (Olist) • Zahwa Annisa Hendajani (2026)")