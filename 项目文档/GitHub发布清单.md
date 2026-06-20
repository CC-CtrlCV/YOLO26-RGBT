# GitHub 发布清单

本文档用于发布 GitHub 前检查项目是否适合作为开源项目公开。

## 1. 发布前必须检查

发布前建议检查：

```text
1. README.md 是否已经是 RGBT 项目说明。
2. 数据集 YAML 中是否没有个人本地绝对路径。
3. 权重文件 .pt 是否不会提交。
4. runs/ 训练结果是否不会提交。
5. ultralytics/settings.json 是否不会提交。
6. __pycache__/ 是否不会提交。
7. 文档中的命令是否同时给出 Windows 和 Linux 写法。
8. requirements.txt 是否存在。
9. 训练、验证、推理脚本是否在根目录。
10. 数据集模板是否可直接复制修改。
```

## 2. 建议不要提交的文件

以下文件或目录通常不建议提交到 GitHub：

```text
runs/
*.pt
*.onnx
*.engine
ultralytics/settings.json
__pycache__/
.vscode/
本地数据集
```

其中 `runs/` 和 `*.pt` 通常已经被 `.gitignore` 忽略。

## 2.1 当前目录中建议清理或忽略的内容

当前项目目录中可能存在以下本地运行产物：

| 文件或目录 | 建议 | 原因 |
| --- | --- | --- |
| `runs/` | 不提交 | 训练、验证、推理结果通常较大，属于本地实验产物 |
| `yolo26n.pt` | 不提交 | 预训练权重文件较大，且 `.gitignore` 已忽略 `*.pt` |
| `ultralytics/settings.json` | 不提交 | Ultralytics 本机运行配置，不适合作为开源配置 |
| `.vscode/` | 视情况不提交 | 编辑器个人配置，不一定适合所有用户 |
| `__pycache__/` | 不提交 | Python 缓存文件 |
| `yolo_train.py` | 可删除或移到 examples | 普通 YOLO 训练脚本，容易和 RGBT 入口混淆 |
| `yolo_val.py` | 可删除或移到 examples | 普通 YOLO 验证脚本，容易和 RGBT 入口混淆 |
| `yolo_predict.py` | 可删除或移到 examples | 普通 YOLO 推理脚本，容易和 RGBT 入口混淆 |

注意：如果要删除这些文件，请先确认路径，尤其是在 Windows 下路径大小写不敏感，避免误删 `ultralytics/` 源码目录。

更稳妥的做法是先依靠 `.gitignore` 忽略它们，再用 `git status` 确认不会被提交。

## 3. 建议保留的文件

以下文件建议保留：

```text
README.md
项目说明文档.md
操作说明文档.md
项目结构与文件说明.md
前端与结果查看说明.md
RGBT网络结构说明.md
多模态代码迁移教程.md
requirements.txt
train_rgbt.py
val_rgbt.py
predict_rgbt.py
export_rgbt.py
check_rgbt_pairs.py
ultralytics/cfg/datasets/rgbt-template.yaml
ultralytics/cfg/models/26-RGBT/
ultralytics/cfg/models/11-RGBT/
ultralytics/cfg/models/v8-RGBT/
ultralytics/cfg/models/v5-RGBT/
tests/test_rgbt.py
```

## 4. 初始化 Git 仓库

如果当前目录还不是 Git 仓库，可以执行：

```powershell
git init
git add .
git status
```

确认没有把权重、runs、数据集提交进去后再提交：

```powershell
git commit -m "Initial release for YOLO26-RGBT multimodal detection"
```

## 5. 关联 GitHub 仓库

在 GitHub 新建仓库后，执行：

```powershell
git remote add origin https://github.com/你的用户名/你的仓库名.git
git branch -M main
git push -u origin main
```

如果仓库已经存在 remote，先查看：

```powershell
git remote -v
```

## 6. 推荐仓库名称

可以考虑以下名称：

```text
YOLO26-RGBT
YOLO-RGBT-Ultralytics
Ultralytics-RGBT-Detection
YOLO-Multimodal-RGBT
```

## 7. 推荐项目简介

GitHub 仓库描述可以写：

```text
RGB + infrared multimodal object detection based on Ultralytics YOLO, supporting RGBT paired loading, 4-channel input, early fusion and mid fusion.
```

中文描述可以写：

```text
基于 Ultralytics YOLO 的 RGB + 红外多模态目标检测项目，支持 RGBT 配对读取、4 通道输入、early fusion 和 mid fusion。
```
