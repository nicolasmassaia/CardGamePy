from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, Enum, func
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()


class SexeEnum(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"


class TimestampMixin:
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime)


class GeneralProfil(Base):
    __tablename__ = 'general_profils'
    profils_id = Column(Integer, ForeignKey('profils.id'), primary_key=True)
    general_id = Column(Integer, ForeignKey('generals.id'), primary_key=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)


class Edition(TimestampMixin, Base):
    __tablename__ = 'editions'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    image = Column(String)
    cards = relationship("Card", backref="edition")


class General(TimestampMixin, Base):
    __tablename__ = 'generals'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    effect_id = Column(Integer, ForeignKey('effects.id'))
    effect = relationship("Effect", backref="general")
    profils = relationship("Profil", secondary='general_profils', backref="generals")
    decks = relationship("Deck", backref="general")


class User(TimestampMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    profils = relationship("Profil", backref="user")


class Profil(TimestampMixin, Base):
    __tablename__ = 'profils'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    image = Column(String)
    birthday = Column(DateTime)
    sexe = Column(Enum(SexeEnum), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    decks = relationship("Deck", backref="profil")
    generals = relationship("General", secondary='general_profils', backref="profils")
    cards = relationship("Card", secondary="profil_cards")


class Deck(TimestampMixin, Base):
    __tablename__ = 'decks'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    profil_id = Column(Integer, ForeignKey('profils.id'))
    general_id = Column(Integer, ForeignKey('generals.id'))
    profil = relationship("Profil", backref="decks")
    general = relationship("General", backref="decks")
    cards = relationship("Card", secondary="deck_cards")


class Card(TimestampMixin, Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey('card_type.id'))
    description = Column(Text)
    attack = Column(Integer)
    defense = Column(Integer)
    edition_id = Column(Integer, ForeignKey('editions.id'))
    edition = relationship("Edition", backref="cards")
    type = relationship("CardType", backref="cards")
    effects = relationship("Effect", secondary="card_effects")
    costs = relationship("Cost", backref="card")


class Cost(TimestampMixin, Base):
    __tablename__ = 'costs'
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    resource_id = Column(Integer, ForeignKey('resource_types.id'))  # Corrected table name
    card_id = Column(Integer, ForeignKey('cards.id'))
    resource = relationship("ResourceType", backref="costs")
    card = relationship("Card", backref="costs")  # Each cost is linked to a single card


class ResourceType(TimestampMixin, Base):
    __tablename__ = 'resource_types'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    costs = relationship("Cost", backref="resource")


class CardType(TimestampMixin, Base):
    __tablename__ = 'card_type'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    cards = relationship("Card", backref="type")


class Effect(TimestampMixin, Base):
    __tablename__ = 'effects'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    function_name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String)
    user = relationship("User")
    general = relationship("General", backref="effect")
    cards = relationship("Card", secondary="card_effects")


# Association Table for many-to-many relationship between Cards and Effects
card_effects = Table(
    'card_effects',
    Base.metadata,
    Column('card_id', Integer, ForeignKey('cards.id'), primary_key=True),
    Column('effect_id', Integer, ForeignKey('effects.id'), primary_key=True)
)

# Association Table for many-to-many relationship between Decks and Cards
deck_cards = Table(
    'deck_cards',
    Base.metadata,
    Column('deck_id', Integer, ForeignKey('decks.id'), primary_key=True),
    Column('card_id', Integer, ForeignKey('cards.id'), primary_key=True)
)

# Association Table for many-to-many relationship between Profils and Cards
profil_cards = Table(
    'profil_cards',
    Base.metadata,
    Column('profil_id', Integer, ForeignKey('profils.id'), primary_key=True),
    Column('card_id', Integer, ForeignKey('cards.id'), primary_key=True)
)
