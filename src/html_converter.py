from collections import deque
from enum import Enum, auto
from typing import TextIO

from markdown_syntax import markdown_symbol_helper, TrieState, END_TOKEN
from memex_logging import memex_logger


class MarkdownToHTMLConverter:
    def __init__(self) -> None:
        self.markdown_tokenizer = MarkdownTokenizer()
        self.token_to_html_converter = TokenToHTMLConverter()

    def convert_file_to_html(self, input_file_path: str, output_file_path: str):
        memex_logger.info(f"Converting input file {input_file_path} to HTML at {output_file_path}")
        with open(input_file_path, mode="r") as markdown_file:
            output_file_token_list = self.markdown_tokenizer.tokenize_markdown(markdown_file)
            output_file_contents = self.token_to_html_converter.convert_token_list_to_html(output_file_token_list)

            with open(output_file_path, mode="x") as output_file:
                output_file.write(output_file_contents)


class TokenizerState(Enum):
    PARSING_SYMBOL = auto()
    CONTENT = auto()
    EOF = auto()
    

class MarkdownTokenizer:
    def __init__(self) -> None:
        self._token_buffer = ""
        self._last_token_buffer_state = TrieState.NOT_FOUND
        self._previous_token_candidate_buffer = ""
        
    def _reset_state_variables(self):
        self._token_buffer = ""
        self._last_token_buffer_state = TrieState.NOT_FOUND
        self._previous_token_candidate_buffer = ""

    def tokenize_markdown(self, input_file: TextIO) -> list[str]:
        self._reset_state_variables()
        self._state = TokenizerState.CONTENT
        
        token_list = []

        while self._state != TokenizerState.EOF:
            char = input_file.read(1)
            if not char:
                self._state = TokenizerState.EOF

            else:
                match self._state:
                    case TokenizerState.CONTENT:
                        symbol_status = markdown_symbol_helper.symbol_trie_lookup(char, markdown_syntax_trie)
                        if symbol_status != TrieState.NOT_FOUND:
                            self._state = TokenizerState.PARSING_SYMBOL
                            self._previous_token_candiate_buffer = self._token_buffer
                            self._token_buffer = char
                            self._last_token_buffer_state = symbol_status
                        else:
                            self._token_buffer += char

                    case TokenizerState.PARSING_SYMBOL:
                        current_symbol = self._token_buffer + char
                        current_symbol_state = markdown_symbol_helper.symbol_trie_lookup(current_symbol, markdown_syntax_trie)
                        char_symbol_state = markdown_symbol_helper.symbol_trie_lookup(char, markdown_syntax_trie)
                        
                        if current_symbol_state == TrieState.NOT_FOUND:
                            if self._last_token_buffer_state == TrieState.EXISTS_PARTIAL:
                                if char_symbol_state == TrieState.NOT_FOUND:
                                    self._token_buffer = self._previous_token_candiate_buffer + current_symbol
                                    self._previous_token_candiate_buffer = ""
                                    self._state = TokenizerState.CONTENT
                                else:
                                    self._previous_token_candiate_buffer = self._previous_token_candiate_buffer + self._token_buffer
                                    self._token_buffer = char
                                    # State is already set to PARSING_SYMBOL

                            elif self._last_token_buffer_state == TrieState.EXISTS_COMPLETE:
                                if self._previous_token_candiate_buffer:
                                    token_list.append(self._previous_token_candiate_buffer)
                                    self._previous_token_candiate_buffer = ""
                                token_list.append(self._token_buffer)
                                self._token_buffer = char
                                if char_symbol_state == TrieState.NOT_FOUND:
                                    self._state = TokenizerState.CONTENT
                                else:
                                    self._state = TokenizerState.PARSING_SYMBOL
                        else:
                            self._token_buffer += char

        # Add anything remaining to token list when EOF is hit
        any_remaining_content = self._previous_token_candiate_buffer + self._token_buffer
        if any_remaining_content:
            token_list.append(any_remaining_content)
                            
        return token_list


class TokenToHTMLConverter:
    def __init__(self):
        pass
    
    def _check_syntax_is_proper(self, token_list: list[str]) -> bool:
        return _check_symbols_that_need_to_be_are_closed_properly(token_list)

    def _check_symbols_that_need_to_be_are_closed_properly(self, token_list: list[str]) -> None:
        expected_closing_symbols = deque()
        for token in token_list:
            if markdown_symbol_helper.symbol_exists(token):
                symbol = markdown_symbol_helper.get_symbol(token)

                if expected_closing_symbols:
                    if symbol.name == expected_closing_symbols[-1]:
                        expected_closing_symbols.pop()
                    else:
                        if symbol.has_closing_symbol():
                            expected_closing_symbols.append(symbol.closing_symbol_name)
                else:
                    if symbol.has_closing_symbol():
                        expected_closing_symbols.append(symbol.closing_symbol_name)
                        
        if expected_closing_symbols:
            raise Exception("Unclosed or improperly nested symbols")

    # TODO: account for multiple tags closed at once
    # TODO: account for paragraphs
    def convert_token_list_to_html(self, token_list: list[str]) -> str:
        self._check_syntax_is_proper(token_list)

        page_content = ""
        expected_closing_symbols = deque()
        closing_tag_stack = deque()
        paragraph_needed_for_next_content = False

        for token in token_list:
            if markdown_symbol_helper.symbol_exists(token):
                symbol = markdown_symbol_helper.get_symbol(token)

                if expected_closing_symbols:
                    if symbol.name == expected_closing_symbols[-1]:
                        expected_closing_symbols.pop()
                        page_content += closing_tag_stack.pop()
                    else:
                        if symbol.has_closing_symbol():
                            expected_closing_symbols.append(symbol.closing_symbol_name)
                            if markdown_symbol.closing_tag is not None:
                                closing_tag_stack.append(markdown_symbol.closing_tag)
                else:
                    if markdown_symbol.opening_tag is not None:
                        page_content += token_open_tag
                    if symbol.has_closing_symbol():
                        expected_closing_symbols.append(symbol.closing_symbol_name)
        
        return page_content
