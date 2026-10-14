# Beginner Tutorial — `E_Commerce_RE`

A step-by-step guide written **like a teacher talking to you**.  
Read a section, do exactly what it says, then move to the next.  
By the end you will have a working Django e-commerce site — and you will understand **why**.

---

## Before you begin

You should know **very little** about Django. If a word is unfamiliar, the tutorial
explains it. Open a **PowerShell** window and keep it open for every step.

The project lives at:

```
C:\Users\Faizy\PycharmProjects\E_Commerce_RE
```

All commands below are run **from that folder** (unless told otherwise).

---

## Task 1 — Turn on the project

> Goal: see a blank Django page in your browser.

### 1.1 Activate your Python environment

A *virtual environment* is like a box that holds its own Python + packages, so they
don't clash with other projects. This project's box is called `.venv`.

```powershell
. .venv\Scripts\Activate.ps1
```

You will know it worked when the prompt changes to:

```
(.venv) PS C:\Users\Faizy\PycharmProjects\E_Commerce_RE>
```

### 1.2 Check you have the right tools

```powershell
python --version         # Python 3.13.15
python -m django version # 6.1.1
```

### 1.3 Make sure PostgreSQL is running

This project talks to **PostgreSQL**, not the tiny `db.sqlite3` file sitting in
the folder. PostgreSQL must be **installed and running** with a database called
`e_commerce_db`.

Check:
```powershell
psql -U postgres -c "SELECT 1;"
```
If it asks for a password, enter `1234` (that is what `settings.py` expects).

If the database doesn't exist yet:
```powershell
psql -U postgres -c "CREATE DATABASE e_commerce_db;"
```

### 1.4 Run the database migrations

"Migrations" are Django's way of turning your `models.py` (which describes tables in
Python) into **real tables** in PostgreSQL.

```powershell
python manage.py showmigrations
```

You will see `[ ]` on many lines — "not applied yet".

Apply them:
```powershell
python manage.py migrate
```

Run `showmigrations` again — now the boxes are `[x]`.

### 1.5 Start the web server

```powershell
python manage.py runserver
```

Leave that window running. In your browser go to:

- <http://127.0.0.1:8000/> — you should see the **home page**.

Press `Ctrl + C` in the terminal to stop the server when you are done.

> 💡 From now on, whenever you want to work, open **two** windows: one for
> `runserver`, one for typing commands. Always activate `.venv` first.

---

## Task 2 — Create an admin account

> Goal: log in to Django's built-in admin panel.

```powershell
python manage.py createsuperuser
```

Fill in:
- **Username** → `admin`
- **Email** → anything (e.g. `admin@example.com`)
- **Password** → something strong like `MyP@ssw0rd!` (Django will reject
  `password123`)
- **Password (again)** → same thing.

You can now log in at <http://127.0.0.1:8000/admin/> with `admin` / your password.

---

## Task 3 — Understand the project layout (read-only, 5 minutes)

Before you touch any code, here is the map. Everything has a place and a reason.

```
E_Commerce_RE/
├── .venv/              ← your Python box (do not edit)
├── manage.py           ← the "do everything" script  (python manage.py ______)
├── main.py             ← a leftover PyCharm file — IGNORE it
│
├── ecom/               ← the Django "project"  (settings, urls, wsgi)
│   └── settings.py     ← ALL your config lives here
│   └── urls.py         ← the master list of URLs
│
├── ecom_app/           ← the Django "app"  (your website code)
│   └── models.py       ← database tables (Python classes)
│   └── forms.py        ← forms that render HTML input fields
│   └── views.py        ← main pages (index, login, signup, dashboards)
│   └── views_admin.py  ← admin-side pages (manage buyers, CRUD)
│   └── views_buyer.py  ← buyer-side pages (profile view)
│   └── views_seller.py ← seller-side pages (profile view + edit)
│   └── urls.py         ← this app's URL list
│   └── admin.py        ← which models show up in /admin
│   └── migrations/     ← saved history of your database changes
│
├── templates/          ← all your HTML files
│   ├── index.html          ← the home page (property-listing theme)
│   ├── login.html          ← the login page (styled, standalone)
│   ├── user_add.html       ← seller signup page
│   ├── customer_add.html   ← buyer signup page
│   ├── user.html           ← leftover unused template — IGNORE it
│   ├── base.html           ← leftover dashboard shell (only /base renders it)
│   ├── seller/             ← seller dashboard templates
│   │   └── seller_base.html            ← Spark Admin dashboard shell
│   │   └── profile_view_seller.html    ← shows seller profile + Update link
│   │   └── update_seller_profile.html  ← edit seller profile form
│   ├── buyer/              ← buyer dashboard templates
│   │   └── buyer_base.html            ← Spark Admin dashboard shell
│   │   └── profile_view_buyer.html    ← shows buyer profile
│   └── admin/              ← admin dashboard templates
│       └── admin_base.html   ← Spark Admin dashboard shell
│       └── customers.html    ← buyer CRUD table
│       └── update.html       ← update buyer form
│       └── delete.html       ← (placeholder, unused)
│
└── static/             ← CSS, JS, images, fonts
    ├── css/            ← old stylesheets (login/index/signup still use css/style.css)
    ├── js/             ← old JS (bootstrap, slider, aos, etc.)
    ├── fonts/          ← icomoon / flaticon icon fonts
    ├── images/         ← property photos, hero banners
    ├── assets/         ← Spark Admin theme (dashboard CSS/JS/images)
    │   ├── css/main.css
    │   ├── js/dashboard.js
    │   ├── libs/       ← bootstrap, apexcharts, flatpickr, etc.
    │   └── images/     ← avatar, favicon.ico, etc.
    └── favicon.png     ← site icon (may be missing — see §10.8)
```

