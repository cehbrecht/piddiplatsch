import pytest

from click.testing import CliRunner

from piddiplatsch import cli


@pytest.mark.skip(reason="not working")
def test_cli():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "piddiplatsch.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
