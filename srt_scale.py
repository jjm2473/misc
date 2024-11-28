import re
import sys

class SubLine:
    def __init__(self, start, end, contents):
        self.start = start
        self.end = end
        self.contents = contents

def calculate_a_b(fs, ls, fv, lv):
    """
    Calculate the linear function parameters a and b.
    
    :param fs: First subtitle start time (milliseconds)
    :param ls: Last subtitle end time (milliseconds)
    :param fv: First video subtitle start time (milliseconds)
    :param lv: Last video subtitle end time (milliseconds)
    :return: (a, b) - parameters of the linear function
    """
    # Calculate a and b
    a = (lv - fv) / (ls - fs)
    b = fv - a * fs
    return a, b

def srt_ts_to_ms(hours, minutes, seconds, milliseconds):
    return (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds

def ms_to_srt_ts(adjusted_milliseconds):
    # Convert back to hours, minutes, seconds, milliseconds
    new_hours = adjusted_milliseconds // (3600 * 1000)
    adjusted_milliseconds %= (3600 * 1000)
    new_minutes = adjusted_milliseconds // (60 * 1000)
    adjusted_milliseconds %= (60 * 1000)
    new_seconds = adjusted_milliseconds // 1000
    new_milliseconds = adjusted_milliseconds % 1000

    return f"{new_hours:02}:{new_minutes:02}:{new_seconds:02},{new_milliseconds:03}"

def apply_linear_function_to_time(hours, minutes, seconds, milliseconds, a, b):
    """Apply the linear function y = ax + b to the time in milliseconds."""
    total_milliseconds = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds
    adjusted_milliseconds = int(a * total_milliseconds + b)
    # Ensure non-negative time
    adjusted_milliseconds = max(0, adjusted_milliseconds)
    
    # Convert back to hours, minutes, seconds, milliseconds
    new_hours = adjusted_milliseconds // (3600 * 1000)
    adjusted_milliseconds %= (3600 * 1000)
    new_minutes = adjusted_milliseconds // (60 * 1000)
    adjusted_milliseconds %= (60 * 1000)
    new_seconds = adjusted_milliseconds // 1000
    new_milliseconds = adjusted_milliseconds % 1000
    
    return f"{new_hours:02}:{new_minutes:02}:{new_seconds:02},{new_milliseconds:03}"

def process_srt(input_path, output_path, a, b):
    """Read, process, and save an SRT file."""
    time_pattern = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})")
    
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    
    adjusted_lines = []
    for line in lines:
        match = time_pattern.match(line)
        if match:
            # Extract start and end times
            start_h, start_m, start_s, start_ms, end_h, end_m, end_s, end_ms = map(int, match.groups())
            # Apply the linear function to both times
            new_start = apply_linear_function_to_time(start_h, start_m, start_s, start_ms, a, b)
            new_end = apply_linear_function_to_time(end_h, end_m, end_s, end_ms, a, b)
            adjusted_lines.append(f"{new_start} --> {new_end}\n")
        else:
            adjusted_lines.append(line)
    
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.writelines(adjusted_lines)

def read_srt(input_path):
    """Read, process, and save an SRT file."""
    time_pattern = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})")
    
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    subs = []
    adjusted_lines = []
    for line in lines:
        match = time_pattern.match(line)
        if match:
            # Extract start and end times
            start_h, start_m, start_s, start_ms, end_h, end_m, end_s, end_ms = map(int, match.groups())
            startms = srt_ts_to_ms(start_h, start_m, start_s, start_ms)
            endms = srt_ts_to_ms(end_h, end_m, end_s, end_ms)
            adjusted_lines = []
            subs.append(SubLine(startms, endms, adjusted_lines))
        else:
            adjusted_lines.append(line)
    return subs

def sub_to_lines(sublines):
    lines = ["1\n"]
    for line in sublines:
        new_start = ms_to_srt_ts(line.start)
        new_end = ms_to_srt_ts(line.end)
        lines.append(f"{new_start} --> {new_end}\n")
        lines.extend(line.contents)
    return lines

def adjust(sublines, a, b):
    for line in sublines:
        line.start = max(0, int(line.start * a + b))
        line.end = max(0, int(line.end * a + b))

# Example usage
input_file = "Futurama.S01E13.chs.utf8.srt"  # Replace with your input file path
output_file = "Futurama.S01E13.chs.scaled.srt"  # Replace with your output file path
fv = "00:00:07,040" # video first subtitle start timestamp
lv = "00:21:46,040" # video last subtitle end timestamp

t_pattern = re.compile(r"(\d{2}):(\d{2}):(\d{2})[\.,](\d{3})")
start_h, start_m, start_s, start_ms = map(int, t_pattern.match(fv).groups())
end_h, end_m, end_s, end_ms = map(int, t_pattern.match(lv).groups())
fvms = srt_ts_to_ms(start_h, start_m, start_s, start_ms)
lvms = srt_ts_to_ms(end_h, end_m, end_s, end_ms)

sublines = read_srt(input_file)
# sys.stderr.writelines(sub_to_lines(sublines))
print("map", sublines[0].start, sublines[len(sublines)-1].end, "to", fvms, lvms, file=sys.stderr)

a, b = calculate_a_b(sublines[0].start, sublines[len(sublines)-1].end, fvms, lvms)

print("a=", a, "b=", b, file=sys.stderr)
adjust(sublines, a, b)

sys.stdout.writelines(sub_to_lines(sublines))
