# Obsidian FastMCP - Research Capabilities Plan

## Current Tools
- `create_note` - Creates notes with frontmatter metadata
- `read_note` - Reads notes and parses frontmatter 
- `update_note` - Updates existing notes preserving creation date

## Proposed Research-Focused Capabilities

### High Priority Research Tools

#### 1. Paper Management
- `import_paper` - Extract metadata from PDFs/DOIs (title, authors, abstract, journal)
- `cite_paper` - Generate citations in various formats
- `link_papers` - Connect related papers automatically

#### 2. Research Organization
- `create_literature_review` - Aggregate notes by theme/topic
- `extract_quotes` - Pull highlighted text with source attribution
- `research_timeline` - Track paper publication dates and research evolution

#### 3. Knowledge Synthesis
- `find_contradictions` - Identify conflicting findings across papers
- `concept_map` - Visualize relationships between ideas
- `research_gaps` - Identify understudied areas from your notes

#### 4. Enhanced Search
- `semantic_search` - Find conceptually similar content
- `author_network` - Track researchers and their collaborations
- `methodology_search` - Find papers using similar methods

### Additional Capabilities (Lower Priority)

#### Search & Discovery
- `search_notes` - Full-text search across vault content
- `list_notes` - Browse notes by folder/tag/type
- `find_backlinks` - Find notes linking to a specific note

#### Link Management
- `create_link` - Insert wikilinks between notes
- `get_graph_data` - Export note connections for visualization
- `find_orphaned_notes` - Identify notes without connections

#### Bulk Operations
- `batch_tag` - Add/remove tags from multiple notes
- `move_notes` - Reorganize notes between folders
- `duplicate_note` - Create copies with template variations

#### Templates & Automation
- `apply_template` - Use predefined note structures
- `daily_note` - Create date-based notes
- `meeting_note` - Structured meeting templates

## Implementation Notes

- Current note model supports "paper" and "concept" types
- Frontmatter includes tags, aliases, related notes, category, type, and summary
- Focus on research workflow optimization
- Consider domain-specific needs (citation styles, mathematical notation, lab protocols)

## Next Steps

1. Determine research field and specific requirements
2. Prioritize capabilities based on workflow needs
3. Design API interfaces for selected tools
4. Implement core research tools first
5. Add advanced features incrementally