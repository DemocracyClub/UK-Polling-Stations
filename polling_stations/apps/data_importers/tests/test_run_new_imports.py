import os
import re
from io import StringIO
from unittest.mock import Mock, patch

import pytest

from data_importers.management.commands.run_new_imports import (
    any_import_scripts,
    any_non_import_scripts,
    get_changed_scripts,
    get_paths_changed,
    git_rev_parse,
    is_import_script,
    sha_in_tree,
    get_last_import_sha_from_ssm,
    LastImportShaNotInTreeError,
)
from django.core.management import call_command
from django.test import TestCase, override_settings

no_scripts = [
    "polling_stations/apps/councils/management/commands/import_councils.py",
    "polling_stations/apps/data_importers/base_importers.py",
    "polling_stations/apps/data_importers/data_quality_report.py",
    "polling_stations/apps/data_importers/management/commands/import_eoni.py",
]
all_scripts = [
    "polling_stations/apps/data_importers/management/commands/import_barrow_in_furness.py",
    "polling_stations/apps/data_importers/management/commands/import_wigan.py",
]
mix_of_scripts_and_not_scripts = [
    "polling_stations/apps/data_importers/management/commands/import_barrow_in_furness.py",
    "polling_stations/apps/data_importers/management/commands/import_eoni.py",
    "polling_stations/apps/data_importers/management/commands/import_wigan.py",
    "requirements/base.txt",
]

os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
IN_TREE_SHA = "1012c398b13d2e9c87f718b87e07ee9cd1c26222"


def test_get_paths_changed():
    expected_empty = []
    expected = [
        "package-lock.json",
        "polling_stations/apps/councils/management/commands/import_councils.py",
        "polling_stations/apps/data_importers/base_importers.py",
        "polling_stations/apps/data_importers/data_quality_report.py",
        "polling_stations/apps/data_importers/management/commands/import_barrow_in_furness.py",
        "polling_stations/apps/data_importers/management/commands/import_eoni.py",
        "polling_stations/apps/data_importers/management/commands/import_wigan.py",
        "polling_stations/settings/constants/councils.py",
        "polling_stations/templates/base.html",
        "polling_stations/templates/postcode_view.html",
        "requirements/base.txt",
    ]
    # This commit sha needs to be in the repos history
    assert expected_empty == get_paths_changed(
        IN_TREE_SHA,
        "1012c398b13d2e9c87f718b87e07ee9cd1c26222",
    )

    # These are two commits in the path history that reflect changes only to those files listed in expected
    # I wanted some edge cases (import_councils/import_eoni) so I `git logged` those files and picked something sensible
    assert expected == get_paths_changed(
        "3de44201",
        "53a93ae7",
    )


def test_git_rev_parse():
    assert re.match(r"[a-f0-9]{40}", git_rev_parse("HEAD"))

    # This commit needs to exist in the repo history
    assert git_rev_parse("1012c39") == "1012c398b13d2e9c87f718b87e07ee9cd1c26222"


def test_is_import_script():
    assert is_import_script(
        "polling_stations/apps/data_importers/management/commands/import_barrow_in_furness.py"
    )
    assert is_import_script(
        "polling_stations/apps/data_importers/management/commands/import_north_warwickshire.py"
    )
    assert not is_import_script(
        "polling_stations/apps/councils/management/commands/import_councils.py"
    )
    assert not is_import_script(
        "polling_stations/apps/data_importers/management/commands/import_eoni.py"
    )
    assert not is_import_script(
        "polling_stations/apps/data_importers/management/commands/import.py"
    )


def test_sha_in_tree():
    assert sha_in_tree(IN_TREE_SHA)
    assert not sha_in_tree("not-in-tree")


