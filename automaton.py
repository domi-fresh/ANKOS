import argparse
import cv2 as cv
import numpy as np


def bitParser(number: int) -> list[str]:
    """Converts a rule number (0-255) into an 8-bit string representation."""
    if not (0 <= number <= 255):
        print("Please specify a number between 0 and 255!")
        return []
    return list(f"{number:08b}")


def setup_automaton(
    number: int = 30, iterations: int = 720, width: int = 1280, height: int = 720
):
    # 1. OpenCV VideoWriter requires uint8 arrays (pixel values 0–255)
    img_array = np.zeros((height, width), dtype=np.uint8)
    img_array[height - 1, int(width / 2)] = 255

    bits = bitParser(number)

    rules = {
        "000": bits[7],
        "001": bits[6],
        "010": bits[5],
        "011": bits[4],
        "100": bits[3],
        "101": bits[2],
        "110": bits[1],
        "111": bits[0],
    }

    cur_state = ["0"] * width
    cur_state[int(width / 2)] = "1"

    output_filename = f"automaton-rule_{number}.mp4"
    # 'mp4v' codec offers reliable cross-platform MP4 rendering
    fourcc = cv.VideoWriter_fourcc(*"mp4v")
    writer = cv.VideoWriter(
        output_filename,
        fourcc,
        30,  # Frames per second
        (width, height),
        isColor=True,
    )

    print(
        f"Generating video for Rule {number} ({width}x{height}, {iterations} frames)..."
    )

    for i in range(iterations):
        next_state = []
        for x in range(width):
            # Fixed modulo to boundary % width instead of % (width - 1)
            snippet = cur_state[x - 1] + cur_state[x] + cur_state[(x + 1) % width]
            next_state.append(rules[snippet])

        # Shift existing rows up instantly using NumPy slicing (replaces nested loops)
        img_array[:-1] = img_array[1:]

        # Set active pixels to 255 (white) and inactive to 0 (black)
        img_array[height - 1] = [255 if sym == "1" else 0 for sym in next_state]

        # Convert 1-channel grayscale to 3-channel BGR for codec compatibility
        frame_bgr = cv.cvtColor(img_array, cv.COLOR_GRAY2BGR)
        writer.write(frame_bgr)

        cur_state = next_state

    # 2. Crucial: Release writer to finalize MP4 container header and write to disk
    writer.release()
    print(f"Successfully saved video to {output_filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Specify the Rule number (0 <= n < 256) for the Automaton to write to a video file."
    )

    parser.add_argument(
        "--rule", "-r", type=int, default=30, help="Rule number (0-255)"
    )
    parser.add_argument(
        "--width", "-w", type=int, default=1280, help="Width of the video frame"
    )
    parser.add_argument(
        "--height", type=int, default=720, help="Height of the video frame"
    )
    parser.add_argument(
        "--iterations", "-i", type=int, default=720, help="Number of frames/iterations"
    )

    args = parser.parse_args()

    setup_automaton(
        number=args.rule,
        iterations=args.iterations,
        width=args.width,
        height=args.height,
    )


if __name__ == "__main__":
    main()
