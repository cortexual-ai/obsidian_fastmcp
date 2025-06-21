"""
Tests for wikilinks utility function.
"""
from utilities.insert_wikilinks import insert_wikilinks


class TestInsertWikilinks:
    """Test cases for the insert_wikilinks function."""

    def test_basic_wikilink_insertion(self):
        """Test basic insertion of wikilinks for simple phrases."""
        content = "This is about Python programming and machine learning."
        phrases = ["Python", "machine learning"]
        result = insert_wikilinks(content, phrases)
        expected = "This is about [[Python]] programming and [[machine learning]]."
        assert result == expected

    def test_no_phrases_returns_original(self):
        """Test that empty phrases list returns original content."""
        content = "This is some content."
        phrases = []
        result = insert_wikilinks(content, phrases)
        assert result == content

    def test_phrase_not_found_returns_original(self):
        """Test that phrases not in content don't modify the text."""
        content = "This is about Python programming."
        phrases = ["JavaScript", "Ruby"]
        result = insert_wikilinks(content, phrases)
        assert result == content

    def test_already_wikilinked_phrases_ignored(self):
        """Test that already wikilinked phrases are not double-linked."""
        content = "This is about [[Python]] programming and machine learning."
        phrases = ["Python", "machine learning"]
        result = insert_wikilinks(content, phrases)
        expected = "This is about [[Python]] programming and [[machine learning]]."
        assert result == expected

    def test_partial_wikilink_not_confused(self):
        """Test that partial wikilinks don't interfere with detection."""
        content = "This is about [Python] and machine learning."
        phrases = ["Python", "machine learning"]
        result = insert_wikilinks(content, phrases)
        # [Python] should become [[[Python]]] since it's not a wikilink
        expected = "This is about [[[Python]]] and [[machine learning]]."
        assert result == expected

    def test_case_sensitive_matching(self):
        """Test that phrase matching is case-sensitive."""
        content = "This is about python programming and Python frameworks."
        phrases = ["Python"]
        result = insert_wikilinks(content, phrases)
        expected = "This is about python programming and [[Python]] frameworks."
        assert result == expected

    def test_word_boundary_matching(self):
        """Test that phrases match as complete words, not substrings."""
        content = "This is about Python programming and scripting."
        phrases = ["script"]
        result = insert_wikilinks(content, phrases)
        # "script" should not match "scripting"
        assert result == content

    def test_multiple_occurrences(self):
        """Test that all occurrences of a phrase get wikilinked."""
        content = "Python is great. I love Python. Python rocks!"
        phrases = ["Python"]
        result = insert_wikilinks(content, phrases)
        expected = "[[Python]] is great. I love [[Python]]. [[Python]] rocks!"
        assert result == expected

    def test_overlapping_phrases_longest_first(self):
        """Test that longer phrases take precedence over shorter ones."""
        content = "This is about machine learning algorithms."
        phrases = ["machine", "machine learning"]
        result = insert_wikilinks(content, phrases)
        expected = "This is about [[machine learning]] algorithms."
        assert result == expected

    def test_special_regex_characters_escaped(self):
        """Test that phrases with special regex characters are handled correctly."""
        content = "The cost is $100 (including tax)."
        phrases = ["$100", "(including tax)"]
        result = insert_wikilinks(content, phrases)
        expected = "The cost is [[$100]] [[(including tax)]]."
        assert result == expected

    def test_punctuation_boundaries(self):
        """Test that phrases are matched correctly with punctuation boundaries."""
        content = "Python, JavaScript, and C++ are programming languages."
        phrases = ["Python", "JavaScript", "C++"]
        result = insert_wikilinks(content, phrases)
        expected = "[[Python]], [[JavaScript]], and [[C++]] are programming languages."
        assert result == expected

    def test_multiline_content(self):
        """Test that wikilinks work across multiple lines."""
        content = """This is a document about Python.

Python is a programming language.
It's used for machine learning."""
        phrases = ["Python", "machine learning"]
        result = insert_wikilinks(content, phrases)
        expected = """This is a document about [[Python]].

[[Python]] is a programming language.
It's used for [[machine learning]]."""
        assert result == expected

    def test_empty_content(self):
        """Test that empty content is handled gracefully."""
        content = ""
        phrases = ["Python"]
        result = insert_wikilinks(content, phrases)
        assert result == ""

    def test_empty_phrase_in_list(self):
        """Test that empty phrases in the list don't cause issues."""
        content = "This is about Python programming."
        phrases = ["", "Python", ""]
        result = insert_wikilinks(content, phrases)
        expected = "This is about [[Python]] programming."
        assert result == expected

    def test_complex_phrase_with_spaces(self):
        """Test phrases with multiple words and spaces."""
        content = "Artificial intelligence and natural language processing are related."
        phrases = ["Artificial intelligence", "natural language processing"]
        result = insert_wikilinks(content, phrases)
        expected = "[[Artificial intelligence]] and [[natural language processing]] are related."
        assert result == expected

    def test_nested_brackets_in_content(self):
        """Test content that already has various bracket types."""
        content = "Python [version 3.9] supports {dict: comprehensions} and (list comprehensions)."
        phrases = ["Python", "dict", "list"]
        result = insert_wikilinks(content, phrases)
        expected = "[[Python]] [version 3.9] supports {[[dict]]: comprehensions} and ([[list]] comprehensions)."
        assert result == expected

    def test_phrase_at_beginning_and_end(self):
        """Test phrases at the beginning and end of content."""
        content = "Python is awesome and I love Python"
        phrases = ["Python"]
        result = insert_wikilinks(content, phrases)
        expected = "[[Python]] is awesome and I love [[Python]]"
        assert result == expected