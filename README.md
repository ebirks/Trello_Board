# 📋 Trello Clone — Full-Stack Project

A collaborative task management board system built with **Django REST Framework** and **React**, featuring user authentication, role-based access control (RBAC), and a nested board/column/card hierarchy.

> A portfolio project demonstrating full-stack development skills: relational database design, secure REST API architecture, JWT authentication, and modern frontend integration.

---

## 📑 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Authentication & RBAC](#authentication--rbac)
- [Database Schema](#database-schema)
- [Frontend](#frontend)
- [Roadmap](#roadmap)
- [Lessons Learned](#lessons-learned)
- [License](#license)

---

## 🎯 Overview

This project is a **Trello-style Kanban board** application where users can organize tasks into boards, columns, and cards. It was built as a learning exercise to demonstrate a full understanding of how systems interact across the stack — from the database layer up to the user interface.

The application currently supports:
- 🔐 Secure JWT-based user authentication
- 👥 Role-based access control (Admin / Editor / Viewer)
- 🗂️ Nested CRUD operations for Boards → Columns → Cards
- 🎨 A responsive React frontend with real-time UI updates
- 🔒 Data isolation — users only see boards they own or are invited to

---

## ✨ Features

### Backend
- **User Authentication** using JSON Web Tokens (JWT)
- **Role-Based Access Control** with three roles:
  - `Admin` — Full control (delete board, manage members)
  - `Editor` — Can create/edit columns and cards
  - `Viewer` — Read-only access to the board
- **Data Isolation** — Boards are scoped to their owner and explicitly invited members
- **Nested CRUD** — Full create/read/update/delete for Boards, Columns, and Cards
- **Cascade Deletion** — Deleting a board removes its columns; deleting a column removes its cards
- **Automatic Ownership** — New boards are auto-assigned to the authenticated user via `perform_create`

### Frontend
- **Login System** with token persistence via `localStorage`
- **Dashboard View** listing all boards the user owns or belongs to
- **Board Detail View** with horizontally arranged columns and cards
- **Inline Forms** for creating new boards, columns, and cards
- **Delete Buttons** with confirmation-free instant removal
- **Axios Interceptor Pattern** — Bearer token is attached to every API request

---

## 🛠️ Tech Stack

| Layer          | Technology                          | Purpose                                              |
|----------------|-------------------------------------|------------------------------------------------------|
| **Frontend**   | React 18 + Vite                     | Component-based UI with hot-module reloading         |
| **HTTP Client**| Axios                               | Promise-based HTTP requests with token management    |
| **Backend**    | Django 6.0                          | Web framework handling routing and security          |
| **API Layer**  | Django REST Framework (DRF)         | Translates Python objects to JSON and auto-generates CRUD endpoints |
| **Auth**       | djangorestframework-simplejwt       | Issues and validates JWT access/refresh tokens       |
| **CORS**       | django-cors-headers                 | Allows the React dev server to communicate with Django |
| **Database**   | SQLite (dev) / PostgreSQL (prod)    | Relational storage for boards, columns, cards, users |
| **ORM**        | Django ORM                          | Translates Python classes into database tables       |

---

## 🏗️ Architecture

The application follows a classic **three-tier architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                    REACT FRONTEND                            │
│  (Vite dev server on localhost:5173)                        │
│                                                              │
│  App.jsx ───┬─── Login Form                                  │
│             └─── Dashboard (list of boards)                  │
│                  └─── BoardDetail.jsx                        │
│                       ├── Columns (horizontal flex)          │
│                       │    └── Cards                         │
│                       └── Add Column / Add Card forms       │
└────────────────────────┬────────────────────────────────────┘
                         │  HTTP requests (Bearer JWT in headers)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  DJANGO REST API                             │
│  (Django server on localhost:8000)                          │
│                                                              │
│  /api/token/         → Login (returns JWT)                  │
│  /api/token/refresh/  → Refresh expired token                │
│  /api/boards/         → BoardViewSet (CRUD + RBAC)          │
│  /api/columns/        → ColumnViewSet                        │
│  /api/cards/          → CardViewSet                          │
│                                                              │
│  Middleware:                                                 │
│   ├── CORS (allow React origin)                             │
│   ├── JWTAuthentication (decode token)                      │
│   └── IsBoardMemberOrReadOnly (RBAC enforcement)            │
└────────────────────────┬────────────────────────────────────┘
                         │  ORM translates Python → SQL
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE (SQLite)                         │
│                                                              │
│  User ──┐                                                    │
│         ├── Board (owner_id FK)                             │
│         │    ├── Column (board_id FK)                        │
│         │    │    └── Card (column_id FK)                   │
│         │    └── BoardMembership (board_id, user_id, role)  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
trello-clone/
├── backend/                     # Django project package
│   ├── settings.py              # DRF + JWT + CORS configuration
│   ├── urls.py                   # Root URL conf (includes JWT + core URLs)
│   └── wsgi.py / asgi.py
├── core/                        # Main application
│   ├── models.py                # Board, Column, Card, BoardMembership
│   ├── serializers.py           # DRF ModelSerializers (Python ↔ JSON)
│   ├── views.py                 # ModelViewSets + perform_create + get_queryset
│   ├── permissions.py           # Custom IsBoardMemberOrReadOnly permission
│   ├── admin.py                 # Admin panel registrations
│   ├── urls.py                  # DRF DefaultRouter for CRUD endpoints
│   └── migrations/              # Database migration history
├── frontend/                    # React + Vite frontend
│   └── src/
│       ├── App.jsx              # Login + Dashboard view
│       └── BoardDetail.jsx      # Nested board/column/card UI
├── manage.py                    # Django CLI entrypoint
├── db.sqlite3                   # SQLite database file (dev only)
├── requirements.txt             # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** (developed on Python 3.13)
- **Node.js 18+** and npm
- A virtual environment tool (`venv`)

### Backend Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2. Install Python dependencies
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers

# 3. Create the Django project (if not already created)
django-admin startproject backend .

# 4. Create the core app
python manage.py startapp core

# 5. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create an admin superuser
python manage.py createsuperuser

# 7. Start the backend server
python manage.py runserver
```

The Django API will be available at `http://127.0.0.1:8000/`.

### Frontend Setup

```bash
# 1. Scaffold the React app with Vite
npm create vite@latest frontend -- --template react

# 2. Move into the frontend folder
cd frontend

# 3. Install Node dependencies
npm install

# 4. Install Axios for HTTP requests
npm install axios

# 5. Start the dev server
npm run dev
```

The React app will be available at `http://localhost:5173/`.

### Run Both Simultaneously

Open two terminal windows:
- **Terminal 1 (Backend):** `python manage.py runserver` (from project root)
- **Terminal 2 (Frontend):** `npm run dev` (from `frontend/` folder)

---

## 🌐 API Endpoints

### Authentication

| Method | Endpoint              | Description                       | Auth Required |
|--------|-----------------------|-----------------------------------|---------------|
| POST   | `/api/token/`         | Login with username/password      | ❌             |
| POST   | `/api/token/refresh/` | Refresh an expired access token   | ✅ (refresh)   |

### Boards

| Method  | Endpoint              | Description                       | Permissions                       |
|---------|-----------------------|-----------------------------------|----------------------------------|
| GET     | `/api/boards/`        | List boards owned by or shared with the user | Authenticated         |
| POST    | `/api/boards/`        | Create a new board (auto-assigned to user)  | Authenticated         |
| GET     | `/api/boards/<id>/`   | Retrieve a specific board         | Owner or Member                  |
| PATCH   | `/api/boards/<id>/`   | Update board title/description    | Owner, Admin, or Editor          |
| DELETE  | `/api/boards/<id>/`   | Delete a board (cascades to columns/cards) | Owner only            |

### Columns

| Method  | Endpoint              | Description                       | Permissions                       |
|---------|-----------------------|-----------------------------------|----------------------------------|
| GET     | `/api/columns/`       | List columns for the user's boards | Authenticated                    |
| POST    | `/api/columns/`       | Create a column in a board        | Authenticated (board owner/member)|
| PATCH   | `/api/columns/<id>/`  | Update column title/position      | Owner, Admin, or Editor           |
| DELETE  | `/api/columns/<id>/`  | Delete column (cascades to cards) | Owner, Admin, or Editor           |

### Cards

| Method  | Endpoint              | Description                       | Permissions                       |
|---------|-----------------------|-----------------------------------|----------------------------------|
| GET     | `/api/cards/`         | List cards for the user's boards | Authenticated                     |
| POST    | `/api/cards/`         | Create a card in a column         | Authenticated                     |
| PATCH   | `/api/cards/<id>/`    | Update card title/description     | Owner, Admin, or Editor           |
| DELETE  | `/api/cards/<id>/`    | Delete a card                    | Owner, Admin, or Editor           |

### Request/Response Examples

**Login Request:**
```http
POST /api/token/
Content-Type: application/json

{
    "username": "johndoe",
    "password": "secretpassword"
}
```

**Login Response:**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Create Board Request:**
```http
POST /api/boards/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "My Sprint Board",
    "description": "Tasks for this sprint"
}
```

---

## 🔐 Authentication & RBAC

### JWT Token Flow

1. The user submits credentials to `/api/token/`.
2. Django verifies the password and returns an **access token** (short-lived, ~5 minutes) and a **refresh token** (longer-lived).
3. The frontend stores the access token in `localStorage` and attaches it to every Axios request as `Authorization: Bearer <token>`.
4. When the access token expires, the frontend can use the refresh token to obtain a new one without forcing the user to log in again.

### Role-Based Access Control

The `BoardMembership` model links a User to a Board with one of three roles:

| Role    | Can View | Can Edit Columns/Cards | Can Delete Board | Can Manage Members |
|---------|----------|------------------------|------------------|---------------------|
| Viewer  | ✅       | ❌                      | ❌                | ❌                   |
| Editor  | ✅       | ✅                      | ❌                | ❌                   |
| Admin   | ✅       | ✅                      | ❌ (owner only)   | ✅                   |
| Owner   | ✅       | ✅                      | ✅                | ✅                   |

This logic is enforced in `core/permissions.py` via the custom `IsBoardMemberOrReadOnly` permission class, which runs *before* the view executes.

### Data Isolation

The `get_queryset` method in each ViewSet restricts the database query so that:
- Users only see boards they **own** OR boards they have a `BoardMembership` for.
- Columns and Cards are scoped to boards owned by the requesting user.

This prevents User A from ever accidentally retrieving User B's data via the API.

---

## 🗄️ Database Schema

### Entities

**User** (Django built-in `auth_user`)
- `id`, `username`, `password` (hashed), `email`

**Board**
- `id` (PK)
- `title` (CharField, max 100)
- `description` (TextField, optional)
- `owner` (FK → User, `on_delete=CASCADE`)

**Column**
- `id` (PK)
- `title` (CharField, max 100)
- `position` (Integer, default 0)
- `board` (FK → Board, `on_delete=CASCADE`)

**Card**
- `id` (PK)
- `title` (CharField, max 255)
- `description` (TextField, optional)
- `position` (Integer, default 0)
- `column` (FK → Column, `on_delete=CASCADE`)

**BoardMembership**
- `id` (PK)
- `board` (FK → Board, `on_delete=CASCADE`)
- `user` (FK → User, `on_delete=CASCADE`)
- `role` (CharField, choices: admin/editor/viewer, default viewer)
- **Unique constraint**: `(board, user)` — prevents duplicate memberships

### Relationships

```
User 1 ──── ∞ Board (owner)
User 1 ──── ∞ BoardMembership
Board 1 ──── ∞ Column
Board 1 ──── ∞ BoardMembership
Column 1 ──── ∞ Card
```

---

## 💻 Frontend

### Component Tree

```
App.jsx
├── (if not logged in) → Login Form
└── (if logged in) → Dashboard
    ├── Logout button
    ├── Create Board form
    ├── List of Boards (clickable)
    └── BoardDetail.jsx (when a board is selected)
        ├── Back to Boards button
        ├── List of Columns (horizontal flex)
        │   ├── Column header + Delete button
        │   ├── List of Cards + Delete buttons
        │   └── Add Card form
        └── Add Column form
```

### State Management

The app uses React's `useState` and `useEffect` hooks:

- **`token`** — Stores the JWT; persisted to `localStorage`
- **`boards` / `columns` / `cards`** — Lists fetched from the API
- **`cardInputs`** — An object mapping `{ [columnId]: "card title" }` to track multiple input fields
- **`useEffect`** — Re-fetches data when the token or `boardId` changes

### Axios Pattern

Instead of attaching the token manually to every request, the app uses an interceptor pattern in `useEffect`:

```javascript
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
```

This ensures every Axios call automatically includes the JWT, mimicking how production apps handle session management.

---

## 🗺️ Roadmap

This project is being built in phases. Here's where we are:

- [x] **Phase 1: Backend CRUD** — REST API with nested Board/Column/Card endpoints
- [x] **Phase 2: Auth & RBAC** — JWT authentication, user isolation, role-based permissions
- [x] **Phase 3: Frontend** — React dashboard, board detail view, create/delete UI
- [ ] **Phase 4: Real-time Collaboration** — WebSockets via Django Channels for live multi-user syncing
- [ ] **Phase 5: Third-Party API** — SendGrid email notifications when mentioned in cards
- [ ] **Phase 6: Unit Testing** — Pytest suite covering auth, RBAC, and CRUD operations
- [ ] **Phase 7: Production Deployment** — Migrate to PostgreSQL, deploy to a cloud provider

---

## 📚 Lessons Learned

### Why Django + DRF?
Django's "batteries-included" philosophy gave us authentication, an admin panel, and a powerful ORM out of the box. DRF's `ModelViewSet` auto-generated all five CRUD endpoints with three lines of code, saving hours of boilerplate.

### Why JWT instead of Sessions?
Sessions require the server to maintain state for each logged-in user, which makes horizontal scaling (adding more servers) difficult. JWT is **stateless** — the token contains everything needed to verify the user, so any server can validate it without checking a central store.

### Why a Custom Permission Class?
DRF's built-in `IsAuthenticated` only checks "is this person logged in?". Our Trello rules are richer: "only Admins/Editors can edit, Viewers can only look, and only the Owner can delete." The `IsBoardMemberOrReadOnly` class encapsulates this logic in one reusable place.

### Why `get_queryset` instead of `queryset`?
Setting `queryset = Board.objects.all()` would expose every board in the database to every user. Overriding `get_queryset` lets us filter dynamically based on `self.request.user`, enforcing data isolation at the database query level — far more secure than filtering on the frontend.

### Why Vite instead of Create React App?
Vite starts in milliseconds (vs. minutes for CRA), supports hot-module reloading natively, and produces smaller production bundles. CRA is also officially deprecated by the React team.

---

## 📄 License

This project is licensed under the MIT License — feel free to use it as a reference, learning resource, or starting point for your own projects.

---

**Built as a portfolio project to demonstrate full-stack development with Python (Django) and React.**
