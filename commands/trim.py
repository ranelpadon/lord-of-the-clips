import os

import rich_click as click

from utils import (
    build_clip_objects_from_timestamps,
    check_file_exists,
    check_valid_file_extension,
    merge_clips_and_save,
    print_in_tree,
    print_rich,
)


@click.command()
@click.argument('filename')
@click.argument('timestamps', nargs=-1)
@click.option('-o', '--output', help='The output file name (e.g. "trimmed.mp4"). Should have the ".mp4" file extension.')
def trim(filename, timestamps, output):
    """
    Trim the video FILENAME in the specified TIMESTAMPS.

    \b
    TIMESTAMPS are the trimming points, could be none or many.
    Format: START-END START-END ...

    \b[dim]Examples:
        [green]lotc[/] [cyan]trim[/] foo.mp4 0:30-0:45
        [green]lotc[/] [cyan]trim[/] --output bar.mp4 foo.mp4 0:30-0:45 1:10-1:40.8  [/]
    """
    if output:
        check_valid_file_extension(output)

    if timestamps:
        print()
        print_rich('Trimming the video with these timestamps:')
        print_in_tree(branches=timestamps)

        # If `output` file name is specified, don't append the descriptor.
        descriptor = '' if output else 'trimmed'

        check_file_exists(filename)

        clip_objects = build_clip_objects_from_timestamps(filename, timestamps)
        output_file = output or filename
        merge_clips_and_save(clip_objects, output_file, descriptor)
    else:
        message = 'There\'s no specified timestamps.'
        print_rich(f'{message} The [blue]{filename}[/blue] will not be trimmed.')
