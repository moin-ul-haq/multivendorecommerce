API USAGE GUIDE - Multi-Vendor E-Commerce

=== AUTHENTICATION ===
All endpoints require authentication via Token (except /register and /login).

1) REGISTER (create account):
   POST /api/register/
   Body:
   {
     "username": "john",
     "password": "pass123",
     "name": "John Doe",
     "age": 25,
     "email": "john@example.com",
     "address": "123 Main St",
     "role": "customer"
   }
   Response: User data + auto-created token

2) LOGIN (get token):
   POST /api/login/
   Body:
   {
     "username": "john",
     "password": "pass123"
   }
   Response:
   {
     "token": "abc123xyz",
     "user": {...}
   }
   Use this token for all requests: Header: Authorization: Token abc123xyz

=== CART WORKFLOW ===

Step 1: GET YOUR CART
   GET /api/carts/
   Headers: Authorization: Token YOUR_TOKEN
   Response: Your cart with all items, total, count

Step 2: ADD PRODUCT TO CART
   POST /api/carts/add/{product_slug}/
   Headers: Authorization: Token YOUR_TOKEN
   (product_slug is auto-generated from product name, e.g., "iphone-15")
   Response: Updated cart

   Example:
   POST /api/carts/add/iphone-15/

Step 3: INCREASE QUANTITY
   POST /api/carts/increase/{product_slug}/
   Headers: Authorization: Token YOUR_TOKEN
   Response: Updated cart

Step 4: DECREASE QUANTITY
   POST /api/carts/decrease/{product_slug}/
   Headers: Authorization: Token YOUR_TOKEN
   Response: Updated cart

Step 5: REMOVE ITEM
   DELETE /api/carts/remove/{product_slug}/
   Headers: Authorization: Token YOUR_TOKEN
   Response: Updated cart

Step 6: CLEAR CART
   POST /api/carts/clear/
   Headers: Authorization: Token YOUR_TOKEN
   Response: {"detail": "cart cleared"}

=== CHECKOUT WORKFLOW ===

After adding items to cart, checkout:

   POST /api/checkout/
   Headers: Authorization: Token YOUR_TOKEN
   Body (optional - default city is Bahawalpur):
   {
     "shipping": {
       "City": "Karachi",
       "Address": "123 Main St",
       "Country": "Pakistan"
     }
   }
   Response: Order object with order ID
   {
     "id": 5,
     "user": 2,
     "status": "pending",
     "total_amount": "5000.00",
     "shipping": {...},
     "items": [...]
   }

*** IMPORTANT: Checkout creates Payment record automatically via signal ***

=== PAYMENT (STRIPE) WORKFLOW ===

Step 1: GET PAYMENT (created during checkout)
   GET /api/payments/{payment_id}/
   Headers: Authorization: Token YOUR_TOKEN
   Response: Payment object with status

Step 2: GET STRIPE CHECKOUT SESSION URL
   POST /api/payments/{payment_id}/stripe/
   Headers: Authorization: Token YOUR_TOKEN
   Response:
   {
     "checkout_url": "https://checkout.stripe.com/pay/cs_..."
   }
   Redirect user to this URL to pay with card

Step 3: USER COMPLETES PAYMENT ON STRIPE
   (User fills card details on Stripe)

Step 4: CONFIRM PAYMENT SUCCESS (after user returns)
   POST /api/payments/{payment_id}/success/
   Headers: Authorization: Token YOUR_TOKEN
   Response: Payment object with status="confirmed"
   This updates order status to "confirmed" and sends email notification

Step 5: IF PAYMENT CANCELLED
   POST /api/payments/{payment_id}/cancel/
   Headers: Authorization: Token YOUR_TOKEN
   Response: Payment reverted to pending

=== PAYPAL WORKFLOW (Similar to Stripe) ===

   POST /api/payments/{payment_id}/paypal/
   Headers: Authorization: Token YOUR_TOKEN
   Response:
   {
     "checkout_url": "https://www.paypal.com/checkoutnow?invoice_id=..."
   }

=== ORDER TRACKING ===

GET YOUR ORDERS:
   GET /api/orders/
   Headers: Authorization: Token YOUR_TOKEN
   Response: List of all user orders

GET SPECIFIC ORDER:
   GET /api/orders/{order_id}/
   Headers: Authorization: Token YOUR_TOKEN
   Response: Order details with items

