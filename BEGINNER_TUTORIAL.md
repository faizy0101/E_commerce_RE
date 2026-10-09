# Beginner Tutorial — `E_Commerce_RE` (Django 6.1 Project)

This guide is written for someone who has **never run a Django project before**.
It does **read-only exploration first**, explains every file you need to
understand, and then walks you through bringing the project to life **one careful
step at a time**.

Everything below is based on the *actual* state of this project as it exists on
disk right now. Nothing is guessed. If something here differs from your screen,
that means the project was changed since this file was written.

---

## 0. The "what is this?" map (30-second version)

```
E_Commerce_RE/                 <- the project root (C:\Users\Faizy\PycharmProjects\E_Commerce_RE)
│
├── .venv/                     <- Python virtual environment (Python 3.13.15)
├── manage.py                  <- Django's command-line tool (the "do everything" script)
├── main.py                    <- a leftover PyCharm sample script (NOT used by the web app)
├── db.sqlite3                 <- the database file (currently EMPTY — 0 tables)
│
├── ecom/                      <- the Django "project" package
│   ├── __init__.py
│   ├── asgi.py                <- for WebSockets/ASGI servers
│   ├── wsgi.py                <- for normal web servers (Apache/Nginx/Gunicorn)
│   ├── settings.py            <- ALL global config (installed apps, DB, static files…)
│   └── urls.py                <- the "master" list of URLs
│
├── ecom_app/                  <- the Django "app" package (your actual website code)
│   ├── __init__.py
│   ├── apps.py                <- tells Django how to load the app
│   ├── admin.py               <- register models for the admin site (Login, seller, buyer)
│   ├── apps.py                <- tells Django how to load the app
│   ├── forms.py               <- ModelForms for login/buyer/seller signup
│   ├── models.py              <- your database tables (Login, seller, buyer)
│   ├── views.py               <- what happens when someone visits a page
│   ├── views_admin.py         <- empty placeholder (reserved for admin views)
│   ├── views_buyer.py         <- empty placeholder (reserved for buyer views)
│   ├── views_seller.py        <- empty placeholder (reserved for seller views)
│   ├── urls.py                <- which URL belongs to which view (inside the app)
│   ├── tests.py               <- automated tests (empty right now)
│   └── migrations/            <- saved record of every change to your database
│       └── __init__.py
│
├── templates/                 <- HTML files live here (top-level, shared by the app)
│   ├── base.html              <- the "shell" page the others extend (simple version)
│   ├── index.html             <- the homepage (a big Bootstrap template)
│   ├── login.html             <- the login page (self-contained, fancy styling)
│   ├── user_add.html          <- seller signup form (renders sellerform)
│   ├── customer_add.html      <- buyer signup form (renders buyerform)
│   ├── user.html              <- leftover sample template (not wired up)
│   └── Modified_files/        <- a scratch/backup folder (see note in §4.5)
│       ├── base.html          <- a much BIGGER base page (not wired up yet)
│       └── index.html         <- identical copy of templates/index.html
│
└── static/                    <- CSS, JavaScript, images, fonts (everything the browser downloads)
    ├── css/
    ├── fonts/
    ├── images/
    ├── js/
    ├── scss/
    ├── 2026.js               <- powers the big base page in Modified_files/
    ├── runtime.js
    ├── vendors.js
    ├── style.css             <- global CSS (used by index.html and base.html)
    ├── vendor-chartjs.js
    └── vendor-fullcalendar.js
```

**Key facts you must remember:**

| Question | Answer |
|---|---|
| Project (the thing `manage.py` talks to) | `ecom` |
| App (where your code lives) | `ecom_app` |
| Database | **PostgreSQL** (`e_commerce_db` on `127.0.0.1:5432`, user `postgres`) — *not* SQLite anymore |
| Web framework | Django 6.1.1 |
| Python | 3.13.15 (`.venv`) |
| Where HTML lives | `templates/` |
| Where CSS/JS/images live | `static/` |
| Where to run commands | in the project root (`E_Commerce_RE`) |
| Custom user model | `ecom_app.Login` (extends `AbstractUser`) |

---

## 1. Before you start — Prerequisites

You need:
1. A working Windows PC (this project was built on Windows 10/11).
2. Python 3.13.x (a `.venv` with 3.13.15 is already created for you — see §3.1).
3. Django 6.1.1 (already installed in the `.venv` — see §3.1).
4. **PostgreSQL** — the project uses PostgreSQL (not SQLite); install it and create
   the `e_commerce_db` database (see §4).
5. A text editor (PyCharm is recommended — the `.idea/` folder proves it).
6. A web browser (Edge, Chrome, Firefox — anything modern).

If you ever need to install Django yourself on another machine, the command is:
```bash
pip install django
```
But **do not do that here** — the virtualenv already has it.

---

## 2. Step 1 — Activate the virtualenv

A *virtual environment* is a folder that holds its own copy of Python plus a list
of installed packages, so your project's dependencies don't clash with anything
else on your computer.

