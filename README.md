# LLM Redaction

**Automatically mask PII before it reaches the LLM — and restore it on the way back.**

When you send contracts, resumes, or other sensitive documents to an LLM, personally identifiable information (names, national IDs, phone numbers, etc.) is transmitted to external servers as-is. LLM Redaction solves this by automatically detecting PII, replacing it with tokens like `[[PII:NAME:3]]`, and forwarding only the masked text to the LLM. Tokens in the LLM response are then restored to their original values before reaching the user — so the user sees natural text while **the LLM never sees real personal data**. A hybrid detection pipeline (Regex + NER + LLM) maximizes precision, token maps are protected with Fernet encryption, and a "Show what LLM sees" toggle visually proves that no real PII was exposed.

## How It Works

```
Original Document → PII Detection → Token Replacement (Masking) → Send to LLM
                                                                       ↓
        User ← Original Restoration ← LLM Response (contains tokens)
```

1. **Upload** a document (TXT or PDF) — PII is detected and replaced with `[[PII:TYPE:id]]` tokens
2. **Chat** with the LLM about the masked document — the LLM only sees tokens, never real data
3. **Receive** a natural response — the server restores tokens to original values before returning
4. **Toggle** "Show what LLM sees" to verify the LLM never saw actual PII

## PII Detection Pipeline

The system uses a multi-stage hybrid approach combining three detectors:

| Detector | Method | What It Catches |
|----------|--------|-----------------|
| **Regex** | Pattern matching with checksum validation | Korean RRN (주민등록번호), BRN (사업자등록번호), phone numbers, email, bank accounts, license plates, API keys |
| **NER** | BERT-based named entity recognition | Person names, organizations, locations |
| **LLM** | Gemini-powered contextual detection | Broad semantic PII — addresses, dates of birth, and context-dependent entities |
| **Hybrid** | All three combined with intelligent merging | Maximum recall with priority-based conflict resolution |

Overlapping detections are merged by source priority (regex > NER > LLM), type sensitivity, span length, and confidence score.

## Key Features

- **Hybrid PII detection** — regex, NER, and LLM detectors with smart span merging
- **Transparent masking** — "Show what LLM sees" toggle proves no PII was exposed
- **Encrypted token maps** — Fernet symmetric encryption; restoration requires admin key
- **Document chat** — ask questions about masked documents via Gemini
- **Auto-expiration** — documents are deleted after a configurable TTL (default: 1 hour)
- **Audit trail** — downloadable JSON with detection details (type, source, confidence, position)
- **PDF & TXT support** — multi-page PDF extraction included
- **Korean PII specialization** — RRN/BRN checksum validation, Korean phone formats, license plates

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI, Uvicorn, Pydantic |
| **LLM** | Google Gemini API (`google-genai`) |
| **Encryption** | Fernet (cryptography library) |
| **PDF Processing** | pypdf |
| **Frontend** | Vanilla JS (ES6 modules), CSS custom properties |
| **Testing** | pytest, pytest-asyncio, httpx |

## Getting Started

### Prerequisites

- Python 3.10+
- Google Gemini API key (for chat and LLM-based detection)

### Installation

```bash
git clone https://github.com/minjcho/LLMredaction.git
cd LLMredaction
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and set values:

```bash
GEMINI_API_KEY=<your-gemini-api-key>    # Required for /chat and LLM detector
ALLOW_REMOTE_LLM=false                  # Set true to enable Gemini-based PII detection
FERNET_KEY=<your-fernet-key>            # Auto-generated if not set
ADMIN_KEY=changeme                      # Key required to restore original text
DOC_TTL_SEC=3600                        # Document lifetime in seconds
```

Generate a Fernet key:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000.

### Test

```bash
pytest -v
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/redaction/{model}` | Detect and mask PII (`model`: regex, ner, gemini, hybrid) |
| `GET` | `/download/{doc_id}` | Download masked text (`?format=masked`) or audit JSON (`?format=audit`) |
| `POST` | `/restore/{doc_id}` | Restore original text (requires `X-ADMIN-KEY` header) |
| `POST` | `/chat` | Chat with LLM about a masked document |
