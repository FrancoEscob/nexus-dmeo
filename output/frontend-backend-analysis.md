# Frontend and Backend Technical Analysis Report

## Frontend Analysis

### Technology Stack
- **Core Framework**: Next.js 14.2.5 (React 18.2.0)
- **Language**: TypeScript 5.4.2
- **Styling**: Tailwind CSS 3.4.10 with custom globals.css

### File Structure
- `src/app/`: Root layout, main demo page (page.tsx), globals.css
- `src/components/`: AudioRecorder.tsx, ScoreGrid.tsx, ErrorCard.tsx, UtteranceBox.tsx, etc.
- `src/lib/`: API integration, SSE handling, browser STT hook, utterances data

### Key Components
- AudioRecorder: WebRTC recording with waveform
- ScoreGrid: Circular progress for metrics (accuracy, fluency, etc.)
- ErrorCard: Technical error display
- UtteranceBox: Text input/generation

### State Management
- React hooks (useState, useEffect)
- LocalStorage for user prefs
- SSE for real-time updates

### Backend Integration
- REST API calls to /api/analyze-pronunciation
- SSE for streaming feedback
- FormData audio uploads

## Backend Analysis

### Technology Stack
- **Framework**: FastAPI (Python)
- **Services**: Azure Cognitive Services Speech, Google Gemini AI, Supabase (PostgreSQL)

### API Endpoints
- POST /api/analyze-pronunciation: Core analysis with SSE stream
- POST /api/teaser: Priority error summary
- POST /api/coach-cards: LLM-generated coaching
- POST /api/weekly-plan: 7-day practice plan

### Azure Integration
- PronunciationAssessmentConfig: HundredMark grading, Phoneme granularity, IPA alphabet
- Scores: Accuracy, Fluency, Completeness, Prosody (0-100)
- Error types: Omission, Insertion, Mispronunciation

### Data Flow
1. Audio upload/conversion (FFmpeg to 16kHz WAV)
2. STT (browser or Azure fallback)
3. Azure assessment
4. Error categorization by severity
5. LLM enhancement (Gemini for coach cards)

### Sample Azure JSON Response
```json
{
  \"pronunciation_chunks\": [
    {
      \"accuracy\": 94.0,
      \"fluency\": 98.0,
      \"prosody\": 78.2,
      \"words\": [
        {
          \"word\": \"record\",
          \"phonemes\": [
            {\"phoneme\": \"ɹ\", \"accuracy\": 66.0}
          ]
        }
      ]
    }
  ]
}
```

### Current Demo Issues
- Technical feedback cards overwhelm users, need to explain in a friendly simple way the phonemes, sounds, etc.
- No simple, actionable insights
- Missing confidence-building UX