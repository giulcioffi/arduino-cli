# This file is part of arduino-cli.
#
# Copyright 2020 ARDUINO SA (http://www.arduino.cc/)
#
# This software is released under the GNU General Public License version 3,
# which covers the main part of arduino-cli.
# The terms of this license can be found at:
# https://www.gnu.org/licenses/gpl-3.0.en.html
#
# You can be released from the requirements of the above licenses by purchasing
# a commercial license. Buying such a license is mandatory if you want to modify or
# otherwise use the software for commercial activities involving the Arduino
# software without disclosing the source code of your own applications. To purchase
# a commercial license, send an email to license@arduino.cc.
from pathlib import Path
import json
import yaml


def test_init(run_command, data_dir, working_dir):
    result = run_command("config init")
    assert "" == result.stderr
    assert result.ok
    assert data_dir in result.stdout


def test_init_with_existing_custom_config(run_command, data_dir, working_dir, downloads_dir):
    result = run_command("config init --additional-urls https://example.com")
    assert result.ok
    assert data_dir in result.stdout

    config_file = open(Path(data_dir) / "arduino-cli.yaml", "r")
    configs = yaml.load(config_file.read(), Loader=yaml.FullLoader)
    config_file.close()
    assert ["https://example.com"] == configs["board_manager"]["additional_urls"]
    assert ["packages/package_index.json"] == configs["board_manager"]["additional_paths"]
    assert "50051" == configs["daemon"]["port"]
    assert data_dir == configs["directories"]["data"]
    assert downloads_dir == configs["directories"]["downloads"]
    assert data_dir == configs["directories"]["user"]
    assert "" == configs["logging"]["file"]
    assert "text" == configs["logging"]["format"]
    assert "info" == configs["logging"]["level"]
    assert ":9090" == configs["telemetry"]["addr"]
    assert configs["telemetry"]["enabled"]

    config_file_path = Path(working_dir) / "config" / "test" / "config.yaml"
    assert not config_file_path.exists()
    result = run_command(f'config init --dest-file "{config_file_path}"')
    assert result.ok
    assert str(config_file_path) in result.stdout

    config_file = open(config_file_path, "r")
    configs = yaml.load(config_file.read(), Loader=yaml.FullLoader)
    config_file.close()
    assert [] == configs["board_manager"]["additional_urls"]
    assert [] == configs["board_manager"]["additional_paths"]
    assert "50051" == configs["daemon"]["port"]
    assert data_dir == configs["directories"]["data"]
    assert downloads_dir == configs["directories"]["downloads"]
    assert data_dir == configs["directories"]["user"]
    assert "" == configs["logging"]["file"]
    assert "text" == configs["logging"]["format"]
    assert "info" == configs["logging"]["level"]
    assert ":9090" == configs["telemetry"]["addr"]
    assert configs["telemetry"]["enabled"]


def test_init_overwrite_existing_custom_file(run_command, data_dir, working_dir, downloads_dir):
    result = run_command("config init --additional-urls https://example.com")
    assert result.ok
    assert data_dir in result.stdout

    config_file = open(Path(data_dir) / "arduino-cli.yaml", "r")
    configs = yaml.load(config_file.read(), Loader=yaml.FullLoader)
    config_file.close()
    assert ["https://example.com"] == configs["board_manager"]["additional_urls"]
    assert ["packages/package_index.json"] == configs["board_manager"]["additional_paths"]
    assert "50051" == configs["daemon"]["port"]
    assert data_dir == configs["directories"]["data"]
    assert downloads_dir == configs["directories"]["downloads"]
    assert data_dir == configs["directories"]["user"]
    assert "" == configs["logging"]["file"]
    assert "text" == configs["logging"]["format"]
    assert "info" == configs["logging"]["level"]
    assert ":9090" == configs["telemetry"]["addr"]
    assert configs["telemetry"]["enabled"]

    result = run_command("config init --overwrite")
    assert result.ok
    assert data_dir in result.stdout

    config_file = open(Path(data_dir) / "arduino-cli.yaml", "r")
    configs = yaml.load(config_file.read(), Loader=yaml.FullLoader)
    config_file.close()
    assert [] == configs["board_manager"]["additional_urls"]
    assert [] == configs["board_manager"]["additional_paths"]
    assert "50051" == configs["daemon"]["port"]
    assert data_dir == configs["directories"]["data"]
    assert downloads_dir == configs["directories"]["downloads"]
    assert data_dir == configs["directories"]["user"]
    assert "" == configs["logging"]["file"]
    assert "text" == configs["logging"]["format"]
    assert "info" == configs["logging"]["level"]
    assert ":9090" == configs["telemetry"]["addr"]
    assert configs["telemetry"]["enabled"]