The project keeps its virtualenv in `.venv/`. **Never delete this folder.**

### 3.1 Open a terminal in the right place

Every step below uses Windows PowerShell. Open PowerShell, then go to the project
folder. The project folder is:

```
C:\Users\Faizy\PycharmProjects\E_Commerce_RE
```

You can navigate there with:

```powershell
Set-Location "C:\Users\Faizy\PycharmProjects\E_Commerce_RE"
```

> **Tip:** From now on, "run this command" means open PowerShell, make sure you are
> in the folder above, and paste the line.

### 3.2 Activate the virtualenv

```powershell
. .venv\Scripts\Activate.ps1
```

(After activation, your prompt will change to show `(.venv)` at the start, like:
`__(.venv)__ PS C:\Users\Faizy\PycharmProjects\E_Commerce_RE>`.)

### 3.3 Verify it works

```powershell
python --version        # should print: Python 3.13.15
python -m django version # should print: 6.1.1
```

If you see numbers close to these, you are good. If you get "command not found"
or a different Django version, you forgot Step 1 (the `Activate` command) — run
it again.

> **Important:** Each new terminal window starts fresh. If you open a new
> PowerShell, you must re-run `. .venv\Scripts\Activate.ps1` every time.

---

## 3. Step 2 — PostgreSQL database setup

**Important:** the project now uses **PostgreSQL**, not SQLite. The `db.sqlite3`
file still exists but is no longer used — the active database is
`e_commerce_db` running on `127.0.0.1:5432` (user `postgres` / password `1234`).

### 3.1 Install PostgreSQL (if not already installed)

Download the installer from <https://www.enterprisedb.com/downloads/postgres-postgresql-downloads>
and run it with the default options. **Remember the password you set** — that
becomes the `postgres` superuser password.

### 3.2 Create the database

From `psql` or pgAdmin, run:

```sql
CREATE DATABASE e_commerce_db;
```

Or from PowerShell:

```powershell
psql -U postgres -c "CREATE DATABASE e_commerce_db;"
```

### 3.3 Install the Python driver

```powershell
pip install psycopg2-binary
```

(The `.venv` may already include it; reinstall if unsure.)

### 3.4 Run the database migrations

Django keeps a record of how the database should look in the `migrations/`
folder. "Migrating" means "build the tables Django expects".

#### 3.4.1 Check current migration status

```powershell
python manage.py showmigrations
```

You will see output like:
```
admin
 [ ] 0001_initial
 [ ] 0002_logentry_remove_auto_add    (etc.)
auth
 [ ] 0001_initial
contenttypes
 [ ] 0001_initial
sessions
 [ ] 0001_initial
ecom_app
 [ ] 0001_initial
```

The `ecom_app` entry is **new** — it reflects the custom `Login`, `seller`, and
`buyer` models in `models.py`. The `[ ]` means "this migration has NOT been applied yet".

#### 3.4.2 Apply all migrations

```powershell
python manage.py migrate
```

This creates the standard Django tables *plus* the project-specific tables
(`ecom_app_login`, `ecom_app_seller`, `ecom_app_buyer`).

#### 3.4.3 Confirm it worked

```powershell
python manage.py showmigrations
```

Now the boxes should be `[x]` (applied).

---

## 4. Step 3 — Create an admin user (so you can log in to /admin)

Django ships with a ready-made login-protected **admin area**. To use it you need
a "superuser" (an account with full permissions).

```powershell
python manage.py createsuperuser
```

The prompts are:
1. **Username** — pick `admin` (or your name).
2. **Email address** — any valid email, e.g. `admin@example.com`.
3. **Password** — must be 8+ characters and **not** a common password (Django
   enforces this; "password123" is rejected — use something like `MyP@ssw0rd!`).
4. **Password (again)** — confirm.

> If you ever forget this password, run `python manage.py changepassword admin`.

---

## 5. Step 4 — Start the website on your computer

Django includes a tiny built-in web server for development. Never use it in
production — it is for your laptop only.

```powershell
python manage.py runserver
```

You will see something like:
```
Watching for file changes...
Performing system checks...

System check identified no issues (0 silenced).
October 05, 2026 - 03:15:00
Django version 6.1.1, using settings 'ecom.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL + C.
```

While that terminal window stays open, open a browser and go to:

- <http://127.0.0.1:8000/> → the **home page** (renders `index.html`)
- <http://127.0.0.1:8000/base> → the **admin dashboard shell** (renders `base.html`)
- <http://127.0.0.1:8000/login> → the **login page** (renders `login.html`)
- <http://127.0.0.1:8000/user_add> → **seller signup** (renders `user_add.html`)
- <http://127.0.0.1:8000/customer_add> → **buyer signup** (renders `customer_add.html`)
- <http://127.0.0.1:8000/admin/> → Django's built-in admin panel (log in with the
  superuser you just created)

> Leave `runserver` running. To stop it, press `Ctrl + C` in that terminal, then
> type `y` when asked to terminate the job.

