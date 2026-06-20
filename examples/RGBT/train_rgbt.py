import argparse

from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(description="Train an RGBT YOLO model.")
    parser.add_argument("--model", default="ultralytics/cfg/models/26-RGBT/yolo26-rgbt-midfusion.yaml")
    parser.add_argument("--data", default="ultralytics/cfg/datasets/KAIST8-rgbt.yaml")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--device", default=0)
    parser.add_argument("--project", default="runs/rgbt")
    parser.add_argument("--name", default="yolo26-rgbt-midfusion")
    return parser.parse_args()


def main():
    args = parse_args()
    model = YOLO(args.model)
    model.train(
        data=args.data,
        imgsz=args.imgsz,
        epochs=args.epochs,
        batch=args.batch,
        device=args.device,
        project=args.project,
        name=args.name,
    )


if __name__ == "__main__":
    main()
