# Relatorio Tecnico - Projeto Interface Arduino + Python

## 1. Identificacao do projeto
- Curso: Desenvolvimento de Sistemas
- Tema: Monitoramento de temperatura com Arduino LM35, interface grafica em Python e comunicacao serial.
- Equipe: preencher com nomes e RA.
- Data: 05/03/2026.

## 2. Objetivo
Desenvolver uma aplicacao em Python capaz de receber continuamente dados de temperatura enviados pelo Arduino via porta serial, exibir essas informacoes em interface grafica Tkinter e manter a interface responsiva durante toda a execucao.

## 3. Tecnologias e bibliotecas utilizadas
- Python 3.x
- Tkinter (interface grafica)
- PySerial (comunicacao serial com Arduino)
- Flask (API auxiliar de status e temperatura)

Arquivos principais do projeto:
- `tk_interface.py`: interface principal com controles de conexao, exibicao do valor atual e historico.
- `serial_backend.py`: deteccao de portas USB/Arduino e funcoes de suporte serial.
- `temperature_parser.py`: parser das mensagens recebidas (`SENSOR=...;VALOR=...;UNIDADE=...`).
- `arduino_lm35_interface.ino`: sketch do Arduino para leitura do LM35 e envio serial.

## 4. Implementacao e funcionamento
A interface possui os componentes solicitados no enunciado:
- selecao/informacao de porta serial;
- botoes de conectar e desconectar;
- area de exibicao do ultimo valor em destaque;
- historico das leituras recebidas.

A leitura serial foi implementada sem travar a interface, utilizando agendamento periodico com `root.after(...)`. A cada ciclo, a aplicacao executa `readline()` na serial, valida o conteudo recebido e atualiza os widgets na tela.

Fluxo resumido:
1. Usuario seleciona a porta e baudrate na interface.
2. Ao conectar, a aplicacao abre `serial.Serial(porta, baud, timeout=0.1)`.
3. A rotina de leitura periodica busca novas linhas.
4. O parser extrai sensor, valor e unidade.
5. O valor em Celsius e o historico sao atualizados na tela.
6. Em desconexao, a serial e fechada com seguranca.

## 5. Padrao de dados entre Arduino e Python
O Arduino envia no formato:
`SENSOR=LM35;VALOR=xx.xx;UNIDADE=C`

Esse formato facilita validacao, exibicao e extensao futura para outros sensores.

## 6. Evidencias e testes realizados
Foram verificados os seguintes cenarios:
- conexao serial com porta valida;
- recebimento continuo das leituras;
- atualizacao do valor principal e do historico;
- desconexao sem travamento da interface;
- simulacao interna para demonstracao sem hardware.

Evidencia sugerida para entrega:
- print da tela com status conectado, ultima linha recebida e historico preenchido;
- opcional: video curto mostrando variacao em tempo real.

## 7. Conclusao
O projeto atende aos requisitos propostos para Desenvolvimento de Sistemas:
- comunicacao serial com Arduino via PySerial;
- interface Tkinter funcional com exibicao clara das leituras;
- atualizacao periodica com `root.after(...)`, mantendo responsividade da UI;
- estrutura modular para manutencao e apresentacao academica.

Como melhoria futura, pode-se adicionar exportacao do historico para CSV e grafico em tempo real.
