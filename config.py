from jogoteca import app
import os


SECRET_KEY = "alumais"  #era assim essa parte do codigo: => app.secret_key = "alumais"

                #era assim essa parte do codigo: =>         app.config"SQLALCHEMY_DATABASE_URI"

SQLALCHEMY_DATABASE_URI = "{SGBD}://{usuario}:{senha}@{servidor}/{database}".format(SGBD = "mysql+mysqlconnector",usuario = "root",senha = "96465840Mt?", servidor = "localhost",database = "jogoteca")

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + "/uploads"