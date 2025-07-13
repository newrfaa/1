import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.title("📈 Optimasi Produksi Banner (dengan Brosur Tetap 40)")

st.write("Nilai produksi brosur (y) dikunci pada **40 unit**, dan sistem akan mencari jumlah banner (x) optimal untuk memaksimalkan keuntungan.")

# Input parameter
profit_x = st.number_input("Keuntungan per unit Banner (Rp)", min_value=1000, value=90000, step=1000)
profit_y = st.number_input("Keuntungan per unit Brosur (Rp)", min_value=1000, value=20000, step=1000)

machine_hours = st.number_input("Kapasitas Waktu Mesin (jam/bulan)", min_value=1, value=150)
material_units = st.number_input("Kapasitas Bahan Baku (unit/bulan)", min_value=1, value=200)
labor_hours = st.number_input("Kapasitas Tenaga Kerja (jam/bulan)", min_value=1, value=200)

# Koefisien kebutuhan per unit
st.markdown("### ⏱️ Waktu Mesin per Unit")
machine_x = st.number_input("Banner (jam)", min_value=0.0, value=1.0)
machine_y = st.number_input("Brosur (jam)", min_value=0.0, value=0.5)

st.markdown("### 🧱 Bahan Baku per Unit")
material_x = st.number_input("Banner (unit)", min_value=0.0, value=2.0)
material_y = st.number_input("Brosur (unit)", min_value=0.0, value=2.0)

st.markdown("### 🧑‍🏭 Tenaga Kerja per Unit")
labor_x = st.number_input("Banner (jam)", min_value=0.0, value=2.0)
labor_y = st.number_input("Brosur (jam)", min_value=0.0, value=1.0)

# Optimasi dengan y = 40
y_fixed = 40

# Fungsi objektif
c = [-profit_x, -profit_y]

# Kendala <=
A_ub = [
    [machine_x, machine_y],
    [material_x, material_y],
    [labor_x, labor_y]
]
b_ub = [machine_hours, material_units, labor_hours]

# Tambahkan kendala kesamaan y = 40
A_eq = [[0, 1]]
b_eq = [y_fixed]

# Optimisasi
if st.button("🔍 Hitung Banner Optimal dengan Brosur = 40"):
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None), (0, None)], method='highs')

    if res.success:
        x = res.x[0]
        y = res.x[1]
        total_profit = -(res.fun)

        st.success("✅ Solusi Optimal Ditemukan:")
        st.write(f"Jumlah **Banner (x)** yang diproduksi: `{x:.2f}` unit")
        st.write(f"Jumlah **Brosur (y)** yang diproduksi: `{y:.2f}` unit")
        st.write(f"Total Keuntungan Maksimal: `Rp {total_profit:,.0f}`")

        # Visualisasi batang jumlah produksi
        st.subheader("📦 Diagram Produksi")
        fig2, ax2 = plt.subplots()
        ax2.bar(["Banner", "Brosur"], [x, y], color=["blue", "green"])
        ax2.set_ylabel("Unit Produksi")
        st.pyplot(fig2)

    else:
        st.error("❌ Tidak ditemukan solusi optimal. Periksa kembali batasan atau kapasitas sumber daya.")
