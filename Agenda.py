import ComprovanteOCR as comp
import CriaImagem as cria

PDFPATH = r"Comprovante.pdf"

texto = comp.lerPDF(PDFPATH)
disciplinas = comp.criaDict(texto)

def confirma():
	print('Suas disciplinas parecem ser:')
	for disciplina in disciplinas:
		print(disciplina)
	entrada = input('Enter para confirmar, ou digite algo para alterar: ')
	return entrada

def escolha(campo):
	print(f'Os campos "{campo}" são: ')
	for n, disciplina in enumerate(disciplinas):
		print(f'{n}: {disciplina[campo]}')
	print(f'{len(disciplinas)}: Para alterar mais de um.')
	num = input('Digite o número desejado: ')
	return int(num)

def alterar(campo, num):
	try:
		print(f'Alterando: {disciplinas[num][campo]}')
		novo = input(f'Digite um novo "{campo}": ')
		disciplinas[num][campo] = novo
	except IndexError:
		for n, disciplina in enumerate(disciplinas):
			alterar(campo, n)


campo = confirma()
while campo != '':
	num = escolha(campo)
	alterar(campo, num)
	campo = confirma()

cria.escreveAulas(disciplinas, 'Horário')