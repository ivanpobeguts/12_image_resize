from PIL import Image
import os
import argparse


def calculate_new_image_size(original_size, scale=None, width=None, height=None):
    orig_width, orig_height = original_size
    if width and height:
        return width, height
    elif scale:
        return round(orig_width * scale), round(orig_height * scale)
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


def resize_image(image, size):
    out = image.resize(size)
    return out


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


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filepath',
        help='path to source image file',
        type=str,
    )
    parser.add_argument(
        '--w',
        help='width of output image',
        default=0,
        type=int,
    )
    parser.add_argument(
        '--h',
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
        '--out',
        help='path to output image file',
        default='',
        type=str,
    )
    check_args(parser)
    return parser


def check_args(parser):
    args = parser.parse_args()
    if not any((args.w, args.h, args.scale)):
        parser.error(
            'Parameters expected',
        )
    if args.scale and (args.w or args.h):
        parser.error(
            "You cant't use both scale and size (width/height)",
        )
    if args.out and not os.path.isdir(args.out):
        parser.error(
            'Output path is not a directory or does not exist',
        )


def generate_output_path(input_image_path, output_image, output_image_path=None):
    output_image_width, output_image_height = output_image.size
    filename, extension = os.path.splitext(input_image_path)
    if output_image_path:
        return '{}_{}x{}{}'.format(
            os.path.join(output_image_path, filename), output_image_width, output_image_height, extension)
    else:
        return '{}_{}x{}{}'.format(
            filename, output_image_width, output_image_height, extension)


if __name__ == '__main__':
    args = get_parser().parse_args()
    image = load_image(args.filepath)
    new_size = calculate_new_image_size(image.size, args.scale, args.w, args.h)
    output_image = resize_image(image, new_size)
    output_path = generate_output_path(args.filepath, output_image, args.out)
    save_image_to_file(output_image, output_path)
    print('Image successfully resized:', output_path)
