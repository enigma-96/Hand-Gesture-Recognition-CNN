import subprocess
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout
from nltk.tokenize import word_tokenize # type: ignore
from nltk.stem import WordNetLemmatizer # type: ignore
from textblob import TextBlob # type: ignore
import nltk # type: ignore
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required


def home_view(request):
	return render(request,'home.html')


def about_view(request):
	return render(request,'about.html')

def spanish_view(request):
	if request.method == 'POST':
		text = request.POST.get('ses')
		#tokenizing the sentence
		text.lower()
		#tokenizing the sentence
		words = word_tokenize(text)

		tagged = nltk.pos_tag(words)
		tense = {}
		tense["future"] = len([word for word in tagged if word[1] == "MD"])
		tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
		tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
		tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])



		#stopwords that will be removed
		stop_words = set(['wasn', 'wouldn', 'has', 'that', 'does', 'shouldn', 'youve', 'off', 'for', 'didn',
                          'aint', 'haven', 'werent', 'are', 'arent', 'shes', 'wasnt', 'its', 'havent', 'wouldn',
                          'dont', 'youve', 'doesnt', 'hadnt', 'is', 'thatll', 'shouldve', 'then', 'the', 'mustn',
                          'nor', 'as', 'its', 'needn', 'am', 'have', 'hasn', 'arent', 'youll', 'couldnt', 'youre',
                          'mustnt', 'didn', 'doesnt', 'll', 'an', 'hadn', 'whom', 'hasnt', 'itself', 'needn',
                          'shant', 'isnt', 'been', 'such', 'shan', 'aren', 'being', 'were', 'did', 'having',
                          'might', 've', 'wont'])



		#removing stopwords and applying lemmatizing nlp process to words
		lr = WordNetLemmatizer()
		filtered_text = []
		for w,p in zip(words,tagged):
			if w not in stop_words:
				if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
					filtered_text.append(lr.lemmatize(w,pos='v'))
				elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
					filtered_text.append(lr.lemmatize(w,pos='a'))

				else:
					filtered_text.append(lr.lemmatize(w))


		#adding the specific word to specify tense
		words = filtered_text
		temp=[]
		for w in words:
			if w=='I':
				temp.append('Me')
			else:
				temp.append(w)
		words = temp
		probable_tense = max(tense,key=tense.get)

		if probable_tense == "past" and tense["past"]>=1:
			temp = ["Before"]
			temp = temp + words
			words = temp
		elif probable_tense == "future" and tense["future"]>=1:
			if "Will" not in words:
					temp = ["Will"]
					temp = temp + words
					words = temp
			else:
				pass
		elif probable_tense == "present":
			if tense["present_continuous"]>=1:
				temp = ["Now"]
				temp = temp + words
				words = temp


		filtered_text = []
		for w in words:
			path = w + ".mp4"
			f = finders.find(path)
			#splitting the word if its animation is not present in database
			if not f:
				for c in w:
					filtered_text.append(c)
			#otherwise animation of word
			else:
				filtered_text.append(w)
		words = filtered_text
		word9=text
		a=TextBlob(word9)
		b=a.translate(from_lang='es',to ='en')
		b=b.split()

		return render(request,'spanish.html',{'words':b,'text':text})
	else:
		return render(request,'spanish.html')


