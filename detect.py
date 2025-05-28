import re
import joblib  # 사전 학습된 모델을 불러올 때 사용

def extract_features(pattern: str):
    """정규표현식에서 간단한 특징 추출"""
    return [
        len(pattern),                      # 길이
        pattern.count('('),                # 괄호 개수
        pattern.count('+'),                # + 연산자 개수
        pattern.count('*'),                # * 연산자 개수
        pattern.count('?'),                # ? 연산자 개수
        pattern.count('|'),                # | 연산자 개수
        pattern.count('{'),                # { 개수
        pattern.count('['),                # [ 개수
    ]

def predict_with_ai(pattern: str):
    features = extract_features(pattern)
    model = joblib.load('redos_model.pkl')  # 사전 학습된 모델 필요
    pred = model.predict([features])[0]
    return pred == 1

def main():
    regex = input("검사할 정규표현식을 입력하세요: ")
    if predict_with_ai(regex):
        print("⚠️ AI가 취약한 정규표현식으로 분류했습니다. ReDoS 위험이 있습니다.")
    else:
        print("✅ AI가 안전한 정규표현식으로 분류했습니다.")

if __name__ == "__main__":
    main()