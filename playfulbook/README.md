# playfulbook media

Compressed image, audio and video assets for [playfulbook](https://github.com/rose-and-code/playfulbook).
Original relative paths are preserved under this directory, including public assets, prototype images and style samples.

| Type | Files | Original MiB | Compressed MiB |
|---|---:|---:|---:|
| JPEG illustrations | 533 | 616.49 | 169.95 |
| JPEG covers/posters | 28 | 4.81 | 3.54 |
| Audio | 106 | 573.69 | 271.23 |
| Video | 170 | 1841.00 | 185.46 |

Total: **837 files, 3036.00 -> 630.19 MiB (79.24% smaller)**.

## Delivery

Use a full immutable Git commit in place of `<commit>`:

```
https://cdn.jsdelivr.net/gh/rose-and-code/html-rebuttal-assets@<commit>/playfulbook/public/images/covers/vegetarian.jpg
https://cdn.jsdelivr.net/gh/rose-and-code/html-rebuttal-assets@<commit>/playfulbook/public/audio/bgm.mp3
https://cdn.jsdelivr.net/gh/rose-and-code/html-rebuttal-assets@<commit>/playfulbook/public/quiz/finitegames/c01.mp4
```

`manifest.json` records every original/output SHA-256, byte count, image dimensions, audio/video streams and durations.
The embedded Su Shi soundtrack is exported as `public/audio/sushi-map/bgm.mp3` (the original embedded payload was MP4/AAC).

## Compression

- JPEG: maximum 1920 px edge, quality 82, progressive, 4:4:4 chroma; preserve aspect ratio.
- MP4: H.264 CRF 24, maximum 1280 px edge, original frame rate, yuv420p, faststart; keep any audio as AAC 128 kbps.
- MP3: at most 128 kbps; long candidate tracks use a lower bitrate to stay below 19 MB. Preserve full duration and tags.
- Keep the original encoding when it is already smaller. Hash-identical inputs reuse one encoding while retaining their paths.
- Source and exported durations must differ by at most 0.15 seconds, and existing audio streams must remain present.

Reproduction script: `scripts/compress-media.py` in the source repository (Pillow + FFmpeg/ffprobe).
Source code revision before migration: `4d3a7835a0053c07aa68aec0e1b81a55fdb736fc`. Original binaries remain recoverable from that revision.
