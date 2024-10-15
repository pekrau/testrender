"Test the 'render' service."

import os

from fasthtml.common import *


app, rt = fast_app(
    live="DEVELOPMENT" in os.environ,
    )

data = {}


@rt("/")
def get():
    "Home page."
    return Titled("Home testrender",
                  P("Some text in a paragraph."),
                  Ul(
                      Li(A("List env vars", href="/env")),
                      Li(A("List data", href="/data")),
                      Li(A("Add data", href="/add")),
                      Li(A("Text input", href="/text")),
                  )
                  )

@rt("/env")
def get():
    "List env vars."
    rows = [Tr(Td(key), Td(value)) for key, value in os.environ.items()]
    return Titled(
        "List env vars",
        Table(*rows),
        P(A("Home", href="/")),
    )

@rt("/data")
def get():
    rows = [Tr(Td(key), Td(value), Td(A("Remove", href=f"/remove/{key}")))
            for key, value in data.items()]
    if rows:
        content = Table(*rows)
    else:
        content = P("No data")
    return Titled(
        "List data",
        content,
        P(A("Add", href="/add")),
        P(A("Clear", href="/clear")),
        P(A("Home", href="/")),
    )

@rt("/add")
def get():
    return Titled(
        "Add data",
        Form(
            Input(id="key", placeholder="key"),
            Input(id="value", placeholder="value"),
            Button("Add"),
            action="/add",
            method="post",
        ),
        P(A("Home", href="/")),
    )

@rt("/add")
def post(key:str, value:str):
    key = key.strip()
    if not key:
        raise ValueError("no key")
    data[key] = value.strip()
    return RedirectResponse("/data", status_code=303)

@rt("/remove/{key}")
def get(key:str):
    data.pop(key, None)
    return RedirectResponse("/data", status_code=303)

@rt("/clear")
def get():
    data.clear()
    return RedirectResponse("/data", status_code=303)

@rt("/text")
def get():
    return Titled(
        "Text input",
        Form(
            Textarea(id="text", rows=10),
            Button("Text"),
            action="/text",
            method="post",
        ),
        P(A("Home", href="/")),
    )

@rt("/text")
def post(text:str):
    length = 0
    paras = []
    for chunk in text.split("\n"):
        chunk = chunk.strip()
        if chunk:
            paras.append(P(chunk))
            length = len(chunk)
    paras.append(f"Characters: {length}")
    return Titled(
        "Text display",
        *paras,
        P(A("Home", href="/")),
    )
    

serve()
