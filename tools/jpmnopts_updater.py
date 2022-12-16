"""
# template is always fixed to be src/jpmn_opts_template.jsonc



# applies changes from latest version to _jpmn-options.js within Anki's media folder
# input is None <=> input is _jpmn-options.js
# output is None <=> output is _jpmn-options.js
python3 jpmnopts_updater.py
python3 jpmnopts_updater.py --apply-changes-update

# can take arbitrary input file
# file can be json or jsonc
python3 jpmnopts_updater.py --input "input_file"

# outputs file
# file can be json or jsonc (jsonc output will use the template)
python3 jpmnopts_updater.py --output "OUTPUT_FILE"

# applies changes from any list of files to _jpmn-options.js
python3 jpmnopts_updater.py --apply-changes-from "CHANGES_1_FILE" "CHANGES_2_FILE" "CHANGES_3_FILE"

# applies changes from files AND from updating if necessary
# files are always applied afterwards
python3 jpmnopts_updater.py --apply-changes-update --apply-changes-from "CHANGES_FILE"

# shorthand for updating the same file, i.e.:
# python3 jpmnopts_updater.py --input "FILE" --output "FILE"
python3 jpmnopts_updater.py --update "FILE"

"""


from __future__ import annotations

import os

# import os.path
import json
import base64
import difflib
import argparse
from typing import Any
from copy import deepcopy
from abc import ABC
from dataclasses import dataclass

try:
    from json_minify import json_minify
except Exception:

    def json_minify(x):
        raise RuntimeError(
            "Attempting to use json_minify without the JSON-minify package installed. Did you forget to run `python3 -m pip install JSON-minify`?"
        )


from note_changes import Version, NoteChange, NOTE_CHANGES
import utils
import action


JSON = dict[str, Any]

OPTIONS_FILE_NAME = "_jpmn-options.js"


def add_args(parser: argparse.ArgumentParser):
    group = parser.add_argument_group(title="jpmnopts_updater")
    # group.add_argument(
    #    "--to-latest",
    #    action="store_true",
    #    help="updates the settings to the latest version (default)",
    # )

    # use --dev-output-version lol
    # group.add_argument(
    #    "--to-version",
    #    type=str,
    #    default=None,
    #    help="updates the settings to the specified version",
    # )

    # group.add_argument(
    #    "--dev-update-json",
    #    type=str,
    #    default=None,
    #    help="(dev option) updates the source json file for building",
    # )

    # group.add_argument(
    #    "--dev-update-json-output",
    #    type=str,
    #    default=None,
    #    help="(dev option) output file for the above",
    # )

    group.add_argument(
        "--apply-changes-update",
        action="store_true",
        help="applies the changes required for your current note version to work with the latest version",
    )

    group.add_argument(
        "--input",
        type=str,
        default=None,
        help="input file (json or jsonc). If not specified, uses Anki's _jpmn-options.js file.",
    )

    group.add_argument(
        "--output",
        type=str,
        default=None,
        help="output file (json or jsonc). If not specified, uses Anki's _jpmn-options.js file.",
    )

    group.add_argument(
        "--apply-changes-from",
        type=str,
        default=[],
        nargs="+",
        help="json (or jsonc) files to get the changes from. If this option"
        "is used, --apply-changes-update must be specified manually if desired.",
    )

    group.add_argument(
        "--update",
        type=str,
        default=None,
        help="specifies both the input and output file (json or jsonc).",
    )

    group.add_argument(
        "--no-template",
        action="store_true",
        help="for jsonc output files, sets to not write the file with the jsonc template",
    )

    group.add_argument(
        "--no-override-warn",
        action="store_true",
        help="no warning on overriding the output file",
    )


def read_json_or_jsonc(filename):
    with open(filename) as f:
        json_str = f.read()
        if os.path.splitext(filename)[1] == ".jsonc":
            json_str = json_minify(json_str)
        json_content = json.loads(json_str)
    return json_content


