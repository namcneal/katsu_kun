from django.db import models
from random import seed, randrange

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

		for substring in split_verb:
			if "," in substring:
				# Split the substring based on comma and take only the first part
				kanji_string += substring.split(",")[0]
			else:
				kanji_string += substring

		return kanji_string

class Conjugator(object):
	def __init__(self):
		self.string = ""
		self.original = ""
		self.translation = ""
		self.type   = ""

		# A-Changes, i-Chances, e-Changes, Ta Endings, Te form Endings
		self.godan_endings = {'う':['わ','い','え','った','って'],
							  'く':['か','き','け','いた','いて'],
							  'ぐ':['が','ぎ','げ','いだ','いで'],
							  'す':['さ','し','せ','した','して'],
							  'つ':['た','ち','て','った','って'],
							  'ぬ':['な','に','ね','んだ','んで'],
							  'む':['ま','み','め','んだ','んで'],
							  'ぶ':['ば','び','べ','んだ','んで'],
							  'る':['ら','り','れ','った','って']}

		self.constructions = {'regular':   self.regular,
					  		  'potential': self.potential,
					  		  'passive':   self.passive,
					  		  'causative': self.causative,
					  	 	  'causative-passive': self.causative_passive}

		self.forms = {'short':self.short, 'polite':self.masu,
		 			  'te':self.te, 'tara':self.tara,  'ba':self.ba}

	def set_verb(self, verb):
		self.string = verb.dictionary_string
		self.original = verb.dictionary_string
		self.translation = verb.translation
		self.type   = verb.verb_type


	""" The next five functions are for the regular though causative_passive constructions"""
	def regular(self):
		pass

	def potential(self):
		if self.type == 'ichidan':
			self.string = self.string[:-1] + "られる"
		elif self.type == 'godan':
			ending = self.string[-1]
			self.string = self.string[:-1] + self.godan_endings[ending][2] + "る"
		elif self.type == 'suru':
			if self.string == 'する':
				self.string = '出,で;来,き;る'
			else:
				self.string = self.string.replace('する', 'できる')
		elif self.type == 'kuru':
			if self.string == '来,く;る':
				self.string = '来,こ;られる'
			else:
				self.string = self.string.replace('くる', 'こられる')


		self.type = "ichidan"

	def passive(self):
		if self.type == 'ichidan':
			self.string = self.string[:-1] + "られる"
		elif self.type == 'godan':
			ending = self.string[-1]
			self.string = self.string[:-1] + self.godan_endings[ending][0] + "れる"
		elif self.type == 'suru':
			self.string = self.string.replace('する', 'される')
		elif self.type == 'kuru':
			if self.string == '来,く;る':
				self.string = '来,こ;られる'
			else:
				self.string = self.string.replace('くる', 'こられる')

		self.type = "ichidan"

	def causative(self):
		if self.type == 'ichidan':
			self.string = self.string[:-1] + "させる"
		elif self.type == 'godan':
			ending = self.string[-1]
			self.string = self.string[:-1] + self.godan_endings[ending][0] + "せる"
		elif self.type == 'suru':
			self.string = self.string.replace('する', 'させる')
		elif self.type == 'kuru':
			if self.string == '来,く;る':
				self.string = '来,こ;させる'
			else:
				self.string = self.string.replace('くる', 'こさせる')

		self.type = "ichidan"

	def causative_passive(self):
		if self.type == 'ichidan':
			self.string = self.string[:-1] + "させられる"
		elif self.type == 'godan':
			ending = self.string[-1]
			self.string = self.string[:-1] + self.godan_endings[ending][0] + "せられる"
		elif self.type == 'suru':
			self.string = self.string.replace('する', 'させられる')
		elif self.type == 'kuru':
			if self.string == '来,く;る':
				self.string = '来,こ;させられる'
			else:
				self.string = self.string.replace('くる', 'こさせられる')

		self.type = "ichidan"

	""" The next functions define the forms:
			* Standard (which requires short and masu defined before it)
			* Te
			* Tara
			* Ba
		Each of these accepts three boolean arguments:
			1. Non-Negative : determines polarity  (= 1 if positive)
			2. Non-past     : determines the tense (= 1 if non-past/present)
			3. short		: determines formality (= 1 if short/plain form)

	"""
	def short(self, non_negative, non_past):
		if non_negative:
			if non_past:
				pass # Same as dictionary

			# Non-negative, past form (ta)
			else:
				if self.type == "ichidan":
					self.string = self.string[:-1] + "た"
				elif self.type == "godan":
					ending = self.string[-1]
					self.string = self.string[:-1] + self.godan_endings[ending][3]
				elif self.type == "suru":
					self.string = self.string.replace('する', 'した')
				elif self.type == "kuru":
					if self.string == '来,く;る':
						self.string = '来,き;た'
					else:
						self.string = self.string.replace('くる', 'きた')
		# Negative Short Forms
		else:
			if non_past:
				if self.type == "ichidan":
					self.string = self.string[:-1] + "ない"
				elif self.type == "godan":
					ending = self.string[-1]
					self.string = self.string[:-1] + self.godan_endings[ending][0] + "ない"
				elif self.type == "suru":
					self.string = self.string.replace('する', 'しない')
				elif self.type == "kuru":
					if self.string == '来,く;る':
						self.string = '来,こ;ない'
					else:
						self.string = self.string.replace('くる', 'こない')
			else:
				if self.type == "ichidan":
					self.string = self.string[:-1] + "なかった"
				elif self.type == "godan":
					ending = self.string[-1]
					self.string = self.string[:-1] + self.godan_endings[ending][0] + "なかった"
				elif self.type == "suru":
					self.string = self.string.replace('する', 'しなかった')
				elif self.type == "kuru":
					if self.string == '来,く;る':
						self.string = '来,こ;なかった'
					else:
						self.string = self.string.replace('くる', 'こなかった')

	def masu(self, non_negative, non_past):
		if self.type == "ichidan":
			self.string = self.string[:-1]
		elif self.type == "godan":
			ending = self.string[-1]
			self.string = self.string[:-1] + self.godan_endings[ending][1]
		elif self.type == "suru":
			self.string = self.string.replace('する', 'し')
		elif self.type == "kuru":
			if self.string == '来,く;る':
				self.string = '来,き;'
			else:
				self.string = self.string.replace('くる', 'き')

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


	def te(self, non_negative, non_past):
		if non_negative:
			if self.type == "ichidan":
				self.string = self.string[:-1] + "て"
			elif self.type == "godan":
				ending = self.string[-1]
				self.string = self.string[:-1] + self.godan_endings[ending][4]
			elif self.type == "suru":
				self.string = self.string.replace('する', 'して')
			elif self.type == "kuru":
				if self.string == '来,く;る':
					self.string = '来,き;て'
				else:
					self.string = self.string.replace('くる', 'きて')
		else:
			if self.type == "ichidan":
				self.string = self.string[:-1] + "なくて"
			elif self.type == "godan":
				ending = self.string[-1]
				self.string = self.string[:-1] + self.godan_endings[ending][0] + "なくて"
			elif self.type == "suru":
				self.string = self.string.replace('する', 'しなくて')
			elif self.type == "kuru":
				if self.string == '来,く;る':
					self.string = '来,こ;なくて'
				else:
					self.string = self.string.replace('くる', 'こなくて')

	def tara(self, non_negative, non_past):
		if non_negative:
			if self.type == "ichidan":
				self.string = self.string[:-1] + "たら"
			elif self.type == "godan":
				ending = self.string[-1]
				self.string = self.string[:-1] + self.godan_endings[ending][3] + "ら"
			elif self.type == "suru":
				self.string = self.string.replace('する', 'したら')
			elif self.type == "kuru":
				if self.string == '来,く;る':
					self.string = '来,き;たら'
				else:
					self.string = self.string.replace('くる', 'きたら')
		# Negative Short Forms
		else:
			if self.type == "ichidan":
				self.string = self.string[:-1] + "なかったら"
			elif self.type == "godan":
				ending = self.string[-1]
				self.string = self.string[:-1] + self.godan_endings[ending][0] + "なかったら"
			elif self.type == "suru":
				self.string = self.string.replace('する', 'しなかったら')
			elif self.type == "kuru":
				if self.string == '来,く;る':
					self.string = '来,こ;なかったら'
				else:
					self.string = self.string.replace('くる', 'こなかったら')

	def ba(self, non_negative, non_past):
		if non_negative:
			if self.type == "ichidan":
				self.string = self.string[:-1] + "れば"
			elif self.type == "godan":
				ending = self.string[-1]
				self.string = self.string[:-1] + self.godan_endings[ending][2] + "ば"
			elif self.type == "suru":
				self.string = self.string[:-1] + "れば"
			elif self.type == "kuru":
				self.string = self.string[:-1] + "れば"

		# Negative Forms
		else:
			if self.type == "ichidan":
				self.string = self.string[:-1] + "なければ"
			elif self.type == "godan":
				ending = self.string[-1]
				self.string = self.string[:-1] + self.godan_endings[ending][0] + "なければ"
			elif self.type == "suru":
				self.string = self.string.replace('する', 'しなければ')
			elif self.type == "kuru":
				if self.string == '来,く;る':
					self.string = '来,こ;なければ'
				else:
					self.string = self.string.replace('くる', 'こなければ')


	def __str__(self):
		kanji_string = ""
		split_verb = self.string.split(";")

		for n in range(len(split_verb)):
			# Handling the kanji, so we'll only grab one character
			if n < len(split_verb) -1: kanji_string += split_verb[n][0]

			# The last entry in the split verb is the okurigana
			else: kanji_string += split_verb[n]
		return kanji_string


	def get_kanji_string(self):
		kanji_string = ""
		split_verb = self.string.split(";")

		for substring in split_verb:
			if "," in substring:
				# Split the substring based on comma and take only the first part
				kanji_string += substring.split(",")[0]
			else:
				kanji_string += substring

		return kanji_string

	def get_kana_string(self):
		kana_string = ""
		split_verb = self.string.split(";")

		for substring in split_verb:
			if "," in substring:
				# Split the substring based on comma and take only the first part
				kana_string += substring.split(",")[1]
			else:
				kana_string += substring

		return kana_string

