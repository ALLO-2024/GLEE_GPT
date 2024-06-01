from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import os
import json
import uuid
from datetime import datetime

import sys
sys.path.append('..')
import inference
import translate_chatgpt
import summary_chatgpt
import keyword_chatgpt


language_list = {'ENGLISH': 'English', 'JAPANESE': 'Japanese', 'CHINESE': 'Chinese', 'VIETNAMESE': 'Vietnamese'}


class ASR_Item(BaseModel):
    
    category: str
    lectureId : int

class Translate_Item(BaseModel):
    
    contents: str
    language: str

class Summary_Item(BaseModel):
    
    contents: str

class Keyword_Item(BaseModel):
    
    contents: str


app = FastAPI()


@app.get('/glee')
#async def root():
def root():
    
    return {'message': 'Fast API'}


@app.get('/glee/home')
def glee():
    
    return {'message': 'glee home'}


@app.post("/glee/asr")
# async def glee_asr(file : UploadFile):
async def glee_asr(category : str = Form(...), lectureId : int = Form(...), file : UploadFile = File(...)):
    
    save_audio_dir = ''
    
    # category = category
    
    audio_file = await file.read()
    
    current_time = datetime.now()
    current_time = current_time.strftime('%Y%m%d_%H%M%S')
    file_name = current_time + '_' + str(uuid.uuid4()) + '.' + str(file.filename).split('.')[-1]
    
    with open(os.path.join(save_audio_dir, file_name), "wb") as f:
        f.write(audio_file)
    
    
    result = inference.run_asr(category, lectureId, file_name)
    
    
    # return JSONResponse({"filename" : file.filename})
    return result


@app.post('/glee/translate')
async def glee_translate(item : Translate_Item):
    
    contents = item.contents
    # language = item.language
    
    if item.language not in language_list:
        
        # return {}
        return # null 리턴
    
    language = language_list[item.language]
    
    result = translate_chatgpt.run_translate(contents, language)
    
    # print(json.loads(result))
    
    return result


@app.post('/glee/summary')
async def glee_summary(item : Summary_Item):
    
    contents = item.contents
    
    result = summary_chatgpt.run_summary(contents)
    
    # print(json.loads(result))
    
    return result


@app.post('/glee/keyword')
async def glee_keyword(item : Keyword_Item):
    
    contents = item.contents
    
    result = keyword_chatgpt.run_keyword(contents)
    
    # print(json.loads(result))
    
    return result
