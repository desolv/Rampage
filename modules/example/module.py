from architecture.base import BaseModule
from architecture.registry import register_module


@register_module
class ExampleModule(BaseModule):
    name = "example"
    required_modules = set()

    def __init__(self):
        super().__init__()

    async def setup(self) -> None:
        print("Example module started...")
