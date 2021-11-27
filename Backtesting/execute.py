from model_dt import ModelDT
from model_knn import ModelKNN
from model_dt import ModelDT
from train import *
from simulator import *

def execute(m, sn, s, e, mn):
    if m=='KNN':
        model = ModelKNN()
    elif m=='DT':
        model = ModelDT()


    call(model, sn)
    d, f1, f2, f3, f4, f5, f6 = execute_s(sn, s, e, mn)
    print(d)
    return d, f1, f2, f3, f4, f5, f6


if __name__ == '__main__':
    start_date = datetime.date(2015, 1, 1)
    end_date = datetime.date(2020, 1, 1)
    sn = "AAPL"
    d = execute('KNN', sn, start_date, end_date, 10000)