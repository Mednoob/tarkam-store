# Tarkam Store
Tautan Deployment: 

## Soal 1
Langkah-langkah yang saya lakukan adalah sebagai berikut

### Checklist 1: Membuat sebuah proyek Django baru.
1. Membuat virtual environment untuk Python terlebih dahulu: `python -m venv env`
2. Mengaktifkan virtual env yang sudah dibuat: `env/Scripts/activate`
3. Membuat file `requirements.txt` yang kemudian diisi dengan dependensi yang diperlukan:
    ```
    django
    gunicorn
    whitenoise
    psycopg2-binary
    requests
    urllib3
    python-dotenv
    ```
4. Menginstall dependensi yang sudah ditulis: `pip install -r requirements.txt`
5. Membuat projek Django baru di folder ini: `django-admin startproject tarkam_store .`
6. Membuat file `.env` yang tiap-tiap key valuenya akan diload oleh program sebagai env variables:
    ```
    PRODUCTION=False
    ```
    Di sini di set `Production=False` karena ketika dijalankan di local, program dalam tahap pengembangan (belum masuk ke tahap production)
7. Membuat file `.env.prod` untuk mencatat env variables yang akan digunakan pada production:
    ```
    DB_NAME=<nama database>
    DB_HOST=<host database>
    DB_PORT=<port database>
    DB_USER=<username database>
    DB_PASSWORD=<password database>
    SCHEMA=tugas_individu
    PRODUCTION=True
    ```
8. Setelah itu, dilakukan set up pada file `tarkam_store/settings.py` sebagai berikut:
    - Me-load env variables yang ada di file `.env`:
        ```python
        import os
        from dotenv import load_dotenv
        # Load environment variables from .env file
        load_dotenv()

        ...
        ```
    - Menambahkan variabel `ALLOWED_HOSTS` dengan value sebagai berikut:
        ```python
        ...
        ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
        ...
        ```
        Line ini berfungsi untuk memberitahu django bahwa web hanya akan bisa diakses melalui alamat-alamat tersebut.
    - Menambahkan variabel `PRODUCTION` dengan value sebagai berikut:
        ```python
        PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'
        ```
        `PRODUCTION` berfungsi sebagai indikator apakah kita sedang berada di lingkungan production atau tidak. Variabel ini akan mengambil informasi berdasarkan apa yang sudah ditulis pada env variable sebelumnya.
    - Mengubah pengaturan `DATABASES` menjadi:
        ```python
        if PRODUCTION:
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': os.getenv('DB_NAME'),
                    'USER': os.getenv('DB_USER'),
                    'PASSWORD': os.getenv('DB_PASSWORD'),
                    'HOST': os.getenv('DB_HOST'),
                    'PORT': os.getenv('DB_PORT'),
                    'OPTIONS': {
                        'options': f"-c search_path={os.getenv('SCHEMA', 'public')}"
                    }
                }
            }
        else:
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR / 'db.sqlite3',
                }
            }
        ```
        Di sini, kita sesuaikan database yang akan digunakan untuk menyimpan data sesuai dengan apakah kita sedang di tahap production atau bukan. Apabila sudah diproduction, maka kita menggunakan database PostgreSQL dengan variabel-variabel yang sudah kita tulis di `.env.prod` sebelumnya. Namun apabila tidak, maka kita menggunakan database yang lebih simpel yaitu SQLite.

### Checklist 2: Membuat aplikasi dengan nama `main` pada proyek tersebut.
1. Membuat aplikasi dengan nama `main`: `python manage.py startapp main`

### Checklist 3: Melakukan _routing_ pada proyek agar dapat menjalankan aplikasi `main`.
1. Membuat folder `templates` di folder `main`
2. Membuat file `main.html` di folder `templates` yang berada di dalam `main`
    Isi dari `main.html`:
    ```html
    <h1>Halo!</h1>
    ```
3. Mengubah isi file `views.py` yang ada di folder `main` menjadi:
    ```python
    from django.shortcuts import render

    def show_main(request):
        context = {}

        return render(request, "main.html", context)
    ```
4. Membuat file `urls.py` di dalam folder `main`.
    Isi file `urls.py`:
    ```python
    from django.urls import path
    from main.views import show_main

    app_name = 'main'

    urlpatterns = [
        path('', show_main, name='show_main'),
    ]
    ```

