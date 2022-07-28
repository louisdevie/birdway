from pygments.lexer import RegexLexer, bygroups
from pygments import token


class BirdwayLexer(RegexLexer):
    name = "Birdway"

    tokens = {
        "root": [
            (r"--.*$", token.Comment),
            (r"\b(let|println|func)\b", token.Keyword),
            (r"[0-9]+", token.Number),
            (r"[a-zA-Z]+", token.Name),
            (r"=|\*", token.Operator),
            (r"{|;|}|\(|,|\)|->|\$", token.Punctuation),
            (r'"', token.String, "string"),
            (r"\s", token.Whitespace),
        ],
        "string": [
            (r"(\$)([A-Za-z0-9_]*)", bygroups(token.Punctuation, token.Name)),
            (r'"', token.String, "#pop"),
            (r".", token.String),
        ],
    }
