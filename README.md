# Argentina Post 🇦🇷📰

Periódico editorial digital construido con **Django**: los usuarios pueden leer artículos públicamente y, al iniciar sesión, crear, editar y eliminar sus propias crónicas.
---

## Características

- **Portada** con grilla de artículos (nota destacada + artículos secundarios).
- **Detalle de artículo** con categoría, autor, fecha y contenido opcional tipo "cómic".
- **Registro, login y logout** de usuarios (`django.contrib.auth`).
- **CRUD completo de artículos**:
  - `Crear` → cualquier usuario autenticado.
  - `Editar` / `Eliminar` → solo el **autor** del artículo (o un usuario `staff`).
- **Acceso público de solo lectura**: el usuario no autenticado únicamente ve los artículos en la portada y el detalle.
- **Admin de Django** para gestionar artículos y categorías.
- Estética periodística (The Economist) con toques cómic, responsive y sin dependencias de frontend.

## Stack tecnológico

| Componente | Tecnología |
|---|---|
| Lenguaje | Python ≥ 3.14 |
| Framework | Django 6.1.1 |
| Base de datos | SQLite (`src/db.sqlite3`) |
| Gestor de paquetes | [uv](https://docs.astral.sh/uv/) |
| Linter de templates | djlint |
| Frontend | HTML5 + CSS3 (sin frameworks JS) |

---

## Estructura del proyecto

```
Argentina-Post/
├── pyproject.toml              # Dependencias (uv)
├── uv.lock
└── src/
    ├── manage.py
    ├── db.sqlite3
    ├── config/                 # Proyecto Django
    │   ├── settings.py
    │   ├── urls.py             # Rutas raíz
    │   ├── wsgi.py / asgi.py
    ├── core/                   # Portada + base.html
    │   ├── views.py            # Inicio
    │   ├── templates/
    │   │   ├── base.html       # Layout global + nav con is_authenticated
    │   │   └── core/index.html # Portada de artículos
    │   └── static/core/css/
    ├── accounts/               # Registro / Login / Logout
    │   ├── forms.py            # RegistroForm (UserCreationForm)
    │   ├── views.py            # Registro
    │   ├── urls.py
    │   └── templates/accounts/ # login.html, registro.html
    └── articles/               # Modelos y CRUD de artículos
        ├── models.py           # Categoria, Articulos
        ├── forms.py            # ArticuloForm
        ├── views.py            # Detail, Create, Update, Delete
        ├── urls.py
        ├── admin.py
        ├── templates/articles/ # article_create / update / delete / datail
        └── static/articles/css/style.css
```

---

## Instalación y ejecución

Requisitos: [uv](https://docs.astral.sh/uv/) instalado y Python ≥ 3.14.

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd Argentina-Post

# 2. Crear el entorno e instalar dependencias
uv sync

# 3. Aplicar migraciones
uv run python src/manage.py migrate

# 4. (Opcional) Crear superusuario para el admin
uv run python src/manage.py createsuperuser

# 5. Levantar el servidor de desarrollo
uv run python src/manage.py runserver
```




## Rutas disponibles

| URL | Vista | Acceso |
|---|---|---|
| `/` | `core:home` (portada) | Público |
| `/articulos/detalle/<pk>/` | `articles:detalle` | Público |
| `/articulos/crear/` | `articles:crear` | Autenticado |
| `/articulos/editar/<pk>/` | `articles:editar` | Autor o staff |
| `/articulos/eliminar/<pk>/` | `articles:eliminar` | Autor o staff |
| `/accounts/` | `accounts:registro` | Público |
| `/accounts/login/` | `accounts:login` | Público |
| `/accounts/logout` | `accounts:logout` | Autenticado (POST) |
| `/admin/` | Django Admin | Superusuario |

## Modelos

```
Categoria
├── name          (CharField)

Articulos
├── title         (CharField)
├── subtitle      (CharField, blank)
├── content       (TextField)
├── opcional_content (TextField, nullable)
├── author        (FK → User, CASCADE)
├── category      (FK → Categoria, CASCADE)
└── crated_at     (DateTimeField, auto_now_add)
```

## Lógica de autenticación y permisos

- **`base.html`** renderiza los enlaces de navegación con `{% if user.is_authenticated %}`:
  - Autenticado → *Crear Artículo*, saludo de usuario y *Logout*.
  - Anónimo → *Login* y *Registrar*.
- **`LoginRequiredMixin`** en las vistas `Create`, `Update` y `Delete`: si no hay sesión, redirige a `/accounts/login/?next=...`.
- **`UserPassesTestMixin`** en `Update` y `Delete`: el `test_func` valida `user == articulo.author or user.is_staff`, devolviendo **403** al resto.
- En `article_datail.html` los botones *Editar* / *Eliminar* solo se pintan para el autor (o staff).
- Al crear un artículo, `form.instance.author = self.request.user` lo asigna automáticamente.

## Templates

| Template | Uso |
|---|---|
| `core/base.html` | Layout global (header, nav, footer) |
| `core/index.html` | Portada con grilla de artículos |
| `articles/article_datail.html` | Detalle + acciones editar/eliminar |
| `articles/article_create.html` | Formulario de alta |
| `articles/article_update.html` | Formulario de edición (pre-cargado) |
| `articles/article_delete.html` | Confirmación de baja (POST) |
| `accounts/login.html` / `registro.html` | Autenticación |

> Nota: el nombre `article_datail.html` es el que usa `ArticleDetailView` (typo histórico del proyecto).

## Tests

```bash
uv run python src/manage.py test core articles accounts
```

| Módulo | Cubre |
|---|---|
| `core` | Portada (200, artículos, estado vacío) y menú según `is_authenticated` |
| `articles` | Detalle con/ sin botones, crear/editar/eliminar, redirección a login y 403 para no autores |
| `accounts` | Login, logout, registro válido e inválido |

> Los tests usan `MD5PasswordHasher` en `accounts` porque PBKDF2 es muy lento en esta máquina; nunca se usa fuera de tests.