**Two names to remember:**
- `ecom` = the **project** (settings, master URLs)
- `ecom_app` = the **app** (models, forms, views, app URLs)

---

## Task 4 — Build the signup flow (models → forms → views → urls → templates)

> Goal: a visitor can **sign up** as a seller or buyer, then **log in**, and get
> redirected to their own dashboard.

This is the most important task. It touches every part of Django.  
We go **bottom-up**: database → form → view → URL → template.

### 4.1 The database tables (`models.py`)

Open `ecom_app/models.py`. You will see three classes:

```python
class Login(AbstractUser):           # the user account (username + password)
    is_seller = models.BooleanField(default=False)
    is_buyer  = models.BooleanField(default=False)

class seller(models.Model):          # extra info for a seller
    user = models.OneToOneField(Login, on_delete=models.CASCADE)
    name = ...
    email = ...
    phone = ...
    location = ...
    tax_number = ...

class buyer(models.Model):           # extra info for a buyer
    user = models.OneToOneField(Login, on_delete=models.CASCADE)
    name = ...
    email = ...
    phone = ...
    pincode = ...
    address = ...
```

**What this means:**
- `Login` is the **user model** — it extends Django's `AbstractUser` (gives you
  username + password for free) and adds two yes/no flags (`is_seller`, `is_buyer`).
- `seller` and `buyer` are **profile** tables — each stores one extra record per
  user, linked by `OneToOneField` (one user → one seller profile, one user → one buyer profile).
- `settings.py` says `AUTH_USER_MODEL = 'ecom_app.Login'`, so Django uses this
  `Login` class everywhere instead of the default `User`.

> ✅ You do **not** need to change the models. They are already correct.

### 4.2 The forms (`forms.py`)

Open `ecom_app/forms.py`:

```python
class loginform(UserCreationForm):     # signup form (username + 2 password fields)
    class Meta:
        model = Login
        fields = ('username', 'password1', 'password2')

class sellerform(forms.ModelForm):     # seller profile form
    class Meta:
        model = seller
        fields = '__all__'
        exclude = ("user",)           # the view sets this manually

class buyerform(forms.ModelForm):       # buyer profile form
    class Meta:
        model = buyer
        fields = '__all__'
        exclude = ("user",)           # the view sets this manually
```

**What this means:**
- `loginform` uses `UserCreationForm` — Django auto-creates the two password
  fields and **hashes** the password when saving. It is tied to the custom `Login`
  model (not the default `User`).
- `sellerform` / `buyerform` are `ModelForm`s — Django reads your `seller` / `buyer`
  model and builds a form field for each database column.
- `exclude = ("user",)` tells Django: "don't show the `user` field on the form —
  the view will link it to the right user behind the scenes."

> ✅ You do **not** need to change the forms. They are already correct.

### 4.3 The views (`views.py`)

Open `ecom_app/views.py` and look at these key functions:

#### `login_view` — logs a user in

