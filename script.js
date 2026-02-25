pdfjsLib.GlobalWorkerOptions.workerSrc =
	"https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

let disciplines = [];

// ============================================
// Inicialização
// ============================================

document.addEventListener('DOMContentLoaded', () => {
	const pdfInput = document.getElementById('pdfInput');
	pdfInput.addEventListener('change', handlePdfUpload);

	document.getElementById('generateBtn').addEventListener('click', drawSchedule);
	document.getElementById('downloadBtn').addEventListener('click', downloadSchedule);
});

// ============================================
// Leitura do PDF
// ============================================

async function handlePdfUpload(e) {
	const file = e.target.files[0];
	if (!file) return;

	const statusEl = document.getElementById('status');
	statusEl.textContent = 'Processando...';

	try {
		const arrayBuffer = await file.arrayBuffer();
		const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;

		let lines = [];

		for (let i = 1; i <= pdf.numPages; i++) {
			const page = await pdf.getPage(i);
			const textContent = await page.getTextContent();
			lines = lines.concat(textContent.items.map(item => item.str));
		}

		disciplines = criaDict(lines);

		if (disciplines.length > 0) {
			statusEl.textContent = `${disciplines.length} disciplina(s) encontrada(s)`;
			showResults();
		} else {
			statusEl.textContent = 'Nenhuma disciplina encontrada';
		}

	} catch (error) {
		console.error(error);
		statusEl.textContent = 'Erro ao processar PDF';
	}
}

// ============================================
// Extração de Disciplinas
// ============================================

function criaDict(lines) {
	const Disciplinas = [];
	let disciplina = null;

	for (const linha of lines) {
		if (!linha.trim()) continue;

		const linhaNome = linha.match(/\([A-Z]{3}\d{5}\)/);
		const linhaHora = linha.match(/[0-2][0-9]:[0-6][0-9]-[0-2][0-9]:[0-6][0-9]/);
		const linhaSala = linha.match(/ [A-Z]\s?\d{3} /);

		if (linhaNome) {
			if (disciplina) Disciplinas.push(disciplina);
			const nome = toTitleCase(linha.split(' ').slice(0, -2).join(' '));
			disciplina = { Nome: nome || 'SEM NOME', Sala: null, Horário: {} };
		}

		if (disciplina && linhaHora) {
			const diaAbrev = linha.substring(0, 3);
			const hora = linhaHora[0].substring(0, 5).replace(':', 'h');
			disciplina.Horário[diaAbrev] = hora;
		}

		if (disciplina && linhaSala) {
			disciplina.Sala = linhaSala[0].replace(/\s/g, '');
		}
	}

	if (disciplina) Disciplinas.push(disciplina);

	return Disciplinas;
}

function toTitleCase(str) {
	return str.replace(/\w\S*/g, txt => txt.charAt(0).toUpperCase() + txt.substring(1).toLowerCase());
}

// ============================================
// Interface
// ============================================

function showResults() {
	document.getElementById('result').classList.remove('hidden');

	const list = document.getElementById('disciplines');
	list.innerHTML = '';
	
	disciplines.forEach((d, idx) => {
		const div = document.createElement('div');
		div.className = 'discipline';
		
		let horariosHTML = '';
		Object.entries(d.Horário).forEach(([dia, hora]) => {
			horariosHTML += `
				<div class="horario-item">
					<label>${dia}: <input type="text" value="${hora}" data-idx="${idx}" data-dia="${dia}" class="horario-input"></label>
				</div>
			`;
		});
		
		div.innerHTML = `
			<div class="discipline-info">
				<label class="nome">Nome: <input type="text" value="${d.Nome}" data-idx="${idx}" data-field="nome" class="edit-input"></label>
				<label class="sala">Sala: <input type="text" value="${d.Sala || ''}" data-idx="${idx}" data-field="sala" class="edit-input"></label>
			</div>
			<div class="discipline-horarios">
				${horariosHTML}
			</div>
		`;
		list.appendChild(div);
	});

	// Atualiza array disciplinas ao editar
	document.querySelectorAll('.edit-input').forEach(input => {
		input.addEventListener('change', (e) => {
			const idx = parseInt(e.target.dataset.idx);
			const field = e.target.dataset.field;
			disciplines[idx][field === 'nome' ? 'Nome' : 'Sala'] = e.target.value;
		});
	});

	document.querySelectorAll('.horario-input').forEach(input => {
		input.addEventListener('change', (e) => {
			const idx = parseInt(e.target.dataset.idx);
			const dia = e.target.dataset.dia;
			disciplines[idx].Horário[dia] = e.target.value;
		});
	});
}

// ============================================
// Canvas - Desenho do Horário
// ============================================

async function drawSchedule() {
	document.getElementById('result-canvas').classList.remove('hidden');

	const canvas = document.getElementById('canvas');
	const ctx = canvas.getContext('2d');
	const img = new Image();

	await document.fonts.load('bold 45px Manjari');

	img.onload = () => {
		canvas.width = img.width;
		canvas.height = img.height;

		ctx.drawImage(img, 0, 0);

		const Y = {
			'Seg': Array.from({length: 5}, (_, i) => 436 + 56 * i),
			'Ter': Array.from({length: 5}, (_, i) => 740 + 56 * i),
			'Qua': Array.from({length: 5}, (_, i) => 1043 + 56 * i),
			'Qui': Array.from({length: 5}, (_, i) => 1347 + 56 * i),
			'Sex': Array.from({length: 5}, (_, i) => 1650 + 56 * i)
		};

		const Cx = { 'hora': 413, 'nome': 773, 'sala': 1192 };

		function escreve(campo, texto, centro, font) {
			ctx.font = font;
			ctx.fillStyle = 'rgb(230,230,230)';
			ctx.textAlign = 'center';
			ctx.textBaseline = 'top';
			ctx.fillText(texto, centro, campo);
		}

		function aula(campo, hora, nome, sala) {
			escreve(campo, hora, Cx.hora, 'bold 45px Manjari, Arial');
			escreve(campo, nome, Cx.nome, 'bold 45px Manjari, Arial');
			escreve(campo, sala, Cx.sala, 'bold 45px Manjari, Arial');
		}

		for (const dia in Y) {
			let ordem = 0;
			const aulasDia = disciplines
				.filter(a => a.Horário[dia])
				.sort((a,b) => parseInt(a.Horário[dia].split('h')[0]) - parseInt(b.Horário[dia].split('h')[0]));

			for (const a of aulasDia) {
				if (ordem >= 5) break;
				aula(Y[dia][ordem], a.Horário[dia], a.Nome, a.Sala || '');
				ordem++;
			}

			while (ordem < 5) {
				aula(Y[dia][ordem], '--h--', '-----', '---');
				ordem++;
			}
		}
	};

	img.src = 'Fundo base/Planner.png';
}

// ============================================
// Download
// ============================================

function downloadSchedule() {
	const canvas = document.getElementById('canvas');
	const link = document.createElement('a');
	link.href = canvas.toDataURL('image/png');
	link.download = 'horario.png';
	link.click();
}
