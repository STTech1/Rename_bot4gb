def escape_invalid_curly_brackets(text: str, valids: List[str]) -> str:
    new_text = ""
    idx = 0
    while idx < len(text):
        if text[idx] == "{":
            if idx + 1 < len(text) and text[idx + 1] == "{":
                new_text += "{{{{"
                idx += 2
                continue
            else:
                success = any(text[idx:].startswith('{' + v + '}') for v in valids)
                if success:
                    for v in valids:
                        if text[idx:].startswith('{' + v + '}'):
                            new_text += text[idx: idx + len(v) + 2]
                            idx += len(v) + 2
                            break
                    continue
                else:
                    new_text += "{{"
        elif text[idx] == "}":
            if idx + 1 < len(text) and text[idx + 1] == "}":
                new_text += "}}}}"
                idx += 2
                continue
            else:
                new_text += "}}"
        else:
            new_text += text[idx]
        idx += 1

    return new_text
    
