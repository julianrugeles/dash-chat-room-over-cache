import dash
from dash import dcc

dash.register_page(
    __name__,
    path="/",
    title="Redirect"
)

layout = dcc.Location(href="/login", id="redirect-to-login")