class JPMNOptsUpdater:
    # TODO merge this entire class with the manager class below

    def __init__(self, template: str, options: JSON = dict()):
        self.template = template
        self.options = options

    def flatten(self, json):
        """
        changes json {"a": {"b": "c", "e": "f"}} to {"a.b": "c", "a.e": "f"}
        """

        result = {}

        for k, v in json.items():
            if isinstance(v, dict):
                if "type" in v:
                    result[k] = v
                else:
                    for k2, v2 in self.flatten(v).items():
                        result[f"{k}.{k2}"] = v2
            # elif isinstance(v, list):
            #    raise SyntaxError(f"cannot flatten list {v}")
            else:
                # string, number, boolean, list
                result[k] = v

        return result

    def unflatten(self, flattened_json):
        """
        changes json {"a.b": "c", "a.e": "f"} to {"a": {"b": "c", "e": "f"}}
        """

        result = {}

        for flattened_key, v in flattened_json.items():
            keys = flattened_key.split(".")
            result_temp = result
            for i, k in enumerate(keys):
                if i == len(keys) - 1:
                    result_temp[k] = v
                else:
                    result_temp[k] = result_temp.get(k, dict())
                    result_temp = result_temp[k]

        return result

    # def flatten_options(self):
    #    flat_templates = self.flatten(json.loads(json_minify(self.template)))
    #    result = {}

    #    for flat_key in flat_templates:

    #        found_item = True

    #        # attempts to visit
    #        item = self.options
    #        keys = flat_key.split(".")

    #        for k in keys:
    #            if k in item:
    #                item = item[k]
    #            else:
    #                found_item = False
    #                print(f"jpmnopts_updater warning: did not find key {flat_key}")
    #                break

    #        if not found_item:
    #            raise RuntimeError(f"Key not found: {flat_key}")

    #        # found full key / item pair
    #        result[flat_key] = item

    #    return result

    # def apply_actions(self, options: JSON, actions: list[action.OptAction]):
    #    """
    #    - applies all actions to given options list
    #    - adds any options in self.options to result if doesn't already exist
    #    """
    #    result = deepcopy(options)

    #    for a in actions:
    #        if isinstance(a, action.MoveOptAction):
    #            if a.key_src in result:
    #                result[a.key_dest] = result.pop(a.key_src)
    #            else:
    #                print(
    #                    f"jpmnopts_updater warning: cannot move {a.key_src} -> {a.key_dest}"
    #                )
    #        elif isinstance(a, action.OverwriteValueOptAction):
    #            result[a.key] = a.value
    #        elif isinstance(a, action.ChangeDefaultValueOptAction):
    #            if result[a.key] == a.default_val:
    #                result[a.key] = a.value

    #    for k in self.options:
    #        if k not in result:
    #            result[k] = self.options[k]

    #    return result

    def apply_actions(
        self, flattened_opts: dict[str, Any], actions: list[action.OptAction]
    ):
        """
        - applies all actions to given options list
        - adds any options in self.options to result if doesn't already exist
        """
        for a in actions:
            if isinstance(a, action.MoveOptAction):
                if a.key_src in flattened_opts:
                    flattened_opts[a.key_dest] = flattened_opts.pop(a.key_src)
                else:
                    print(
                        f"jpmnopts_updater warning: cannot move {a.key_src} -> {a.key_dest}"
                    )
            elif isinstance(a, action.OverwriteValueOptAction):
                flattened_opts[a.key] = a.value
            elif isinstance(a, action.ChangeDefaultValueOptAction):
                if flattened_opts[a.key] == a.default_val:
                    flattened_opts[a.key] = a.value

    def apply_overrides(self, flattened_opts: dict[str, Any], overrides: JSON):
        flattened_overrides = self.flatten(overrides)
        for k, v in flattened_overrides.items():
            flattened_opts[k] = v

    def generate(self, actions: list[action.OptAction]):
        """
        - create options in format of k1. (...) .kn: v (flattened)
        - replaces all k1. (...) .kn instances in template string with value in options
        """

        result_template = self.template
        flattened_opts = self.flatten(self.options)
        self.apply_actions(flattened_opts, actions)

        for key, value in flattened_opts.items():
            find_str = '"{{ ' + key + ' }}"'
            replace_str = utils.javascript_format(value)

            result_template = result_template.replace(find_str, replace_str)

        return result_template


