import pandas as pd

from src.controller.FutebolController import app
from src.services.DataFrameTable import DataFrameTable
from src.services.ServiceTable import ServiceTable

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
