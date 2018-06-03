import re
import collections
import termextract.japanese_plaintext
import termextract.core
import MeCab
from datetime import datetime
from django.core.management.base import BaseCommand
from tecqii.models import Tag, User, Item, UserTagRelation, UserKeyword

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Running batch 'user_keyword' ... at: ",datetime.now() )
        mecab = MeCab.Tagger()

        # only those who have ever posted articles
        users = User.objects.filter(items_count__gte=1)
        for user in users:
            if not UserKeyword.objects.filter(user=user):
                print('user： ',user,' -----------------')
                items = Item.objects.filter(user=user).order_by('updated_at').reverse()[:19]
                text = ''
                for item in items:
                    # tell wheather Japanese or not for each character since termextract doesn't accept non Japanese.
                    # https://qiita.com/EastResident/items/0cdc7c5ac1f0a6b3cf1d

                    for char in item.body:
                        if re.findall('[ぁ-んァ-ン一-龠ー]' , char):
                            text += char
                        else:
                            text += '、' # still need to keep the splits in articles.
                    text = re.sub(r"、+", "、", text)

                    words = []
                    words_parsed = mecab.parse(text)
                    for row in words_parsed.split("\n"):
                        word = row.split("\t")[0]
                        if word == "EOS":
                            break
                        else:
                            pos = row.split("\t")[1].split(",")[0]
                            if pos == "名詞":
                                words.append(word)
                    text = '、'.join(words)


                print('文字列:', len(text))

                try:
                    frequency = termextract.japanese_plaintext.cmp_noun_dict(text)
                    LR = termextract.core.score_lr(frequency,
                                                   ignore_words=termextract.japanese_plaintext.IGNORE_WORDS,
                                                   lr_mode=1, average_rate=1
                                                   )
                    term_imp = termextract.core.term_importance(frequency, LR)
                    # 重要度が高い順に並べ替えて出力
                    data_collection = collections.Counter(term_imp)
                    counter = 0
                    for cmp_noun, value in data_collection.most_common():
                        cmp_noun = cmp_noun.replace(' ', '')
                        if len(cmp_noun) > 4:
                            print(termextract.core.modify_agglutinative_lang(cmp_noun), value, sep="\t")
                            UserKeyword.objects.update_or_create(
                                user=user,
                                keyword=cmp_noun,
                                defaults={
                                    'weight': value
                                }
                            )
                            counter += 1
                            if counter >= 50:
                                break
                except OverflowError:
                    print('OverflowError')
                    continue

        print('finished. at: ', datetime.now())
                    # frequency = termextract.japanese_plaintext.cmp_noun_dict(text)
                    # LR = termextract.core.score_lr(frequency,
                    #                                ignore_words=termextract.japanese_plaintext.IGNORE_WORDS,
                    #                                lr_mode=1, average_rate=1
                    #                                )
                #     term_imp = termextract.core.term_importance(frequency, LR)
                #     # 重要度が高い順に並べ替えて出力
                #     data_collection = collections.Counter(term_imp)
                #     counter = 0
                #     for cmp_noun, value in data_collection.most_common():
                #         cmp_noun = cmp_noun.replace(' ','')
                #         if len(cmp_noun) > 4:
                #             keywords.append([value, cmp_noun])
                #             counter += 1
                #             if counter > 50:
                #                 break
                #
                # keyword_counter = 0
                # keywords = sorted(keywords, reverse=True)
                # for keyword in keywords:
                #     print(keyword[1], keyword[0], sep="\t")
                #     result, success = UserKeyword.objects.update_or_create(
                #         user=user,
                #         keyword=keyword[1],
                #         defaults={
                #             'weight': keyword[0]
                #         }
                #     )
                #
                #     if success == True:
                #         keyword_counter += 1
                #         if keyword_counter > 50:
                #             break

