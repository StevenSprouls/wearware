from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from WearWareRESTAPI.models import *

ex_study_id = 6
ex_participant_id = 101
ex_time_start = '2021-03-12'
ex_time_end = '2021-03-13'


engine = create_engine("postgresql://wearware:databit! \
                       @wearware.cqr2btyia7sd.us-west-1.rds.amazonaws.com:5432/wearware",
                       echo=True)

Session = sessionmaker(bind=engine)
session = Session()


def query_all_participants(study_id):
    records = session.query(Participant)\
        .join(StudyHasParticipant, StudyHasParticipant.participant == Participant.pk)\
        .join(Study, StudyHasParticipant.study == Study.pk)\
        .filter(Study.pk == study_id)


def query_data(study_id, record_type=FitbitHeartRecord, participant_id=None, start_date=None, end_date=None):
    records = session.query(record_type)\
        .join(FitbitAccount, FitbitHeartRecord.device == FitbitAccount.pk) \
        .join(Participant, FitbitAccount.subject == Participant.pk) \
        .join(StudyHasParticipant, Participant.pk == StudyHasParticipant.participant) \
        .join(Study, StudyHasParticipant.study == Study.pk) \
        .filter(Study.pk == study_id)

    if participant_id is not None:
        records.filter(Participant.pk == participant_id)

    if (start_date is not None) and (end_date is not None):
        records.filter()    # might need to address models.py??
