# 🔍 EPROC TJMG - Web Scraper de Processos Judiciais

Sistema automatizado para captura de dados de processos judiciais do sistema eproc do Tribunal de Justiça de Minas Gerais (TJMG).

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
  - [Windows](#windows)
  - [Linux/Mac](#linuxmac)
- [Configuração](#configuração)
- [Execução](#execução)
- [Estrutura de Dados](#estrutura-de-dados)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Sobre o Projeto

Este projeto implementa um web scraper utilizando **Selenium WebDriver** para capturar automaticamente dados de processos judiciais do sistema eproc do TJMG. O sistema consulta nomes predefinidos e armazena os resultados em formato JSON.

**Características:**
- ✅ Desenvolvido em Python 3.13.3
- ✅ Utiliza Selenium WebDriver para automação
- ✅ Salva resultados em JSON estruturado
- ✅ Sistema de logging completo
- ✅ Tratamento robusto de erros
- ✅ Código comentado em nível profissional

**Nomes consultados:**
- ADILSON DA SILVA
- JOÃO DA SILVA MORAES
- RICARDO DE JESUS
- SERGIO FIRMINO DA SILVA
- HELENA FARIAS DE LIMA
- PAULO SALIM MALUF
- PEDRO DE SÁ

---

## 📦 Requisitos

### Requisitos de Sistema
- Python 3.13.3 ou superior
- Google Chrome instalado
- ChromeDriver (será instalado automaticamente via webdriver-manager ou manualmente)
- Conexão com a internet

### Bibliotecas Python
- selenium >= 4.15.0

---

## 🚀 Instalação

### Windows

#### Passo 1: Instalar Python

1. Acesse o site oficial: https://www.python.org/downloads/
2. Baixe o instalador do Python 3.13.3 para Windows
3. Execute o instalador
4. ⚠️ **IMPORTANTE**: Marque a opção "Add Python to PATH"
5. Clique em "Install Now"
6. Aguarde a conclusão da instalação

**Verificar instalação:**
```cmd
python --version
```
Deve exibir: `Python 3.13.3`

#### Passo 2: Instalar Google Chrome

1. Acesse: https://www.google.com/chrome/
2. Baixe e instale o Google Chrome
3. Anote a versão do Chrome instalada (Menu → Ajuda → Sobre o Google Chrome)

#### Passo 3: Baixar ChromeDriver

**Opção A - Automática (Recomendado):**
O ChromeDriver será gerenciado automaticamente pelo Selenium 4.x

**Opção B - Manual:**
1. Acesse: https://googlechromelabs.github.io/chrome-for-testing/
2. Baixe o ChromeDriver compatível com sua versão do Chrome
3. Extraia o arquivo `chromedriver.exe`
4. Adicione o diretório ao PATH do Windows ou coloque na pasta do projeto

#### Passo 4: Criar Ambiente Virtual

Abra o **Prompt de Comando** ou **PowerShell** e navegue até a pasta do projeto:

```cmd
cd C:\caminho\para\o\projeto
```

Crie o ambiente virtual:
```cmd
python -m venv venv
```

Ative o ambiente virtual:
```cmd
# Prompt de Comando
venv\Scripts\activate

# PowerShell
venv\Scripts\Activate.ps1
```

⚠️ **Nota para PowerShell**: Se encontrar erro de execução de scripts, execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Passo 5: Instalar Dependências

Com o ambiente virtual ativado:
```cmd
pip install --upgrade pip
pip install selenium
```

#### Passo 6: Executar o Scraper

```cmd
python eproc_scraper.py
```

---

### Linux/Mac

#### Passo 1: Instalar Python

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv python3-pip
```

**Fedora/RHEL:**
```bash
sudo dnf install python3.13 python3-pip
```

**macOS (usando Homebrew):**
```bash
brew install python@3.13
```

**Verificar instalação:**
```bash
python3 --version
```

#### Passo 2: Instalar Google Chrome

**Ubuntu/Debian:**
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
```

**Fedora:**
```bash
sudo dnf install google-chrome-stable
```

**macOS:**
```bash
brew install --cask google-chrome
```

#### Passo 3: Instalar ChromeDriver

**Linux (Automático):**
```bash
# O Selenium 4.x gerencia automaticamente o ChromeDriver
# Mas você pode instalar manualmente se preferir:
sudo apt install chromium-chromedriver  # Ubuntu/Debian
```

**macOS:**
```bash
brew install chromedriver
```

#### Passo 4: Criar Ambiente Virtual

Navegue até a pasta do projeto:
```bash
cd /caminho/para/o/projeto
```

Crie o ambiente virtual:
```bash
python3 -m venv venv
```

Ative o ambiente virtual:
```bash
source venv/bin/activate
```

#### Passo 5: Instalar Dependências

```bash
pip install --upgrade pip
pip install selenium
```

#### Passo 6: Executar o Scraper

```bash
python3 eproc_scraper.py
```

---

## ⚙️ Configuração

### Configurações Disponíveis

Edite o arquivo `eproc_scraper.py` para personalizar:

```python
# Modo headless (sem interface gráfica)
scraper = EProcScraper(headless=True)  # True = sem janela do navegador

# Timeout de espera (em segundos)
DEFAULT_TIMEOUT = 15

# Adicionar/remover nomes para consulta
NOMES_CONSULTA = [
    "NOME COMPLETO 1",
    "NOME COMPLETO 2",
    # ...
]
```

### Estrutura de Diretórios

Após a primeira execução:
```
projeto/
│
├── eproc_scraper.py          # Script principal
├── README.md                  # Este arquivo
├── venv/                      # Ambiente virtual (não versionar)
│
└── resultados/                # Criado automaticamente
    ├── processos_eproc_YYYYMMDD_HHMMSS.json
    └── scraper_YYYYMMDD_HHMMSS.log
```

---

## ▶️ Execução

### Execução Padrão

```bash
# Windows
python eproc_scraper.py

# Linux/Mac
python3 eproc_scraper.py
```

### Execução em Modo Headless

Para executar sem abrir o navegador (útil para servidores):

1. Edite `eproc_scraper.py`
2. Localize a linha: `scraper = EProcScraper(headless=False)`
3. Altere para: `scraper = EProcScraper(headless=True)`
4. Execute normalmente

### Saída Esperada

Durante a execução, você verá logs como:

```
2025-11-06 10:30:00 - INFO - ================================================================================
2025-11-06 10:30:00 - INFO - EPROC TJMG - Web Scraper Iniciado
2025-11-06 10:30:00 - INFO - ================================================================================
2025-11-06 10:30:01 - INFO - Inicializando scraper (headless=False)
2025-11-06 10:30:03 - INFO - WebDriver configurado com sucesso
2025-11-06 10:30:03 - INFO - Iniciando processamento de 7 nomes
2025-11-06 10:30:03 - INFO - Processando 1/7: ADILSON DA SILVA
...
```

---

## 📊 Estrutura de Dados

### Formato do JSON de Saída

```json
{
  "metadata": {
    "data_extracao": "2025-11-06T10:30:00.000000",
    "total_processos": 15,
    "nomes_consultados": [
      "ADILSON DA SILVA",
      "JOÃO DA SILVA MORAES",
      ...
    ],
    "url_fonte": "https://eproc-consulta-publica-1g.tjmg.jus.br/..."
  },
  "processos": [
    {
      "nome_consultado": "ADILSON DA SILVA",
      "numero_processo": "0000000-00.0000.0.00.0000",
      "polo_ativo": "Nome do Autor",
      "polo_passivo": "Nome do Réu",
      "classe": "Procedimento Comum",
      "assunto": "Dano Material",
      "orgao_julgador": "1ª Vara Cível",
      "data_captura": "2025-11-06T10:30:15.000000",
      "url_consulta": "https://eproc-consulta-publica-1g.tjmg.jus.br/..."
    },
    ...
  ]
}
```

### Campos Capturados

| Campo | Descrição |
|-------|-----------|
| `nome_consultado` | Nome que foi pesquisado no sistema |
| `numero_processo` | Número único do processo judicial |
| `polo_ativo` | Parte autora do processo |
| `polo_passivo` | Parte ré do processo |
| `classe` | Classificação do processo |
| `assunto` | Assunto principal do processo |
| `orgao_julgador` | Vara ou órgão responsável |
| `data_captura` | Data e hora da captura dos dados |
| `url_consulta` | URL do sistema consultado |

---

## 🔧 Troubleshooting

### Problema: "python não é reconhecido como comando"

**Windows:**
- Reinstale o Python marcando "Add Python to PATH"
- Ou adicione manualmente: `C:\Python313\` e `C:\Python313\Scripts\` ao PATH

**Linux/Mac:**
- Use `python3` ao invés de `python`

### Problema: "chromedriver não encontrado"

**Solução 1 - Atualizar Selenium:**
```bash
pip install --upgrade selenium
```

**Solução 2 - Instalar manualmente:**
- Baixe o ChromeDriver compatível com sua versão do Chrome
- Coloque na pasta do projeto ou adicione ao PATH

### Problema: "Timeout ao aguardar elemento"

**Causas possíveis:**
- Conexão lenta com a internet
- Site do TJMG fora do ar ou lento
- Estrutura da página foi alterada

**Soluções:**
- Aumente o `DEFAULT_TIMEOUT` no código
- Verifique sua conexão com a internet
- Verifique se o site está acessível: https://eproc-consulta-publica-1g.tjmg.jus.br/

### Problema: "Permission denied" ao ativar venv (Linux/Mac)

```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

### Problema: Erro de execução de scripts no PowerShell

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problema: Chrome não abre ou fecha imediatamente

**Verifique:**
1. Google Chrome está instalado corretamente
2. Versão do ChromeDriver é compatível com a versão do Chrome
3. Tente executar em modo não-headless para ver erros visuais

### Problema: "No module named 'selenium'"

**Certifique-se de:**
1. O ambiente virtual está ativado
2. Instalou as dependências: `pip install selenium`

---

## 📝 Logs

Todos os logs são salvos em:
```
resultados/scraper_YYYYMMDD_HHMMSS.log
```

Os logs incluem:
- ✅ Informações de execução
- ⚠️ Avisos e alertas
- ❌ Erros e exceções
- 📊 Estatísticas de captura

---

## 🛡️ Boas Práticas

1. **Respeite o sistema**: Não execute o scraper com frequência excessiva
2. **Verifique os dados**: Sempre valide os dados capturados
3. **Mantenha atualizado**: Atualize o Selenium e ChromeDriver regularmente
4. **Use logs**: Consulte os logs para diagnosticar problemas
5. **Backup**: Faça backup dos arquivos JSON gerados

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais e de avaliação técnica.

---

## 👨‍💻 Suporte

Para problemas ou dúvidas:
1. Verifique a seção [Troubleshooting](#troubleshooting)
2. Consulte os logs em `resultados/`
3. Verifique se o site do TJMG está acessível

---

## 📚 Referências

- [Documentação Selenium](https://www.selenium.dev/documentation/)
- [Python Official Documentation](https://docs.python.org/3/)
- [TJMG eproc](https://eproc-consulta-publica-1g.tjmg.jus.br/)

---

**Desenvolvido com ❤️ para captura automatizada de dados judiciais**