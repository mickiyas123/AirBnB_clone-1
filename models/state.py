#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete", backref='state')

    @property
    def cities(self):
        """Returns the list of City instances with
        state_id equals to the current State.id
        """
        from models import storage
        from models import City

        city_list = []

        all_cities = storage.all(City)

        for key, val in all_cities.items():
            if val['state_id'] == self.id:
                city_list.append(val)
        return city_list
