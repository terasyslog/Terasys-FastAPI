from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from . import models, schemas
from datetime import datetime
# [ USERS ]USERNAME으로 조회
def search_userName(db: Session, name: str):
    return db.query(models.Users).filter(models.Users.name == name).first()

# [ USERS ]USERID로 조회
def search_userId(db: Session, id: str):
    return db.query(models.Users).filter(models.Users.id == id).first()

# # [ USERS EMAIL, PASSWORD로 조회 ]   
# def search_email(db: Session, email: str, pw: str):
#     return db.query(models.Users).filter(models.Users.email == email, models.Users.pw == pw).all()

# --------------------------- ISSUE SEARCH ------------------------------------------------------------------------------------
# 전체리스트 조회
def search_all(db: Session, offset: int, limit: int):
    return db.query(models.Issue).filter(models.Issue.state==1).order_by(models.Issue.update_time.desc()).offset(offset).limit(limit).all()
    #return db.query(models.Issue).order_by(models.Issue.update_time.desc()).all()

# 키값으로 조회
def search_key(db: Session, key: int):
    return db.query(models.Issue).filter(models.Issue.key == key).order_by(models.Issue.update_time.desc()).all()

# 이슈제목으로 조회
def search_title(db: Session, title, offset: int, limit: int):
    return db.query(models.Issue).filter(models.Issue.title.like(f'%{title}%')).filter(models.Issue.state==1).order_by(models.Issue.update_time.desc()).offset(offset).limit(limit).all()

# 이슈내용으로 조회
def search_detail(db: Session, detail, offset: int, limit: int):
    return db.query(models.Issue).filter(models.Issue.detail.like(f'%{detail}%')).filter(models.Issue.state==1).order_by(models.Issue.update_time.desc()).offset(offset).limit(limit).all()

# 해결방안으로 조회
def search_solution(db: Session, solution, offset: int, limit: int):
    return db.query(models.Issue).filter(models.Issue.solution.like(f'%{solution}%')).filter(models.Issue.state==1).order_by(models.Issue.update_time.desc()).offset(offset).limit(limit).all()

# 작성날짜로 조회
def search_write_time(db: Session, write_time, offset: int, limit: int):
    write_time = datetime.strptime(write_time, '%Y-%m-%d').date()
    return db.query(models.Issue).filter(models.Issue.write_time == write_time).filter(models.Issue.state==1).order_by(models.Issue.update_time.desc()).offset(offset).limit(limit).all()

# 갱신날짜로 조회
def search_update_time(db: Session, update_time, offset: int, limit: int):
    update_time = datetime.strptime(update_time, '%Y-%m-%d').date()
    return db.query(models.Issue).filter(models.Issue.update_time == update_time).filter(models.Issue.state==1).order_by(models.Issue.update_time.desc()).offset(offset).limit(limit).all()

# 작성자로 조회
def search_author_name(db: Session, author_name, offset: int, limit: int):
    return db.query(models.Issue).filter(models.Issue.author_name.like(f'%{author_name}%')).order_by(models.Issue.update_time.desc()).offset(offset).limit(limit).all()

# 프로젝트로 조회
def search_project_name(db: Session, project_name, offset: int, limit: int):
    return db.query(models.Issue).filter(models.Issue.project_name.like(f'%{project_name}%')).order_by(models.Issue.update_time.desc()).offset(offset).limit(limit).all()

# 카테고리로 조회
def search_category_name(db: Session, category_name, offset: int, limit: int):
    return db.query(models.Issue).filter(models.Issue.category_name.like(f'%{category_name}%')).order_by(models.Issue.update_time.desc()).offset(offset).limit(limit).all()

# ----------------------------------- ISSUE CREATE -------------------------------------------------------------------------

def create_issue(db: Session, issue: schemas.Issue):
    insert_issue = models.Issue(
        title = issue.title,
        detail = issue.detail,
        author_name = issue.author_name,
        author_id = issue.author_id,
        write_time = issue.write_time,
        update_time = issue.update_time,
        solution = issue.solution,
        project_id = issue.project_id,
        project_name = issue.project_name,
        category_id	= issue.category_id,
        category_name = issue.category_name
    )
    db.add(insert_issue)
    db.commit()
    db.refresh(insert_issue)
    print("ADD_ISSUE COMPLETE", datetime.now())
    return "0"

# -------------------------------------------------------------------------------------------------------------------

# 선택대상 업데이트 (flutter 용도)
def update_list(db: Session, update_data):
    update_key = int(update_data["key"])
    update_title = update_data["title"]
    update_detail = update_data["detail"]
    update_solution = update_data["solution"]
    db.query(models.Issue).filter(
        models.Issue.key == update_key).update({
            models.Issue.title : update_title, 
            models.Issue.detail : update_detail,
            models.Issue.solution : update_solution,
            models.Issue.update_time : datetime.now()
        }
    )
    db.commit()
    return "0"
    

