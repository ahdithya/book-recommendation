	# Project Book Recommendation

Disusun oleh: Aditya Atallah

## Overview
Buku merupakan salah satu media dalam menyampaikan informasi dan pengetahuan bahkan sebuah cerita. Pada era digital sekarang, jumlah informasi dan buku yang dapat diakses sangatlah banyak, dengan berbagai variasi topik pada setiap informasi dan buku yang ada. Hal ini menyebabkan kesulitan dalam menemukan buku yang sesuai dengan minat pembaca. Untuk mengatasi hal tersebut, Sistem rekomendasi dapat digunakan untuk memprediksi barang tertentu yang disukai oleh pengguna atau untuk mengidentifikasi beberapa barang yang mungkin disukai oleh pengguna tertentu [1]. 


Sistem sekomendasi buku adalah salah sistem rekomendasi yang digunakan untuk memberikan rekomenadasi buku kepada pengguna. sehingga sistem ini dapat memudahkan pengguna menemukan buku yang disukai. Jika sistem ini diterapkan pada usaha buku, sistem dapat meningkatkan kepuasan pelanggan, meningkat visibilitas buku serta meningkatkan penjualan buku. Penerapan rekomendasi di dalam sebuah sistem biasanya melakukan prediksi di dalam sebuah item, seperti rekomendasi film, musik, buku, berita dan lain sebagainya [2].

Berdasarkan hal itu, sistem rekomendasi ini memberikan manfaat bagi pengguna, pelaku industri buku dan masyarakat umum. yaitu menemukan buku yang sesua keinginan pengguna, meningkatkan penjualan pelaku industri serta meningkatkan keingintahuan dan minat membaca masyarakat

## Bussines Understanding
### Problem Statement
- Bagaimana cara menemukan buku yang relevan dengan pengguna?
- Bagaimana cara sistem rekomendasi buku dapat memberikan buku yang sesuai minat pengguna?

### Goals
-  Menerapkan sistem rekomendasi dengan metode content base filtering
-  Menghasilkan rekomendasi yang sesuai minat pengguna secara akurat dan relevan

### Solution Statement
- Mengumpulkan data pengguna dan buku yang cukup untuk melatih sistem rekomendasi.
- Implementasikan sistem rekomendasi buku dengan menggunakan metode collaborative filtering dan content-based filtering
## Data Understanding
Dataset yang digunakan adalah `Book Recommendation Dataset` yang dapat diakses melalui situs kaggle. berikut tautannya : [Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset). Pada Dataset ini tidak terdapat genre, sehingga nantinya untuk proyek ini pengguna akan ditentukan berdasarkan kesukaan pengguna terhadap author buku tersebut.

Pada dataset ini terdapat 3 file yaitu Books, Ratings dan Users. Berikut penjelasan tiap file
__Books__
- File dalam bentuk csv (Comma Seperated Value)
- File memiliki 271360 sample data dan 8 variable
- Terdapat missing values



__Ratings__
- File dalam bentuk csv (Comma Seperated Value)
- File memiliki 1149780 sample data dan 3 variable
- tidak terdapat missing value

__Users__
- File dalam bentuk csv (Comma Seperated Value)
- File memiliki 278858 samples data 3 variable
- tidak terdapat missing value

### Informasi Variable 
__Books__
- `ISBN` : Kode Buku 
- `Book-Title` : Judul Buku
- `Book-Author`: Penulis Buku
- `Year-Of-Publication ` : Tahun Terbit Buku
- `Publisher` : Penerbit Buku
- `Image-URL-S`: Ukuran Kecil Gambar Buku
- `Image-URL-M` : Ukuran Menengah Gambar Buku
- `Image-URL-L` : Ukuran Besar Gambar Buku



__Ratings__
- `Users-ID`: Id pengguna
- `ISBN`: Kode Buku
- `Book-Rating`: Penilaian Buku

__Users__
- `Users-ID`: Id Pengguna
- `Location`: Lokasi Pengguna
- `Age`: Umur Pengguna

### Exploratory Data Analysis
#### Univariate
##### Books
Pada informasi variable terhadap data books, terdapat type data yang tidak sesuai yaitu `Year-Of-Publication` sehingga akan melakukan pengubahan type data. Pada variable `Image-URL-S`, `Image-URL-M` dan `Image-URL-L` akan dihapus karena tidak terlalu digunakan dalam pemodelan sistem rekomendasi nantinya. Berikut tampilan jumlah nilai unique tiap variable:
- Jumlah ISBN Buku: 271357 
- Jumlah Judul Buku: 242132 
- Jumlah Penulis Buku: 102022
- Jumlah Tahun Terbit buku: 116 
- Jumlah Penerbit Buku: 16805

