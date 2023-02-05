import os

import rich_click as click
from halo import Halo
from moviepy.editor import VideoFileClip

from utils import (
    OUTPUT_FILE_EXTENSION,
    build_clip_objects_from_timestamps,
    check_valid_file_extension,
    download_video,
    get_effective_filename,
    get_filename_without_extension,
    get_video_filename_from_download_logs,
    merge_clips_and_save,
    print_in_tree,
    print_rich,
    save_as,
    strip_bracketed_characters,
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
    download_logs = download_video(url)
    filename = get_video_filename_from_download_logs(download_logs)

    output_file = ''
    if timestamps:
        print()
        print_rich('Trimming the video with these timestamps:')
        print_in_tree(branches=timestamps)

        # If `output` file name is specified, don't append the descriptor.
        descriptor = '' if output else 'trimmed'

        clip_objects = build_clip_objects_from_timestamps(filename, timestamps)
        output_file = output or filename
        output_file = strip_bracketed_characters(output_file)
        output_file = get_effective_filename(output_file, descriptor)

        merge_clips_and_save(clip_objects, output_file)

        # Remove the original video downloaded by VIDEO_DOWNLOADER.
        os.remove(filename)
    else:
        # Convert to `mp4` format if needed.
        # Converting HD videos using MoviePy seems to have better quality
        # than downloading video directly with `--format mp4` option.
        if not filename.endswith(OUTPUT_FILE_EXTENSION):
            print_rich(f'Converting to [green]{OUTPUT_FILE_EXTENSION}[/]...')

            clip_object = VideoFileClip(filename)

            original_filename = filename
            filename_without_extension = get_filename_without_extension(filename)
            filename = f'{filename_without_extension}{OUTPUT_FILE_EXTENSION}'

            output_file = output or filename
            output_file = strip_bracketed_characters(output_file)

            with Halo(spinner='dots'):
                save_as(clip_object, output_file)
                os.remove(original_filename)

        print('There\'s no specified timestamps. The full video is downloaded.')

    print_rich(f'\nOutput file saved as [blue]{output_file}[/blue]')
