# ImageInsight API

A FastAPI-based REST API for intelligent image analysis and background removal. Upload images to get detailed metadata, AI-generated descriptions powered by Meta Llama 3.2 Vision, and background removal using the BriaRMBG deep learning model. All processed images are stored securely in AWS S3.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Model Setup (RMBG-1.4)](#model-setup-rmbg-14)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)

---

## Project Overview

ImageInsight API provides three core capabilities:

- **Image Analysis** — Extract metadata (dimensions, file type, size, pixel count, aspect ratio, alpha channel, RGB histograms) and generate a natural-language description of the image using an LLM.
- **Background Removal** — Remove the background from any image using the BriaRMBG-1.4 ML model, returning a transparent PNG.
- **Secure Storage** — All images are stored in an AWS S3 bucket and accessible via pre-signed URLs.

Access to all image endpoints is protected by JWT authentication.

---

## Prerequisites

Make sure the following are installed and available on your machine before proceeding:

| Requirement | Version | Notes |
|---|---|---|
| Python | >= 3.13 | Check with `python --version` |
| [UV](https://docs.astral.sh/uv/) | Latest | Fast Python package manager |
| AWS Account | — | S3 bucket + IAM credentials required |
| PostgreSQL / AWS RDS | >= 14 | PostgreSQL database instance |
| Git | — | To clone the repository |

### Install UV

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd ImageInsight-API
```

### 2. Create a virtual environment and install dependencies

UV handles both the virtual environment and dependency installation in one step:

```bash
uv sync
```

This reads `pyproject.toml` and installs all required packages into a local `.venv` directory.

> **Note:** The initial install includes PyTorch and other large ML libraries. It may take several minutes depending on your internet connection.

---

## Model Setup (RMBG-1.4)

The background removal feature uses the **BriaRMBG-1.4** model from HuggingFace. The model files must be downloaded manually and placed in a local directory, as they are excluded from version control.

### Step 1 — Install the HuggingFace CLI (already included in dependencies)

```bash
uv run huggingface-cli login
```

You will be prompted for a HuggingFace token. Create a free account at [huggingface.co](https://huggingface.co) and generate a token from your account settings if you don't already have one.

### Step 2 — Download the model

```bash
uv run huggingface-cli download briaai/RMBG-1.4 --local-dir rmbg_model
```

This downloads all model files into the `rmbg_model/` directory at the root of the project.

### Step 3 — Verify the directory

After downloading, your project root should contain:

```
rmbg_model/
├── config.json
├── model.safetensors
├── preprocessor_config.json
└── ...
```

The application reads the model path from the `RMBG_MODEL_PATH` environment variable (defaults to `rmbg_model`).

> **Note:** The model is loaded lazily — it is only loaded into memory on the first background removal request.

---

## Environment Variables

Create a `.env` file in the root of the project by copying the template below. **Never commit your `.env` file to version control.**

```bash
# .env

# --- AWS S3 Storage ---
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_BUCKET_NAME=your_s3_bucket_name
AWS_REGION=your_aws_region               # e.g. eu-north-1

# --- LLM (OpenRouter) ---
OPENROUTER_API_KEY=your_openrouter_api_key

# --- Database (PostgreSQL / AWS RDS) ---
DB_HOST=your_db_host                     # e.g. mydb.xxxxxxxx.rds.amazonaws.com
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password

# --- JWT Authentication ---
JWT_SECRET_KEY=your_secret_key           # generate with: openssl rand -hex 32
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# --- ML Model ---
RMBG_MODEL_PATH=rmbg_model
```

### Variable Descriptions

| Variable | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key with S3 read/write permissions |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `AWS_BUCKET_NAME` | Name of the S3 bucket where images will be stored |
| `AWS_REGION` | AWS region where the S3 bucket is located |
| `OPENROUTER_API_KEY` | API key from [openrouter.ai](https://openrouter.ai) — used to call Meta Llama 3.2 Vision for image descriptions |
| `DB_HOST` | Hostname of your PostgreSQL database or RDS instance |
| `DB_PORT` | Database port (PostgreSQL default is `5432`) |
| `DB_NAME` | Name of the database to connect to |
| `DB_USER` | Database username |
| `DB_PASSWORD` | Database password |
| `JWT_SECRET_KEY` | Secret key used to sign and verify JWT tokens — use a long random string |
| `JWT_ALGORITHM` | JWT signing algorithm (keep as `HS256`) |
| `JWT_EXPIRE_MINUTES` | How many minutes a login token remains valid |
| `RMBG_MODEL_PATH` | Path to the directory containing the downloaded RMBG model files |

### Generate a secure JWT secret key

```bash
openssl rand -hex 32
```

---

## Database Setup

The application uses **PostgreSQL** (via AWS RDS or any hosted PostgreSQL instance). The database schema is created automatically on startup — no manual migration steps are needed.

### Required: Create the database

Make sure a PostgreSQL database exists with the name you set in `DB_NAME`. You can create one using `psql`:

```bash
psql -h <DB_HOST> -U <DB_USER> -c "CREATE DATABASE <DB_NAME>;"
```

### Automatic table creation

When the application starts, it automatically runs:

```python
await create_tables()
```

This creates all required tables (e.g., the `user` table) using SQLModel.

### Seeding initial users (optional)

A seed script is included to populate the database with test users:

```bash
uv run python -m app.db.seed
```

This creates two users:

| Email | Password |
|---|---|
| `maha@gmail.com` | `12345678` |
| `hasan@gmail.com` | `password123` |

> These are for development/testing purposes only. Remove or replace them before deploying to production.

### AWS RDS Setup (recommended for production)

1. Create a **PostgreSQL** RDS instance in your AWS account.
2. Set the instance to be publicly accessible (or configure a VPC/security group for access from your server).
3. Use the RDS endpoint as `DB_HOST` in your `.env` file.
4. Make sure port `5432` is open in the RDS security group.

---

## Running the Project

### Start the development server

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Access the interactive API documentation

| URL | Description |
|---|---|
| `http://localhost:8000/docs` | Swagger UI (interactive) |
| `http://localhost:8000/redoc` | ReDoc documentation |

### Start the server on a custom host/port

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

---

## API Endpoints

### Authentication

All image endpoints are protected. You must first log in to receive a JWT token, then include it in subsequent requests.

---

#### `POST /auth/login`

Authenticate with email and password to receive a Bearer token.

**Request body (JSON):**

```json
{
  "email": "maha@gmail.com",
  "password": "12345678"
}
```

**Response (`200 OK`):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error responses:**

| Status | Description |
|---|---|
| `401 Unauthorized` | Invalid email or password |

**Include the token in all subsequent requests:**

```
Authorization: Bearer <access_token>
```

---

### Image Analysis

#### `POST /v1/image-info`

Analyze an image and return metadata plus an AI-generated description. The image is stored in S3.

**Request body (JSON):**

Provide either a base64-encoded image string or a publicly accessible image URL. At least one is required.

```json
{
  "base64": "<base64-encoded-image-string>"
}
```

```json
{
  "url": "https://example.com/photo.jpg"
}
```

**Response (`200 OK`):**

```json
{
  "file_type": "JPEG",
  "file_size": 204800,
  "width": 1920,
  "height": 1080,
  "pixel_count": 2073600,
  "aspect_ratio": "16:9",
  "alpha_channel": false,
  "histogram": {
    "red": [0, 12, 34, ...],
    "green": [0, 8, 22, ...],
    "blue": [0, 5, 19, ...]
  },
  "description": "A vibrant outdoor landscape featuring rolling green hills under a clear blue sky. The image conveys a sense of openness and calm, with warm sunlight illuminating the scene. At 1920×1080, the 16:9 aspect ratio gives it a cinematic quality.",
  "image_id": "images/f3a1b2c4-xxxx-xxxx-xxxx-d5e6f7a8b9c0.jpeg"
}
```

---

#### `GET /v1/images/{image_id}`

Download a previously analyzed image as binary data.

**Path parameter:** `image_id` — the value returned in `image_id` from the analysis response.

**Response:** Binary `image/jpeg` content.

---

#### `GET /v1/images/url/{image_id}`

Get a pre-signed S3 URL for a previously analyzed image (valid for 1 hour).

**Path parameter:** `image_id` — the value returned in `image_id` from the analysis response.

**Response (`200 OK`):**

```json
{
  "url": "https://your-bucket.s3.amazonaws.com/images/f3a1b2c4-xxxx.jpeg?X-Amz-Signature=..."
}
```

---

### Background Removal

#### `POST /v1/remove-background`

Remove the background from an uploaded image. Returns a transparent PNG stored in S3.

**Request:** `multipart/form-data` with a file field named `file`.

```bash
curl -X POST http://localhost:8000/v1/remove-background \
  -H "Authorization: Bearer <token>" \
  -F "file=@photo.jpg"
```

**Accepted file types:** `image/jpeg`, `image/png`, `image/webp`, `image/avif`
**Maximum file size:** 10 MB

**Response (`200 OK`):**

```json
{
  "image_id": "removed-bg/a1b2c3d4-xxxx-xxxx-xxxx-e5f6a7b8c9d0.png",
  "url": "https://your-bucket.s3.amazonaws.com/removed-bg/a1b2c3d4-xxxx.png?X-Amz-Signature=...",
  "message": "Background removed successfully."
}
```

**Error responses:**

| Status | Description |
|---|---|
| `400 Bad Request` | Unsupported file type or empty file |
| `413 Request Entity Too Large` | File exceeds 10 MB |

---

#### `GET /v1/remove-background/{image_id}`

Download a background-removed image as a transparent PNG.

**Path parameter:** `image_id` — the value returned in `image_id` from the remove-background response.

**Response:** Binary `image/png` content with alpha (transparency) channel.

---

### Endpoint Summary

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/login` | None | Log in and get a JWT token |
| `POST` | `/v1/image-info` | Required | Analyze image metadata + AI description |
| `GET` | `/v1/images/{image_id}` | Required | Download analyzed image |
| `GET` | `/v1/images/url/{image_id}` | Required | Get pre-signed URL for analyzed image |
| `POST` | `/v1/remove-background` | Required | Remove background from uploaded image |
| `GET` | `/v1/remove-background/{image_id}` | Required | Download background-removed image |

---

## Project Structure

```
ImageInsight API/
├── main.py                         # Root entry point
├── pyproject.toml                  # Project metadata and dependencies
├── .env                            # Environment variables (not committed)
├── .python-version                 # Python version pin
├── rmbg_model/                     # BriaRMBG-1.4 model files (not committed)
└── app/
    ├── main.py                     # FastAPI app initialization, router registration, startup
    ├── dependencies.py             # Shared FastAPI dependencies (image validator)
    ├── routes/
    │   ├── auth.py                 # POST /auth/login
    │   ├── image_info.py           # GET/POST /v1/image-info, /v1/images/...
    │   └── image_remove_background.py  # GET/POST /v1/remove-background/...
    ├── services/
    │   ├── auth_service.py         # JWT creation, password verification, user lookup
    │   ├── background_remover.py   # BriaRMBG model inference (PyTorch)
    │   ├── image_analyzer.py       # Metadata extraction + LLM description orchestration
    │   ├── llm_service.py          # OpenRouter API client (Llama 3.2 Vision)
    │   └── storage_service.py      # AWS S3 upload, download, and pre-signed URL generation
    ├── schemas/
    │   ├── auth_schema.py          # LoginRequest, TokenResponse
    │   └── image_schema.py         # ImageRequest, InfoResponse, ColorHistogram
    ├── db/
    │   ├── database.py             # Async SQLModel engine, session factory, create_tables()
    │   ├── models.py               # User ORM model
    │   └── seed.py                 # Script to seed test users
    └── middleware/
        └── auth_middleware.py      # JWT validation middleware for /v1/* routes
```