def korean_view(request):
	if request.method == 'POST':
		text = request.POST.get('ses')
		#tokenizing the sentence
		text.lower()
		#tokenizing the sentence
		words = word_tokenize(text)

		tagged = nltk.pos_tag(words)
		tense = {}
		tense["future"] = len([word for word in tagged if word[1] == "MD"])
		tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
		tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
		tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])



		#stopwords that will be removed
		stop_words = set(['wasn', 'wouldn', 'has', 'that', 'does', 'shouldn', 'youve', 'off', 'for', 'didn',
                          'aint', 'haven', 'werent', 'are', 'arent', 'shes', 'wasnt', 'its', 'havent', 'wouldn',
                          'dont', 'youve', 'doesnt', 'hadnt', 'is', 'thatll', 'shouldve', 'then', 'the', 'mustn',
                          'nor', 'as', 'its', 'needn', 'am', 'have', 'hasn', 'arent', 'youll', 'couldnt', 'youre',
                          'mustnt', 'didn', 'doesnt', 'll', 'an', 'hadn', 'whom', 'hasnt', 'itself', 'needn',
                          'shant', 'isnt', 'been', 'such', 'shan', 'aren', 'being', 'were', 'did', 'having',
                          'might', 've', 'wont'])


		#removing stopwords and applying lemmatizing nlp process to words
		lr = WordNetLemmatizer()
		filtered_text = []
		for w,p in zip(words,tagged):
			if w not in stop_words:
				if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
					filtered_text.append(lr.lemmatize(w,pos='v'))
				elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
					filtered_text.append(lr.lemmatize(w,pos='a'))

				else:
					filtered_text.append(lr.lemmatize(w))


		#adding the specific word to specify tense
		words = filtered_text
		temp=[]
		for w in words:
			if w=='I':
				temp.append('Me')
			else:
				temp.append(w)
		words = temp
		probable_tense = max(tense,key=tense.get)

		if probable_tense == "past" and tense["past"]>=1:
			temp = ["Before"]
			temp = temp + words
			words = temp
		elif probable_tense == "future" and tense["future"]>=1:
			if "Will" not in words:
					temp = ["Will"]
					temp = temp + words
					words = temp
			else:
				pass
		elif probable_tense == "present":
			if tense["present_continuous"]>=1:
				temp = ["Now"]
				temp = temp + words
				words = temp


		filtered_text = []
		for w in words:
			path = w + ".mp4"
			f = finders.find(path)
			#splitting the word if its animation is not present in database
			if not f:
				for c in w:
					filtered_text.append(c)
			#otherwise animation of word
			else:
				filtered_text.append(w)
		words = filtered_text
		word9=text
		a=TextBlob(word9)
		b=a.translate(from_lang='ko',to ='en')
		b=b.split()

		return render(request,'korean.html',{'words':b,'text':text})
	else:
		return render(request,'korean.html')



def french_view(request):
	if request.method == 'POST':
		text = request.POST.get('ses')
		#tokenizing the sentence
		text.lower()
		#tokenizing the sentence
		words = word_tokenize(text)

		tagged = nltk.pos_tag(words)
		tense = {}
		tense["future"] = len([word for word in tagged if word[1] == "MD"])
		tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
		tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
		tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])



		#stopwords that will be removed
		stop_words = set(['wasn', 'wouldn', 'has', 'that', 'does', 'shouldn', 'youve', 'off', 'for', 'didn',
                          'aint', 'haven', 'werent', 'are', 'arent', 'shes', 'wasnt', 'its', 'havent', 'wouldn',
                          'dont', 'youve', 'doesnt', 'hadnt', 'is', 'thatll', 'shouldve', 'then', 'the', 'mustn',
                          'nor', 'as', 'its', 'needn', 'am', 'have', 'hasn', 'arent', 'youll', 'couldnt', 'youre',
                          'mustnt', 'didn', 'doesnt', 'll', 'an', 'hadn', 'whom', 'hasnt', 'itself', 'needn',
                          'shant', 'isnt', 'been', 'such', 'shan', 'aren', 'being', 'were', 'did', 'having',
                          'might', 've', 'wont'])



		#removing stopwords and applying lemmatizing nlp process to words
		lr = WordNetLemmatizer()
		filtered_text = []
		for w,p in zip(words,tagged):
			if w not in stop_words:
				if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
					filtered_text.append(lr.lemmatize(w,pos='v'))
				elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
					filtered_text.append(lr.lemmatize(w,pos='a'))

				else:
					filtered_text.append(lr.lemmatize(w))


		#adding the specific word to specify tense
		words = filtered_text
		temp=[]
		for w in words:
			if w=='I':
				temp.append('Me')
			else:
				temp.append(w)
		words = temp
		probable_tense = max(tense,key=tense.get)

		if probable_tense == "past" and tense["past"]>=1:
			temp = ["Before"]
			temp = temp + words
			words = temp
		elif probable_tense == "future" and tense["future"]>=1:
			if "Will" not in words:
					temp = ["Will"]
					temp = temp + words
					words = temp
			else:
				pass
		elif probable_tense == "present":
			if tense["present_continuous"]>=1:
				temp = ["Now"]
				temp = temp + words
				words = temp


		filtered_text = []
		for w in words:
			path = w + ".mp4"
			f = finders.find(path)
			#splitting the word if its animation is not present in database
			if not f:
				for c in w:
					filtered_text.append(c)
			#otherwise animation of word
			else:
				filtered_text.append(w)
		words = filtered_text
		word9=text
		a=TextBlob(word9)
		b=a.translate(from_lang='fr',to ='en')
		b=b.split()

		return render(request,'french.html',{'words':b,'text':text})
	else:
		return render(request,'french.html')
	

