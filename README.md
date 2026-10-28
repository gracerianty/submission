# Bike Sharing Data Analysis
## Deskripsi Proyek

Proyek ini menganalisis pola penyewaan sepeda berdasarkan data harian dan per jam. Analisis mencakup proses pengumpulan data, penilaian kualitas data, pembersihan data, eksplorasi data, visualisasi, dan analisis lanjutan yang relevan.

Dashboard dibuat menggunakan Streamlit untuk memudahkan eksplorasi tren penyewaan sepeda berdasarkan tanggal, musim, dan kondisi cuaca.

## Struktur Folder
- `dashboard/`: kode dashboard dan dataset yang digunakan dashboard.
- `data/`: dataset harian, dataset per jam, dan dokumentasi dataset.
- `notebook.ipynb`: notebook analisis data.
- `requirements.txt`: daftar library yang dibutuhkan.
- `url.txt`: tautan dashboard setelah deployment.

## Dataset
Dataset yang digunakan adalah Bike Sharing Dataset, yang terdiri dari:

- `day.csv`: data penyewaan sepeda harian.
- `hour.csv`: data penyewaan sepeda per jam.
- `Readme.txt`: dokumentasi dataset.

## Persiapan Lingkungan
Pastikan Python telah terpasang. Buka terminal pada folder utama proyek, kemudian jalankan:

```bash
pip install -r requirements.txt
```

## Menjalankan Notebook
Buka notebook melalui Jupyter Notebook atau JupyterLab:

```bash
jupyter notebook
```

Pilih `notebook.ipynb`, lalu jalankan seluruh sel secara berurutan.

## Menjalankan Dashboard
Dari folder utama proyek, jalankan:

```bash
streamlit run dashboard/dashboard.py
```
Dashboard akan terbuka melalui browser pada alamat lokal yang ditampilkan oleh Streamlit.

## Deployment Dashboard
Dashboard dapat di-deploy melalui Streamlit Community Cloud dengan menghubungkan repository GitHub yang berisi proyek ini dan memilih file `dashboard/dashboard.py` sebagai entry point.

Setelah deployment berhasil, masukkan URL dashboard yang aktif ke dalam `url.txt`.

## Catatan
Hasil analisis bersifat deskriptif. Perbedaan jumlah penyewaan yang terlihat pada grafik tidak dengan sendirinya membuktikan hubungan sebab-akibat.
