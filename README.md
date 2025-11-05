# 📊 DevMetrics Backend

![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.121.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

> **API Backend para Dashboard de Productividad** - Conecta tu tiempo de trabajo con tu actividad en Git y genera métricas de productividad.

---

## 🌟 ¿Qué es DevMetrics Backend?

**DevMetrics Backend** es una API RESTful construida con FastAPI que rastrea el tiempo de desarrollo, se integra con repositorios Git, y genera métricas detalladas de productividad.

### 💡 El Problema

- ¿Cuánto tiempo realmente dedico a cada proyecto?
- ¿Qué tareas consumen más tiempo del esperado?
- ¿Cómo vincular mi tiempo de trabajo con commits específicos?

### ✨ La Solución

Un backend robusto que:

- ⚡ **API RESTful de alto rendimiento** con FastAPI y asyncio
- 🔐 **Autenticación JWT** para seguridad
- 🐍 **Scripts de integración Git** automáticos
- 📊 **Base de datos PostgreSQL** con consultas SQL avanzadas

---

## 🚀 Características

### 🔧 API Endpoints

- ⏱️ **Time Tracking** - Registro de sesiones de trabajo
- 👤 **User Management** - Autenticación y perfiles
- 📁 **Projects** - Gestión de proyectos y tareas
- 📊 **Analytics** - Reportes y métricas
- 🔗 **Git Integration** - Vinculación con commits y branches

### 🔐 Seguridad

- JWT Authentication con tokens de acceso y refresh
- Bcrypt para hashing de contraseñas
- Validación de datos con Pydantic
- CORS configurado para producción

### 🗄️ Base de Datos

- Modelo relacional con SQLAlchemy ORM
- Migraciones versionadas con Alembic
- Consultas SQL avanzadas (CTEs, Window Functions, JOINs)
- Índices optimizados para queries de reportes

### 🐍 Scripts de Automatización

- Lectura automática de estado Git (branches, commits, diff)
- Asociación de tiempo con eventos Git
- CLI con argparse para integración en workflows

---

## 🏗️ Arquitectura

```text
┌─────────────────┐
│  Client Apps    │
│ (Web/Mobile)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │
│   Endpoints     │
│   + JWT Auth    │
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
    ▼          ▼
┌─────────┐ ┌──────────┐
│PostgreSQL│ │   Git    │
│ Database│ │  Repos   │
└─────────┘ └──────────┘
```

---

## 🛠️ Stack Tecnológico

### Core

- **Python 3.11+** - Lenguaje principal
- **FastAPI** - Framework web asíncrono
- **Uvicorn** - ASGI server de alto rendimiento
- **Pydantic** - Validación de datos y schemas

### Database

- **PostgreSQL** - Base de datos principal
- **SQLAlchemy 2.0** - ORM asíncrono
- **Alembic** - Sistema de migraciones
- **asyncpg** - Driver asíncrono para PostgreSQL

### Authentication & Security

- **python-jose** - JWT tokens
- **passlib + bcrypt** - Hashing de contraseñas
- **python-dotenv** - Variables de entorno

### Testing & Quality

- **pytest** - Framework de testing
- **pytest-asyncio** - Tests asíncronos
- **httpx** - Cliente HTTP para tests

### Git Integration

- **subprocess** - Ejecución de comandos Git
- **argparse** - CLI para scripts de automatización

---

## 📊 Modelo de Datos

```text
users
├── id
├── email
├── hashed_password
└── created_at

projects
├── id
├── name
├── user_id (FK)
└── repository_url

time_entries
├── id
├── user_id (FK)
├── project_id (FK)
├── start_time
├── end_time
└── duration

git_events
├── id
├── time_entry_id (FK)
├── commit_hash
├── branch_name
└── files_changed
```

---

## 🎯 Roadmap

### ✅ Fase 1: MVP (Actual)

- [x] Setup inicial del proyecto
- [x] Estructura base con FastAPI
- [x] Requirements y dependencias
- [ ] Modelos de base de datos
- [ ] Sistema de autenticación JWT
- [ ] Endpoints básicos de time tracking

### 🔄 Fase 2: Git Integration

- [ ] Script CLI para lectura de Git
- [ ] Endpoint para asociar commits con tiempo
- [ ] Análisis de branches activos
- [ ] Webhook handlers para eventos Git

### 📊 Fase 3: Analytics

- [ ] Queries SQL avanzadas con CTEs
- [ ] Endpoints de reportes personalizados
- [ ] Agregaciones por día/semana/mes
- [ ] Optimización con índices y EXPLAIN

### 🚀 Fase 4: Production Ready

- [ ] CI/CD con GitHub Actions
- [ ] Dockerización
- [ ] Logging estructurado
- [ ] Monitoring y health checks

---

## 🎓 Skills Demostradas

```text
✓ FastAPI & Async Python     ✓ RESTful API Design
✓ JWT Authentication          ✓ SQL Avanzado (CTEs, JOINs)
✓ PostgreSQL + SQLAlchemy     ✓ Git Automation
✓ Database Migrations         ✓ Testing con pytest
✓ Asyncio & Concurrency       ✓ CLI Tools
```

---

## 📁 Estructura del Proyecto

```text
backend/
├── alembic/              # Migraciones de base de datos
├── app/
│   ├── main.py          # Aplicación principal FastAPI
│   ├── config.py        # Configuración y variables de entorno
│   ├── db.py            # Conexión a base de datos
│   ├── models.py        # Modelos SQLAlchemy
│   ├── auth.py          # Utilidades de autenticación
│   └── routers/         # Endpoints organizados por dominio
│       ├── auth_router.py
│       └── ping_router.py
└── requirements.txt     # Dependencias Python
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

## 🙏 Acknowledgments

Backend desarrollado como demostración de habilidades en Python, FastAPI, y arquitectura de APIs RESTful.

---

**⭐ DevMetrics Backend** - *API robusta para métricas de productividad*
