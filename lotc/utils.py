import re
from pathlib import Path

from moviepy.editor import (
    VideoFileClip,
    concatenate_videoclips,
)
from rich import print as print_rich
from rich.traceback import install
from rich.tree import Tree

# Improve traceback rendering.
install()

VIDEO_DOWNLOADER = 'yt-dlp'

# Use a safe conversion format since MoviePy has issue with some codecs.
OUTPUT_FILE_FORMAT = 'mp4'
OUTPUT_FILE_EXTENSION = f'.{OUTPUT_FILE_FORMAT}'


def strip_escape_characters(url):
    # Pasting URL in the terminal may insert the `\` escape characters, remove it.
    return url.replace('\\', '')


def strip_bracketed_characters(text):
    # The VIDEO_DOWNLOADER will insert tokens in the downloaded video's filename
    # which messes-up with `rich`'s print function due to the enclosing brackets.
    return re.sub(r'\s?\[.+\]', '', text)


def split_timestamps(timestamps):
    splitted_timestamps = []

    for _timestamps in timestamps:
        clip = _timestamps.split('-')

        # `strip()` handles the case of "1:30 - 1:45".
        clip_start = clip[0].strip()
        clip_end = clip[1].strip()

        splitted_timestamps.append([clip_start, clip_end])

    return splitted_timestamps


def build_clip_objects_from_timestamps(input_video, timestamps):
    main_clip_object = VideoFileClip(input_video)
    splitted_timestamps = split_timestamps(timestamps)
    clip_objects = []

    for clip_timestamps in splitted_timestamps:
        # Expand the timestamp tuples and create a new clip.
        clip_object = main_clip_object.subclip(*clip_timestamps)
        clip_objects.append(clip_object)

    return clip_objects


def check_file_exists(filename):
    path_object = Path(filename)

    if not path_object.exists():
        message = f'"{filename}" could not be found!'
        raise FileNotFoundError(message)


def check_valid_file_extension(filename):
    path_object = Path(filename)
    file_extension = path_object.suffix

    message = f'"{filename}" must be in "{OUTPUT_FILE_EXTENSION}" format!'
    assert file_extension == OUTPUT_FILE_EXTENSION, message


def get_filename_without_extension(filename):
    path_object = Path(filename)

    # Get the `baz` in `foo/bar/baz.mp4`.
    return path_object.stem


def build_clip_objects_from_clip_names(clip_names):
    clip_objects = []

    for clip_name in clip_names:
        check_file_exists(clip_name)
        clip_object = VideoFileClip(clip_name)
        clip_objects.append(clip_object)

    return clip_objects


def get_concatenated_clip_names(clip_names):
    filenames = []

    for clip_name in clip_names:
        check_file_exists(clip_name)
        filename_without_extension = get_filename_without_extension(clip_name)
        filenames.append(filename_without_extension)

    concatenated_names = ' - '.join(filenames)
    return f'{concatenated_names}{OUTPUT_FILE_EXTENSION}'


def get_video_filename_from_download_logs(download_logs):
    # Match if the file is merged (mkv = mp4 + webm) or already existing.
    # Happens if `ffmpeg` is installed.
    pattern = (
        '(\[ffmpeg\])? Merging formats into "(.+)"'
        '|\[download\] (.+) has already been downloaded and merged'
    )
    match = re.search(pattern, download_logs)
    if match:
        merged_filename_new = match.group(2)
        merged_filename_existing = match.group(3)
        return merged_filename_new or merged_filename_existing

    # Match if it's new file or already existing.
    match = re.search('\[download\] (Destination: (.+)|(.+) has already been downloaded)', download_logs)

    if match:
        filename_new = match.group(2)
        filename_existing = match.group(3)
        return filename_new or filename_existing


def get_effective_filename(filename, descriptor):
    if not descriptor:
        return filename

    path_object = Path(filename)

    # `/foo/bar/baz.mp4` will become `/foo/bar/baz`
    truncated_filename = path_object.with_suffix('')

    return f'{truncated_filename} - {descriptor}{OUTPUT_FILE_EXTENSION}'


def save_as(clip_object, filename):
    # Disable the logger to minimize clutter.
    clip_object.write_videofile(filename, logger=None)


def merge_clips_and_save(clip_objects, filename):
    merged_clips = concatenate_videoclips(clip_objects)
    merged_clips.write_videofile(filename, logger=None)


def print_in_tree(header='', branches=None):
    tree = Tree(header)

    if not branches:
        branches = []

    for branch in branches:
        tree.add(f'[blue]{branch}[/]')

    print_rich(tree)
