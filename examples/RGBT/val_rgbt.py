import argparse

from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(description="Validate an RGBT YOLO model.")
    parser.add_argument("--model", default="runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt")
    parser.add_argument("--data", default="ultralytics/cfg/datasets/KAIST8-rgbt.yaml")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--device", default=0)
    parser.add_argument("--split", default="val", choices=["val", "test", "train"])
    parser.add_argument("--project", default="runs/rgbt-val")
    parser.add_argument("--name", default="yolo26-rgbt-midfusion")
    return parser.parse_args()


def main():
    args = parse_args()
    model = YOLO(args.model)
    model.val(
        data=args.data,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        split=args.split,
        project=args.project,
        name=args.name,
    )


if __name__ == "__main__":
    main()
