import os.path
import logging
import argparse

import pcpe2_core

class _Env(object):
    def __init__(self):
        self._temp_path = os.path.abspath(pcpe2_core.env_get_temp_path())
        self._buffer_size = pcpe2_core.env_get_buffer_size()
        self._io_buffer_size = pcpe2_core.env_get_io_buffer_size()
        self._output_min_len = pcpe2_core.env_get_min_output_length()
        self._compare_seq_size = pcpe2_core.env_get_compare_seq_size()
        self._thread_size = pcpe2_core.env_get_thread_size()

        if not os.path.isdir(self._temp_path):
            os.makedirs(self._temp_path)

    @property
    def temp_path(self):
        return self._temp_path

    @temp_path.setter
    def temp_path(self, path):
        self._temp_path = os.path.abspath(path)
        pcpe2_core.env_set_temp_path(self._temp_path)

        if not os.path.isdir(self._temp_path):
            os.makedirs(self._temp_path)

    @property
    def buffer_size(self):
        return self._buffer_size

    @buffer_size.setter
    def buffer_size(self, set_size):
        self._buffer_size = set_size
        pcpe2_core.env_set_buffer_size(self._buffer_size)

    @property
    def io_buffer_size(self):
        return self._io_buffer_size

    @io_buffer_size.setter
    def io_buffer_size(self, set_size):
        self._io_buffer_size = set_size
        pcpe2_core.env_set_io_buffer_size(self._io_buffer_size)

    @property
    def output_min_len(self):
        return self._output_min_len

    @output_min_len.setter
    def output_min_len(self, set_size):
        self._output_min_len = set_size
        pcpe2_core.env_set_min_output_length(self._output_min_len)

    @property
    def compare_seq_size(self):
        return self._compare_seq_size

    @compare_seq_size.setter
    def compare_seq_size(self, set_size):
        self._compare_seq_size = set_size
        pcpe2_core.env_set_compare_seq_size(self._compare_seq_size)

    @property
    def thread_size(self):
        return self._thread_size

    @thread_size.setter
    def thread_size(self, set_size):
        self._thread_size = set_size
        pcpe2_core.env_set_thread_size(self._thread_size)


_env_instance = None
def env():
    global _env_instance
    if _env_instance is not None:
        return _env_instance
    else:
        _env_instance = _Env()
        return _env_instance


def init_logging(*, log_path=None, level=logging.WARNING):
    # Set logging format string
    if level <= logging.DEBUG:
        format_str = "[%(levelname)s:%(filename)s:%(lineno)d]: %(message)s"
    else:
        format_str = "[%(levelname)s]: %(message)s"

    # Apply the setting
    logging.basicConfig(filename=None, level=level, format=format_str)
    pcpe2_core.init_logging(level)


def parse_command_args(sys_argv):
    setting = dict()
    return setting


def init_env(sys_argv):
    """
    Read command argument and init the program environment.

    The function inits all environment variables  and reurn the input and
    output paths.

    Args:
        sys_argv ([str]): the command line arguments

    Return:
        a dict to present the input/ output paths which are needed.

        key                  value      meaning
        "x_input_path"       str        input file path
        "y_input_path"       str        input file path
        "output_path"        str        output file path
        "output_human_path"  str        output human-redable file path.
                                        The value could be None
    """
    setting = parse_command_args(sys_argv)
    init_logging(level=logging.DEBUG)

    env().output_min_len = 7

    program_path = dict()
    program_path['x_input_path']       = "./test/testdata/read_fasta/test1.txt"
    program_path['y_input_path']       = "./test/testdata/read_fasta/test2.txt"
    program_path['output_path']        = "./output_test.txt"
    program_path['output_human_path']  = "./output_test_human.txt"

    return program_path
