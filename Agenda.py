import LerComprovante as comp
import CriaImagem as cria

PDFPATH = r"Comprovante.pdf"

texto = comp.lerPDF(PDFPATH)
disciplinas = comp.criaDict(texto)

def confirma():
	print('\nSuas disciplinas parecem ser:\n')
	for disciplina in disciplinas:
		print(disciplina)
	print('\nPara confirmar aperte "Enter", ou digite um campo para alterar.')
	entrada = input('("nome", "sala", "horário"): ')
	return entrada

def escolha(campo):
	print(f'\nOs campos "{campo}" são: ')
	for n, disciplina in enumerate(disciplinas):
		print(f'{n}: {disciplina[campo]}')
	print(f'{len(disciplinas)}: Para alterar mais de um.')
	num = input('Digite o número desejado: ')
	return int(num)

def alterar(campo, num):
	try:
		print(f'\nAlterando: {disciplinas[num][campo]}')
		novo = input(f'Digite um novo "{campo}" ("Enter" para manter): ').title()
		if novo != '':
			disciplinas[num][campo] = novo
	except IndexError:
		for n, disciplina in enumerate(disciplinas):
			alterar(campo, n)

if __name__ == '__main__':
	campo = confirma().title()
	while campo != '':
		if campo.lower() in ("nome", "sala", "horário"):
			num = escolha(campo)
			alterar(campo, num)
		campo = confirma().title()

	cria.escreveAulas(disciplinas, 'Horário')