class Game(object):
	managaged = False

	def __init__(self, game_params):
		self.game_params = game_params

		self.conjugator = Conjugator()

		"""Filter the options based on user selection"""
		# The types of verbs
		self.types = list(set(['ichidan', 'godan','suru','kuru'])
				        & set(self.game_params))
		# Which constructions to use
		self.constructions = list(set(['regular','potential','passive','causative','causative-passive'])
		 			    	    & set(self.game_params))

		# The polarity and tenses
		self.polarities  = list(set(['non-negative', 'negative']) & set(self.game_params))
		self.tenses      = list(set(['non-past', 'past']) & set(self.game_params))

		# The actual verb conjugation forms themselves
		self.forms = list(set(['short', 'polite','te', 'tara','ba']) & set(self.game_params))

		# Create the list of verbs by selecting those of the appropriate type
		types = list(set(self.types) & set(self.game_params))
		self.verbs = Verb.objects.filter(verb_type__in=types)

	def print_all_conjugations(self):
		verb = self.verbs[0]
		self.conjugator.set_verb(verb)
		for con in list(self.conjugator.constructions.keys()):
			for form in list(self.conjugator.forms.keys()):
				for i in [1,0]:
					for j in [1,0]:
						for k in [1,0]:
							self.conjugator.constructions[con]()
							self.conjugator.forms[form](i,j,k)
							print(self.conjugator)
							self.conjugator.set_verb(verb)

	def get_conjugation(self):
		seed()

		# Get a random verb
		verb = self.verbs[randrange(len(self.verbs))]
		self.conjugator.set_verb(verb)

		print(len(self.forms))
		# Get a potential, passive, etc. construction
		construction= self.constructions[randrange(len(self.constructions))]
		self.conjugator.constructions[construction]()

		# Get a formality and a polarity
		# formality = self.formalities[randrange(len(self.formalities))]

		# Get a polarity
		polarity = self.polarities[randrange(len(self.polarities))]

		# Get a tense
		tense = self.tenses[randrange(len(self.tenses))]

		# Get a construction from standard, te, tara, ba
		form  = self.forms[randrange(len(self.forms))]

		self.conjugator.forms[form](polarity=="non-negative", tense=="non-past")

		print("The answer is " + str(self.conjugator))
		return(self.conjugator.original, self.conjugator.translation,
			   [construction, polarity, tense, form],
			   [self.conjugator.get_kanji_string(), self.conjugator.get_kana_string()])
