# 🚀 AI Chatbot SaaS Backend  
**FastAPI • Redis • JWT • Docker • Usage Quotas • Analytics**

A **production-ready AI chatbot backend** built with **FastAPI**, designed as a **SaaS-style API** with authentication, pricing plans, usage limits, analytics, and Dockerized infrastructure.

This project is intentionally built like a **real commercial AI API**, not a demo toy.

---

## ✨ Key Features

### 🔐 Authentication & Authorization
- API Key–based client onboarding
- JWT (Bearer token) authentication
- Master Admin Key for admin-only operations
- Secure environment-variable configuration

### 🤖 AI Chatbot
- Chat endpoint with session-based memory
- Redis-backed conversation history
- Clean service-layer architecture
- LLM provider–agnostic (OpenAI-compatible, easily replaceable)

### 💳 Pricing & Usage Control
Built-in SaaS pricing tiers:

| Plan        | Daily Requests |
|------------|----------------|
| Free       | 50             |
| Pro        | 1000           |
| Enterprise | Unlimited      |

- Per-client daily quota enforcement
- Instant plan upgrades/downgrades
- Rate limiting for abuse protection

### 📊 Usage Analytics (Per Client)
- Total requests per client
- Per-endpoint usage tracking
- Hourly usage statistics
- Last activity timestamp
- Admin-only analytics APIs

### 🐳 Infrastructure
- Fully Dockerized backend
- Redis for fast, scalable state management
- Stateless API (horizontal scaling ready)
- Cloud-deployment ready (Railway / Azure / AWS)

---

## 🛠️ Tech Stack
- Backend: FastAPI (Python 3.12)
- Auth: JWT
- Storage: Redis
- Container: Docker

---

## 👨‍💻 Author
**Asif Iqbal**
