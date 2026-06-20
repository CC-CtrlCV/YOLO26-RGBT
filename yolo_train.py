import warnings

warnings.filterwarnings("ignore")
from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO(r"ultralytics/cfg/models/HD/WTPP-YOLO-T3.yaml")  # , task='detect')
    model.load(r"yolo11n.pt")  # 注释则不加载
    results = model.train(
        data=r"data/20.yaml",  # 数据集配置文件的路径
        epochs=200,  # 训练轮次总数
        batch=8,  # 批量大小，即单次输入多少图片训练
        imgsz=640,  # 训练图像尺寸
        workers=8,  # 加载数据的工作线程数
        device=0,  # 指定训练的计算设备，无nvidia显卡则改为 'cpu'
        optimizer="SGD",  # 训练使用优化器，可选 auto,SGD,Adam,AdamW 等
        amp=True,  # True 或者 False, 解释为：自动混合精度(AMP) 训练
        # classes=[1,2,4],
        cache=False,  # True 在内存中缓存数据集图像，服务器推荐开启
    )

# import warnings
#
# warnings.filterwarnings('ignore')
# from ultralytics import YOLO
#
# if __name__ == '__main__':
#     # 直接加载yolo11s.pt，框架自动匹配对应的s规模网络结构（无需手动加载yaml）
#     model = YOLO('yolov3u.pt')  # 核心修改：直接加载s规模预训练权重
#
#     results = model.train(
#         data='data/20.yaml',  # 数据集配置文件的路径
#         epochs=200,  # 训练轮次总数
#         batch=8,  # 批量大小，即单次输入多少图片训练
#         imgsz=640,  # 训练图像尺寸
#         workers=8,  # 加载数据的工作线程数
#         device=0,  # 指定训练的计算设备，无nvidia显卡则改为 'cpu'
#         optimizer='SGD',  # 训练使用优化器，可选 auto,SGD,Adam,AdamW 等
#         amp=True,  # True 或者 False, 解释为：自动混合精度(AMP) 训练
#         # classes=[1,2,4],
#         cache=False  # True 在内存中缓存数据集图像，服务器推荐开启
#     )
