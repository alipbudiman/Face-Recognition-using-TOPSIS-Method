# Face-recognition dengan metode TOPSIS

## METODE TOPSIS

[Metode TOPSIS, yang merupakan singkatan dari **Technique for Order of Preference by Similarity to Ideal Solution**, adalah teknik analisis keputusan yang digunakan untuk memilih alternatif terbaik dari sejumlah pilihan yang ada berdasarkan beberapa kriteria yang relevan]((https://dosenit.com/kuliah-it/metode-topsis)). [Metode ini dikembangkan oleh Hwang dan Yoon pada tahun 1981 dan sering digunakan dalam konteks pengambilan keputusan multi-kriteria](https://nictodev.com/mengenal-metode-topsis-adalah/).

Prinsip dasar dari metode TOPSIS adalah membandingkan setiap alternatif dengan solusi ideal positif (alternatif terbaik) dan solusi ideal negatif (alternatif terburuk) dalam ruang solusi multi-kriteria. [Tujuannya adalah untuk menentukan alternatif yang paling mendekati solusi ideal positif dan paling jauh dari solusi ideal negatif]((https://dosenit.com/kuliah-it/metode-topsis)).

Langkah-langkah dalam metode TOPSIS meliputi:
1. Menentukan kriteria dan alternatif yang akan dievaluasi.
2. Menetapkan bobot untuk setiap kriteria.
3. Membangun matriks keputusan yang dinormalisasi.
4. Menghitung jarak setiap alternatif dari solusi ideal positif dan negatif.
5. Menghitung skor preferensi untuk setiap alternatif.
6. Mengurutkan alternatif berdasarkan skor preferensi dari yang tertinggi ke terendah.

[Metode ini dianggap efisien dalam komputasinya dan memberikan cara yang mudah dipahami untuk mengukur kinerja relatif dari alternatif-alternatif keputusan](https://dosenit.com/kuliah-it/metode-topsis).

## ABOUT PROJECT

Dengan menggunakan [Flask](https://pypi.org/project/Flask/), [Python Face-recognition](https://pypi.org/project/face-recognition/), [Python Open-CV](https://pypi.org/project/opencv-python/), [Numpy](https://pypi.org/project/numpy/) dan modul-modul lainnya. kami membuat aplikasi berbasis web untuk pengenalan wajah dan mengukur keterkaitan kemiripan antara gambar A dengan gambar B, C dan D. Metode TOPSIS akan menghitung beberapa faktor, diantaranya:

1. **Minimum Square Error (MSE).**

    Perbedaan antara setiap piksel pada gambar A dan piksel yang sesuai pada gambar B dihitung, dikuadratkan, dan ditambahkan. Kemudian, jumlah total dibagi dengan jumlah total piksel (lebar dikalikan dengan tinggi) untuk mendapatkan rata-rata, atau “mean”, dari kesalahan kuadrat, yang disebut Mean Squared Error.

    MSE adalah salah satu dari banyak metrik yang dapat digunakan untuk mengukur seberapa mirip dua gambar.

2. **Average Standar Deviation.**

    Standar deviasi adalah ukuran seberapa jauh sekelompok angka menyebar dari rata-rata mereka. Dalam konteks ini, standar deviasi adalah ukuran seberapa jauh intensitas piksel dalam gambar menyebar dari rata-rata intensitas piksel.

    Jika standar deviasi antara gambar A dan gambar lainnya semakin kecil, itu berarti intensitas piksel dalam kedua gambar tersebut menyebar dekat dengan rata-rata mereka, yang berarti gambar tersebut memiliki pola intensitas piksel yang serupa. Oleh karena itu, kita bisa mengatakan bahwa gambar tersebut lebih “mirip” satu sama lain.

2. **Face Distance.**

    Dalam konteks pengenalan wajah, “face distance” merujuk pada pengukuran jarak antara dua enkoding wajah. Jarak ini biasanya dihitung menggunakan metrik seperti Euclidean distance, yang mengukur jarak terpendek antara dua titik dalam ruang berdimensi banyak.

    Dalam pustaka face_recognition Python, fungsi face_distance digunakan untuk menghitung jarak Euclidean antara enkoding wajah yang diketahui dan enkoding wajah yang tidak diketahui. Jarak ini memberi tahu seberapa mirip wajah tersebut. Nilai yang lebih rendah menunjukkan bahwa dua wajah lebih mirip, sementara nilai yang lebih tinggi menunjukkan bahwa mereka kurang mirip.



## PREVIEW



## MENJALANKAN

```
python3 app.py
```

## KONEKSIKAN KE FIREBASE REALTIME DATABASE


sebenarnya untuk melakukan koneksi ke firebase sudah di buat pada program ini, jadi hanya tinggal melakukan setting pada `system_config.jso` pada folder `config/system_config.json`. Untuk melakukan koneksi ke firebase realtime database, ikuti langkah di bawah ini:

1. **Masukan File Firebase Ptivate Key ke dalam folder Config**.

    Untuk file private key kamu bisa dapatkan secara langsung di bagian `Settings -> Project Settings -> Service Account` lalu klick button `Generate New Private Key`. Setelah File Private Key berhasil di download, masukan file private key dari firebase ke dalam folder config

    berikut skemanya:
    ```
    Folder: config
            ↳ system_config.json
            ↳ {{letakan file firebase private key disini}}
    ```

2. **Setting system_config.json**.

Selanjutnya, setting pengaturan di `system_config.json` pada dalam folder `config`.

- "use_firebase_database" menjadi `true`
- "firebase_database_path" menjadi `config/{{nama file firebase private.key}}` 
- "firebase_db_uri" menjadi `refrence url anda` 

contoh config di bawah ini:
```JSON
{
    "use_firebase_database":false,
    "firebase_database_path":"config/spk-alif-firebase-adminsdk-kyjwn-a5042873f7.json",
    "firebase_db_uri":"https://myrealtimedatabase.asia-southeast1.firebasedatabase.app/",
    "firebase_delete_image_time":120
}
```

## AKHIR KATA

Ya begitulah, ini untuk tugas mata kulaih SPK, jadi seadanya aja ya, karena TA nya dikejar deadline wkwk

Thanks to:
    - Bpk. Weri Sirait M.kom (Dosen Matakuliah SPK)
    - Fajar Jero (Yg nemenin ngerjain TA nya wkwkw)



