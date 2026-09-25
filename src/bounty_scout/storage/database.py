from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..models import BountyOpportunity


Base = declarative_base()


class BountyOpportunityDB(Base):
    __tablename__ = 'bounty_opportunities'
    
    id = Column(Integer, primary_key=True)
    repository = Column(String(255), nullable=False)
    issue_url = Column(String(512), unique=True, nullable=False)
    title = Column(Text, nullable=False)
    comments = Column(Integer, default=0)
    last_updated = Column(DateTime, nullable=False)
    bounty_tags = Column(ARRAY(String), default=[])
    scan_timestamp = Column(DateTime, default=datetime.utcnow)


class BountyDatabase:
    def __init__(self, db_url: str = "postgresql://user:password@localhost/bounty_scout"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def bulk_insert_opportunities(self, opportunities: List[BountyOpportunity]) -> None:
        """Bulk inserts a list of opportunities."""
        session = self.Session()
        try:
            session.bulk_save_objects([
                BountyOpportunityDB(
                    repository=opportunity.repository,
                    issue_url=opportunity.issue_url,
                    title=opportunity.title,
                    comments=opportunity.comments,
                    last_updated=opportunity.last_updated,
                    bounty_tags=opportunity.bounty_tags,
                    scan_timestamp=opportunity.scan_timestamp
                ) for opportunity in opportunities
            ])
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_recent_opportunities(self, limit: int = 20) -> List[BountyOpportunity]:
        """Retrieves the most recently scanned opportunities."""
        session = self.Session()
        try:
            results = session.query(BountyOpportunityDB).order_by(BountyOpportunityDB.scan_timestamp.desc()).limit(limit).all()
            return [
                BountyOpportunity(
                    repository=result.repository,
                    issue_url=result.issue_url,
                    title=result.title,
                    comments=result.comments,
                    last_updated=result.last_updated,
                    bounty_tags=result.bounty_tags,
                    scan_timestamp=result.scan_timestamp
                ) for result in results
            ]
        finally:
            session.close()