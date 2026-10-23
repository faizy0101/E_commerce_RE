# Beginner Tutorial: E-Commerce Django Project

This tutorial walks through the E-Commerce Django project task by task, chapter by chapter, sorted by creation order and difficulty (low to high).

## Project Overview

A Django-based e-commerce platform with three user roles:
- **Admin** - manages customers, views all data
- **Seller** - creates and manages products
- **Buyer** - browses products, adds to cart, and checks out

## Directory Structure

- ecom/ - Django project configuration (settings, urls, wsgi)
- ecom_app/ - main application (models, views, forms, urls, migrations)
- 	emplates/ - HTML templates for all user roles
- static/ - CSS, JS, images
- media/ - uploaded product images
- db.sqlite3 - SQLite database (PostgreSQL config is commented out)

## Chapters (sorted by difficulty - lowest first)

## Chapter 1: Project Setup & Django Configuration (Difficulty: Low)

### What you will learn
- How to set up a Django project
- Configure project settings
- Set up database and static/media files

### Files involved
- ecom/settings.py
- manage.py
- main.py

### Key concepts
- Django project structure
- Settings: SECRET_KEY, DEBUG, ALLOWED_HOSTS, INSTALLED_APPS
- Database configuration (PostgreSQL or SQLite)
- Static files (STATIC_URL, STATICFILES_DIRS)
- Media files (MEDIA_URL, MEDIA_ROOT)

### Step by step
1. Create a new Django project using django-admin startproject ecom
2. Edit ecom/settings.py to configure your database
3. Set up static and media file paths
4. Add your app to INSTALLED_APPS
5. Run migrations with python manage.py migrate
6. Start the server with python manage.py runserver

### Code references
- ecom/settings.py:33-43 - INSTALLED_APPS list
- ecom/settings.py:79-94 - Database configuration
- ecom/settings.py:128-135 - Static and media files

---

## Chapter 2: User Model & Authentication (Difficulty: Low-Medium)

### What you will learn
- Create a custom user model
- Create user registration forms
- Implement login/logout functionality

### Files involved
- ecom_app/models.py - Login model
- ecom_app/forms.py - loginform, buyerform, sellerform
- ecom_app/views.py - login_view, logout_view, user_add, customer_add
- 	emplates/login.html
- 	emplates/user_add.html
- 	emplates/customer_add.html

### Key concepts
- AbstractUser for custom user model
- UserCreationForm for registration
- authenticate() and login() for authentication
- Role-based user (is_seller, is_buyer)

### Step by step
1. Create Login model extending AbstractUser in models.py:5
2. Add is_seller and is_buyer boolean fields
3. Create forms in orms.py:8-29
4. Implement login_view in iews.py:19-36
5. Create user_add view for seller registration in iews.py:52-66
6. Create customer_add view for buyer registration in iews.py:68-82
7. Create login.html template
8. Create signup templates for both roles

### Code references
- ecom_app/models.py:5-8 - Login model
- ecom_app/forms.py:8-11 - loginform
- ecom_app/views.py:19-36 - login_view
- ecom_app/views.py:52-66 - user_add (seller)
- ecom_app/views.py:68-82 - customer_add (buyer)

---

## Chapter 3: Database Models - Core Entities (Difficulty: Medium)

### What you will learn
- Design database models for e-commerce
- Define relationships between models
- Create and apply migrations

### Files involved
- `ecom_app/models.py`
- `ecom_app/migrations/0001_initial.py` through `0006_cart_quantity.py`

### Key concepts
- OneToOneField, ForeignKey
- Model field types (CharField, EmailField, DecimalField, ImageField)
- Migration workflow
- Model __str__ method

### Step by step
1. Create Login model (Chapter 2 already covers this)
2. Create buyer model in models.py:10-18 with OneToOneField to Login
3. Create seller model in models.py:20-28 with OneToOneField to Login
4. Create product model in models.py:31-38 with ForeignKey to seller
5. Run `python manage.py makemigrations` and `python manage.py migrate`
6. Later add cart model in models.py:40-43
7. Add quantity field to cart via migration 0006_cart_quantity.py

### Model Relationships
- Login 1-to-1 -> buyer
- Login 1-to-1 -> seller
- seller 1-to-many -> product
- buyer 1-to-many -> cart
- product 1-to-many -> cart

### Code references
- `ecom_app/models.py:10-18` - buyer model
- `ecom_app/models.py:20-28` - seller model
- `ecom_app/models.py:31-38` - product model
- `ecom_app/models.py:40-43` - cart model
- `ecom_app/migrations/0001_initial.py` - initial migrations
- `ecom_app/migrations/0002_product.py` - product model added
- `ecom_app/migrations/0003_product_product_image.py` - image field added
- `ecom_app/migrations/0004_cart.py` - cart model created
- `ecom_app/migrations/0005_remove_cart_seller_cart_buyer.py` - cart buyer added
- `ecom_app/migrations/0006_cart_quantity.py` - quantity field added

