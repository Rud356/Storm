from typing import Union

# All flat types
ASGI_SUPPORTED_TYPES = Union[
    str, bytes, int, float,
    bool, None
]
# Here we add lists as some nested types
ASGI_SUPPORTED_TYPES = Union[
    ASGI_SUPPORTED_TYPES, list[ASGI_SUPPORTED_TYPES]
]

# Add some nested dicts inside of lists and etc.
ASGI_SUPPORTED_TYPES = Union[
    dict[
        str,
        Union[
            ASGI_SUPPORTED_TYPES, dict[str, ASGI_SUPPORTED_TYPES]
        ]
    ], ASGI_SUPPORTED_TYPES
]
ASGI_SUPPORTED_TYPES = Union[
    ASGI_SUPPORTED_TYPES, list[ASGI_SUPPORTED_TYPES]
]

