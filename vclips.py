import os
import re
from pathlib import Path

import delegator
import rich_click as click
from moviepy.editor import (
    VideoFileClip,
    concatenate_videoclips,
)
from rich import print as print_rich
from rich.traceback import install
from rich.tree import Tree

# Debugging utility.
try:
    from icecream import ic  # noqa
except ImportError:
    pass

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

VIDEO_DOWNLOADER = 'youtube-dl'

# Use a safe conversion format since MoviePy has issue with some codecs.
OUTPUT_FORMAT = '.mp4'


def _strip_escape_characters(url):
    # Pasting URL in the terminal may insert the `\` escape characters, remove it.
    return url.replace('\\', '')


def _download_video(url):
    command = delegator.run(f'{VIDEO_DOWNLOADER} {url}')
    return command.out


def _split_timestamps(timestamps):
    splitted_timestamps = []

    for _timestamps in timestamps:
        clip = _timestamps.split('-')

        # `strip()` handles the case of "1:30 - 1:45".
        clip_start = clip[0].strip()
        clip_end = clip[1].strip()

        splitted_timestamps.append([clip_start, clip_end])

    return splitted_timestamps


def _build_clip_objects_from_timestamps(input_video, timestamps):
    main_clip_object = VideoFileClip(input_video)
    splitted_timestamps = _split_timestamps(timestamps)
    clip_objects = []

    for clip_timestamps in splitted_timestamps:
        # Expand the timestamp tuples and create a new clip.
        clip_object = main_clip_object.subclip(*clip_timestamps)
        clip_objects.append(clip_object)

    return clip_objects


def _check_file_exists(filename):
    path_object = Path(filename)

    if not path_object.exists():
        message = f'"{filename}" could not be found!'
        raise FileNotFoundError(message)


def _check_valid_file_extension(filename):
    path_object = Path(filename)
    file_extension = path_object.suffix
    file_extension_recommended = '.mp4'

    message = f'"{filename}" must be in ".mp4" format!'
    assert file_extension == file_extension_recommended, message


def _build_clip_objects_from_clip_names(clip_names):
    clip_objects = []

    for clip_name in clip_names:
        _check_file_exists(clip_name)
        clip_object = VideoFileClip(clip_name)
        clip_objects.append(clip_object)

    return clip_objects


def _get_concatenated_clip_names(clip_names):
    filenames = []

    for clip_name in clip_names:
        _check_file_exists(clip_name)
        path_object = Path(clip_name)

        # Get the `baz` in `foo/bar/baz.mp4`.
        filename_without_extension = path_object.stem
        filenames.append(filename_without_extension)

    concatenated_names = ' - '.join(filenames)

    return f'{concatenated_names}{OUTPUT_FORMAT}'


def _get_video_filename_from_download_output(download_output):
    # Match if the file is merged (mkv = mp4 + webm) or already existing.
    # Happens if `ffmpeg` is installed.
    pattern = (
        '(\[ffmpeg\])? Merging formats into "(.+mkv|.+mp4)"'
        '|\[download\] (.+mkv|.+mp4) has already been downloaded and merged'
    )
    match = re.search(pattern, download_output)
    if match:
        merged_filename_new = match.group(2)
        merged_filename_existing = match.group(3)
        return merged_filename_new or merged_filename_existing

    # Match if it's new file or already existing.
    match = re.search('\[download\] (Destination: (.+mp4)|(.+mp4) has already been downloaded)', download_output)

    if match:
        filename_new = match.group(2)
        filename_existing = match.group(3)
        return filename_new or filename_existing


def _get_effective_filename(filename, descriptor):
    path_object = Path(filename)

    # `/foo/bar/baz.mp4` will become `/foo/bar/baz`
    truncated_filename = path_object.with_suffix('')

    return f'{truncated_filename} - {descriptor}{OUTPUT_FORMAT}'


def _merge_clips_and_save(clip_objects, filename, descriptor=''):
    merged_clips = concatenate_videoclips(clip_objects)

    if descriptor:
        filename = _get_effective_filename(filename, descriptor)

    merged_clips.write_videofile(filename, logger=None)

    print()
    print_rich(f'Output file saved as [blue]{filename}[/blue]')


