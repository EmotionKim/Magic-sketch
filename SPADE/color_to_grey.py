from PIL import Image


def convert_rgb_image_to_greyscale(input_file, output_file):
    label_to_grey = {}
    label_to_rgb = {}
    rgb_to_label = {}

    with open("labels.txt", "r") as labels:
        for line in labels.readlines():
            line = line.strip()
            split_line = line.split(' ')
            if len(split_line) < 3:
                continue
            grey, label, rgb_list = split_line
            rgb = tuple(map(int, rgb_list.split(',')))

            label_to_rgb[label] = rgb
            rgb_to_label[rgb] = label
