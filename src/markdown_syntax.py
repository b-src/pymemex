from enum import Enum, auto
from typing import Optional


END_TOKEN = "END_TOKEN"


class TrieState(Enum):
    EXISTS_PARTIAL = auto()
    EXISTS_COMPLETE = auto()
    NOT_FOUND = auto()


class MarkdownSymbol:
    def __init__(self, symbol_name: str, markdown_syntax: "str", opening_tag: Optional[str], closing_tag: Optional[str], closing_symbol_name: Optional[str]) -> None:
        self.name = symbol_name
        self.markdown_syntax = markdown_syntax
        self.opening_tag = opening_tag
        self.closing_tag = closing_tag
        self.closing_symbol_name = closing_symbol_name
    
    def has_closing_symbol(self) -> bool:
        return self.closing_symbol_name is not None


class MarkdownSymbolHelper:
    def __init__(self, markdown_symbol_list: list[MarkdownSymbol]) -> None:
        self._symbols = markdown_symbol_list
        self._syntax_dict = self._build_syntax_dict()
        self._symbol_name_dict = self._build_symbol_name_dict()
        self._syntax_trie = self._build_syntax_trie()
        
    def _build_syntax_dict(self) -> dict[str, str]:
        syntax_dict = {}
        for symbol in self._symbols:
            syntax_dict[symbol.markdown_syntax] = symbol
            
        return syntax_dict
        
    def _build_symbol_name_dict(self) -> dict[str, str]:
        symbol_name_dict = {}
        for symbol in self._symbols:
            symbol_name_dict[symbol.name] = symbol
            
        return symbol_name_dict

    def _build_syntax_trie(self) -> dict[dict]:
        root = dict()
        for symbol in self._symbols:
            current_dict = root
            for char in symbol.markdown_syntax:
                current_dict = current_dict.setdefault(char, {})
            
            current_dict[END_TOKEN] = END_TOKEN

        return root

    def symbol_trie_lookup(self, value: str) -> TrieState:
        current_dict = self._syntax_trie
        for char in value:
            if char in current_dict:
                current_dict = current_dict[char]
            else:
                return TrieState.NOT_FOUND
            
        if END_TOKEN in current_dict:
            return TrieState.EXISTS_COMPLETE
        else:
            return TrieState.EXISTS_PARTIAL
        
    def symbol_exists(self, symbol: str) -> bool:
        return symbol in self._syntax_dict
    
    def get_symbol(self, symbol: str) -> MarkdownSymbol:
        return self._syntax_dict[symbol]


_markdown_symbols = [
    MarkdownSymbol(symbol_name="h1", markdown_syntax="#", opening_tag="<h1>", closing_tag="</h1>", closing_symbol_name="single-linebreak"),
    MarkdownSymbol(symbol_name="h2", markdown_syntax="##", opening_tag="<h2>", closing_tag="</h2>", closing_symbol_name="single-linebreak"),
    MarkdownSymbol(symbol_name="h3", markdown_syntax="###", opening_tag="<h3>", closing_tag="</h3>", closing_symbol_name="single-linebreak"),
    MarkdownSymbol(symbol_name="h4", markdown_syntax="####", opening_tag="<h4>", closing_tag="</h4>", closing_symbol_name="single-linebreak"),
    MarkdownSymbol(symbol_name="h5", markdown_syntax="#####", opening_tag="<h5>", closing_tag="</h5>", closing_symbol_name="single-linebreak"),
    MarkdownSymbol(symbol_name="h6", markdown_syntax="######", opening_tag="<h6>", closing_tag="</h6>", closing_symbol_name="single-linebreak"),
    MarkdownSymbol(symbol_name="single-linebreak", markdown_syntax="\n", opening_tag=None, closing_tag=None, closing_symbol_name=None),
    MarkdownSymbol(symbol_name="paragraph-separator", markdown_syntax="\n\n", opening_tag=None, closing_tag=None, closing_symbol_name=None),
    MarkdownSymbol(symbol_name="explicit-linebreak", markdown_syntax="\\\\\\", opening_tag="<br />", closing_tag=None, closing_symbol_name=None),
    MarkdownSymbol(symbol_name="bold", markdown_syntax="*", opening_tag="<b>", closing_tag="</b>", closing_symbol_name="bold"),
    MarkdownSymbol(symbol_name="italic", markdown_syntax="**", opening_tag="<i>", closing_tag="</i>", closing_symbol_name="italic"),
    MarkdownSymbol(symbol_name="bold-italic", markdown_syntax="***", opening_tag="<b><i>", closing_tag="</i></b>", closing_symbol_name="bold-italic"),
    MarkdownSymbol(symbol_name="internal-link-start", markdown_syntax="{", opening_tag="<a>", closing_tag=None, closing_symbol_name="internal-link-end"),
    MarkdownSymbol(symbol_name="internal-link-end", markdown_syntax="}", opening_tag=None, closing_tag="</a>", closing_symbol_name=None),
    MarkdownSymbol(symbol_name="external-link-start", markdown_syntax="[", opening_tag="<a>", closing_tag=None, closing_symbol_name="external-link-end"),
    MarkdownSymbol(symbol_name="external-link-end", markdown_syntax="]", opening_tag=None, closing_tag="</a>", closing_symbol_name=None),
    MarkdownSymbol(symbol_name="quote", markdown_syntax='""', opening_tag=None, closing_tag=None, closing_symbol_name="quote"),
    MarkdownSymbol(symbol_name="citation-start", markdown_syntax="{{", opening_tag=None, closing_tag=None, closing_symbol_name="citation-end"),
    MarkdownSymbol(symbol_name="citation-end", markdown_syntax="}}", opening_tag=None, closing_tag=None, closing_symbol_name=None),
    MarkdownSymbol(symbol_name="figure-start", markdown_syntax="[[", opening_tag=None, closing_tag=None, closing_symbol_name="figure-end"),
    MarkdownSymbol(symbol_name="figure-end", markdown_syntax="]]", opening_tag=None, closing_tag=None, closing_symbol_name=None),
    MarkdownSymbol(symbol_name="inline-code", markdown_syntax="`", opening_tag=None, closing_tag=None, closing_symbol_name="inline-code"),
    MarkdownSymbol(symbol_name="multiline-code", markdown_syntax="```", opening_tag=None, closing_tag=None, closing_symbol_name="multiline-code"),
    MarkdownSymbol(symbol_name="backslash", markdown_syntax="\\\\", opening_tag="\\", closing_tag=None, closing_symbol_name=None),
    MarkdownSymbol(symbol_name="octothorpe", markdown_syntax="\\#", opening_tag="#", closing_tag=None, closing_symbol_name=None),
    MarkdownSymbol(symbol_name="asterisk", markdown_syntax="\\*", opening_tag="*", closing_tag=None, closing_symbol_name=None),
    MarkdownSymbol(symbol_name="open-curly-brace", markdown_syntax="\\{", opening_tag="{", closing_tag=None, closing_symbol_name=None),
    MarkdownSymbol(symbol_name="close-curly-brace", markdown_syntax="\\}", opening_tag="}", closing_tag=None, closing_symbol_name=None),
    MarkdownSymbol(symbol_name="open-square-bracket", markdown_syntax="\\[", opening_tag="[", closing_tag=None, closing_symbol_name=None),
    MarkdownSymbol(symbol_name="close-square-bracket", markdown_syntax="\\]", opening_tag="]", closing_tag=None, closing_symbol_name=None),
]

markdown_symbol_helper = MarkdownSymbolHelper(_markdown_symbols)
