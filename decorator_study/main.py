import time
import array
import numpy
import pickle

def logging_time(original_fn):
    def wrapper_fn(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()
        print("WorkingTime[{}]: {} sec".format(original_fn.__name__, end_time-start_time))
        return result
    return wrapper_fn



@logging_time
def fun_list(): # python list
    list_ = [i for i in range(50000000)]
    return pickle.dumps(list_)

@logging_time
def fun_array(): # c언어 array
    array_ = array.array('i', range(50000000))
    return pickle.dumps(array_)

@logging_time
def fun_numpy(): # numpy array
    numpy_ = numpy.arange(50000000)
    return pickle.dumps(numpy_)



if __name__ == "__main__":
    fun_list()
    fun_array()
    fun_numpy()