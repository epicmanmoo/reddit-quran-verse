import json
import urllib.request
import praw
import random
import time


def check(my_red):
    for message in my_red.inbox.unread(limit=None):
        subject = message.subject.lower()
        print(subject)
        if subject == 'username mention' or subject == 'comment reply':
            ayah = message.body.split()
            print(ayah)
            eng_text = ""
            eng_data = ""
            arab_text = ""
            arab_data = ""
            try:
                if ayah[1] == 'random':
                    ayah_num = random.randrange(1, 6237)
                    eng_text = urllib.request.urlopen("http://api.alquran.cloud/v1/ayah/" + str(ayah_num) + "/en.asad")
                    eng_data = json.loads(eng_text.read().decode())
                    arab_text = urllib.request.urlopen("http://api.alquran.cloud/v1/ayah/" + str(ayah_num))
                    arab_data = json.loads(arab_text.read().decode())
                elif ":" in ayah[1]:
                    surah_verse = ayah[1].split(":")
                    surah = surah_verse[0]
                    verse = surah_verse[1]
                    eng_text = urllib.request.urlopen(
                        "http://api.alquran.cloud/v1/ayah/" + str(surah) + ':' + str(verse) + "/en.asad")
                    eng_data = json.loads(eng_text.read().decode())
                    arab_text = urllib.request.urlopen("http://api.alquran.cloud/v1/ayah/" + str(surah) + ':' + str(verse))
                    arab_data = json.loads(arab_text.read().decode())
                else:
                    eng_text = urllib.request.urlopen("http://api.alquran.cloud/v1/ayah/" + str(ayah[1]) + "/en.asad")
                    eng_data = json.loads(eng_text.read().decode())
                    arab_text = urllib.request.urlopen("http://api.alquran.cloud/v1/ayah/" + str(ayah[1]))
                    arab_data = json.loads(arab_text.read().decode())
                arname_of_surah = eng_data['data']['surah']['englishName']
                enname_of_surah = eng_data['data']['surah']['englishNameTranslation']
                en_c_text = 'English Text:\n\nSurah: ' + enname_of_surah + ': ' + eng_data['data']['text']
                ar_c_text = '\n\nArabic Text:\n\n' + '\u0633\u064f\u0648\u0631\u064e\u0629\u200e: ' + arname_of_surah + ': ' + \
                            arab_data['data']['text']
                surah_num = eng_data['data']['surah']['number']
                verse_num = eng_data['data']['numberInSurah']
                loc_text = ' (' + str(surah_num) + ':' + str(verse_num) + ')'
                final = en_c_text + ar_c_text + loc_text
                message.reply(final)
                message.mark_read()
            except Exception as e:
                print(e)
                return


while True:
    red_inst = praw.Reddit(private_info)
    check(red_inst)
    time.sleep(5)
