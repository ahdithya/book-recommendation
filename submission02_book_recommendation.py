# -*- coding: utf-8 -*-
"""submission02_book_recommendation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z-JVHMFnTN_PP2lru93xkMXbdB9xfjnL

# Book Recommendation

oleh: Aditya Atallah

dataset: https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset/data

## Preparing
"""

!pip install kaggle

from google.colab import files
files.upload()

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d arashnic/book-recommendation-dataset

!unzip book-recommendation-dataset.zip

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from zipfile import ZipFile
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path

"""## Data Collecting"""

books = pd.read_csv('Books.csv')
ratings = pd.read_csv('Ratings.csv')
users = pd.read_csv('Users.csv')

books.head()

ratings.head()

users.head()

"""### Exploratory Data Analysis

#### Univariate

##### Books
"""

# Melihat info data
books.info()

"""pada variable Year-of-Publication, type data bernilai object yang harusnya menjadi int"""

# mengubah type data
books = books[(books['Year-Of-Publication'] !=  'DK Publishing Inc') & (books['Year-Of-Publication'] !=  'Gallimard')]
books['Year-Of-Publication'] = books['Year-Of-Publication'].astype('int')
books.info()

# melakukan drop pada variable Image-URL-S, Image-URL-M, Image-URL-L
books.drop(columns=['Image-URL-S', 'Image-URL-M', 'Image-URL-L'], inplace=True)

print('Jumlah ISBN Buku', len(books['ISBN'].unique()))
print('Jumlah Judul Buku', len(books['Book-Title'].unique()))
print('Jumlah Penulis Buku', len(books['Book-Author'].unique()))
print('Jumlah Tahun Terbit buku', len(books['Year-Of-Publication'].unique()))
print('Jumlah Penerbit Buku', len(books['Publisher'].unique()))

"""##### Ratings"""

ratings.info()

print('Jumlah User ID:', len(ratings['User-ID'].unique()))
print('Jumlah ISBN buku:', len(ratings['ISBN'].unique()))

sns.histplot(ratings['Book-Rating'], bins=10)
plt.show()

"""##### Users"""

users.info()

print('Jumlah User ID:', len(ratings['User-ID'].unique()), '\n')

sns.histplot(users['Age'])
plt.show

"""## Data Preparation

### Integration Data
"""

# menggabungkan data untuk pemodelan
books_rating =  pd.merge(ratings, books, on='ISBN', how='left')
books_rating.head()

"""### Missing Value"""

# mengecek missing value
books_rating.isna().sum()

# menghapus nilai missing value
books_clean = books_rating.dropna()
books_clean.isna().sum()

books_clean.shape

# menghapus nilai rating yang bernilai 0
books_clean = books_clean[(books_clean['Book-Rating'] != 0)]
books_clean.shape

"""### Duplicated"""

# menghapus duplikat pada data
fix_books = books_clean.drop_duplicates('ISBN')

# mengubah tipe data year-ofpublication
fix_books['Year-Of-Publication'] =fix_books['Year-Of-Publication'].astype('int')
fix_books.info()

# Mempersiapkan data untuk model

preparation = fix_books
preparation.sort_values('ISBN')

isbn = preparation['ISBN'].tolist()
title = preparation['Book-Title'].tolist()
rating = preparation['Book-Rating'].tolist()
author = preparation['Book-Author'].tolist()
publication = preparation['Year-Of-Publication'].tolist()
publisher = preparation['Publisher'].tolist()

print(len(isbn))
print(len(title))
print(len(rating))
print(len(author))
print(len(publication))
print(len(publisher))

"""Jumlah data berukuran sama sehingga dapat digunakan untuk pemodelan"""

books_df = pd.DataFrame({
    'ISBN': isbn,
    'Rating': rating,
    'Title': title,
    'Author': author,
    'Publication': publication,
    'Publisher': publisher
})

books_df.head()

# karena laptop saya cukup berat menjalankan komputasi maka data yang banyak maka akan melakukan sampling secara acak sebanyak 10000 data
books_sample = books_df.sample(n=10000, random_state=123)

"""## Modeling and Result

### Content Based Filtering
"""

data = books_sample
data.sample(5)

"""#### TF-IDF"""

from sklearn.feature_extraction.text import TfidfVectorizer

tfid = TfidfVectorizer()
tfid.fit(data['Author'])

tfidf_matrix = tfid.fit_transform(data['Author'])

# Melihat ukuran matrix tfidf
tfidf_matrix.shape

# melihat hasil representasi fitur
pd.DataFrame(
    tfidf_matrix.todense(),
    columns=tfid.get_feature_names_out(),
    index=data.Title
).sample(22, axis=1).sample(10, axis=0)

"""#### Cosine Similarity"""

from sklearn.metrics.pairwise import cosine_similarity

cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim

cosine_sim_df = pd.DataFrame(cosine_sim, index=data['Title'], columns=data['Title'])
print('Shape:', cosine_sim_df.shape)

# Melihat similarity matrix pada setiap resto
cosine_sim_df.sample(5, axis=1).sample(10, axis=0)

def book_recommendations(title, similarity_data=cosine_sim_df, items=data[['Title', 'Author']], k=10):
    index = similarity_data.loc[:,title].to_numpy().argpartition(
        range(-1, -k, -1))
    closest = similarity_data.columns[index[-1:-(k+2):-1]]
    closest = closest.drop(title, errors='ignore')
    return pd.DataFrame(closest).merge(items).head(k)

data.Title.sample(5)

data[data.Title.eq("Second Inspector Thanet")]

"""#### Result"""

# menampilkan rekomendasi buku berdasarkan author
book_recommendations('Second Inspector Thanet')

"""### Collaborative Filtering

#### Data Preparation
"""

# karena data yang terlalu banyak menyebabkan kegagalan saat melakukan komputasi maka hanya akan diambil 10000 data saja
ratings_sample = ratings.sample(n=10000, random_state=123).reset_index()

df = ratings_sample
df.head()

user_ids = df['User-ID'].unique().tolist()
print('list userID: ', user_ids)

user_to_user_encoded = {x: i for i, x in enumerate(user_ids)}
print('encoded User-ID : ', user_to_user_encoded)

# Melakukan proses encoding angka ke ke user-ID
user_encoded_to_user = {i: x for i, x in enumerate(user_ids)}
print('encoded angka ke UserID: ', user_encoded_to_user)

# Mengubah ISBN menjadi list tanpa nilai yang sama
books_ids = df['ISBN'].unique().tolist()

# Melakukan proses encoding ISBN
book_to_book_encoded = {x: i for i, x in enumerate(books_ids)}

# Melakukan proses encoding angka ke ISBN
book_encoded_to_book = {i: x for i, x in enumerate(books_ids)}

# Mapping kedalam variable baru
df['user'] = df['User-ID'].map(user_to_user_encoded)
df['ISBN-Book'] = df['ISBN'].map(book_to_book_encoded)

# Mendapatkan jumlah user
num_users = len(user_to_user_encoded)
print(num_users)

# Mendapatkan jumlah resto
num_books = len(book_encoded_to_book)
print(num_books)

df['Book-Rating'] = df['Book-Rating'].values.astype(np.float32)

# Nilai minimum Book-Rating
min_rating = min(df['Book-Rating'])

# Nilai maksimal Book-Rating
max_rating = max(df['Book-Rating'])

print('Number of User: {}, Number of Resto: {}, Min Rating: {}, Max Rating: {}'.format(
    num_users, num_books, min_rating, max_rating
))

"""#### Spliting Data"""

# Mengacak dataset
df = df.sample(frac=1, random_state=42)
df

# Membuat variabel x untuk mencocokkan data user dan resto menjadi satu value
x = df[['user', 'ISBN-Book']].values

# Membuat variabel y untuk membuat rating dari hasil
y = df['Book-Rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values

# Membagi menjadi 80% data train dan 20% data validasi
train_indices = int(0.8 * df.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:]
)

print(x, y)

"""#### Modeling"""

