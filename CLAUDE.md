# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Essential Commands
- **Activate environment**: `source .venv/bin/activate`
- **Install for Claude Desktop**: `fastmcp install src/main.py`
- **Run tests**: `pytest` (after activating venv)
- **Lint code**: `ruff check . && ruff format .`
- **Type checking**: `mypy src/`
- **Run single test**: `pytest tests/test_specific.py::test_function`

### Testing & Quality Assurance
Always run these before committing:
1. `source .venv/bin/activate`
2. `ruff check . && ruff format .`
3. `mypy src/`
4. `pytest`

## Architecture Overview

This is an **Obsidian FastMCP server** that bridges Claude Desktop with Obsidian vaults for AI-powered note management.

### Core Architecture Pattern
```
src/
    main.py              # FastMCP server entry point
    config/settings.py   # Environment configuration
    models/              # Pydantic data models
    handlers/            # FastMCP @mcp.tool wrappers
    tools/              # Core business logic (async functions)
    utils/              # Shared utilities
```

### Key Components

**Configuration Layer (`src/config/`)**:
- Environment-based configuration with `OBSIDIAN_VAULT_PATH`
- Handles path expansion (`~`) and validation
- Centralized logging setup

**Data Models (`src/models/note_models.py`)**:
- `ObsidianNote`: Rich Pydantic model with YAML frontmatter support
- Supports metadata: tags, aliases, related notes, categories, note types
- Type system: note, concept, tool, person, framework, paper, project

**Tool Layer (`src/tools/`)**:
- `create_note.py`: Creates notes with YAML frontmatter
- `read_note.py`: Parses notes with frontmatter extraction
- `update_note.py`: Updates notes preserving creation timestamps
- `load_metadata.py`: Aggregates vault-wide metadata
- `insert_wikilinks_note.py`: Intelligent wikilink insertion

**Handler Layer (`src/handlers/note_registrations.py`)**:
- FastMCP tool registration with `@mcp.tool` decorators
- Wraps core tools for MCP compatibility
- Comprehensive error handling

## Code Style Standards

- **KISS principle**: Keep implementations simple and straightforward
- **Composition over inheritance**: Prefer functions over classes
- **Strong type hints**: Use Pydantic models and proper Python typing
- **Async/await**: All tool functions are async
- **Structured logging**: Use logger with proper error handling and `exc_info=True`
- **Environment config**: Use `.env` files and `os.getenv()`

## Testing Architecture

- **Test framework**: pytest with async support (`pytest-asyncio`)
- **Test isolation**: Temporary vault fixture for each test
- **Coverage**: 20+ test cases covering core functionality
- **Mocking**: FastMCP client/server testing infrastructure
- **Edge cases**: Whitespace handling, error conditions, file operations

## Repository Etiquette

### Development Workflow
- Always start from latest main
```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

- Develop and commit
```bash
# Make your changes
git add .
git commit -m "Clear, descriptive commit message"

# Push branch to GitHub
git push origin feature/your-feature-name
```
- Once PR is merged, clean up
```bash
# Switch back to main and update
git checkout main
git pull origin main

# Delete local feature branch
git branch -d feature/your-feature-name

# Delete remote branch (if not auto-deleted)
git push origin --delete feature/your-feature-name
```

### Development Guidelines
- When working on a new implementation, please work on a new branch

## Future Development Plans

The project includes detailed plans for:
- **Anki Integration**: Flashcard generation from notes
- **Academic Paper Server**: arXiv/PubMed integration
- **Research Capabilities**: Literature review and synthesis

## Environment Setup

Create `.env` file:
```
OBSIDIAN_VAULT_PATH=~/Desktop/work_vault
PYTHONPATH=/absolute/path/to/project/root
```

The project uses **uv** for package management with `uv.lock` for reproducible builds.
```

The project uses Python>=3.13 and can use modern typing syntax.