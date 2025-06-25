from datetime import datetime
from models.note_models import ObsidianNote
from config.settings import get_vault_path


async def create_note(note: ObsidianNote):
    try:
        vault_path = get_vault_path()

        # Create folder if it doesn't exist
        if note.folder:
            folder_path = vault_path / note.folder
            folder_path.mkdir(parents=True, exist_ok=True)
            file_path = folder_path / f"{note.title}.md"
        else:
            file_path = vault_path / f"{note.title}.md"

        # Format the note content with metadata
        formatted_content = f"""---
title: {note.title}
created: {datetime.now().isoformat()}
modified: {datetime.now().isoformat()}
tags: {", ".join(note.tags)}
aliases: {", ".join(note.aliases)}
related: {", ".join(note.related)}
category: {note.category}
type: {note.type} # one of note, paper, concept, etc.
summary: {note.summary}
---

{note.content}
"""

        # Write the note to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(formatted_content)

        return {
            "message": "Note created successfully",
            "path": str(file_path),
            "title": note.title,
        }

    except Exception as e:
        raise Exception(f"Failed to create note: {str(e)}")
