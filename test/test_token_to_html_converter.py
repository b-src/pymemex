import os
import random
import string

import pytest
from html_converter import TokenToHTMLConverter

@pytest.fixture()
def token_to_html_converter():
    _token_to_html_converter = TokenToHTMLConverter()
    return _token_to_html_converter


def test_token_to_html_converter_handles_h1(token_to_html_converter, tmp_path):
    test_token_list = ["#", " Test H1"]
    expected_result = "<h1> Test H1</h1>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_h2(token_to_html_converter, tmp_path):
    test_token_list = ["##", " Test H2"]
    expected_result = "<h2> Test H2</h2>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_h3(token_to_html_converter, tmp_path):
    test_token_list = ["###", " Test H3"]
    expected_result = "<h3> Test H3</h3>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_h4(token_to_html_converter, tmp_path):
    test_token_list = ["####", " Test H4"]
    expected_result = "<h4> Test H4</h4>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_h5(token_to_html_converter, tmp_path):
    test_token_list = ["#####", " Test H5"]
    expected_result = "<h5> Test H5</h5>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_h6(token_to_html_converter, tmp_path):
    test_token_list = ["######", " Test H6"]
    expected_result = "<h6> Test H6</h6>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_single_linebreak(token_to_html_converter, tmp_path):
    test_token_list = ["\n", "this", "\n", "is", "\n", "a", "\n", "string", "\n", "with", "\n", "single", "\n", "linebreaks"]
    expected_result = "<p>this is a string with single linebreaks</p>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_paragraph_separator(token_to_html_converter, tmp_path):
    test_token_list = ["\n\n", "\n\n", "this is a paragraph", "\n\n", "second paragraph", "\n\n", "\n\n"]
    expected_result = "<p>this is a paragraph</p><p>second paragraph</p>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_explicit_linebreak(token_to_html_converter, tmp_path):
    test_token_list = ["explicit", "\\\\\\", "linebreak"]
    expected_result = "<p>explicit<br />linebreak</p>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_bold(token_to_html_converter, tmp_path):
    test_token_list = ["this is ", "*", "bold", "*", " text"]
    expected_result = "<p>this is <b>bold</b> text</p>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_italic(token_to_html_converter, tmp_path):
    test_token_list = ["this is ", "**", "italic", "**", " text"]
    expected_result = "<p>this is <i>italic</i> text</p>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_bold_italic(token_to_html_converter, tmp_path):
    test_token_list = ["this is ", "***", "bold-italic", "***", " text"]
    expected_result = "<p>this is <b><i>bold-italic</i></b> text</p>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_internal_link(token_to_html_converter, tmp_path):
    test_token_list = ["link here ", "{", "internal link (who knows what this format looks like?)", "}"]
    expected_result = '<p>link here <a href="who knows what this format looks like?">internal link</a></p>'
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_external_link(token_to_html_converter, tmp_path):
    test_token_list = ["link here ", "[", "external link (who knows what this format looks like?)", "]"]
    expected_result = '<p>link here <a href="who knows what this format looks like?">external link</a></p>'
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_quote(token_to_html_converter, tmp_path):
    test_token_list = ["quote incoming ", '""', "blah blah blah (attribution)", '""']
    expected_result = '<p>"blah blah blah" (attribution)</p>'
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_citation(token_to_html_converter, tmp_path):
    test_token_list = ["{{", "source", "}}"]
    expected_result = "[TODO]"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result
    assert False


def test_token_to_html_converter_handles_figure(token_to_html_converter, tmp_path):
    test_token_list = ["[[", "path to figure (description)", "]]"]
    expected_result = '<img src="path to figure" alt="description"'
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_inline_code(token_to_html_converter, tmp_path):
    test_token_list = ["here is some ", "`", "inline code", "`"]
    expected_result = "<p>here is some [TODO]inline code[/TODO]</p>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result
    assert False


def test_token_to_html_converter_handles_multiline_code(token_to_html_converter, tmp_path):
    test_token_list = ["here is some ", "```", "multi", "\n", "line", "\n", "code", "```"]
    expected_result = "<p>here is some [TODO]multi<br />line<br />code[/TODO]</p>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result
    assert False


def test_token_to_html_converter_handles_explicit_backslash(token_to_html_converter, tmp_path):
    test_token_list = ["explicit", "\\\\", "backslash"]
    expected_result = "<p>explicit\\backslash</p>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_explicit_octothorpe(token_to_html_converter, tmp_path):
    test_token_list = ["explicit", "\\#", "octothorpe"]
    expected_result = "<p>explicit#octothorpe</p>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_explicit_asterisk(token_to_html_converter, tmp_path):
    test_token_list = ["explicit", "\\*", "asterisk"]
    expected_result = "<p>explicit*asterisk</p>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_explicit_curly_braces(token_to_html_converter, tmp_path):
    test_token_list = ["\\{", "text in curly braces", "\\}"]
    expected_result = "<p>{text in curly braces}</p>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result


def test_token_to_html_converter_handles_explicit_square_brackets(token_to_html_converter, tmp_path):
    test_token_list = ["\\[", "text in square brackets", "\\]"]
    expected_result = "<p>[text in curly braces]</p>"
    
    assert token_to_html_converter.convert_token_list_to_html(test_token_list) == expected_result
