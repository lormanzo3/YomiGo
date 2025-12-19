# YomiGo

Japanese manga OCR and dictionary lookup browser extension.

## Architecture

- **Backend**: Python FastAPI server (OCR, parsing, dictionary)
- **Extension**: React + TypeScript browser extension

## Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 5000
```

### Extension

```bash
cd extension
npm install
npm run build
```

Load `extension/dist` as unpacked extension in Chrome.

## API Endpoints

- `POST /parse` - Image → OCR → Tokens → Definitions
- `POST /ocr` - Image → Text only
- `GET /health` - Service status
