# Acousto-LED 해석 코드

2026 디스플레이 챌린지 출품작 **Acousto-LED**(팀 전자물리학과 무적함대) 제안서에 들어간 도식을 생성하는 파이썬 스크립트입니다.

| 파일 | 생성 도식 | 내용 |
|---|---|---|
| `Acousto-LED_배열시뮬레이션.py` | 도식 5 | 16채널 선형 배열(피치 21.6 mm) 빔 조향·지향 패턴 시뮬레이션 |
| `Acousto-LED_원가사업성계산.py` | 도식 6, 7 | 패널당 예비 BOM 구조와 단위 경제 |

## 실행

```bash
pip install -r requirements.txt
python Acousto-LED_배열시뮬레이션.py
python Acousto-LED_원가사업성계산.py
```

결과 이미지는 스크립트와 같은 폴더의 `figures/`에 저장됩니다.

## 참고

- 그림 폰트로 `Noto Sans CJK JP`를 사용합니다. 설치되어 있지 않으면 한글이 깨질 수 있으니, 폰트를 설치하거나 스크립트 상단의 `font.family`를 `Malgun Gothic`(Windows) / `AppleGothic`(macOS) 등으로 바꿔 주세요.