```python
def login_view(request):
    if request.method == "POST":           # the user clicked "Log In"
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:               # password matched!
            login(request, user)
            if user.is_seller:
                return redirect('seller_page')
            elif user.is_buyer:
                return redirect('buyer_page')
            elif user.is_staff:
                return redirect('admin_page')
        else:
            print('invalid creds...')      # wrong password — see the bug note below
    else:                                  # the user just opened the page
        return render(request, 'login.html')
```

This is the **real** auth flow. It:
1. Reads `username` and `password` from the submitted form.
2. Calls `authenticate()` — Django checks the password hash.
3. Calls `login()` — Django stores the user ID in a session cookie.
4. **Redirects** to the right dashboard based on `is_seller` / `is_buyer` / `is_staff`.

> ⚠️ **Bug to fix later:** when the password is wrong, the function prints a message
> but returns nothing → Django throws a 500 error. The fix is to `return render(...)`
> or `return redirect('login')` after the `print`. (See §10.1.)

#### `user_add` — signs up a seller

```python
def user_add(request):
    form1 = loginform()      # the loginform (username + passwords)
    form2 = sellerform()     # the sellerform (name, email, phone, etc.)
    if request.method == "POST":
        form1 = loginform(request.POST)
        form2 = sellerform(request.POST)
        if form1.is_valid() and form2.is_valid():
            user_data = form1.save(commit=False)  # don't save yet
            user_data.is_seller = True             # mark this user as a seller
            user_data.save()                       # NOW save to the database
            user1 = form2.save(commit=False)       # don't save yet
            user1.user = user_data                 # link seller profile to the user
            user1.save()                           # NOW save to the database
            return redirect('login')              # go to the login page
    return render(request, 'user_add.html', {'form1': form1, 'form2': form2})
```

**The pattern:**
1. Create **two** forms — one for the user account, one for the profile.
2. On `POST`, fill both from `request.POST` (the submitted data).
3. If both are valid: save the user first, set the flag (`is_seller`), then link
   the profile and save it.
4. Redirect to login.

#### `customer_add` — signs up a buyer

This is **identical** to `user_add`, except:
- It uses `buyerform` instead of `sellerform`.
- It sets `user_data.is_buyer = True`.

#### `seller_page`, `buyer_page`, `admin_page`

These are the dashboards shown **after login**:

```python
def seller_page(request):
    return render(request, 'seller/seller_base.html')

def buyer_page(request):
    return render(request, 'buyer/buyer_base.html')

def admin_page(request):
    return render(request, 'admin/admin_base.html')
```

> ⚠️ There are **two** `admin_page` functions in the file. The second one (the
> one that renders `admin/admin_base.html`) wins. The first one (renders `base.html`)
> is dead code. Rename the first one later (see §10.2).

### 4.4 The URLs (`urls.py`)

Every page needs a **URL**. Open `ecom_app/urls.py`:

```python
from django.urls import path
from ecom_app import views, views_admin, views_buyer, views_seller

urlpatterns = [
    path('', views.index, name='index'),              # /         → home
    path('base', views.admin_page, name='base'),      # /base     → Spark Admin dashboard shell
    path('login', views.login_view, name='login'),    # /login    → login
    path('user_add', views.user_add, name='user_add'),# /user_add → seller signup
    path('customer_add', views.customer_add, name='customer_add'), # buyer signup
    path('seller_page', views.seller_page, name='seller_page'),
    path('buyer_page', views.buyer_page, name='buyer_page'),
    path('admin_page', views.admin_page, name='admin_page'),

    # admin-side routes
    path('view_customers', views_admin.view_customers, name='view_customers'),
    path('update_customers/<int:id>', views_admin.update_customers, name='update_customers'),
    path('delete_customers/<int:id>', views_admin.delete_customers, name='delete_customers'),

    # customer (buyer) routes
    path('profile_buyer', views_buyer.profile_view, name='profile_buyer'),

    # seller routes
    path('profile_seller', views_seller.profile_view, name='profile_seller'),
    path('update_seller_profile/<int:id>', views_seller.update_seller_profile, name='update_seller_profile'),
]
```

**Each line means:**
```
path('the url after 127.0.0.1:8000/', which-function-handles-it, name='short-label')
```

The **`name=`** is important — in your HTML you use `{% url 'login' %}` instead of
hard-coding `/login`. This way, if you change the URL later, the link updates
automatically.

