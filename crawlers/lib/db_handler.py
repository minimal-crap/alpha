import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta

from settings import MYSQL_DATABASE_URL
from models import Job


class HandleDB:
    """
    HandleDB class for handling db interactions.
    """

    def __init__(self):
        """
        HandleDB __init__ method.
        """
        try:
            # creating database session instance
            self.engine = create_engine(MYSQL_DATABASE_URL)
            Session = sessionmaker(bind=self.engine)
            self.session_instance = Session()
        except Exception as error:
            print(error.message)

    def create_job(self, **job_params):
        """
        create_job method to create job entries in db.
        Args:
            job_params (kwarg): multi key value params required to create
            Job entry.
        Returns:
            Job object if successful, None otherwise.
        """
        try:
            current_job = Job(**job_params)
            self.session_instance.add(current_job)
            self.session_instance.commit()
            return current_job
        except Exception as error:
            import ipdb; ipdb.set_trace()
            print(error.message)
            return None

    def list_job(self, **query_params):
        """
        list_job method to list job entries stored in database.
        Args:
            query_params (kwarg): multi key value params containing filters
            for returning specific job entries.
        Returns:
            list collection of job entries as dict if successful,
            None otherwise.
        """
        try:
            query_result = self.session_instance.query(
                Job).filter_by(**query_params)
            job_list = [job.as_dict() for job in query_result]
            return job_list
        except Exception as error:
            print(error)
            return None