def test_get_changed_scripts():
    changed = [
        "polling_stations/apps/councils/management/commands/import_councils.py",
        "polling_stations/apps/data_importers/base_importers.py",
        "polling_stations/apps/data_importers/data_quality_report.py",
        "polling_stations/apps/data_importers/management/commands/import_barrow_in_furness.py",
        "polling_stations/apps/data_importers/management/commands/import_eoni.py",
        "polling_stations/apps/data_importers/management/commands/import_wigan.py",
        "requirements/base.txt",
    ]
    expected = [
        "polling_stations/apps/data_importers/management/commands/import_barrow_in_furness.py",
        "polling_stations/apps/data_importers/management/commands/import_wigan.py",
    ]
    assert expected == get_changed_scripts(changed)


def test_any_import_scripts():
    assert any_import_scripts(all_scripts)
    assert not any_import_scripts(no_scripts)
    assert any_import_scripts(mix_of_scripts_and_not_scripts)


def test_any_non_import_scripts():
    assert not any_non_import_scripts(all_scripts)
    assert any_non_import_scripts(no_scripts)
    assert any_non_import_scripts(mix_of_scripts_and_not_scripts)


@pytest.fixture
def mock_ssm():
    with patch("boto3.client") as mock_client:
        mock_ssm = Mock()
        mock_client.return_value = mock_ssm
        yield mock_ssm


def test_get_last_import_sha_success(mock_ssm):
    mock_ssm.get_parameter.return_value = {"Parameter": {"Value": IN_TREE_SHA}}

    result = get_last_import_sha_from_ssm()

    assert result == IN_TREE_SHA
    mock_ssm.get_parameter.assert_called_once_with(Name="LAST_IMPORT_SHA")


def test_get_last_import_sha_failure(mock_ssm):
    not_in_tree_sha = "notintree"
    mock_ssm.get_parameter.return_value = {"Parameter": {"Value": not_in_tree_sha}}

    with pytest.raises(LastImportShaNotInTreeError) as err:
        get_last_import_sha_from_ssm()

    assert (
        str(err.value)
        == f"Value of LAST_IMPORT_SHA ('{not_in_tree_sha}') stored in parameter store not in working tree."
    )
    mock_ssm.get_parameter.assert_called_once_with(Name="LAST_IMPORT_SHA")


@override_settings(DC_ENVIRONMENT="production")
def test_get_last_import_sha_failure_prod(mock_ssm):
    not_in_tree_sha = "notintree"
    mock_ssm.get_parameter.return_value = {"Parameter": {"Value": not_in_tree_sha}}

    with pytest.raises(LastImportShaNotInTreeError) as err:
        get_last_import_sha_from_ssm()

    assert (
        str(err.value)
        == f"Value of LAST_IMPORT_SHA ('{not_in_tree_sha}') stored in parameter store not in working tree."
    )
    mock_ssm.get_parameter.assert_called_once_with(Name="LAST_IMPORT_SHA")


@override_settings(DC_ENVIRONMENT="development")
def test_get_last_import_sha_not_in_tree_dev(mock_ssm):
    not_in_tree_sha = "notintree"
    master_sha = "headofmasterbranch"
    mock_ssm.get_parameter.return_value = {"Parameter": {"Value": not_in_tree_sha}}

    with patch(
        "data_importers.management.commands.run_new_imports.sha_in_tree"
    ) as mock_sha_in_tree, patch(
        "data_importers.management.commands.run_new_imports.git_rev_parse"
    ) as mock_git_rev_parse:
        # First call returns False (original SHA not in tree), second call returns True (master SHA is in tree)
        mock_sha_in_tree.side_effect = [False, True]
        # Just mock rev_parse to always return master
        mock_git_rev_parse.return_value = master_sha

        result = get_last_import_sha_from_ssm()

    assert result == master_sha
    mock_ssm.get_parameter.assert_called_once_with(Name="LAST_IMPORT_SHA")