Terlihat ISBN buku tidak memiliki jumlah yang sama dengan Judul Buku, yang berarti didalam data terdapat data yang hilang atau duplikat. Sehingga nanti akan dilakukan _Cleaning_ pada data

##### Ratings
Pada Informasi Variable terhadap data Ratings, data tidak memiliki suatu error atau _missing value_. berikut hasil jumlah nilai unique tiap variable :
- Jumlah User ID: 105283 
- Jumlah ISBN buku: 340556

Terdapat 105.283 user yang melakukan penilai terhadap 340556 buku. untuk penyebaran rating dapat dilihat sebagai berikut:

<div>
    <img src="https://github.com/ahdithya/book-recommendation/assets/91508590/adf69bff-3f13-4503-a109-6b8524c22ced"  style='display: block;
    margin-left: auto;
    margin-right: auto;'/>
  </div><br>

Jumlah users yang menilai rating 0 mencapai 700.000 sedangkan pada rating yang lain berada dibawah 200.000.

##### Users
Pada Informasi Variable terhadap data users, data memiliki missing value pada variable age. Jumlah User yang terdaftar pada data users adalah 105.283. Selanjutnya pada umur pengguna sebagai berikut

<div>
    <img src="https://github.com/ahdithya/book-recommendation/assets/91508590/ef8b94c0-3024-4774-b7b6-e4a4ed1e39ff"  style='display: block;
    margin-left: auto;
    margin-right: auto;'/>
  </div><br>

terlihat umur rata-rata user berada disekitaran 25-35 tahun.
## Data Preparation
Mempersiapkan data sangatlah penting dalam proses pengembangan model machine learning. pada proyek ini sangat penting melakukan _Data Preparation_. Jika data tidak dipersiapkan dengan benar maka akan mengganggu hasil analisis terhadap data dan pada modelan machine learning nantinya serta _Data Preparation_ sangat penting untuk meningkatkan kualitas data

Pada Proyek ini akan melakukan beberapa tahapan _Data Preparation_ sebagai berikut:
### Integrasi Data
Pada tahap ini menggabungkan data `Books` dan `Ratings` agar dapat digunakan dalam pemodelan nantinya. untuk melakukan penggabungan data, dapat menggunakan code berikut:

```
books_rating =  pd.merge(ratings, books, on='ISBN', how='left')
```

### Missing Value
Pada proses penggabung bisa saja terdapat missing value, sehingga perlu melakukan pengecekan agar tidak terjadi error nantinya dalam proses pemodelan. Pada DataFrame terdapat missing value berjumlah 118.648 pada variable `Book-Title`, `Book-Author`, `Year-Of-Publication` dan `Publisher`. Untuk mengatasi ini akan melakukan penghapusan pada data yang terdapat missing value dengan code berikut :

```
books_clean = books_rating.dropna()
```

Sebelumnya, terdapat rating yang bernilai 0, pada dasarnya rating tidak dimulai dari 0 melainkan dari satu. penyebab rating 0 bisa berbagai hal seperti pengguna tidak mengisi penilaian sehingga sistem akan memasukan nilai 0. untuk itu akan melakukan penghapusan juga pada data yang memiliki rating 0
### Duplicated
Pada sebuah data bisa terdapat duplikat, karena dalam pemodelan ini hanya akan menggunakan data unik, sehingga akan melakukan pembersihan pada data yang duplikat dengan code berikut:
```
preparation = books_clean.drop_duplicates('placeID')
```


## Modelling and Result
Pada Modelling sistem rekomendasi akan menggunakan 2 pendeketan yaitu Metode Content Based Filtering dan Collaborative Filtering.

### Content Based Filtering
Untuk memudahkan pengguna mendapatkan buku yang sesuai atau relavan dapat menggunakan pendekatan Content Based Filtering yang memberikan item (buku) yang sesuai berdasarkan kesukaan pengguna sebelumnya. Content Based Filtering mempelajari minat pengguna berdasarkan dari data objek yang disukai di masa lalu. Semakin banyak informasi yang diberikan pengguna, semakin baik akurasi sistem rekomendasi.

Berikut Kelebihan dan Kekurangan Content Based Filtering:

Kelebihan :
- Memberikan rekomendasi berdasarkan preferensi pengguna
- Tidak bergantung pada Data Eksternal, seperti item populer atau pengguna lain
- Dapat memberikan rekomendasi terhadap item baru

