import sussify
from PIL import Image


if __name__ == '__main__':
    frames = sussify.get_frames(
        input_file='input.png',
        output_width=30,
        resize_filter=Image.NEAREST
    )
    sussify.export_gif(frames)
