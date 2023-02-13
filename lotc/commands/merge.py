import rich_click as click

from lotc.utils import (
    build_clip_objects_from_clip_names,
    check_valid_file_extension,
    get_concatenated_clip_names,
    merge_clips_and_save,
    print_in_tree,
    print_rich,
)


@click.command()
@click.argument('clips', nargs=-1, required=True)
@click.option('-o', '--output', help='The output file name (e.g. "merged.mp4"). Should have the ".mp4" file extension.')
def merge(clips, output):
    """
    Merges the specified video CLIPS (filenames).

    [dim][/]

    \b
    Examples:
        [green]lotc[/] [cyan]merge[/] "foo-1.mp4" "foo-2.mp4"
        [green]lotc[/] [cyan]merge[/] --output merged.mp4 "foo-1.mp4" "foo-2.mp4" "bar.mp4"
    """
    if output:
        check_valid_file_extension(output)

    print_rich('Merging these video clips:')
    print_in_tree(branches=clips)

    clip_names = clips
    clip_objects = build_clip_objects_from_clip_names(clip_names)
    output_file = output or get_concatenated_clip_names(clip_names)

    merge_clips_and_save(clip_objects, output_file)
    print_rich(f'\nOutput file saved as [blue]{output_file}[/blue]')
