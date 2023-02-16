from fastapi import APIRouter, Depends
from typing import Dict
from util.util import get_db
from sqlalchemy.orm import Session
from sql_app import crud, schemas
from datetime import datetime as dt
from loguru import logger

router = APIRouter(
    prefix="/issue",
    tags=["crud"],
    responses={404: {"description": "Not found"}}
)

@router.post("/create")
async def createList(context: Dict[str, str], db: Session = Depends(get_db)):
    try:
        db_user = crud.search_userId(db, context['author_id'])
        insert_issue = crud.create_issue(db, schemas.IssueBase(
            title=context['title'],
            detail=context['detail'],
            solution=context['solution'],
            author_id=db_user.id,
            author_name=db_user.name,
            write_time=dt.now(),
            update_time=dt.now(),
        ))
        if insert_issue == "0":
            result = "0"
        else :
            result = "-1"
        return {"result":result}
    except Exception as e :
        logger.debug(f"issue Create Failed {e}")
        return {"result":result}
    
# 업데이트 (flutter)
@router.post("/update")
async def updateList(context: Dict[str, str], db: Session = Depends(get_db)):
    try:
        if crud.search_key(db, context["key"]) is not None:
            result = crud.update_list(db, context)
        else:
            result = "-1"
        return {"result" : result}
    except Exception as e :
        logger.debug(f"issue Update Failed {e}")
        return {"result" : result}


# 삭제 (flutter)
@router.post("/delete")
async def deleteList(context: Dict[str, str], db: Session = Depends(get_db)):
    try:
        if crud.search_key(db, context["key"]) is not None:
            result = crud.delete_list(db, context)
        else:
            result = "-1"
        return {"result":result}
    except Exception as e :
        logger.debug(f"issue Delete Failed {e}")
        return {"result":"-1"}