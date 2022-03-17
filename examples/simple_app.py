import uvicorn

import storm
from storm.routing import Router


class ExampleApp(storm.StormApp):
    async def on_start(self) -> None:
        print("Hello world!")

    async def on_shutdown(self) -> None:
        print("Goodbye")


class MockRouter(Router):
    pass


app = ExampleApp(MockRouter())


if __name__ == "__main__":
    uvicorn.run("examples.simple_app:app", debug=True)
