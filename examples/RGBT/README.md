# YOLO-RGBT

This example trains YOLO with paired RGB/visible and infrared images. The RGBT loader is shared by YOLOv5, YOLOv8, YOLO11, and YOLO26 model YAMLs.

## Dataset Layout

The visible path is listed in the dataset YAML. The infrared path is found by
replacing the first token in `rgbt_pair` with the second token.

```text
KAIST8/
  visible/
    train/
      img001.jpg
      img001.txt
    test/
      img101.jpg
      img101.txt
  infrared/
    train/
      img001.jpg
    test/
      img101.jpg
```

The paired images must have matching relative paths and filenames.

## Dataset YAML

```yaml
path: E:/BaiduNetdiskDownload/RGBTO/KAIST8
train: visible/train
val: visible/test

channels: 4
rgbt: true
rgbt_pair: [visible, infrared]

names:
  0: person
```

## Train

```bash
yolo detect train model=ultralytics/cfg/models/26-RGBT/yolo26-rgbt-midfusion.yaml data=ultralytics/cfg/datasets/KAIST8-rgbt.yaml imgsz=640 epochs=100 batch=16
```

or:

```bash
python examples/RGBT/train_rgbt.py
```

With another model family:

```bash
python examples/RGBT/train_rgbt.py --model ultralytics/cfg/models/v8-RGBT/yolov8-rgbt-midfusion.yaml --name yolov8-rgbt-midfusion
```

Available model configs:

```text
ultralytics/cfg/models/v5-RGBT/yolov5-rgbt-earlyfusion.yaml
ultralytics/cfg/models/v5-RGBT/yolov5-rgbt-midfusion.yaml
ultralytics/cfg/models/v8-RGBT/yolov8-rgbt-earlyfusion.yaml
ultralytics/cfg/models/v8-RGBT/yolov8-rgbt-midfusion.yaml
ultralytics/cfg/models/11-RGBT/yolo11-rgbt-earlyfusion.yaml
ultralytics/cfg/models/11-RGBT/yolo11-rgbt-midfusion.yaml
ultralytics/cfg/models/26-RGBT/yolo26-rgbt-earlyfusion.yaml
ultralytics/cfg/models/26-RGBT/yolo26-rgbt-midfusion.yaml
```

## Predict

```bash
yolo detect predict model=runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt source=E:/BaiduNetdiskDownload/RGBTO/KAIST8/visible/test rgbt=True rgbt_pair="[visible,infrared]"
```

or:

```bash
python examples/RGBT/predict_rgbt.py
```

## Validate

Validation uses the RGBT options from the dataset YAML:

```bash
yolo detect val model=runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt data=ultralytics/cfg/datasets/KAIST8-rgbt.yaml imgsz=640 batch=16
```

or:

```bash
python examples/RGBT/val_rgbt.py --model runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt --data ultralytics/cfg/datasets/KAIST8-rgbt.yaml
```

## Export

Export keeps the 4-channel model input. Deployment preprocessing must provide tensors in `BGR + T` channel order.

```bash
yolo export model=runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt format=onnx imgsz=640
```

or:

```bash
python examples/RGBT/export_rgbt.py --model runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt --format onnx --imgsz 640
```

## Check Pairs

Before training, verify that every visible image has a paired infrared image:

```bash
python examples/RGBT/check_rgbt_pairs.py E:/BaiduNetdiskDownload/RGBTO/KAIST8/visible/train
python examples/RGBT/check_rgbt_pairs.py E:/BaiduNetdiskDownload/RGBTO/KAIST8/visible/test
```

For custom directory names:

```bash
python examples/RGBT/check_rgbt_pairs.py /data/LLVIP/rgb/train --rgb-token rgb --ir-token ir
```