def print_in_tree(header='', branches=None):
    tree = Tree(header)

    if not branches:
        branches = []

    for branch in branches:
        tree.add(branch)

    print_rich(tree)


# Register sub-commands as part of `cli` group.
@click.group()
def cli():
    pass


@cli.command()
@click.argument('url_or_file')
@click.argument('timestamps', nargs=-1)
@click.option('--output', help='The output file name (e.g. "trimmed.mp4"). Should have the ".mp4" file extension.')
def trim(url_or_file, timestamps, output):
    """
    Trims the video in the URL_OR_FILE in the specified TIMESTAMPS.

    \b
    If it's a URL, it will download the video first before trimming.
    Supports multiple video sites (YouTube, Facebook, etc):
    [link]http://ytdl-org.github.io/youtube-dl/supportedsites.html[/]

    TIMESTAMPS are the trimming points, could be none or many.

    \b
    [dim]
    Sample runs:

    \b
    [green]URL[/]
    * vclips [cyan]trim[/] https://www.youtube.com/watch?v=Y7JG63IuaWs
    * vclips [cyan]trim[/] https://www.youtube.com/watch?v=Y7JG63IuaWs 0:30-0:45
    * vclips [cyan]trim[/] --output bar.mp4 https://www.youtube.com/watch?v=Y7JG63IuaWs 0:30-0:45 1:10-1:40.8

    \b
    FILE
    * vclips [cyan]trim[/] foo.mp4 0:30-0:45
    * vclips [cyan]trim[/] --output bar.mp4 foo.mp4 0:30-0:45 1:10-1:40.8  [/]
    """
    if output:
        _check_valid_file_extension(output)

    filename = ''
    url_prefix = 'http'
    is_url = url_or_file.startswith(url_prefix)

    if is_url:
        print_rich('Downloading the video...')

        url = url_or_file
        url = _strip_escape_characters(url)

        download_output = _download_video(url)
        filename = _get_video_filename_from_download_output(download_output)

    if timestamps:
        print()
        print_rich('Trimming the video with these timestamps:')
        print_in_tree(branches=timestamps)

        output_file = ''
        if is_url:
            clip_objects = _build_clip_objects_from_timestamps(filename, timestamps)
            output_file = output or filename

            _merge_clips_and_save(clip_objects, output_file, 'trimmed')

            # Remove the original video downloaded by VIDEO_DOWNLOADER.
            os.remove(filename)
        else:
            input_video = url_or_file
            _check_file_exists(input_video)

            clip_objects = _build_clip_objects_from_timestamps(input_video, timestamps)
            output_file = output or input_video

            _merge_clips_and_save(clip_objects, output_file, 'trimmed')
    else:
        message = 'There\'s no specified timestamps.'

        if is_url:
            print(f'{message} The full video is downloaded.')
            print_rich(f'\nFile saved as [blue]{filename}[/blue]')
        else:
            input_video = url_or_file
            print_rich(f'{message} The [blue]{input_video}[/blue] will not be trimmed.')


@cli.command()
@click.argument('clips', nargs=-1, required=True)
@click.option('--output', help='The output file name (e.g. "merged.mp4"). Should have the ".mp4" file extension.')
def merge(clips, output):
    """
    Merges the specified video CLIPS.

    \b
    [dim]
    Sample runs:
    \b
    * vclips [cyan]merge[/] foo-1.mp4 foo-2.mp4
    * vclips [cyan]merge[/] --output bar.mp4 foo-1.mp4 foo-2.mp4 baz.mp4  [/]
    """
    if output:
        _check_valid_file_extension(output)

    print_rich('Merging these video clips:')
    print_in_tree(branches=clips)

    clip_names = clips
    clip_objects = _build_clip_objects_from_clip_names(clip_names)
    output_video = output or _get_concatenated_clip_names(clip_names)
    _merge_clips_and_save(clip_objects, output_video)


if __name__ == '__main__':
    cli()
