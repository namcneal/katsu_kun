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
		('ichidan', 'Ichidan'),
		('godan', 'Godan'),
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

class Conjugator():
	def __init__(self):
		self.string = ""
		self.type   = ""

	godan_endings = {'う':['わ','い','え'],
					 'く':['か','き','け'],
					 'ぐ':['が','ぎ','げ'],
					 'す':['さ','し','せ'],
					 'つ':['た','ち','て'],
					 'ぬ':['な','に','ね'],
					 'む':['ま','み','め'],
					 'ぶ':['ば','び','べ'],
					 'る':['ら','り','れ']}

	def set_verb(self, verb):
		self.string = verb.dictionary_string
		self.type   = verb.verb_type

	def potential(self):
		if self.type == 'ichidan':
			self.string = self.string[:-1] + "られる"
		elif self.type == 'godan':
			ending = self.string[-1]
			self.string = self.string[:-1] + godan_endings[ending][2] + "る"
		elif self.type == 'suru':
			pass
		elif self.type == 'kuru':
			pass