---

## Chapter 4: Django Forms (Difficulty: Medium)

### What you will learn
- Create ModelForms for different user roles
- Use crispy-forms for better rendering
- Handle form validation and file uploads

### Files involved
- `ecom_app/forms.py`
- Templates that render forms

### Key concepts
- ModelForm vs Form
- exclude fields from form
- crispy_forms rendering
- FileField and ImageField handling

### Step by step
1. Create loginform in forms.py:8-11 (UserCreationForm)
2. Create buyerform in forms.py:13-17 (ModelForm, exclude user)
3. Create sellerform in forms.py:19-23 (ModelModel, exclude user)
4. Create productform in forms.py:25-29 (ModelForm, exclude seller)
5. Load crispy_forms_tags in templates
6. Render forms with `{{ form|crispy }}`

### Code references
- `ecom_app/forms.py:8-11` - loginform
- `ecom_app/forms.py:13-17` - buyerform
- `ecom_app/forms.py:19-23` - sellerform
- `ecom_app/forms.py:25-29` - productform
- `templates/user_add.html:185-188` - form rendering
- `templates/customer_add.html:185-188` - form rendering

---

## Chapter 5: URL Routing & Views Structure (Difficulty: Medium)

### What you will learn
- Organize views by user role
- Set up URL patterns
- Create view functions for each page

### Files involved
- `ecom_app/urls.py`
- `ecom_app/views.py`
- `ecom_app/views_buyer.py`
- `ecom_app/views_seller.py`
- `ecom_app/views_admin.py`

### Key concepts
- path() with parameters
- URL namespacing
- View separation by role
- redirect() vs render()

### Step by step
1. Set up main urls in ecom/urls.py:22-25 to include app urls
2. Create app urls in ecom_app/urls.py:5-41
3. Create base views in views.py:12-84 (index, login, register)
4. Create buyer views in views_buyer.py:6-86
5. Create seller views in views_seller.py:8-61
6. Create admin views in views_admin.py:7-26

### URL Structure
- `ecom_app/urls.py:6` - index (home page)
- `ecom_app/urls.py:8-10` - login/logout
- `ecom_app/urls.py:18-20` - admin customer management
- `ecom_app/urls.py:24-31` - buyer features
- `ecom_app/urls.py:34-40` - seller features

### Code references
- `ecom_app/urls.py:5-41` - all URL patterns
- `ecom_app/views.py:12-84` - base views
- `ecom_app/views_buyer.py:6-86` - buyer views
- `ecom_app/views_seller.py:8-61` - seller views
- `ecom_app/views_admin.py:7-26` - admin views

---

## Chapter 6: Seller Features - Product Management (Difficulty: Medium-High)

### What you will learn
- Create, read, update, delete products
- Handle file uploads
- Filter products by seller
- Build seller dashboard

### Files involved
- `ecom_app/views_seller.py`
- `templates/seller/` templates

### Key concepts
- CRUD operations
- request.FILES for image upload
- commit=False for setting foreign keys
- Filtering querysets

### Step by step
1. Create profile_view in views_seller.py:8-11 to show seller profile
2. Create update_seller_profile in views_seller.py:14-23 for profile editing
3. Create product_create in views_seller.py:26-38 to add products
4. Create product_view in views_seller.py:40-44 to list seller's products
5. Create product_update in views_seller.py:47-56 to edit products
6. Create product_delete in views_seller.py:58-61 to remove products
7. Create templates: seller_base.html, add_product.html, product_view.html, product_update.html, profile_view_seller.html, update_seller_profile.html

### Code references
- `ecom_app/views_seller.py:8-11` - profile_view
- `ecom_app/views_seller.py:14-23` - update_seller_profile
- `ecom_app/views_seller.py:26-38` - product_create
- `ecom_app/views_seller.py:40-44` - product_view
- `ecom_app/views_seller.py:47-56` - product_update
- `ecom_app/views_seller.py:58-61` - product_delete

---

## Chapter 7: Buyer Features - Shopping Cart (Difficulty: Medium-High)

### What you will learn
- Implement shopping cart functionality
- Add/remove items from cart
- Update item quantities
- Calculate totals

### Files involved
- `ecom_app/views_buyer.py`
- `templates/buyer/` templates

### Key concepts
- Session-based cart vs database cart
- Foreign key relationships
- Aggregation and calculations
- Redirect after actions

### Step by step
1. Create Cart view in views_buyer.py:20-28 to add items to cart
2. Create Cart_view in views_buyer.py:32-44 to display cart and calculate total
3. Create product_delete_from_cart in views_buyer.py:46-49 to remove items
4. Create increase_quantity in views_buyer.py:51-58 to increment quantity
5. Create decrease_quantity in views_buyer.py:60-65 to decrement quantity
6. Create templates: product_base.html, product_card_list.html, cart_page.html, open_product_page.html

### Cart Logic
- Cart items stored in database with buyer, product, quantity
- Total calculated by iterating cart items
- Quantity validation against product stock

