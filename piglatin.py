import argparse
import re
import string
import unittest

class Translator():
	VOWELS = 'aeiou'

	def translate(self, english):
		'''Takes full phrases and translates into piglatin'''
		# finds groups of word and non-word items
		chunks = re.finditer(r'(?P<word>\w+)|(?P<non_word>\W+)', english)
		return ''.join([self._selective_translation(c.groupdict()) for c in chunks])

	def _selective_translation(self, match):
		'''This only translates words, i.e. leaves non words untouched; match is a dict with 'word' & 'non_word' keys'''
		if match['word'] is not None:
			return self._translate_word(match['word'])
		else:
			return match['non_word']

	def _translate_word(self, word):
		'''Only takes ascii character words'''
		translated_word = ''

		first_vowel_index = next((i for i, c in enumerate(word) if c in self.VOWELS), None)

		beginning_consonants = word[:first_vowel_index].lower()
		rest_of_word = word[first_vowel_index:]
		
		if word[0].lower() not in self.VOWELS:
			translated_word = rest_of_word + beginning_consonants + 'ay'
		else:
			translated_word = word + "ay"

		if word[0].isupper():   # preserve capitalization of first letter
			translated_word = translated_word[0].upper() + translated_word[1:]

		return translated_word

class TranslatesCorrectly(unittest.TestCase):
	KNOWN_RULES = [
		{
			'english': 'hello',
			'piglatin': 'ellohay',
			'description': 'single consonant moves to end with -ay'
		},
		{
			'english': 'eat',
			'piglatin': 'eatay',
			'description': 'words starting with a vowel add -ay'
		},
		{
			'english': 'hello apples',
			'piglatin': 'ellohay applesay',
			'description': 'simple phrase translates'
		},
		{
			'english': 'Hello apples',
			'piglatin': 'Ellohay applesay',
			'description': 'first letter capitalization is preserved for consonant-beginning words'
		},
		{
			'english': 'Eat apples',
			'piglatin': 'Eatay applesay',
			'description': 'first letter capitalization is preserved for vowel-beginning words'
		},
		{
			'english': 'hello...  world?!',
			'piglatin': 'ellohay...  orldway?!',
			'description': 'punctuation is kept in place around words'
		},
		{
			'english': 'school',
			'piglatin': 'oolschay',
			'description': 'words beginning with multiple consonants move ALL the consonants to the end'
		}	
	]

	def __init__(self, english, piglatin, description=None):
		super(TranslatesCorrectly, self).__init__()
		self.english, self.piglatin, self.description = (english, piglatin, description)
		self.translator = Translator()

	def runTest(self):
		result = self.translator.translate(self.english)
		description = "{0}\ndesired: {1} --> {2}\nactual: {1} --> {3}".format(
			self.description, self.english, self.piglatin, result
		)
		self.assertEqual(result, self.piglatin, description)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Translate English phrases to piglatin')
	parser.add_argument('-t','--text', type=str, required=False, default=None)
	args = parser.parse_args()

	suite = unittest.TestSuite()
	suite.addTests([TranslatesCorrectly(**rule) for rule in TranslatesCorrectly.KNOWN_RULES])
	unittest.TextTestRunner().run(suite)
		
	if args.text is not None:
		translator = Translator()
		print(translator.translate(args.text.strip()))
