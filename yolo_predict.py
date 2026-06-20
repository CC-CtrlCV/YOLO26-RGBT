from ultralytics import YOLO

# 加载预训练的 YOLOv8n 模型
# model = YOLO('runs/detect/train8/weights/best.pt')
model = YOLO(r"D:\XiangMu\YOLO\yolov11-ultralytics-main\runs\detect\train44\weights\best.pt")
# 定义图像文件的路径
source = r"D:\Data\UAV_DaJiang\Chouzhen_images\ShuJuJi\D4\shiyan_queren\images\frame1_000408_248_crop_760_680_6.jpg"  # 更改为自己的图片路径
# 运行推理，并附加参数
model.predict(source, save=True)


# from ultralytics import YOLO
# # 加载训练好的模型，改为自己的路径
# model = YOLO('runs/detect/train/weights/best.pt')
# # 修改为自己的图像或者文件夹的路径
# source = 'test1.jpg' #修改为自己的图片路径及文件名
# # 运行推理，并附加参数
# model.predict(source, save=True)

# 1frame1_000236_156_crop_2280_0_3.jpg
# 2frame_000024_024_crop_2280_680_8.jpg
# 2frame_000224_144_crop_1520_0_2.jpg
# 2frame_000244_164_crop_2280_680_8.jpg
# frame_000240_160_crop_1520_680_7.jpg
# frame1_000408_248_crop_760_680_6.jpg
