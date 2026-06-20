# RGBT 网络结构说明：yolo26、earlyfusion、midfusion 怎么选

本文档用于补充说明本项目中 RGBT 多模态模型 YAML 的设计思路，重点解释下面三个文件的区别：

```text
ultralytics/cfg/models/26/yolo26.yaml
ultralytics/cfg/models/26-RGBT/yolo26-rgbt-earlyfusion.yaml
ultralytics/cfg/models/26-RGBT/yolo26-rgbt-midfusion.yaml
```

如果你刚开始做 RGB + 红外目标检测，建议先看完本文档，再决定训练时使用哪个模型配置。

## 1. 普通 YOLO26 和 RGBT YOLO26 的区别

原版 YOLO26 是为普通 RGB 图像设计的，默认输入是一张 3 通道图片：

```text
RGB image -> 3 channels -> YOLO26 backbone -> YOLO26 head -> Detect
```

而 RGBT 多模态检测通常同时使用一张可见光图像和一张红外图像：

```text
RGB image       -> 3 channels
Infrared image  -> 1 channel
```

在本项目中，数据加载器会把它们拼接成 4 通道输入：

```text
RGB + IR -> 4 channels
```

所以训练 RGBT 数据集时，模型 YAML 和数据集 YAML 都需要知道当前输入是 4 通道。

数据集 YAML 中需要写：

```yaml
channels: 4
rgbt: true
rgbt_pair: [visible, infrared]
```

模型 YAML 中也建议写：

```yaml
channels: 4
```

## 2. 三种模型配置的区别

### 2.1 原版 yolo26.yaml

文件位置：

```text
ultralytics/cfg/models/26/yolo26.yaml
```

这是 Ultralytics 原版 YOLO26 检测模型配置，主要面向普通 RGB 图像。

它的结构可以简单理解为：

```text
RGB image -> Conv -> C3k2 -> SPPF -> C2PSA -> Detect
```

原版配置中通常没有：

```yaml
channels: 4
```

也没有：

```yaml
ChannelSlice
```

所以它本身不包含 RGB/IR 分离、配对、融合等多模态设计。

如果你直接用原版 `yolo26.yaml` 训练 RGBT 数据集，容易遇到两类问题：

```text
1. 数据是 4 通道，但模型按 3 通道构建，输入通道不匹配。
2. 即使改成 4 通道，也只是普通卷积接收 4 通道，没有专门的多模态融合结构。
```

因此，原版 `yolo26.yaml` 不建议直接作为 RGBT 项目的默认模型。

### 2.2 yolo26-rgbt-earlyfusion.yaml

文件位置：

```text
ultralytics/cfg/models/26-RGBT/yolo26-rgbt-earlyfusion.yaml
```

这是早期融合版本。

它在 YAML 顶部写了：

```yaml
channels: 4
```

并在网络开头使用：

```yaml
- [-1, 1, ChannelSlice, [0, 4]]
```

它的整体思路是：

```text
RGB image      \
                -> 拼接为 4 通道 -> YOLO26 backbone -> Detect
Infrared image /
```

也可以理解为：

```text
RGB + IR -> 4 channels -> 普通 YOLO26 主干网络
```

优点：

```text
1. 结构简单。
2. 更容易跑通。
3. 训练流程最接近原版 YOLO。
4. 适合作为 RGBT 项目的入门 baseline。
```

缺点：

```text
1. RGB 和红外从输入层就混在一起。
2. 没有显式区分 RGB 特征和红外特征。
3. 多模态融合能力相对简单。
```

如果你是第一次跑本项目，推荐先用它确认数据集、标签和训练流程没有问题。

### 2.3 yolo26-rgbt-midfusion.yaml

文件位置：

```text
ultralytics/cfg/models/26-RGBT/yolo26-rgbt-midfusion.yaml
```

这是中期融合版本，也是更符合多模态思路的版本。

它同样使用：

```yaml
channels: 4
```

但是它会先把 4 通道输入切成两个分支：

```yaml
- [0, 1, ChannelSlice, [0, 3]]
- [0, 1, ChannelSlice, [3, 4]]
```

含义是：

```text
ChannelSlice [0, 3] -> 取 RGB 三通道
ChannelSlice [3, 4] -> 取红外一通道
```

然后 RGB 和红外分别经过各自的浅层/中层特征提取，再进行融合：

```yaml
- [[6, 16], 1, Concat, [1]]
- [[8, 18], 1, Concat, [1]]
- [[10, 20], 1, Concat, [1]]
```

它的整体思路是：

