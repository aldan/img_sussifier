import logging
from PIL import Image
import numpy as np

logging.basicConfig(format='%(name)s :: %(levelname)-8s :: %(message)s', level=logging.ERROR)


def get_frames(input_file, output_width=25, resize_filter=Image.BILINEAR):
    """Sussifies image
    :param input_file: input image file
    :param output_width: output width in crewmates (default 25)
    :param resize_filter: filter used to resize image (default Image.BILINEAR)
    :return: list of Image objects (frames)
    """
    # Load twerk frames
    twerk_frames = []
    twerk_frames_data = []  # Image as numpy array, pre-calculated for performance
    for i in range(6):
        try:
            img = Image.open(f"twerk_imgs/{i}.png").convert("RGBA")
        except:
            logging.error('can\'t load frames')
            raise RuntimeError
        twerk_frames.append(img)
        twerk_frames_data.append(np.array(img))
    # Get dimensions of first twerk frame. Assume all frames have same dimensions
    twerk_width, twerk_height = twerk_frames[0].size
    logging.info('frames loaded')

    # Get image to sussify
    try:
        input_image = Image.open(input_file).convert("RGB")
    except:
        logging.error('can\'t load input file')
        raise RuntimeError
    input_width, input_height = input_image.size

    # Height of output gif (in crewmates)
    output_height = int(output_width * (input_height / input_width) * (twerk_width / twerk_height))
    # Width, height of output in pixels
    output_px = (int(output_width * twerk_width), int(output_height * twerk_height))
    # Scale image to number of crewmates, so each crewmate gets one color
    input_image_scaled = input_image.resize((output_width, output_height), resize_filter)
    logging.info('input image loaded')

    # Process frames
    frames = []
    for frame_number in range(6):
        # Create blank canvas
        frame = Image.new(mode="RGBA", size=output_px)
        for y in range(output_height):
            for x in range(output_width):
                r, g, b = input_image_scaled.getpixel((x, y))

                # Grab the twerk data we calculated earlier
                # (x - y + frame_number) is the animation frame index,
                # we use the position and frame number as offsets to produce the wave-like effect
                sussified_frame_data = np.copy(twerk_frames_data[(x - y + frame_number) % len(twerk_frames)])
                red, green, blue, alpha = sussified_frame_data.T
                # Replace all pixels with colour (214,224,240) with the input image colour at that location
                color_1 = (red == 214) & (green == 224) & (blue == 240)
                sussified_frame_data[..., :-1][color_1.T] = (r, g, b)  # thx stackoverflow
                # Repeat with colour (131,148,191) but use two thirds of the input image colour to get a darker colour
                color_2 = (red == 131) & (green == 148) & (blue == 191)
                sussified_frame_data[..., :-1][color_2.T] = (int(r*2/3), int(g*2/3), int(b*2/3))

                # Convert sussy frame data back to sussy frame
                sussified_frame = Image.fromarray(sussified_frame_data)

                # Slap said frame onto the background
                frame.paste(sussified_frame, (x * twerk_width, y * twerk_height))
        frames.append(frame.convert('RGBA', dither=None))
        logging.info(f'frame #{frame_number} processed')

    logging.info('image processing is finished')
    return frames


def export_gif(frames):
    """Exports gif to base directory
    :param frames: list of Image objects
    :return: None
    """
    try:
        frames[0].save('sussified.gif', save_all=True, append_images=frames[1:], loop=0, duration=50)
        logging.info('export success - sussified.gif')
    except:
        logging.error('can\'t export gif')
        raise RuntimeError

# lamkas a cute
# my cock and balls itch
