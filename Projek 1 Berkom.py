# Deskripsi: Menghitung total volume air yang harus disiram pada lahan cabai berdasarkan kelembapan tanah, fase pertumbuhan, dan curah hujan harian dengan rumus Delta VWC.

# PROGRAM
# Menghitung rekomendasi volume air siraman presisi (dalam Liter) untuk komoditas cabai
# Tetapan awal:
# Jenis tanah adalah Lempung (kelembaban ideal 16-32%, diambil 24% sebagai nilai tengah)
# Jarak tanam: [antar tanaman: 50 cm], [antar baris: 60 cm]
# Luas area per tanaman = 0.5 m x 0.6 m = 0.3 m²
# Jumlah tanaman/m² = 1 m² / 0.3 m² = 3.33 pohon/m²

# KAMUS
# luas = float
# fase = string
# kmrn_hujan = string
# hujan = float
# humid_awal = float
# delta_vwc = float
# laju_evapo = float
# humid_akhir = float
# f_tanah = float
# base_air = float
# total_kebutuhan = float
# kebutuhan_aktual = float
# air_dari_hujan = float
# total_volume = float
# vol_per_m2 = float

# ALGORITMA

# Variabel Warna ANSI untuk Terminal
RESET = "\033[0m"
KUNING  = "\033[93m"
TEBAL   = "\033[1m"


# Input
print(KUNING + TEBAL + "---Kondisi Perkebunan---" + RESET)
luas = float(input("Masukkan Luas Tanah (m2): "))
if luas <= 0:
    print("Masukkan nilai lebih dari 0 !")
    exit()
else:
    print("Sekarang Masukkan Fase Tanaman !")
print("Pilihan Fase: awal | vegetatif | pembungaan_pembuahan | pemasakan")
print("Tulis sesuai dengan keterangan di atas!")
fase = input("Masukkan Fase Tanaman: ")

kmrn_hujan = input("Apakah kemarin terjadi hujan? (y/n): ")
if kmrn_hujan == "y":
    hujan = float(input("Masukkan Curah Hujan kemarin (mm): "))
else:
    hujan = 0.0

# 1. PROSES HITUNG SIMULASI KELEMBAPAN TANAH
# Kelembapan awal tanah lempung ideal diambil nilai tengahnya (24%)
humid_awal = 24.0

# Hitung kenaikan kelembapan dari hujan kemarin dengan Rumus Delta VWC
# Delta VWC = Hujan (mm) / Kedalaman akar efektif cabai dewasa (300 mm)
delta_vwc = (hujan / 300.0) * 100
kelembapan_pasca_hujan = humid_awal + delta_vwc

# Hitung penurunan kelembapan akibat laju evapotranspirasi (penguapan harian)
if hujan == 0:
    laju_evapo = 5.0  # Cuaca terik, tanah kering 5% sehari
elif hujan < 10.0:
    laju_evapo = 3.0  # Cuaca normal/mendung sejuk, tanah kering 3% sehari
else:
    laju_evapo = 1.0  # Cuaca hujan lebat, penguapan turun 1% sehari

# Hasil akhir kelembapan tanah hari ini setelah hujan dan penguapan
humid_akhir = kelembapan_pasca_hujan - laju_evapo

# Pembatasan logika (menutup selang)
if humid_akhir > 100.0:
    humid_akhir = 100.0
elif humid_akhir < 0.0:
    humid_akhir = 0.0

# 2. PROSES PENENTUAN FAKTOR SIRAM BERDASAR STATUS KELEMBAPAN BARU
if humid_akhir >= 32.0:
    f_tanah = 0.0      # Tanah sangat basah (melampaui batas ideal 32%), stop siram
elif humid_akhir >= 24.0:
    f_tanah = 0.4      # Tanah ideal, hanya butuh air kecil (40%) untuk maintenance
else:
    f_tanah = 1.0      # Tanah di bawah batas ideal minimal, butuh pasokan air penuh (100%)

# 3. PROSES HITUNG VOLUME AIR SIRAMAN (LITER)
if fase == "awal":
    base_air = 0.15
elif fase == "vegetatif":
    base_air = 0.25
elif fase == "pembungaan_pembuahan":
    base_air = 0.52
elif fase == "pemasakan":
    base_air = 0.45
else:
    base_air = 0.0

# Hitung total kebutuhan dasar lahan berdasarkan kelembapan tanah
total_kebutuhan = base_air * 3.33 * luas
kebutuhan_aktual = total_kebutuhan * f_tanah

# Konversi curah hujan harian menjadi volume air dalam liter (1 mm = 1 Liter/m2)
air_dari_hujan = hujan * luas

# KEPUTUSAN FINAL: Kebutuhan aktual kebun dikurangi sumbangan air dari hujan
total_volume = kebutuhan_aktual - air_dari_hujan

# Proteksi ujung selang jika air hujan kemarin sudah melimpah melebihi kebutuhan
if total_volume < 0:
    total_volume = 0.0

# Hitung rata-rata volume air per meter persegi
if luas > 0:
    vol_per_m2 = total_volume / luas
else:
    vol_per_m2 = 0.0

# Output
print()
print("=" * 45)
print()
print(KUNING + TEBAL + "--- HASIL KALKULASI PENYIRAMAN (VWC) ---" + RESET)
print(f"Estimasi Delta VWC Hujan : +{delta_vwc:.2f}%")
print(f"Kelembapan Tanah Hari Ini: {humid_akhir:.2f}%")
print(f"Luas Lahan Kebun         : {luas:.2f} m²")
print(f"Fase Pertumbuhan Cabai   : {fase}")
print()
print("-" * 45)
print()
print(f"Kebutuhan Air/m²         : {vol_per_m2:.2f} Liter/m²")
print(f"TOTAL AIR HARUS DISIRAM  : {total_volume:.2f} Liter")
print()

if total_volume == 0:
    print(KUNING + TEBAL + "💡 Catatan: Tanah sudah cukup basah, hari ini libur menyiram!" + RESET)
print("=" * 45)

