from sqlalchemy import *
from sqlalchemy.orm import *
import os
from datetime import datetime
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

def query_data(study_id, record_type, participant_id=None, start_date=None, end_date=None):
    records = ''
    id_filter = Study.sa.id == study_id
    participant_filter = Participant.sa.id == participant_id
    start_date_filter = Study.sa.study_id.start_date >= start_date
    end_date_filter = Study.sa.study_id.end_date <= end_date

    session = db.get_session()

    if start_date is None:
        start_date = Study.sa.study_id.start_date
    if end_date is None:
        end_date = Study.sa.study_id.end_date

    try:
        records = session.query(FitbitHeartRecord.sa)\
            .join(FitbitAccount.sa, FitbitHeartRecord.sa.device) \
            .join(Participant.sa, FitbitAccount.sa.subject) \
            .join(StudyHasParticipant.sa, Participant.sa.id) \
            .join(Study, StudyHasParticipant.sa.study) \
            .filter(id_filter)\
            .filter(start_date_filter).filter(end_date_filter)

        if participant_id is not None:
            records.filter(participant_filter)
    except:
        session.rollback()
        raise
    finally:
        session.close() # !important

    return records