def arabic_view(request):
	if request.method == 'POST':
		text = request.POST.get('ses')
		#tokenizing the sentence
		text.lower()
		#tokenizing the sentence
		words = word_tokenize(text)

		tagged = nltk.pos_tag(words)
		tense = {}
		tense["future"] = len([word for word in tagged if word[1] == "MD"])
		tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
		tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
		tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])



		#stopwords that will be removed
		stop_words = set(['wasn', 'wouldn', 'has', 'that', 'does', 'shouldn', 'youve', 'off', 'for', 'didn',
                          'aint', 'haven', 'werent', 'are', 'arent', 'shes', 'wasnt', 'its', 'havent', 'wouldn',
                          'dont', 'youve', 'doesnt', 'hadnt', 'is', 'thatll', 'shouldve', 'then', 'the', 'mustn',
                          'nor', 'as', 'its', 'needn', 'am', 'have', 'hasn', 'arent', 'youll', 'couldnt', 'youre',
                          'mustnt', 'didn', 'doesnt', 'll', 'an', 'hadn', 'whom', 'hasnt', 'itself', 'needn',
                          'shant', 'isnt', 'been', 'such', 'shan', 'aren', 'being', 'were', 'did', 'having',
                          'might', 've', 'wont'])



		#removing stopwords and applying lemmatizing nlp process to words
		lr = WordNetLemmatizer()
		filtered_text = []
		for w,p in zip(words,tagged):
			if w not in stop_words:
				if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
					filtered_text.append(lr.lemmatize(w,pos='v'))
				elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
					filtered_text.append(lr.lemmatize(w,pos='a'))

				else:
					filtered_text.append(lr.lemmatize(w))


		#adding the specific word to specify tense
		words = filtered_text
		temp=[]
		for w in words:
			if w=='I':
				temp.append('Me')
			else:
				temp.append(w)
		words = temp
		probable_tense = max(tense,key=tense.get)

		if probable_tense == "past" and tense["past"]>=1:
			temp = ["Before"]
			temp = temp + words
			words = temp
		elif probable_tense == "future" and tense["future"]>=1:
			if "Will" not in words:
					temp = ["Will"]
					temp = temp + words
					words = temp
			else:
				pass
		elif probable_tense == "present":
			if tense["present_continuous"]>=1:
				temp = ["Now"]
				temp = temp + words
				words = temp


		filtered_text = []
		for w in words:
			path = w + ".mp4"
			f = finders.find(path)
			#splitting the word if its animation is not present in database
			if not f:
				for c in w:
					filtered_text.append(c)
			#otherwise animation of word
			else:
				filtered_text.append(w)
		words = filtered_text
		word9=text
		a=TextBlob(word9)
		b=a.translate(from_lang='ar',to ='en')
		b=b.split()

		return render(request,'arabic.html',{'words':b,'text':text})
	else:
		return render(request,'arabic.html')


