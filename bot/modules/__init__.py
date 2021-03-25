from glob import glob
from os.path import dirname, basename, isfile

from bot import LOAD, NO_LOAD, LOGGER


# generate a list of modules in this folder
def __list_all_modules():
    mod_paths = glob(f"{dirname((__file__))}/*.py")
    all_modules = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    if LOAD or NO_LOAD:
        to_load = LOAD
        if to_load:
            if not all(any(mod == module_name for module_name in all_modules) for mod in to_load):
                LOGGER.error("Invalid loadorder names. Quitting.")
                quit(1)

        else:
            to_load = all_modules

        if NO_LOAD:
            LOGGER.info(f"Not loading: {str(NO_LOAD)}")
            return [item for item in to_load if item not in NO_LOAD]

        return to_load

    return all_modules


ALL_MODULES = sorted(__list_all_modules())
LOGGER.info(f"Loading: {str(ALL_MODULES)}")
__all__ = [*ALL_MODULES, "ALL_MODULES"]
