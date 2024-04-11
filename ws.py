# pylint: disable=protected-access missing-function-docstring missing-module-docstring missing-class-docstring
# Forgive me for disabling the pylint checks
from functools import cache
import json
from typing import TYPE_CHECKING

import pandas as pd
from colorhash import ColorHash

if TYPE_CHECKING:
    from flask import Flask
    from flask_socketio import SocketIO

IMPORTANT_LINES = ["T1", "T2", "T3", "T4"]
"""Lines that should be shown at the top of any list."""

@cache
def _get_routes():
    with open('gtfs/routes.txt', encoding="utf8") as f:
        raw_routes = pd.read_csv(f)
    # Set all columns to string
    raw_routes = raw_routes.astype(str)
    # Remove "route_desc" column
    routes = raw_routes\
        .drop(columns=['route_short_name', 'route_desc', 'route_url'])\
        .to_dict(orient='records')
    parsed_routes = []
    for route in routes:
        route['route_long_name'] = json.dumps(route['route_long_name'])
        route['route_color'] = "#" + route['route_color']\
            if len(route['route_color']) > 4 else ColorHash(route['route_id']).hex
        parsed_routes.append(route)
    # Sort routes by moving important lines to the top
    important_routes, non_important_routes = [], []
    for route in parsed_routes:
        if route['route_id'] in IMPORTANT_LINES:
            important_routes.append(route)
        else:
            non_important_routes.append(route)
    sorted_routes = important_routes + non_important_routes
    return sorted_routes


def fetch_routes(socketio: 'SocketIO'):
    routes = _get_routes()
    socketio.emit('fetchRoutes', routes)


def main(socketio: 'SocketIO'):
    # pylint: disable=unused-variable

    @socketio.on('connect')
    def connect():
        print('Client connected')

    @socketio.on('disconnect')
    def disconnect():
        print('Client disconnected')

    @socketio.on('fetch')
    def fetch(data):
        if data.get('type') is None:
            return

        if data['type'] == 'routes':
            return fetch_routes(socketio)
        if data['type'] == 'stops':
            socketio.emit('fetch', {
                "type": "stops",
                "data": []
            })

