from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#  Veritabanı Dosyasının Adını ve Konumunu Belirleme
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# SQLAlchemy "Motorunu" Oluşturma
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} 
)

# Veritabanına "Oturum" (Session) Açmak İçin Kalıp Oluşturma
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modellerimizin Miras Alacağı Base Sınıfını Tekrar Tanımlama

Base = declarative_base()