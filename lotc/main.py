from lotc.commands.download import download
from lotc.commands.merge import merge
from lotc.commands.trim import trim

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

# Set the commands' ordering, instead of the alphabetical default.
click.rich_click.COMMAND_GROUPS = {
    'lotc': [
        {
            'name': 'Commands',
            'commands': ['download', 'trim', 'merge'],
        },
    ]
}


# Define the main group/namespace for sub-commands.
@click.group()
def cli():
    """
    Use [yellow]--help[/] in subcommands for more details.

    [dim][/]

    \b
    Examples:
        [green]lotc[/] [cyan]download[/] [yellow]--help[/]
        [green]lotc[/] [cyan]trim[/] [yellow]--help[/]
        [green]lotc[/] [cyan]merge[/] [yellow]--help[/]
    """


cli.add_command(download)
cli.add_command(merge)
cli.add_command(trim)


if __name__ == '__main__':
    cli()
