import os

import pytest
from html_converter import MarkdownTokenizer

@pytest.fixture()
def markdown_tokenizer():
    _markdown_tokenizer = MarkdownTokenizer()
    return _markdown_tokenizer

def test_markdown_tokenizer_handles_h1(markdown_tokenizer, tmp_path):
    test_markdown = "# Test H1"
    temp_file_path = os.path.join(tmp_path, "test_h1")
    with open(temp_file_path, mode="x") as f:
        f.write(test_markdown)
        
    expected_result = ["#", " Test H1"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result
