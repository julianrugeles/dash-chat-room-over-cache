import dash
from dash import html, dcc, Input, Output, State
from cache.redis import RedisManager
import uuid
import random
import datetime

chat = RedisManager(host="localhost", port=6379)

USER_NAMES = [
    "caballo-de-troya", "gusano-troyano", "dragon-bot",
    "serpiente-cibernetica", "zorro-ligero", "lobo-solitario",
    "tigre-de-hierro", "aguila-vigilante", "pantera-nocturna",
    "murcielago-volador"
]

dash.register_page(
    __name__,
    path_template="/room/<room_id>",
    title="Chat Room"
)

def layout(room_id=None):
    return html.Div(
        [
            dcc.Interval(id="interval-component", interval=2*1000, n_intervals=0),
            dcc.Store(id="user-id-store", storage_type="session"),

            html.Div(
                [
                    html.Div(
                        children=[
                            html.H2("Anonymous Chat Room", style={"marginBottom": "0"}),
                            html.H3(f"Session: {room_id}", style={"marginBottom": "0"}),
                            html.Div(id="user-id-display", style={"marginBottom": "10px"})
                        ],
                        style={"display": "flex", "flexDirection": "column"}
                    ),
                    html.Button(
                        "Salir",
                        id="exit-button",
                        n_clicks=0,
                        style={
                            "marginLeft": "auto",
                            "padding": "8px 16px",
                            "backgroundColor": "#f44336",
                            "color": "white",
                            "border": "none",
                            "borderRadius": "5px",
                            "cursor": "pointer"
                        }
                    )
                ],
                style={"display": "flex", "alignItems": "center", "width": "100%", "marginBottom": "20px"}
            ),

            html.Div(
                id="chat-window",
                style={
                    "border": "1px solid #ccc",
                    "height": "400px",
                    "width": "100%",
                    "overflowY": "auto",
                    "padding": "10px",
                    "marginBottom": "10px",
                    "background": "#f9f9f9",
                    "borderRadius": "8px"
                }
            ),

            html.Div(
                [
                    dcc.Input(
                        id="message-input",
                        type="text",
                        placeholder="Type your message...",
                        style={"width": "80%", "padding": "10px", "marginRight": "5px"}
                    ),
                    html.Button("Send", id="send-button", n_clicks=0, style={"padding": "10px"})
                ],
                style={"display": "flex", "width": "100%", "marginBottom": "20px"}
            ),

            dcc.Location(id="exit-redirect", refresh=True)
        ],
        style={
            "minHeight": "100vh",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "flex-start",
            "alignItems": "center",
            "padding": "20px",
            "maxWidth": "600px",
            "margin": "auto"
        }
    )


@dash.callback(
    Output("user-id-store", "data"),
    Output("exit-redirect", "href"),
    Input("interval-component", "n_intervals"),
    Input("exit-button", "n_clicks"),
    State("user-id-store", "data"),
    prevent_initial_call=False
)
def manage_user_id(n_intervals, exit_clicks, stored_id):
    ctx = dash.callback_context
    if not ctx.triggered:
        if stored_id:
            return stored_id, dash.no_update
        name = random.choice(USER_NAMES)
        number = str(random.randint(10000, 99999))
        return f"{name}-{number}", dash.no_update

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == "exit-button":
        return None, "/login"

    if not stored_id:
        name = random.choice(USER_NAMES)
        number = str(random.randint(10000, 99999))
        return f"{name}-{number}", dash.no_update

    return stored_id, dash.no_update


@dash.callback(
    Output("user-id-display", "children"),
    Input("user-id-store", "data")
)
def show_user_id(user_id):
    if not user_id:
        return ""
    return f"Your ID: {user_id}"


@dash.callback(
    Output("message-input", "value"),
    Input("send-button", "n_clicks"),
    State("message-input", "value"),
    State("url", "pathname"),
    State("user-id-store", "data"),
    prevent_initial_call=True
)
def send_message(n_clicks, message, pathname, user_id):
    if message and user_id:
        room_id = pathname.split("/")[-1]
        chat.save_message(room_id, user_id, message)
    return ""


@dash.callback(
    Output("chat-window", "children"),
    Input("interval-component", "n_intervals"),
    Input("url", "pathname")
)
def refresh_chat(n_intervals, pathname):
    room_id = pathname.split("/")[-1]
    msgs = chat.get_messages(room_id)
    if not msgs:
        return "No messages yet."
    chat_divs = [
        html.Div(
            [
                html.Div(m['text'], style={"marginBottom": "5px", "fontSize": "16px"}),
                html.Div(f"{m['user']} • {m['time']}", style={"fontSize": "12px", "color": "#555"})
            ],
            style={
                "marginBottom": "12px",
                "padding": "10px 14px",
                "borderRadius": "12px",
                "backgroundColor": "#e1ffc7",
                "maxWidth": "80%",
                "wordBreak": "break-word",
                "boxShadow": "0 1px 3px rgba(0,0,0,0.1)"
            }
        )

        for m in msgs
    ]
    return chat_divs
