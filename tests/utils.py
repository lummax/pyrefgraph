# coding=utf-8

import functools
import multiprocessing
import sys
import traceback


def isolated(function):
    def wrapper(queue, *args, **kwargs):
        try:
            (result, error) = (function(*args, **kwargs), None)
        except Exception:
            (ex_type, ex_value, tb) = sys.exc_info()
            (result, error) = (
                None,
                (ex_type, ex_value, "".join(traceback.format_tb(tb))),
            )
        queue.put((result, error))

    @functools.wraps(function)
    def runner(*args, **kwargs):
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(
            target=wrapper, args=(queue,) + args, kwargs=kwargs
        )
        process.start()
        (result, error) = queue.get()
        process.join()

        if error:
            (ex_type, ex_value, tb_str) = error
            raise ex_type("{} (in subprocess)\n{}".format(ex_value, tb_str))

        return result

    return runner