class test_run_new_imports(TestCase):
    maxDiff = 1000
    run_scripts_mock = Mock()
    run_new_imports_name = "run_new_imports"

    def setUp(self):
        # To get these changes I just `git logged` the imports directory and picked some sensible pairs.
        self.cases = {
            "scripts_only": ("4173ae16", "13accc3f"),
            "app_only": ("f865aaf1", "557c71d6"),
            "scripts_and_app": ("4078f6ac", "cf57110a"),
        }

    @patch(
        "data_importers.management.commands.run_new_imports.Command.run_scripts",
        run_scripts_mock,
    )
    def test_called_with_scripts_only(self):
        out = StringIO()
        (to_sha, from_sha) = self.cases["scripts_only"]

        call_command(
            self.run_new_imports_name,
            to_sha=to_sha,
            from_sha=from_sha,
            stdout=out,
        )
        expected_std_out = "Only import scripts have changed\n"
        self.assertIn(expected_std_out, out.getvalue())
        self.run_scripts_mock.assert_called_with(
            [
                "polling_stations/apps/data_importers/management/commands/import_glasgow_city.py",
                "polling_stations/apps/data_importers/management/commands/import_hackney.py",
                "polling_stations/apps/data_importers/management/commands/import_knowsley.py",
                "polling_stations/apps/data_importers/management/commands/import_lambeth.py",
            ],
            {
                "nochecks": True,
                "verbosity": 1,
                "use_postcode_centroids": False,
                "include_past_elections": False,
            },
        )

    def test_called_with_app_only(self):
        out = StringIO()
        (to_sha, from_sha) = self.cases["app_only"]

        call_command(
            self.run_new_imports_name,
            to_sha=to_sha,
            from_sha=from_sha,
            stdout=out,
        )
        expected_std_out = "No import scripts have changed. So nothing new to import.\n"
        self.assertIn(expected_std_out, out.getvalue())

    def test_called_without_mock(self):
        out = StringIO()
        (to_sha, from_sha) = self.cases["scripts_and_app"]

        call_command(
            self.run_new_imports_name,
            to_sha=to_sha,
            from_sha=from_sha,
            post_deploy=True,
            stdout=out,
        )
        expected_std_out = "App has deployed. OK to run import scripts\n"
        self.assertIn(expected_std_out, out.getvalue())
        self.assertIn("could not be run", out.getvalue())

    def test_called_with_app_and_scripts_before_deploy(self):
        out = StringIO()
        (to_sha, from_sha) = self.cases["scripts_and_app"]

        call_command(
            self.run_new_imports_name,
            to_sha=to_sha,
            from_sha=from_sha,
            stdout=out,
        )
        expected_std_out = "Need to deploy before running import scripts\n"
        self.assertIn(expected_std_out, out.getvalue())

    @patch(
        "data_importers.management.commands.run_new_imports.Command.run_scripts",
        run_scripts_mock,
    )
    def test_called_with_app_and_scripts_after_deploy(self):
        out = StringIO()
        (to_sha, from_sha) = self.cases["scripts_and_app"]

        call_command(
            self.run_new_imports_name,
            to_sha=to_sha,
            from_sha=from_sha,
            post_deploy=True,
            stdout=out,
        )
        expected_std_out = "App has deployed. OK to run import scripts\n"
        self.assertIn(expected_std_out, out.getvalue())
        self.run_scripts_mock.assert_called_with(
            [
                "polling_stations/apps/data_importers/management/commands/import_birmingham.py",
                "polling_stations/apps/data_importers/management/commands/import_ealing.py",
                "polling_stations/apps/data_importers/management/commands/import_hackney.py",
                "polling_stations/apps/data_importers/management/commands/import_hambleton.py",
                "polling_stations/apps/data_importers/management/commands/import_merthyr.py",
                "polling_stations/apps/data_importers/management/commands/import_ryedale.py",
                "polling_stations/apps/data_importers/management/commands/import_somerset_west_taunton.py",
                "polling_stations/apps/data_importers/management/commands/import_south_cambridge.py",
                "polling_stations/apps/data_importers/management/commands/import_south_tyneside.py",
                "polling_stations/apps/data_importers/management/commands/import_welwyn_hatfield.py",
            ],
            {
                "nochecks": True,
                "verbosity": 1,
                "use_postcode_centroids": False,
                "include_past_elections": False,
            },
        )
