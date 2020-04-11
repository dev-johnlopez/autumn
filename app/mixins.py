from flask import g
from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from transitions import Machine
from flask_security import current_user


class AuditMixin(object):
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @declared_attr
    def created_by_id(cls):
        return Column(Integer,
                      ForeignKey('user.id',
                                 name='fk_%s_created_by_id'
                                 % cls.__name__, use_alter=True),
                      default=_current_user_id_or_none
                      )

    @declared_attr
    def created_by(cls):
        return relationship(
            'User',
            primaryjoin='User.id == %s.created_by_id' % cls.__name__,
            remote_side='User.id'
        )

    @declared_attr
    def updated_by_id(cls):
        return Column(Integer,
                      ForeignKey('user.id',
                                 name='fk_%s_updated_by_id' % cls.__name__,
                                      use_alter=True),
                      default=_current_user_id_or_none,
                      onupdate=_current_user_id_or_none)

    @declared_attr
    def updated_by(cls):
        return relationship(
            'User',
            primaryjoin='User.id == %s.updated_by_id' % cls.__name__,
            remote_side='User.id'
        )


def _current_user_id_or_none():
    create_user_id = None
    try:
        return g.user.id
    except Exception as e:
        pass
    try:
        return current_user.id
    except Exception as e:
        pass
    return None


class ClaimStateMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def status(cls):
        return Column(String())

    @property
    def state(self):
        return self.status

    @state.setter
    def state(self, value):
        if self.status != value:
            self.status = value

    def after_state_change(self):
        db.session.add(self)

    @classmethod
    def init_state_machine(cls, obj, *args, **kwargs):
        states = ['Draft', 'Open', 'Closed']
        transitions = [
            ['open', '*', 'Open'],
            ['close', '*', 'Closed']
        ]

        initial = obj.status or states[0]

        machine = Machine(model=obj, states=states, transitions=transitions,
                          initial=initial,
                          after_state_change='after_state_change')

        # in case that we need to have machine obj in model obj
        setattr(obj, 'machine', machine)
