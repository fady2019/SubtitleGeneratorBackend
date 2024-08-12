from sqlalchemy import Column
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import TypedDict
from collections import defaultdict
import regex as re
import os


class ColumnMeta(TypedDict):
    type: type  # the type of the column
    optional: bool  # is the column optional? (nullable)
    updatable: bool  # can we update this column?
    excluded: bool  # exclude at creation?


def get_py_type(column: Column):
    try:
        return column.type.python_type
    except Exception as err:
        print("from db utils => ", type(err), err)
        raise err


def create_annotations_from_entity(entity: type[DeclarativeMeta]):
    annotations: dict[str, ColumnMeta] = {}

    columns: list[Column] = entity.__table__.columns

    for column in columns:
        annotations[column.name] = {
            "type": get_py_type(column),
            "optional": column.nullable,
            "updatable": column.info.get("updatable", True),
            "excluded": column.info.get("excluded", False),
        }

    return annotations


def generate_dict_from_entity(entity: type[DeclarativeMeta], ignore_if_exist: bool = False):
    dict_name = entity.__name__ + "Dict"
    file_path = f"db/entity_dicts/{to_snake_case(dict_name)}.py"

    if ignore_if_exist and os.path.exists(file_path):
        return

    annotations = create_annotations_from_entity(entity)

    if not annotations:
        return

    imports = defaultdict(set)

    create_entity_dict_definition = [f"class Create{dict_name}(CreateEntityDict):"]
    update_entity_dict_definition = [f"class Update{dict_name}(UpdateEntityDict):"]

    for name, metadata in annotations.items():
        if metadata["excluded"] and not metadata["updatable"]:
            continue

        imports[metadata["type"].__module__].add(metadata["type"].__name__)
        type_name = metadata["type"].__name__

        if metadata["optional"]:
            imports["typing"].add("Optional")
            type_name = f"Optional[{metadata['type'].__name__}]"

        if not metadata["excluded"]:
            create_entity_dict_definition.append(f"{name}: {type_name}")

        if metadata["updatable"]:
            imports["typing"].add("Optional")
            update_entity_dict_definition.append(f"{name}: Optional[{metadata['type'].__name__}]")

    imports["db.entity_dicts.entity_dict"].add("CreateEntityDict")

    if len(update_entity_dict_definition) > 1:
        imports["db.entity_dicts.entity_dict"].add("UpdateEntityDict")

    # CREATE DICT FILE
    with open(file_path, "w") as file:
        for module in sorted(imports.keys()):
            types = ", ".join(sorted(imports[module]))
            file.write(f"from {module} import {types}\n")

        file.write("\n\n")
        file.write("\n    ".join(create_entity_dict_definition))

        if len(update_entity_dict_definition) > 1:
            file.write("\n\n\n")
            file.write("\n    ".join(update_entity_dict_definition))


def to_snake_case(s: str) -> str:
    s = re.sub(r"(?<!^)(?<!_)([A-Z][a-z])", r"_\1", s)
    s = re.sub(r"([a-z])([A-Z])", r"\1_\2", s)
    s = re.sub(r"[\s-]+", "_", s)
    s = s.lower()
    s = re.sub(r"__+", "_", s)

    return s
