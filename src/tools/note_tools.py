from datetime import datetime
import logging
import yaml
from pathlib import Path
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
        logger.info(f"Writing content to file: {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(formatted_content)
        
        logger.info(f"Note created successfully at: {file_path}")

        return {
            "message": "Note created successfully",
            "path": str(file_path),
            "title": note.title
        }

    except Exception as e:
        logger.error(f"Error creating note: {str(e)}", exc_info=True)
        raise Exception(f"Failed to create note: {str(e)}")

async def read_note(title: str, folder: str = "") -> ObsidianNote:
    """
    Read an Obsidian note from the vault.
    
    Args:
        title (str): The title of the note to read
        folder (str, optional): The folder containing the note. Defaults to "".
        
    Returns:
        ObsidianNote: The parsed note object
        
    Raises:
        Exception: If the note cannot be found or read
    """
    try:
        logger.info(f"Reading note: {title} from folder: {folder}")
        vault_path = get_vault_path()
        
        # Construct the file path
        if folder:
            file_path = vault_path / folder / f"{title}.md"
        else:
            file_path = vault_path / f"{title}.md"
            
        logger.info(f"Reading from file path: {file_path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"Note not found: {file_path}")
            
        # Read the file content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Split frontmatter and content
        if content.startswith("---"):
            _, frontmatter, content = content.split("---", 2)
            frontmatter = yaml.safe_load(frontmatter.strip())
        else:
            frontmatter = {}
            
        # Create ObsidianNote object
        note = ObsidianNote(
            title=title,
            content=content.strip(),
            folder=folder,
            tags=frontmatter.get("tags", "").split(", ") if frontmatter.get("tags") else [],
            aliases=frontmatter.get("aliases", "").split(", ") if frontmatter.get("aliases") else [],
            related=frontmatter.get("related", "").split(", ") if frontmatter.get("related") else [],
            category=frontmatter.get("category", ""),
            type=frontmatter.get("type", "note"),
            summary=frontmatter.get("summary", "")
        )
        
        logger.info(f"Successfully read note: {title}")
        return note
        
    except Exception as e:
        logger.error(f"Error reading note: {str(e)}", exc_info=True)
        raise Exception(f"Failed to read note: {str(e)}")