TUGAS 1 JWT Marketplace API
📌 Deskripsi

Proyek ini merupakan implementasi API sederhana berbasis Flask dengan fitur JWT Authentication, endpoint publik dan proteksi token, serta pengujian menggunakan Postman.
Studi kasus ini meniru sistem marketplace sederhana yang memiliki user login, daftar produk (items), dan update profil user menggunakan JWT.

⚙️ Cara Setup Environment & Menjalankan Server
1. Clone / ekstrak project
```bash
git clone <>
cd TUGAS_1_EAI
```
2. Buat virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # untuk Windows
# atau
source venv/bin/activate  # untuk Linux/Mac
```
3. Install dependency
```bash
pip install -r requirements.txt
```

Menjalankan Server
1. Jalankan python app.py
```bash
export FLASK_APP=app.py
flask run --port 5000
```
EndPoint Penting 
- ` POST http://localhost:5000/auth/login` untuk mendapatkan JWT.
- ` GET https://localhost:5000/items` untuk menampilkan list items
- ` PUT https://localhost:5000/profile` untuk update profile akun

Contoh Alur Penggunaan
1. POST /auth/login

Request Body:
```bash
{
  "email": "user1@example.com",
  "password": "pass123"
}
```
Response 200 (Success):
```bash
{
  "access_token": "<JWT_TOKEN>"
}
```
![WhatsApp Image 2025-10-15 at 20 01 55_d7627b7f](https://github.com/user-attachments/assets/bbda0bb5-4a25-48e6-8bee-5473cedec6b1)

Response 401 (Invalid):
```bash
{
  "error": "Invalid credentials"
}
```
![WhatsApp Image 2025-10-17 at 22 45 40_baa55333](https://github.com/user-attachments/assets/4c81a86b-34d8-4677-8791-5c88a1b902a1)

2. GET /items (Public)
Tidak membutuhkan JWT

Response 200:
```bash
{
    "items": [
        {
            "id": 1,
            "name": "Kopi Hitam",
            "price": 15000
        },
        {
            "id": 2,
            "name": "Teh Tarik",
            "price": 12000
        },
        {
            "id": 3,
            "name": "Es Coklat",
            "price": 18000
        }
    ]
}
```
![WhatsApp Image 2025-10-15 at 20 21 24_b9b59e55](https://github.com/user-attachments/assets/12d18410-8a07-4a4b-97df-04b8c78eed52)

3. PUT /profile

Header:
```bash
Authorization: Bearer <access_token>
```
Request body
```bash
{
  "name": "Nama Baru"
}
```
Response 200
```bash
{
  "message": "Profile updated",
  "profile": {
    "name": "Nama Baru",
    "email": "user1@example.com"
  }
}
```

Response 401 (Tanpa Token / Token Kadaluarsa)
```bash
{
  "error": "Token expired"
}
```
![WhatsApp Image 2025-10-15 at 20 30 34_ad98a01f](https://github.com/user-attachments/assets/e438b0be-ddec-47da-af21-c9fd4944cddb)

4. POST /auth/refresh

Header:
```bash
Authorization: Bearer <access_token> udh basi atau mau baru
```
Respons 200
```bash
{
  "access_token": "<JWT_TOKEN_BARU>"
}
```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a7aba3ab-18d0-40fe-abc2-0d15fd5b6009" />

5. POST /auth/login Admin Only

Header:
```bash
{
  "email": "admin@example.com",
  "password": "adminpass"
}
```
Respons 200
```bash
{
  "access_token": "<JWT_TOKEN>"
}
```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/751036f4-9066-4fdd-b521-ec7e86133f6e" />

6. GET /admin-only

Header:
```bash
Authorization: Bearer <access_token>
```
Respons 200
```bash
{
    "message": "Welcome admin!"
}
```
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/817db180-fc37-47d5-a3b7-3a5e72361d2a" />

Catatan/kendala
Token Expire 15menit (waktu nyata)
