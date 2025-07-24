---
title: "RFD-000: Ephemeral RAG Chat Widget for Jekyll Blog"
author: "Wentao Jiang"
date: "2025-07-23"
created: "2025-07-23 22:21:48 PDT"
status: "Draft"
type: "Request for Discussion"
version: "1.0"
---

# RFD-000: Ephemeral RAG Chat Widget for Jekyll Blog

## Metadata

- **Title**: Ephemeral RAG Chat Widget for Jekyll Blog
- **Author**: Wentao Jiang
- **Date**: 2025-07-23
- **Created**: 2025-07-23 22:21:48 PDT
- **Last Updated**: 2025-07-24
- **Status**: Implemented
- **Type**: Request for Discussion
- **Version**: 1.1

## Abstract

This RFD proposes the implementation of an ephemeral chat widget for the Jekyll blog hosted on GitHub Pages. The widget will integrate with an existing RAG (Retrieval-Augmented Generation) chatbot API running on an OCI instance to provide users with an interactive way to search and discover blog content.

## Design Requirements

### Core Requirements

1. **No Emoji Policy**: The implementation must not use any emoji characters in the RFD documentation, actual code, or chat UI components.
2. **Ephemeral Design**: One question, one answer, reset for next question - no persistent conversation state
3. **GitHub Pages Compatibility**: Must work with static site generation and GitHub Pages constraints
4. **API Integration**: Connect to existing RAG API using environment variable configuration
5. **Rate Limiting**: Respect API rate limits with client-side throttling
6. **Responsive Design**: Work on both desktop and mobile devices

### Functional Requirements

1. **User Interface**:
   - Floating chat button for non-intrusive access
   - Modal dialog for question input and response display
   - Clean, accessible design matching site theme
   - Dynamic technical sample questions as placeholders
   - ESC key support for modal dismissal

2. **Response Display**:
   - Render main answer as formatted markdown
   - Display source references with relevance scores
   - Provide clickable links to referenced blog posts

3. **Error Handling**:
   - Graceful handling of API failures
   - User-friendly error messages
   - Network timeout handling

## Technical Architecture

### API Integration

The widget will integrate with the existing RAG API using environment variable configuration:

- **Environment Variable**: `CHATBOT_API_URL` (configured via GitHub Secrets)
- **Endpoint**: `POST /rag/generate-test`
- **Request Format**:
  ```json
  {
    "query": "user question",
    "context_limit": 3
  }
  ```
- **Response Format**:
  ```json
  {
    "answer": "Generated response text",
    "context_used": [
      {
        "content": "Content snippet",
        "metadata": {
          "title": "Blog post title",
          "url": "GitHub URL",
          "categories": "Post categories",
          "tags": "Post tags"
        },
        "distance": 0.93
      }
    ]
  }
  ```

### Implementation Components

1. **JavaScript Widget** (`assets/js/blog-chat-widget.js`):
   - Main widget logic and API communication
   - DOM manipulation and event handling
   - Rate limiting and error handling
   - Dynamic sample question generation
   - Keyboard event handling (ESC key support)

2. **CSS Styling** (`assets/css/blog-chat-widget.css`):
   - Widget appearance and responsive design
   - Modal dialog styling
   - Loading states and animations

3. **Layout Integration** (`_layouts/default.html`):
   - Include widget scripts and styles
   - Ensure compatibility with Minimal Mistakes theme

### Rate Limiting Strategy

- **Client-side throttling**: Maximum 1 request per 30 seconds
- **User feedback**: Clear messaging when rate limit is hit
- **Graceful degradation**: Widget remains functional during API issues

## User Experience Flow