---

## 6. How does a web page actually get built? (Django's MVT explained, slowly)

When a visitor opens a URL, a *chain of four* files decides what they see:

```
Browser request
      │
      ▼
ecom/urls.py        ← "master list" — says e.g. path('', include('ecom_app.urls'))
      │
      ▼
ecom_app/urls.py    ← "app list"  — says e.g. path('login', views.login)
      │
      ▼
ecom_app/views.py   ← runs a Python function, builds data, picks an HTML file
      │
      ▼
templates/login.html ← the HTML template that becomes the page
```

### 6.1 ecom/urls.py — the project-level "master map"

```python
from django.contrib import admin
from django.urls import path, include          # include() lets you merge in another file's URLs

urlpatterns = [
    path('admin/', admin.site.urls),            # /admin/ → Django's built-in admin area
    path('', include('ecom_app.urls')),         # everything else → handed to ecom_app
]
```

`path('', include(...))` means "for the root URL and anything below it, ask the
app's `urls.py` to decide."

### 6.2 ecom_app/urls.py — the app's "menu of pages"

```python
from django.urls import path

from ecom_app import views

urlpatterns=[
    path('',views.index,name='index'),
    path('base',views.admin_page, name='base'),
    path('login',views.login,name='login'),
    path('user_add',views.user_add,name='user_add'),
    path('customer_add',views.customer_add,name='customer_add'),
]
```

Each entry: `path('URL-fragment', the-function-that-handles-it, name='short-label')`.

- The `name=` is **crucial** — templates use `{% url 'login' %}` to build links so
  they won't break if you later move the page.
- Notice there are **no trailing slashes** on `base`, `login`, `user_add`, and
  `customer_add`. By default Django redirects `/base/` to `/base`. This is fine but
  inconsistent; the home page `'` does end effectively at the root.

### 6.3 ecom_app/views.py — the "controller"

```python
from urllib import request

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from ecom_app.forms import loginform, sellerform, buyerform


# Create your views here.
def index(request):
    return render(request,'index.html')

def admin_page(request):
    return render(request,'base.html')

def login(request):
    return render(request,'login.html')

def user_add(request):
    form1=loginform()
    form2=sellerform()
    if request.method=="POST":
        form1=loginform(request.POST)
        form2=sellerform(request.POST)
        if form1.is_valid() and form2.is_valid():
            user_data=form1.save(commit=False)
            user_data.is_seller=True
            user_data.save()
            user1=form2.save(commit=False)
            user1.user=user_data
            user1.save()
            return redirect('login')
    return render(request,'user_add.html',{'form1':form1,'form2':form2})

def customer_add(request):
    form1=loginform()
    form2=buyerform()
    if request.method=="POST":
        form1=loginform(request.POST)
        form2=buyerform(request.POST)
        if form1.is_valid() and form2.is_valid():
            user_data=form1.save(commit=False)
            user_data.is_buyer=True
            user_data.save()
            user1=form2.save(commit=False)
            user1.user=user_data
            user1.save()
            return redirect('login')
    return render(request,'customer_add.html',{'form1':form1,'form2':form2})
```

`render(request, 'template.html')` loads the named template from `templates/` and
returns it to the browser. The `request` object holds everything about the
visitor's HTTP request (cookies, POST data, user, etc.).

- `index`, `admin_page`, and `login` are simple render functions.
- `user_add` and `customer_add` are **form-handling** views: they show a blank
  `loginform` + `sellerform` (or `buyerform`) on `GET`, and on `POST` they validate
  both forms, set `is_seller=True` (or `is_buyer=True`) on the `Login` user, save
  both objects, then redirect to the login page.
- `ecom_app/forms.py` defines three `ModelForm`s (`loginform`, `sellerform`,
  `buyerform`) tied to the models in §6.5.
- The view function is named `login`, which shadows `django.contrib.auth.login`.
  If you later want real authentication you must alias the import (see §14.1).

> ⚠️ **Note for later:** the current `login` view just *shows* the form — it does
> not actually log anyone in. Fixing this is in §14.1.

### 6.4 templates/login.html — the visual page

This file is a complete, self-contained HTML page: it declares its own `<head>`,
inline `<style>`, and inline JavaScript (`togglePass()`). It even has:

```django
<a href="{% url 'index' %}">Property</a>
```

which proves `{% url %}` reverse-lookup works (you can jump to the home page from
the login screen).

### 6.5 ecom_app/models.py — the database tables

The project uses a **custom user model** (`Login`) plus two related profile models:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class Login(AbstractUser):
    is_seller=models.BooleanField(default=False)
    is_buyer=models.BooleanField(default=False)

