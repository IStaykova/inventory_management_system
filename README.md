# Documentation for Inter Store

Django Web application for managing products and customer orders.

## Idea
Inter Store started as an Inventory management system and expanded to an online store. Main task is to have full functionality and options for an online store.

## Run the project

```
Admin test account:
inter_admin@gmail.com
12345interadmin
```
### 🌐 Open
```
http://13.51.236.3/
```
- Windows
```
git clone https://github.com/IStaykova/inventory_management_system
cd inventory_management_system
```
create .env and add your variables → see [Environment variables](#environment-variables)
```
vim .env
or
notepad .env

## When ready → ESC → :wq → Enter
```
Continue with Docker setup
```
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```
---
### ⚠️ Important
- Project requires .env file. SendGrid credentials are required for emails. 
Without them, password reset and email features will not work. Credentials are provided for test usage only.
---

## Environment variables
Setup .env file

Create an `.env` file in the root directory and copy the following variables:

```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=13.51.236.3,127.0.0.1,localhost
DB_NAME=inter_store
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=inter_store_db
DB_PORT=5432
SENDGRID_API_KEY=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
SENDGRID_FROM_EMAIL=i_staykova@abv.bg
SENDGRID_CHANGE_PASSWORD_TEMPLATE=d-04d956cfe2eb43848f5918379fdf17b3
SENDGRID_ORDER_CONFIRMATION_TEMPLATE=d-ea9892bc866b4100b0e0cd0a746ab38b
```
---
## Features
### User - Authentication and authorization
- Register/ login + permissions
- Password change
- User profile
- Email functionality for registration and password reset

### Product management
- Products catalog and search form
- Products details page, reviews
- Products create/ edit/ delete functionality (admin)

### Order management
- Cart functionality
- Create and manage orders
- Stock validation
- Change order status (admin)

### Review management
- Product reviews create/ edit/ delete (owner)
- Reviews list page + average rating functionality

### Error Handling
- Custom 404 page
- User-friendly validation messages
---
