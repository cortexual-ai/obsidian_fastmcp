import logging
from tools.read_note import read_note
from tools.update_note import update_note
from utils.insert_wikilinks import insert_wikilinks

logger = logging.getLogger(__name__)


async def insert_wikilinks_in_note(title: str, phrases: list[str], folder: str = ""):
    """
    Insert wikilinks for specified phrases in an existing note.

    Args:
        title (str): The title of the note to modify
        phrases (list[str]): List of phrases to convert to wikilinks
        folder (str, optional): The folder containing the note. Defaults to "".

    Returns:
        dict: A dictionary containing the update status and modified content info

    Raises:
        Exception: If the note cannot be found, read, or updated
    """
    try:
        logger.info(f"Starting wikilinks insertion for note: {title}")
        logger.info(f"Phrases to link: {phrases}")

        # Read the existing note
        note = await read_note(title, folder)

        # Apply wikilinks to the content
        original_content = note.content
        modified_content = insert_wikilinks(original_content, phrases)

        # Check if any changes were made
        if original_content == modified_content:
            logger.info("No changes made - phrases not found or already linked")
            return {
                "message": "No changes made - phrases not found or already linked",
                "title": title,
                "phrases_processed": phrases,
                "changes_made": False,
            }

        # Update the note with modified content
        note.content = modified_content
        update_result = await update_note(note)

        logger.info(f"Successfully inserted wikilinks in note: {title}")

        return {
            "message": "Wikilinks inserted successfully",
            "title": title,
            "phrases_processed": phrases,
            "changes_made": True,
            "path": update_result["path"],
            "original_length": len(original_content),
            "modified_length": len(modified_content),
        }

    except Exception as e:
        logger.error(f"Error inserting wikilinks in note: {str(e)}", exc_info=True)
        raise Exception(f"Failed to insert wikilinks in note: {str(e)}")
