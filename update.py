import argparse
import contextlib
import importlib
import logging
import os
import sys
import time
import traceback
import json
import threestudio
import copy

def load_custom_module(module_path):
    module_name = os.path.basename(module_path)
    if os.path.isfile(module_path):
        sp = os.path.splitext(module_path)
        module_name = sp[0]
    try:
        if os.path.isfile(module_path):
            module_spec = importlib.util.spec_from_file_location(
                module_name, module_path
            )
        else:
            module_spec = importlib.util.spec_from_file_location(
                module_name, os.path.join(module_path, "__init__.py")
            )

        module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_name] = module
        module_spec.loader.exec_module(module)
        return True
    except Exception as e:
        print(traceback.format_exc())
        print(f"Cannot import {module_path} module for custom nodes:", e)
        return False


def load_custom_modules():
    existing_modules = json.load(open("custom/threestudio-extensions_disabled/custom-extensions-list.json", "r"))["custom_nodes"]
    name2files = {}
    for custom_node in existing_modules:
        name2files[custom_node["title"]] = custom_node["files"][0]
    extension_modules = {}
    
    node_paths = ["custom"]
    node_import_times = []
    for custom_node_path in node_paths:
        possible_modules = os.listdir(custom_node_path)
        if "__pycache__" in possible_modules:
            possible_modules.remove("__pycache__")

        for possible_module in possible_modules:
            module_path = os.path.join(custom_node_path, possible_module)
            if (
                os.path.isfile(module_path)
                and os.path.splitext(module_path)[1] != ".py"
            ):
                continue
            if module_path.endswith("_disabled"):
                continue
            time_before = time.perf_counter()
            print(possible_module)
            register_modules = copy.deepcopy(threestudio.__modules__)
            success = load_custom_module(module_path)
            node_import_times.append(
                (time.perf_counter() - time_before, module_path, success)
            )
            if success and (possible_module in name2files):
                new_modules = []
                new_register_modules = threestudio.__modules__
                for name in new_register_modules:
                    if name in register_modules:
                        continue
                    new_modules.append(name)
                extension_modules[str(name2files[possible_module])] = [new_modules]
                print(new_modules)


    if len(node_import_times) > 0:
        print("\nImport times for custom modules:")
        for n in sorted(node_import_times):
            if n[2]:
                import_message = ""
            else:
                import_message = " (IMPORT FAILED)"
            print("{:6.1f} seconds{}:".format(n[0], import_message), n[1])
        print()

    json.dump(extension_modules, open("custom/threestudio-extensions_disabled/custom-extensions-modules-map.json", "w"), indent=4)

def main() -> None:
    load_custom_modules()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    main()
