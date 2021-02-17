# Chaplianskaya, Czyżkowski
# W14 W21
import numpy
import arrow


class HashTable:
    def __init__(self, k, n):
        self.H = numpy.full(shape=(k, n), fill_value=None)
        self.K = k
        self.N = n

    def __str__(self):
        column_str = str()
        for row_index in range(len(self.H)):
            row_str = f"{row_index+1}.  "
            for column in self.H[row_index]:
                if column is None:
                    continue
                else:
                    row_str += f"[{column}], "
            column_str += row_str[:-2] + '\n'
        return column_str

    def get_hash(self, arg):
        # in order to stop single character strings going into the same category
        value = 1 if len(arg) == 0 else ord(arg[0])
        for i in range(len(arg)):
            value *= (ord(arg[i]) / 10 + i)
        return int(value) % self.K

    def insert_value(self, arg):
        k = self.get_hash(arg)
        for index in range(self.N):
            if self.H[k][index] == arg:  # the value is already in the table
                return
            if self.H[k][index] is None:
                self.H[k][index] = arg
                return
        raise Exception(f"N = {self.N} is not big enough to fit next argument: {arg}")

    def remove_value(self, arg):
        k = self.get_hash(arg)
        if arg not in self.H[k]:
            return
        for index in range(self.N):
            if self.H[k][index] == arg:
                for inner_index in range(index, self.N - 1, 1):
                    if self.H[k][inner_index] is None:
                        return
                    else:
                        self.H[k][inner_index] = self.H[k][inner_index + 1]
                self.H[k][self.N - 1] = None

    def enumerate_time(self):
        start_time = arrow.utcnow()
        print(self)
        end_time = arrow.utcnow()
        return (end_time - start_time).total_seconds()

