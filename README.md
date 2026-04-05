# Documentation for Inter Store

Django Web application for managing products and customer orders.

## Idea
Inter Store started as an Inventory management system and expanded to an online store. Main task is to have full functionality and options for an online store.

## Run the project
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
### 🌐 Open
```
http://13.51.236.3/
```
---
### ⚠️ Important
Project requires .env file. SendGrid credentials are required for emails. 
Without them, password reset and email features will not work.
---

## Environment variables
Setup .env file

Create a `.env` file in the root directory and copy the following variables:
Default values are set to "" for SendGrid credentials if you don't have profile.

```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=13.51.236.3,127.0.0.1,localhost
DB_NAME=inter_store
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=your_sendgrid_email
SENDGRID_CHANGE_PASSWORD_TEMPLATE=your_change_password_template
SENDGRID_ORDER_CONFIRMATION_TEMPLATE=your_order_confirmation_template
SENDGRID_REGISTER_TEMPLATE=your_register_template
```
```
Admin test account:
inter_admin@gmail.com
12345interadmin
```
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