```text
RGB image -> RGB branch \
                         -> feature concat -> YOLO head -> Detect
IR image  -> IR branch  /
```

优点：

```text
1. RGB 和红外有相对独立的特征提取分支。
2. 更符合多模态融合实验的常见设计。
3. 后续更容易替换为注意力融合、加权融合、Transformer 融合等模块。
```

缺点：

```text
1. 网络结构更复杂。
2. 参数量和显存占用通常更高。
3. 如果数据量很小，训练可能比 early fusion 更难调。
```

如果你想做论文实验、消融实验或者进一步改进融合模块，推荐使用 midfusion。

## 3. 如果我想用原版 yolo26.yaml 训练多模态数据，怎么改

可以改，但不建议直接修改原始文件。推荐复制一份，例如：

```text
ultralytics/cfg/models/26-RGBT/yolo26-rgbt-simple.yaml
```

然后在复制出来的文件顶部加入：

```yaml
channels: 4
```

例如原版开头可能是：

```yaml
nc: 80
end2end: True
reg_max: 1
```

可以改成：

```yaml
nc: 80
channels: 4
end2end: True
reg_max: 1
```

这样模型会按 4 通道输入构建第一层卷积。

这种结构可以理解为一个最简单的 RGBT early fusion：

```text
RGB + IR -> 4 通道 -> 原版 YOLO26 网络 -> Detect
```

但是需要注意：这不是严格意义上的双分支多模态融合模型，它只是让普通 YOLO26 能接收 4 通道输入。

## 4. 训练时模型 YAML 和数据集 YAML 要配套

如果使用 RGBT 模型，数据集 YAML 推荐这样写：

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

其中：

```text
channels: 4
```

表示模型输入为 4 通道。

```text
rgbt: true
```

表示启用 RGB + 红外配对读取。

```text
rgbt_pair: [visible, infrared]
```

表示读取 `visible` 图像时，自动找到对应的 `infrared` 图像。

例如：

```text
visible/train/000001.jpg
infrared/train/000001.jpg
```

训练命令示例：

```bash
python train_rgbt.py --model ultralytics/cfg/models/26-RGBT/yolo26-rgbt-earlyfusion.yaml --data ultralytics/cfg/datasets/KAIST8-rgbt.yaml
```

或者：

```bash
python train_rgbt.py --model ultralytics/cfg/models/26-RGBT/yolo26-rgbt-midfusion.yaml --data ultralytics/cfg/datasets/KAIST8-rgbt.yaml
```

## 5. 预训练权重需要注意什么

普通 YOLO26 预训练权重通常来自 RGB 数据集，第一层卷积是 3 通道输入。

而 RGBT 模型是 4 通道输入，所以第一层权重尺寸可能不匹配。

常见情况：

```text
原版权重第一层: [out_channels, 3, k, k]
RGBT 模型第一层: [out_channels, 4, k, k]
```

因此，如果你从 RGBT YAML 从头训练，最稳。

如果想加载普通 RGB 预训练权重，需要考虑：

```text
1. 跳过第一层不匹配权重。
2. 复制 RGB 权重并初始化红外通道。
3. 使用项目或框架自身的 partial load 逻辑。
```

对新手来说，建议先不要纠结预训练权重，先保证数据读取、训练、验证、推理流程可以跑通。

## 6. 推荐选择

如果你只是想快速跑通：

```text
yolo26-rgbt-earlyfusion.yaml
```

如果你想做正式的 RGB + 红外多模态实验：

```text
yolo26-rgbt-midfusion.yaml
```

如果你想保留原版 YOLO26 结构，只是让它接收 4 通道输入：

```text
复制 yolo26.yaml，添加 channels: 4
```

推荐顺序：

```text
1. 先用 earlyfusion 跑通数据和训练流程。
2. 再用 midfusion 做多模态融合实验。
3. 最后把 simple 4 通道 YOLO26 当作消融实验 baseline。
```

## 7. 可以写进论文或博客的表述

如果需要在博客、论文实验说明或项目 README 中描述，可以写成：

```text
本项目提供三种 RGBT 检测模型配置。第一种是基于原版 YOLO26 的简单 4 通道输入版本，可作为 early fusion baseline；第二种是 yolo26-rgbt-earlyfusion，将 RGB 与红外图像在输入层拼接后送入 YOLO26 主干网络；第三种是 yolo26-rgbt-midfusion，分别对 RGB 与红外分支进行特征提取，并在中间层进行特征拼接融合。相比普通 RGB YOLO26，RGBT 模型能够同时利用可见光纹理信息和红外热辐射信息，更适合夜间、弱光和复杂天气条件下的目标检测任务。
```
