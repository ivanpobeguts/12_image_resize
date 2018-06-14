from PIL import Image
import os
import argparse


def calculate_new_image_size(original_size,
                             scale=None,
                             width=None,
                             height=None):

    orig_width, orig_height = original_size
    if width and height:
        return width, height
    elif scale:
        return (round(orig_width * scale),
                round(orig_height * scale))
    elif width:
        return width, round((width * orig_height) / orig_width)
    elif height:
        return round((height * orig_width) / orig_height), height
    else:
        return original_size


def is_ratio_changed(img_size, new_img_size):
    return (
        round(img_size[0] / new_img_size[0]) !=
        round(img_size[1] / new_img_size[1])
    )


def resize_image(img, size):
    resized_image = img.resize(size)
    return resized_image


def load_image(filepath):
    try:
        source_image = Image.open(filepath)
        return source_image
    except OSError:
        return None


def save_image_to_file(output_image, output_image_filepath):
    try:
        output_image.save(output_image_filepath)
        return True
    except PermissionError:
        return False


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filepath',
        help='path to source image file',
        type=str,
    )
    parser.add_argument(
        '--width',
        help='width of output image',
        default=0,
        type=int,
    )
    parser.add_argument(
        '--height',
        help='height of output image',
        default=0,
        type=int,
    )
    parser.add_argument(
        '--scale',
        help='scaling coefficient of output image',
        default=0.0,
        type=float,
    )
    parser.add_argument(
        '--output',
        help='path to output image file',
        default='',
        type=str,
    )
    args = check_args(parser)
    return args


def check_args(parser):
    args = parser.parse_args()
    if not os.path.isfile(args.filepath):
        parser.error(
            "Source image doesn't exist"
        )
    if not any((args.width, args.height, args.scale)):
        parser.error(
            'Parameters expected',
        )
    if any(arg < 0 for arg in (args.width, args.height, args.scale)):
        parser.error(
            "Parameters can't be less than 0",
        )
    if args.scale and (args.width or args.height):
        parser.error(
            "You can't use both scale and size (width/height)",
        )
    if args.output and not os.path.isdir(args.output):
        parser.error(
            'Output path is not a directory or does not exist',
        )
    return args


def generate_output_path(input_image_path,
                         output_image_size,
                         output_image_path=None):

    output_image_width, output_image_height = output_image_size
    filename, extension = os.path.splitext(input_image_path)

    output_path = '{}_{}x{}{}'.format(
        os.path.join(output_image_path, filename),
        output_image_width,
        output_image_height, extension)

    if output_image_path:
        return os.path.join(output_path)
    else:
        return output_path


if __name__ == '__main__':
    args = get_args()
    image = load_image(args.filepath)
    new_size = calculate_new_image_size(
        image.size, args.scale, args.width, args.height)
    output_image = resize_image(image, new_size)
    if is_ratio_changed(image.size, new_size):
        print('Warning: the image ratio was changed!')
    output_path = generate_output_path(
        args.filepath, output_image.size, args.output)
    save_image_to_file(output_image, output_path)
    print('Image successfully resized:', output_path)
