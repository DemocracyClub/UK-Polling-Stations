import ast
import logging
import re
import sys

if sys.version_info < (3, 9):
    from ast_compat import unparse as ast_unparse
else:
    from ast import unparse as ast_unparse


import black

logger = logging.getLogger(__name__)


class ImportScript:
    def __init__(
        self,
        council_id,
        ems,
        addresses_name,
        stations_name,
        elections,
        encoding,
        existing_script=None,
    ):
        self.council_id = council_id
        self.ems = ems
        self.addresses_name = addresses_name
        self.stations_name = stations_name
        self.encoding = encoding
        self.elections = elections
        self.existing_script = existing_script

    @property
    def importer_class(self):
        classes = {
            "Idox Eros (Halarose)": "BaseHalaroseCsvImporter",
            "Xpress WebLookup": "BaseXpressWebLookupCsvImporter",
            "Xpress DC": "BaseXpressDemocracyClubCsvImporter",
            "Democracy Counts": "BaseDemocracyCountsCsvImporter",
        }
        return classes[self.ems]

    @property
    def delimiter(self):
        return "\t" if self.addresses_name[-3:] in ("tsv", "TSV") else ","

    @property
    def csv_delimiter_string(self):
        if self.delimiter == ",":
            return ""
        else:
            return f"\n    csv_delimiter = {repr(self.delimiter)}"

    @property
    def csv_encoding_string(self):
        if self.encoding == "utf-8":
            return ""
        else:
            return f"\n    csv_encoding = {repr(self.encoding)}"

    @property
    def script(self):
        try:
            script = self._get_updated_existing_script()
        except Exception:
            raise
            logger.exception(
                "Exception modifying existing script; returning simple script instead."
            )
            script = self._get_new_script()

        # Run the updated script through black before returning it
        return black.format_str(script, mode=black.Mode())

    def _get_new_script(self):
        return f"""\
from data_importers.management.commands import {self.importer_class}


class Command({self.importer_class}):
    council_id = "{self.council_id}"
    addresses_name = "{self.addresses_name}"
    stations_name = "{self.stations_name}"
    elections = {self.elections}{self.csv_encoding_string}{self.csv_delimiter_string}
"""

    def _get_updated_existing_script(self):
        """Update an existing script with the new Command parameters.

        This uses the `ast` module to parse the existing script, and then:

        * ensures that the Command has the right base class
        * adds, removes and updates assignment statements in the Command as necessary

        It has a couple of limitations:

        * Multiple assignments are ignored, so a new assignment will be added later on.
          This can be tidied up by hand.

        * It might break an "import [...].commands from [...]" line if the original line
          didn't import only the previous command base class.
        """
        existing_script = self.existing_script or self._get_new_script()
        module = ast.parse(existing_script)

        import_module = "data_importers.management.commands"
        import_names = [ast.alias(name=self.importer_class, asname=None)]
        command_bases = [ast.Name(id=self.importer_class)]

        desired_assigns = {
            "council_id": ast.Constant(self.council_id, kind=None),
            "addresses_name": ast.Constant(self.addresses_name, kind=None),
            "stations_name": ast.Constant(self.stations_name, kind=None),
            "elections": ast.List(
                [ast.Constant(election, kind=None) for election in self.elections]
            ),
            "csv_encoding": (
                None
                if self.encoding == "utf-8"
                else ast.Constant(self.encoding, kind=None)
            ),
            "csv_delimiter": (
                None
                if self.delimiter == ","
                else ast.Constant(self.delimiter, kind=None)
            ),
        }

        # First, find the base importer command import statement and Command class definition.
        # If either don't exist we create a new one and add it to the module (at the top and
        # the bottom, respectively).

        import_stmt = None
        classdef_stmt = None

        for i, stmt in enumerate(list(module.body)):
            if isinstance(stmt, ast.ImportFrom):
                if stmt.module != import_module:
                    continue
                stmt.names = import_names
                import_stmt = stmt
            if isinstance(stmt, ast.ClassDef) and stmt.name == "Command":
                classdef_stmt = stmt
                # Remove trailing module-level statements; we'll readd it verbatim later.
                module.body[i + 1 :] = []
                break

        if not import_stmt:
            module.body.insert(
                0, ast.ImportFrom(level=0, module=import_module, names=command_bases)
            )

        if classdef_stmt:
            classdef_stmt.bases = command_bases
        else:
            classdef_stmt = ast.ClassDef(name="Command", bases=command_bases)
            module.body.append(classdef_stmt)

        # Next find all the existing assignments for the names we care about.

        assigns = {}
        last_assignment_line = classdef_stmt.lineno + 1
        for stmt in classdef_stmt.body:
            # Ignore unpacking assignments
            if (
                isinstance(stmt, ast.Assign)
                and len(stmt.targets) == 1
                and stmt.targets[0].id in desired_assigns
            ):
                assigns[stmt.targets[0].id] = stmt
                last_assignment_line = stmt.end_lineno
            else:
                break

        # Remove trailing ClassDef statements; we'll re-add it verbatim later.
        classdef_stmt.body[len(assigns) :] = []

        # Finally, we reconcile the assignments.

        for name, value in desired_assigns.items():
            if name in assigns and value:
                # existing assignment: update it
                assigns[name].value = value
            elif name not in assigns and value:
                # no existing assignment, so we need to add a new one
                classdef_stmt.body.append(
                    ast.Assign(targets=[ast.Name(name)], value=value, lineno=None),
                )
            elif name in assigns and not value:
                # existing assignment, but we don't want it
                classdef_stmt.body.remove(assigns[name])

        # Find all the trailing lines, so we can reinclude them as appropriate.
        # Following lines in the class definition block are commented. The lines
        # after that in the module body are not commented.
        # We can't do this using the AST because that drops comments, which we want
        # to preserve.

        class_following_lines = existing_script.splitlines(keepends=True)[
            last_assignment_line : classdef_stmt.end_lineno
        ]
        while class_following_lines and not class_following_lines[0].strip():
            class_following_lines.pop(0)

        module_following_lines = existing_script.splitlines(keepends=True)[
            classdef_stmt.end_lineno :
        ]
        while module_following_lines and not module_following_lines[0].strip():
            module_following_lines.pop(0)

        script = ast_unparse(module)
        script += (
            "\n\n"
            + "".join(
                "    # " + re.sub("^    ", "", line) for line in class_following_lines
            )
            + "".join(module_following_lines)
        )

        return script
