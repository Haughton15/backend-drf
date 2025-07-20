# backend-drf

# Tabla de contenidos 
- [Requisitos previos](#prerequisites)
- [Docker](#docker)
- [Probar la API](#api)
- [Otros](#other)

# Requisitos Previos <a name="prerequisites"></a>
Crea un archivo `.env` en la raíz del proyecto. Puedes basarte en el archivo [.env.template](./.env.template) o utilizar este contenido como ejemplo:

```env
# PostgreSQL
POSTGRES_DB=drf_db
POSTGRES_USER=drf_user
POSTGRES_PASSWORD=drf_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@drf.mx
PGADMIN_DEFAULT_PASSWORD=admin@drf.mx

# Django
DJANGO_DEBUG=True

```

---

## Configuración con Docker

### Levantar los servicios con logs en la terminal

```bash
docker compose up --build
```

### Levantar los servicios en segundo plano

```bash
docker compose up -d --build
```

Esto iniciará tres servicios:

- `db`: Base de datos PostgreSQL
- `web`: API de Django REST Framework
- `pgadmin`: Interfaz gráfica para administrar la base de datos

---


# Probar la API <a name="api"></a>
Una vez que Docker esté corriendo, la base de datos se poblará automáticamente con datos de ejemplo. Puedes acceder a la documentación de la API a través de Swagger:

🔗 [http://127.0.0.1:8000/api/docs/#/](http://127.0.0.1:8000/api/docs/#/)


# Otros <a name="other"></a>

## pgAdmin

Para acceder a la interfaz de administración de base de datos:

🔗 [http://localhost:8888/](http://localhost:8888/)

Credenciales (desde el `.env`):

- **Email:** `admin@drf.mx`
- **Password:** `admin@drf.mx`

### Conectar al servidor en pgAdmin

Una vez dentro de pgAdmin:

1. Clic derecho en "Servers" → "Create" → "Server..."
2. En la pestaña **General**, ponle cualquier nombre (ej. `DRF Local`)
3. En la pestaña **Connection**:
   - **Host name/address:** `db`
   - **Port:** `5432`
   - **Username:** `drf_user`
   - **Password:** `drf_pass`