1. **Discovery**: User sees floating chat button on blog pages
2. **Interaction**: Click button opens modal dialog with random technical sample question
3. **Inspiration**: User sees contextually relevant placeholder questions that change each time
4. **Query**: User types question about blog content (or uses suggested question)
5. **Processing**: Loading indicator while API processes request
6. **Response**: Display formatted answer with source references
7. **Navigation**: User can click source links to read full posts
8. **Dismissal**: User can close widget via close button, ESC key, or outside click
9. **Reset**: User can ask another question with new sample placeholder

## Response Rendering

### Main Answer Display

- Parse and render markdown formatting
- Support for bold, italic, and links
- Proper paragraph breaks and line spacing

### Source References Section

For each source in `context_used`:
- Extract blog post title from `metadata.title`
- Calculate relevance percentage from `distance` score
- Create clickable link from `metadata.url`
- Display content snippet for context

Example source display:
```
Sources:

[Document Icon] This week's outside five sigma (#28)
Relevance: 93% | View Post [Arrow]

[Document Icon] This week's outside five sigma (#36)
Relevance: 89% | View Post [Arrow]
```

## Dynamic Sample Questions

### Purpose and Design

To improve user engagement and provide inspiration for queries, the widget includes a curated set of technical sample questions that appear as placeholders in the input field. These questions are:

1. **Technically Specific**: Reflect the advanced technical content of the blog
2. **Contextually Relevant**: Based on actual blog post content and topics
3. **Dynamically Selected**: Randomly chosen each time the modal opens
4. **Educationally Valuable**: Demonstrate the depth of content available

### Current Sample Questions

The widget includes the following technically sophisticated questions:

- "What's the de Broglie wavelength of 10 kV electrons in e-beam lithography?"
- "How do you calculate the flux quantum threading for superconducting resonator tuning?"
- "Why do wavelength-scale acoustic waveguides need large transducers for efficient coupling?"
- "What's the Schwinger limit for dielectric breakdown in perfect vacuum?"
- "How does kinetic inductance in NbTiN change with magnetic flux threading?"

### Implementation Details

- Questions are stored in a JavaScript array within the widget constructor
- Random selection occurs in the `openModal()` method using `Math.floor(Math.random())`
- Placeholder updates dynamically each time the modal is opened
- Questions are designed to showcase the blog's coverage of advanced topics in:
  - Nanofabrication and e-beam lithography
  - Superconducting circuits and quantum physics
  - Acoustic/mechanical waveguides and transduction
  - Fundamental physics limits and phenomena
  - Materials science and device physics

## Accessibility and User Experience Enhancements

### Keyboard Navigation Support

The widget implements comprehensive keyboard accessibility:

1. **ESC Key Dismissal**: Users can press the ESC key to close the modal dialog
2. **Enter Key Submission**: Users can press Enter in the textarea to submit questions
3. **Focus Management**: Modal automatically focuses the input field when opened
4. **Event Handling**: Global ESC key listener only responds when modal is visible

### Implementation Details

- ESC key event listener attached to the document object
- Conditional check ensures ESC only works when modal is not hidden
- Prevents conflicts with other page elements that might use ESC
- Maintains standard web accessibility patterns

## Security Considerations

1. **Environment Variables**: API endpoint URL stored in GitHub Secrets, not in code
2. **CORS Configuration**: OCI instance must allow requests from GitHub Pages domain
3. **Rate Limiting**: Prevent abuse through client-side throttling
4. **Input Sanitization**: Sanitize user input before API calls
5. **XSS Prevention**: Properly escape rendered content
6. **No Hardcoded URLs**: All sensitive configuration via environment variables

## Implementation Plan

### Phase 1: Core Widget
- Create basic floating button and modal
- Implement API integration
- Add basic error handling

### Phase 2: Enhanced UI
- Add CSS styling and responsive design
- Implement loading states
- Add keyboard navigation and ESC key support

### Phase 3: Polish
- Optimize for mobile devices
- Add accessibility features
- Performance optimization

## Testing Strategy

1. **API Testing**: Verify integration with test queries
2. **Cross-browser Testing**: Ensure compatibility across browsers
3. **Mobile Testing**: Verify responsive behavior
4. **Error Testing**: Test network failures and rate limiting

