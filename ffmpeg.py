import ffmpeg
 
def get_stream_resolution(stream_url):
    probe = ffmpeg.probe(stream_url)
    video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
    
    if video_streams:
        width = video_streams[0]['width']
        height = video_streams[0]['height']
        return f"{width}x{height}"
    else:
        return "Unable to find video stream"
 
# 示例直播源URL
stream_url = "http://223.82.161.157:8822/hls/1/index.m3u8"
resolution = get_stream_resolution(stream_url)
print(f"The live stream resolution is: {resolution}")
