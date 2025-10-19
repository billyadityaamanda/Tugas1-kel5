# JWT Marketplace API

Proyek ini adalah implementasi sederhana REST API dengan autentikasi JWT untuk tugas mata kuliah **Integrasi Aplikasi & Enterprise**.

---

## Cara Setup Environment & Menjalankan Server

### 1️⃣ Masuk ke folder proyek
```bash
cd jwt_marketplace
````

### 2️⃣ Aktifkan Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependensi

```bash
pip install -r requirements.txt
```

### 4️⃣ Jalankan server

```bash
python app.py
```

Server akan berjalan di:

* [http://127.0.0.1:5000](http://127.0.0.1:5000)
* [http://192.168.x.x:5000](http://192.168.x.x:5000) (jika diakses lewat jaringan lokal)

---

## ⚙️ Variabel ENV yang Diperlukan

Buat file `.env` berdasarkan contoh `.env.example`:

```
SECRET_KEY=your_secret_key_here
USER_EMAIL=user1@example.com
USER_PASSWORD=pass123
```

## 📡 Daftar Endpoint + Skema Request/Response

| Endpoint      | Method | Deskripsi                          | Auth  |
| ------------- | ------ | ---------------------------------- | ----- |
| `/auth/login` | POST   | Login dan mendapatkan JWT token    | ❌     |
| `/items`      | GET    | Menampilkan daftar barang (publik) | ❌     |
| `/profile`    | PUT    | Mengubah data profil user          | ✅ JWT |

### 🔸 Contoh Request & Response

#### 1. POST `/auth/login`

**Request Body:**

```json
{
  "email": "user1@example.com",
  "password": "pass123"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5..."
}
```

#### 2. GET `/items`

**Response:**

```json
{
  "items": [
    {"id": 1, "name": "Laptop", "price": 12000000},
    {"id": 2, "name": "Mouse", "price": 250000},
    {"id": 3, "name": "Keyboard", "price": 500000}
  ]
}
```

#### 3. PUT `/profile`

**Header:**

```
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "name": "Nama Baru"
}
```

**Response:**

```json
{
  "message": "Profile updated successfully"
}
```

## 🧪 Contoh cURL / Postman

### cURL (contoh login)

```bash
curl -X POST http://127.0.0.1:5000/auth/login \
-H "Content-Type: application/json" \
-d "{\"email\": \"user1@example.com\", \"password\": \"pass123\"}"
```

### Postman

Koleksi Postman dapat ditemukan pada file:

```
JWT_Marketplace_Collection.json
```

---

## ⚠️ Catatan Kendala / Asumsi

* Token JWT berlaku selama 15 menit.
* Endpoint `/profile` hanya dapat diakses menggunakan token valid.
* Server Flask berjalan di mode development untuk pengujian lokal.

---

📁 **Struktur Folder**

```
jwt_marketplace/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── templates/
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── venv/
└── JWT_Marketplace_Collection.json
```

---

✅ **Dibuat oleh: kelompok 5
                  -Aulia indah nuriaji 102022300187
                  -Aura Haya Azka      102022300104
                  -Billy Aditya Amanda 102022300252
                  -Noviardha Fitri Yuldhari 102022300274
                  -M.Fariz Eka Putra   102022300300
🧩 **Mata Kuliah:** Integrasi Aplikasi & Enterprise
📅 **Tanggal:** 18 Oktober 2025


