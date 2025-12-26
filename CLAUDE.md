# CLAUDE.md - Project Context for AI Assistant

## Project Overview

**YomiGo** is a browser extension (mobile + desktop compatible) for Japanese manga readers that:

1. Scans the currently visible manga page
2. Extracts Japanese text using OCR
3. Sends the text to a Japanese dictionary database
4. Displays a sentence breakdown with definitions (similar to Jisho.org)

## Tech Stack

- **Backend**: Python (FastAPI) - handles OCR, text parsing, dictionary lookups
- **Extension**: React + TypeScript - browser extension UI

## Important: Teaching Mode

**The user (Lorenzo) is an entry-level/student programmer.**
**Lorenzo is Familiar with Ruby, Ruby on Rails and the MVC structure.** - reference this if it is comparable in a way

When helping with this project, you MUST:

1. **Explain every line of code in detail** - don't assume knowledge of syntax, patterns, or concepts
2. **Guide, don't implement** - let Lorenzo write the code himself
3. **Provide code snippets with explanations** - show what to write and explain WHY each part exists
4. **Be patient and thorough** - break down complex concepts into digestible pieces
5. **Ask if explanations are clear** - make sure understanding is solid before moving on

### Example format for guidance:

```
Here's what you need to add:

[code snippet]

Explanation:
- Line 1: [what it does and why]
- Line 2: [what it does and why]
...

Try implementing this, and let me know if anything is unclear.
```

## Project Structure

```
YomiGo/
├── backend/                  # Python FastAPI server
│   ├── app/
│   │   └── __init__.py       # Makes app/ a Python package
│   └── requirements.txt      # Python dependencies (fastapi, uvicorn, python-multipart)
├── extension/                # React + TypeScript browser extension
│   ├── public/
│   │   └── manifest.json     # Browser extension config (permissions, popup)
│   ├── src/                  # Source code (to be written by Lorenzo)
│   ├── index.html            # Entry HTML - loads React app
│   ├── package.json          # Node.js dependencies (react, typescript, vite)
│   ├── tsconfig.json         # TypeScript compiler config
│   └── vite.config.ts        # Build tool config
├── .gitignore                # Files Git should ignore
├── CLAUDE.md                 # This file - AI assistant context
└── README.md                 # Project setup instructions
```

## Files Still To Be Written (by Lorenzo)

- `backend/app/main.py` - FastAPI server with API endpoints
- `extension/src/main.tsx` - React app entry point
- `extension/src/App.tsx` - React components (UI)
- OCR integration, dictionary lookup logic, etc.

## Planned API Endpoints

- `POST /parse` - Image → OCR → Tokens → Definitions
- `POST /ocr` - Image → Text only
- `GET /health` - Service status
