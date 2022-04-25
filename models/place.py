#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import (
        Column,
        String,
        Integer,
        ForeignKey,
        Float,
        Table)
from sqlalchemy.orm import relationship

place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column(
            'place_id',
            String(60),
            ForeignKey('places.id'),
            primary_key=True,
            nullable=False),
        Column(
            'amenity_id',
            String(60),
            ForeignKey('amenities.id'),
            primary_key=True,
            nullable=False)
        )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    reviews = relationship("Review", cascade="all, delete", backref='place')
    amenities = relationship(
            'Amenity',
            secondary=place_amenity,
            viewonly=False,
            backref='place')

    @property
    def amenities(self):
        """Getter method that returns the list of Amenity
           instances based on the attribute amenity_ids that
           contains all Amenity.id linked to the Place
        """
        from models import storage
        from models import Amenity


        amenity_list = []

        all_amenities = storage.all(Amenity)

        for key, val in all_amenities.items():
            if val['amenity_id'] in self.amenity_ids:
                amenity_list.append(val)

        return amenity_list

    @amenities.setter
    def amenities(self, obj):
        """Setter method for amenities that handles append method
           for adding an Amenity.id to the attribute amenity_ids
        """
        from models import Amenity

        if isinstance(obj, Amenity):
            Place.amenity_ids.append(obj.id)
        else:
            pass

    @property
    def reviews(self):
        """Getter method that returns the list of Review
           instances with place_id equals to the current Place.id
        """
        from models import storage
        from models import Review

        review_list = []

        all_reviews = storage.all(Review)

        for key, val in all_reviews.items():
            if val['place_id'] == self.id:
                reviews_list.append(val)
        return reviews_list
