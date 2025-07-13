import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.set_page_config(page_title="Optimasi Produksi", layout="centered")

st.title("📊 Aplikasi Optimasi Produksi Dua Produk")

st.markdown("Masukkan parameter produksi dan batasan sumber daya untuk menentukan kombinasi produksi optimal dua produk (x dan y).")

# =========================
# INPUT DATA
# =========================

st.header("🧾 Input Data Produksi")

col1, col2 = st.columns(2)

with col1:
    profit_x = st.number_input("Keuntungan per unit produk x (misal: Banner)", value=90000)
    mesin_x = st.number_input("Jam mesin per unit produk x", value=1.0)
    bahan_x = st.number_input("Bahan baku per unit produk x", value=2.0)
    tenaga_x = st.number_input("Jam kerja per unit produk x", value=2.0)

with col2:
    profit_y = st.number_input("Keuntungan per unit produk y (misal: Brosur)", value=20000)
    mesin_y = st.number_input("Jam mesin per unit produk y", value=0.5)
    bahan_y = st.number_input("Bahan baku per unit produk y", value=2.0)
    tenaga_y = st.number_input("Jam kerja per unit produk y", value=1.0)

# =========================
# BATASAN SUMBER DAYA
# =========================

st.header("📦 Batasan Sumber Daya (Maksimum)")
max_mesin = st.number_input("Total jam mesin tersedia", value=180.0)
max_bahan = st.number_input("Total bahan baku tersedia", value=400.0)
max_tenaga = st.number_input("Total jam tenaga kerja tersedia", value=220.0)

# =========================
# OPTIMASI LINEAR
# =========================

# Fungsi objektif
c = [-profit_x, -profit_y]

# Matriks kendala
A = [
    [mesin_x, mesin_y],
    [bahan_x, bahan_y],
    [tenaga_x, tenaga_y]
]
b = [max_mesin, max_bahan, max_tenaga]
bounds = [(0, None), (0, None)]

# Solusi LP
res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

# =========================
# OUTPUT HASIL
# =========================

if res.success:
    x, y = res.x
    z = -res.fun

    st.success("✅ Optimasi Berhasil!")
    st.write(f"Jumlah produk **x** (contoh: Banner): **{x:.0f} unit**")
    st.write(f"Jumlah produk **y** (contoh: Brosur): **{y:.0f} unit**")
    st.write(f"Total Keuntungan Maksimum: **Rp {z:,.0f}**")

    # =========================
    # GRAFIK DAERAH SOLUSI
    # =========================
    st.subheader("📈 Grafik Daerah Feasible & Titik Optimal")

    fig1, ax1 = plt.subplots()
    x_vals = np.linspace(0, max(100, x + 20), 400)

    def safe_divide(a, b):
        return a / b if b != 0 else np.full_like(x_vals, np.inf)

    y_mesin = safe_divide(max_mesin - mesin_x * x_vals, mesin_y)
    y_bahan = safe_divide(max_bahan - bahan_x * x_vals, bahan_y)
    y_tenaga = safe_divide(max_tenaga - tenaga_x * x_vals, tenaga_y)

    y_min = np.minimum.reduce([y_mesin, y_bahan, y_tenaga])
    y_min = np.maximum(y_min, 0)

    ax1.plot(x_vals, y_mesin, label="Kendala Mesin")
    ax1.plot(x_vals, y_bahan, label="Kendala Bahan Baku")
    ax1.plot(x_vals, y_tenaga, label="Kendala Tenaga Kerja")
    ax1.fill_between(x_vals, 0, y_min, alpha=0.4, color='skyblue', label="Daerah Feasible")

    ax1.plot(x, y, 'ro', label=f"Titik Optimal ({x:.0f}, {y:.0f})")
    ax1.annotate(f"({x:.0f}, {y:.0f})", (x, y), textcoords="offset points", xytext=(-10, 10), color='red')

    ax1.set_xlabel("Jumlah Produk x")
    ax1.set_ylabel("Jumlah Produk y")
    ax1.set_xlim(0, max(100, x + 20))
    ax1.set_ylim(0, max(100, y + 20))
    ax1.grid(True)
    ax1.set_title("Daerah Solusi Optimasi Produksi")
    ax1.legend()

    st.pyplot(fig1)

    # =========================
    # GRAFIK BATANG PRODUKSI
    # =========================
    st.subheader("📊 Grafik Jumlah Produksi Optimal")

    fig2, ax2 = plt.subplots()
    produk = ['Produk x', 'Produk y']
    jumlah = [x, y]
    warna = ['#1f77b4', '#ff7f0e']

    bars = ax2.bar(produk, jumlah, color=warna)
    ax2.set_ylabel("Jumlah Unit")
    ax2.set_title("Jumlah Produksi Optimal")

    for bar in bars:
        height = bar.get_height()
        ax2.annotate(f'{height:.0f}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom')

    st.pyplot(fig2)

else:
    st.error("❌ Optimasi gagal. Periksa kembali input kendala dan parameter.")
