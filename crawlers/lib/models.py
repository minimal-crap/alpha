from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import(Column, String, Text, DateTime)
from sqlalchemy import create_engine

from settings import MYSQL_DATABASE_URL, MYSQL_DB

engine = create_engine(MYSQL_DATABASE_URL)
Base = declarative_base()


class Job(Base):
    """
    Model class for Job entries fetched from different websites.
    """
    __tablename__ = "job"
    uuid = Column(String(128), primary_key=True)
    source = Column(String(256))
    url = Column(String(256))
    title = Column(String(256))
    description = Column(Text)
    image = Column(String(256))
    job_type = Column(String(256))
    city = Column(String(256))
    state = Column(String(256))
    how_to_apply = Column(String(256))
    author = Column(String(256))
    posted_at = Column(DateTime)

    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns}  # noqa


if __name__ == '__main__':
    # code to create all models in database
    print("[*]creating tables...")
    Base.metadata.create_all(engine)
