import re

# Utility function to insert wikilinks for given phrases in markdown content
def insert_wikilinks(content: str, phrases: list[str]) -> str:
    """
    Inserts wikilinks into the content for each phrase found.

    Args:
        content (str): The original markdown content.
        phrases (list[str]): List of phrases to convert into wikilinks.

    Returns:
        str: Modified content with wikilinks inserted.
    """

    def replace_phrase(text, phrase):
        # Escape special regex characters in phrase
        escaped = re.escape(phrase)
        # Regex to find standalone instances of the phrase not already wikilinked
        pattern = r'(?<!\[\[)(' + escaped + r')(?![\]\]])'
        return re.sub(pattern, r'[[\1]]', text)

    for phrase in sorted(phrases, key=len, reverse=True):  # Longest phrases first
        content = replace_phrase(content, phrase)

    return content