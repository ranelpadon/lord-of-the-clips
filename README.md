# lord-of-the-clips (lotc)
Video downloader, trimmer, and merger using the terminal. Supports YouTube, Facebook, Reddit, Twitter, TikTok, Instagram, LinkedIn, 9GAG, [etc](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md). Downloads/trims at multiple points. Merges multiple clips.

## Standing on the Shoulders of Giants
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): video downloader
    - `ffmpeg` is [strongly recommended](https://github.com/yt-dlp/yt-dlp#strongly-recommended) to be installed since some websites have split video/audio files:
        - Mac: `brew install ffmpeg`
        - Ubuntu: `sudo apt install ffmpeg`
        - [Others](https://ffmpeg.org/download.html)
- [moviepy](https://github.com/Zulko/moviepy): video trimmer/merger
- [click](https://github.com/pallets/click/): CLI app creator
- [rich](https://github.com/Textualize/rich) / [rich-click](https://github.com/ewels/rich-click/): CLI app styler

## Installation

```shell
pip install lord-of-the-clips
```

This will install a global `lotc` shell command which you could run in the terminal.
`lotc` is the acronym for `lord-of-the-clips`.


## Usage

For further details/sample usages, run this command:

```shell
lotc --help
```

And for its subcommands:

```shell
lotc download --help
lotc trim --help
lotc merge --help
```
