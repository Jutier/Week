import pymupdf
import re


def lerPDF(PDFPath):
	with pymupdf.open(PDFPath) as file:
		pag = file[0]
		txt = pag.get_text()
	return txt

def criaDict(rawtext):
	Disciplinas = []

	for linha in rawtext.split('\n'):

		linhaNome = re.search(r"\([A-Z]{3}[0-9]{5}\)", linha) # Encontra código: (ABC01234)
		linhaHora = re.search("[0-2][0-9]:[0-6][0-9]-[0-2][0-9]:[0-6][0-9]", linha) # Encontra horário: 10:30-12:10
		linhaSala = re.search(r" [A-Z] ?[0-9]{3} ", linha) # Encontra sala: A123

		if linhaNome:
			try:
				# Essa é uma forma de garantir que uma disciplina só seja salva quando outra estiver para ser criada
				# Parece idiota, mas resolve a inconsistencia e agrupa os horarios com facilidade
				Disciplinas.append(disciplina)
			except UnboundLocalError:
				pass

			disciplina = {'Nome':' '.join(linha.split(' ')[:-2]).title(),'Sala': None, 'Horário':{}}
	
		if linhaHora:
			disciplina['Horário'][linha[:3]] = linhaHora.group()[:5].replace(':', 'h')

		if linhaSala:
			disciplina['Sala'] = linhaSala.group().replace(' ', '')

	Disciplinas.append(disciplina) # Salva a ultima disciplina no final do arquivo

	return Disciplinas

if __name__ == "__main__":
	print('Este código deve ser importado.')
