import pygatt

import logging
logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)

def handleData(handle, value):
    if len(value) == 2:
        pressure = str(value[1])
        print('PRESSURE {} mmHg'.format(pressure))

    if len(value) == 18:
        sysHigh, sysLow = value[1] << 8, value[2] & 0xFF
        sys = str(sysHigh | sysLow)
        diaHigh, diaLow = value[3] << 8, value[4] & 0xFF
        dia = str(diaHigh | diaLow)
        pulseHigh, pulseLow = value[7] << 8, value[8] & 0xFF
        pulse = str(pulseHigh | pulseLow)

        print('SYS {} mmHg , DIA {} mmHg , PULSE {} / minutes'.format(sys, dia, pulse))

try:
    adapter = pygatt.GATTToolBackend(hci_device='hci0')
    adapter.start()

    for discover in adapter.scan(run_as_root=True, timeout=5):
        if discover['name'] == 'BPM_01':
            try:
                print('Device found, try to connect with device')
                device = adapter.connect(discover['address'])
                print('Connected with device')
                                
                while True:
                    device.subscribe('0000fff4-0000-1000-8000-00805f9b34fb', callback=handleData)

            except KeyboardInterrupt:
                print('Terminate')
            except:
                print('Failed to connect with device')
            finally:
                device.disconnect()
                
except KeyboardInterrupt:
    print('Terminate')
except:
    print('Something went wrong with adapter')
finally:
    adapter.stop()