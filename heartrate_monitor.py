
from max30102 import MAX30102
import hrcalc
import threading
import time
import numpy as np


LOOP_TIME = 0.1


def run_sensor():
    sensor = MAX30102()
    bpm_ = 0
    spo2_ = 0
    ir_data = []
    red_data = []
    bpms = []
    spo2s = []

    results = []
    # run until told to stop
    for i in range(150):
        # check if any data is available
        num_bytes = sensor.get_data_present()
        if num_bytes > 0:
            # grab all the data and stash it into arrays
            while num_bytes > 0:
                red, ir = sensor.read_fifo()
                num_bytes -= 1
                ir_data.append(ir)
                red_data.append(red)

            while len(ir_data) > 100:
                ir_data.pop(0)
                red_data.pop(0)

            if len(ir_data) == 100:
                bpm, valid_bpm, spo2, valid_spo2 = hrcalc.calc_hr_and_spo2(ir_data, red_data)
                if valid_bpm:
                    bpms.append(bpm)
                    if len(bpms) > 4:
                        bpms.pop(0)
                    bpm_ = np.mean(bpms)
                if valid_spo2:
                    spo2s.append(spo2)
                    if len(spo2s) >4:
                        spo2s.pop(0)
                    spo2_ = np.mean(spo2)

                if (np.mean(ir_data) < 50000 and np.mean(red_data) < 50000):
                    bpm_ = 0
                    spo2_ = 0

                results.append(spo2_)
                print("BPM: {0}, SpO2: {1}".format(bpm_, spo2_))

        time.sleep(LOOP_TIME)

    sensor.shutdown()
    return results


if __name__ == '__main__':
    results = run_sensor()
    print(results)
    print(len(results))