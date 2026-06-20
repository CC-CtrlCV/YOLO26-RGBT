# YOLO-RGBT: RGB + 红外双模态目标检测框架

本项目基于 Ultralytics YOLO 扩展了 RGB + 红外双模态目标检测能力，支持在训练、验证和推理阶段自动读取可见光图像与对应红外图像，并合成为 4 通道 RGBT 输入。

项目适合以下场景：

- 夜间行人检测
- 红外/可见光双模态目标检测
- KAIST、LLVIP、FLIR、M3FD 等 RGB-IR 数据集实验
- 想把 RGBT 多模态能力迁移到自己 YOLO 项目的研究者和工程用户

## 主要特性

- 支持 RGB + 红外图像自动配对加载
- 支持 4 通道 RGBT 输入：`BGR + T`
- 支持训练、验证、推理、导出完整流程
- 支持 YOLOv5、YOLOv8、YOLO11、YOLO26
- 提供 early-fusion 和 mid-fusion 两种融合结构
- 提供数据集配对检查脚本
- 提供中文使用说明和代码迁移教程
- 不需要提前生成 4 通道图像文件

## 支持的模型配置

当前提供以下 RGBT 模型 yaml：

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

两种融合方式：

- `earlyfusion`：RGB 和红外在输入阶段直接融合，结构简单，适合作为 baseline。
- `midfusion`：RGB 和红外分别经过分支提取特征，在多尺度特征层融合，更适合双模态检测实验。

## 数据集目录结构

推荐数据集结构如下：

```text
YourDataset/
  visible/
    train/
      img001.jpg
      img001.txt
      img002.jpg
      img002.txt
    val/
      img101.jpg
      img101.txt
    test/
      img201.jpg

  infrared/
    train/
      img001.jpg
      img002.jpg
    val/
      img101.jpg
    test/
      img201.jpg
```

要求：

- `visible` 和 `infrared` 目录同级。
- 可见光和红外图像文件名一一对应。
- 标签使用标准 YOLO txt 格式。
- 标签推荐放在 `visible` 对应目录下。

例如：

```text
visible/train/img001.jpg
infrared/train/img001.jpg
visible/train/img001.txt
```

## 数据集 YAML

可以参考：

```text
ultralytics/cfg/datasets/rgbt-template.yaml
ultralytics/cfg/datasets/KAIST8-rgbt.yaml
```

示例：

```yaml
path: D:/datasets/YourDataset
train: visible/train
val: visible/val
test: visible/test

channels: 4
rgbt: true
rgbt_pair: [visible, infrared]

names:
  0: person
  1: car
  2: bicycle
```

说明：

- `channels: 4` 表示模型输入为 4 通道。
- `rgbt: true` 表示启用 RGBT 配对加载。
- `rgbt_pair: [visible, infrared]` 表示把可见光路径中的 `visible` 替换成 `infrared` 来寻找红外图像。

如果你的目录名是 `rgb` 和 `ir`，则写成：

```yaml
train: rgb/train
val: rgb/val
rgbt_pair: [rgb, ir]
```

## 安装环境

建议先安装依赖。新手可以先使用 `requirements.txt`：

```bash
pip install -r requirements.txt
```

如果希望以本地源码开发方式安装，再执行：

```bash
pip install -e .
```

如果使用 GPU 训练，请根据自己的 CUDA 版本安装对应的 PyTorch，不要盲目固定某一个 torch 版本。

如需导出 ONNX 等格式，请根据 Ultralytics 原项目要求安装对应依赖。

## 检查图像配对

训练前建议先检查 RGB 和红外图像是否一一对应：

```bash
python check_rgbt_pairs.py D:/datasets/YourDataset/visible/train
python check_rgbt_pairs.py D:/datasets/YourDataset/visible/val
```

如果输出：

```text
All infrared pairs were found.
```

说明配对正常。

自定义目录名示例：

```bash
python check_rgbt_pairs.py D:/datasets/YourDataset/rgb/train --rgb-token rgb --ir-token ir
```

## 训练

使用 YOLO26-RGBT midfusion 训练：

