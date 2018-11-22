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

		# A-Changes, i-Chances, e-Changes, Past Short Endings, Te form Endings
		self.godan_endings = {'う':['わ','い','え','った','って'],
							  'く':['か','き','け','いた','いて'],
							  'ぐ':['が','ぎ','げ','いだ','いで'],
							  'す':['さ','し','せ','した','して'],
							  'つ':['た','ち','て','った','って'],
							  'ぬ':['な','に','ね','んだ','んで'],
							  'む':['ま','み','め','んだ','んで'],
							  'ぶ':['ば','び','べ','んだ','んで'],
							  'る':['ら','り','れ','った','って']}

	def set_verb(self, verb):
		self.string = verb.dictionary_string
		self.type   = verb.verb_type

	def potential(self):
		if self.type == 'ichidan':
			self.string = self.string[:-1] + "られる"
		elif self.type == 'godan':
			ending = self.string[-1]
			self.string = self.string[:-1] + self.godan_endings[ending][2] + "る"
		elif self.type == 'suru':
			pass
		elif self.type == 'kuru':
			pass

		self.type = "ichidan"

	def passive(self):
		if self.type == 'ichidan':
			self.string = self.string[:-1] + "られる"
		elif self.type == 'godan':
			ending = self.string[-1]
			self.string = self.string[:-1] + self.godan_endings[ending][0] + "れる"
		elif self.type == 'suru':
			pass
		elif self.type == 'kuru':
			pass

		self.type = "ichidan"

	def causative(self):
		if self.type == 'ichidan':
			self.string = self.string[:-1] + "させる"
		elif self.type == 'godan':
			ending = self.string[-1]
			self.string = self.string[:-1] + self.godan_endings[ending][0] + "せる"
		elif self.type == 'suru':
			pass
		elif self.type == 'kuru':
			pass

		self.type = "ichidan"

	def causative_passive(self):
		if self.type == 'ichidan':
			self.string = self.string[:-1] + "させる"
		elif self.type == 'godan':
			ending = self.string[-1]
			self.string = self.string[:-1] + self.godan_endings[ending][0] + "せる"
		elif self.type == 'suru':
			pass
		elif self.type == 'kuru':
			pass

		self.type = "ichidan"

	def short(self, non_negative, non_past):
		if non_negative:
			if non_past:
				pass # Same as dictionary
			else:
				if self.type == "ichidan":
					self.string = self.string[:-1] + "た"
				elif self.type == "godan":
					ending = self.string[-1]
					self.string = self.string[:-1] + self.godan_endings[ending][3]
				elif self.type == "suru":
					pass
				elif self.string_type == "kuru":
					pass
		# Negative Short Forms
		else:
			if non_past:
				if self.type == "ichidan":
					self.string = self.string[:-1] + "ない"
				elif self.type == "godan":
					ending = self.string[-1]
					self.string = self.string[:-1] + self.godan_endings[ending][0] + "ない"
				elif self.type == "suru":
					pass
				elif self.string_type == "kuru":
					pass
			else:
				if self.type == "ichidan":
					self.string = self.string[:-1] + "なかった"
				elif self.type == "godan":
					ending = self.string[-1]
					self.string = self.string[:-1] + self.godan_endings[ending][0] + "なかった"
				elif self.type == "suru":
					pass
				elif self.string_type == "kuru":
					pass

	def masu(self, non_negative, non_past):
		if self.type == "ichidan":
			self.string = self.string[:-1]
		elif self.type == "godan":
			ending = self.string[-1]
			self.string = self.string[:-1] + self.godan_endings[ending][1]
		elif self.type == "suru":
			pass
		elif self.type == "kuru":
			pass

		if non_negative:
			if non_past:
				self.string += "ます"
			else:
				self.string += "ました"
		else:
			if non_past:
				self.string += "ません"
			else:
				self.string += "ませんでした"

	def te(self, non_negative):
		if non_negative:
			if self.type == "ichidan":
				self.string = self.string[:-1] + "て"
			elif self.type == "godan":
				ending = self.string[-1]
				self.string = self.string[:-1] + self.godan_endings[ending][4]
			elif self.type == "suru":
				pass
			elif self.type == "kuru":
				pass
		else:
			if self.type == "ichidan":
				self.string = self.string[:-1] + "なくて"
			elif self.type == "godan":
				ending = self.string[-1]
				self.string = self.string[:-1] + self.godan_endings[ending][0] + "なくて"
			elif self.type == "suru":
				pass
			elif self.type == "kuru":
				pass

	def tai(self, non_negative, non_past):
		if self.type == "ichidan":
			self.string = self.string[:-1]
		elif self.type == "godan":
			ending = self.string[-1]
			self.string = self.string[:-1] + self.godan_endings[ending][1]
		elif self.type == "suru":
			pass
		elif self.type == "kuru":
			pass

		if non_negative:
			if non_past:
				self.string += "たい"
			else:
				self.string += "たかった"
		else:
			if non_past:
				self.string += "たくない"
			else:
				self.string += "たくなかった"

	def tara(self, non_negative):
		if non_negative:
			if self.type == "ichidan":
				self.string = self.string[:-1] + "たら"
			elif self.type == "godan":
				ending = self.string[-1]
				self.string = self.string[:-1] + self.godan_endings[ending][3] + "ら"
			elif self.type == "suru":
				pass
			elif self.string_type == "kuru":
				pass
		# Negative Short Forms
		else:
			if self.type == "ichidan":
				self.string = self.string[:-1] + "なかったら"
			elif self.type == "godan":
				ending = self.string[-1]
				self.string = self.string[:-1] + self.godan_endings[ending][0] + "なかったら"
			elif self.type == "suru":
				pass
			elif self.string_type == "kuru":
				pass

	def ba(self, non_negative):
		if non_negative:
			if self.type == "ichidan":
				self.string = self.string[:-1] + "れば"
			elif self.type == "godan":
				ending = self.string[-1]
				self.string = self.string[:-1] + self.godan_endings[ending][2] + "ば"
			elif self.type == "suru":
				pass
			elif self.string_type == "kuru":
				pass
		# Negative Short Forms
		else:
			if self.type == "ichidan":
				self.string = self.string[:-1] + "なければ"
			elif self.type == "godan":
				ending = self.string[-1]
				self.string = self.string[:-1] + self.godan_endings[ending][0] + "なければ"
			elif self.type == "suru":
				pass
			elif self.string_type == "kuru":
				pass

	def __str__(self):
		kanji_string = ""
		split_verb = self.string.split(";")

		for n in range(len(split_verb)):
			# Handling the kanji, so we'll only grab one character
			if n < len(split_verb) -1: kanji_string += split_verb[n][0]

			# The last entry in the split verb is the okurigana
			else: kanji_string += split_verb[n]
		return kanji_string
