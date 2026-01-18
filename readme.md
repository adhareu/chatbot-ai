# 🚀 AI Chatbot SaaS Backend (FastAPI + Redis + JWT + Docker)

A **production-ready AI chatbot backend** built with **FastAPI**, designed as a **SaaS-style API** with authentication, usage limits, analytics, and Dockerized infrastructure.

This project demonstrates how to build and operate a **monetizable AI API** similar to real-world AI platforms.

---

## ✨ Features

### 🔐 Authentication & Security
- API Key–based client onboarding
- JWT authentication (Bearer tokens)
- Master Admin Key for admin operations
- Secure environment-based configuration

### 🧠 AI Chatbot
- Chat endpoint with session-based memory
- Redis-backed chat history
- Clean service-layer architecture
- Easy to replace OpenAI with any LLM provider

### 📊 Usage Control & Monetization
- Plan-based pricing:
  - **Free** → 50 requests/day
  - **Pro** → 1000 requests/day
  - **Enterprise** → Unlimited
- Per-client daily quota enforcement
- Rate limiting (API abuse protection)

### 📈 Usage Analytics
- Total requests per client
- Per-endpoint usage
- Hourly request tracking
- Last activity timestamp
- Admin analytics APIs

### 🐳 Infrastructure
- Fully Dockerized (FastAPI + Redis)
- docker-compose for local & cloud-ready deployment
- Stateless API design (scales horizontally)

---

## 🏗️ Architecture Overview

