import dash
from dash import html, dcc, Input, Output, State
import uuid

dash.register_page(
    __name__,
    path="/login",
    title="Room Access"
)

layout = html.Div(
    html.Div(
        [
            html.H2("Room Access Anonymous Chat", style={"marginBottom": "10px", "justifyContent": "center"}),
            html.P("Enter a room code or create a new one"),

            dcc.Input(
                id="room-id-input",
                type="text",
                placeholder="Room ID",
                style={
                    "width": "93%",
                    "padding": "12px",
                    "marginBottom": "15px",
                    "fontSize": "16px"
                }
            ),

            html.Button(
                "Generate Room Code",
                id="generate-room",
                style={
                    "width": "100%",
                    "padding": "12px",
                    "marginBottom": "10px",
                    "fontSize": "16px"
                }
            ),

            html.Button(
                "Enter Room",
                id="enter-room",
                style={
                    "width": "100%",
                    "padding": "12px",
                    "fontSize": "16px"
                }
            ),

            html.Div(id="room-output", style={"marginTop": "15px"})
        ],
        style={
            "width": "100%",
            "maxWidth": "420px",
            "padding": "30px",
            "borderRadius": "8px",
            "boxShadow": "0 0 15px rgba(0,0,0,0.1)",
            "background": "white"
        }
    ),
    style={
        "minHeight": "100vh",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "background": "#f5f6fa"
    }
)

@dash.callback(
    Output("room-id-input", "value"),
    Input("generate-room", "n_clicks"),
    prevent_initial_call=True
)
def generate_room(n):
    return str(uuid.uuid4())

@dash.callback(
    Output("room-output", "children"),
    Input("enter-room", "n_clicks"),
    State("room-id-input", "value"),
    prevent_initial_call=True
)
def enter_room(n, room_id):
    if not room_id:
        return "Room ID is required"
    return dcc.Location(href=f"/room/{room_id}", id="redirect")
