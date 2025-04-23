from src.Database.Database import Database
from src.models.ModelPlay import ModelPlay
from src.repositories.DataRepository import DataRepository
from src.repositories.RequestTable import RequestTable
from src.services.ServiceTable import app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
