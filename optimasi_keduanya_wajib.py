import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.title("📊 Aplikasi Optimasi Produksi (Manual Input)")

st.markdown("Masukkan parameter produksi dan batasan sumber daya untuk menentukan kombinasi produksi optimal dua produk (x dan y).")

st.header("🧾 Input Data Produksi")

col1, col2 = st.columns(2)

with col1:
    profit_x = st.number_input("Keuntungan per unit produk x (contoh: 90000)", value=90000)
    mesin_x = st.number_input("Jam mesin per unit produk x", value=1.0)
    bahan_x = st.number_input("Bahan baku per unit produk x", value=2.0)
    tenaga_x = st.number_input("Jam kerja per unit produk x", value=2.0)

with col2:
    profit_y = st.number_input("Keuntungan per unit produk y (contoh: 20000)", value=20000)
    mesin_y = st.number_input("Jam mesin per unit produk y", value=0.5)
    bahan_y = st.number_input("Bahan baku per unit produk y", value=2.0)
    tenaga_y = st.number_input("Jam kerja per unit produk y", value=1.0)

st.header("📦 Batasan Sumber Daya (Maksimum)")
max_mesin = st.number_input("Total jam mesin tersedia", value=180.0)
max_bahan = st.number_input("Total bahan baku tersedia", value=400.0)
max_tenaga = st.number_input("Total jam tenaga kerja tersedia", value=220.0)

# Model LP
c = [-profit_x, -profit_y]

A = [
    [mesin_x, mesin_y],
    [bahan_x, bahan_y],
    [tenaga_x, tenaga_y]
]
b = [max_mesin, max_bahan, max_tenaga]
bounds = [(0, None), (0, None)]

# Solve
res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

if res.success:
    x, y = res.x
    z = -res.fun

    st.success("✅ Optimasi Berhasil")
    st.write(f"Jumlah produk x (contoh: Banner): **{x:.0f} unit**")
    st.write(f"Jumlah produk y (contoh: Brosur): **{y:.0f} unit**")
    st.write(f"Total Keuntungan Maksimum: **Rp {z:,.0f}**")

    # Visualisasi
    st.subheader("📈 Visualisasi Daerah Solusi dan Titik Optimal")

    fig, ax = plt.subplots()
    x_vals = np.linspace(0, 100, 400)

    try:
        y_mesin = (max_mesin - mesin_x * x_vals) / mesin_y
    except ZeroDivisionError:
        y_mesin = np.full_like(x_vals, np.inf)

    try:
        y_bahan = (max_bahan - bahan_x * x_vals) / bahan_y
    except ZeroDivisionError:
        y_bahan = np.full_like(x_vals, np.inf)

    try:
        y_tenaga = (max_tenaga - tenaga_x * x_vals) / tenaga_y
    except ZeroDivisionError:
        y_tenaga = np.full_like(x_vals, np.inf)

    y_min = np.minimum(np.minimum(y_mesin, y_bahan), y_tenaga)
    y_min = np.maximum(y_min, 0)

    ax.plot(x_vals, y_mesin, label="Kendala Mesin")
    ax.plot(x_vals, y_bahan, label="Kendala Bahan Baku")
    ax.plot(x_vals, y_tenaga, label="Kendala Tenaga Kerja")

    ax.fill_between(x_vals, 0, y_min, color="skyblue", alpha=0.5, label="Daerah Feasible")

    ax.plot(x, y, 'ro', label=f"Titik Optimal ({x:.0f}, {y:.0f})")
    ax.annotate(f"({x:.0f}, {y:.0f})", (x, y), textcoords="offset points", xytext=(-10, 10), color="red")

    ax.set_xlabel("Produk x")
    ax.set_ylabel("Produk y")
    ax.set_xlim(0, max(100, x + 10))
    ax.set_ylim(0, max(100, y + 10))
    ax.grid(True)
    ax.set_title("Grafik Optimasi Produksi")
    ax.legend()

    st.pyplot(fig)
else:
    st.error("❌ Optimasi gagal. Cek kembali input kendala dan parameter.")
