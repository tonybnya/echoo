# Echoo

Real-time chat application built with Vue 3 and Django.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Vue 3, TypeScript, Vite, Pinia, Tailwind CSS |
| Backend | Django 5.2, Django REST Framework, Django Channels |
| Database | PostgreSQL (Neon) |
| Real-time | WebSockets via channels_redis |
| Auth | Djoser + SimpleJWT |

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ECHOO APP ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────────────────┘

                                    ┌─────────────────┐
                                    │   PostgreSQL    │
                                    │    (Neon DB)    │
                                    └────────┬────────┘
                                             │
                                             ▼
┌─────────────────┐     ┌─────────────────┐     │
│   Vue 3 SPA     │────▶│  Django REST   │◀────┘
│   (Frontend)    │     │  API + Channels│
└────────┬────────┘     └────────┬────────┘
         │                       │
         │               ┌───────┴───────┐
         │               │               │
         │               ▼               ▼
         │        ┌──────────┐    ┌──────────┐
         │        │  Redis   │    │  RabbitMQ│
         │        │ (Upstash)│    │ (unused) │
         │        └──────────┘    └──────────┘
         │               │
         │               ▼
         │        ┌──────────────┐
         │        │   WebSocket │
         │        │   (Channels)│
         │        └──────────────┘
         ▼
    End Users
```

## Features

- Real-time messaging via WebSockets
- User authentication (JWT)
- Create/join chat sessions
- Share session links to invite friends

## Quick Start

### Backend

```bash
cd backend
cp .env.example .env  # Configure DATABASE_URL and REDIS_URL
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chats/` | Create chat session |
| PATCH | `/api/chats/<uri>/` | Join session |
| GET | `/api/chats/<uri>/messages/` | Get messages |
| WebSocket | `/ws/chats/<uri>/` | Real-time messaging |

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://...
REDIS_URL=rediss://...
SECRET_KEY=...
DEBUG=True
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```
