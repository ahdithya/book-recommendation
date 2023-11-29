# Project Book Recommendation

Disusun oleh: Aditya Atallah

## Overview
Buku merupakan salah satu media dalam menyampaikan informasi dan pengetahuan bahkan sebuah cerita. Pada era digital sekarang, jumlah informasi dan buku yang dapat diakses sangatlah banyak, dengan berbagai variasi topik pada setiap informasi dan buku yang ada. Hal ini menyebabkan kesulitan dalam menemukan buku yang sesuai dengan minat pembaca. Untuk mengatasi hal tersebut, Sistem rekomendasi dapat digunakan untuk memprediksi barang tertentu yang disukai oleh pengguna atau untuk mengidentifikasi beberapa barang yang mungkin disukai oleh pengguna tertentu [1]. 


Sistem sekomendasi buku adalah salah sistem rekomendasi yang digunakan untuk memberikan rekomenadasi buku kepada pengguna. sehingga sistem ini dapat memudahkan pengguna menemukan buku yang disukai. Jika sistem ini diterapkan pada usaha buku, sistem dapat meningkatkan kepuasan pelanggan, meningkat visibilitas buku serta meningkatkan penjualan buku.

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
Dataset yang digunakan adalah `Book Recommendation Dataset` yang dapat diakses melalui situs kaggle. berikut tautannya : [Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)

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
  
## Data Preparation
## Modelling and Result
## Evaluation
## Conclusion


#### REFERENCE 
[1] SISTEM REKOMENDASI BUKU MENGGUNAKAN METODE ITEM-BASED COLLABORATIVE FILTERING. In Sistem Rekomendasi Buku Menggunakan Metode… 24 Jurnal Masyarakat Informatika (Vol. 9, Issue 2).

[2] 
