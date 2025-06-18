# 🧶Data Preprocessing🧵

본 저장소는 뜨개질 패턴 생성 프로젝트를 위한 데이터 전처리 및 준비 과정을 포함하고 있습니다. <br> 
수집한 뜨개질 제품 이미지를 모델 학습용으로 전처리하는 파이프라인을 구성합니다.

## 폴더 구성

* **Crawling** : 웹 크롤링을 통한 원본 이미지 수집 코드
* **Cleansing** : 수집한 이미지의 노이즈 제거 및 클렌징 스크립트
* **Preprocessing** : 데이터 전처리 및 의미 없는 라벨 삭제, 통합 처리

## 주요 코드

* **augmentation.ipynb** : 데이터 증강 (Augmentation) 코드
* **test\_train\_val.ipynb** : 전체 데이터를 70:15:15 비율로 train/test/validation으로 분할하는 코드

## 전체 파이프라인

1. **Crawling** → 이미지 수집
2. **Cleansing** → 이미지 정제 및 라벨링 오류 제거
3. **Preprocessing** → 의미 없는 라벨 삭제 및 데이터 통합 정리
4. **augmentation.ipynb** → 데이터 증강
5. **test\_train\_val.ipynb** → 학습 데이터셋 분할

이 저장소를 통해 생성된 최종 전처리 데이터는 DeepLabV3+, SCHP 모델 학습에 활용됩니다.
