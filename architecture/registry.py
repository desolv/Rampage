from typing import Type

from architecture.base import BaseModule

_module_registry: dict[str, Type[BaseModule]] = {}


def register_module(module_class: Type[BaseModule]) -> Type[BaseModule]:
    """
    Registers a module class
    :param module_class:
    :return:
    """
    if not hasattr(module_class, "name") or not module_class.name:
        raise ValueError(f"Module {module_class} must define a name attribute..")

    if module_class.name in _module_registry:
        raise ValueError(f"Module '{module_class.name}' is already registered!")

    _module_registry[module_class.name] = module_class
    return module_class


def get_module_class(module_name: str) -> Type[BaseModule]:
    """
    Gets a module class by name
    :param module_name:
    :return:
    """
    if module_name not in _module_registry:
        raise KeyError(f"Module '{module_name}' is not registered!")
    return _module_registry[module_name]


def get_all_registered_modules() -> dict[str, Type[BaseModule]]:
    """
    Gets all registered architecture
    :return:
    """
    return _module_registry.copy()
