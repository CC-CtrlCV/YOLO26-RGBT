# RGBT 快速开始

本项目已经加入 RGB + 红外双模态目标检测支持。新手建议先看这几个文件：

```text
使用说明书.md              # 从数据集准备到训练、验证、推理、导出的完整说明
多模态代码迁移教程.md      # 如何把 RGBT 代码迁移到自己的 YOLO/Ultralytics 项目
train_rgbt.py              # 训练入口
val_rgbt.py                # 验证入口
predict_rgbt.py            # 推理入口
export_rgbt.py             # 模型导出入口
check_rgbt_pairs.py        # 检查 visible/infrared 图像是否一一配对
```

## 1. 数据集结构

推荐结构：

```text
YourDataset/
  visible/
    train/
      img001.jpg
      img001.txt
    val/
      img101.jpg
      img101.txt
    test/
      img201.jpg

  infrared/
    train/
      img001.jpg
    val/
      img101.jpg
    test/
      img201.jpg
```

可见光和红外图像文件名必须对应。

## 2. 数据集 yaml

参考：

```text
ultralytics/cfg/datasets/rgbt-template.yaml
ultralytics/cfg/datasets/KAIST8-rgbt.yaml
```

核心字段：

```yaml
channels: 4
rgbt: true
rgbt_pair: [visible, infrared]
```

## 3. 检查配对

```bash
python check_rgbt_pairs.py D:/datasets/YourDataset/visible/train
python check_rgbt_pairs.py D:/datasets/YourDataset/visible/val
```

## 4. 训练

```bash
python train_rgbt.py --model ultralytics/cfg/models/26-RGBT/yolo26-rgbt-midfusion.yaml --data ultralytics/cfg/datasets/KAIST8-rgbt.yaml --imgsz 640 --epochs 100 --batch 16 --device 0
```

## 5. 验证

```bash
python val_rgbt.py --model runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt --data ultralytics/cfg/datasets/KAIST8-rgbt.yaml --imgsz 640 --batch 16
```

## 6. 推理

```bash
python predict_rgbt.py --model runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt --source D:/datasets/YourDataset/visible/test --imgsz 640
```

## 7. 导出

```bash
python export_rgbt.py --model runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt --format onnx --imgsz 640
```

更多细节请看：

```text
使用说明书.md
多模态代码迁移教程.md
```
