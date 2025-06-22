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
        # Skip empty phrases
        if not phrase or not phrase.strip():
            return text
            
        # Escape special regex characters in phrase
        escaped = re.escape(phrase)
        
        # Find exact phrase matches that aren't already wikilinked
        # Use word boundaries for alphanumeric phrases, exact match for others
        if re.match(r'^\w+$', phrase):
            # Simple word - use word boundaries
            pattern = r'(?<!\[\[)\b(' + escaped + r')\b(?!\]\])'
        else:
            # Complex phrase or special characters - use exact match
            pattern = r'(?<!\[\[)(' + escaped + r')(?!\]\])'
        
        def replacement(match):
            # Check if this match is inside existing wikilinks
            start_pos = match.start()
            
            # Look backward for unclosed [[
            before_text = text[:start_pos]
            open_brackets = before_text.count('[[') - before_text.count(']]')
            
            # If we're inside wikilinks, don't replace
            if open_brackets > 0:
                return match.group(1)
            else:
                return f'[[{match.group(1)}]]'
        
        return re.sub(pattern, replacement, text)

    # Filter out empty phrases and sort by length (longest first)
    valid_phrases = [p for p in phrases if p and p.strip()]
    for phrase in sorted(valid_phrases, key=len, reverse=True):
        content = replace_phrase(content, phrase)

    return content