### Code references
- `ecom_app/views_buyer.py:20-28` - Cart (add to cart)
- `ecom_app/views_buyer.py:32-44` - Cart_view
- `ecom_app/views_buyer.py:46-49` - product_delete_from_cart
- `ecom_app/views_buyer.py:51-58` - increase_quantity
- `ecom_app/views_buyer.py:60-65` - decrease_quantity
- `templates/buyer/cart_page.html:1-133` - cart display

---

## Chapter 8: Buyer Features - Product Browsing & Checkout (Difficulty: Medium)

### What you will learn
- Display products in a grid
- Create product detail pages
- Implement checkout flow

### Files involved
- `ecom_app/views_buyer.py`
- `templates/buyer/` templates

### Key concepts
- QuerySet filtering
- Detail views with URL parameters
- Checkout flow

### Step by step
1. Create profile_view in views_buyer.py:6-9 for buyer profile
2. Create product_view_buyer in views_buyer.py:12-14 to list all products
3. Create open_product in views_buyer.py:16-18 for product details
4. Create checkout in views_buyer.py:68-86 (currently incomplete)
5. Create templates: profile_view_buyer.html, product_card_list.html, open_product_page.html, checkout.html

### Code references
- `ecom_app/views_buyer.py:6-9` - profile_view
- `ecom_app/views_buyer.py:12-14` - product_view_buyer
- `ecom_app/views_buyer.py:16-18` - open_product
- `ecom_app/views_buyer.py:68-86` - checkout (incomplete)
- `templates/buyer/product_card_list.html:1-75` - product grid
- `templates/buyer/open_product_page.html:1-84` - product detail

---

## Chapter 9: Admin Features - Customer Management (Difficulty: Medium)

### What you will learn
- Build admin dashboard
- View all customers
- Update and delete customer records

### Files involved
- `ecom_app/views_admin.py`
- `templates/admin/` templates

### Key concepts
- Admin-only access
- List views with iteration
- Update and delete patterns

### Step by step
1. Create view_customers in views_admin.py:7-9 to list all customers
2. Create update_customers in views_admin.py:11-20 to edit customer
3. Create delete_customers in views_admin.py:22-25 to remove customer
4. Create templates: admin_base.html, customers.html, update.html

### Code references
- `ecom_app/views_admin.py:7-9` - view_customers
- `ecom_app/views_admin.py:11-20` - update_customers
- `ecom_app/views_admin.py:22-25` - delete_customers
- `templates/admin/customers.html:1-33` - customer list
- `templates/admin/update.html:1-12` - update form

---

## Chapter 10: Templates & UI (Difficulty: Medium)

### What you will learn
- Create base templates for each role
- Use template inheritance
- Render dynamic data
- Use static files and Bootstrap

### Files involved
- All files in `templates/` directory

### Key concepts
- Template inheritance with {% extends %}
- {% block %} for content injection
- Django template language
- Static files with {% load static %}
- Bootstrap 5 styling

### Step by step
1. Create base templates for each role:
   - `templates/index.html` - home page
   - `templates/login.html` - login page
   - `templates/admin/admin_base.html` - admin base
   - `templates/seller/seller_base.html` - seller base
   - `templates/buyer/product_base.html` - buyer base
2. Create child templates extending base templates:
   - `templates/buyer/product_card_list.html`
   - `templates/buyer/open_product_page.html`
   - `templates/buyer/cart_page.html`
   - `templates/buyer/profile_view_buyer.html`
   - `templates/buyer/checkout.html`
   - `templates/seller/add_product.html`
   - `templates/seller/product_view.html`
   - `templates/seller/product_update.html`
   - `templates/seller/profile_view_seller.html`
   - `templates/admin/customers.html`
   - `templates/admin/update.html`
3. Create registration templates:
   - `templates/user_add.html` (seller signup)
   - `templates/customer_add.html` (buyer signup)

### Code references
- `templates/index.html:1-1046` - home page
- `templates/login.html:1-277` - login page
- `templates/admin/admin_base.html:1-641` - admin base
- `templates/seller/seller_base.html:1-641` - seller base
- `templates/buyer/product_base.html:1-110` - buyer base
- `templates/buyer/product_card_list.html:1-75` - product grid
- `templates/buyer/open_product_page.html:1-84` - product detail
- `templates/buyer/cart_page.html:1-133` - cart page
- `templates/buyer/profile_view_buyer.html:1-11` - buyer profile
- `templates/buyer/checkout.html:1-8` - checkout page
- `templates/seller/add_product.html:1-16` - add product form
- `templates/seller/product_view.html:1-41` - product list
- `templates/seller/product_update.html:1-12` - update form
- `templates/seller/profile_view_seller.html:1-14` - seller profile
- `templates/admin/customers.html:1-33` - customer list
- `templates/admin/update.html:1-12` - update form
- `templates/user_add.html:1-212` - seller signup
- `templates/customer_add.html:1-212` - buyer signup

---

