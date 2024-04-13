import math
import time

# Define a list of wave characters for the progress bar
wave_characters = ['~', '-', '=', '#', '*']

async def progress_for_pyrogram(current, total, ud_type, message, start):
    # Calculate the current time and difference from the start
    now = time.time()
    diff = now - start

    # Only update progress at specific intervals or if completed
    if round(diff % 10.00) == 0 or current == total:
        # Calculate progress, speed, and times
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time_ms = round(diff * 1000)
        time_to_completion_ms = round((total - current) / speed * 1000)
        estimated_total_time_ms = elapsed_time_ms + time_to_completion_ms

        # Format elapsed and estimated time
        elapsed_time = TimeFormatter(elapsed_time_ms)
        estimated_total_time = TimeFormatter(estimated_total_time_ms)

        # Calculate the index for wave characters based on time and percentage
        wave_index = int((now * 10) % len(wave_characters))

        # Create progress bar with wave effect
        progress_bar = ''.join(
            wave_characters[(wave_index + i) % len(wave_characters)] if i < math.floor(percentage / 5) else '○' 
            for i in range(20)
        )

        # Create progress message
        progress_message = f"[{progress_bar}] \n**Progress**: {percentage:.2f}%\n"

        # Create final message
        final_message = f"{progress_message}{humanbytes(current)} of {humanbytes(total)}\n" \
                        f"**Speed**: {humanbytes(speed)}/s\n**ETA**: {estimated_total_time}\n"

        # Update the message with the progress information
        try:
            await message.edit(text=f"{ud_type}\n{final_message}")
        except Exception as e:
            print(f"Error updating message: {e}")

def humanbytes(size):
    # Convert bytes to human-readable units
    if not size:
        return ""
    units = ['', 'KiB', 'MiB', 'GiB', 'TiB']
    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} {unit}"

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d, {hours}h, {minutes}m, {seconds}s, {milliseconds}ms".strip(", ")
