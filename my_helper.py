from ujson import loads
import pyautogui
import speech_recognition as sr
from subprocess import Popen, PIPE
from re import search


def run(comand):
    comand = comand.split(' ')
    print(comand)
    Popen(comand, close_fds=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)


def split_query(arr, b):
    text = ''

    for i in range(len(arr)):
        if i > b:
            text += arr[i] + '+'

    return text[:-1]


def process(sayed):
    word = sayed.split(' ')

    if word[0] != 'asus':
        return

    print(sayed)

    if search('закр(ой|ыть) иначе', sayed):
        pyautogui.hotkey('ctrl', 'q')

    elif 'новая вкладка' in sayed:
        pyautogui.hotkey('ctrl', 't')

    elif search('верн(и|уть) вкладку', sayed):
        pyautogui.hotkey('ctrl', 'shift', 't')

    elif 'новое окно' in sayed:
        pyautogui.hotkey('ctrl', 'n')

    elif 'найди фильм' in sayed:
        query = split_query(word, 2)

        run(_run['браузер'] +
            ' http://gidonline.in/?s=' + query + '&submit=Поиск')

    elif 'найди песню' in sayed:
        query = split_query(word, 2)

        run(_run['браузер'] + ' https://soundcloud.com/search?q=' + query)

    elif search('най(д|т)и в (ютубе|youtube)', sayed):
        query = split_query(word, 3)

        run(_run['браузер'] +
            ' https://www.youtube.com/results?search_query=' + query)

    elif search('най(д|т)и', word[1]):
        query = split_query(word, 1)

        run(_run['браузер'] + ' https://www.google.com/search?q=' +
            query + '&ie=utf-8&oe=utf-8')

    elif search('(откр(ой|ыть)|запуст(ить|и))', word[1]):
        run(_run[word[2]])

    elif word[1] == 'назад':
        pyautogui.hotkey('esc')

    elif word[1] == 'убей':
        run('killall ' + _run[word[2]])

    elif search('закр(ой|ыть)', word[1]):
        pyautogui.hotkey('ctrl', 'w')

    elif word[1] == 'ок':
        pyautogui.hotkey('enter')

    elif search('верн(уть|и)', word[1]):
        pyautogui.hotkey('ctrl', 'y')

    elif word[1] == 'отмен(ить|и)':
        pyautogui.hotkey('ctrl', 'z')

    elif word[1] == 'прощай':
        exit(0)


if __name__ == "__main__":
    with open('ru_open.json', 'r', encoding='utf-8') as r:
        _run = loads(r.read())

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=3)

    while True:
        print("Free")

        with microphone as source:
            audio = recognizer.listen(source)

        print("Busy")

        try:
            sayed = recognizer.recognize_google(audio, language="ru-RU")
            sayed = sayed.lower()
            process(sayed)
        except SystemExit:
            break
        except:
            pass