The routes fall into three groups:
- **Core** (`/`, `/login`, `/user_add`, `/customer_add`, `/seller_page`, `/buyer_page`, `/admin_page`) — handled by `views.py`.
- **Admin CRUD** (`/view_customers`, `/update_customers/<id>`, `/delete_customers/<id>`) — handled by `views_admin.py`.
- **Profile pages** (`/profile_buyer`, `/profile_seller`, `/update_seller_profile/<id>`) — handled by `views_buyer.py` and `views_seller.py` (covered in Task 5b).

### 4.5 The templates (HTML)

#### `login.html`

A standalone page (own `<head>`, own CSS, own JS). The form posts to itself:

```html
<form action="#" method="post" class="login-form">
  {% csrf_token %}
  <input type="text" id="username" name="username" />
  <input type="password" id="password" name="password" />
  <button type="submit">Log In</button>
</form>
```

- `{% csrf_token %}` is Django's anti-forgery token — **required** on every POST form.
- `name="username"` and `name="password"` are what `login_view` reads.

#### `user_add.html` (seller signup)

```html
{% load crispy_forms_tags %}
<form action="#" method="post" class="signup-form">
  {% csrf_token %}
  {{ form1|crispy }}    {{ form2|crispy }}
  <button type="submit">Sign Up</button>
</form>
```

- `{{ form1|crispy }}` renders the `loginform` with nice Bootstrap markup (thanks to
  `crispy_forms` + `crispy_bootstrap5` from `settings.py`).
- The view passes `form1` and `form2` in a context dictionary.

#### `customer_add.html` (buyer signup)

Same structure, but renders `loginform` + `buyerform`.

### 4.6 Try it end-to-end

With `runserver` running, do this in your browser:

1. Go to <http://127.0.0.1:8000/user_add> — sign up a **seller** (username: `alice`,
   password: `TestP@ss1!`).
2. Go to <http://127.0.0.1:8000/login> — log in as `alice`.
   → You land on <http://127.0.0.1:8000/seller_page> (the seller dashboard).
3. Go to <http://127.0.0.1:8000/customer_add> — sign up a **buyer** (username: `bob`).
4. Log in as `bob` → you land on <http://127.0.0.1:8000/buyer_page>.
5. Log in as your **admin** (from Task 2) → you land on <http://127.0.0.1:8000/admin_page>.

**That's the full signup → login → redirect cycle.** It works.

---

## Task 5 — The admin CRUD (manage buyers in a table)

> Goal: the admin can list, edit, and delete buyers from a table.

### 5.1 The views (`views_admin.py`)

```python
def view_customers(request):
    customers = buyer.objects.all()               # grab every buyer
    return render(request, 'admin/customers.html', {'customers': customers})

def update_customers(request, id):
    customers = buyer.objects.get(id=id)           # find one buyer
    if request.method == "POST":
        form = buyerform(request.POST, instance=customers)
        if form.is_valid():
            form.save()
            return redirect('view_customers')
    else:
        form = buyerform(instance=customers)       # pre-fill with existing data
    return render(request, 'admin/update.html', {'form': form})  # renders the edit form page

def delete_customers(request, id):
    customers = buyer.objects.get(id=id)
    customers.delete()
    return redirect('view_customers')   # ← already fixed! (see §10.3)
```

**Pattern:**
- `view_customers` — `Model.objects.all()` → pass to template → `{% for %}` loop.
- `update_customers` — `Model.objects.get(id=id)` → `Form(instance=obj)` to
  pre-fill → on POST, `Form(request.POST, instance=obj)` → `form.save()`.
- `delete_customers` — `Model.objects.get(id=id)` → `.delete()`.

### 5.2 The URLs

Already wired in `ecom_app/urls.py` (see §4.4):

```python
path('view_customers', views_admin.view_customers, name='view_customers'),
path('update_customers/<int:id>', views_admin.update_customers, name='update_customers'),
path('delete_customers/<int:id>', views_admin.delete_customers, name='delete_customers'),
```

`<int:id>` captures a number from the URL and passes it to the view.

### 5.3 The template (`admin/customers.html`)

