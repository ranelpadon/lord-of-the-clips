from commands.merge import merge
from commands.trim import trim

import rich_click as click
from rich.traceback import install

# Improve traceback rendering.
install()

# https://github.com/ewels/rich-click/#configuration-options
click.rich_click.MAX_WIDTH = 120
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.SHOW_METAVARS_COLUMN = True
click.rich_click.STYLE_ARGUMENT = 'blue'
click.rich_click.STYLE_HELPTEXT = ''
click.rich_click.STYLE_OPTION = 'yellow'
click.rich_click.USE_RICH_MARKUP = True


# Register sub-commands as part of the `cli` group.
@click.group()
def cli():
    pass


cli.add_command(merge)
cli.add_command(trim)


if __name__ == '__main__':
    cli()