```bash
python train_rgbt.py \
  --model ultralytics/cfg/models/26-RGBT/yolo26-rgbt-midfusion.yaml \
  --data ultralytics/cfg/datasets/KAIST8-rgbt.yaml \
  --imgsz 640 \
  --epochs 100 \
  --batch 16 \
  --device 0 \
  --name yolo26-rgbt-midfusion
```

也可以使用 YOLO CLI：

```bash
yolo detect train model=ultralytics/cfg/models/26-RGBT/yolo26-rgbt-midfusion.yaml data=ultralytics/cfg/datasets/KAIST8-rgbt.yaml imgsz=640 epochs=100 batch=16
```

切换到 YOLOv8：

```bash
python train_rgbt.py \
  --model ultralytics/cfg/models/v8-RGBT/yolov8-rgbt-midfusion.yaml \
  --data ultralytics/cfg/datasets/KAIST8-rgbt.yaml \
  --name yolov8-rgbt-midfusion
```

## 验证

```bash
python val_rgbt.py \
  --model runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt \
  --data ultralytics/cfg/datasets/KAIST8-rgbt.yaml \
  --imgsz 640 \
  --batch 16
```

或：

```bash
yolo detect val model=runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt data=ultralytics/cfg/datasets/KAIST8-rgbt.yaml imgsz=640 batch=16
```

## 推理

推理时 `source` 指向可见光图像或可见光目录：

```bash
python predict_rgbt.py \
  --model runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt \
  --source D:/datasets/YourDataset/visible/test \
  --imgsz 640
```

YOLO CLI：

```bash
yolo detect predict model=runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt source=D:/datasets/YourDataset/visible/test rgbt=True rgbt_pair="[visible,infrared]" imgsz=640 save=True
```

如果目录名是 `rgb/ir`：

```bash
python predict_rgbt.py \
  --model runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt \
  --source D:/datasets/YourDataset/rgb/test \
  --rgb-token rgb \
  --ir-token ir
```

## 导出

导出 ONNX：

```bash
python export_rgbt.py \
  --model runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt \
  --format onnx \
  --imgsz 640
```

注意：导出的模型仍然是 4 通道输入。部署时需要在前处理阶段自行拼接：

```text
BGR + T
```

## 根目录入口文件

为了方便新手使用，项目根目录提供了以下文件：

```text
RGBT快速开始.md
使用说明书.md
多模态代码迁移教程.md
train_rgbt.py
val_rgbt.py
predict_rgbt.py
export_rgbt.py
check_rgbt_pairs.py
```

推荐阅读顺序：

1. `RGBT快速开始.md`
2. `使用说明书.md`
3. `多模态代码迁移教程.md`

## 如何迁移到自己的项目

如果你想把本项目中的 RGBT 能力迁移到自己的 YOLO/Ultralytics 项目，请阅读：

```text
多模态代码迁移教程.md
```

该文档说明了需要迁移哪些文件、哪些函数、哪些 yaml，以及如何做最小验证。

## 常见问题

### 1. 为什么不提前生成 4 通道图像？

本项目在 dataloader 中动态读取并拼接 RGB 和红外图像，避免重复保存数据，也更容易兼容现有 RGB-IR 数据集。

### 2. 红外图必须是灰度图吗？

推荐使用单通道灰度红外图。如果你的红外图是伪彩色图，建议先转成灰度图。

### 3. 可见光和红外尺寸不同怎么办？

代码会把红外图 resize 到可见光图尺寸，但更推荐提前做好图像配准和尺寸统一。

### 4. 标签放在哪里？

推荐放在 `visible` 对应目录下，例如：

```text
visible/train/img001.txt
```

### 5. 报错找不到红外图怎么办？

先运行：

```bash
python check_rgbt_pairs.py D:/datasets/YourDataset/visible/train
```

检查目录名、文件名和 `rgbt_pair` 是否一致。

## 致谢

本项目基于 Ultralytics YOLO 框架开发，感谢 Ultralytics 社区和 RGB-IR 多模态目标检测相关开源工作。

## License

请遵循原 Ultralytics 项目的许可证要求。