class buyer(models.Model):
    user=models.OneToOneField(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class seller(models.Model):
    user=models.OneToOneField(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    tax_number=models.CharField(max_length=100)
    def __str__(self):
        return self.name
```

- `Login` extends `AbstractUser`, adding `is_seller` and `is_buyer` flags so a
  single account can be either a seller *or* a buyer.
- `buyer` and `seller` are linked to `Login` via a `OneToOneField` (one user → one
  profile). Their extra fields store contact/address/tax details.
- `settings.py` declares `AUTH_USER_MODEL = 'ecom_app.Login'` so Django uses this
  model everywhere instead of the built-in `User`.
- These three models are registered in `ecom_app/admin.py` and appear in the Django
  admin under the same names.

### 6.4 templates/login.html — the visual page

This file is a complete, self-contained HTML page: it declares its own `<head>`,
inline `<style>`, and inline JavaScript (`togglePass()`). It even has:

```django
<a href="{% url 'index' %}">Property</a>
```

which proves `{% url %}` reverse-lookup works (you can jump to the home page from
the login screen).

---

## 7. The settings file explained (ecom/settings.py) — one setting per concern

You will spend most of your time here. Each block below is a copy/paste excerpt
with an explanation.

### 7.1 Project root

```python
BASE_DIR = Path(__file__).resolve().parent.parent
```
`__file__` = the path to `settings.py` = `.../ecom/settings.py`.
`.parent` = `.../ecom`.
`.parent.parent` = `.../` (the project root).
**Everything is built from `BASE_DIR`.**

### 7.2 Security (development only — these must change for real deployment)

```python
SECRET_KEY = 'django-insecure-...'     # never commit the real one to GitHub
DEBUG = True                           # shows full error pages when something breaks
ALLOWED_HOSTS = []                     # empty = only localhost may view the site
```
While `DEBUG = True` you get helpful red error pages. Leave this on while learning.

### 7.3 Installed apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',            # the /admin/ area
    'django.contrib.auth',             # users, groups, permissions
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ecom_app',                        # YOUR app
    'crispy_forms',                    # renders Bootstrap-friendly forms
    'crispy_bootstrap5'                # crispy-forms adapter for Bootstrap 5
]
```

Adding `'ecom_app'` is what makes Django treat `ecom_app/` as part of the site
(so its `models.py`, `templates/` fallback, `migrations/` are all discovered).
The two `crispy_*` apps enable `{{ form|crispy }}` rendering in templates.

### 7.4 Middleware (runs before/after every request)

Standard list — security headers, sessions, CSRF (form forgery protection),
authentication, messages, clickjacking. You normally don't touch this while
learning.

### 7.5 Templates

```python
ROOT_URLCONF = 'ecom.urls'             # use the project-level URL file shown in §6.1

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],   # look in /templates FIRST
    'APP_DIRS': True,                                  # ALSO look inside app folders
    'OPTIONS': {
        'context_processors': [                       # inject `request` and messages
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]
```
The `templates/` folder is where `login.html`, `index.html`, and `base.html` live
— that is why `views.py` can find them by name.

### 7.6 The database (now PostgreSQL)

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "e_commerce_db",
        "USER": "postgres",
        "PASSWORD": "1234",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
```

PostgreSQL replaced SQLite — make sure PostgreSQL is installed and running, and
that the `e_commerce_db` database exists (see §3). The `psycopg2-binary` driver
must be installed in the `.venv` for Django to connect.

### 7.6b Custom user model

```python
AUTH_USER_MODEL = 'ecom_app.Login'
```

This tells Django to use the project-defined `Login` model (in
`models.py` §6.5) as the user model. Changing this *after* the first migration
is painful — it is already set, so don't change it unless you know what you are
doing.

### 7.7 Password rules

Four validators enforce secure passwords for new users (length, not-common, not-
fully numeric, not too similar to username). That's why `createsuperuser` rejects
weak passwords in §4.

### 7.8 Internationalization

Defaults (`en-us`, `UTC`, internationalization on). No change needed.

### 7.9 Static files

```python
STATIC_URL = 'static/'                              # the URL prefix
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # where to FIND extra static files
```
This tells Django: "when a browser asks for `/static/style.css`, look in the
`static/` folder in the project root." That is why `login.html` can use
`{% static 'css/style.css' %}` and find the real file.

### 7.10 The `main.py` file

`main.py` is **NOT part of the website.** It is a leftover auto-generated file
PyCharm creates when you start a project ("Press Shift+F10 to execute…"). It only
prints "Hi, PyCharm" when you double-click it in the IDE. **Ignore it.** Django never
reads it. You can delete it later if you want.

### 7.11 Email (currently broken — see "Known issues" in §14)

```python
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}
```
This uses the key `MAILERS`, which is **not a real Django setting**. The correct
key is `EMAIL_BACKEND`. See §14.2 for the fix.

---

## 8. The templates, side by side

| File | Size | Role | Status |
|---|---|---|---|
| `templates/base.html` | 53 lines, ~2 KB | simple shell with `{% block content %}` | **live** (used by `/base`) |
| `templates/index.html` | 1040 lines, ~42 KB | full Bootstrap "Property" homepage | **live** (used by `/`) |
| `templates/login.html` | 276 lines, ~6.7 KB | standalone login page | **live** (used by `/login`) |
| `templates/user_add.html` | — | seller signup page (renders `loginform` + `sellerform`) | **live** (used by `/user_add`) |
| `templates/customer_add.html` | — | buyer signup page (renders `loginform` + `buyerform`) | **live** (used by `/customer_add`) |
| `templates/user.html` | — | leftover sample template | **NOT used** |
| `templates/Modified_files/base.html` | 517 lines, ~30 KB | a fancier dashboard shell | **NOT used** |
| `templates/Modified_files/index.html` | identical to `templates/index.html` | duplicate backup | **NOT used** |

### 8.1 templates/base.html (simple shell, 53 lines)

- Has `{% load static %}` at the top — good.
- Loads `runtime.js`, `vendors.js`, `2026.js`, `vendor-chartjs.js`,
  `vendor-fullcalendar.js`, and `style.css` from `static/`.
- Sets the page `<title>` to "Dashboard · 2026 Redesign Preview".
- Contains a placeholder `<h1>welcome</h1>` followed by `{% block content %}{% endblock %}`
  where child templates inject page-specific markup.

> ⚠️ The `<h1>welcome</h1>` sits *before* `{% block content %}`, so it will show on
> every page that extends this base. That may not be what you want.

### 8.2 templates/Modified_files/base.html (the big one, 517 lines)

This is a complete dashboard UI (KPIs, charts, cards). But:
- It **lacks `{% load static %}`** — if any line uses `{% static %}` it raises
  "TemplateSyntaxError: 'static' is not a valid tag". (The version you read
  actually has no static tag — it loads JS from raw paths — so it *renders*,
  but it is inconsistent.)
- It is **not referenced by any view** (only the small `base.html` is).
- `static/2026.js` is a webpack bundle that **builds the sidebar and topbar
  client-side** from hard-coded menu data (Dashboard, Email, Calendar, Chat,
  Charts, Forms, …). Those menu links point to files like `email.html`,
  `calendar.html` that do **not exist** as routes — they rely on the old
  multi-page `index.html` asset set.

There is also a stray empty file at the **project-root** `Modified_files/base.html`
(size 0) — clearly an accidental copy. You can delete the whole `Modified_files/`
scratch folder once you no longer need the backup.

### 8.3 templates/index.html (the homepage)

- Uses the "Property" Bootstrap template (author: Untree.co), 1040 lines.
- Loads `icomoon` and `flaticon` icon fonts plus AOS + tiny-slider JS.
- The hero title: "Easiest way to find your dream home".
- **Broken links to be aware of:** the navbar uses `{% static 'index.html' %}`,
  `{% static 'properties.html' %}`, `{% static 'services.html' %}`, etc. — these
  files don't exist in `static/`, so those menu items 404. Fix by changing them
  to `{% url 'index' %}` or removing them.

### 8.5 templates/user_add.html & templates/customer_add.html

- Both render two `ModelForm`s side-by-side (`loginform` + `sellerform` or
  `buyerform`).
- They use `{% csrf_token %}` inside the `<form>` so POST works.
- On successful submit the view redirects to `/login` (see §6.3).

- Declares its own `<style>` and JavaScript inline.
- Contains a "Show/Hide password" toggle (`togglePass()`).
- Has a fake "Forgot password?" link and a "Sign up" link that both `#` (dead).

---

## 9. Step 5 — Understanding the URL→view→template flow

Visit these URLs while `runserver` is running to see each part in action:

| URL | View called | Template shown |
|---|---|---|
| <http://127.0.0.1:8000/> | `views.index` | `templates/index.html` |
| <http://127.0.0.1:8000/base> | `views.admin_page` | `templates/base.html` |
| <http://127.0.0.1:8000/login> | `views.login` | `templates/login.html` |
| <http://127.0.0.1:8000/user_add> | `views.user_add` | `templates/user_add.html` |
| <http://127.0.0.1:8000/customer_add> | `views.customer_add` | `templates/customer_add.html` |
| <http://127.0.0.1:8000/admin/> | Django's built-in | admin login page |

Open the browser's "View source" and "Inspect element" on each page. You will see
exactly the templates above rendered to HTML. This is the quickest way to confirm
"the file I edited is the one the browser sees."

---

## 10. Step 6 — Make your first tiny change (and see it live)

Django's dev server watches files and reloads automatically.

1. Stop `runserver` with `Ctrl + C` (if running).
2. Open `templates/login.html` in your editor.
3. Find the line:
   ```html
   <h1 class="login-title">Welcome back</h1>
   ```
4. Change the text to:
   ```html
   <h1 class="login-title">Welcome back — Django is working</h1>
   ```
5. Save the file.
6. Restart `python manage.py runserver`.
7. Reload <http://127.0.0.1:8000/login>.

You will see the new text. This proves the request → view → template chain.

---

## 11. Step 7 — Add a real page (create your own)

This is the smallest useful exercise: make a third page appear at `/about`.

### 11.1 Add a view

Open `ecom_app/views.py` and add:

```python
def about(request):
    return render(request, 'about.html')
```

Save.

### 11.2 Add a URL

Open `ecom_app/urls.py` and add a line:

```python
path('about', views.about, name='about'),
```

Save.

### 11.3 Add the template

Create `templates/about.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>About — E_Commerce_RE</title>
</head>
<body>
  <h1>About this site</h1>
  <p>This page was created in the beginner tutorial.</p>
  <p><a href="{% url 'index' %}">Back to home</a></p>
</body>
</html>
```

### 11.4 Verify

Restart `runserver` (dev server doesn't always pick up new modules instantly).
Go to <http://127.0.0.1:8000/about>. You should see your new page, and the
"Back to home" link works because of `{% url 'index' %}`.

---

## 12. Step 8 — Connect templates with `{% block %}` (template inheritance)

The small `base.html` is designed to be *extended*. Try it with `login.html`.

At the very top of `login.html` (before `<!DOCTYPE html>`), you currently have a
full standalone page. To inherit from `base.html` instead, you would eventually
replace the whole file with:

```django
{% extends 'base.html' %}
{% block content %}
  <div class="login-wrapper">
    <form method="post">{% csrf_token %}
      <!-- your existing form markup -->
    </form>
  </div>
{% endblock %}
```

For now, **do the standalone version** — it works. The inheritance is an optional
refactor covered in §14 ("what's broken").

> ⚠️ `base.html` pulls in `style.css`, `2026.js`, etc. If `login.html` extends it,
> the fancy inline styles in the current `login.html` will be overridden by the
> dashboard's `style.css`. Keep the standalone `login.html` for the pretty login
> card; only switch to inheritance once you are ready to restyle it.

---

## 13. Common commands you will type (the cheat sheet)

| Command | What it does |
|---|---|
| `python manage.py runserver` | start the dev web server (Ctrl+C to stop) |
| `python manage.py migrate` | apply database changes (always run after pulling new code) |
| `python manage.py makemigrations` | tell Django you changed `models.py` |
| `python manage.py createsuperuser` | make an admin login |
| `python manage.py changepassword USER` | reset a user's password |
| `python manage.py shell` | open a Python prompt with Django loaded |
| `python manage.py test` | run `tests.py` |
| `python manage.py showmigrations` | list which migrations are installed/applied |
| `python manage.py check` | run Django's self-diagnostics |
| `python manage.py startapp NAME` | create a new app folder |

Type them **in the project root** and with the virtualenv **activated** (`. .venv\Scripts\Activate.ps1`).

---

## 14. Known issues & "things a beginner always misses"

These are real problems in the current code. They do not block you from running
the site, but you will hit them eventually.

### 14.1 The login view does not actually log anyone in

`views.py`:
```python
def login(request):
    return render(request, 'login.html')
```
This only shows the form. The form has no `{% csrf_token %}`, no `action`, and no
server-side code that calls Django's `authenticate()` / `login()`. Clicking "Log
In" does nothing useful.

**Fix sketch (advanced):**
```python
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect

def user_login(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user is not None:
            auth_login(request, user)
            return redirect('index')
    return render(request, 'login.html')
```
Plus add `{% csrf_token %}` inside the `<form>`, set `action="{% url 'login' %}"}`,
add `LOGIN_URL = 'login'` and `LOGIN_REDIRECT_URL = 'index'` to
`settings.py`, and protect pages with `@login_required`.

> The current function is *also* named `login`, which shadows the standard Django
> `django.contrib.auth.login` function. Rename it before importing — that's why
> the sketch above aliases the import as `auth_login`.
>
> **Contrast with signup:** the `user_add` and `customer_add` views (§6.3) *do*
> handle `POST` correctly — they validate two forms, save the user with the
> right flag (`is_seller`/`is_buyer`), link the profile, then redirect. Use them
> as a reference when you write the real login handler.

### 14.2 `MAILERS` is the wrong setting name

```python
MAILERS = { 'default': { 'BACKEND': 'django.core.mail.backends.console.EmailBackend' } }
```
This should be:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
`MAILERS` is not a real Django setting, so email sending is currently
"unconfigured" (Django would raise an exception the first time you actually try
to send mail). Renaming it fixes that.

### 14.3 No `requirements.txt`

There is no `requirements.txt`. The project relies on the `.venv` folder being
committed/shared. For a fresh setup you would need to recreate it. To fix:

```powershell
. .venv\Scripts\Activate.ps1
python -m pip freeze > requirements.txt
```
Then on a new machine:
```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
> Note: you must also install `psycopg2-binary` separately if PostgreSQL support
> was missing from the freeze output.

### 14.4 No `.gitignore` at the project root

There is **no** `.gitignore` inside `E_Commerce_RE`. The `.gitignore` that exists
is at `C:\Users\Faizy` (the parent). Consequence: `db.sqlite3`, `.venv/`, and
`__pycache__/` could accidentally get committed.

Add a `E_Commerce_RE/.gitignore` containing at minimum:
```
__pycache__/
*.pyc
*.pyo
/staticfiles/
.DS_Store
.venv/
```
> Note: `db.sqlite3` is **no longer used** (PostgreSQL is the active database),
> but the line is harmless and protects the old file if it reappears.

### 14.5 The git repository lives in the wrong place

`git rev-parse --show-toplevel` reports `C:/Users/Faizy`, not the project folder.
That means **Git is tracking your whole user profile**, not just this project.
`git status` from the project folder shows dozens of unrelated files.

**Fix:** if you want real version control for just this project, run from inside
`E_Commerce_RE`:
```powershell
git init            # creates E_Commerce_RE/.git
```
…then the first commit will snapshot only project files. (Do this only if you
intend to use Git here — it's optional and read-only-exploration does not require it.)

### 14.6 Missing `favicon.png`

`login.html` and `index.html` both call `{% static 'favicon.png' %}`, but
`static/favicon.png` does not exist. The page still renders (the `<link>` just
gets a 404 URL), but it's untidy. Add a `favicon.png` to `static/` or remove the
line.

### 14.7 The `/base` URL has no trailing slash

`path('base', ...)` vs the more idiomatic `path('base/', ...)`. With the current
setting, a visitor typing `/base/` gets redirected to `/base` (and vice-versa for
pages with trailing slashes). Django's default `APPEND_SLASH = True` hides it, but
the inconsistency is easy to trip over. Use trailing slashes everywhere once you
have time.

### 14.8 `main.py` is confusing

It is a PyCharm template, not Django code. See §7.11. Delete or ignore it; it
does not affect the website.

### 14.9 `Modified_files/` is ambiguous

Two copies exist:
- `templates\Modified_files\base.html` (full dashboard, 517 lines) — not wired to
  a view.
- `Modified_files\base.html` (project root, **0 bytes**) — accidental empty
  file.

Both are backups/prototypes. To avoid confusion, decide on ONE `base.html` and
delete the rest.

---

## 15. The Django admin site (your built-in control panel)

Once you `createsuperuser` (§4) and `migrate` (§3), go to:

<http://127.0.0.1:8000/admin/>

You will see the login form, then the Django admin index. The three models in
`models.py` are **already registered** in `ecom_app/admin.py`:

```python
from django.contrib import admin
from ecom_app.models import seller, buyer, Login

admin.site.register(Login)
admin.site.register(seller)
admin.site.register(buyer)
```

So the admin will show **Login**, **seller**, and **buyer** sections where you can
add/edit/delete records — not just Django's defaults.

---

## 16. Project folder layout (quick visual reference)

```
E_Commerce_RE/
├── .idea/                 # PyCharm project metadata (auto-generated, share or ignore)
├── .venv/                 # Python virtual environment (DO NOT edit; re-create with pip)
├── static/                # CSS / JS / fonts / images  (browser downloads these)
│   ├── css/               │  ├── bootstrap.css
│   │   ├── aos.css           └── tiny-slider.css
│   ├── fonts/             │  ├── flaticon/   (font icons)
│   │   └── icomoon/        └── (webfont packs)
│   ├── images/            #   hero_bg_1..3.jpg, logo.png, person_1..6.jpg
│   ├── js/                #   bootstrap.bundle.min.js, aos.js, custom.js
│   ├── scss/              #   Bootstrap SCSS sources (source of css/bootstrap)
│   ├── 2026.js            #   webpack bundle → builds dashboard DOM (sidebar/topbar)
│   ├── runtime.js         #   webpack runtime chunk
│   ├── vendors.js         #   third-party vendor bundle
│   ├── style.css          #   global stylesheet (the big one)
│   ├── vendor-chartjs.js
│   └── vendor-fullcalendar.js
├── templates/             # HTML pages
│   ├── base.html          # simple shell
│   ├── index.html         # home page
│   ├── login.html         # login page
│   ├── user_add.html      # seller signup page
│   ├── customer_add.html  # buyer signup page
│   ├── user.html          # leftover sample (NOT used)
│   └── Modified_files/    # backup / prototype versions (not live)
├── ecom/                  # the Django "project" package
│   ├── __init__.py
│   ├── asgi.py            # entry for async servers
│   ├── settings.py        # ALL configuration
│   ├── urls.py            # master URL map
│   └── wsgi.py            # entry for normal (sync) servers
├── ecom_app/              # the Django "app" package  (your code lives here)
│   ├── __init__.py
│   ├── admin.py           # register models (Login, seller, buyer) for admin
│   ├── apps.py            # app metadata (registers the app)
│   ├── forms.py           # ModelForms: loginform, sellerform, buyerform
│   ├── migrations/        # saved database-change history
│   ├── models.py          # Login, seller, buyer
│   ├── tests.py           # automated tests (currently empty)
│   ├── urls.py            # app-level URL map
│   ├── views.py           # index, admin_page, login, user_add, customer_add
│   ├── views_admin.py     # empty placeholder
│   ├── views_buyer.py     # empty placeholder
│   ├── views_seller.py    # empty placeholder
│   ├── manage.py is at the project root (runserver, migrate, test...)
└── main.py                # PyCharm sample script (ignore)
```

---

## 17. How to run the project from a totally fresh terminal (one checklist)

Follow these steps verbatim each time you sit down to work:

1. Open **PowerShell**.
2. Go to the project folder:
   ```powershell
   Set-Location "C:\Users\Faizy\PycharmProjects\E_Commerce_RE"
   ```
3. Activate the virtualenv:
   ```powershell
   . .venv\Scripts\Activate.ps1
   ```
4. (Only the first time) make sure PostgreSQL is running and `e_commerce_db`
   exists (see §3).
5. (Only the first time) build the database:
   ```powershell
   python manage.py migrate
   ```
6. (Only the first time) create an admin user:
   ```powershell
   python manage.py createsuperuser
   ```
7. Start the server:
   ```powershell
   python manage.py runserver
   ```
8. Open a browser to <http://127.0.0.1:8000/>.

That's it. Leave step 7 running while you work; the page reloads when you save a
file.

Then open the browser to <http://127.0.0.1:8000/> and try the checklist in §17
whenever you start a new terminal session.

---

## 18. Troubleshooting (read this when something is "not working")

| Symptom | Cause / Fix |
|---|---|
| `python` is not recognized | You are not in the virtualenv. Re-run `. .venv\Scripts\Activate.ps1` **in this terminal**. |
| "No module named django.contrib" | Wrong Python. Activate the `.venv` (step 3 above). |
| "No module named psycopg2" / "could not connect to server" | PostgreSQL driver missing or server not running. `pip install psycopg2-binary` in the venv, then verify PostgreSQL is running and `e_commerce_db` exists (§3). |
| Admin page says "database is locked" | A previous `runserver`/`shell` is still open. Close other terminals, then `migrate` again. |
| Page shows a 404 at `/login` but the code looks right | You removed `runserver`, edited code, but forgot to restart the server. Restart it. |
| `TemplateDoesNotExist at /` for some file | The template name in `views.py` doesn't match a file in `templates/`. Check spelling and case (Linux/Mac is case-sensitive; Windows is not). |
| Form POST does nothing | There is no `{% csrf_token %}` in the `<form>`, or the view ignores `request.method == 'POST'`. |
| Static CSS missing (page is unstyled) | Either (a) dev server not running, (b) `STATIC_URL` mismatch, (c) the file isn't in `static/`. With `DEBUG = True` and `runserver`, Django serves `/static/` automatically. |
| "fatal: your current branch 'master' does not have any commits yet" | Normal for a brand-new repo with no commits. Nothing to fix unless you intend to commit (see §14.5). |
| Login form still won't log you in after edits | You replaced `views.login` but the URL still points to the old function, *or* the function name `login` shadows `django.contrib.auth.login`. Rename and re-save, then restart `runserver`. |

---

## 19. Where to go next (beyond this tutorial)

1. Make the `/login` page actually authenticate (§14.1) — use the working `user_add`
   / `customer_add` views as a POST-handling reference.
2. The `Login`, `seller`, and `buyer` models are already defined, migrated, and
   registered in admin (§6.5, §15). Add a `Product` model next, then
   `makemigrations` → `migrate` → register it in `admin.py`.
3. Create a listing page that reads products with `Product.objects.all()` and
   loops over them in a template with `{% for %}`.
4. Add `{% url %}` links and `{% block %}` inheritance so `login.html` and
   `about.html` extend `base.html`.
5. Add `LOGIN_URL` / `LOGIN_REDIRECT_URL` settings and protect pages with
   `@login_required`.
6. Add a `requirements.txt` and a proper `.gitignore` (§14.3, §14.4).
7. Refactor `user_add` / `customer_add` into `views_seller.py` / `views_buyer.py`
   (the empty placeholder files exist for this purpose) and wire them through
   `ecom_app/urls.py`.
8. When ready, switch `DEBUG = False`, set `ALLOWED_HOSTS`, and serve with a real
   WSGI server (Gunicorn) behind a reverse proxy — but that is a separate topic.

---

## Quick reference recap — the 4 files that make each page

Every time you build a new page, touch these *four* things (in order):

1. `templates/NEW_PAGE.html` — write the HTML.
2. `ecom_app/views.py` — add `def new_page(request): return render(request, 'NEW_PAGE.html')`.
3. `ecom_app/urls.py` — add `path('new-page', views.new_page, name='new_page')`.
4. (Optional) `ecom/settings.py` — add `LOGIN_URL = 'login'` once you need auth.

Then **restart `runserver`** and visit `/new-page`.

---

You now understand the whole project. The fastest path forward is:

```powershell
Set-Location "C:\Users\Faizy\PycharmProjects\E_Commerce_RE"
. .venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open the browser to <http://127.0.0.1:8000/> and try the checklist in §17
whenever you start a new terminal session.
