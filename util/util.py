from sql_app.database import SessionLocal, engine
from urllib import parse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from util.config import slack_token
from passlib.context import CryptContext
import json

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
async def get_context(req):
    context = {i.split("=")[0]:i.split("=")[1] for i in req.decode("utf-8").split("&")}
    context['text'] = parse.unquote(context['text']).replace('+', " ")
    if context['text']!='' and '||' in context['text'] :
        context['text'] = context['text'].split("||")
    return context

def output(res):
    data = {"key":res.key,
        #"no":res.no,
        "author_id":res.author_id,
        "state":res.state,
        "author_name":res.author_name,
        "title":res.title,
        "detail":res.detail,
        "write_time":res.write_time}
    txt="-"*10
    for i in data:
        txt= txt + f"\n * {i} : {data[i]}\n"
    return txt



def sendMassage(text: str, slack_token: str = slack_token):
    client = WebClient(token=slack_token)
    try:
        response = client.chat_postMessage(
            channel="issue-bot",
            text=text
        )
    except SlackApiError as e:
                # You will get a SlackApiError if "ok" is False
        assert e.response["error"]
        
# update 용도 (flutter)
async def get_update_context(req):
    context = json.loads(req.decode('utf-8'))
    return context

#키 값 있는지 확인 (flutter)
def _is_json_key(json, key):
    try:
        tmp = json[key]
    except KeyError:
        return False
    return True

class hash:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def validate_date(date_text):
	try:
		datetime.datetime.strptime(date_text,"%Y-%m-%d")
		return True
	except ValueError:
		print("Incorrect data format({0}), should be YYYY-MM-DD".format(date_text))
		return False