UPDATE ORDER STATUS (admin only):
   PATCH /api/orders/{order_id}/status/
   Headers: Authorization: Token YOUR_TOKEN
   Body: {"status": "shipped"}
   Statuses: pending, confirmed, shipped, delivered

=== PRODUCTS & STORES ===

LIST ALL PRODUCTS:
   GET /api/products/
   Headers: Authorization: Token YOUR_TOKEN
   Query params: ?store=1&catagory=2 (optional)

GET PRODUCT DETAIL (by slug):
   GET /api/products/{product_slug}/
   Headers: Authorization: Token YOUR_TOKEN

LIST ALL STORES:
   GET /api/stores/

GET STORE DETAIL (by slug):
   GET /api/stores/{store_slug}/

ADD REVIEW:
   POST /api/reviews/
   Headers: Authorization: Token YOUR_TOKEN
   Body:
   {
     "product": 5,
     "rating": 4,
     "review": "Great product!"
   }

=== PAYOUT (Admin Only) ===

LIST PAYOUTS:
   GET /api/payouts/
   Headers: Authorization: Token YOUR_TOKEN
   (Returns all payouts for admin, only owner payouts for vendors)

UPDATE PAYOUT STATUS:
   PATCH /api/payouts/{payout_id}/status/
   Headers: Authorization: Token YOUR_TOKEN (admin only)
   Body: {"status": "paid"}
   Statuses: pending, paid, failed

=== COMPLETE FLOW EXAMPLE (cURL) ===

# 1. Login
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "pass123"}'

# Get token from response, e.g., "abc123xyz"

# 2. Get cart
curl -X GET http://localhost:8000/api/carts/ \
  -H "Authorization: Token abc123xyz"

# 3. Add product to cart (product must exist in store)
curl -X POST http://localhost:8000/api/carts/add/iphone-15/ \
  -H "Authorization: Token abc123xyz"

# 4. Checkout
curl -X POST http://localhost:8000/api/checkout/ \
  -H "Authorization: Token abc123xyz" \
  -H "Content-Type: application/json" \
  -d '{"shipping": {"City": "Karachi"}}'

# Get payment_id from order response, e.g., payment_id=3

# 5. Get Stripe URL
curl -X POST http://localhost:8000/api/payments/3/stripe/ \
  -H "Authorization: Token abc123xyz"

# Get checkout_url, open in browser for user to pay

# 6. Confirm payment
curl -X POST http://localhost:8000/api/payments/3/success/ \
  -H "Authorization: Token abc123xyz"

=== ENVIRONMENT VARIABLES NEEDED ===

Create .env file in project root:

STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_API_KEY=pk_test_...
BACKEND_DOMAIN=http://localhost:8000
PAYMENT_SUCCESS_URL=http://localhost:3000/payment/success
PAYMENT_CANCEL_URL=http://localhost:3000/payment/cancel
DEFAULT_FROM_EMAIL=noreply@daraz.local
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
PAYPAL_CHECKOUT_URL=https://www.paypal.com/checkoutnow

=== ENDPOINTS SUMMARY ===

API Root: /api/
All Endpoints List: /api/endpoints/

Authentication:
  POST /api/register/
  POST /api/login/
  GET /api/profile/

Cart:
  GET /api/carts/
  POST /api/carts/add/{slug}/
  DELETE /api/carts/remove/{slug}/
  POST /api/carts/increase/{slug}/
  POST /api/carts/decrease/{slug}/
  POST /api/carts/clear/

Orders & Checkout:
  POST /api/checkout/
  GET /api/orders/
  GET /api/orders/{id}/
  PATCH /api/orders/{id}/status/

Payments:
  GET /api/payments/
  GET /api/payments/{id}/
  POST /api/payments/{id}/stripe/
  POST /api/payments/{id}/paypal/
  POST /api/payments/{id}/success/
  POST /api/payments/{id}/cancel/

Payouts:
  GET /api/payouts/
  PATCH /api/payouts/{id}/status/

Store & Products:
  GET /api/stores/
  GET /api/stores/{slug}/
  GET /api/catagories/
  GET /api/catagories/{slug}/
  GET /api/products/
  GET /api/products/{slug}/
  GET /api/reviews/
  POST /api/reviews/

Vendors:
  GET /api/vendors/
