import argparse

from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(description="Export a trained RGBT YOLO model.")
    parser.add_argument("--model", default="runs/rgbt/yolo26-rgbt-midfusion/weights/best.pt")
    parser.add_argument("--format", default="onnx")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=1)
    parser.add_argument("--dynamic", action="store_true")
    parser.add_argument("--simplify", action="store_true")
    parser.add_argument("--opset", type=int, default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    model = YOLO(args.model)
    export_args = dict(
        format=args.format,
        imgsz=args.imgsz,
        batch=args.batch,
        dynamic=args.dynamic,
        simplify=args.simplify,
    )
    if args.opset is not None:
        export_args["opset"] = args.opset
    model.export(**export_args)


if __name__ == "__main__":
    main()
