# YomiGo

Japanese manga OCR and dictionary lookup browser extension.

## Project Structure

- `backend/` - Python FastAPI server (OCR, parsing, dictionary)
- `extension/` - React + TypeScript browser extension

## Setup

### Backend

1. Create a virtual environment:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Extension

1. Install dependencies:
   ```bash
   cd extension
   npm install
   ```

2. Build the extension:
   ```bash
   npm run build
   ```

3. Load in Chrome:
   - Go to `chrome://extensions`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select the `extension/dist` folder