def hindi_view(request):
	if request.method == 'POST':
		text = request.POST.get('ses')
		#tokenizing the sentence
		text.lower()
		#tokenizing the sentence
		words = word_tokenize(text)

		tagged = nltk.pos_tag(words)
		tense = {}
		tense["future"] = len([word for word in tagged if word[1] == "MD"])
		tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
		tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
		tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])



		#stopwords that will be removed
		stop_words = set(['wasn', 'wouldn', 'has', 'that', 'does', 'shouldn', 'youve', 'off', 'for', 'didn',
                          'aint', 'haven', 'werent', 'are', 'arent', 'shes', 'wasnt', 'its', 'havent', 'wouldn',
                          'dont', 'youve', 'doesnt', 'hadnt', 'is', 'thatll', 'shouldve', 'then', 'the', 'mustn',
                          'nor', 'as', 'its', 'needn', 'am', 'have', 'hasn', 'arent', 'youll', 'couldnt', 'youre',
                          'mustnt', 'didn', 'doesnt', 'll', 'an', 'hadn', 'whom', 'hasnt', 'itself', 'needn',
                          'shant', 'isnt', 'been', 'such', 'shan', 'aren', 'being', 'were', 'did', 'having',
                          'might', 've', 'wont'])


		#removing stopwords and applying lemmatizing nlp process to words
		lr = WordNetLemmatizer()
		filtered_text = []
		for w,p in zip(words,tagged):
			if w not in stop_words:
				if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
					filtered_text.append(lr.lemmatize(w,pos='v'))
				elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
					filtered_text.append(lr.lemmatize(w,pos='a'))

				else:
					filtered_text.append(lr.lemmatize(w))


		#adding the specific word to specify tense
		words = filtered_text
		temp=[]
		for w in words:
			if w=='I':
				temp.append('Me')
			else:
				temp.append(w)
		words = temp
		probable_tense = max(tense,key=tense.get)

		if probable_tense == "past" and tense["past"]>=1:
			temp = ["Before"]
			temp = temp + words
			words = temp
		elif probable_tense == "future" and tense["future"]>=1:
			if "Will" not in words:
					temp = ["Will"]
					temp = temp + words
					words = temp
			else:
				pass
		elif probable_tense == "present":
			if tense["present_continuous"]>=1:
				temp = ["Now"]
				temp = temp + words
				words = temp


		filtered_text = []
		for w in words:
			path = w + ".mp4"
			f = finders.find(path)
			#splitting the word if its animation is not present in database
			if not f:
				for c in w:
					filtered_text.append(c)
			#otherwise animation of word
			else:
				filtered_text.append(w)
		words = filtered_text
		word9=text
		a=TextBlob(word9)
		b=a.translate(from_lang='hi',to ='en')
		b=b.split()

		return render(request,'hindi.html',{'words':b,'text':text})
	else:
		return render(request,'hindi.html')

def telugu_view(request):
	if request.method == 'POST':
		text = request.POST.get('ses')
		#tokenizing the sentence
		text.lower()
		#tokenizing the sentence
		words = word_tokenize(text)

		tagged = nltk.pos_tag(words)
		tense = {}
		tense["future"] = len([word for word in tagged if word[1] == "MD"])
		tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
		tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
		tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])



		#stopwords that will be removed
		stop_words = set(['wasn', 'wouldn', 'has', 'that', 'does', 'shouldn', 'youve', 'off', 'for', 'didn',
                          'aint', 'haven', 'werent', 'are', 'arent', 'shes', 'wasnt', 'its', 'havent', 'wouldn',
                          'dont', 'youve', 'doesnt', 'hadnt', 'is', 'thatll', 'shouldve', 'then', 'the', 'mustn',
                          'nor', 'as', 'its', 'needn', 'am', 'have', 'hasn', 'arent', 'youll', 'couldnt', 'youre',
                          'mustnt', 'didn', 'doesnt', 'll', 'an', 'hadn', 'whom', 'hasnt', 'itself', 'needn',
                          'shant', 'isnt', 'been', 'such', 'shan', 'aren', 'being', 'were', 'did', 'having',
                          'might', 've', 'wont'])



		#removing stopwords and applying lemmatizing nlp process to words
		lr = WordNetLemmatizer()
		filtered_text = []
		for w,p in zip(words,tagged):
			if w not in stop_words:
				if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
					filtered_text.append(lr.lemmatize(w,pos='v'))
				elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
					filtered_text.append(lr.lemmatize(w,pos='a'))

				else:
					filtered_text.append(lr.lemmatize(w))


		#adding the specific word to specify tense
		words = filtered_text
		temp=[]
		for w in words:
			if w=='I':
				temp.append('Me')
			else:
				temp.append(w)
		words = temp
		probable_tense = max(tense,key=tense.get)

		if probable_tense == "past" and tense["past"]>=1:
			temp = ["Before"]
			temp = temp + words
			words = temp
		elif probable_tense == "future" and tense["future"]>=1:
			if "Will" not in words:
					temp = ["Will"]
					temp = temp + words
					words = temp
			else:
				pass
		elif probable_tense == "present":
			if tense["present_continuous"]>=1:
				temp = ["Now"]
				temp = temp + words
				words = temp


		filtered_text = []
		for w in words:
			path = w + ".mp4"
			f = finders.find(path)
			#splitting the word if its animation is not present in database
			if not f:
				for c in w:
					filtered_text.append(c)
			#otherwise animation of word
			else:
				filtered_text.append(w)
		words = filtered_text
		word9=text
		a=TextBlob(word9)
		b=a.translate(from_lang='te',to ='en')
		b=b.split()

		return render(request,'telugu.html',{'words':b,'text':text})
	else:
		return render(request,'telugu.html')


