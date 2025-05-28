import joblib
from sklearn.ensemble import RandomForestClassifier

patterns = [
    "(a+)+",      # 취약
    "a*b+",       # 안전
    "(ab|cd)+",   # 취약
    "abc*",       # 안전
]
labels = [1, 0, 1, 0]  # 1: 취약, 0: 안전

def extract_features(pattern: str):
    return [
        len(pattern),
        pattern.count('('),
        pattern.count('+'),
        pattern.count('*'),
        pattern.count('?'),
        pattern.count('|'),
        pattern.count('{'),
        pattern.count('['),
    ]

X = [extract_features(p) for p in patterns]
y = labels

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, 'redos_model.pkl')