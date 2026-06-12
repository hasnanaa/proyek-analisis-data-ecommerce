# E-COMMERCE PUBLIC DASHBOARD

*Dashboard* interaktif ini dibuat menggunakan **Streamlit** untuk memvisualisasikan dan menganalisis data publik *e-commerce*. *Dashboard* ini menampilkan tren pesanan harian, preferensi metode pembayaran, demografi pelanggan berdasarkan wilayah, serta segmentasi pelanggan menggunakan analisis RFM (*Recency, Frequency, Monetary*).

---

## Persyaratan Sistem

Sebelum menjalankan program ini, diperlukan **Python** dengan rekomendasi versi 3.8 atau lebih baru, serta beberapa *library* Python berikut:

* `pandas`
* `matplotlib`
* `seaborn`
* `streamlit`

---

## Persiapan & Instalasi

**1. Verifikasi *File* Program**
Pastikan *file* kode program (`dashboard.py`), *file* dataset (`main_data.csv`), serta *file requirements* (`requirements.txt`) berada di **direktori/*folder* yang sama**.

**2. Buat *Virtual Environment***
Buat *Virtual Environment* pada Python dengan **menjalankan perintah berikut** pada Terminal atau Command Prompt:
```bash
# Pengguna Windows
python -m venv env
env\Scripts\activate

# Pengguna Mac/Linux
python3 -m venv env
source env/bin/activate
```

**3. Instalasi *Library* yang Dibutuhkan**
*Install* seluruh *library* yang dibutuhkan dengan menjalankan perintah berikut pada Terminal atau Command Prompt:
```bash
pip install -r requirements.txt
```

---

## Cara Menjalankan Dashboard

Jalankan aplikasi Streamlit dengan mengeksekusi perintah berikut di Terminal/Command Prompt:

```bash
streamlit run dashboard.py
```

Setelah perintah dijalankan, *browser* akan otomatis terbuka dan memuat tampilan antarmuka dashboard pada server lokal dengan alamat `http://localhost:8501`.

---

## Fitur Dashboard

* **Filter Tanggal (*Sidebar*):** Pengguna dapat memfilter seluruh data yang ditampilkan berdasarkan rentang tanggal pesanan (*Start Date* & *End Date*).
* ***Daily Orders* & *Revenue*:** Menampilkan total pesanan dan pendapatan, beserta grafik garis (*line chart*) tren pesanan dari waktu ke waktu.
* ***Payment Method Preference*:** Menampilkan diagram batang kombinasi garis yang membandingkan total penggunaan suatu metode pembayaran dengan rata-rata nilai transaksinya.
* ***Customer Demographics by State*:** Menampilkan 10 peringkat teratas (*Top 10*) negara bagian (*state*) dengan jumlah pelanggan terbanyak.
* **RFM *Analysis* & *Segmentation*:** Menampilkan metrik rata-rata nilai *Recency*, *Frequency*, dan *Monetary* pelanggan. Dilengkapi dengan diagram batang yang mendistribusikan pelanggan ke dalam berbagai segmen kualitas pelanggan (contoh: *Champions*, *Lost Customers*, dll).
