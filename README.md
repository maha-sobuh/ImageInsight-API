# ImageInsight API

FastAPI service for image analysis and background removal. Upload images to extract metadata and AI-generated descriptions (via Llama 3.2 Vision), or remove backgrounds using the BriaRMBG model. Images are stored in AWS S3.

---

## Prerequisites

- Python >= 3.13
- [UV](https://docs.astral.sh/uv/installation/)
- AWS account with an S3 bucket
- PostgreSQL database (or AWS RDS)
- [OpenRouter](https://openrouter.ai) API key

---

## Setup

```bash
git clone <repository-url>
cd ImageInsight-API
uv sync
```

---

## RMBG-1.4 Model

Download the model from HuggingFace into the `rmbg_model/` directory:

```bash
uv run huggingface-cli login
uv run huggingface-cli download briaai/RMBG-1.4 --local-dir rmbg_model
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_BUCKET_NAME=
AWS_REGION=

OPENROUTER_API_KEY=

DB_HOST=
DB_PORT=5432
DB_NAME=
DB_USER=
DB_PASSWORD=

JWT_SECRET_KEY=        # generate: openssl rand -hex 32
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

RMBG_MODEL_PATH=rmbg_model
```

---

## Run

```bash
uv run uvicorn app.main:app --reload
```

API available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/auth/login` | Login and receive a JWT token |
| `POST` | `/v1/image-info` | Analyze image metadata and generate AI description |
| `GET` | `/v1/images/{image_id}` | Download an analyzed image |
| `GET` | `/v1/images/url/{image_id}` | Get a pre-signed S3 URL for an analyzed image |
| `POST` | `/v1/remove-background` | Remove background from an uploaded image |
| `GET` | `/v1/remove-background/{image_id}` | Download a background-removed image |

All `/v1/` endpoints require `Authorization: Bearer <token>`.
