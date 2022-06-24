from enum import Enum, auto


END_TOKEN = "END_TOKEN"

class TrieState(Enum):
    EXISTS_PARTIAL = auto()
    EXISTS_COMPLETE = auto()
    NOT_FOUND = auto()
    

def trie_lookup(value: str, trie: dict[dict]) -> TrieState:
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


def _build_trie(symbols: dict[str,str]) -> dict[dict]:
    root = dict()
    for symbol in symbols:
        current_dict = root
        for char in symbol:
            current_dict = current_dict.setdefault(char, {})
        
        current_dict[END_TOKEN] = END_TOKEN

    return root
            

markdown_syntax_dict = {
    "#": "h1",
    "##": "h2",
    "###": "h3",
    "####": "h4",
    "#####": "h5",
    "######": "h6",
}

markdown_token_to_html_dict = {
    "h1": ("<h1>", "</h1>"),
    "h2": ("<h2>", "</h2>"),
    "h3": ("<h3>", "</h3>"),
    "h4": ("<h4>", "</h4>"),
    "h5": ("<h5>", "</h5>"),
    "h6": ("<h6>", "</h6>"),
}

markdown_syntax_trie = _build_trie(markdown_syntax_dict) 

