# 🏔️ Nomadly Backend

[![Django](https://img.shields.io/badge/Django-6.0-092e20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16-a30000?style=for-the-badge&logo=django)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/JWT-Authentication-black?style=for-the-badge&logo=json-web-tokens)](https://jwt.io/)

Nomadly is a robust backend API for property management and real estate platforms. Built with **Django 6.0** and **Django REST Framework**, it provides a scalable, secure, and feature-rich foundation for handling property listings, user roles, and media management.

## ✨ Features

-   **🏠 Property Management**: Detailed APIs for properties, amenities, features, and locations.
-   **🔐 Advanced Authentication**: Custom user model with JWT-based authentication (SimpleJWT).
-   **🛡️ Role-Based Access Control (RBAC)**: Comprehensive system for managing permissions and groups.
-   **☁️ Media Management**: Seamless integration with **Cloudinary** for cloud-based image and file storage.
-   **📖 API Documentation**: Auto-generated interactive documentation using **Swagger UI** and **ReDoc**.
-   **🚀 Performance**: Built-in throttling, pagination, and health check endpoints.
-   **🐳 Docker Ready**: Simplified deployment and development environment using Docker.

## 🛠️ Tech Stack

-   **Framework**: [Django 6.0](https://www.djangoproject.com/) & [Django REST Framework](https://www.django-rest-framework.org/)
-   **Database**: [PostgreSQL](https://www.postgresql.org/)
-   **Authentication**: [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)
-   **Image Storage**: [Cloudinary](https://cloudinary.com/)
-   **Documentation**: [drf-spectacular](https://drf-spectacular.readthedocs.io/)
-   **Containerization**: [Docker](https://www.docker.com/)

## 🚀 Getting Started

### Prerequisites

-   Python 3.10+
-   PostgreSQL
-   Cloudinary Account (optional, for media)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/hossainchisty/Nomadly-Backend.git
    cd Nomadly-Backend
    ```

2.  **Set up Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Setup**:
    Create a `.env` file in the root directory and add the following:
    ```env
    SECRET_KEY=your_django_secret_key
    DEBUG=True
    DATABASE_URL=postgres://user:password@localhost:5432/nomadly
    CLOUD_NAME=your_cloudinary_name
    API_KEY=your_cloudinary_api_key
    API_SECRET=your_cloudinary_api_secret
    ```

5.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

6.  **Start Development Server**:
    ```bash
    python manage.py runserver
    ```

## 📂 API Documentation

The API comes with interactive documentation accessible at:

-   **Swagger UI**: `http://localhost:8000/swagger/`
-   **ReDoc**: `http://localhost:8000/redoc/`
-   **API Schema**: `http://localhost:8000/schema/`

## 🐳 Docker Deployment

To run the project using Docker:

```bash
docker build -t nomadly-backend .
docker run -p 8000:8000 nomadly-backend
```

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

Built with ❤️ by [Hossain Chisty](https://github.com/hossainchisty)