def test_init_dest_absolute_path(run_command, working_dir):
    dest = Path(working_dir) / "config" / "test"
    expected_config_file = dest / "arduino-cli.yaml"
    assert not expected_config_file.exists()
    result = run_command(f'config init --dest-dir "{dest}"')
    assert result.ok
    assert str(expected_config_file) in result.stdout
    assert expected_config_file.exists()


def test_init_dest_relative_path(run_command, working_dir):
    dest = Path(working_dir) / "config" / "test"
    expected_config_file = dest / "arduino-cli.yaml"
    assert not expected_config_file.exists()
    result = run_command('config init --dest-dir "config/test"')
    assert result.ok
    assert str(expected_config_file) in result.stdout
    assert expected_config_file.exists()


def test_init_dest_flag_with_overwrite_flag(run_command, working_dir):
    dest = Path(working_dir) / "config" / "test"

    expected_config_file = dest / "arduino-cli.yaml"
    assert not expected_config_file.exists()

    result = run_command(f'config init --dest-dir "{dest}"')
    assert result.ok
    assert expected_config_file.exists()

    result = run_command(f'config init --dest-dir "{dest}"')
    assert result.failed
    assert "Config file already exists, use --overwrite to discard the existing one." in result.stderr

    result = run_command(f'config init --dest-dir "{dest}" --overwrite')
    assert result.ok
    assert str(expected_config_file) in result.stdout


def test_init_dest_and_config_file_flags(run_command, working_dir):
    result = run_command('config init --dest-file "some_other_path" --dest-dir "some_path"')
    assert result.failed
    assert "Can't use both --dest-file and --dest-dir flags at the same time." in result.stderr


def test_init_config_file_flag_absolute_path(run_command, working_dir):
    config_file = Path(working_dir) / "config" / "test" / "config.yaml"
    assert not config_file.exists()
    result = run_command(f'config init --dest-file "{config_file}"')
    assert result.ok
    assert str(config_file) in result.stdout
    assert config_file.exists()


def test_init_config_file_flag_relative_path(run_command, working_dir):
    config_file = Path(working_dir) / "config.yaml"
    assert not config_file.exists()
    result = run_command('config init --dest-file "config.yaml"')
    assert result.ok
    assert str(config_file) in result.stdout
    assert config_file.exists()


def test_init_config_file_flag_with_overwrite_flag(run_command, working_dir):
    config_file = Path(working_dir) / "config" / "test" / "config.yaml"
    assert not config_file.exists()

    result = run_command(f'config init --dest-file "{config_file}"')
    assert result.ok
    assert config_file.exists()

    result = run_command(f'config init --dest-file "{config_file}"')
    assert result.failed
    assert "Config file already exists, use --overwrite to discard the existing one." in result.stderr

    result = run_command(f'config init --dest-file "{config_file}" --overwrite')
    assert result.ok
    assert str(config_file) in result.stdout


def test_dump(run_command, data_dir, working_dir):
    # Create a config file first
    config_file = Path(working_dir) / "config" / "test" / "config.yaml"
    assert not config_file.exists()
    result = run_command(f'config init --dest-file "{config_file}"')
    assert result.ok
    assert config_file.exists()

    result = run_command(f'config dump --config-file "{config_file}" --format json')
    assert result.ok
    settings_json = json.loads(result.stdout)
    assert [] == settings_json["board_manager"]["additional_urls"]
    assert [] == settings_json["board_manager"]["additional_paths"]

    result = run_command('config init --additional-urls "https://example.com"')
    assert result.ok
    config_file = Path(data_dir) / "arduino-cli.yaml"
    assert str(config_file) in result.stdout
    assert config_file.exists()

    result = run_command("config dump --format json")
    assert result.ok
    settings_json = json.loads(result.stdout)
    assert ["https://example.com"] == settings_json["board_manager"]["additional_urls"]
    assert ["packages/package_index.json"] == settings_json["board_manager"]["additional_paths"]


def test_dump_with_config_file_flag(run_command, working_dir):
    # Create a config file first
    config_file = Path(working_dir) / "config" / "test" / "config.yaml"
    assert not config_file.exists()
    result = run_command(f'config init --dest-file "{config_file}" --additional-urls=https://example.com')
    assert result.ok
    assert config_file.exists()

    result = run_command(f'config dump --config-file "{config_file}" --format json')
    assert result.ok
    settings_json = json.loads(result.stdout)
    assert ["https://example.com"] == settings_json["board_manager"]["additional_urls"]
    assert ["packages/package_index.json"] == settings_json["board_manager"]["additional_paths"]

    result = run_command(
        f'config dump --config-file "{config_file}" --additional-urls=https://another-url.com --format json'
    )
    assert result.ok
    settings_json = json.loads(result.stdout)
    assert ["https://another-url.com"] == settings_json["board_manager"]["additional_urls"]
    assert ["packages/package_new_index.json"] == settings_json["board_manager"]["additional_paths"]
