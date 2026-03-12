import re

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}:{self.value}"


KEYWORDS = {
    "int","float","double","bool","char","string","void",
    "if","else","while","for","return","true","false","main"
}

OPERATORS = {
    "==","!=","<=",">=","+","-","*","/","=","<",">"
}

SPECIAL = {
    "(",")","{","}",";"
}


token_specification = [
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),
    ('OP',       r'==|!=|<=|>=|\+|\-|\*|\/|=|<|>'),
    ('SPECIAL',  r'[(){};]'),
    ('SKIP',     r'[ \t]+'),
    ('NEWLINE',  r'\n'),
]


tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)


def tokenize(code):

    tokens = []

    for mo in re.finditer(tok_regex, code):

        kind = mo.lastgroup
        value = mo.group()

        if kind == 'NUMBER':
            tokens.append(Token("Numeric_constants", value))

        elif kind == 'ID':
            if value in KEYWORDS:
                tokens.append(Token("Keywords", value))
            else:
                tokens.append(Token("Identifiers", value))

        elif kind == 'OP':
            tokens.append(Token("Operators", value))

        elif kind == 'SPECIAL':
            tokens.append(Token("Special_characters", value))

        elif kind in ('SKIP','NEWLINE'):
            continue

    return tokens


if __name__ == "__main__":

    code = """
int main() {
    int x,y;
    // This is a single-line comment
    if (x == 42) {
        /* This is
           a block
           comment */
        x = x-3;
    } else {
        y = 3.1; // Another comment
    }
    return 0;
}
    """

    tokens = tokenize(code)

    for t in tokens:
        print(t)