from enum import Enum, auto
from typing import TextIO

from markdown_syntax import markdown_syntax_dict, markdown_syntax_trie, trie_lookup, TrieState, END_TOKEN
from memex_logging import memex_logger


class ElementTreeNode:
    def __init__(self, token, content, parent=None) -> None:
        self.token = token
        self.content = content
        self.children = []
        self.parent = parent
        
    def __str__(self):
        string = f"ElementTreeNode with token {self.token} and content {self.content}\n\n"
        for child in self.children:
            string += f"Has child: {child}"
 
        return string
    

class MarkdownToHTMLConverter:
    def __init__(self) -> None:
        self.markdown_tokenizer = MarkdownTokenizer()

    def convert_file_to_html(self, input_file_path: str, output_file_path: str):
        memex_logger.info(f"Converting input file {input_file_path} to HTML at {output_file_path}")
        with open(input_file_path, mode="r") as markdown_file:
            output_file_element_tree_root = self.markdown_tokenizer.tokenize_markdown(markdown_file)
            output_file_contents = str(output_file_element_tree_root)

            with open(output_file_path, mode="x") as output_file:
                output_file.write(output_file_contents)
                output_file.write("\n\nfile has been processed.")
                
                
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

    def tokenize_markdown(self, input_file: TextIO) -> ElementTreeNode:
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
                        symbol_status = trie_lookup(char, markdown_syntax_trie)
                        if symbol_status != TrieState.NOT_FOUND:
                            self._state = TokenizerState.PARSING_SYMBOL
                            self._previous_token_candiate_buffer = self._token_buffer
                            self._token_buffer = char
                            self._last_token_buffer_state = symbol_status
                        else:
                            self._token_buffer += char

                    case TokenizerState.PARSING_SYMBOL:
                        current_symbol = self._token_buffer + char
                        current_symbol_state = trie_lookup(current_symbol, markdown_syntax_trie)
                        char_symbol_state = trie_lookup(char, markdown_syntax_trie)
                        
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
