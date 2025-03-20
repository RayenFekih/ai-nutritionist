from ai_nutritionist.graph.utils.helpers import remove_asterisk_content


class TestRemoveAsteriskContent:

    # Removes content between a pair of asterisks
    def test_removes_content_between_asterisks(self):

        # Test with a simple string containing asterisks
        input_text = "Hello *world* how are you?"
        expected_output = "Hello  how are you?"
        result = remove_asterisk_content(input_text)
        assert result == expected_output

        # Test with multiple asterisk pairs
        input_text = "Start *remove this* middle *and this too* end"
        expected_output = "Start  middle  end"
        result = remove_asterisk_content(input_text)
        assert result == expected_output

    # Handles empty string input
    def test_handles_empty_string(self):
        # Test with empty string
        input_text = ""
        expected_output = ""
        result = remove_asterisk_content(input_text)
        assert result == expected_output

        # Test with only whitespace
        input_text = "   "
        expected_output = ""
        result = remove_asterisk_content(input_text)
        assert result == expected_output

    # Handles multiple pairs of asterisks in the same string
    def test_removes_multiple_asterisk_pairs(self):
        # Test with multiple pairs of asterisks in the string
        input_text = "This *should* be *removed* and *this* too"
        expected_output = "This  be  and  too"
        result = remove_asterisk_content(input_text)
        assert result == expected_output

    # Returns the original string when no asterisks are present
    def test_returns_original_string_when_no_asterisks(self):
        # Test with a string that contains no asterisks
        input_text = "This is a simple test string."
        expected_output = "This is a simple test string."
        result = remove_asterisk_content(input_text)
        assert result == expected_output

    # Strips leading and trailing whitespace from the result
    def test_strips_leading_and_trailing_whitespace(self):
        # Test with leading and trailing whitespace
        input_text = "   *remove this*   "
        expected_output = ""
        result = remove_asterisk_content(input_text)
        assert result == expected_output

        # Test with content and surrounding whitespace
        input_text = "   Hello *world*   "
        expected_output = "Hello"
        result = remove_asterisk_content(input_text)
        assert result == expected_output
