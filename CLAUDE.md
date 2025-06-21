# Claude Code Collaboration Contract

This document establishes the working contract between the user and Claude Code for implementing features in the obsidian_fastmcp repository.

## Project Overview
This is an Obsidian FastMCP server that provides tools for interacting with Obsidian vaults. The project integrates tools from various MCPs (Obsidian, Anki, Zotero) while maintaining a consistent codebase style.

## Codebase Architecture & Patterns

### Current Structure
- `src/main.py`: FastMCP server setup with graceful shutdown handling
- `src/config/settings.py`: Environment-based configuration (OBSIDIAN_VAULT_PATH)
- `src/models/`: Pydantic models with strong typing (ObsidianNote)
- `src/handlers/`: FastMCP tool registration wrappers
- `src/tools/`: Core business logic implementations
- `src/utils/`: Helper utilities

### Code Style Standards
- **KISS principle**: Keep implementations simple and straightforward
- **Composition over inheritance**: Prefer functions over classes
- **Strong type hints**: Use Pydantic models and proper Python typing
- **Async/await**: All tool functions are async
- **Structured logging**: Use logger with proper error handling and exc_info=True
- **Environment config**: Use .env files and os.getenv()
- **YAML frontmatter**: Obsidian notes use YAML metadata blocks

### File Organization Pattern
```
handlers/: FastMCP @mcp.tool decorators that wrap core functions
tools/: Core business logic functions (async)
models/: Pydantic data models
config/: Configuration and settings
utils/: Shared utility functions
```

## Implementation Workflow

### For Each New Feature
1. **Pre-Planning Phase**
   - **Check for useful MCPs**: Before starting any task, evaluate if there are MCPs that would be helpful (GitHub, context7, etc.)
   - **Request MCP setup**: If useful MCPs are identified but not available, help user set them up first
   - **Verify MCP availability**: Confirm required MCPs are configured and accessible

2. **Planning Phase**
   - Use TodoWrite tool to create detailed task breakdown
   - Ask user for GitHub repo links to analyze external MCP implementations
   - Analyze external patterns vs current codebase patterns
   - Ask user for guidance when conflicts arise

3. **Implementation Phase**
   - Always implement in a new git branch
   - Always activate environment via `source .venv/bin/activate`
   - Follow existing code patterns and architecture
   - Implement async functions with proper error handling
   - Use structured logging throughout
   - Maintain type safety with Pydantic models
   - Keep functions simple and focused

4. **Quality Assurance**
   - Run `ruff` for linting
   - Run `mypy` for type checking
   - Write tests after implementation
   - Commit significant updates
   - Ask user for approval before major testing phases

5. **Testing & Deployment**
   - User tests via `fastmcp install <path>` and Claude Desktop
   - User provides feedback from user perspective
   - Make adjustments based on user testing

### External MCP Integration
- User provides GitHub repo links for reference
- Analyze their tool implementations first
- Adapt their patterns to match our codebase style
- When unsure about design decisions, ask user with recommendations
- User may copy/paste specific implementations when needed

### Commit Strategy
- Commit changes as work progresses
- Ask for user approval before significant milestones
- Request user testing after major feature completion
- Never commit without explicit user approval for testing phases

### Communication Protocol
- Create todo lists for complex/multi-step tasks
- Ask questions when external patterns conflict with current style
- Present options with recommendations for design decisions
- Keep user informed of progress through todo list updates
- Request approval before user testing phases

## Quality Standards

### Code Quality
- All functions must have proper type hints
- Use Pydantic models for data validation
- Implement proper error handling with logging
- Follow async/await patterns consistently
- Maintain clean separation between handlers, tools, and models

### Testing Standards
- Write tests after implementation
- User performs integration testing via Claude Desktop
- Address feedback iteratively
- Run linting (ruff) and type checking (mypy) before commits

### Documentation Standards
- Use clear docstrings for functions
- Log important operations with structured logging
- Maintain this contract document as collaboration evolves

## Tools & Commands
- **Linting**: `ruff`
- **Type checking**: `mypy`
- **Installation/Testing**: `fastmcp install <path>`
- **User testing environment**: Claude Desktop client

## Available MCPs
- **GitHub MCP**: Official GitHub server for repository access
  - Installation: `npm install -g @modelcontextprotocol/server-github`
  - Config: Add to `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Requires: GitHub Personal Access Token
- **Other useful MCPs**: Evaluate context7, filesystem, database MCPs as needed

## Decision Making
- Claude asks user when external MCP patterns conflict with current codebase
- User provides guidance on design decisions
- Focus on maintaining consistency with existing patterns
- Prioritize simplicity and maintainability

This contract ensures smooth collaboration while maintaining code quality and consistency across the project.