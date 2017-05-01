"""
Read/ Parse Fasta file module

The module supports read fasta file and save to related data structures.
"""
import collections

class SeqFile(object):
    def __init__(self, fasta_path):
        self._fasta_path = ""
        self._seq_path = ""
        self._id_path = ""
        self._id_info_path = ""

    @staticmethod
    def parse_seqfile(seqfile):
        create_seq_id_file(seqfile.seq_path, seqfile.seq_path, seqfile.id_path)
        create_id_info_file(seqfile.seq_path, seqfile.id_info_path)

    def seq_path():
        doc = "The seq_path property."
        def fget(self):
            return self._seq_path
        return locals()
    seq_path = property(**seq_path())

    def id_path():
        doc = "The fasta_id_path property."
        def fget(self):
            return self._id_path
        return locals()
    fasta_id_path = property(**id_path())

    def id_info_path():
        doc = "The fasta_id_info property."
        def fget(self):
            return self.id_info_path
        return locals()
    fasta_id_info = property(**id_info_path())


SeqInfo = collections.namedtuple('SeqInfo', ['seq', 'ids'])


class SeqFileInfo(object):
    def __init__(self, seq_file):
        self._seq_file = seq_file
        self._seq_info = list()
        self._id_info = dict()

    def get_seq_info(self, index):
        return self._seq_info[index]

    def get_id_info(self, fasta_id):
        return self._id_info[fasta_id]


def retrieve_fasta_id(id_line):
    """
    Parse fasta first line to get the fasta id.

    Return:
        id (str)
    """
    return id_line.split('|')[1]


def read_fasta_file(path):
    """
    Generator function for reading fasta file.

    Returns:
        info: the first line of the sequences
        seq: the main body of the sequence
    """
    id_line = ""
    seq = ""

    with open(path, 'r') as fin:
        for line in fin:
            if line.startswith('>'):
                if id_line and seq:
                    # Yield the previous one
                    yield id_line, seq
                id_line = line.strip()
                seq = ""
            else:
                seq += line.strip()

    if id_line and seq:
        yield id_line.strip(), seq.strip()


def create_id_info_file(fasta_path, info_path):
    """
    Parse fasta file to make a fasta id information file.

    The output file format is as the following.

        [FASTA ID_0] [INFO_0]
        [FASTA ID_1] [INFO_1]
        ...
        [FASTA ID_n] [INFO_n]

    Args:
        fasta_path (str): The input fasta file
        info_path (str): The output fasta information file.
    """
    with open(info_path, 'w') as fout:
        for info, _ in read_fasta_file(fasta_path):
            fasta_id = retrieve_fasta_id(info)

            fout.write(" ".join([fasta_id, info]) + "\n")


def create_seq_id_file(fasta_path, seq_path, id_path):
    """
    Parse fasta file to make a unique sequence file and a id mapping file.

    The seq file format is as the following

        [number of seqs]
        [len_0] [seq_0]
        [len_1] [seq_1]
        ...
        [len_n] [seq_n]

    The id file format is as the following

        [number of seqs]
        [size_m0] [id_0_0] [id_0_1] ... [id_0_m0]
        [size_m1] [id_1_0] [id_1_1] ... [id_1_m1]
        ...
        [size_mn] [id_n_0] [id_n_1] ... [id_n_mn]

    The seq file and id file is line-to-line mapping. It means the seq has
    one or several fasta ids in the same line number of id file.

    Args:
        fasta_path (str): The input fasta file
        seq_path (str): The output seqeunce file.
        id_path (str): The output id mapping file.
    """
    seq_ids = dict()

    for info, seq in read_fasta_file(fasta_path):
        fasta_id = retrieve_fasta_id(info)
        seq_ids.setdefault(seq, []).append(fasta_id)

    with open(seq_path, 'w') as f_seq, open(id_path, 'w') as f_id:
        f_seq.write(str(len(seq_ids)) + "\n")
        f_id.write(str(len(seq_ids)) + "\n")

        for seq, ids in seq_ids.items():
            f_seq.write(" ".join([str(len(seq)), seq]) + "\n")

            write_ids = [len(ids)] + ids
            f_id.write(" ".join([str(i) for i in write_ids]) + "\n")


def create_seq_file(path):
    sf = SeqFile(path)
    SeqFile.parse_seqfile(sf)

    return sf
