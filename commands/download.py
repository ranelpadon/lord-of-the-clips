import os

import rich_click as click

from utils import (
    OUTPUT_FILE_EXTENSION,
    build_clip_objects_from_timestamps,
    check_valid_file_extension,
    download_video,
    get_video_filename_from_download_output,
    merge_clips_and_save,
    print_in_tree,
    print_rich,
    strip_escape_characters,
)


@click.command()
@click.argument('url')
@click.argument('timestamps', nargs=-1)
@click.option('-o', '--output', help='The output file name (e.g. "trimmed.mp4"). Should have the ".mp4" file extension.')
def download(url, timestamps, output):
    """
    Download the video in the given URL. If TIMESTAMPS are specified, they will be used for trimming/subclipping.

    \b
    Supports multiple video sites (YouTube, Facebook, Reddit, Twitter, etc).

    \b
    TIMESTAMPS are the trimming/subclipping points, could be none or many.
    Format: START-END START-END ...

    \b[dim]Examples:
        [green]lotc[/] [cyan]download[/] https://www.youtube.com/watch?v=Y7JG63IuaWs
        [green]lotc[/] [cyan]download[/] https://www.youtube.com/watch?v=Y7JG63IuaWs 0:30-0:45
        [green]lotc[/] [cyan]download[/] --output bar.mp4 https://www.youtube.com/watch?v=Y7JG63IuaWs 0:30-0:45 1:10-1:40.8
    """
    if output:
        check_valid_file_extension(output)

    print_rich('Downloading the video...')

    url = strip_escape_characters(url)
    download_output = download_video(url)
    filename = get_video_filename_from_download_output(download_output)

    if timestamps:
        print()
        print_rich('Trimming the video with these timestamps:')
        print_in_tree(branches=timestamps)

        # If `output` file name is specified, don't append the descriptor.
        descriptor = '' if output else 'trimmed'

        clip_objects = build_clip_objects_from_timestamps(filename, timestamps)
        output_file = output or filename

        merge_clips_and_save(clip_objects, output_file, descriptor)

        # Remove the original video downloaded by VIDEO_DOWNLOADER.
        os.remove(filename)
    else:
        message = 'There\'s no specified timestamps.'

        print(f'{message} The full video is downloaded.')
        print_rich(f'\nFile saved as [blue]{filename}[/blue]')
