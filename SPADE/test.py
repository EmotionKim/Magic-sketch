"""
Copyright (C) 2019 NVIDIA Corporation.  All rights reserved.
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
"""

import importlib

from models.pix2pix_model import Pix2PixModel
from options.test_options import TestOptions


def run(verbose=False):
    opt = TestOptions().parse(verbose = verbose)

    dataset_name = "coco"
    dataset_filename = "data." + dataset_name + "_dataset"

    datasetlib = importlib.import_module(dataset_filename)

    dataset = None
    target_dataset_name = dataset_name.replace('_', '') + 'dataset'

    # TODO: dataset 이름 정렬

    model = Pix2PixModel(opt, verbose)
    model.eval()

    if verbose:
        print(dataloader)
    for i, data_i in enumerate(dataloader):
        if i * opt.batchSize >= opt.how_many:
            break
        model(data_i, mode='inference', verbose=verbose)


if __name__ == "__main__":
    run()
