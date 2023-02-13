
import rich_click as click

from lotc.utils import (
    build_clip_objects_from_timestamps,
    check_file_exists,
    check_valid_file_extension,
    get_effective_filename,
    merge_clips_and_save,
    print_in_tree,
    print_rich,
)


@click.command()
@click.argument('filename')
@click.argument('durations', nargs=-1)
@click.option('-o', '--output', help='The output file name (e.g. "trimmed.mp4"). Should have the ".mp4" file extension.')
def trim(filename, durations, output):
    """
    Trim the video FILENAME in the specified DURATIONS.

    [dim][/]

    \b
    DURATIONS are the trimming points, could be none or many.
    Format: START-END START-END ...

    \bExamples:
        [green]lotc[/] [cyan]trim[/] "foo.mp4" 0:30-0:45
        [green]lotc[/] [cyan]trim[/] --output trimmed.mp4 "foo.mp4" 0:30-0:45 1:10-1:40.8
    """
    if output:
        check_valid_file_extension(output)

    if durations:
        print()
        print_rich('Trimming the video with these durations:')
        print_in_tree(branches=durations)

        # If `output` file name is specified, don't append the descriptor.
        descriptor = '' if output else 'trimmed'

        check_file_exists(filename)

        clip_objects = build_clip_objects_from_timestamps(filename, durations)
        output_file = output or filename
        output_file = get_effective_filename(output_file, descriptor)

        merge_clips_and_save(clip_objects, output_file)
        print_rich(f'\nOutput file saved as [blue]{output_file}[/blue]')
    else:
        print_rich(f'There\'s no specified duration(s). The [blue]{filename}[/blue] will not be trimmed.')
