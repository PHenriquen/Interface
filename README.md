# Interface Arduino + Python

Projeto para ler temperatura do LM35 no Arduino, mostrar no Tkinter em tempo real e disponibilizar por API Flask.

## Estrutura do projeto

- `tk_interface.py`: interface principal (Tkinter)
- `serial_backend.py`: leitura serial, simulacao e deteccao de Arduino USB
- `temperature_parser.py`: parser das linhas recebidas e conversao para Celsius
- `api.py`: API Flask (`/api/temperature` e `/api/status`)
- `data_source.py`: fonte de dados da API (serial + fallback simulacao)
- `arduino_lm35_interface.ino`: sketch do Arduino (referencia)
- `run_all.bat`: inicia API + interface no Windows
- `requirements.txt`: dependencias Python

## Requisitos

- Windows 10/11
- Python 3.10+ instalado e no PATH
- Arduino conectado por USB (com sketch ja gravado)
- Dependencias Python: `flask`, `pyserial`

## Instalacao (novo PC)

1. Abra o terminal na pasta do projeto.
2. Crie ambiente virtual:

```powershell
python -m venv .venv
```

3. Ative o ambiente virtual:

```powershell
.venv\Scripts\activate
```

4. Instale dependencias:

```powershell
pip install -r requirements.txt
```

## Execucao

### Opcao 1: API + Interface juntas (recomendado)

```powershell
run_all.bat
```

### Opcao 2: Rodar separado

Interface:

```powershell
python tk_interface.py
```

API:

```powershell
python api.py
```

## Como usar na apresentacao

1. Conecte o Arduino por USB.
2. Execute `run_all.bat`.
3. Na interface, clique `Atualizar portas`.
4. No painel **Conexao USB (Arduino)**:
- escolha a porta detectada
- deixe `Baudrate` em `9600`
- clique `Conectar`
5. Verifique leitura em tempo real em Celsius.
6. Mostre a API no navegador:
- `http://127.0.0.1:5000/api/status`
- `http://127.0.0.1:5000/api/temperature`

## Interface (Tkinter)

- Painel de conexao serial separado do painel de simulacao.
- Simulacao fica no canto direito inferior (`Iniciar` / `Parar`).
- Exibicao sempre em Celsius na tela.
- Deteccao automatica de portas USB com prioridade para Arduino.

### Testar sem Arduino (modo simulacao)

1. Abra `python tk_interface.py`.
2. No painel **Simulacao**, escolha o intervalo.
3. Clique `Iniciar`.

## API

Endpoint de status:

```http
GET /api/status
```

Resposta esperada:

```json
{"status": "online"}
```

Endpoint de temperatura:

```http
GET /api/temperature
```

Resposta exemplo:

```json
{"temperature": 27.5, "unit": "C", "source": "serial", "detail": "porta COM4"}
```

## Modos da API (variavel de ambiente)

`TEMP_SOURCE_MODE`:

- `auto` (padrao): tenta serial e cai para simulacao se falhar
- `serial`: exige leitura serial (sem fallback)
- `sim`: sempre simulado

Variaveis opcionais:

- `ARDUINO_PORT`: se vazio, usa deteccao automatica
- `ARDUINO_BAUD`: padrao `9600`
- `ARDUINO_TIMEOUT`: padrao `1.0`
- `ARDUINO_READ_WINDOW_S`: padrao `3.0`

Exemplos no PowerShell:

```powershell
$env:TEMP_SOURCE_MODE="sim"
python api.py
```

```powershell
$env:TEMP_SOURCE_MODE="serial"
$env:ARDUINO_PORT="COM3"
$env:ARDUINO_BAUD="9600"
python api.py
```

Voltar para auto-detect de porta:

```powershell
$env:ARDUINO_PORT=""
```

## Formato serial aceito

Formato estruturado (preferido):

```text
SENSOR=LM35;VALOR=26.40;UNIDADE=C
```

Tambem aceita formato legado com texto (ex.: `Celsius: 26.4`) e numero puro.

## Solucao de problemas (check rapido)

1. `pyserial nao instalado`
- Rode: `pip install -r requirements.txt`

2. Porta nao aparece
- Clique `Atualizar portas`
- Troque cabo USB (usar cabo de dados)
- Teste outra porta USB do PC

3. Nao conecta na serial
- Feche o Serial Monitor da IDE Arduino
- Confirme baudrate `9600`
- Tente outra COM listada

4. API responde simulacao em vez de serial
- Verifique se Arduino esta conectado
- Deixe `TEMP_SOURCE_MODE=auto` ou `serial`
- Limpe porta forcada: `$env:ARDUINO_PORT=""`

5. `python` nao reconhecido
- Reinstale Python e marque opcao "Add Python to PATH"

## Checklist final para apresentar em outro PC

1. Python 3.10+ instalado
2. Projeto copiado
3. `python -m venv .venv`
4. `.venv\Scripts\activate`
5. `pip install -r requirements.txt`
6. Arduino conectado
7. `run_all.bat`
8. Interface conectada em `9600`
9. API abrindo `/api/status` e `/api/temperature`
