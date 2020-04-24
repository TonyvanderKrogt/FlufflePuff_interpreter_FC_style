import re
from typing import List


def tokenize(source: str) -> List[str]:
    tokens = []
    def loop(source: str, tokens: List[str]) -> List[str]:
        temp = tokens.copy()
        if bool(re.match(r"pf", source)):
            temp.append('PLUS_ONE')
            return loop(source[2:], temp)
        elif bool(re.match(r"bf", source)):
            temp.append('MINUS_ONE')
            return loop(source[2:], temp)
        elif bool(re.match(r"b", source)):
            temp.append('MOV_RIGHT')
            return loop(source[1:], temp)
        elif bool(re.match(r"t", source)):
            temp.append('MOV_LEFT')
            return loop(source[1:], temp)
        elif bool(re.match(r"!", source)):
            temp.append('OUTPUT')
            return loop(source[1:], temp)
        elif bool(re.match(r"\?", source)):
            temp.append('INPUT')
            return loop(source[1:], temp)
        elif bool(re.match(r"\*gasp\*", source)):
            temp.append('OPEN_LOOP')
            return loop(source[6:], temp)
        elif bool(re.match(r"\*pomf\*", source)):
            temp.append('CLOSE_LOOP')
            return loop(source[6:], temp)
        elif bool(re.match(r"\r", source)):
            return temp
        elif len(source) == 0:
            return temp
        return loop(source[1:], temp)
    return loop(source, tokens)


if __name__ == "__main__":
    src = "pfbfbt!?*gasp**pomf*"
    print(tokenize(src))