Kekurangan:
- Merekomendasikan item yang serupa
- Tidak Mampu Menangani Perubahan Selera Pengguna

#### TF-IDF
Sebelum data digunakan untuk pemodelan, data perlu diubah terlebih dahulu kedalam bentuk numerik agar dapat digunakan sebagai masukan pada Model Machine Learning nantinya.  Salah satu teknik yang akan digunakan pada proyek ini adalah TF-IDF (_Term Frequency-Inverse Document Frequency_). 

TF-IDF bertujuan untuk mengukur seberapa penting suatu kata terhadap kata-kata lain dalam dokumen. TF-IDF adalah skema representasi yang umum digunakan untuk sistem pengambilan informasi dan ekstraksi dokumen yang relevan dengan kueri tertentu.

pada proyek ini TF-IDF dapat digunakan dengan cara memanggil fungsi `TfidfVectorizer()` pada sklearn.

#### Cosine Similarity
Cosine similarity adalah metrik yang digunakan untuk mengukur sejauh mana dua vektor arah mendekati sejajar satu sama lain. Dalam sistem rekomendasi, cosine similarity digunakan untuk menentukan seberapa mirip dua item atau dua profil pengguna berdasarkan preferensi mereka terhadap fitur-fitur tertentu. Semakin tinggi nilai cosine similarity antara dua item, semakin mirip kedua item tersebut. 

Rumus Cosine Similarity

<div>
    <img src="https://github.com/ahdithya/book-recommendation/assets/91508590/8b084110-c054-4091-b08b-f33ba8f67591"  style='display: block;
    margin-left: auto;
    margin-right: auto;'/>
  </div><br>

Hasil dari perhitungan cosine similarity adalah nilai antara -1 dan 1. Nilai 1 menunjukkan bahwa dua vektor sepenuhnya sejajar (sama persis), nilai 0 menunjukkan bahwa vektor tersebut tegak lurus (tidak ada kesamaan), dan nilai -1 menunjukkan bahwa dua vektor sejajar tetapi berlawanan arah.

Pada penerepan Cosine Similarity dapat diakses dengan menggunakan sklearn dan memanggil fungsi `cosine_similarity`

#### Result
Pada hasil pengujian pengguna menyukai buku *Second Inspector Thanet* karya Dorothy Simpson. Berikut hasil 10 Top rekomendasi buku yang telah direkomendasikan berdasarkan sistem rekomendasi:

|  | Title | Author|
|--|----|--------------------------------------------------------------------------|
| 1  | Doomed to Die| Dorothy Simpson|
| 2  | Night She Died -Op/67 | Dorothy Simpson |
| 3  | Close Her Eyes | Dorothy Simpson |
| 4  | Male Impersonators: Men Performing Masculinity | Mark Simpson|
| 5  | Windows 98 To Go | Alan Simpson|
| 6  | The Authentic Annals of the Early Hebrews | Wayne Simpson|
| 7  | American Elegy: A Family Memoir | Jeffrey Simpson|
| 8  | Mccain'S Memories (Intimate Moments, No 785) | Maggie Simpson|
| 9  | James Whitcomb Riley Cookbook (Hoosier Hearths.)| Dorothy J. Williams|
| 10 | Anywhere but here (Vintage contemporaries) | Mona Simpson|

### Collaborative Filtering

Collaborative Filtering berfokus pada memprediksi preferensi pengguna berdasarkan informasi pengguna lain. pendekatan ini melihat pengguna yang memiliki preferensi yang sama dari masa lalu cenderung akan memiliki prefensi yang serupa dimasa depan.

Berikut Kelebihan dan Kekurangan Collaborative Filtering:

Kelebihan :
- Memberikan rekomendasi bahkan untuk pengguna atau item baru berdasarkan  preferensi pengguna lain.
- Dapat Menangani perubahan serela
- Rekomendasi dapat bervariasi

Kekurangan:
- Membutuhkan data yang besar dalam menerapakan Collaborative Filtering
- Rekomendasi sangat bergantung pada kesamaan pengguna atau item
- mengalami kesulitan menangani penambahan item baru atau tren baru

#### Result

Pada Pengujian dilakukan rekomendasi pada user 206109, berikut hasil rekomendasinya

Buku dengan rating tertinggi dari user adalah:
 - Bridal Bargains: Secrets to Throwing a Fantastic Wedding on a Realistic Budget (Bridal Bargains: Secrets to Throwing a Fantastic Wedding on a Realistic Budget) : Denise Fields

