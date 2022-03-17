from typing import Type, Union

from storm.types import events


class EventDispatcher:
    def __init__(self):
        self.events_mapping: dict[
            str, Union[
                Type[events.http.HttpRequest],
                Type[events.http.HttpDisconnect],
                Type[events.lifespan.Startup],
                Type[events.lifespan.Shutdown]
            ]
        ] = {
            'http.request': events.http.HttpRequest,
            'http.disconnect': events.http.HttpDisconnect,
            'lifespan.startup': events.lifespan.Startup,
            'lifespan.shutdown': events.lifespan.Shutdown
        }

    def dispatch_event(self, received_data: dict) -> Union[
        events.http.HttpRequest,
        events.http.HttpDisconnect,
        events.lifespan.Startup,
        events.lifespan.Shutdown
    ]:
        try:
            return self.events_mapping[received_data["type"]].construct(
                **received_data
            )
        except KeyError as err:
            raise KeyError("Unknown received event type") from err
