# 🎥✂️🔗 lord-of-the-clips (lotc)
Video downloader, trimmer, and merger using the terminal. Supports YouTube, Facebook, Reddit, Twitter, TikTok, Instagram, LinkedIn, 9GAG, [etc](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md). Downloads/trims at multiple points. Merges multiple clips.

## 💫 Background
As per the [Pareto Principle](https://en.wikipedia.org/wiki/Pareto_principle), a video usually has its best parts. Hence, Reels/Shorts/Stories are popular nowadays. Likewise, I frequently download videos from various sites (e.g. YouTube, Facebook, Reddit, etc) using various online video downloaders, then I clip the most interesting/best parts only which is usually posted in social media sites or shared in private/group chats.

Got tired of these routines eventually, and I want a tool that given a URL and timestamps/durations will download the video AND auto-clip them at the desired segments in a single command AND it should support multiple sites. This is the missing tool that I wanted. In the simplest case, this `lotc` CLI app will download the full video.

## ⚡Features
- downloads a video and auto-trims/clips the specified durations
- trims a saved video file and/or clips the specified durations
- merges saved video files, usually for concatenating related clips
- provides smart output file name by default
- accepts a custom output file name
- leverages CLI styling for better experience

## 🦾 Standing on the Shoulders of Giants
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): video downloader
- [moviepy](https://github.com/Zulko/moviepy): video trimmer/merger
- [click](https://github.com/pallets/click/): CLI app creator
- [rich](https://github.com/Textualize/rich) / [rich-click](https://github.com/ewels/rich-click/): CLI app styler

## 🔨 Installation

```shell
pip install lord-of-the-clips
```

This will install a global `lotc` shell command which you could run in the terminal.
`lotc` is the acronym for `lord-of-the-clips`.

## 🔧 Dependencies

`ffmpeg` is [strongly recommended](https://github.com/yt-dlp/yt-dlp#strongly-recommended) by `yt-dlp` to be installed since some websites have split video/audio files:
- Mac: `brew install ffmpeg`
- Ubuntu: `sudo apt install ffmpeg`
- [Others](https://ffmpeg.org/download.html)


## ⚙️ Usage

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

## 🚀 Demo
The GIF below demonstrates the output of `lotc --help` command and its `lotc download --help` subcommand, and running an example provided in the output:
![See https://github.com/ranelpadon/lord-of-the-clips#-demo](https://github.com/ranelpadon/lord-of-the-clips/blob/main/demo.gif)

## ⚠️ Rate Limits
Some sites (e.g. Facebook) imposes scraping rate limits on their pages and could cause issues in your succeeding downloads.
Hence, throttle your usage or don't use `lotc` excessively in a short amount of time.
