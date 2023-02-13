import os
import re
from time import time
from urllib.parse import urlparse

import delegator
import requests
import rich_click as click
from halo import Halo
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio

from lotc.utils import (
    OUTPUT_FILE_EXTENSION,
    VIDEO_DOWNLOADER,
    build_clip_objects_from_timestamps,
    check_valid_file_extension,
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


@Halo(spinner='dots')
def _download_video(url):
    command = delegator.run(f'{VIDEO_DOWNLOADER} --verbose {url}')

    has_download_error = (command.return_code != 0)
    if has_download_error:
        print_rich('[red]Encountered error while downloading the video![red]')
        print()

        is_facebook_url = ('facebook' in url)
        if is_facebook_url:
            print_rich('[yellow]Trying the alternative FB video downloader...[/]')
            print()

            # `yt-dlp`'s Facebook downloader might be broken due to rate limiting:
            # https://github.com/yt-dlp/yt-dlp/issues/4311
            # Hence, use a custom handler.
            filename = _download_facebook_video(url)
        else:
            print_rich(f'{command.err}')
            quit()
    else:
        download_logs = command.out
        filename = get_video_filename_from_download_logs(download_logs)

    return filename


def _parse_filename_from_download_url(url):
    relative_url = urlparse(url).path
    filename = os.path.basename(relative_url)
    return filename


def _save_linked_file(url):
    response = requests.get(url)
    video_blob = response.content
    filename = _parse_filename_from_download_url(url)

    with open(filename, 'wb') as downloaded_file:
        downloaded_file.write(video_blob)

    return filename


def get_video_html(page_html, fb_video_id):
    pattern = re.compile(f'"id":"{fb_video_id}".+?{fb_video_id}')
    video_data = pattern.search(page_html).group()
    return video_data


def get_video_links(video_html):
    pattern = re.compile(f'(FBQualityLabel=\\\\"\d+p){_get_url_pattern()}')
    video_links = pattern.findall(video_html)
    videos = {_parse_resolution(quality): _strip_special_url_characters(link) for quality, link in video_links}
    return videos


def get_audio_link(video_html):
    pattern = re.compile(f'audio_channel_configuration{_get_url_pattern()}')
    audio_link = pattern.search(video_html).groups()
    return _strip_special_url_characters(audio_link[0])


def get_video_id(url):
    pattern = re.compile('\d+')
    video_id = pattern.search(url).group()
    return video_id


def _get_url_pattern():
    return '.+?(https:\\\\/\\\\/video.+?oe=[A-Za-z0-9]+)'


def _strip_special_url_characters(url):
    return url.replace('amp;', '').replace('\\', '')


def _parse_resolution(video_quality):
    pattern = re.compile('\d+')
    return pattern.search(video_quality).group()


def _get_facebook_request_headers():
    # Required GET headers.
    return {
        'authority': 'www.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en,en-US;q=0.9,pt-BR;q=0.8,pt;q=0.7',
        'cache-control': 'max-age=0',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
        'viewport-width': '2560',
        'x-token': f'{int(time())}',  # Dummy token to differentiate each request.
    }


def _get_video_audio_links(url, video_id):
    page_content = requests.get(url, headers=_get_facebook_request_headers()).text
    html_content = get_video_html(page_content, video_id)
    resolutions_links = get_video_links(html_content)
    best_quality = sorted(resolutions_links.keys(), reverse=True)[0]

    video_link = resolutions_links[best_quality]
    audio_link = get_audio_link(html_content)

    return (
        video_link,
        audio_link
    )


def _download_facebook_video(url):
    """
    Some FB scraping/downloading ideas taken from https://github.com/renanrgs/fb-video-downloader.
    """
    video_id = get_video_id(url)
    video_link, audio_link = _get_video_audio_links(url, video_id)
    video_filename = _save_linked_file(video_link)
    audio_filename = _save_linked_file(audio_link)

    print_rich('Merging the video and audio...')
    print()
    filename = f'{video_id}.mp4'
    ffmpeg_merge_video_audio(
        video_filename,
        audio_filename,
        output=filename,
        vcodec='mpeg4',
        logger=None,
    )

    # Remove temp files.
    os.remove(video_filename)
    os.remove(audio_filename)

    return filename


@click.command()
@click.argument('url')
@click.argument('durations', nargs=-1)
@click.option('-o', '--output', help='The output file name (e.g. "trimmed.mp4"). Should have the ".mp4" file extension.')
def download(url, durations, output):
    """
    Download the video in the given URL. If DURATIONS are specified, they will be used for trimming/subclipping.

    \b
    Supports multiple video sites (YouTube, Facebook, Reddit, Twitter, TikTok, Instagram, LinkedIn, etc).

    \b
    DURATIONS are the trimming/subclipping points, could be empty or many.
    Format: START-END START-END ...

    \bExamples:
        [green]lotc[/] [cyan]download[/] "https://www.youtube.com/watch?v=jSRHpA2giUk"
        [green]lotc[/] [cyan]download[/] "https://www.youtube.com/watch?v=jSRHpA2giUk" 0:30-0:45
        [green]lotc[/] [cyan]download[/] "https://www.youtube.com/watch?v=jSRHpA2giUk" 0:30-0:45 1:10-1:40.8
        [green]lotc[/] [cyan]download[/] --output foo.mp4 "https://www.youtube.com/watch?v=jSRHpA2giUk" 0:30-0:45 1:10-1:40.8
    """
    if output:
        check_valid_file_extension(output)

    print_rich('Downloading the video...')
    print()

    url = strip_escape_characters(url)
    filename = _download_video(url)

    output_file = output or filename
    if durations:
        print_rich('Trimming the video with these durations:')
        print_in_tree(branches=durations)
        print()

        # If `output` file name is specified, don't append the descriptor.
        descriptor = '' if output else 'trimmed'

        with Halo(spinner='dots'):
            clip_objects = build_clip_objects_from_timestamps(filename, durations)
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
            print()

            clip_object = VideoFileClip(filename)

            original_filename = filename
            filename_without_extension = get_filename_without_extension(filename)
            filename = f'{filename_without_extension}{OUTPUT_FILE_EXTENSION}'

            output_file = output or filename
            output_file = strip_bracketed_characters(output_file)

            with Halo(spinner='dots'):
                save_as(clip_object, output_file)
                os.remove(original_filename)
        else:
            output_file = strip_bracketed_characters(output_file)

        print('There\'s no specified duration(s). The full video is downloaded.')
        print()

    print_rich(f'Output file saved as [blue]{output_file}[/blue]')
