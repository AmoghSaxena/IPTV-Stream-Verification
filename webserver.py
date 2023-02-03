from pathlib import Path
import uuid

import dash
import dash_auth
import dash_uploader as du
import dash_html_components as html
from dash.dependencies import Input, Output, State


VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'digivalet'
}


#app = dash.Dash(__name__)
app = dash.Dash(__name__, url_base_pathname='/upload/')
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
app.title = 'IPTV FeedChecker Uploader'


UPLOAD_FOLDER_ROOT = r"/home/rundeck-auto/IPTV_Data/"
du.configure_upload(app, UPLOAD_FOLDER_ROOT)


def get_upload_component(id):
    return du.Upload(
        id=id,
        max_file_size=5120,  # 1800 Mb
        filetypes=['xlsx'],
        upload_id="file",  # Unique session id
    )


def get_app_layout():

    return html.Div(
        [
            html.H1('IPTV Feed Checker Excel Uploader'),
            html.Div(
                [
                    get_upload_component(id='dash-uploader'),
                    html.Div(id='callback-output'),
                ],
                style={  # wrapper div style
                    'textAlign': 'center',
                    'width': '600px',
                    'padding': '10px',
                    'display': 'inline-block'
                }),
            html.Br(),
        ],
        style={
            'textAlign': 'center',
        },
    )


# get_app_layout is a function
# This way we can use unique session id's as upload_id's
app.layout = get_app_layout


@du.callback(
    output=Output('callback-output', 'children'),
    id='dash-uploader',
)
def get_a_list(filenames):
    return html.H3("File Uploaded Successfully")


if __name__ == '__main__':
    app.run_server(debug=False, host="localhost", port='8123')