class RecommenderNet(tf.keras.Model):

  # Insialisasi fungsi
  def __init__(self, num_users, num_books, embedding_size, **kwargs):
    super(RecommenderNet, self).__init__(**kwargs)
    self.num_users = num_users
    self.num_books = num_books
    self.embedding_size = embedding_size
    self.user_embedding = layers.Embedding( # layer embedding user
        num_users,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.user_bias = layers.Embedding(num_users, 1) # layer embedding user bias
    self.resto_embedding = layers.Embedding( # layer embeddings books
        num_books,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.book_bias = layers.Embedding(num_books, 1) # layer embedding books bias

  def call(self, inputs):
    user_vector = self.user_embedding(inputs[:,0]) # memanggil layer embedding 1
    user_bias = self.user_bias(inputs[:, 0]) # memanggil layer embedding 2
    book_vector = self.resto_embedding(inputs[:, 1]) # memanggil layer embedding 3
    book_bias = self.book_bias(inputs[:, 1]) # memanggil layer embedding 4

    dot_user_book = tf.tensordot(user_vector, book_vector, 2)

    x = dot_user_book + user_bias + book_bias

    return tf.nn.sigmoid(x) # activation

model = RecommenderNet(num_users, num_books, 50)
# model compile
model.compile(
    loss = tf.keras.losses.BinaryCrossentropy(),
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001),
    metrics=[tf.keras.metrics.RootMeanSquaredError()]
)

history = model.fit(
    x = x_train,
    y = y_train,
    batch_size = 8,
    epochs = 100,
    validation_data = (x_val, y_val)
)

"""#### Visualiasi Metrik"""

plt.plot(history.history['root_mean_squared_error'])
plt.plot(history.history['val_root_mean_squared_error'])
plt.title('model_metrics')
plt.ylabel('root_mean_squared_error')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

"""#### Result"""

books_df = books
df_ratings = ratings_sample

# mengambil sample user
user_id = df_ratings['User-ID'].sample(1).iloc[0]
book_read_by_user = df_ratings[df_ratings['User-ID'] == user_id]


book_no_read = books_df[~books_df['ISBN'].isin(book_read_by_user['User-ID'].values)]['ISBN']
book_no_read = list(
    set(book_no_read)
    .intersection(set(book_to_book_encoded.keys()))
)

book_no_read = [[book_to_book_encoded.get(x)] for x in book_no_read]
user_encoder = user_to_user_encoded.get(user_id)
user_book_array = np.hstack(
    ([[user_encoder]] * len(book_no_read), book_no_read)
)

rating = model.predict(user_book_array).flatten()

top_ratings_indices = rating.argsort()[-10:][::-1]
recommended_book_ids = [
    book_encoded_to_book.get(book_no_read[x][0]) for x in top_ratings_indices
]

print('Showing recommendations for users: {}'.format(user_id))
print('===' * 9)
print('Books with high ratings from user')
print('----' * 8)

top_books_user = (
    book_read_by_user.sort_values(
        by = 'Book-Rating',
        ascending=False
    )
    .head(5)
    .ISBN.values
)

books_df_rows = books_df[books_df['ISBN'].isin(top_books_user)]
for row in books_df_rows.itertuples():
    print(row._2, ':', row._3)

print('----' * 8)
print('Top 10 Books recommendation')
print('----' * 8)

recommended_books = books_df[books_df['ISBN'].isin(recommended_book_ids)]
for row in recommended_books.itertuples():
    print(row._2, ':', row._3)

"""## Evaluation

### Content Based Filtering
"""

from sklearn.metrics import precision_score, recall_score, f1_score


# menentukan batasan similarity 1 atau 0
threshold = 0.5

# rekomendasi berdasarkan judul
true_title = 'Second Inspector Thanet'
predicted_books = book_recommendations(true_title, similarity_data=cosine_sim_df, items=data[['Title', 'Author']], k=10)

#  Menyusun data label_truth dengan asumsi threshold
label_truth = np.where(cosine_sim_df >= threshold, 1, 0)

# Mengambil subset dari matriks similarity dan label_truth
sample_size = 10000
cosine_sim_sample = cosine_sim_df.iloc[:sample_size, :sample_size]
label_truth_sample = label_truth[:sample_size, :sample_size]

# Mengonversi matriks similarity menjadi array satu dimensi untuk perbandingan
cosine_sim_flat = cosine_sim_sample.values.flatten()

# Mengonversi matriks label_truth menjadi array satu dimensi
label_truth_flat = label_truth_sample.flatten()

# Menghitung metrik evaluasi
precision = precision_score(label_truth_flat, (cosine_sim_flat >= threshold).astype(int), zero_division=1)
recall = recall_score(label_truth_flat, (cosine_sim_flat >= threshold).astype(int), zero_division=1)
f1 = f1_score(label_truth_flat, (cosine_sim_flat >= threshold).astype(int), zero_division=1)

evaluation_result = pd.DataFrame({
    'Metric': ['Precision', 'Recall', 'F1-Score'],
    'Value': [precision, recall, f1]
})

evaluation_result

"""### Collaborative Filtering"""

from sklearn.metrics import mean_squared_error

# Prediksi rating untuk buku yang tidak dibaca oleh user
predicted_ratings = model.predict(user_book_array).flatten()

# Ambil rating sebenarnya untuk buku yang tidak dibaca oleh user
true_ratings = np.array([
    df_ratings[
        (df_ratings['User-ID'] == user_id) &
        (df_ratings['ISBN'] == book_encoded_to_book.get(book_id))
    ]['Book-Rating'].values[0]
    if not df_ratings[
        (df_ratings['User-ID'] == user_id) &
        (df_ratings['ISBN'] == book_encoded_to_book.get(book_id))
    ].empty
    else 0  # Atau nilai default sesuai kebutuhan Anda
    for book_id in recommended_book_ids
])

# Pastikan panjang true_ratings dan predicted_ratings sama
min_len = min(len(true_ratings), len(predicted_ratings))
true_ratings = true_ratings[:min_len]
predicted_ratings = predicted_ratings[:min_len]

# Hitung RMSE
rmse = np.sqrt(mean_squared_error(true_ratings, predicted_ratings))

print(f'RMSE: {rmse}')

