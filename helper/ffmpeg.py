import time
import os
import asyncio
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fix_thumb(thumb):
    """
    Processes a thumbnail image to meet specific requirements.
    Args:
        thumb: Path to the thumbnail image.
    Returns:
        Tuple containing width, height, and the processed thumbnail file path.
    """
    width = 0
    height = 0
    if thumb is None:
        return width, height, None
    
    try:
        metadata = extractMetadata(createParser(thumb))
        if metadata and metadata.has("width"):
            width = metadata.get("width")
        if metadata and metadata.has("height"):
            height = metadata.get("height")
            with Image.open(thumb) as img:
                img = img.convert("RGB")
                img.save(thumb, "JPEG")
                img = img.resize((320, height))
                img.save(thumb, "JPEG")
    except Exception as e:
        logger.error(f"Failed to process thumbnail: {e}")
        thumb = None
    
    return width, height, thumb
    
async def take_screen_shot(video_file, output_directory, ttl):
    """
    Takes a screenshot from the video file at the specified time.
    Args:
        video_file: Path to the video file.
        output_directory: Directory where the screenshot will be saved.
        ttl: Time (in seconds) from the start of the video to take the screenshot.
    Returns:
        Path to the saved screenshot image if successful, otherwise None.
    """
    out_put_file_name = f"{output_directory}/{time.time()}.jpg"
    file_generator_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    
    process = await asyncio.create_subprocess_exec(
        *file_generator_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    
    if os.path.exists(out_put_file_name):
        return out_put_file_name
    else:
        logger.error(f"Failed to take screenshot: {e_response}")
        return None
    
