# RAG App

A full-stack application with a Retrieval-Augmented Generation (RAG) service, backend API, and frontend UI, deployed using Docker and managed behind NGINX.

---

## 🚀 Tech Stack

* **Frontend:** React + Vite + TypeScript
* **Backend:** Node.js (Express)
* **RAG Service:** Python
* **Reverse Proxy:** NGINX
* **Containerization:** Docker & Docker Compose

---

## 📁 Project Structure

```
rag-app/
├── backend/        # Node.js API
├── frontend/       # React frontend
├── rag/            # Python RAG service
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Prerequisites

* Docker
* Docker Compose
* NGINX (installed on server or containerized)

---

## 🌐 Architecture

```
Client (Browser)
       ↓
     NGINX
       ↓
 ┌───────────────┬───────────────┬───────────────┐
 │   Frontend    │    Backend    │   RAG Service │
 │  (React App)  │ (Node.js API) │   (Python)    │
 └───────────────┴───────────────┴───────────────┘
```

---

## ▶️ How to Run

### 1. Clone the repository

```
git clone https://github.com/pramodGit/rag-app.git
cd rag-app
```

---

### 2. Start services

```
docker-compose up --build -d
```

---

### 3. Access the application

Access via your domain or server IP configured in NGINX:

```
http://your-domain.com
```

---

## 🔧 NGINX Configuration (Example)

```
server {
    listen 80;

    location / {
        proxy_pass http://frontend:3001;
    }

    location /api/ {
        proxy_pass http://backend:5001;
    }

    location /rag/ {
        proxy_pass http://rag:8001;
    }
}
```

*(Adjust based on your actual service names and ports in docker-compose)*

---

## 🔧 Environment Variables

Create a `.env` file if needed:

```
ENV_VAR_NAME=value
```

---

## 📦 Useful Commands

### View running containers

```
docker ps
```

### Stop services

```
docker-compose down
```

### Rebuild services

```
docker-compose up --build
```

---

## 📌 Notes

* NGINX acts as a reverse proxy for all services
* Services communicate internally via Docker network
* Only NGINX is exposed publicly

---

## 👤 Author

**pramodGit**

---

## 📄 License

MIT License
