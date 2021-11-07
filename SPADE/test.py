"""
Copyright (C) 2019 NVIDIA Corporation.  All rights reserved.
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
"""

import torch
import importlib

from data.base_dataset import BaseDataset
from models.pix2pix_model import Pix2PixModel
from options.test_options import TestOptions


def run(verbose=False):
    opt = TestOptions().parse(verbose = verbose)

    dataset_name = "coco"
    dataset_filename = "data." + dataset_name + "_dataset"

    datasetlib = importlib.import_module(dataset_filename)

    dataset = None
    target_dataset_name = dataset_name.replace('_', '') + 'dataset'

    for name, cls in datasetlib.__dict__.items():
        if name.lower() == target_dataset_name.lower() \
                and issubclass(cls, BaseDataset):
            dataset = cls

    instance = dataset()
    instance.initialize(opt)
    if verbose:
        print("dataset [%s] of size %d was created" %
              (type(instance).__name__, len(instance)))

    dataloader = torch.utils.data.DataLoader(
        instance,
        batch_size=opt.batchSize,
        shuffle=not opt.serial_batches,
        num_workers=int(opt.nThreads),
        drop_last=opt.isTrain
    )

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
