import re
import string
import unittest

class TestPigLatin(unittest.TestCase):
	
	def setUp(self):
		self.vowels = ['a','e','i','o','u']

	def translate(self, english):
		'''Takes full phrases and translates into piglatin'''

		# finds groups of word and non-word items
		chunks = re.findall(r'(\w+|\W+)', english) 

		output = ""
		for w in chunks:
			if w[0] in string.ascii_letters:
				output += self.wordTranslate(w)
			else:
				output += w
		return output.strip()
		
	def wordTranslate(self, word):
		'''Only takes ascii character words'''
		firstLetter = word[0]
		lowerFirstLetter = word[0].lower()
		
		returnStr = ""
		
		positionFirstVowel = -1
		for i, c in enumerate(word):
			if c in self.vowels:
				positionFirstVowel = i
				break
		
		consonantChunk = word[:positionFirstVowel].lower()
		endChunk = word[positionFirstVowel:]
		
		if lowerFirstLetter not in self.vowels:
			returnStr = endChunk + consonantChunk + "ay"
		else:
			returnStr = word + "ay"

		if firstLetter != lowerFirstLetter:
			returnStr = returnStr[0].upper() + returnStr[1:]  # capitalizes first letter

		return returnStr

	def test_starting_consonant(self):
		self.assertEqual(self.translate("hello"), "ellohay")

	def test_starting_vowel(self):
		self.assertEqual(self.translate("eat"), "eatay")

	def test_hello_apples(self):
		self.assertEqual(self.translate("hello apples"), "ellohay applesay")

	def test_uppercase_phrase_consonant(self):
		self.assertEqual(self.translate("Hello apples"), "Ellohay applesay")

	def test_uppercase_phrase_vowel(self):
		self.assertEqual(self.translate("Eat apples"), "Eatay applesay")
		
	def test_punctuation_phrase(self):
		self.assertEqual(self.translate("hello...  world?!"), "ellohay...  orldway?!")
	
	def test_multi_consonant(self):
		self.assertEqual(self.translate("school"), "oolschay")
	
if __name__ == "__main__":
	unittest.main()