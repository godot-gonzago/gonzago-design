from re import sub


def camel_case(string: str) -> str:
    # https://www.w3resource.com/python-exercises/string/python-data-type-string-exercise-96.php
    s: str = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


def snake_case(string: str) -> str:
    # https://www.w3resource.com/python-exercises/string/python-data-type-string-exercise-97.php
    s: str = sub(
        "([A-Z][a-z]+)", r" \1", sub("([A-Z]+)", r" \1", string.replace("-", " "))
    )
    return "_".join(s.split()).lower()