class JPMNOptsUpdateManager:
    def __init__(
        self,
        updater: JPMNOptsUpdater,
        input_file: str | None,
        output_file: str | None,
        apply_changes_update: bool,
        apply_changes_from: list[str],
        output_template: bool,
    ):

        self.updater = updater
        self.input_file = input_file
        self.output_file = output_file
        self.apply_changes_update = apply_changes_update
        self.apply_changes_from = apply_changes_from
        self.output_template = output_template

        self.result_flattened_opts = {}

    def read(self):
        """
        if input_file is None:
            - read the options file from ankiConnect
        else:
            - read input file as normal
        """
        if self.input_file is None:
            # read from anki connect

            contents_b64 = utils.invoke("retrieveMediaFile", filename=OPTIONS_FILE_NAME)
            if not contents_b64:
                # TODO
                raise NotImplementedError()

            contents = base64.b64decode(contents_b64).decode("utf-8")
            # attempts to get the json from the options file

            SEARCH_STR = "my.settings = {"
            i = contents.find(SEARCH_STR)
            jsonc_content = contents[i + len(SEARCH_STR) - 1 :]

            # allows extra content past the json
            d = json.JSONDecoder()
            # _ is the end position of the json string
            json_content, _ = d.raw_decode(json_minify(jsonc_content))

        else:
            json_content = read_json_or_jsonc(self.input_file)

        self.updater.options = json_content

    def update(self, args):
        flattened_opts = self.updater.flatten(self.updater.options)

        if self.apply_changes_update:
            actions = self.get_actions(args)
            self.updater.apply_actions(flattened_opts, actions)

        for f in self.apply_changes_from:
            json_content = read_json_or_jsonc(f)
            self.updater.apply_overrides(flattened_opts, json_content)

        self.result_flattened_opts = flattened_opts

    def write(self, should_warn):
        # output string

        if self.output_file is None:
            # write to anki connect
            # TODO
            result = ""

        elif self.output_template and os.path.splitext(self.output_file)[1] == ".jsonc":
            result = self.updater.template

            for key, value in self.result_flattened_opts.items():
                find_str = '"{{ ' + key + ' }}"'
                replace_str = utils.javascript_format(value)

                result = result.replace(find_str, replace_str)

        else:
            # writes standard json
            opts = self.updater.unflatten(self.result_flattened_opts)
            result = json.dumps(opts, indent=2)


        if should_warn and (
            (
                self.input_file is self.output_file is None # to and from ankiconnect
            )
            or (
                self.output_file is not None and os.path.isfile(self.output_file)
            )  # the output file already exists
        ):

            # TODO diff option

            x = input(
                "WARNING: This will overwrite the output file with the updated options.\n"
                "Type 'yes' to proceed with overwriting the file, or anything else to abort: "
            )
            if x != "yes":
                return

        if self.output_file is None:
            # write to anki connect
            pass
        else:
            with open(self.output_file, "w", encoding="utf-8") as f:
                f.write(result)


    def get_actions(self, args):
        current_ver = Version.from_str(utils.get_version_from_anki(args))
        new_ver = Version.from_str(utils.get_version(args))

        return self._get_actions_from_version(current_ver, new_ver, NOTE_CHANGES)

    def _get_actions_from_version(
        self, current_ver: Version, new_ver: Version, note_changes: list[NoteChange]
    ) -> list[action.OptAction]:
        """
        gets actions for the given versions
        """

        result: list[NoteChange] = []

        if current_ver == new_ver:
            # nothing to do
            return []

        if current_ver > new_ver:
            print("Warning: current version is higher than the newer version?")
            return []

        for data in reversed(note_changes):
            ver = data.version
            # finds all versions that are > current_ver and <= new_ver
            if (ver > current_ver) and (ver <= new_ver):
                result.append(data)

            if ver > new_ver:
                break

        return sum((c.option_actions for c in result), start=[])


def main(args=None):

    if args is None:
        args = utils.get_args(utils.add_args, add_args)

    input_file = args.input
    output_file = args.output
    if args.update:
        input_file = output_file = args.update

    apply_changes_update = True
    if args.apply_changes_from:
        apply_changes_update = False
        if args.apply_changes_update:
            apply_changes_update = True

    output_template = False
    if output_file is not None and os.path.splitext(output_file)[1] == ".jsonc":
        output_template = True
        if args.no_template:
            output_template = False

    # config = utils.get_config(args)

    # actions = get_actions(current_ver, new_ver, NOTE_CHANGES)
    # print(actions)

    root_folder = utils.get_root_folder()
    template_file_path = os.path.join(root_folder, "src", "jpmn_opts_template.jsonc")
    with open(template_file_path) as f:
        template = f.read()
    # with open("config/example_jpmn_opts.json") as f:
    #    options = json.load(f)

    upt = JPMNOptsUpdater(
        template,
    )

    mgr = JPMNOptsUpdateManager(
        upt,
        input_file,
        output_file,
        apply_changes_update,
        args.apply_changes_from,
        output_template,
    )

    mgr.read()
    mgr.update(args)
    mgr.write(should_warn=(not args.no_override_warn))

    # print(upt.unflatten({"a.b": "c", "a.e": "f"}))

    # mgr.write(should_warn=True)

    # if args.dev_update_json:
    #    input_path = args.dev_update_json
    #    output_path = (
    #        args.dev_update_json_output if args.dev_update_json_output else input_path
    #    )

    #    if input_path == output_path:
    #        x = input(
    #            f"WARNING: Overriding {input_path}.\n"
    #            "Please type 'yes' to confirm, or anything else to abort: "
    #        )

    #        if x != "yes":
    #            print("Aborting update...")
    #            return

    #    with open(input_path) as f:
    #        user_json = json.load(f)

    #    result = upt.generate(user_json, actions)
    #    with open(output_path, "w") as f:
    #        print(f"Writing to {output_path}...")
    #        f.write(result)


if __name__ == "__main__":
    main()
