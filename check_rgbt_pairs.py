import argparse
from pathlib import Path

IMG_FORMATS = {"bmp", "dng", "jpeg", "jpg", "mpo", "png", "tif", "tiff", "webp", "pfm", "heic"}


def parse_args():
    parser = argparse.ArgumentParser(description="Check visible/infrared image pairing for an RGBT dataset split.")
    parser.add_argument("visible_dir", help="Directory containing visible/RGB images, e.g. KAIST8/visible/train")
    parser.add_argument("--rgb-token", default="visible")
    parser.add_argument("--ir-token", default="infrared")
    parser.add_argument("--limit", type=int, default=20, help="Maximum missing pairs to print")
    return parser.parse_args()


def main():
    args = parse_args()
    visible_dir = Path(args.visible_dir)
    if not visible_dir.is_dir():
        raise FileNotFoundError(f"Visible directory not found: {visible_dir}")

    image_files = sorted(p for p in visible_dir.rglob("*") if p.suffix.lower().lstrip(".") in IMG_FORMATS)
    missing = []
    for image_file in image_files:
        image_path = str(image_file)
        if args.rgb_token not in image_path:
            raise ValueError(f"'{args.rgb_token}' not found in visible image path: {image_file}")
        ir_file = Path(image_path.replace(args.rgb_token, args.ir_token, 1))
        if not ir_file.is_file():
            missing.append((image_file, ir_file))

    print(f"Checked {len(image_files)} visible images.")
    if not missing:
        print("All infrared pairs were found.")
        return

    print(f"Missing {len(missing)} infrared pairs:")
    for visible, infrared in missing[: args.limit]:
        print(f"{visible} -> {infrared}")
    if len(missing) > args.limit:
        print(f"... {len(missing) - args.limit} more")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
