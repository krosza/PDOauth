from end2endtest.config import Config as IntegrationTestConfig

class Config(IntegrationTestConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
BASE_URL = Config.BASE_URL
