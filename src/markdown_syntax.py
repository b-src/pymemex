END_TOKEN = "END_TOKEN"


def _build_trie(symbols: dict[str,str]) -> dict[dict]:
    root = dict()
    for symbol in symbols:
        current_dict = root
        for char in symbol:
            current_dict = current_dict.setdefault(char, {})
        
        current_dict["_end"] = END_TOKEN

    return root
            

markdown_syntax_dict = {
    "#": "h1",
    "##": "h2",
    "###": "h3",
    "####": "h4",
    "#####": "h5",
    "######": "h6",
}

markdown_syntax_trie = _build_trie(markdown_syntax_dict) 

print(markdown_syntax_trie)
