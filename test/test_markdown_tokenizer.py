import os
import random
import string

import pytest
from html_converter import MarkdownTokenizer

@pytest.fixture()
def markdown_tokenizer():
    _markdown_tokenizer = MarkdownTokenizer()
    return _markdown_tokenizer


def write_data_to_temp_file(data: str, temp_path_root: os.PathLike) -> os.PathLike:
    temp_file_name = "".join(random.choice(string.ascii_lowercase) for i in range(20))
    temp_file_path = os.path.join(temp_path_root, temp_file_name)

    with open(temp_file_path, mode="x") as f:
        f.write(data)
        
    return temp_file_path


def test_markdown_tokenizer_handles_h1(markdown_tokenizer, tmp_path):
    test_markdown = "# Test H1"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["#", " Test H1"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result
