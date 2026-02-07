import importlib
from pathlib import Path
from typing import Optional

import discord

from architecture.base import BaseModule
from architecture.registry import get_module_class


class ModuleManager:
    ESSENTIAL_MODULES = ["rampage"]

    def __init__(
        self,
        bot: discord.Client,
        guild_enabled_modules: dict[
            int,
            set[str],
        ],
    ):
        self.bot = bot
        self.guild_enabled_modules = guild_enabled_modules
        self.enabled_modules: dict[str, BaseModule] = {}
        self._discover_modules()

    def _discover_modules(self) -> None:
        """
        Discovers and imports all Python architecture
        :return:
        """
        modules_dir = Path(__file__).parent.parent.parent / "architecture"
        for module_path in modules_dir.rglob("module.py"):
            relative_path = module_path.relative_to(modules_dir.parent)
            module_name = str(relative_path.with_suffix("")).replace("/", ".")
            importlib.import_module(module_name)

    def _detect_cycle(
        self,
        module_name: str,
        dependency_graph: dict[str, set[str]],
    ) -> Optional[list[str]]:
        """
        Detects if there is a cycle in the module dependencies
        :param module_name:
        :param dependency_graph:
        :return:
        """
        visited = set()
        recursion_stack = set()

        def detect_cycle(current: str, path: list[str]) -> Optional[list[str]]:
            if current in recursion_stack:
                cycle_start = path.index(current)
                return path[cycle_start:] + [current]

            if current in visited:
                return None

            visited.add(current)
            recursion_stack.add(current)
            path.append(current)

            if current in dependency_graph:
                for dependency in dependency_graph[current]:
                    cycle = detect_cycle(dependency, path.copy())
                    if cycle:
                        return cycle

            recursion_stack.remove(current)
            return None

        return detect_cycle(module_name, [])

    def _build_dependency_graph(self, module_names: list[str]) -> dict[str, set[str]]:
        """
        Builds a dependency graph for the given module names
        :param module_names:
        :return:
        """
        dependency_graph = {}
        for module_name in module_names:
            module_class = get_module_class(module_name)
            dependency_graph[module_name] = module_class.required_modules
        return dependency_graph

    def _validate_dependencies(
        self,
        module_name: str,
        enabled_module_names: set[str],
    ) -> None:
        """
        Validates that all required architecture for the given module are enabled
        :param module_name:
        :param enabled_module_names:
        :return:
        """
        for required_module in get_module_class(module_name).required_modules:
            if required_module not in enabled_module_names:
                raise ValueError(f"Module '{module_name}' requires module '{required_module}', but it is not enabled..")

    async def enable_modules(self, module_names: list[str]) -> None:
        """
        Enables the given architecture and their dependencies
        :param module_names:
        :return:
        """
        all_module_names = list(self.ESSENTIAL_MODULES) + module_names

        for module_name in all_module_names:
            try:
                get_module_class(module_name)
            except KeyError:
                raise ValueError(f"Module '{module_name}' does not exist!")

        dependency_graph = self._build_dependency_graph(all_module_names)

        for module_name in all_module_names:
            cycle = self._detect_cycle(module_name, dependency_graph)
            if cycle:
                cycle_str = " -> ".join(cycle)
                raise RuntimeError(f"Dependency cycle detected: {cycle_str}..")

        enabled_module_names = set(all_module_names)
        for module_name in all_module_names:
            self._validate_dependencies(module_name, enabled_module_names)

        for module_name in all_module_names:
            module_class = get_module_class(module_name)
            module_instance = module_class()
            module_instance.bot = self.bot
            await module_instance.setup()
            self.enabled_modules[module_name] = module_instance

    async def disable_module(self, module_name: str) -> None:
        """
        Disables the given module and its dependencies
        :param module_name:
        :return:
        """
        if module_name not in self.enabled_modules:
            raise ValueError(f"Module '{module_name}' is not enabled!")

        module_instance = self.enabled_modules[module_name]
        await module_instance.teardown()
        del self.enabled_modules[module_name]

    def is_enabled_for_guild(self, module_name: str, guild_id: int) -> bool:
        """
        Checks if the given module is enabled for the given guild
        :param module_name:
        :param guild_id:
        :return:
        """
        if module_name not in self.enabled_modules:
            return False

        if guild_id not in self.guild_enabled_modules:
            return False

        return module_name in self.guild_enabled_modules[guild_id]