```django
{% extends 'admin/admin_base.html' %}
{% block content %}
  <table class="table table-dark">
    <thead>
      <tr>
        <th scope="col">No.</th>
        <th scope="col">Name</th>
        <th scope="col">Email</th>
        <th scope="col">Phone</th>
        <th scope="col">Pincode</th>
        <th scope="col">Address</th>
        <th scope="col" colspan="2">Actions</th>
      </tr>
    </thead>
    <tbody>
    {% for i in customers %}
      <tr>
        <td>{{ forloop.counter }}</td>
        <td>{{ i.name }}</td>
        <td>{{ i.email }}</td>
        <td>{{ i.phone }}</td>
        <td>{{ i.pincode }}</td>
        <td>{{ i.address }}</td>
        <td><a class="btn btn-info" href="{% url 'update_customers' i.id %}">Update</a></td>
        <td><a class="btn btn-danger" href="{% url 'delete_customers' i.id %}" onclick="return confirm('Are you sure you want to delete?');">Delete</a></td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
{% endblock %}
```

- `{% extends 'admin/admin_base.html' %}` — inherits the Spark Admin dashboard shell.
- `<thead>` / `<tbody>` — proper table structure with `table table-dark` Bootstrap classes.
- `{{ forloop.counter }}` — auto-numbered row (1, 2, 3, …).
- `{{ i.name }}`, `{{ i.email }}`, etc. — shows each buyer's fields.
- `<a class="btn btn-info">` / `<a class="btn btn-danger">` — Bootstrap styled buttons.
- `{% url 'update_customers' i.id %}` — builds the URL `/update_customers/3`.
- `onclick="return confirm(...)"` — asks the admin before deleting.

### 5.4 Try it

1. Sign up a few buyers at `/customer_add` (Task 4).
2. Go to <http://127.0.0.1:8000/view_customers> — you see a table of all buyers.
3. Click **Update** → fix a phone number → submit → redirected back to the table.
4. Click **Delete** → the buyer is removed from the table.

---

## Task 5b — Profile pages (buyer view, seller view + edit)

> Goal: after logging in, the user can visit their own profile page and (for
> sellers) edit their profile.

This feature is split across **two new view files** that mirror the CRUD pattern
in `views_admin.py`.

### 5b.1 The buyer profile (`views_buyer.py`)

```python
def profile_view(request):
    userdata = request.user                   # the currently logged-in user
    buyer_user = buyer.objects.get(user=userdata)   # find this user's buyer profile
    return render(request, 'buyer/profile_view_buyer.html', {'buyer_user': buyer_user})
```

- **Pattern:** read `request.user` → look up the matching `buyer` record via the
  `OneToOneField` → pass it to the template.

### 5b.2 The seller profile + edit (`views_seller.py`)

```python
def profile_view(request):
    userdata = request.user
    seller_user = seller.objects.get(user=userdata)
    return render(request, 'seller/profile_view_seller.html', {'seller_user': seller_user})

def update_seller_profile(request, id):
    seller_user = seller.objects.get(id=id)
    if request.method == "POST":
        form = sellerform(request.POST, instance=seller_user)
        if form.is_valid():
            form.save()
            return redirect('profile_seller')     # back to the profile page
    else:
        form = sellerform(instance=seller_user)   # pre-fill with existing data
    return render(request, 'seller/update_seller_profile.html', {'form': form})
```

- `profile_view` is the same pattern as the buyer view — just for `seller`.
- `update_seller_profile` follows the same edit-then-redirect pattern as
  `update_customers` in §5.1: `instance=obj` pre-fills, `form.save()` persists,
  then redirect back to the profile page.

> ⚠️ **Bug to fix later:** `update_seller_profile.html` has a broken URL tag —
> `{% url '' seller_user.id %}` (empty name). It should point to the correct
> route. See §10.10.

### 5b.3 The template — buyer profile (`buyer/profile_view_buyer.html`)

```django
{% extends 'buyer/buyer_base.html' %}
{% block content %}
  <label>Name: {{ buyer_user.name }}</label>
  <label>Email: {{ buyer_user.email }}</label>
  <label>Phone: {{ buyer_user.phone }}</label>
  <label>Pincode: {{ buyer_user.pincode }}</label>
  <label>Address: {{ buyer_user.address }}</label>
{% endblock %}
```

### 5b.4 The template — seller profile (`seller/profile_view_seller.html`)

```django
{% extends 'seller/seller_base.html' %}
{% block content %}
  {{ seller_user }}
  <label>Name: {{ seller_user.name }}</label>
  <label>Email: {{ seller_user.email }}</label>
  <label>Phone: {{ seller_user.phone }}</label>
  <label>Location: {{ seller_user.location }}</label>
  <label>Tax Number: {{ seller_user.tax_number }}</label>
  <a class="btn btn-info" href="{% url 'update_seller_profile' seller_user.id %}">Update</a>
{% endblock %}
```

