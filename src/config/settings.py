from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional

# Load environment variables
load_dotenv()


def get_vault_path() -> Path:
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    if not vault_path:
        raise Exception(
            "OBSIDIAN_VAULT_PATH environment variable is not set. Please set it in your .env file."
        )

    # Expand the home directory if using ~
    vault_path = os.path.expanduser(vault_path)
    path = Path(vault_path)

    if not path.exists():
        raise Exception(f"Obsidian vault path does not exist: {vault_path}")

    if not path.is_dir():
        raise Exception(f"Obsidian vault path is not a directory: {vault_path}")

    return path


class AnkiConfig(BaseModel):
    files_path: Path
    default_deck_name: str = Field(default="Obsidian Notes")
    include_obsidian_links: bool = Field(default=True)
    auto_create_decks: bool = Field(default=True)
    export_format: str = Field(default="apkg")
    max_cards_per_deck: Optional[int] = Field(default=None)

    @classmethod
    def create(cls, vault_path: Path) -> AnkiConfig:
        """Create AnkiConfig with smart defaults derived from vault path."""
        # Auto-derive anki_files_path from vault_path
        anki_files_path = os.getenv("ANKI_FILES_PATH")
        if anki_files_path:
            files_path = Path(os.path.expanduser(anki_files_path))
        else:
            files_path = vault_path / "anki_cards"

        # Create directory if it doesn't exist
        try:
            files_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise Exception(
                f"Cannot create Anki files directory at {files_path}: {str(e)}"
            )

        # Validate directory is writable
        if not os.access(files_path, os.W_OK):
            raise Exception(f"Anki files directory is not writable: {files_path}")

        return cls(files_path=files_path)
