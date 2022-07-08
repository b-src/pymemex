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


def test_markdown_tokenizer_handles_h2(markdown_tokenizer, tmp_path):
    test_markdown = "## Test H2"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["##", " Test H2"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_h3(markdown_tokenizer, tmp_path):
    test_markdown = "### Test H3"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["###", " Test H3"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_h4(markdown_tokenizer, tmp_path):
    test_markdown = "#### Test H4"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["####", " Test H4"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_h5(markdown_tokenizer, tmp_path):
    test_markdown = "##### Test H5"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["#####", " Test H5"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_h6(markdown_tokenizer, tmp_path):
    test_markdown = "###### Test H6"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["######", " Test H6"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_single_linebreak(markdown_tokenizer, tmp_path):
    test_markdown = "\nthis\nis\na\nstring\nwith\nsingle\nlinebreaks"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["\n", "this", "\n", "is", "\n", "a", "\n", "string", "\n", "with", "\n", "single", "\n", "linebreaks"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_paragraph_separator(markdown_tokenizer, tmp_path):
    test_markdown = "\n\n\n\nthis is a paragraph\n\nsecond paragraph\n\n\n\n"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["\n\n", "\n\n", "this is a paragraph", "\n\n", "second paragraph", "\n\n", "\n\n"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_explicit_linebreak(markdown_tokenizer, tmp_path):
    test_markdown = "explicit\\\\\\linebreak"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["explicit", "\\\\\\", "linebreak"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_bold(markdown_tokenizer, tmp_path):
    test_markdown = "this is *bold* text"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["this is ", "*", "bold", "*", " text"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_italic(markdown_tokenizer, tmp_path):
    test_markdown = "this is **italic** text"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["this is ", "**", "italic", "**", " text"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_bold_italic(markdown_tokenizer, tmp_path):
    test_markdown = "this is ***bold-italic*** text"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["this is ", "**", "bold-italic", "**", " text"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_internal_link(markdown_tokenizer, tmp_path):
    test_markdown = "link here {internal link (who knows what this format looks like?)}"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["link here ", "{", "internal link (who knows what this format looks like?)", "}"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_external_link(markdown_tokenizer, tmp_path):
    test_markdown = "link here [external link (who knows what this format looks like?)]"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["link here ", "[", "external link (who knows what this format looks like?)", "]"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_quote(markdown_tokenizer, tmp_path):
    test_markdown = 'quote incoming ""blah blah blah (attribution)""'
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["quote incoming ", '""', "blah blah blah (attribution)", '""']
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_citation(markdown_tokenizer, tmp_path):
    test_markdown = "{{source}}"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["{{", "source", "}}"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_figure(markdown_tokenizer, tmp_path):
    test_markdown = "[[path to figure (description)]]"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["[[", "path to figure (description)", "]]"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_inline_code(markdown_tokenizer, tmp_path):
    test_markdown = "here is some `inline code`"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["here is some ", "`", "inline code", "`"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_multiline_code(markdown_tokenizer, tmp_path):
    test_markdown = "here is some ```multi\nline\ncode```"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["here is some ", "```", "multi", "\n", "line", "\n", "code", "```"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_explicit_backslash(markdown_tokenizer, tmp_path):
    test_markdown = "explicit\\\\backslash"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["explicit", "\\\\", "backslash"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_explicit_octothorpe(markdown_tokenizer, tmp_path):
    test_markdown = "explicit\\#octothorpe"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["explicit", "\\#", "octothorpe"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_explicit_octothorpe(markdown_tokenizer, tmp_path):
    test_markdown = "explicit\\#octothorpe"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["explicit", "\\#", "octothorpe"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_explicit_asterisk(markdown_tokenizer, tmp_path):
    test_markdown = "explicit\\*asterisk"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["explicit", "\\*", "asterisk"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_explicit_curly_braces(markdown_tokenizer, tmp_path):
    test_markdown = "\\{text in curly braces\\}"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["\\{", "text in curly braces", "\\}"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result


def test_markdown_tokenizer_handles_explicit_square_brackets(markdown_tokenizer, tmp_path):
    test_markdown = "\\[text in square brackets\\]"
    temp_file_path = write_data_to_temp_file(test_markdown, tmp_path)
        
    expected_result = ["\\[", "text in square brackets", "\\]"]
    
    with open(temp_file_path, mode="r") as f:
        assert markdown_tokenizer.tokenize_markdown(f) == expected_result
