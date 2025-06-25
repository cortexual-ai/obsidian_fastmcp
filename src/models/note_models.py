from pydantic import BaseModel
from typing import Literal


class ObsidianNote(BaseModel):
    title: str
    content: str
    tags: list[str] = []
    folder: str = ""
    aliases: list[str] = []
    related: list[str] = []
    category: str = ""
    type: Literal[
        "note", "concept", "tool", "person", "framework", "paper", "project"
    ] = "note"
    summary: str = ""
