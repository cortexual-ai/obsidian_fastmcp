from pathlib import Path
from typing import List
import yaml
from config.settings import get_vault_path


async def load_all_notes_metadata() -> List[dict]:
    """
    Load metadata from all notes in the Obsidian vault.

    Returns:
        List[dict]: A list of dictionaries containing metadata for each note

    Raises:
        Exception: If there is an error reading the vault or parsing notes
    """
    try:
        vault_path = get_vault_path()
        notes = []

        # Recursively find all .md files
        for file_path in vault_path.rglob("*.md"):
            try:
                # Get relative folder path from vault root
                rel_path = file_path.relative_to(vault_path)
                folder = str(rel_path.parent) if rel_path.parent != Path(".") else ""

                # Read file content
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Parse frontmatter
                frontmatter = {}
                if content.startswith("---"):
                    try:
                        _, fm, _ = content.split("---", 2)
                        frontmatter = yaml.safe_load(fm.strip())
                    except Exception:
                        # Skip files with invalid frontmatter
                        pass

                # Extract title from filename if not in frontmatter
                title = frontmatter.get("title", file_path.stem)

                # Build metadata dict
                metadata = {
                    "title": title,
                    "folder": folder,
                    "tags": frontmatter.get("tags", "").split(", ")
                    if frontmatter.get("tags")
                    else [],
                    "category": frontmatter.get("category", ""),
                    "summary": frontmatter.get("summary", ""),
                    "type": frontmatter.get("type", "note"),
                    "aliases": frontmatter.get("aliases", "").split(", ")
                    if frontmatter.get("aliases")
                    else [],
                    "related": frontmatter.get("related", "").split(", ")
                    if frontmatter.get("related")
                    else [],
                    "created": frontmatter.get("created", ""),
                    "modified": frontmatter.get("modified", ""),
                    "path": str(file_path),
                }

                notes.append(metadata)

            except Exception:
                # Skip files that can't be processed
                continue

        return notes

    except Exception as e:
        raise Exception(f"Failed to load notes metadata: {str(e)}")
