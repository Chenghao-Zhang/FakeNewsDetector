from django.db import models

class Vocabulary (models.Model):
	#word, lang, spanish, english, german, es_definition, en_definition, ger_definition

	base_word=models.CharField(max_length=20)
	base_lang=models.CharField(max_length=3,choices=[('es',"SPANISH"),('en',"ENGLISH"),('ger',"GERMAN")])
	spanish=models.CharField(max_length=30)
	english=models.CharField(max_length=30)
	german=models.CharField(max_length=30)
	es_definition=models.CharField(max_length=200)
	en_definition=models.CharField(max_length=200)
	ger_definition=models.CharField(max_length=200)

	objects = models.Manager()

	def __str__(self) -> str:
		d = "{} - {} - {}"
		return d.format(self.english, self.spanish, self.german)




class ErrorLog(models.Model):
	base_word=models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
	error_type=models.CharField(max_length=300)

	objects = models.Manager()

	def __str__(self) -> str:
		d = "{} - {}"
		return d.format(self.base_word, self.error_type)

