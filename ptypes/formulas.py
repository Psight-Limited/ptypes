from sympy import simplify_logic
import re


VAR_REGEX = re.compile(r'[A-Z][a-z0-9_]*')


def format(formula):
    positions = [(m.start(), m.end())
                 for m in VAR_REGEX.finditer(formula)]
    zipped_positions = zip(positions[:-1], positions[1:])
    res = ""
    last_end = 0
    inside = False
    for ((cur_start, cur_end), (nex_start, _)) in zipped_positions:
        res += formula[last_end:cur_start]
        if cur_end == nex_start \
                or re.search(r'\S', formula[cur_end:nex_start]) is None:
            if not inside:
                res += "("
            inside = True
            res += formula[cur_start:cur_end] + " and "
        else:
            res += formula[cur_start:cur_end]
            if inside:
                res += ")"
            inside = False
            res += formula[cur_end:nex_start]
        last_end = nex_start
    res += formula[last_end:]
    if inside:
        res += ")"
    res = res.replace("AND", "&")
    res = res.replace("OR", "|")
    res = res.replace("NOT", "!")
    res = res.replace("&&", "&")
    res = res.replace("||", "|")
    res = res.replace("!", " not ")
    res = res.replace("|", " or ")
    res = res.replace("&", " and ")
    res = re.sub(r'\s+', ' ', res)
    res = res.strip()
    return res


def _replace_operators(expr):
    expr = re.sub(r'AND', '&', expr, flags=re.IGNORECASE)
    expr = re.sub(r'OR', '|', expr, flags=re.IGNORECASE)
    expr = re.sub(r'NOT', '~', expr, flags=re.IGNORECASE)
    expr = re.sub(r'&&', '&', expr, flags=re.IGNORECASE)
    expr = re.sub(r'\|\|', '|', expr, flags=re.IGNORECASE)
    expr = re.sub(r'!', '~', expr, flags=re.IGNORECASE)
    return expr


def _encode(expr):
    expr = expr.replace("I", "~A")
    expr = expr.replace("N", "~B")
    expr = expr.replace("F", "~C")
    expr = expr.replace("P", "~D")
    expr = expr.replace("E", "A")
    expr = expr.replace("S", "B")
    expr = expr.replace("T", "C")
    expr = expr.replace("J", "D")
    return expr


def _decode(expr):
    expr = expr.replace("~A", "I")
    expr = expr.replace("~B", "N")
    expr = expr.replace("~C", "F")
    expr = expr.replace("~D", "P")
    expr = expr.replace("A", "E")
    expr = expr.replace("B", "S")
    expr = expr.replace("C", "T")
    expr = expr.replace("D", "J")
    expr = re.sub(r'\s*&\s*', '', expr)
    expr = re.sub(r'\s*', '', expr)
    return expr


def simplify(expr):
    expr = _encode(expr)
    expr = _replace_operators(expr)
    expr = str(simplify_logic(expr))
    expr = _decode(expr)
    return expr


def main():
    while True:
        expr = input("Simplify formula for:\n")
        expr = format(expr)
        expr = simplify(expr)
        print(expr)


if __name__ == "__main__":
    main()
