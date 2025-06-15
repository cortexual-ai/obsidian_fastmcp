from datetime import datetime
from pathlib import Path
import re
from ..models.note_models import ObsidianNote
from ..config.settings import get_vault_path

async def create_note(note: ObsidianNote):
    try:
        vault_path = get_vault_path()
        print(f"Vault path from env: {vault_path}")  # Debug log

        # Create folder if it doesn't exist
        if note.folder:
            folder_path = vault_path / note.folder
            folder_path.mkdir(parents=True, exist_ok=True)
            file_path = folder_path / f"{note.title}.md"
        else:
            file_path = vault_path / f"{note.title}.md"
        
        print(f"File will be created at: {file_path}")  # Debug log

        # Format the note content with metadata
        formatted_content = f"""---
title: {note.title}
created: {datetime.now().isoformat()}
modified: {datetime.now().isoformat()}
tags: {', '.join(note.tags)}
aliases: {', '.join(note.aliases)}
related: {', '.join(note.related)}
category: {note.category}
type: {note.type} # one of note, paper, concept, etc.
summary: {note.summary}
---

{note.content}
"""

        # Write the note to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(formatted_content)
        
        print(f"File created successfully at: {file_path}")  # Debug log

        return {
            "message": "Note created successfully",
            "path": str(file_path),
            "title": note.title
        }

    except Exception as e:
        print(f"Error creating note: {str(e)}")  # Debug log
        raise Exception(str(e))

async def create_linked_notes(note_path: str):
    try:
        vault_path = get_vault_path()
        full_note_path = vault_path / note_path

        if not full_note_path.exists():
            raise Exception(f"Note not found at {note_path}")

        # Read the note content
        with open(full_note_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract the title from the frontmatter
        title_match = re.search(r'title:\s*(.+?)\n', content)
        if not title_match:
            raise Exception("Could not find title in note")
        original_title = title_match.group(1).strip()

        # Find potential keywords (words that start with capital letters and are not already in wikilinks)
        words = re.findall(r'\b[A-Z][a-z]+\b', content)
        existing_links = re.findall(r'\[\[(.*?)\]\]', content)
        potential_keywords = [word for word in words if word not in existing_links]

        created_notes = []
        for keyword in potential_keywords:
            # Create a new note for each keyword
            note_content = f"""---
title: {keyword}
created: {datetime.now().isoformat()}
modified: {datetime.now().isoformat()}
tags: [concept]
type: concept
summary: A note about {keyword}
---

# {keyword}

This note is related to [[{original_title}]].

## Definition
[Add definition here]

## Key Points
- [Add key points here]

## Related Concepts
- [[{original_title}]]
"""

            # Create the note using the existing create_note function
            new_note = ObsidianNote(
                title=keyword,
                content=note_content,
                tags=["concept"],
                type="concept",
                summary=f"A note about {keyword}"
            )
            
            result = await create_note(new_note)
            created_notes.append(result)

        return {
            "message": f"Created {len(created_notes)} linked notes",
            "created_notes": created_notes
        }

    except Exception as e:
        print(f"Error creating linked notes: {str(e)}")
        raise Exception(str(e)) 