def urdu_view(request):
	if request.method == 'POST':
		text = request.POST.get('ses')
		#tokenizing the sentence
		text.lower()
		#tokenizing the sentence
		words = word_tokenize(text)

		tagged = nltk.pos_tag(words)
		tense = {}
		tense["future"] = len([word for word in tagged if word[1] == "MD"])
		tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
		tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
		tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])



		#stopwords that will be removed
		stop_words = set(['wasn', 'wouldn', 'has', 'that', 'does', 'shouldn', 'youve', 'off', 'for', 'didn',
                          'aint', 'haven', 'werent', 'are', 'arent', 'shes', 'wasnt', 'its', 'havent', 'wouldn',
                          'dont', 'youve', 'doesnt', 'hadnt', 'is', 'thatll', 'shouldve', 'then', 'the', 'mustn',
                          'nor', 'as', 'its', 'needn', 'am', 'have', 'hasn', 'arent', 'youll', 'couldnt', 'youre',
                          'mustnt', 'didn', 'doesnt', 'll', 'an', 'hadn', 'whom', 'hasnt', 'itself', 'needn',
                          'shant', 'isnt', 'been', 'such', 'shan', 'aren', 'being', 'were', 'did', 'having',
                          'might', 've', 'wont'])



		#removing stopwords and applying lemmatizing nlp process to words
		lr = WordNetLemmatizer()
		filtered_text = []
		for w,p in zip(words,tagged):
			if w not in stop_words:
				if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
					filtered_text.append(lr.lemmatize(w,pos='v'))
				elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
					filtered_text.append(lr.lemmatize(w,pos='a'))

				else:
					filtered_text.append(lr.lemmatize(w))


		#adding the specific word to specify tense
		words = filtered_text
		temp=[]
		for w in words:
			if w=='I':
				temp.append('Me')
			else:
				temp.append(w)
		words = temp
		probable_tense = max(tense,key=tense.get)

		if probable_tense == "past" and tense["past"]>=1:
			temp = ["Before"]
			temp = temp + words
			words = temp
		elif probable_tense == "future" and tense["future"]>=1:
			if "Will" not in words:
					temp = ["Will"]
					temp = temp + words
					words = temp
			else:
				pass
		elif probable_tense == "present":
			if tense["present_continuous"]>=1:
				temp = ["Now"]
				temp = temp + words
				words = temp


		filtered_text = []
		for w in words:
			path = w + ".mp4"
			f = finders.find(path)
			#splitting the word if its animation is not present in database
			if not f:
				for c in w:
					filtered_text.append(c)
			#otherwise animation of word
			else:
				filtered_text.append(w)
		words = filtered_text
		word9=text
		a=TextBlob(word9)
		b=a.translate(from_lang='ur',to ='en')
		b=b.split()

		return render(request,'urdu.html',{'words':b,'text':text})
	else:
		return render(request,'urdu.html')



