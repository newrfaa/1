import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.title("📈 Optimasi Produksi Banner & Brosur")

st.markdown("""
Aplikasi ini menentukan kombinasi optimal produksi banner dan brosur
untuk memaksimalkan keuntungan, berdasarkan keterbatasan sumber daya (mesin, bahan baku, dan tenaga kerja).
""")

# Data sesuai dokumen
profit_banner = 90000
profit_brosur = 20000

# Kendala kapasitas
mesin = 180   # x + 0.5y ≤ 180 → akan cocok dengan x=60, y=100
bahan_baku = 400  # 2x + 2y ≤ 400
tenaga_kerja = 220  # 2x + 1y ≤ 220

# Fungsi objektif
c = [-profit_banner, -profit_brosur]  # Negatif karena linprog = minimisasi

# Kendala
A = [
    [1, 0.5],     # Waktu mesin
    [2, 2],       # Bahan baku
    [2, 1]        # Tenaga kerja
]
b = [mesin, bahan_baku, tenaga_kerja]
bounds = [(0, None), (0, None)]

# Solusi LP
res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

if res.success:
    x, y = res.x
    z = -res.fun

    st.subheader("✅ Hasil Optimasi Produksi")
    st.write(f"Banner (x): **{x:.0f} unit**")
    st.write(f"Brosur (y): **{y:.0f} unit**")
    st.write(f"Keuntungan Maksimal: **Rp {z:,.0f}**")

    # Grafik Wilayah Feasible
    st.subheader("📊 Grafik Daerah Solusi")
    fig, ax = plt.subplots()

    x_vals = np.linspace(0, 100, 400)

    # Setiap garis batas kendala
    y1 = (mesin - 1*x_vals) / 0.5       # mesin
    y2 = (bahan_baku - 2*x_vals) / 2    # bahan baku
    y3 = (tenaga_kerja - 2*x_vals)      # tenaga kerja

    y_vals = np.minimum.reduce([y1, y2, y3])
    y_vals = np.maximum(y_vals, 0)

    ax.plot(x_vals, y1, label="Mesin: x + 0.5y ≤ 180")
    ax.plot(x_vals, y2, label="Bahan: 2x + 2y ≤ 400")
    ax.plot(x_vals, y3, label="Tenaga: 2x + y ≤ 220")

    ax.fill_between(x_vals, 0, y_vals, color="lightblue", alpha=0.5, label="Daerah Feasible")

    # Titik optimal
    ax.plot(x, y, 'ro', label=f"Titik Optimal ({x:.0f}, {y:.0f})")
    ax.annotate(f"({x:.0f}, {y:.0f})", (x, y), textcoords="offset points", xytext=(-15,10), color='red')

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 150)
    ax.set_xlabel("Jumlah Banner (x)")
    ax.set_ylabel("Jumlah Brosur (y)")
    ax.set_title("Visualisasi Optimasi Produksi")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

else:
    st.error("Optimasi gagal. Silakan periksa parameter.")
