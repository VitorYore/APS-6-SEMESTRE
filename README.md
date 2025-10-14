# Sistema de Reconhecimento Facial 

![Python](https://img.shields.io/badge/python-3.10+-blue?logo=python) ![Flask](https://img.shields.io/badge/flask-2.3+-green) ![DeepFace](https://img.shields.io/badge/deepface-1.0+-orange)

Sistema de reconhecimento facial em tempo real para controle de acesso e monitoramento. Desenvolvido com Python, Flask, OpenCV e DeepFace.

---

## Pré-requisitos

* Python 3.10 ou superior
* pip
* Webcam ou câmera USB

> ⚠️ Ao instalar o `DeepFace`, todas as principais dependências de visão computacional e aprendizado profundo são automaticamente instaladas (TensorFlow, OpenCV, numpy, pandas etc).

---

## Instalação

1. Clone este repositório:

```bash
git clone <URL>
cd nomedorepositorio
```

2. Crie e ative o ambiente virtual:

```bash
python -m venv .venv
# Windows
source .venv/Scripts/activate
# Linux/Mac
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Executando o sistema

1. Execute o servidor Flask:

```bash
python app.py
```

2. Abra o navegador e acesse:

```
http://localhost:5000
```

---

## Como usar

### 1️⃣ Dashboard / Cadastro de usuários

* Vá para a seção **Dashboard**.
* Clique em **Cadastrar Usuário**.
* Preencha **nome**, **nível de acesso** e tire a **foto**.

> O sistema salva a foto na pasta `fotos/` e registra o usuário no `users.json`.

---

### 2️⃣ Recarregar embeddings

* Após cadastrar novos usuários, clique em **Recarregar Sistema**.
* Isso atualiza os embeddings de reconhecimento facial, evitando erros na detecção.

---

### 3️⃣ Monitor / Detecção

* Vá para a seção **Monitor** e clique em **Ativar Câmera**.
* O sistema verificará em tempo real as faces capturadas.
* Se o usuário for reconhecido, o status mostrará:

```
ACESSO AUTORIZADO
```

* Caso não seja reconhecido, mostrará:

```
ACESSO NEGADO
```

> O sistema suporta níveis de acesso (1 a 3) para dinamizar a autorização.

---

### 4️⃣ Logs de acesso

* Vá para a seção **Logs**.

* Confira os registros de acesso, mostrando:

  * Usuário
  * Nível de acesso
  * Status (AUTORIZADO / NEGADO)
  * Confiança da detecção

* O log mantém os registros recentes, evitando acumular dados desnecessários.

* Há opção de **apagar logs** diretamente pela interface.

---

### 5️⃣ Atualização do Dashboard

* Usuários cadastrados aparecem no dashboard.
* Qualquer modificação será refletida ao recarregar os embeddings.

---

### 6️⃣ Apagar usuário

* No dashboard, selecione o usuário e clique em **Apagar**.
* Confirme que o usuário foi removido do dashboard e do `users.json`.

---

## Estrutura do projeto

```
college/
├─ app.py                     # Arquivo principal
├─ requirements.txt           # Dependências
├─ users.json                 # Banco de usuários
├─ access_log.json            # Logs de acesso
├─ fotos/                     # Fotos dos usuários
├─ templates/                 # HTML do dashboard
├─ static/                    # CSS, JS, imagens estáticas
└─ utils/                     # Funções auxiliares
   ├─ face_recognition.py     # Verificação facial
   ├─ database.py             # Manipulação de JSON
   └─ config.py               # Configurações gerais
```

---

## Observações

* O sistema cria automaticamente pastas e arquivos se não existirem (`fotos/`, `users.json`, `access_log.json`).
* Para melhor desempenho, recomenda-se usar **câmera USB externa**.
* Logs podem ser apagados pelo dashboard para evitar acúmulo.