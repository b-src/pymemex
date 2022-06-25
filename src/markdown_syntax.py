from enum import Enum, auto
from typing import Optional


END_TOKEN = "END_TOKEN"


class TrieState(Enum):
    EXISTS_PARTIAL = auto()
    EXISTS_COMPLETE = auto()
    NOT_FOUND = auto()


class MarkdownSymbol:
    def __init__(symbol_name: str, markdown_syntax: "str", opening_tag: Optional[str], closing_tag: Optional[str], has_closing_symbol: bool) -> None:
        self.symbol_name = symbol_name
        self.markdown_syntax = markdown_syntax
        self.opening_tag = opening_tag
        self.closing_tag = closing_tag
        self.has_closing_symbol = has_closing_symbol
        

class MarkdownSymbolHelper:
    def __init__(markdown_symbol_list: list[MarkdownSymbol]) -> None:
        self._symbols = markdown_symbol_list
        self._syntax_dict = self._build_syntax_dict()
        self._symbol_name_dict = self._build_symbol_name_dict()
        self._syntax_trie = self._build_syntax_trie()
        
    def _build_syntax_dict() -> dict[str, str]:
        syntax_dict = {}
        for symbol in self._symbols:
            syntax_dict[symbol.markdown_syntax] = symbol
            
        return syntax_dict
        
    def _build_symbol_name_dict() -> dict[str, str]:
        symbol_name_dict = {}
        for symbol in self._symbols:
            syntax_dict[symbol.symbol_name] = symbol
            
        return symbol_name_dict

    def _build_syntax_trie(symbols: dict[str,str]) -> dict[dict]:
        root = dict()
        for symbol in self._symbols:
            current_dict = root
            for char in symbol.markdown_syntax:
                current_dict = current_dict.setdefault(char, {})
            
            current_dict[END_TOKEN] = END_TOKEN

        return root

    def symbol_trie_lookup(value: str, trie: dict[dict]) -> TrieState:
        current_dict = trie
        for char in value:
            if char in current_dict:
                current_dict = current_dict[char]
            else:
                return TrieState.NOT_FOUND
            
        if END_TOKEN in current_dict:
            return TrieState.EXISTS_COMPLETE
        else:
            return TrieState.EXISTS_PARTIAL


_markdown_symbols = [
    MarkdownSymbol("h1", "#", "<h1>", "</h1>", False),
    MarkdownSymbol("h2", "##", "<h2>", "</h2>", False),
    MarkdownSymbol("h3", "###", "<h3>", "</h3>", False),
    MarkdownSymbol("h4", "####", "<h4>", "</h4>", False),
    MarkdownSymbol("h5", "#####", "<h5>", "</h5>", False),
    MarkdownSymbol("h6", "#######", "<h6>", "</h6>", False),
    MarkdownSymbol("paragraph-separator", "\n\n", None, None, False),
    MarkdownSymbol("linebreak", "\\\\\\", "<br />", None, False),
    MarkdownSymbol("bold", "*", "<b>", "</b>", True),
    MarkdownSymbol("italic", "**", "<i>", "</i>", True),
    MarkdownSymbol("bold-italic", "***", "<b><i>", "</i></b>", True),
    MarkdownSymbol("internal-link-start", "{", "<a>", None, False),
    MarkdownSymbol("internal-link-end", "}", None, "</a>", False),
    MarkdownSymbol("external-link-start", "[", "<a>", None, False),
    MarkdownSymbol("external-link-end", "]", None, "</a>", False),
    MarkdownSymbol("quote", '""', None, None, True),
    MarkdownSymbol("citation-start" "{{", None, None, False),
    MarkdownSymbol("citation-end" "}}", None, None, False),
    MarkdownSymbol("figure-start", "[[", None, None, False),
    MarkdownSymbol("figure-end", "]]", None, None, False),
    MarkdownSymbol("inline-code", "`", None, None, True),
    MarkdownSymbol("multiline-code", "```", None, None, True),
    MarkdownSymbol("backslash", "\\\\", "\\", None, False),
    MarkdownSymbol("octothorpe", "\\#", "#", None, False),
    MarkdownSymbol("asterisk", "\\*", "*", None, False),
    MarkdownSymbol("open-curly-brace", "\\{", "{", None, False),
    MarkdownSymbol("close-curly-brace", "\\}", "}", None, False),
    MarkdownSymbol("open-square-bracket" "\\[", "[", None, False),
    MarkdownSymbol("close-square-bracket", "\\]", "]", None, False),
]

markdown_symbol_helper = MarkdownSymbolHelper(_markdown_symbols)
