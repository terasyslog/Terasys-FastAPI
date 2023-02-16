import uuid
import contextvars
from typing import Dict
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from util.util import get_context, get_db, output, sendMassage, get_update_context, _is_json_key, hash
from datetime import datetime as dt
import route.issue_route as issue_route
# gpt
from gptapi.gpt_api import request_gpt
from threading import Thread
# add 오경진.. zz
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


app = FastAPI()
app.include_router(issue_route.router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def getTest():
    return {"Hello" : "this is main page"}

@app.middleware("http")
async def request_middleware(request: Request, call_next):
    request_id_contextvar = contextvars.ContextVar("request_id", default=None)
    request_id = str(uuid.uuid4())
    request_id_contextvar.set(request_id)
    logger.debug("Request started")
    try:
        return await call_next(request)

    except Exception as e:
        logger.debug(f"Request failed: {e}")
        return {"result": "-1"}

    finally:
        assert request_id_contextvar.get() == request_id
        logger.debug("Request ended")


# @app.post("/create")
# async def createList(context: Dict[str, str], db: Session = Depends(get_db)):
#     try:
#         db_user = crud.search_userId(db, context['author_id'])
#         insert_issue = crud.create_issue(db, schemas.IssueBase(
#             title=context['title'],
#             detail=context['detail'],
#             solution=context['solution'],
#             author_id=db_user.id,
#             author_name=db_user.name,
#             write_time=dt.now(),
#             update_time=dt.now(),
#         ))
#         if insert_issue == "0":
#             result = "0"
#         else :
#             result = "-1"
#         return {"result":result}
#     except Exception as e :
#         logger.debug(f"issue Create Failed {e}")
#         return {"result":result}


# flutter 연동 테스트니깐 지우지 말아줘.----------------------------------------
@app.post("/issue/list")        
async def getList(db: Session = Depends(get_db)):
    try :
        print('il----------------')
        return crud.search_all(db)
    except Exception as e:
        logger.debug(f"Search Failed {e}")
        return {"result":"-1"}

@app.post("/userCreate")
async def userCreate(context: Dict[str, str], db: Session = Depends(get_db)):
    try:
        hash_pw=hash.get_password_hash(context['pw'])
        insert_user = crud.create_user(id=context['id'], name=context['name'], pw=hash_pw, email=context['email'])
        result = "0" if insert_user=="0" else "-1"
        return {"result":result}
    except Exception as e:
        logger.debug(f"Search Failed {e}")
        return {"result":"-1"}
    
@app.post("/userLogin")
async def Login(context : Dict[str, str],db: Session = Depends(get_db)):
    hash_pw = crud.get_email(db, context['email']).pw
    if hash.verify_password(context['pw'], hash_pw):
        return {"result":"0"}
    else:
        return {"result":"-1"}

# ------------------------------------------------------------------------
# 유저 정보 불러오기
@app.post("/userList")
async def getUserList(request: Request, db: Session = Depends(get_db)):
    try: 
        context = await request.body()
        context = await get_update_context(context)
        
        result = crud.get_email(db, context['email'], context['pw'])
        if result is None:
            ret = [{"result": "-1"}]
        else:
            ret = jsonable_encoder(result)
            ret['result'] = "0"
            ret = [ret]
        
        return JSONResponse(ret)
    except Exception as e :
        logger.debug(f"Find User Failed {e}")
        ret['result'] = "-1"
        ret = [ret]
        return JSONResponse(ret)
    
# 유저 비밀번호 찾기
@app.post("/findUser")
async def findUserList(request: Request, db: Session = Depends(get_db)):
    try: 
        context = await request.body()
        context = await get_update_context(context)
        
        result = crud.find_pw(db, context['email'], context['name'])
        if result is None:
            ret = [{"result": "-1"}]
        else:
            ret = jsonable_encoder(result)
            ret['result'] = "0"
            ret = [ret]
        
        return JSONResponse(ret)
    except Exception as e :
        logger.debug(f"Find User Failed {e}")
        ret['result'] = "-1"
        ret = [ret]
        return JSONResponse(ret)

@app.post("/gpt")
async def getText(request: Request):
    try:
        req = await request.body()
        context = await get_context(req)
        txt=context['text']
        thr = Thread(target=backgroundworker, args=[txt] )
        thr.start()
        return "응답중"
    except Exception as e :
        logger.debug(f"Failed {e}")
        return {"result":"-1"}
def backgroundworker(text):
    result = request_gpt(text)
    return sendMassage(result)


# # 유저 정보 불러오기 - backup
# @app.post("/userList")
# async def getUserList(request: Request, db: Session = Depends(get_db)):
#     try: 
#         li = []
#         context = await request.body()
#         context = await get_update_context(context)
        
#         result = crud.get_email(db, context['email'], context['pw'])
#         ret = jsonable_encoder(result)
#         if len(ret) == 1 :
#             for a in ret :
#                 a['result']=str(len(ret))
#                 li.append(a)
#             ret = li
#         else :
#             ret = [{"result":"0"}]
#         print(ret)
        
#         return JSONResponse(ret)
#     except Exception as e :
#         logger.debug(f"User List Failed {e}")
#         return JSONResponse([{"result":"-1"}])

# # 업데이트 (flutter)
# @app.post("/update")
# async def updateList(context: Dict[str, str], db: Session = Depends(get_db)):
#     try:
#         # request.body() 가 binary 타입으로 전달 될 경우를 위해 'get_update_context(context)' 부분 추가하였습니다.
#         # context = await request.body()
#         # context = await get_update_context(context)  # 혹시나 flutter에서 바로 dict타입으로 넘어온다면 해당 줄 삭제 필요합니다.
#         # 예시 -> context = { "key": 0, "title": "A", "detail": "B", "solution": "C" }
#         if crud.search_key(db, context["key"]) is not None:
#             result = crud.update_list(db, context)
#         else:
#             result = "-1"
#         return {"result" : result}
#     except Exception as e :
#         logger.debug(f"issue Update Failed {e}")
#         return {"result" : result}


# # 삭제 (flutter)
# @app.post("/delete")
# async def deleteList(request: Request, db: Session = Depends(get_db)):
#     try:
#         # request.body() 가 binary 타입으로 전달 될 경우를 위해 'get_update_context(context)' 부분 추가하였습니다.
#         context = await request.body()
#         context = await get_update_context(context) # 혹시나 flutter에서 바로 dict타입으로 넘어온다면 해당 줄 삭제 필요합니다.
#         # 예시 -> context = { "key": 0 }
#         if crud.search_key(db, context["key"]) is not None:
#             result = crud.delete_list(db, context)
#         else:
#             result = "-1"
#         return {"result":result}
#     except Exception as e :
#         logger.debug(f"issue Delete Failed {e}")
#         return {"result":"-1"}
    
# 조회 (flutter)
@app.post("/search")
async def search_all(request: Request, db: Session = Depends(get_db)): # 예시 -> context = { "key": 0, "title": "A", "detail": "B", "solution": "C" }
    try:
        context = await request.body()
        context = await get_update_context(context) # 혹시나 flutter에서 바로 dict타입으로 넘어온다면 해당 줄 삭제 필요합니다.
        
        #조회할 키 값이 있는경우 해당 내용으로 조회 / 키값 없이 요청받을 경우 전체조회
        if(_is_json_key(context, 'key')):return jsonable_encoder(crud.search_key(db,context['key']))
        elif(_is_json_key(context, 'title')):return jsonable_encoder(crud.search_title(db,context['title']))
        elif(_is_json_key(context, 'detail')):return jsonable_encoder(crud.search_detail(db,context['detail']))
        elif(_is_json_key(context, 'solution')):return jsonable_encoder(crud.search_solution(db,context['solution']))
        elif(_is_json_key(context, 'write_time')):return jsonable_encoder(crud.search_write_time(db,context['write_time']))
        elif(_is_json_key(context, 'update_time')):return jsonable_encoder(crud.search_update_time(db,context['update_time']))
        elif(_is_json_key(context, 'author_name')):return jsonable_encoder(crud.search_author_name(db,context['author_name']))
        elif(_is_json_key(context, 'project_name')):return jsonable_encoder(crud.search_project_name(db,context['project_name']))
        elif(_is_json_key(context, 'category_name')):return jsonable_encoder(crud.search_category_name(db,context['category_name']))
        
        return jsonable_encoder(crud.search_all(db))
    except Exception as e :
        logger.debug(f"search Failed {e}")
        return {"result":"-1"}
        #return {f"search_all Failed {e}"}


if __name__ == '__main__' :
  uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=False, workers=10, log_config='log.ini')
       

