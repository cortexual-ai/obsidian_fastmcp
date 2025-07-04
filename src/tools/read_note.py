import yaml
from models.note_models import ObsidianNote
from config.settings import get_vault_path


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
        vault_path = get_vault_path()

        # Clean the title by stripping whitespace but preserving internal spaces
        cleaned_title = title.strip()
        if not cleaned_title:
            raise ValueError("Note title cannot be empty or whitespace only")

        # Construct the file path
        if folder:
            folder_path = vault_path / folder.strip()
            if not folder_path.exists():
                raise FileNotFoundError(f"Folder not found: {folder_path}")
            file_path = folder_path / f"{cleaned_title}.md"
        else:
            file_path = vault_path / f"{cleaned_title}.md"

        if not file_path.exists():
            raise FileNotFoundError(f"Note not found: {file_path}")

        # Read the file content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split frontmatter and content
        if content.startswith("---"):
            _, frontmatter_text, content = content.split("---", 2)
            frontmatter = yaml.safe_load(frontmatter_text.strip()) or {}
        else:
            frontmatter = {}

        # Create ObsidianNote object
        note = ObsidianNote(
            title=cleaned_title,
            content=content.strip(),
            folder=folder.strip() if folder else "",
            tags=frontmatter.get("tags", "").split(", ")
            if frontmatter.get("tags")
            else [],
            aliases=frontmatter.get("aliases", "").split(", ")
            if frontmatter.get("aliases")
            else [],
            related=frontmatter.get("related", "").split(", ")
            if frontmatter.get("related")
            else [],
            category=frontmatter.get("category") or "",
            type=frontmatter.get("type", "note"),
            summary=frontmatter.get("summary") or "",
        )

        return note

    except Exception as e:
        raise Exception(f"Failed to read note: {str(e)}")
