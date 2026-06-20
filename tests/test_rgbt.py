from pathlib import Path
from types import SimpleNamespace

import cv2
import numpy as np

from ultralytics import YOLO
from ultralytics.data.build import load_inference_source
from ultralytics.data.dataset import YOLODataset


RGBT_MODELS = (
    "ultralytics/cfg/models/v5-RGBT/yolov5-rgbt-earlyfusion.yaml",
    "ultralytics/cfg/models/v5-RGBT/yolov5-rgbt-midfusion.yaml",
    "ultralytics/cfg/models/v8-RGBT/yolov8-rgbt-earlyfusion.yaml",
    "ultralytics/cfg/models/v8-RGBT/yolov8-rgbt-midfusion.yaml",
    "ultralytics/cfg/models/11-RGBT/yolo11-rgbt-earlyfusion.yaml",
    "ultralytics/cfg/models/11-RGBT/yolo11-rgbt-midfusion.yaml",
    "ultralytics/cfg/models/26-RGBT/yolo26-rgbt-earlyfusion.yaml",
    "ultralytics/cfg/models/26-RGBT/yolo26-rgbt-midfusion.yaml",
)


def _write_rgbt_pair(root: Path, split: str = "train"):
    visible = root / "visible" / split
    infrared = root / "infrared" / split
    visible.mkdir(parents=True, exist_ok=True)
    infrared.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(visible / "img001.jpg"), np.full((32, 32, 3), 80, np.uint8))
    cv2.imwrite(str(infrared / "img001.jpg"), np.full((32, 32), 180, np.uint8))
    (visible / "img001.txt").write_text("0 0.5 0.5 0.5 0.5\n", encoding="utf-8")
    return visible


def _hyp():
    return SimpleNamespace(
        deterministic=True,
        mosaic=0.0,
        copy_paste_mode="flip",
        copy_paste=0.0,
        degrees=0.0,
        translate=0.0,
        scale=0.0,
        shear=0.0,
        perspective=0.0,
        mixup=0.0,
        cutmix=0.0,
        augmentations=None,
        hsv_h=0.0,
        hsv_s=0.0,
        hsv_v=0.0,
        flipud=0.0,
        fliplr=0.0,
        mask_ratio=4,
        overlap_mask=True,
        bgr=0.0,
    )


def test_rgbt_inference_loader_pairs_visible_and_infrared(tmp_path):
    visible = _write_rgbt_pair(tmp_path, "test")
    dataset = load_inference_source(str(visible), channels=4, rgbt=True, rgbt_pair=["visible", "infrared"])
    _, images, _ = next(iter(dataset))
    assert images[0].shape == (32, 32, 4)
    assert images[0][0, 0].tolist() == [80, 80, 80, 180]


def test_rgbt_training_dataset_returns_four_channels(tmp_path):
    visible = _write_rgbt_pair(tmp_path, "train")
    dataset = YOLODataset(
        img_path=str(visible),
        imgsz=32,
        batch_size=1,
        augment=False,
        hyp=_hyp(),
        data={"channels": 4, "rgbt": True, "rgbt_pair": ["visible", "infrared"], "names": {0: "person"}},
        task="detect",
    )
    sample = dataset[0]
    assert tuple(sample["img"].shape) == (4, 32, 32)
    assert sample["img"][-1, 0, 0].item() == 180


def test_rgbt_model_yamls_build():
    for model in RGBT_MODELS:
        assert YOLO(model).model.yaml["channels"] == 4
