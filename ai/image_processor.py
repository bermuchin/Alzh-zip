import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np

class ImageFeatureExtractor:
    def __init__(self):
        # 사전 학습된 ResNet18 로드 (의료 영상의 기본 특징 포착 능력이 좋음)
        self.model = models.resnet18(pretrained=True)
        # 마지막 분류 레이어를 제거하여 '특징 추출기'로만 사용
        self.model = torch.nn.Sequential(*(list(self.model.children())[:-1]))
        self.model.eval()
        
        # 이미지 전처리 (CNN 입력 규격에 맞춤)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def extract(self, img_path):
        """이미지를 넣으면 512차원 특징 벡터를 반환"""
        try:
            image = Image.open(img_path).convert('RGB')
            image = self.transform(image).unsqueeze(0)
            with torch.no_grad():
                feature = self.model(image)
            return feature.flatten().numpy()
        except Exception as e:
            print(f"이미지 추출 오류: {e}")
            return np.zeros(512) # 오류 시 빈 벡터 반환