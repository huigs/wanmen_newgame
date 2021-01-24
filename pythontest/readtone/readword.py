from subprocess import call
from time import sleep

hiragana = {
'1':'one',
'2':'two',
'3':'three',
}

for word in hiragana:
    sleep(2.5)
    call(['say',hiragana[word]])
    sleep(2.5)
    call(['say',hiragana[word]])