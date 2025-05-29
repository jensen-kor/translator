from googletrans import Translator
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn

def ko_en_auto_translate(text):
    """
    입력한 문장이 한글이면 영어로, 영어면 한글로 번역해서 반환합니다.
    번역 실패 시 원본을 그대로 반환합니다.
    """
    translator = Translator()
    try:
        detected = translator.detect(text)
        if detected.lang == 'ko':
            translated = translator.translate(text, src='ko', dest='en').text
        else:
            translated = translator.translate(text, src=detected.lang, dest='ko').text
        return translated
    except Exception:
        return text

class TranslateRequest(BaseModel):
    text: str

app = FastAPI()

@app.post("/translate")
async def translate(req: TranslateRequest):
    result = ko_en_auto_translate(req.text)
    return {"original": req.text, "translated": result}

if __name__ == "__main__":
    # 사용자 입력 받기
    user_input = input("한글 또는 영어 문장을 입력하세요: ")
    print("원본:", user_input)
    print("번역:", ko_en_auto_translate(user_input))
    # FastAPI 서버 실행 옵션 (원할 때만 사용)
    # uvicorn.run(app, host="0.0.0.0", port=8000) 