from PIL import Image, ImageFont, ImageDraw


# Fonte para horas
HFont = ImageFont.truetype('Fontes/Cousine/Cousine-Regular.ttf', size=46)
# Fonte para texto
TFont = ImageFont.truetype('Fontes/Nanum_Gothic/NanumGothic-Bold.ttf', size=45)

# Valor de y para cada dia
Y = {'Seg':[427+56*i for i in range(5)],
	 'Ter':[731+56*i for i in range(5)],
	 'Qua':[1034+56*i for i in range(5)],
	 'Qui':[1338+56*i for i in range(5)],
	 'Sex':[1641+56*i for i in range(5)]}

# Fundo padrão
img = Image.open('Fundo base/Planner.png')
draw = ImageDraw.Draw(img)

# Formato Disciplinas:
# [{'Nome':'Modelo A', 'Sala':'O999', 'Horário':{'Seg':'13h30', 'Ter':'13h30', 'Qua':'13h30', 'Qui':'13h30', 'Sex':'13h30'}}]

Exemplo_Disciplinas = [
					  {'Nome':'Modelo A', 'Sala':'O999', 'Horário':{'Ter':'13h30', 'Qua':'13h30', 'Qui':'13h30', 'Sex':'13h30'}},
					  {'Nome':'Modelo B', 'Sala':'O999', 'Horário':{'Seg':'10h30', 'Ter':'10h30', 'Qua':'10h30', 'Qui':'10h30', 'Sex':'10h30'}},
					  {'Nome':'Modelo C', 'Sala':'O999', 'Horário':{'Seg':'18h30', 'Ter':'18h30', 'Qua':'18h30', 'Qui':'18h30', 'Sex':'18h30'}}
					  ]



def escreve(Campo, Texto, Centro, Fonte):
	'''Escreve 'Texto' na linha 'Campo' centrado em 'Centro' com 'Fonte'.'''

	x = Centro - (draw.textlength(Texto, Fonte) / 2)
	y = Campo

	draw.text((x, y), Texto, font=Fonte, fill='rgb(230, 230, 230)')


def aula(Campo, Hora, Nome, Sala):
	'''Passa a 'Hora', o 'Nome' e a 'Sala' na linha do 'Campo' 
	para a função escreve() com a fonte adequada e com
	a posição x definida no centro desses campos'''

	# Horário
	escreve(Campo, Hora, 413, HFont)
	# Disciplina
	escreve(Campo, Nome, 773, TFont)
	# Sala
	escreve(Campo, Sala, 1192, TFont)


def escreveAulas(Aulas, Arquivo):
	'''Recebe um dicionário com as disciplinas,
	organiza elas em cada dia de acordo com o horário
	e passa as informações para a função aula().
	Salva uma imagem no mesmo diretório com o nome $Arquivo'''

	for Dia in Y:
		Ordem = 0
		AulasDia = []
		for a in Aulas:
			if Dia in a['Horário']:
				AulasDia.append(a)
		AulasDia.sort(key=lambda x: int(x['Horário'][Dia][0:2]))
		for a in AulasDia:
			Nome = a['Nome']
			Hora = a['Horário'][Dia]
			Sala = a['Sala']
			aula(Y[Dia][Ordem], Hora, Nome, Sala)
			Ordem += 1
		while Ordem < 5:
			aula(Y[Dia][Ordem], '--h--', '-----', '---')
			Ordem += 1

	img.save(Arquivo+'.png')


if __name__ == '__main__':
	print('Este código deve ser importado.')
	print('Executar ele salva um exemplo do uso. Pode ser adaptado para atender certas nescessidades.')
	escreveAulas(Exemplo_Disciplinas, 'Exemplo')
