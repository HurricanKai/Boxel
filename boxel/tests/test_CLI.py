from click.testing import CliRunner
from boxel.boxel import cli

runner = CliRunner()

def test_img():
    img_result = runner.invoke(cli, ['-W', '50', 'img', 'artwork/selfie.jpg'])
    broken_result = runner.invoke(cli, ['img', 'not/existing/path.png'])
    help_result = runner.invoke(cli, ['img', '--help'])
    fake_color_result = runner.invoke(cli, ['-C', 'not/a/pallete/path.yml','img'])
    assert img_result.exit_code == 0
    assert help_result.exit_code == 0
    assert help_result.exit_code == 0
    assert broken_result.exit_code != 0
    assert fake_color_result.exit_code != 0

def test_web():
    web_result = runner.invoke(cli, [])
    help_result = runner.invoke(cli, ['web', '--help'])
    multiple_result = runner.invoke(cli, ['web', 'http://www.google.com', 'http://www.why.com'])
    assert web_result.exit_code == 0
    assert help_result.exit_code == 0
    assert multiple_result.exit_code == 0

def test_video():
    help_result = runner.invoke(cli, ['video', '--help'])
    assert help_result.exit_code == 0