### 5b.5 The template — seller edit form (`seller/update_seller_profile.html`)

```django
{% extends 'seller/seller_base.html' %}
{% block content %}
  <label> Profile : {{ seller_user }}</label>
  {{ form }}
{% endblock %}
```

> ⚠️ **Bug to fix later:** this template renders `{{ form }}` as raw HTML and has
> no `<form>` tag or submit button. It should wrap `{{ form }}` in a proper
> `<form method="post">` with `{% csrf_token %}`. See §10.10.

### 5b.6 The dashboard shells

All three dashboard base templates (`admin/admin_base.html`, `buyer/buyer_base.html`,
`seller/seller_base.html`) share the **"Spark Admin"** design — a Bootstrap 5
dashboard theme with a sidebar, top navbar, and footer. They are nearly identical;
each extends its role-specific base and fills `{% block content %}`.

The buyer shell links **My Account** → `{% url 'profile_buyer' %}`, and the seller
shell links **My Account** → `{% url 'profile_seller' %}`.

### 5b.7 Try it

1. Sign up a seller at `/user_add`, log in, and get redirected to `/seller_page`.
2. In the seller dashboard's profile dropdown, click **My Account** → you land on
   `/profile_seller` and see your profile.
3. Click **Update** → fill in the form → submit → redirected back to the profile.
4. Sign up a buyer at `/customer_add`, log in → `/buyer_page` → **My Account** →
   `/profile_buyer`.

---

## Task 6 — Django's built-in admin panel (`/admin/`)

You get a professional admin interface **for free**.

Remember in Task 2 you ran `createsuperuser`? That same account logs into Django's
built-in admin at <http://127.0.0.1:8000/admin/>.

`ecom_app/admin.py` registers all three models:

```python
admin.site.register(Login)
admin.site.register(seller)
admin.site.register(buyer)
```

So when you log in to `/admin/` you can add, edit, and delete **Login**, **seller**,
and **buyer** records right from the browser — no code needed.

---

## Task 7 — Make your first small change (and see it live)

> Goal: prove the request → view → template chain by editing text.

1. Keep `runserver` running.
2. Open `templates/login.html`.
3. Find:
   ```html
   <h1 class="login-title">Welcome back</h1>
   ```
4. Change to:
   ```html
   <h1 class="login-title">Welcome back — I edited this!</h1>
   ```
5. Save the file.
6. Refresh <http://127.0.0.1:8000/login>.

You see your new text. ✅

> **Note:** HTML/CSS changes auto-reload. **Python** changes (`.py` files) require
> you to **stop + restart** `runserver`.

---

## Task 8 — Add your own page (build from nothing)

> Goal: a new page at `/about` that you create yourself.

Follow the **4-file recipe** every time:

| Step | File | What to do |
|---|---|---|
| 1 | `templates/about.html` | Write the HTML. |
| 2 | `ecom_app/views.py` | Add `def about(request): return render(request, 'about.html')`. |
| 3 | `ecom_app/urls.py` | Add `path('about', views.about, name='about')`. |
| 4 | (restart `runserver`) | Visit <http://127.0.0.1:8000/about>. |

**Template (`templates/about.html`):**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>About</title>
</head>
<body>
  <h1>About this site</h1>
  <p>Built by following the beginner tutorial.</p>
  <a href="{% url 'index' %}">Back to home</a>
</body>
</html>
```

---

## Task 9 — Common commands (cheat sheet)

Run these from the project root **with `.venv` activated**:

| Command | What it does |
|---|---|
| `python manage.py runserver` | start the dev server (Ctrl+C to stop) |
| `python manage.py migrate` | build/update database tables from `models.py` |
| `python manage.py makemigrations` | tell Django you changed `models.py` |
| `python manage.py createsuperuser` | make an admin account |
| `python manage.py changepassword USER` | reset a user's password |
| `python manage.py shell` | open a Python prompt with Django loaded |
| `python manage.py test` | run `tests.py` |
| `python manage.py showmigrations` | see which tables are built |
| `python manage.py check` | run Django's self-diagnostics |

---

## Task 10 — Things to fix (the bugs a beginner misses)

These are real problems in the code. They don't stop the site from running, but
they will bite you later.

### 10.1 `login_view` returns nothing on bad password

When `authenticate()` returns `None` (wrong password), the function prints a
message and **falls through without returning anything**. Django shows a 500 error.

**Fix:** at the end of the `if request.method == "POST"` block, after the
`else:` branch, add:

```python
    return render(request, 'login.html')   # show login again, with no error message yet
