import ffmpeg

def get_live_source_resolution(url):
    input_stream = ffmpeg.input(url)
    metadata = input_stream.global_args('-hide_banner', '-loglevel', 'quiet', '-vframes', '1', '-vf', 'scale=n:-1').output('null', format='null').run().stdout.decode()
    for line in metadata.split('\n'):
        if 'Stream' in line and 'Video' in line:
            resolution = line.split(',')[0].split(' ')[-1]
            return resolution.split('x')
    return None

# 替换为你的直播源URL
live_source_url = "YOUR_LIVE_SOURCE_URL_HERE"
resolution = get_live_source_resolution(live_source_url)
if resolution:
    print(f"Detected resolution: {resolution[0]}x{resolution[1]}")
else:
    print("Failed to detect resolution.")
