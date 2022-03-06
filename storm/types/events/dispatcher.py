from typing import Type, Union

from . import http, lifespan


class EventDispatcher:
    def __init__(self):
        self.events_mapping: dict[
            str, Union[
                Type[http.HttpRequest],
                Type[http.HttpDisconnect],
                Type[lifespan.Startup],
                Type[lifespan.Shutdown]
            ]
        ] = {
            'http.request': http.HttpRequest,
            'http.disconnect': http.HttpDisconnect,
            'lifespan.startup': lifespan.Startup,
            'lifespan.shutdown': lifespan.Shutdown
        }

    def dispatch_event(self, received_data: dict) -> Union[
        http.HttpRequest,
        http.HttpDisconnect,
        lifespan.Startup,
        lifespan.Shutdown
    ]:
        try:
            return self.events_mapping[received_data["type"]].construct(
                **received_data
            )
        except KeyError as err:
            raise KeyError("Unknown received event type") from err
