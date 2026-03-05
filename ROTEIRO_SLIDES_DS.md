# Roteiro de Slides - Apresentacao (2 paginas)

## Pagina 1 - Contexto, problema e solucao

### Slide 1 - Titulo
Fala sugerida:
"Nosso projeto integra Arduino e Python para monitorar temperatura em tempo real com interface grafica e comunicacao serial."

### Slide 2 - Problema
Fala sugerida:
"Precisavamos ler dados de um sensor LM35, exibir isso de forma clara para o usuario e manter a interface sempre responsiva."

### Slide 3 - Objetivos
Fala sugerida:
"Os objetivos foram: conectar na serial, ler continuamente, mostrar o ultimo valor em destaque e manter historico das leituras."

### Slide 4 - Tecnologias
Fala sugerida:
"Utilizamos Python, Tkinter para interface, PySerial para comunicacao com o Arduino e Flask para endpoints de apoio."

### Slide 5 - Arquitetura
Fala sugerida:
"Separamos o projeto em modulos: interface (`tk_interface.py`), backend serial (`serial_backend.py`), parser (`temperature_parser.py`) e sketch Arduino (`arduino_lm35_interface.ino`)."

## Pagina 2 - Demonstracao, requisitos e fechamento

### Slide 6 - Fluxo de funcionamento
Fala sugerida:
"O usuario seleciona a porta, conecta, o app le a serial periodicamente, interpreta os dados e atualiza valor principal e historico."

### Slide 7 - Requisito importante (UI sem travar)
Fala sugerida:
"Atendemos ao requisito de nao travar a interface usando `root.after(...)` para leitura periodica, sem `while True` na thread principal."

### Slide 8 - Interface em execucao
Fala sugerida:
"Aqui mostramos a tela conectada, com status, ultima linha recebida, valor em Celsius e historico das ultimas leituras."

### Slide 9 - Evidencias de teste
Fala sugerida:
"Validamos conexao, desconexao, leitura continua, parser de mensagens e modo simulacao para cenarios sem Arduino conectado."

### Slide 10 - Conclusao
Fala sugerida:
"Concluimos que o sistema atende aos requisitos da disciplina, com codigo organizado, leitura estavel e interface clara para o usuario final."

## Tempo sugerido de apresentacao
- 7 a 10 minutos no total.
- ~45 segundos por slide.

## Checklist final para o dia da banca
1. Conectar Arduino e confirmar porta serial.
2. Executar `run_all.bat`.
3. Mostrar interface recebendo dados em tempo real.
4. Mostrar print/evidencia e concluir com os requisitos atendidos.