Rekomendasi Sistem yang diberikan: 

|  | Title | Author|
|--|----|--------------------------------------------------------------------------|
| 1  |Seabiscuit: An American Legend| LAURA HILLENBRAND|
| 2  | The Phantom Tollbooth  | Norton Juster  |
| 3  | Olive Ann Burns Point of Origin| Patricia Daniels Cornwell  |
| 4  | Tis: A Memoir  | Frank McCourt |
| 5  |  Nicolae: The Rise of Antichrist (Left Behind No. 3) | Tim F. Lahaye |
| 6  | The Sisterhood of the Traveling Pants | Ann Brashares|
| 7  | Message from Nam | Danielle Steel|
| 8  | Attack Of The Deranged Mutant Killer Snow Goons  |Bill Watterson |
| 9  | Forbidden Magic | Jo Beverley |
| 10 | Cold Sassy Tree | Olive Ann Burns|

## Evaluation
Perhitungan akurasi rekomendasi dilakukan untuk mencari nilai error atau kesalahan dari sistem rekomendasi. Perhitungan ini dilakukan dengan membandingkan nilai prediksi dan nilai aktual yang diberikan pengguna untuk setiap pasangan pengguna dan item.

### Content Based Filtering
Untuk mengukur seberapa bagus akurasi rekomendasi, disini menggunakan 3 evaluasi yaitu Precision, Recall dan F1-Score

- Precision
	Precision adalah perbandingan antara True Positive (TP) dengan banyaknya data yang diprediksi positif. rumus untuk Precision

<div>
    <img src="https://github.com/ahdithya/book-recommendation/assets/91508590/f012ef4c-0a4e-4ae7-936d-580c59b3e430"  style='display: block;
    margin-left: auto;
    margin-right: auto;'/>
  </div><br>

- Recall
	Recall adalah perbandingan antara True Positive (TP) dengan banyaknya data yang sebenarnya positif. rumus untuk Recall

<div>
    <img src="https://github.com/ahdithya/book-recommendation/assets/91508590/fb4e74bd-bf3b-44aa-97f0-e1d6b2b2ef51"  style='display: block;
    margin-left: auto;
    margin-right: auto;'/>
  </div><br>

- F1-Score
	F1-Score adalah harmonic mean dari precision dan recall. Nilai terbaik F1-Score adalah 1.0 dan nilai terburuknya adalah 0. Secara representasi, jika F1-Score punya skor yang baik mengindikasikan bahwa model klasifikasi k precision dan recall yang baik. rumus untuk F1-Score:

<div>
    <img src="https://github.com/ahdithya/book-recommendation/assets/91508590/eafaaba2-55c4-4964-b0f6-9ea03ccea8d7"  style='display: block;
    margin-left: auto;
    margin-right: auto;'/>
  </div><br>


Pada Evaluasi hasil model, mendapatkan hasil sebagai berikut:

| | Metrics | Value |  
|-|-----|----|
| | Precision | 1.0 |
| |Recall | 1.0 |
| |F1-Score |1.0|

### Collaborative Filtering
 Perhitungan nilai akurasi rekomendasi dengan pendekatan Collaborative Filtering dilakukan dengan pendekatan Root Mean Square Error (RMSE). RMSE adalah ukuran perbedaan antara angka (nilai populasi dan sampel) yang sering diterapkan yang diprediksi oleh estimator atau mode. RMSE menggambarkan deviasi standar sampel dari perbedaan antara nilai prediksi dan nilai observasi. Berikut hasil RMSE pada sistem rekomendasi:

<div>
    <img src="https://github.com/ahdithya/book-recommendation/assets/91508590/c344c37a-ecbe-4dca-b129-1bb196bdfcc6"  style='display: block;
    margin-left: auto;
    margin-right: auto;'/>
  </div><br>
 
```
RMSE = 0.4652476
```

#### REFERENCE 
[1] SISTEM REKOMENDASI BUKU MENGGUNAKAN METODE ITEM-BASED COLLABORATIVE FILTERING. In Sistem Rekomendasi Buku Menggunakan Metode… 24 Jurnal Masyarakat Informatika (Vol. 9, Issue 2).

[2] Rosita, A., Puspitasari, N., & Kamila, V. Z. (2022). REKOMENDASI BUKU PERPUSTAKAAN KAMPUS DENGAN METODE ITEM-BASED COLLABORATIVE FILTERING. _Sebatik_, _26_(1), 340–346. https://doi.org/10.46984/sebatik.v26i1.1551
