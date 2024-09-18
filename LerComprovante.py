import pymupdf
import re


def lerPDF(PDFPath):
	pag = pymupdf.open(PDFPath)[0]
	#rawtext = pytesseract.image_to_string(img[0], lang='por')
	return pag.get_text()

def criaDict(rawtext):
	Disciplinas = []

	for linha in rawtext.split('\n'):

		linhaNome = re.search(r"\([A-Z]{3}[0-9]{5}\)", linha)
		linhaHora = re.search("[0-2][0-9]:[0-6][0-9]-[0-2][0-9]:[0-6][0-9]", linha)
		linhaSala = re.search(r" [A-Z] ?[0-9]{3} ", linha)

		if linhaNome:
			try:
				Disciplinas.append(disciplina)
			except:
				pass
			print(linha)
			disciplina = {'Nome':' '.join(linha.split(' ')[:-2]).title(),'Sala': None, 'Horário':{}}
	
		if linhaHora:
			disciplina['Horário'][linha[:3]] = linhaHora.group()[:5].replace(':', 'h')

		if linhaSala:
			disciplina['Sala'] = linhaSala.group().replace(' ', '')

	Disciplinas.append(disciplina)

	return Disciplinas