# 선택대상 삭제 (flutter 용도)
def delete_list(db: Session, delete_data):
    delete_key = int(delete_data["key"])
    db.query(models.Issue).filter(models.Issue.key == delete_key).delete()
    db.commit()
    return "0"



# ----------------- LOGIN ------------------------------------------------------------------

# 계정생성
def create_user(db: Session, user: schemas.UserCreate):
    insert_user = models.Users(id=user.id, name=user.name, pw=user.pw, email=user.email)
    db.add(insert_user)
    db.commit()
    db.refresh(insert_user)
    return "0"

def get_email(db: Session, email: str, pw: str):
    return db.query(models.Users).filter(models.Users.email == email, models.Users.pw == pw).first()

def find_pw(db: Session, email: str, name: str):
    return db.query(models.Users).filter(models.Users.email == email, models.Users.name == name).first()

# ---------------------------------------------------------------------------------------------





'''
# 이슈번호로 이슈날짜 갱신
def write_date(db: Session, get_text):
    no = int(get_text[0])
    date = get_text[1]
    user_name = get_text[2]
    db.query(models.Issue).filter(models.Issue.no == no).update({models.Issue.state : 0})
    db.commit()
    issue = db.query(models.Issue).filter(models.Issue.no == no).first()
    insert_issue = models.Issue(
        title = issue.title,
        detail = issue.detail,
        author_name = db.query(models.Users).filter(models.Users.id == user_name).first().name,
        author_id = user_name,
        no = issue.no,
        write_time = datetime.strptime(date, '%Y-%m-%d').date(),
        solution = issue.solution,
        project_id = issue.project_id,
        project_name = issue.project_name,
        category_id	= issue.category_id,
        category_name = issue.category_name
    )
    db.add(insert_issue)
    db.commit()
    db.refresh(insert_issue)
    return insert_issue

# 이슈번호로 작성자 갱신
def write_author(db: Session, get_text):
    no = int(get_text[0])
    name = get_text[1]
    db.query(models.Issue).filter(models.Issue.no == no).update({models.Issue.state : 0})
    db.commit()
    issue = db.query(models.Issue).filter(models.Issue.no == no).first()
    insert_issue = models.Issue(
        title = issue.title,
        detail = issue.detail,
        author_name = name,
        author_id = db.query(models.Users).filter(models.Users.name == name).first().id,
        no = issue.no,
        write_time = datetime.now(),
        solution = issue.solution,
        project_id = issue.project_id,
        project_name = issue.project_name,
        category_id	= issue.category_id,
        category_name = issue.category_name
    )
    db.add(insert_issue)
    db.commit()
    db.refresh(insert_issue)
    return insert_issue

# 이슈번호로 프로젝트 갱신
def write_project(db: Session, get_text):
    no = int(get_text[0])
    name = get_text[1]
    user_name = get_text[2]
    db.query(models.Issue).filter(models.Issue.no == no).update({models.Issue.state : 0})
    db.commit()
    issue = db.query(models.Issue).filter(models.Issue.no == no).first()
    insert_issue = models.Issue(
        title = issue.title,
        detail = issue.detail,
        author_name = db.query(models.Users).filter(models.Users.id == user_name).first().name,
        author_id = user_name,
        no = issue.no,
        write_time = datetime.now(),
        solution = issue.solution,
        project_id = db.query(models.Project).filter(models.Project.name == name).first().id,
        project_name = name,
        category_id	= issue.category_id,
        category_name = issue.category_name
    )
    db.add(insert_issue)
    db.commit()
    db.refresh(insert_issue)
    return insert_issue


# 이슈번호로 카테고리 갱신
def write_category(db: Session, get_text):
    no = int(get_text[0])
    name = get_text[1]
    user_name = get_text[2]
    db.query(models.Issue).filter(models.Issue.no == no).update({models.Issue.state : 0})
    db.commit()
    issue = db.query(models.Issue).filter(models.Issue.no == no).first()
    insert_issue = models.Issue(
        title = issue.title,
        detail = issue.detail,
        author_name = db.query(models.Users).filter(models.Users.id == user_name).first().name,
        author_id = user_name,
        no = issue.no,
        write_time = datetime.now(),
        solution = issue.solution,
        project_id = issue.project_id,
        project_name = issue.project_name,
        category_id	= db.query(models.Category).filter(models.Category.name == name).first().id,
        category_name = name
    )
    db.add(insert_issue)
    db.commit()
    db.refresh(insert_issue)
    return insert_issue
'''