'''
# 이슈번호로 이슈날짜 갱신
@app.post("/write_date")
async def test(request: Request, db: Session = Depends(get_db)):
    req = await request.body()
    context = await get_context(req)
    text = context['text']
    output_text = list(map(output, [crud.write_date(db, text)]))
    output_text = tabulate(output_text[0], headers='keys',tablefmt="heavy_grid")
    return sendMassage(f"*success*\n{output_text}")

# 이슈번호로 작성자 갱신
@app.post("/write_author")
async def test(request: Request, db: Session = Depends(get_db)):
    req = await request.body()
    context = await get_context(req)
    text = context['text']
    output_text = list(map(output, [crud.write_author(db, text)]))
    output_text = tabulate(output_text[0], headers='keys',tablefmt="heavy_grid")
    return sendMassage(f"*success*\n{output_text}")

# 이슈번호로 프로젝트 갱신
@app.post("/write_project")
async def write_project(request: Request, db: Session = Depends(get_db)):
    req = await request.body()
    context = await get_context(req)
    text = context['text'] + [context['user_name']]
    output_text = list(map(output, [crud.write_project(db, text)]))
    output_text = tabulate(output_text[0], headers='keys',tablefmt="heavy_grid")
    return sendMassage(f"*success*\n{output_text}")

# 이슈번호로 카테고리 갱신
@app.post("/write_category")
async def write_category(request: Request, db: Session = Depends(get_db)):
    req = await request.body()
    context = await get_context(req)
    text = context['text'] + [context['user_name']]
    output_text = list(map(output, [crud.write_category(db, text)]))
    output_text = tabulate(output_text[0], headers='keys',tablefmt="heavy_grid")
    return sendMassage(f"*success*\n{output_text}")

'''
