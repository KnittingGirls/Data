import os
import json

# 폴더 경로 설정 (절대 경로로 변경)
input_folder = os.path.abspath("./txtLabel")
output_folder = os.path.abspath("./jsonLabel")

# 디렉토리가 없으면 생성
os.makedirs(output_folder, exist_ok=True)

# 데이터 변환 함수
def parse_labels_to_json(file_path, image_name):
    annotations = []

    # 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split()
        category_id = int(parts[0])  # 카테고리 ID
        points = list(map(float, parts[1:]))  # 좌표들

        # 폴리곤 좌표 생성
        polygon = [[points[i], points[i + 1]] for i in range(0, len(points), 2)]

        # JSON 구조 추가
        annotations.append({
            "image_name": image_name,  # 이미지 파일 이름
            "category_id": category_id,
            "polygon": polygon
        })

    # 최종 JSON 구조 반환
    return {"annotations": annotations}

# 폴더 내 모든 .txt 파일 처리
for file_name in os.listdir(input_folder):
    if file_name.endswith(".txt"):
        # 파일 경로 설정
        input_path = os.path.join(input_folder, file_name)
        image_name = file_name.replace(".txt", ".jpg")  # 이미지 이름 변경
        output_path = os.path.join(output_folder, file_name.replace(".txt", ".json"))

        # 기존 파일이 열려 있다면 닫기
        if os.path.exists(output_path):
            try:
                os.remove(output_path)  # 기존 파일 삭제
            except PermissionError:
                print(f"경고: {output_path} 삭제 권한이 없습니다.")

        # 데이터 변환
        json_output = parse_labels_to_json(input_path, image_name)

        # JSON 파일로 저장
        try:
            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump(json_output, json_file, indent=4)
            print(f"변환 완료: {input_path} -> {output_path}")
        except PermissionError:
            print(f"오류: {output_path} 파일 쓰기 권한이 없습니다. 관리자 권한으로 실행하세요.")