5. Mengubah isi file `urls.py` yang ada di direktori proyek (`tarkam_store`) menjadi:
    ```python
    from django.contrib import admin
    from django.urls import path, include
    from django.views.generic.base import RedirectView

    urlpatterns = [
        path('admin/', admin.site.urls),
        path("store/", include("main.urls")),
        path("", RedirectView.as_view(url="/store/", permanent=True))
    ]
    ```

    Di sini dibuat agar ketika user mengakses `<url>/store`, maka akan memunculkan aplikasi `main`. Lalu apabila user mengakses `<url>/`, user akan diredirect ke `<url>/store/`.

### Checklist 4: Membuat model pada aplikasi `main` dengan nama `Product`
1. Mengubah isi file `models.py` yang ada di direktori `main` menjadi:
    ```python
    import uuid
    from django.db import models

    class Product(models.Model):
        CATEGORIES = [
            ("shoes", "Shoes"),
            ("clothes", "Clothes"),
            ("accessories", "Accessories"),
            ("balls", "Balls"),
            ("other", "Other")
        ]

        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        name = models.CharField(max_length=100)
        price = models.PositiveIntegerField()
        description = models.TextField()
        thumbnail = models.URLField(blank=True, null=True)
        category = models.CharField(max_length=20, choices=CATEGORIES, default="other")
        is_featured = models.BooleanField(default=False)

        def __str__(self):
            return self.name
    ```
2. Membuat migrasi dari model yang baru saja dibuat: `python manage.py makemigrations`
3. Menerapkan migrasi pada database lokal: `python manage.py migrate`

### Checklist 5: Membuat sebuah fungsi pada `views.py` untuk dikembalikan ke dalam sebuah _template_ HTML
1. Mengubah isi file `views.py` yang ada di folder `main` menjadi:
    ```python
    from django.shortcuts import render

    def show_main(request):
        context = {
            "app_name": "Tarkam Store",
            "name": "Ahmad Yaqdhan",
            "class": "PBP A",
            "npm": 2406399081,
            "message": "Coming soon!"
        }

        return render(request, "main.html", context)
    ```
2. Mengubah isi file `main.html` yang ada di folder `main/templates`:
    ```html
    <h1>{{ app_name }}</h1>

    <h4>Nama</h4>
    <p>{{ name }}</p>

    <h4>Kelas</h4>
    <p>{{ class }}</p>

    <h4>NPM</h4>
    <p>{{ npm }}</p>

    <h4>Message:</h4>
    <p>{{ message }}</p>
    ```

### Checklist 6: Membuat sebuah routing pada `urls.py` aplikasi `main` untuk memetakan fungsi yang telah dibuat pada `views.py`.
Tahap ini sudah dilakukan bersamaan dengan checklist 3, dimana kita sudah menambahkan penggunaan fungsi `show_main` pada routing yang berada di file `urls.py`.

### Checklist 7: Melakukan _deployment_ ke PWS
1. Membuat project baru di [PWS](https://pbp.cs.ui.ac.id/), di sini saya menggunakan nama `tarkamstore` untuk projectnya
2. Menambahkan `"<username>-tarkamstore.pbp.cs.ui.ac.id"` ke array `ALLOWED_HOSTS` yang ada di file `settings.py`:
    ```python
    ...
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "ahmad-yaqdhan-tarkamstore.pbp.cs.ui.ac.id"]
    ...
    ```
    Perhatikan bahwa url yang saya tulis di contoh kode atas menyesuaikan dengan username saya yaitu `ahmad.yaqdhan`. Silahkan ubah string url tersebut sesuai dengan username anda. Jangan lupa untuk mengubah simbol titik menjadi strip `-` apabila username anda mengandung titik.
3. Salin kredensial yang ditampilkan ke tempat lain terlebih dahulu
4. Membuka menu `Environs` dan memasukkan env variabel yang sudah ditulis sebelumnya di file `.env.prod` melalui tombol `Raw Editor` yang ada di menu `Environs`.
5. Menjalankan perintah pada konsol / terminal sebagai berikut:
    ```
    git remote add pws "https://pbp.cs.ui.ac.id/ahmad.yaqdhan/tarkamstore.git"
    git branch -M master
    git push pws master
    ```

    Perlu diperhatikan bahwa pada perintah di atas, url git yang saya tulis menyesuaikan dengan username SCELE saya yaitu `ahmad.yaqdhan`.
    Silahkan ganti ke username yang sesuai untuk akun SCELE anda.
6. Ketika perintah yang terakhir dijalankan, seharusnya git menanyakan username dan password. Di sini, masukkan kredensial yang kita salin sebelumnya pada tahap 3.
7. Setelah selesai push, program seharusnya sudah berhasil dideploy.