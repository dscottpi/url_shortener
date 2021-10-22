from time import time

class Snowflake():
    sequence_bits: int = 12
    worker_bits: int = 5
    data_center_bits: int  = 5
    timestamp_bits: int = 41
    sign_bits: int = 1
    # (1 << worker_bits) is the same as 2**5 = 32.
    # 32 in binary is 100000 which is 6 bits. 
    # so the max id of a worker id (which can only be 5 bits) is 31
    # if worker_bits was 6 then the max id would be 63
    max_worker_id = (1 << worker_bits) - 1
    max_data_center_id = (1 << data_center_bits) - 1
    max_sequence_bits = (1 << sequence_bits) - 1

    worker_bits_shift = sequence_bits
    data_center_shift = worker_bits + sequence_bits
    timestamp_shift = data_center_bits + worker_bits + sequence_bits
    sign_shift = timestamp_bits + data_center_bits + worker_bits + sequence_bits

    epoch = 1325376000000

    worker_id: int
    data_center_id: int
    last_timestamp: int = 0
    sequence: int

    def __init__(self, worker_id: int = 0, data_center_id: int = 0) -> None:
        if worker_id > self.max_worker_id or worker_id < 0:
           raise Exception("Invalid worker_id %d" % worker_id)
        
        if data_center_id > self.max_data_center_id or data_center_id < 0:
            raise Exception("Invalid data_center_id %d" % data_center_id)

        self.data_center_id = data_center_id
        self.worker_id = worker_id 

    def _custom_timestamp(self):
        return int(time() * 1000) - self.epoch

    def mint_id(self) -> int:
        timestamp = self._custom_timestamp()
        if timestamp != self.last_timestamp:
            if timestamp < self.last_timestamp:
               raise Exception("Clock has moved backwards")
           
            if timestamp < 0:
               raise Exception("Clock is before epoch")

            self.sequence = 0
            self.last_timestamp = timestamp
        else:
            self.sequence += 1
            if self.sequence > self.max_sequence_bits:
                raise Exception("Max sequence exceeded")

        return ((self.last_timestamp << self.timestamp_shift) 
                    | (self.data_center_id << self.data_center_shift)
                    | (self.worker_id << self.worker_bits_shift)
                    | self.sequence)