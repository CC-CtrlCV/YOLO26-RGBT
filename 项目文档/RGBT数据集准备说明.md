# RGBT 数据集准备说明

本文档说明 RGB + 红外多模态目标检测数据集应该如何准备。

如果你是刚下载本项目的新手，建议先按本文档整理数据集，再运行训练命令。

## 1. 本项目需要什么数据

本项目用于 RGB + 红外目标检测，每个样本需要包含：

```text
1. 一张 RGB 可见光图像
2. 一张与 RGB 图像对应的红外图像
3. 一个 YOLO 格式目标检测标签文件
```

例如：

```text
RGB 图像:   visible/train/000001.jpg
红外图像:  infrared/train/000001.jpg
标签文件:  visible/train/000001.txt
```

其中 RGB 图像和红外图像的文件名必须一一对应。

## 2. 推荐目录结构

推荐把数据集整理成下面的结构：

```text
YourRGBTDataset/
├── visible/
│   ├── train/
│   │   ├── 000001.jpg
│   │   ├── 000001.txt
│   │   ├── 000002.jpg
│   │   ├── 000002.txt
│   │   └── ...
│   └── val/
│       ├── 000101.jpg
│       ├── 000101.txt
│       └── ...
└── infrared/
    ├── train/
    │   ├── 000001.jpg
    │   ├── 000002.jpg
    │   └── ...
    └── val/
        ├── 000101.jpg
        └── ...
```

说明：

```text
1. visible 目录放 RGB 可见光图像。
2. infrared 目录放红外图像。
3. 标签 txt 推荐放在 visible 对应目录下，并与图片同名。
4. infrared 目录下可以没有 txt，训练主要使用 visible 目录下的标签。
```

## 3. . 数据集 YAML 怎么写

如果你的数据集路径是：

```text
D:/XM/SJJ/KAIST8
```

可以新建：

```text
ultralytics/cfg/datasets/my-rgbt.yaml
```

内容写成：

```yaml
path: D:/XM/SJJ/KAIST8
train: visible/train
val: visible/test
test:

channels: 4
rgbt: true
rgbt_pair: [visible, infrared]

names:
  0: person
```

字段解释：

```text
path: 数据集根目录
train: 训练集 RGB 图像目录
val: 验证集 RGB 图像目录
channels: 4 表示 RGB 三通道 + 红外一通道
rgbt: true 表示启用 RGB + 红外配对读取
rgbt_pair: [visible, infrared] 表示把 visible 路径替换成 infrared 路径
names: 类别名称
```

## 4. 为什么 visible 和 infrared 要同名

本项目会先读取 `visible` 中的 RGB 图像。

例如：

```text
D:/XM/SJJ/KAIST8/visible/train/set07_V000_I00319.jpg
```

然后根据：

```yaml
rgbt_pair: [visible, infrared]
```

自动找到：

```text
D:/XM/SJJ/KAIST8/infrared/train/set07_V000_I00319.jpg
```

所以两个模态的文件名必须一致。

如果文件名不一致，程序会找不到对应红外图像。

## 5. 如果目录名不是 visible 和 infrared

如果你的数据集目录叫：

```text
rgb/
ir/
```

那么 YAML 应该写成：

```yaml
path: D:/datasets/YourDataset
train: rgb/train
val: rgb/val
test:

channels: 4
rgbt: true
rgbt_pair: [rgb, ir]

names:
  0: person
```

如果目录叫：

```text
color/
thermal/
```

则写成：

```yaml
rgbt_pair: [color, thermal]
```

## 6. 标签格式

标签使用 YOLO 检测格式：

```text
class_id x_center y_center width height
```

例如：

```text
0 0.5123 0.4375 0.1200 0.3500
```

含义：

```text
class_id: 类别编号，从 0 开始
x_center: 目标中心点 x 坐标，归一化到 0 到 1
y_center: 目标中心点 y 坐标，归一化到 0 到 1
width: 目标框宽度，归一化到 0 到 1
height: 目标框高度，归一化到 0 到 1
```

一个图像中有多个目标时，一行表示一个目标：

```text
0 0.5123 0.4375 0.1200 0.3500
0 0.2330 0.5200 0.0800 0.2200
```

## 7. 训练前检查 RGB 和红外是否配对

进入项目根目录：

```powershell
cd D:/XM/DMT/ultralytics-main
```

检查训练集：

```powershell
python check_rgbt_pairs.py D:/XM/SJJ/KAIST8/visible/train
```

检查验证集：

```powershell
python check_rgbt_pairs.py D:/XM/SJJ/KAIST8/visible/test
```

正常输出类似：

```text
Checked 3178 visible images.
All infrared pairs were found.
```

如果出现：

```text
Missing infrared pairs
```

说明有些 RGB 图像找不到对应红外图像，需要检查文件名或目录结构。

## 9. 先跑 1 个 epoch 测试

建议新手先用 small batch 和 1 个 epoch 测试流程。

推荐先使用 earlyfusion：

```powershell
python train_rgbt.py --model ultralytics/cfg/models/26-RGBT/yolo26-rgbt-earlyfusion.yaml --data ultralytics/cfg/datasets/my-rgbt.yaml --imgsz 640 --epochs 1 --batch 2 --device 0
```

如果能正常跑完，说明：

```text
1. 数据集 YAML 路径正确。
2. visible 和 infrared 可以正常配对。
3. 标签可以正常读取。
4. RGBT 模型可以正常构建。
5. 训练流程基本跑通。
```

## 10. 正式训练命令

如果 1 个 epoch 测试没问题，可以训练 midfusion：

```powershell
python train_rgbt.py --model ultralytics/cfg/models/26-RGBT/yolo26-rgbt-midfusion.yaml --data ultralytics/cfg/datasets/my-rgbt.yaml --imgsz 640 --epochs 100 --batch 8 --device 0 --name yolo26-rgbt-midfusion
```

如果显存充足，可以适当增大 batch。

如果显存不足，可以减小：

```text
--batch
--imgsz
```

## 11. 推理命令

训练完成后，推理时只需要传入 `visible` 目录：

```powershell
python predict_rgbt.py --model runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt --source D:/XM/SJJ/KAIST8/visible/test --imgsz 640
```

程序会自动寻找：

```text
D:/XM/SJJ/KAIST8/infrared/test
```

## 12. 常见问题

### 12.1 Dataset yaml does not exist

说明命令中的 `--data` 指向的 YAML 文件不存在。

例如：

```text
ultralytics/cfg/datasets/my-rgbt.yaml
```

需要确认这个文件是否已经创建。

### 12.2 找不到红外图像

常见原因：

```text
1. visible 和 infrared 文件名不一致。
2. rgbt_pair 写错。
3. 红外图像目录层级和 visible 不一致。
```

先运行：

```powershell
python check_rgbt_pairs.py D:/XM/SJJ/KAIST8/visible/train
```

### 12.3 标签读取不到

当前示例数据集推荐标签放在：

```text
visible/train/xxx.txt
visible/test/xxx.txt
```

并且要和图片同名：

```text
visible/train/set07_V000_I00379.jpg
visible/train/set07_V000_I00379.txt
```

### 12.4 输入通道不匹配

检查数据集 YAML 是否写了：

```yaml
channels: 4
rgbt: true
```

检查模型是否使用 RGBT 模型，例如：

```text
ultralytics/cfg/models/26-RGBT/yolo26-rgbt-midfusion.yaml
```

```

```
