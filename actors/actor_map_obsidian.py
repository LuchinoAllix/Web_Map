import csv
import os

rep = os.path.abspath(os.path.dirname(__file__))
actors = os.path.join(rep, 'actors.csv')

dico = {}

with open(actors,encoding='utf8') as csv_file :
	csv_reader = csv.reader(csv_file, delimiter=',')
	dico["Chris Pratt"] = ['Omar Sy']
	dico["Omar Sy"] = ['Chris Pratt']
	for row in csv_reader:
		if len(row)>1 : # Parce que la première ligne comprend "\ufeff" donc traiter manuellement
			pass
		else :
			names = []
			name =''
			inLink = False
			i = 0
			while i < len(row[0]) : #rajout des noms par ligne(film)
				c = row[0][i]
				if c == '(' :
					inLink = True
					name =name[:-1] # on retire l'espace avant le lien
					names.append(name)
					name = ''
				elif c == ')' :
					inLink = False
					i+=2
				elif not inLink :
					name += c
				i+=1
			for name in names : # rajout des noms dans le dico
				if name not in dico :
					dico[name] = []
				for other_name in names :
					if name != other_name :
						if name not in dico[name] :
							dico[name].append(other_name)

del dico['~Not Notable~'] #on retire les éléments non voulus

for name in dico : # on écrit le dico dans les fichiers (séparé par lettre parce que obsidian a du mal sinon)
	loc = os.path.join(rep,"files",name[0],name+".md")
	with open(loc,"w",encoding="UTF8") as file:
		content = ""
		for actor in dico[name] :
			content += "[["+actor+"]]\n"
		file.write(content)
		
