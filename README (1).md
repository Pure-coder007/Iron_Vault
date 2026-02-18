# IronVault API

IronVault is a robust digital wallet and mini banking backend built with
FastAPI.

It simulates core financial operations such as transfers, deposits,
withdrawals, savings vaults, and administrative controls.

Every new user receives **100,000** in starting balance upon
registration.

------------------------------------------------------------------------

## Features

-   JWT Authentication (Access & Refresh Tokens)
-   Email Verification
-   Password Reset Flow
-   Wallet Transfers (Atomic Transactions)
-   Savings Vault with Lock Period & Interest
-   Transaction History with Filters & Pagination
-   Admin Controls (Freeze Accounts, Reverse Transactions)
-   Audit Logs
-   Background Email Notifications
-   Dockerized Setup
-   Unit Tested Endpoints
-   Database Migrations (Alembic)

------------------------------------------------------------------------

## Tech Stack

-   FastAPI
-   PostgreSQL
-   SQLAlchemy
-   Alembic
-   Pydantic
-   Pytest
-   Docker
-   Mailtrap (Development Email Testing)

------------------------------------------------------------------------

## Project Structure

    ironvault/
     ├── app/
     │   ├── main.py
     │   ├── config.py
     │   ├── database.py
     │   ├── models.py
     │   ├── schemas.py
     │   ├── oauth2.py
     │   ├── utils.py
     │   ├── email_utils.py
     │   ├── services/
     │   │     ├── wallet_service.py
     │   │     ├── savings_service.py
     │   │     └── transaction_service.py
     │   └── routers/
     │         ├── auth.py
     │         ├── wallet.py
     │         ├── savings.py
     │         ├── admin.py
     │         └── transactions.py
     ├── tests/
     ├── Dockerfile
     ├── docker-compose.yml
     ├── alembic/
     ├── requirements.txt
     └── README.md

------------------------------------------------------------------------

## Getting Started

### 1. Clone Repository

    git clone https://github.com/yourusername/ironvault.git
    cd ironvault

### 2. Create .env File

    DATABASE_URL=postgresql://postgres:password@localhost/ironvault
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    MAIL_USERNAME=your_mailtrap_username
    MAIL_PASSWORD=your_mailtrap_password
    MAIL_SERVER=sandbox.smtp.mailtrap.io
    MAIL_PORT=2525
    MAIL_FROM=noreply@ironvault.com
    BASE_URL=http://localhost:8000

### 3. Run Database Migrations

    alembic upgrade head

### 4. Start the Server

    uvicorn app.main:app --reload

------------------------------------------------------------------------

## Core Endpoints

### Authentication

-   POST /auth/register
-   POST /auth/login
-   GET /auth/verify-email
-   POST /auth/forgot-password
-   POST /auth/reset-password

### Wallet

-   GET /wallet/balance
-   POST /wallet/deposit
-   POST /wallet/withdraw
-   POST /wallet/transfer

### Savings

-   POST /savings/create
-   POST /savings/withdraw
-   GET /savings

### Transactions

-   GET /transactions
-   GET /transactions/{id}

### Admin

-   GET /admin/users
-   PATCH /admin/freeze/{user_id}
-   POST /admin/reverse-transaction

------------------------------------------------------------------------

## Security Considerations

-   All transfers must be atomic using database transactions.
-   Prevent self-transfers.
-   Prevent negative balances.
-   Rate limit sensitive endpoints.
-   Hash passwords securely.
-   Use environment variables for secrets.
-   Validate all request payloads with Pydantic.

------------------------------------------------------------------------

## Testing

Run unit tests with:

    pytest -v

------------------------------------------------------------------------

## Future Improvements

-   Integrate real payment gateway
-   Add Redis for caching & rate limiting
-   Implement 2FA
-   Add CI/CD pipeline
-   Deploy with Docker & Nginx

------------------------------------------------------------------------

## License

MIT License

------------------------------------------------------------------------

IronVault --- Where money moves with discipline.
