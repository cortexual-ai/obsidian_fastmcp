# Obsidian FastMCP + Anki Integration Plan

## Overview
This document outlines the step-by-step plan to add Anki card creation capabilities to the Obsidian FastMCP server. The integration will allow users to create Anki flashcards from Obsidian notes and manage them through Claude.

## Goals
- Create `.apkg` files using genanki for Anki import
- Support multiple card types: Basic, Reverse, Cloze, Image Occlusion
- Intelligent card creation from Obsidian notes
- Deck management and organization
- Bidirectional linking between Obsidian and Anki

## Phase 1: Foundation Setup

### 1.1 Dependencies & Configuration
- [ ] Add `genanki>=1.20.0` to pyproject.toml
- [ ] Create `AnkiConfig` class in `src/config/settings.py`
  - [ ] Configurable Anki files location
  - [ ] Default deck settings
  - [ ] Export preferences
- [ ] Update environment variables for Anki paths

### 1.2 Data Models
- [ ] Create `src/models/anki_models.py`
  - [ ] `AnkiCard` base model
  - [ ] `BasicCard`, `ReverseCard`, `ClozeCard`, `ImageOcclusionCard` models
  - [ ] `AnkiDeck` model
  - [ ] Card type enums and validation

### 1.3 Deck Management System
- [ ] Create `src/tools/deck_management.py`
  - [ ] `create_deck()` - Create new deck
  - [ ] `list_decks()` - List available decks
  - [ ] `get_deck_info()` - Get deck metadata
- [ ] Create deck registry file (`anki_decks.json`)
- [ ] Implement deck ID generation and tracking

## Phase 2: Core Anki Tools

### 2.1 Individual Card Creation Tools
- [ ] Create `src/tools/anki_cards/`
  - [ ] `create_basic_card.py` - Front/back card creation
  - [ ] `create_reverse_card.py` - Bidirectional card creation
  - [ ] `create_cloze_card.py` - Cloze deletion cards
  - [ ] `create_image_occlusion_card.py` - Image-based cards

### 2.2 Smart Card Creation
- [ ] Create `src/tools/create_anki_card.py`
  - [ ] Analyze content and suggest card type
  - [ ] Guide user through card creation process
  - [ ] Chain to specific card creation tools

### 2.3 Card File Management
- [ ] Create `src/tools/anki_files.py`
  - [ ] Save cards as `.md` files with Anki frontmatter
  - [ ] Load existing card files
  - [ ] Generate `.apkg` files from card collections

## Phase 3: Obsidian Integration

### 3.1 Parse Obsidian Notes for Cards
- [ ] Create `src/tools/obsidian_to_anki.py`
  - [ ] Extract key concepts from notes
  - [ ] Suggest multiple card types per note
  - [ ] Parse headings, definitions, and Q&A sections
  - [ ] Handle image references and file paths

### 3.2 Cloze Detection
- [ ] Implement automatic cloze detection
  - [ ] Identify important terms and concepts
  - [ ] Suggest cloze positions
- [ ] Support manual cloze markup (`{{c1::text}}`)

### 3.3 Bidirectional Linking
- [ ] Add Obsidian URI to Anki cards
- [ ] Option to add Anki card references to Obsidian notes
- [ ] Implement cross-reference tracking

## Phase 4: Advanced Features

### 4.1 Batch Operations
- [ ] Create `src/tools/batch_anki.py`
  - [ ] Batch card creation from multiple notes
  - [ ] Bulk deck operations
  - [ ] Export entire deck collections

### 4.2 Media Support
- [ ] Image file path handling
- [ ] Copy images to Anki media folder
- [ ] Support for audio files (future)

### 4.3 Card Templates
- [ ] Create template system for consistent card formatting
- [ ] Support for custom CSS styling
- [ ] Note type customization

## Phase 5: MCP Integration

### 5.1 Tool Registration
- [ ] Update `src/handlers/note_registrations.py`
  - [ ] Register all Anki tools
  - [ ] Add resource handlers for Anki content
  - [ ] Implement proper error handling

### 5.2 Resource Providers
- [ ] Add Anki card resources
- [ ] Support URI scheme: `anki://deck/card_id`
- [ ] Implement card content serving

## Phase 6: Testing & Documentation

### 6.1 Test Suite
- [ ] Create `tests/test_anki/`
  - [ ] Unit tests for all Anki tools
  - [ ] Integration tests with Obsidian
  - [ ] Mock genanki for testing

### 6.2 Documentation
- [ ] Update README with Anki features
- [ ] Create usage examples
- [ ] Document card creation workflows

## File Structure
```
src/
├── config/
│   └── settings.py          # Add AnkiConfig
├── models/
│   ├── note_models.py       # Existing
│   └── anki_models.py       # New Anki models
├── tools/
│   ├── anki_cards/          # Individual card tools
│   ├── create_anki_card.py  # Smart card creation
│   ├── deck_management.py   # Deck operations
│   ├── obsidian_to_anki.py  # Note parsing
│   └── batch_anki.py        # Batch operations
├── handlers/
│   └── note_registrations.py # Updated with Anki tools
└── utils/
    └── anki_utils.py        # Helper functions
```

## Dependencies to Add
```toml
[project.dependencies]
genanki = ">=1.20.0"
```

## Configuration Example
```python
# In settings.py
class AnkiConfig:
    anki_files_path: str = "./anki_cards"
    default_deck_name: str = "Obsidian Notes"
    include_obsidian_links: bool = True
    auto_create_decks: bool = True
```

## Usage Examples

### Create a basic card
```
Claude: Create an Anki card about Python functions
User: What type of card would you like?
Claude: Based on the content, I suggest a basic card. Here's what I'll create:
Front: What is a Python function?
Back: A reusable block of code that performs a specific task...
```

### Create cards from Obsidian note
```
Claude: Create Anki cards from my "Machine Learning" note
User: I found 5 potential cards in your note. Would you like me to create:
1. Basic card about supervised learning
2. Cloze card about neural networks
3. Basic card about gradient descent
...
```

## Success Criteria
- [ ] Can create all supported card types
- [ ] Generates valid `.apkg` files
- [ ] Integrates seamlessly with existing Obsidian tools
- [ ] Provides intelligent card suggestions
- [ ] Maintains proper deck organization
- [ ] Supports bidirectional linking

## Future Enhancements
- AnkiConnect API integration for automatic syncing
- Advanced media support (audio, video)
- Spaced repetition analytics
- Card review scheduling
- Template marketplace