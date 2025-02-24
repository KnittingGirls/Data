import json
import os
import numpy as np
import cv2
from PIL import Image

json_folder = "./purl/label"
image_folder = "./purl/image"
output_folder = "./purl/annotation"

category_colors = {
    1: (255, 255, 0),  # single_jersey
    2: (0, 0, 255),    # rib
    3: (0, 255, 0),    # purl
    5: (147, 20, 255), # moss
    6: (0, 255, 255),  # ajour
    0: (0, 0, 0)       # background
}

os.makedirs(output_folder, exist_ok=True)

image_files = {os.path.splitext(f)[0]: f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))}

# 좌표 정렬 함수 (시계 방향 정렬)
def sort_clockwise(points):
    center = np.mean(points, axis=0)
    return sorted(points, key=lambda p: np.arctan2(p[1] - center[1], p[0] - center[0]))

# JSON 폴더 안의 모든 JSON 파일 처리
for json_file in os.listdir(json_folder):
    if not json_file.endswith(".json"):
        continue

    json_number, _ = os.path.splitext(json_file)
    if json_number not in image_files:
        print(f"Warning: No matching image for {json_file}. Skipping...")
        continue

    json_path = os.path.join(json_folder, json_file)
    image_path = os.path.join(image_folder, image_files[json_number])

    # JSON 파일 로드
    with open(json_path, "r") as f:
        data = json.load(f)

    # 원본 이미지 열기
    original = Image.open(image_path)
    width, height = original.size

    # 빈 라벨 이미지 생성 (배경색은 흰색)
    label_image = np.ones((height, width, 3), dtype=np.uint8) * 255

    # 각 주석(annotations)에 대해 라벨 이미지 생성
    for annotation in data.get("annotations", []):
        category_id = annotation["category_id"]
        polygon = annotation["polygon"]

        # 정규화된 좌표를 실제 픽셀 좌표로 변환 후 중복 제거
        polygon_pixels = list(set((round(x * width), round(y * height)) for x, y in polygon))

        # ⚠️ 최소 3개 좌표가 없으면 스킵
        if len(polygon_pixels) < 3:
            print(f"Warning: Polygon with {len(polygon_pixels)} points in {json_file} skipped.")
            continue

        # 좌표 정렬 (시계 방향)
        polygon_pixels = sort_clockwise(polygon_pixels)

        # OpenCV 다각형 단순화 (Ramer-Douglas-Peucker 알고리즘)
        epsilon = 0.01 * cv2.arcLength(np.array(polygon_pixels, np.int32), True)
        polygon_pixels = cv2.approxPolyDP(np.array(polygon_pixels, np.int32), epsilon, True)

        # 라벨 색상 선택 (BGR 변환)
        color = category_colors.get(category_id, (0, 255, 0))
        color_bgr = (color[2], color[1], color[0])  # OpenCV는 BGR 사용

        # OpenCV로 폴리곤 내부 채우기
        cv2.fillPoly(label_image, [polygon_pixels], color_bgr)

    # OpenCV에서 변경된 이미지를 PIL 형식으로 변환 후 저장
    label_image_pil = Image.fromarray(label_image)
    label_path = os.path.join(output_folder, f"label_{image_files[json_number]}")
    label_image_pil.save(label_path)

    print(f"Saved label image: {label_path}")

print("Label image generation complete.")
