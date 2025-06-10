import uuid
from sqlalchemy.orm import sessionmaker
from app.database import engine
from app.models.case import Case

Session = sessionmaker(bind=engine)
session = Session()

cases = session.query(Case).filter((Case.case_id == None) | (Case.case_id == '')).all()

for case in cases:
    case.case_id = str(uuid.uuid4())
    print(f"Updated case id {case.id} with new case_id {case.case_id}")

session.commit()
session.close()
print("All cases with missing case_id have been updated.")