from sqlalchemy import *
from sqlalchemy.orm import *
import os
from datetime import datetime, timedelta
from WearWareRESTAPI.models import *
import aldjemy

DB_HOST = 'wearware.cqr2btyia7sd.us-west-1.rds.amazonaws.com'
DBMS = 'postgresql'
DB_PORT = '5432'
DB_NAME = 'wearware'
DB_USER = 'wearware'
DB_PWD = 'databit!'

DB_ENGINE_URL = '%s://%s:%s@%s:%s/%s' % (DBMS, DB_USER, DB_PWD, DB_HOST,\
             DB_PORT, DB_NAME)


class MyDBUtil(object):
 engine = None
 Session = None

 def __init__(self):
  self.connect()

 def connect(self):
  if MyDBUtil.engine is None:
   MyDBUtil.engine = create_engine(DB_ENGINE_URL, echo=False)

  if MyDBUtil.Session is None:
   MyDBUtil.Session = sessionmaker(bind=MyDBUtil.engine)

 def get_session(self):
  self.connect()
  return MyDBUtil.Session()

def query_all_participants(db,study_id:int):
     records = ''
     id_filter = Study.sa.id == study_id
     session = db.get_session()
     try:
        records = session.query(Participant.sa)\
            .join(StudyHasParticipant.sa)\
            .join(Study.sa)\
            .filter(id_filter)
     except:
        session.rollback()
        raise
     finally:
        session.close() # !important

     return records

def query_data(db,study_id:int, record_type, nickname="", start_date="", end_date=""):
    session = db.get_session()
    nickname_filter = Participant.sa.nickname == nickname
    id_filter = Study.sa.id == study_id
    timestamp_format = '%Y-%m-%d'

    if record_type == 'hr':
        table = FitbitHeartRecord.sa
    elif record_type == 'sleep':
        table = FitbitSleepRecord.sa
    elif record_type == 'activity':
        table = FitbitMinuteRecord.sa

    try:
        study = session.query(Study.sa).filter(id_filter).first()

        if start_date == "":
            start_date = study.start_date

        else:
            start_date = datetime.strptime(start_date, timestamp_format)
            if start_date.date() < study.start_date:
                start_date = study.start_date

        if end_date == "":
            end_date = study.end_date
            end_date = end_date + timedelta(days=1)

        else:
            end_date = datetime.strptime(end_date, timestamp_format)
            end_date = end_date + timedelta(days=1)
            if end_date.date() < study.end_date:
                end_date = study.end_date

        if  nickname == "":
            participant_id=-1
        else:
            participant = session.query(Participant.sa).filter(nickname_filter).first()
            participant_id = participant.id

        records = ''

        participant_filter = Participant.sa.id == participant_id
        start_date_filter = table.timestamp >= start_date
        end_date_filter = table.timestamp < end_date

        records = session.query(table)\
            .join(FitbitAccount.sa) \
            .join(Participant.sa) \
            .join(StudyHasParticipant.sa) \
            .join(Study.sa) \
            .filter(id_filter)\
            .filter(start_date_filter)\
            .filter(end_date_filter)

        if int(participant_id) >= 0:
            records = records.filter(participant_filter)
    except:
        session.rollback()
        raise
    finally:
        session.close() # !important
    print(records)
    return records
