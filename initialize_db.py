from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
db_path = 'sqlite:///card_game.db'
engine = create_engine(db_path)

#lien du tuto: https://www.youtube.com/watch?v=g0-7TrVCNtg&ab_channel=SimpleTech   a voir sa video sur les migration

try:
    # create database
    Base.metadata.create_all(bind=engine)
    # create session
   # Session = sessionmaker(bind=engine)
    # create session instance
    #session = Session()
    #create new objet in db for test
    #rarity_legendary = Rarity(name='legendary')
    # equivalent au persist de doctrine
    #session.add(rarity_legendary)
    #equivalent au flush de doctrine
    #session.commit()

    #rarity_db = session.query(Rarity).filter(Rarity.name == 'legendary').first()
    #print(f" rareté trouvé: {rarity_db.name}")
    #print("Success !!!")
except Exception as ex:
    print(ex)
