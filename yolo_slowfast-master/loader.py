from slowfast.models.build import build_model
from slowfast.config.defaults import assert_and_infer_cfg
from slowfast.utils.parser import load_config
import slowfast.utils.checkpoint as cu
import torch


def slowfast_detection(args):
    for path_to_config in args.cfg_files:
        cfg = load_config(args, path_to_config)
        cfg = assert_and_infer_cfg(cfg)

    gpu_id = 0

    if cfg.NUM_GPUS:
        gpu_id = torch.cuda.current_device() if gpu_id is None else gpu_id

    # Build the video model and print model statistics.
    model = build_model(cfg, gpu_id=gpu_id).eval()
    cu.load_test_checkpoint(cfg, model)

    return model
