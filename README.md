# YOLO26-RGBT 多模态目标检测项目

</div>

## 项目定位

本项目面向 RGB 可见光图像和红外图像的多模态目标检测任务，适合 KAIST、LLVIP、FLIR 等 RGBT 数据集实验，也适合夜间行人检测、安防监控、自动驾驶感知、无人机巡检。

原版 YOLO 通常读取 3 通道 RGB 图像，本项目在 Ultralytics YOLO26 基础上增加了 RGB + infrared 配对读取能力，将可见光图像和红外图像拼接为 4 通道输入，并提供多种 RGBT 模型结构。

## 快速入口


| 文档                                                 | 作用                                          |
| ---------------------------------------------------- | --------------------------------------------- |
| [项目说明文档](项目文档/项目说明文档.md)             | 介绍项目做了什么、用了哪些技术和算法          |
| [操作说明文档](项目文档/操作说明文档.md)             | 从环境配置到训练、验证、推理、导出的完整命令  |
| [项目结构与文件说明](项目文档/项目结构与文件说明.md) | 说明每个主要文件夹和关键代码文件的作用        |
| [前端与结果查看说明](项目文档/前端与结果查看说明.md) | 说明预测结果、训练曲线、可视化页面/输出怎么看 |
| [RGBT网络结构说明](项目文档/RGBT网络结构说明.md)     | 说明 yolo26、earlyfusion、midfusion 的区别    |
| [多模态代码迁移教程](项目文档/多模态代码迁移教程.md) | 说明如何把 RGBT 代码迁移到自己的 YOLO 项目    |
|                                                      |                                               |

## 新手最短流程

### 1. 安装依赖

```bash
pip install -r requirements.txt
pip install -e .
```

如果使用 GPU 训练，请先根据自己的 CUDA 版本安装 PyTorch。

### 2. 准备数据集

推荐数据结构：

```text
YourDataset/
├── visible/
│   ├── train/
│   └── val/
├── infrared/
│   ├── train/
│   └── val/
└── labels/
    ├── train/
    └── val/
```

可见光和红外图像文件名需要一一对应，例如：

```text
visible/train/000001.jpg
infrared/train/000001.jpg
labels/train/000001.txt
```

### 3. 修改数据集 YAML

参考：

```text
ultralytics/cfg/datasets/rgbt-template.yaml
```

关键字段：

```yaml
channels: 4
rgbt: true
rgbt_pair: [visible, infrared]
```

### 4. 检查图像配对

```bash
python check_rgbt_pairs.py D:/datasets/YourDataset/visible/train
python check_rgbt_pairs.py D:/datasets/YourDataset/visible/val
```

### 5. 训练

Windows PowerShell 写法：

```powershell
python train_rgbt.py `
  --model ultralytics/cfg/models/26-RGBT/yolo26-rgbt-midfusion.yaml `
  --data ultralytics/cfg/datasets/rgbt-template.yaml `
  --imgsz 640 `
  --epochs 100 `
  --batch 16 `
  --device 0 `
  --name yolo26-rgbt-midfusion
```

Windows CMD 或单行写法：

```cmd
python train_rgbt.py --model ultralytics/cfg/models/26-RGBT/yolo26-rgbt-midfusion.yaml --data ultralytics/cfg/datasets/rgbt-template.yaml --imgsz 640 --epochs 100 --batch 16 --device 0 --name yolo26-rgbt-midfusion
```

Linux/macOS 才使用反斜杠换行：

```bash
python train_rgbt.py \
  --model ultralytics/cfg/models/26-RGBT/yolo26-rgbt-midfusion.yaml \
  --data ultralytics/cfg/datasets/rgbt-template.yaml \
  --imgsz 640 \
  --epochs 100 \
  --batch 16 \
  --device 0 \
  --name yolo26-rgbt-midfusion
```

### 6. 验证

```bash
python val_rgbt.py --model runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt --data ultralytics/cfg/datasets/rgbt-template.yaml --imgsz 640 --batch 16
```

### 7. 推理

```bash
python predict_rgbt.py --model runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt --source D:/datasets/YourDataset/visible/val --imgsz 640
```

推理时只需要传入 `visible` 目录，代码会根据 `rgbt_pair` 自动寻找对应的 `infrared` 图像。

### 8. 导出

```bash
python export_rgbt.py --model runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt --format onnx --imgsz 640
```

## 支持的 RGBT 模型配置

```text
ultralytics/cfg/models/v5-RGBT/
ultralytics/cfg/models/v8-RGBT/
ultralytics/cfg/models/11-RGBT/
ultralytics/cfg/models/26-RGBT/
```

每个版本提供：

```text
earlyfusion: RGB 和红外在输入阶段拼接为 4 通道
midfusion: RGB 和红外先走不同分支，再在中间层融合
```

如果只是想快速跑通，建议先使用 `earlyfusion`；如果要做正式多模态实验，建议使用 `midfusion`。
