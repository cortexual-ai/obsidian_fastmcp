from datetime import datetime
import logging
from models.note_models import ObsidianNote
from config.settings import get_vault_path

logger = logging.getLogger(__name__)


async def create_note(note: ObsidianNote):
    try:
        logger.info(f"Starting note creation for title: {note.title}")
        vault_path = get_vault_path()
        logger.info(f"Vault path: {vault_path}")

        # Create folder if it doesn't exist
        if note.folder:
            folder_path = vault_path / note.folder
            logger.info(f"Creating folder path: {folder_path}")
            folder_path.mkdir(parents=True, exist_ok=True)
            file_path = folder_path / f"{note.title}.md"
        else:
            file_path = vault_path / f"{note.title}.md"

        logger.info(f"Target file path: {file_path}")

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
        logger.info(f"Writing content to file: {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(formatted_content)

        logger.info(f"Note created successfully at: {file_path}")

        return {
            "message": "Note created successfully",
            "path": str(file_path),
            "title": note.title,
        }

    except Exception as e:
        logger.error(f"Error creating note: {str(e)}", exc_info=True)
        raise Exception(f"Failed to create note: {str(e)}")