def german_view(request):
	if request.method == 'POST':
		text = request.POST.get('ses')
		#tokenizing the sentence
		text.lower()
		#tokenizing the sentence
		words = word_tokenize(text)

		tagged = nltk.pos_tag(words)
		tense = {}
		tense["future"] = len([word for word in tagged if word[1] == "MD"])
		tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
		tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
		tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])



		#stopwords that will be removed
		stop_words = set(['wasn', 'wouldn', 'has', 'that', 'does', 'shouldn', 'youve', 'off', 'for', 'didn',
                          'aint', 'haven', 'werent', 'are', 'arent', 'shes', 'wasnt', 'its', 'havent', 'wouldn',
                          'dont', 'youve', 'doesnt', 'hadnt', 'is', 'thatll', 'shouldve', 'then', 'the', 'mustn',
                          'nor', 'as', 'its', 'needn', 'am', 'have', 'hasn', 'arent', 'youll', 'couldnt', 'youre',
                          'mustnt', 'didn', 'doesnt', 'll', 'an', 'hadn', 'whom', 'hasnt', 'itself', 'needn',
                          'shant', 'isnt', 'been', 'such', 'shan', 'aren', 'being', 'were', 'did', 'having',
                          'might', 've', 'wont'])


		#removing stopwords and applying lemmatizing nlp process to words
		lr = WordNetLemmatizer()
		filtered_text = []
		for w,p in zip(words,tagged):
			if w not in stop_words:
				if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
					filtered_text.append(lr.lemmatize(w,pos='v'))
				elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
					filtered_text.append(lr.lemmatize(w,pos='a'))

				else:
					filtered_text.append(lr.lemmatize(w))


		#adding the specific word to specify tense
		words = filtered_text
		temp=[]
		for w in words:
			if w=='I':
				temp.append('Me')
			else:
				temp.append(w)
		words = temp
		probable_tense = max(tense,key=tense.get)

		if probable_tense == "past" and tense["past"]>=1:
			temp = ["Before"]
			temp = temp + words
			words = temp
		elif probable_tense == "future" and tense["future"]>=1:
			if "Will" not in words:
					temp = ["Will"]
					temp = temp + words
					words = temp
			else:
				pass
		elif probable_tense == "present":
			if tense["present_continuous"]>=1:
				temp = ["Now"]
				temp = temp + words
				words = temp


		filtered_text = []
		for w in words:
			path = w + ".mp4"
			f = finders.find(path)
			#splitting the word if its animation is not present in database
			if not f:
				for c in w:
					filtered_text.append(c)
			#otherwise animation of word
			else:
				filtered_text.append(w)
		words = filtered_text
		word9=text
		a=TextBlob(word9)
		b=a.translate(from_lang='de',to ='en')
		b=b.split()

		return render(request,'german.html',{'words':b,'text':text})
	else:
		return render(request,'german.html')
	


def japanese_view(request):
	if request.method == 'POST':
		text = request.POST.get('ses')
		#tokenizing the sentence
		text.lower()
		#tokenizing the sentence
		words = word_tokenize(text)

		tagged = nltk.pos_tag(words)
		tense = {}
		tense["future"] = len([word for word in tagged if word[1] == "MD"])
		tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
		tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
		tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])



		#stopwords that will be removed
		stop_words = set(['wasn', 'wouldn', 'has', 'that', 'does', 'shouldn', 'youve', 'off', 'for', 'didn',
                          'aint', 'haven', 'werent', 'are', 'arent', 'shes', 'wasnt', 'its', 'havent', 'wouldn',
                          'dont', 'youve', 'doesnt', 'hadnt', 'is', 'thatll', 'shouldve', 'then', 'the', 'mustn',
                          'nor', 'as', 'its', 'needn', 'am', 'have', 'hasn', 'arent', 'youll', 'couldnt', 'youre',
                          'mustnt', 'didn', 'doesnt', 'll', 'an', 'hadn', 'whom', 'hasnt', 'itself', 'needn',
                          'shant', 'isnt', 'been', 'such', 'shan', 'aren', 'being', 'were', 'did', 'having',
                          'might', 've', 'wont'])


		#removing stopwords and applying lemmatizing nlp process to words
		lr = WordNetLemmatizer()
		filtered_text = []
		for w,p in zip(words,tagged):
			if w not in stop_words:
				if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
					filtered_text.append(lr.lemmatize(w,pos='v'))
				elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
					filtered_text.append(lr.lemmatize(w,pos='a'))

				else:
					filtered_text.append(lr.lemmatize(w))


		#adding the specific word to specify tense
		words = filtered_text
		temp=[]
		for w in words:
			if w=='I':
				temp.append('Me')
			else:
				temp.append(w)
		words = temp
		probable_tense = max(tense,key=tense.get)

		if probable_tense == "past" and tense["past"]>=1:
			temp = ["Before"]
			temp = temp + words
			words = temp
		elif probable_tense == "future" and tense["future"]>=1:
			if "Will" not in words:
					temp = ["Will"]
					temp = temp + words
					words = temp
			else:
				pass
		elif probable_tense == "present":
			if tense["present_continuous"]>=1:
				temp = ["Now"]
				temp = temp + words
				words = temp


		filtered_text = []
		for w in words:
			path = w + ".mp4"
			f = finders.find(path)
			#splitting the word if its animation is not present in database
			if not f:
				for c in w:
					filtered_text.append(c)
			#otherwise animation of word
			else:
				filtered_text.append(w)
		words = filtered_text
		word9=text
		a=TextBlob(word9)
		b=a.translate(from_lang='ja',to ='en')
		b=b.split()

		return render(request,'japanese.html',{'words':b,'text':text})
	else:
		return render(request,'japanese.html')



