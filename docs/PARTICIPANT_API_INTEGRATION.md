# Participant API Integration Guide

## Overview

The Participant API integration allows the Cimeika chat interface to communicate with an external AI participant service hosted on Hugging Face Spaces. This integration implements the "Ci Participant Protocol v1" for structured API interactions.

## Architecture

### Components

1. **Participant Client** (`frontend/src/services/participantClient.ts`)
   - TypeScript client for API communication
   - Handles authentication via X-API-KEY header
   - Provides typed interfaces for requests/responses

2. **Chat UI** (`frontend/src/pages/Chat.jsx`)
   - Extended to support participant messages
   - Toggle controls for participant mode
   - Renders participant responses with special formatting

3. **Type Definitions** (`frontend/src/modules/Ci/types.ts`)
   - Participant message types
   - Action types (suggest, check, patch)
   - Response severity levels

## Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# Participant API URL (default: https://ihorog-cimeika-api.hf.space)
VITE_PARTICIPANT_API_URL=https://ihorog-cimeika-api.hf.space

# Optional: API Key for authentication
VITE_PARTICIPANT_API_KEY=your_api_key_here
```

### Security Notes

- **API Key**: The `VITE_PARTICIPANT_API_KEY` is optional. If provided, it's sent as `X-API-KEY` header.
- **No Logging**: API keys are never logged to console.
- **Client-Side**: Currently, the client calls the API directly. For production, consider proxying through the backend.

## Usage

### User Interface

1. **Open Chat**: Navigate to `/chat` in the application
2. **Toggle Participant Controls**: Click "🤖 Показати контроль API Participant"
3. **Configure Mode**:
   - **analysis**: Get diagnosis and ordered actions
   - **autofix**: Request automated fixes with patches
   - **logger**: Log messages for audit/tracking
4. **Optional Topic**: Enter a specific topic for context
5. **Send Message**: Click "🤖 API" button to send to participant API

### Response Format

Participant responses appear as blue message cards with:
- **Speaker**: "🤖 API (participant-name)"
- **Severity Indicator**: ⚠️ for warnings, ❌ for errors
- **Message**: The diagnostic or response text
- **Patch Section** (if provided):
  - Unified diff display
  - "📋 Copy" button to copy patch to clipboard
  - "💾 Download" button to download as `.diff` file
- **Actions List**: Suggested actions with type indicators:
  - 💡 Suggest
  - ✅ Check
  - 🔧 Patch

### Example Interaction

**User Input:**
```
My npm install is failing with EACCESS error
```

**Mode:** `analysis`

**Participant Response:**
```
participant: cimeika-api
message: Detected npm permission issue. This commonly occurs when npm tries 
         to write to system directories.
severity: info
outputs:
  actions:
    - type: suggest
      title: Clear npm cache
      details: Run 'npm cache clean --force' to clear corrupted cache
    - type: check
      title: Check directory permissions
      details: Verify you have write access to node_modules directory
    - type: suggest
      title: Use nvm
      details: Consider using nvm to manage Node.js versions and avoid permission issues
```

## API Protocol

### Request Schema

```typescript
POST /api/participant/message
Content-Type: application/json
X-API-KEY: optional_api_key

{
  "conversation_id": "conv-1234567890",
  "mode": "analysis" | "autofix" | "logger",
  "topic": "optional topic string",
  "input": {
    "text": "User message here",
    "artifacts": [
      {
        "name": "file.txt",
        "content_base64": "base64_encoded_content"
      }
    ],
    "metadata": {
      "source": "ci" | "ci-cd" | "user",
      "repo": "Ihorog/cimeika-unified",
      "run_id": "optional_ci_run_id",
      "pr": 123
    }
  }
}
```

### Response Schema

```typescript
{
  "participant": "cimeika-api",
  "message": "Diagnostic or response message",
  "severity": "info" | "warn" | "error",
  "outputs": {
    "patch_unified_diff": "optional unified diff string",
    "actions": [
      {
        "type": "suggest" | "check" | "patch",
        "title": "Action title",
        "details": "Detailed description"
      }
    ]
  }
}
```

## Error Handling

### API Unavailable

If the participant API is unreachable, the UI displays:
```
🤖 API (system)
⚠️ API unavailable: Unable to connect to the participant service.
```

### Authentication Failure

401 responses indicate missing or invalid API key. Check your `VITE_PARTICIPANT_API_KEY` configuration.

### Network Errors

All network errors are caught and displayed as participant messages with `severity: warn`.

## Development

### Testing Locally

1. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

2. Navigate to `http://localhost:5173/chat`

3. Toggle participant controls and send a test message

### Mocking Responses

For testing without the live API, you can modify `participantClient.ts` to return mock responses:

```typescript
async sendMessage(request: ParticipantMessageRequest): Promise<ParticipantMessageResponse> {
  // Mock response for testing
  return {
    participant: 'mock-api',
    message: 'This is a mock response',
    severity: 'info',
    outputs: {
      actions: [
        {
          type: 'suggest',
          title: 'Test Action',
          details: 'This is a test action'
        }
      ]
    }
  };
}
```

## Future Enhancements

### Backend Proxy (Recommended for Production)

Instead of calling the participant API directly from the browser:

1. Create a FastAPI endpoint in `backend/app/modules/ci/api.py`:
   ```python
   @router.post("/participant/message")
   async def proxy_participant_message(request: ParticipantMessageRequest):
       # Forward to HF Space with backend API key
       # Add rate limiting, logging, monitoring
       pass
   ```

2. Update `participantClient.ts` to call backend proxy:
   ```typescript
   const response = await fetch(`${API_BASE}/api/v1/ci/participant/message`, {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify(request)
   });
   ```

Benefits:
- API key stays on server
- Backend can add rate limiting
- Centralized logging and monitoring
- CORS issues eliminated

### Advanced Features

- **Artifact Upload**: UI for uploading log files/patches
- **Conversation History**: Persist participant conversations
- **Action Execution**: Click to execute suggested actions
- **Multi-Participant**: Support multiple participant services
- **Voice Mode**: Speak participant responses via TTS

## Troubleshooting

### Issue: Participant button not appearing
**Solution**: Click "🤖 Показати контроль API Participant" to toggle controls

### Issue: API always returns 401
**Solution**: Verify `VITE_PARTICIPANT_API_KEY` is set correctly in `.env`

### Issue: CORS errors in browser console
**Solution**: 
- Check that HF Space has CORS enabled
- Consider using backend proxy (see Future Enhancements)

### Issue: Patch download not working
**Solution**: Check browser permissions for downloads

## References

- [Ci Participant Protocol Spec](./CI_PARTICIPANT_PROTOCOL.md)
- [Hugging Face Space](https://huggingface.co/spaces/Ihorog/cimeika-api)
- [Chat Component Source](../frontend/src/pages/Chat.jsx)
- [Participant Client Source](../frontend/src/services/participantClient.ts)