## Success Metrics

1. **Functionality**: Widget successfully queries API and displays results
2. **Usability**: Users can easily discover and use the chat feature
3. **Performance**: Fast response times and smooth interactions
4. **Reliability**: Graceful handling of errors and edge cases

## Future Considerations

1. **Authentication**: Potential migration to authenticated API endpoint
2. **Conversation History**: Adding session-based conversation memory
3. **Analytics**: Tracking usage patterns and popular queries
4. **Enhanced Features**: File upload, voice input, or advanced formatting

## Implementation Decisions

### Final Architecture Decision
After evaluation, the following approach was selected:

**Environment Variable Configuration via Jekyll**:
- Production: Use GitHub Repository Variables to set `CHATBOT_API_URL`
- Local Development: Use `.env` file with setup script (`scripts/setup-local-dev.sh`)
- Configuration: Inline JavaScript config generation in `_layouts/default.html`
- Fallback: Chat widget disabled when no API URL configured

**Rejected Alternatives**:
- Custom GitHub Actions workflow (would conflict with default GitHub Pages build)
- Hardcoded API URLs (security risk)
- Client-side config files (complexity without benefit)

### Configuration Details
- **Production Setup**: Repository Variables → `CHATBOT_API_URL` → `site.chatbot_api_url` → inline JavaScript
- **Local Setup**: `.env` file → `scripts/setup-local-dev.sh` → Jekyll environment variable
- **Rate Limiting**: 30 seconds between requests (adjusted from initial 10 seconds)
- **Security**: No API URLs in source code, environment variable based configuration

### File Structure
```
├── docs/RFD-000-ephemeral-rag-chat-widget.md  # This specification
├── assets/js/blog-chat-widget.js              # Main widget implementation
├── assets/css/blog-chat-widget.css            # Widget styling
├── scripts/setup-local-dev.sh                 # Local development setup
├── .env.example                               # Environment template
└── _layouts/default.html                      # Modified to include widget
```

## Conclusion

This ephemeral RAG chat widget provides users with an intuitive way to discover and explore blog content through natural language queries. The implementation prioritizes simplicity, reliability, and user experience while respecting API constraints and maintaining compatibility with the existing Jekyll/GitHub Pages infrastructure.

The chosen architecture avoids conflicts with the default GitHub Pages build process while maintaining security through environment variable configuration.

## Implementation Status

**Status**: ✅ **IMPLEMENTED** (Version 1.1)

### Completed Features

- ✅ Core widget functionality with floating button and modal
- ✅ API integration with RAG backend
- ✅ Rate limiting (30 seconds between requests)
- ✅ Error handling and user feedback
- ✅ Responsive design and dark theme styling
- ✅ Dynamic technical sample questions as placeholders
- ✅ ESC key support for modal dismissal
- ✅ Keyboard accessibility improvements
- ✅ Environment variable configuration
- ✅ GitHub Pages deployment

### Recent Updates (v1.1 - 2025-07-24)

1. **Dynamic Sample Questions**: Added 5 technically sophisticated sample questions that randomly rotate as placeholders, showcasing the blog's advanced technical content
2. **Enhanced Keyboard Support**: Implemented ESC key functionality for modal dismissal
3. **Improved User Experience**: Placeholder questions now update each time the modal is opened, providing fresh inspiration for users

## Changelog

### Version 1.1 (2025-07-24)
- **Added**: Dynamic technical sample questions with random selection
- **Added**: ESC key support for modal dismissal
- **Enhanced**: Keyboard accessibility and user experience
- **Updated**: Documentation to reflect new features

### Version 1.0 (2025-07-23)
- **Initial**: Core widget implementation
- **Initial**: API integration and rate limiting
- **Initial**: Basic UI and styling
- **Initial**: Environment variable configuration
