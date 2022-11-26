import uvicorn

import storm


class ExampleApp(storm.StormApp):
    async def on_start(self) -> None:
        print("Hello world!")

    async def on_shutdown(self) -> None:
        print("Goodbye")


class MockRouter(storm.StormRouter):
    pass


app = ExampleApp(MockRouter())


if __name__ == "__main__":
    uvicorn.run("simple_app:app", debug=True)
