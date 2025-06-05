# VaxPlus - REST API for a Vaccination Management System

![Django](https://img.shields.io/badge/Django-5.2.1-green)
![DRF](https://img.shields.io/badge/DRF-3.16.0-red)
![JWT](https://img.shields.io/badge/JWT_Authentication-5.5.0-yellow)

VaxPlus is a secure and scalable RESTful API built using Django and Django REST Framework. This system allows users to register, book vaccination slots, view vaccine details, and manage appointments efficiently. It also includes admin-level capabilities to manage vaccine centers, doses, and more.

---

## 🌐 Live Deployment

- 🔗 **Base URL** – *Coming Soon*
- 🔗 **API Root** – *Coming Soon*

---

## 🚀 Key Features

- **JWT Authentication** – Secure, token-based login and access management  
- **Email Activation** – Automatic account activation via email upon registration  
- **User Management** – Register, log in, and manage user profiles  
- **Campaign Management** – Full CRUD operations for vaccination campaigns  
- **Vaccination Centers** – Create, update, and manage vaccine center details  
- **Booking System** – Book, reschedule, or cancel vaccination appointments  
- **Admin Panel** – Manage users, vaccine info, and appointment data 
- **Advanced Filters** – Filter campaigns by category, date, status, and more  
- **Search & Ordering** – Search by campaign or vaccine title and description; order by date or relevance  
- **API Documentation** – Integrated Swagger and ReDoc for easy API exploration  

---

## 🛠️ Technologies Used

- **Backend**: Django 5.2.1
- **REST Framework**: DRF 3.16.0
- **Authentication**: JWT (SimpleJWT), Djoser
- **Docs**: drf-yasg (Swagger/ReDoc)
- **Database**: SQLite (development)
- **Image Handling**: Pillow
- **Filtering**: django-filter
- **Dependencies**: See [requirements.txt](requirements.txt)

---

## 📚 API Documentation

- 🔍 **Swagger UI** – `/swagger/`
- 📘 **ReDoc UI** – `/redoc/`

---

## 🔧 Installation & Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/anis191/vaxplus-backend.git
    cd vaxplus-backend
   ```
2. **Create & activate virtual environment**
   ```bash
   python -m venv .example_env
   # For Windows
   source .example_env/Scripts/activate
   # For macOS/Linux
   source .example_env/bin/activate
    ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run migrations**
   ```bash
   python manage.py migrate
   ```
5. **Start development server**
   ```bash
   python manage.py runserver
   ```
* API Access:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/) *(Localhost only)*

## 🔐 Authentication

This API uses **JWT (JSON Web Tokens)** for secure, stateless user authentication.

### 📌 Endpoints  
**Base URL:** `http://127.0.0.1:8000/api/v1` *(Localhost only)*

### 🔑 Endpoints

| Method | Endpoint                  | Description                        |
|--------|---------------------------|------------------------------------|
| POST   | `/auth/jwt/create/`       | Login – Obtain access & refresh tokens |
| POST   | `/auth/jwt/refresh/`      | Refresh access token               |
| POST   | `/auth/users/`            | **Register a new user (Sign up)** ✅ |

> 💡 **Note:** After registration, use the [`/auth/jwt/create/`](http://127.0.0.1:8000/api/v1/auth/jwt/create/) endpoint to log in and receive your **JWT tokens**.

## 📂 Project Structure

`vaxplus-backend/`  
&emsp;├── `vaxplus/` – Django settings & core configs  
&emsp;│&emsp;├── `__init__.py`  
&emsp;│&emsp;├── `settings.py`  
&emsp;│&emsp;├── `urls.py`  
&emsp;│&emsp;└── `wsgi.py`  
&emsp;│  
&emsp;├── `api/` – Manage all core APIs  
&emsp;│&emsp;├── `views.py`  
&emsp;│&emsp;├── `urls.py` – All API endpoints  
&emsp;│&emsp;└── `models.py`  
&emsp;│  
&emsp;├── `bookings/` – Slot booking logic  
&emsp;│&emsp;└── *(models, views, serializers)*  
&emsp;│  
&emsp;├── `campaigns/` – Manage all campaigns related logic  
&emsp;│&emsp;└── *(models, views, serializers)*  
&emsp;│  
&emsp;├── `fixtures/` – Demo/sample data for the project  
&emsp;│&emsp;└── `campaigns_data.json` *(project demo data)*  
&emsp;│  
&emsp;├── `media/` – Uploaded images or files  
&emsp;│  
&emsp;├── `users/` – Custom user logic, registration, user profiles  
&emsp;│&emsp;└── *(models, views, serializers, urls)*  
&emsp;│  
&emsp;├── `requirements.txt` – Project dependencies  
&emsp;├── `manage.py` – Django management script  
&emsp;└── `README.md` – Project documentation  

## 🤝 Contributing

Contributions help make this project better and are always welcome!

### How to Contribute

- ⭐ Star the repo  
- 🍴 Fork the project  
- 📥 Clone your fork  
- 💡 Create a feature branch: `git checkout -b feature/awesome-feature`  
- ✅ Commit your changes: `git commit -m 'Add some feature'`  
- 📤 Push your branch: `git push origin feature/awesome-feature`  
- 🛠️ Open a Pull Request

Ensure your code follows the project standards and passes all tests.

## 💻 Author

[**Anisul Alam**](https://github.com/anis191)  
Backend Developer | Django & REST APIs  
[🔗 LinkedIn](https://www.linkedin.com/in/anisul-alam-a330042a9/)

---

