import os

import rich_click as click

from utils import (
    OUTPUT_FILE_EXTENSION,
    OUTPUT_FILE_FORMAT,
    build_clip_objects_from_clip_names,
    build_clip_objects_from_timestamps,
    check_file_exists,
    check_valid_file_extension,
    download_video,
    get_video_filename_from_download_output,
    merge_clips_and_save,
    print_in_tree,
    print_rich,
    strip_escape_characters,
)


@click.command()
@click.argument('url_or_file')
@click.argument('timestamps', nargs=-1)
@click.option('-o', '--output', help='The output file name (e.g. "trimmed.mp4"). Should have the ".mp4" file extension.')
def trim(url_or_file, timestamps, output):
    """
    Trims the video in the URL_OR_FILE in the specified TIMESTAMPS.

    \b
    If it's a URL, it will download the video first before trimming.
    Supports multiple video sites (YouTube, Reddit, Facebook, etc):
    [link=http://ytdl-org.github.io/youtube-dl/supportedsites.html]kuko[/]



    [underline][blue]http://ytdl-org.github.io/youtube-dl/supportedsites.html[/][/]

    TIMESTAMPS are the trimming points, could be none or many.

    \b
    [dim]
    Sample runs:

    \b
    [green]URL[/]
    * lotc [cyan]trim[/] https://www.youtube.com/watch?v=Y7JG63IuaWs
    * lotc [cyan]trim[/] https://www.youtube.com/watch?v=Y7JG63IuaWs 0:30-0:45
    * lotc [cyan]trim[/] --output bar.mp4 https://www.youtube.com/watch?v=Y7JG63IuaWs 0:30-0:45 1:10-1:40.8

    \b
    FILE
    * lotc [cyan]trim[/] foo.mp4 0:30-0:45
    * lotc [cyan]trim[/] --output bar.mp4 foo.mp4 0:30-0:45 1:10-1:40.8  [/]
    """
    if output:
        check_valid_file_extension(output)

    filename = ''
    url_prefix = 'http'
    is_url = url_or_file.startswith(url_prefix)

    if is_url:
        print_rich('Downloading the video...')

        url = url_or_file
        url = strip_escape_characters(url)

        download_output = download_video(url)
        filename = get_video_filename_from_download_output(download_output)

    if timestamps:
        print()
        print_rich('Trimming the video with these timestamps:')
        print_in_tree(branches=timestamps)

        # If `output` file name is specified, don't append the descriptor.
        descriptor = '' if output else 'trimmed'

        output_file = ''
        if is_url:
            clip_objects = build_clip_objects_from_timestamps(filename, timestamps)
            output_file = output or filename

            merge_clips_and_save(clip_objects, output_file, descriptor)

            # Remove the original video downloaded by VIDEO_DOWNLOADER.
            os.remove(filename)
        else:
            input_video = url_or_file
            check_file_exists(input_video)

            clip_objects = build_clip_objects_from_timestamps(input_video, timestamps)
            output_file = output or input_video

            merge_clips_and_save(clip_objects, output_file, descriptor)
    else:
        message = 'There\'s no specified timestamps.'

        if is_url:
            print(f'{message} The full video is downloaded.')
            print_rich(f'\nFile saved as [blue]{filename}[/blue]')
        else:
            input_video = url_or_file
            print_rich(f'{message} The [blue]{input_video}[/blue] will not be trimmed.')
