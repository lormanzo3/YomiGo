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
├── backend/          # Python FastAPI server
│   └── app/
│       └── main.py   # API endpoints
├── extension/        # React + TypeScript browser extension
│   ├── src/
│   └── public/
└── README.md
```

## API Endpoints

- `POST /parse` - Image → OCR → Tokens → Definitions
- `POST /ocr` - Image → Text only
- `GET /health` - Service status
