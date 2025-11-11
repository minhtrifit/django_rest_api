## Run server

```console
python manage.py runserver 5000
```

## Load seed data

```console
python manage.py loaddata products
```

## Migration

```console
python manage.py makemigrations
python manage.py migrate
```

## API List

- [Get List of Categories](#1-get-list-of-categories)
- [Create a Category](#2-create-a-category)
- [Update a Category](#3-update-a-category)

---

- [Get List of Products](#4-get-list-of-products)
- [Get Product Details](#5-get-product-details)
- [Create a Product](#6-create-a-product)
- [Update a Product](#7-update-a-product)

---

- [Create user](#8-create-user)
- [Login](#9-login)
- [Get user profile](#10-get-user-profile)

---

- [Get payment methods](#11-get-payment-methods)
- [Create payment method](#12-create-payment-method)

---

- [Get List of orders](#13-get-list-of-orders)
- [Get Order Details](#14-get-order-details)
- [Create order](#15-create-order)
- [Update order](#16-update-order)

## 1. Get List of Categories

**Endpoint:** `[GET] http://localhost:5000/categories`

**Query Parameters:**
| Parameter | Type | Description | Value |
|-----------|------|-------------|---------|
| is_active | boolean | Filter categories by is_active (optional) | true/false |

## 2. Create a Category

**Endpoint:** `[POST] http://localhost:5000/categories/create`

**Request body:**

```json
{
  "name": "Energy food"
}
```

## 3. Update a Category

**Endpoint:** `[PATCH] http://localhost:5000/categories/update/{id}`

**Request body:**

```json
{
  "name": "Energy food",
  "is_active": true
}
```

## 4. Get List of Products

**Endpoint:** `[GET] http://localhost:5000/products`

**Query Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| page | int | Page number for pagination | 1 |
| limit | int | Number of items per page | 10 |
| q | str | Filter products by name (optional) | - |

## 5. Get Products Details

**Endpoint:** `[GET] http://localhost:5000/products/detail/{id}`

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | UUID | PUnique ID of the product |

## 6. Create a Product

**Endpoint:** `[POST] http://localhost:5000/products/create`

**Request body:**

```json
{
  "name": "Bánh ngọt vị dâu",
  "price": 55000000,
  "description": "Dành cho người nhớn",
  "category_ids": [
    "22222222-2222-2222-2222-222222222222", // Snacks
    "99999999-9999-9999-9999-999999999999" // Bakery
  ]
}
```

## 7. Update a Product

**Endpoint:** `[PATCH] http://localhost:5000/products/update/{id}`

**Request body:**

```json
{
  "name": "Bánh ngọt vị dâu",
  "price": 55000000,
  "description": "Dành cho người nhớn",
  "category_ids": [
    "22222222-2222-2222-2222-222222222222", // Snacks
    "99999999-9999-9999-9999-999999999999" // Bakery
  ],
  "is_active": false
}
```

## 8. Create user

**Endpoint:** `[POST] http://localhost:5000/auth/register`

**Request body:**

```json
{
  "username": "minhtri",
  "password": "123",
  "name": "Lê Minh Trí"
}
```

## 9. Login

**Endpoint:** `[POST] http://localhost:5000/auth/login`

**Request body:**

```json
{
  "username": "minhtri",
  "password": "123"
}
```

## 10. Get user profile

**Endpoint:** `[POST] http://localhost:5000/auth/profile`

**Request header:**

```json
{
  "Authorization": "Bearer login_token"
}
```

## 11. Get payment methods

**Endpoint:** `[GET] http://localhost:5000/payment_methods`

**Query Parameters:**
| Parameter | Type | Description | Value |
|-----------|------|-------------|---------|
| is_active | boolean | Filter categories by is_active (optional) | true/false |

## 12. Create payment method

**Endpoint:** `[POST] http://localhost:5000/payment_methods/create`

**Request header:**

```json
{
  "Authorization": "Bearer login_token"
}
```

**Request body:**

```json
{
  "key": "installment",
  "name": "Trả góp"
}
```

## 13. Get List of Orders

**Endpoint:** `[GET] http://localhost:5000/orders`

**Query Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| page | int | Page number for pagination | 1 |
| limit | int | Number of items per page | 10 |
| status | str | Filter orders by status (optional) | pending/paid/shipped/completed/canceled |
| payment_method | str | Filter orders by payment method (optional) | - |

## 14. Get Order Details

**Endpoint:** `[GET] http://localhost:5000/orders/detail/{id}`

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | UUID | PUnique ID of the order |

## 15. Create order

**Endpoint:** `[POST] http://localhost:5000/orders/create`

**Request header:**

```json
{
  "Authorization": "Bearer login_token"
}
```

**Request body:**

```json
{
  "user_id": "a563a31d-d802-4e15-94b6-1447cc2b87cb",
  "payment_method": "11111111-1111-1111-1111-111111111111",
  "note": "Bấm chuông khi giao hàng",
  "items": [
    { "product": "00000006-0000-0000-0000-000000000006", "quantity": 3 },
    { "product": "0000000e-0000-0000-0000-00000000000e", "quantity": 5 },
    { "product": "00000013-0000-0000-0000-000000000013", "quantity": 7 }
  ]
}
```

## 16. Update a Order

**Endpoint:** `[PATCH] http://localhost:5000/orders/update/{id}`

**Request header:**

```json
{
  "Authorization": "Bearer login_token"
}
```

**Request body:**

```json
{
  "status": "shipped",
  "payment_method": "33333333-3333-3333-3333-333333333333",
  "note": "Gửi kèm quà",
  "items": [
    { "product": "00000006-0000-0000-0000-000000000006", "quantity": 1 },
    { "product": "0000000e-0000-0000-0000-00000000000e", "quantity": 2 }
  ]
}
```
