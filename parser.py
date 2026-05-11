from scanner import tokenize


class Parser:

    VALID_TYPES = [
        "int",
        "float",
        "double",
        "char",
        "bool",
        "string",
        "void"
    ]

    VALID_RELOPS = [
        "==",
        "!=",
        "<",
        ">",
        "<=",
        ">="
    ]

    def __init__(self, tokens):

        self.tokens = tokens
        self.pos = 0

        self.current_token = (
            self.tokens[self.pos]
            if self.tokens else None
        )

    def advance(self):

        self.pos += 1

        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def peek(self):

        next_pos = self.pos + 1

        if next_pos < len(self.tokens):
            return self.tokens[next_pos]

        return None

    def error(self):

        raise SyntaxError("Compilation Error")

    def match(self, token_type, value=None):

        if not self.current_token:
            self.error()

        if self.current_token.type != token_type:
            self.error()

        if value and self.current_token.value != value:
            self.error()

        self.advance()

    # ==========================
    # PROGRAM
    # ==========================

    def parse_program(self):

        self.parse_function()

        if self.current_token is not None:
            self.error()

    # ==========================
    # FUNCTION
    # ==========================

    def parse_function(self):

        self.parse_type()

        self.match("IDENTIFIER")

        self.match("SPECIAL", "(")
        self.match("SPECIAL", ")")

        self.match("SPECIAL", "{")

        self.parse_statement_list()

        self.match("SPECIAL", "}")

    # ==========================
    # TYPE
    # ==========================

    def parse_type(self):

        if (
            self.current_token
            and self.current_token.type == "KEYWORD"
            and self.current_token.value in self.VALID_TYPES
        ):

            self.advance()

        else:
            self.error()

    # ==========================
    # STATEMENTS
    # ==========================

    def parse_statement_list(self):

        while self.current_token and (
            self.current_token.type == "KEYWORD"
            or self.current_token.type == "IDENTIFIER"
        ):

            self.parse_statement()

    def parse_statement(self):

        if (
            self.current_token.type == "KEYWORD"
            and self.current_token.value in self.VALID_TYPES
        ):

            self.parse_declaration()

        elif (
            self.current_token.type == "IDENTIFIER"
        ):

            self.parse_assignment()

        elif (
            self.current_token.type == "KEYWORD"
            and self.current_token.value == "if"
        ):

            self.parse_if()

        elif (
            self.current_token.type == "KEYWORD"
            and self.current_token.value == "return"
        ):

            self.parse_return()

        else:
            self.error()

    # ==========================
    # DECLARATION
    # ==========================

    def parse_declaration(self):

        self.parse_type()

        self.match("IDENTIFIER")

        while (
            self.current_token
            and self.current_token.type == "SPECIAL"
            and self.current_token.value == ","
        ):

            self.match("SPECIAL", ",")

            self.match("IDENTIFIER")

        self.match("SPECIAL", ";")

    # ==========================
    # ASSIGNMENT
    # ==========================

    def parse_assignment(self):

        self.match("IDENTIFIER")

        self.match("OPERATOR", "=")

        self.parse_expression()

        self.match("SPECIAL", ";")

    # ==========================
    # IF
    # ==========================

    def parse_if(self):

        self.match("KEYWORD", "if")

        self.match("SPECIAL", "(")

        self.parse_condition()

        self.match("SPECIAL", ")")

        self.match("SPECIAL", "{")

        self.parse_statement_list()

        self.match("SPECIAL", "}")

        if (
            self.current_token
            and self.current_token.type == "KEYWORD"
            and self.current_token.value == "else"
        ):

            self.match("KEYWORD", "else")

            self.match("SPECIAL", "{")

            self.parse_statement_list()

            self.match("SPECIAL", "}")

    # ==========================
    # RETURN
    # ==========================

    def parse_return(self):

        self.match("KEYWORD", "return")

        self.parse_expression()

        self.match("SPECIAL", ";")

    # ==========================
    # CONDITION
    # ==========================

    def parse_condition(self):

        self.parse_expression()

        if (
            self.current_token
            and self.current_token.type == "OPERATOR"
            and self.current_token.value in self.VALID_RELOPS
        ):

            self.advance()

            self.parse_expression()

    # ==========================
    # EXPRESSION
    # ==========================

    def parse_expression(self):

        self.parse_term()

        while (
            self.current_token
            and self.current_token.type == "OPERATOR"
            and self.current_token.value in ["+", "-"]
        ):

            self.advance()

            self.parse_term()

    def parse_term(self):

        self.parse_factor()

        while (
            self.current_token
            and self.current_token.type == "OPERATOR"
            and self.current_token.value in ["*", "/"]
        ):

            self.advance()

            self.parse_factor()

    def parse_factor(self):

        if (
            self.current_token.type == "IDENTIFIER"
        ):

            self.advance()

        elif (
            self.current_token.type == "NUMBER"
        ):

            self.advance()

        elif (
            self.current_token.type == "SPECIAL"
            and self.current_token.value == "("
        ):

            self.match("SPECIAL", "(")

            self.parse_expression()

            self.match("SPECIAL", ")")

        else:
            self.error()


# ==========================
# MAIN
# ==========================

if __name__ == "__main__":

    code = """
int main() {

    int x,y;

    // comment

    if (x == 42) {

        x = x - 3;

    } else {

        y = 3.1;

    }

    return 0;
}
"""

    try:

        tokens = tokenize(code)

        parser = Parser(tokens)

        parser.parse_program()

        print("Compilation Successful")

    except:

        print("Compilation Error")