```

### 10.2 Two `admin_page` functions in `views.py`

There are two definitions. The second one wins. Rename the first to
`dashboard_page` and update `urls.py`:

```python
def dashboard_page(request):
    return render(request, 'base.html')
```
```python
path('base', views.dashboard_page, name='base'),
```

### 10.3 `delete_customers` is missing `request`  *(already fixed!)*

The original bug was that `delete_customers` returned `render('admin/customers.html')`
without the `request` object — a crash. The code in `views_admin.py` now correctly
returns:

```python
def delete_customers(request, id):
    customers = buyer.objects.get(id=id)
    customers.delete()
    return redirect('view_customers')
```

No action needed — this one is already fixed.

### 10.4 `MAILERS` is not a real Django setting

In `settings.py` the email configuration uses `MAILERS` (the syntax from the
`django-mailer` package), but Django's built-in email system ignores it:

```python
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    }
}
```

Django expects a top-level `EMAIL_BACKEND` setting instead. Change to:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### 10.5 No `requirements.txt`

To make the project reproducible on another machine:

```powershell
python -m pip freeze > requirements.txt
```

Then on a new machine:
```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
> Don't forget `psycopg2-binary` and `crispy-bootstrap5`.

### 10.6 No `.gitignore` at the project root

Add a file `E_Commerce_RE/.gitignore`:
```
__pycache__/
*.pyc
*.pyo
.venv/
*.sqlite3
```

### 10.7 Broken links in `index.html`

The navbar uses `{% static 'index.html' %}`, `{% static 'properties.html' %}`, etc.
— those files don't exist. They produce 404s. Change them to real URLs or remove them.

### 10.8 Missing `favicon.png`

`login.html` and `index.html` reference `{% static 'favicon.png' %}` but the file
doesn't exist. Either add one to `static/` or remove the `<link rel="shortcut icon">` line.

### 10.9 Unused / incorrect imports in `views.py`

At the top of `ecom_app/views.py`:

```python
from urllib import request            # ← wrong — `urllib.request` is a stdlib module, not a Django request
from django.core.mail import message   # ← wrong — `message` is not exported from django.core.mail
```

Neither is used anywhere in the file. They won't crash the app (Python just loads
unused names), but they are misleading. Remove both lines.

### 10.10 `update_seller_profile.html` is missing a `<form>` wrapper

The template in `templates/seller/update_seller_profile.html` renders `{{ form }}`
as raw HTML with no `<form>` tag, no `{% csrf_token %}`, and no submit button.
Additionally, the Save link uses a broken URL tag: `{% url '' seller_user.id %}`
(empty name → `NoReverseMatch`).

**Fix:** wrap the form properly:

```django
{% extends 'seller/seller_base.html' %}
{% block content %}
  <form method="post">
    {% csrf_token %}
    {{ form }}
    <button type="submit">Save</button>
  </form>
{% endblock %}
```

---

## Task 11 — Where to go next

Now you understand every piece. Here is the logical next step for each part:

1. **Models** — add a `Product` model, run `makemigrations` + `migrate`, register it
   in `admin.py`.
2. **Views** — make the buyer/seller dashboards show real data (products, orders,
   etc.) instead of being empty shells. Add profile pages for buyers (mirror the
   seller pattern in `views_buyer.py`).
3. **Templates** — make `login.html` extend `base.html` so all pages share the same
   header/footer. Fix the broken links in `index.html`. Finish the
   `update_seller_profile.html` form (§10.10).
4. **Forms** — add search / filter / pagination to `view_customers`.
5. **Auth** — add password reset emails (fix the `EMAIL_BACKEND` setting first).
6. **Profiles** — add login-required decorators (`@login_required`) to the profile
   views so anonymous users can't access them. Add a logout view.
7. **Testing** — write a test in `tests.py` that signs up a user and logs in.
8. **Deployment** — set `DEBUG = False`, add `ALLOWED_HOSTS`, and serve with
   Gunicorn behind Nginx. (Different topic.)

---

## Quick restart checklist

Every time you come back to work:

```powershell
Set-Location "C:\Users\Faizy\PycharmProjects\E_Commerce_RE"
. .venv\Scripts\Activate.ps1
python manage.py runserver
```

Then open <http://127.0.0.1:8000/>.