def contact_view(request):
	return render(request,'contact.html')

@login_required(login_url="login")
def animation_view(request):
	if request.method == 'POST':
		text = request.POST.get('sen')
		#tokenizing the sentence
		text.lower()
		#tokenizing the sentence
		words = word_tokenize(text)

		tagged = nltk.pos_tag(words)
		tense = {}
		tense["future"] = len([word for word in tagged if word[1] == "MD"])
		tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
		tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
		tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])



		#stopwords that will be removed
		stop_words = set(['wasn', 'wouldn', 'has', 'that', 'does', 'shouldn', 'youve', 'off', 'for', 'didn',
                          'aint', 'haven', 'werent', 'are', 'arent', 'shes', 'wasnt', 'its', 'havent', 'wouldn',
                          'dont', 'youve', 'doesnt', 'hadnt', 'is', 'thatll', 'shouldve', 'then', 'the', 'mustn',
                          'nor', 'as', 'its', 'needn', 'am', 'have', 'hasn', 'arent', 'youll', 'couldnt', 'youre',
                          'mustnt', 'didn', 'doesnt', 'll', 'an', 'hadn', 'whom', 'hasnt', 'itself', 'needn',
                          'shant', 'isnt', 'been', 'such', 'shan', 'aren', 'being', 'were', 'did', 'having',
                          'might', 've', 'wont'])


		#removing stopwords and applying lemmatizing nlp process to words
		lr = WordNetLemmatizer()
		filtered_text = []
		for w,p in zip(words,tagged):
			if w not in stop_words:
				if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
					filtered_text.append(lr.lemmatize(w,pos='v'))
				elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
					filtered_text.append(lr.lemmatize(w,pos='a'))

				else:
					filtered_text.append(lr.lemmatize(w))


		#adding the specific word to specify tense
		words = filtered_text
		temp=[]
		for w in words:
			if w=='I':
				temp.append('Me')
			else:
				temp.append(w)
		words = temp
		probable_tense = max(tense,key=tense.get)

		if probable_tense == "past" and tense["past"]>=1:
			temp = ["Before"]
			temp = temp + words
			words = temp
		elif probable_tense == "future" and tense["future"]>=1:
			if "Will" not in words:
					temp = ["Will"]
					temp = temp + words
					words = temp
			else:
				pass
		elif probable_tense == "present":
			if tense["present_continuous"]>=1:
				temp = ["Now"]
				temp = temp + words
				words = temp


		filtered_text = []
		for w in words:
			path = w + ".mp4"
			f = finders.find(path)
			#splitting the word if its animation is not present in database
			if not f:
				for c in w:
					filtered_text.append(c)
			#otherwise animation of word
			else:
				filtered_text.append(w)
		words = filtered_text


		return render(request,'animation.html',{'words':words,'text':text})
	else:
		return render(request,'animation.html')

@login_required(login_url="login")

def handgestures_view(request):
    if request.method == 'GET':
        return render(request, 'handgestures.html')
    elif request.method == 'POST':
        if 'start_detection' in request.POST:
            subprocess.Popen(["python", "C://Users/Mohammed/audio2/A2SL/test.py"])
            return JsonResponse({'message': 'Real-time detection started. Click on CLOSE to exit'})
        elif 'stop_detection' in request.POST:
            # Add code to stop the real-time detection process if needed
            return JsonResponse({'message': 'Real-time detection stopped'})
        


def signup_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request,user)
			# log the user in
			return redirect('animation')
	else:
		form = UserCreationForm()
	return render(request,'signup.html',{'form':form})



def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			#log in user
			user = form.get_user()
			login(request,user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				return redirect('animation')
	else:
		form = AuthenticationForm()
	return render(request,'login.html',{'form':form})


def logout_view(request):
	logout(request)
	return redirect("home")
