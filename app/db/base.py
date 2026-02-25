from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.db.models import user
from app.db.models import course
from app.db.models import enrollment