import time
import csv
import threading
import pyautogui
from pynput.keyboard    import Key, Listener

def main():
    with Listener(on_press=KeyLogger.on_press, on_release=KeyLogger.on_release) as listener:
        listener.join()

class KeyLogger:
    press = {}
    timer = []
    start = time.time()

    def threadKeyboard(key,releaseTime):
        ok2 = time.perf_counter()
        pyautogui.keyDown(key)
        time.sleep(float(releaseTime))
        pyautogui.keyUp(key)
        time.sleep(time.perf_counter() - ok2 - float(releaseTime))

    def replay():

        latestTime = 0
        x = 0
        with open('C:\\Users\\koryouz\\Documents\\kori\\greatkeylog\\keysTimer.csv', 'r') as csvfile:
            keyTimer_reader = csv.reader(csvfile)
            rowsTimer = list(keyTimer_reader)

            for lines in rowsTimer:
                if lines != []:
                    ok = time.perf_counter()
                    time.sleep(float(lines[2]) - latestTime)

                    key = lines[0].replace('\'', '')
                    releaseTime = lines[1]

                    threadName = 't' + str(x)
                    time.sleep(time.perf_counter() - ok - (float(lines[2]) - latestTime))

                    threadName = threading.Thread(target=KeyLogger.threadKeyboard,args=(key,releaseTime)).start()


                    ok3 = time.perf_counter()
                    latestTime = float(lines[2])
                    x = x + 1
                    time.sleep(time.perf_counter() - ok3)

    def dif_time():
        return time.time() - KeyLogger.start

    def on_press(key):
        if key not in KeyLogger.press:
            KeyLogger.press[key] = KeyLogger.dif_time()

    def on_release(key):
        if str(key) == "'*'":
            KeyLogger.csv()
            exit()

        if str(key) == "'-'":
            KeyLogger.replay()
            exit()

        if key in KeyLogger.press:
            KeyLogger.press[key] - KeyLogger.dif_time()
            KeyLogger.timer.append([key, KeyLogger.dif_time() - KeyLogger.press[key], KeyLogger.press[key]])
            KeyLogger.press.pop(key)

    def csv():
        KeyLogger.timer.sort(key=lambda entry:entry[2])

        with open('C:\\Users\\koryouz\\Documents\\kori\\greatkeylog\\keysTimer.csv', 'w') as csvfile:
            keyTimer_writer = csv.writer(csvfile)
            for entry in KeyLogger.timer:
                keyTimer_writer.writerow(entry)


if __name__ == '__main__':
    main()
