import argparse

from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(description="Run prediction with a trained RGBT YOLO model.")
    parser.add_argument("--model", default="runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt")
    parser.add_argument("--source", default="E:/BaiduNetdiskDownload/RGBTO/KAIST8/visible/test")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--rgb-token", default="visible")
    parser.add_argument("--ir-token", default="infrared")
    parser.add_argument("--project", default="runs/rgbt-predict")
    parser.add_argument("--name", default="yolo26-rgbt-midfusion")
    parser.add_argument("--conf", type=float, default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    model = YOLO(args.model)
    predict_args = dict(
        source=args.source,
        imgsz=args.imgsz,
        rgbt=True,
        rgbt_pair=[args.rgb_token, args.ir_token],
        save=True,
        project=args.project,
        name=args.name,
    )
    if args.conf is not None:
        predict_args["conf"] = args.conf
    model.predict(**predict_args)


if __name__ == "__main__":
    main()
