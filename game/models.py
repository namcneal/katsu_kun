from django.db import models

# Create your models here.
"""
Explanation of Formats

*The Dictionary String:
    * Each kanji in the verb should be followed by a comma and have the furigana come after itself.
      After each furigana, separate that kanji-furigana pair with a semi-colonself.
      In this way, each kanji is contained as a unit with its pronunciationself.
    * Examples:
        * "出,で;来,き;る"
        * "泳,およ;ぐ"
        * "連,つ;れてくる"
        * "運,うん;転,てん;する"
        * "待,ま;つ"
"""
class Verb(models.Model):
    VERB_TYPES = (
        ('godan', 'Godan'),
        ('ichidan', 'Ichidan'),
        ('suru', '~Suru'),
        ('kuru', '~Kuru')
    )

    dictionary_string = models.CharField(max_length = 30)
    translation = models.CharField(max_length = 50)
    verb_type   = models.CharField(max_length = 10, choices=VERB_TYPES)
    genki_chapter = models.PositiveSmallIntegerField()

    def __str__(self):
        kanji_string = ""
        split_verb = self.dictionary_string.split(";")

        for n in range(len(split_verb)):
            # Handling the kanji, so we'll only grab one character
            if n < len(split_verb) -1: kanji_string += split_verb[n][0]

            # The last entry in the split verb is the okurigana
            else: kanji_string += split_verb[n]
        return kanji_string

class UserAttempt(models.Model):
    managed = False
    submitted_attempt = models.CharField(max_length = 30)

    def __unicode__(self):
        return sumitted_attempt
