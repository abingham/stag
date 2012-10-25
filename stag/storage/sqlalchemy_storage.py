import logging

from sqlalchemy import (Column,
                        create_engine,
                        Integer,
                        String)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

log = logging.getLogger(__file__)

Base = declarative_base()

class Definition(Base):
    __tablename__ = 'definitions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    filename = Column(String)
    lineno = Column(Integer)

    def __repr__(self):
        return '<Definition("{}", "{}", "{}")>'.format(
            self.name, self.filename, self.lineno)

class Reference(Base):
    __tablename__ = 'references'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    filename = Column(String)
    lineno = Column(String)

    def __repr__(self):
        return '<Reference("{}", "{}", "{}")>'.format(
            self.name, self.filename, self.lineno)

class SqlAlchemyStorage:
    def __init__(self, filename):
        self.filename = filename
        self.session = None

    def connect(self):
        engine = create_engine('sqlite:///{}'.format(self.filename))
        metadata = Base.metadata
        metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()

    def close(self):
        self.session.commit()

    def clear_defs(self):
        for d in self.session.query(Definition).all():
            self.session.delete(d)

    def add_def(self, name, filename, lineno):
        log.info(
            'SqlAlchemyStorage.add_def(name={}, filename={}, lineno={})'.format(
                name, filename, lineno))

        self.session.add(
            Definition(
                name=name,
                filename=filename,
                lineno=lineno))

    def definitions(self):
        for d in self.session.query(Definition).all():
            yield (d.name, d.filename, d.lineno)

    def find_definitions(self, name):
        for d in self.session.query(Definition).filter_by(name=name):
            yield (d.name, d.filename, d.lineno)

    def add_ref(self, name, filename, lineno):
        log.info(
            'SqlAlchemyStorage.add_def(name={}, filename={}, lineno={})'.format(
                name, filename, lineno))

        self.session.add(
            References(
                name=name,
                filename=filename,
                lineno=lineno))

    def references(self):
        for r in self.session.query(Reference).all():
            yield (r.name, r.filename, r.lineno)

    def find_references(self, name):
        for r in self.session.query(Reference).filter_by(name=name):
            yield (r.name, r.filename, r.lineno)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, t, v, tb):
        self.close()
