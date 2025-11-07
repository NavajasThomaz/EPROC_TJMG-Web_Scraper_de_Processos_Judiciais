"""
=============================================================================
EPROC TJMG - Web Scraper de Processos Judiciais
=============================================================================
Autor: Thomaz Colalillo Navajas
Versão: 1.0.0
Python: 3.13.3
Descrição: Script para captura automatizada de dados de processos judiciais
          do sistema eproc do TJMG utilizando Selenium WebDriver.
Observação: Se quiser o scrap completo, extraindo todas as informações entrar em contato: thomaznavajas@gmail.com
=============================================================================
"""

# =============================================================================
# IMPORTAÇÕES DE BIBLIOTECAS
# =============================================================================
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)

# =============================================================================
# CONFIGURAÇÕES GLOBAIS
# =============================================================================

# URL do sistema eproc TJMG
EPROC_URL = "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"

# Lista de nomes para consulta
NOMES_CONSULTA = [
    "ADILSON DA SILVA",
    "JOÃO DA SILVA MORAES",
    "RICARDO DE JESUS",
    "SERGIO FIRMINO DA SILVA",
    "HELENA FARIAS DE LIMA",
    "PAULO SALIM MALUF",
    "PEDRO DE SÁ"
]

# Timeout padrão para espera de elementos (em segundos)
DEFAULT_TIMEOUT = 15

# Diretório de saída para os resultados
OUTPUT_DIR = Path("resultados")

# Configuração de logging
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = OUTPUT_DIR / f"scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# =============================================================================
# CONFIGURAÇÃO DO SISTEMA DE LOGGING
# =============================================================================

def configurar_logging():
    """
    Configura o sistema de logging para registrar eventos do scraper.
    Logs são salvos em arquivo e exibidos no console.
    """
    # Cria o diretório de saída se não existir
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Configura o logging
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logging.info("=" * 80)
    logging.info("EPROC TJMG - Web Scraper Iniciado")
    logging.info("=" * 80)

# =============================================================================
# CLASSE PRINCIPAL DO SCRAPER
# =============================================================================

class EProcScraper:
    """
    Classe responsável pela captura de dados de processos judiciais
    do sistema eproc do TJMG.
    
    Attributes:
        driver: Instância do Selenium WebDriver
        wait: Instância do WebDriverWait para esperas explícitas
        resultados: Lista com todos os dados capturados
    """
    
    def __init__(self, headless: bool = False):
        """
        Inicializa o scraper e configura o WebDriver.
        
        Args:
            headless: Se True, executa o navegador em modo headless (sem interface gráfica)
        """
        self.driver = None
        self.wait = None
        self.resultados = {}
        self.headless = headless
        
        logging.info(f"Inicializando scraper (headless={headless})")
        self._configurar_driver()
    
    def _configurar_driver(self):
        """
        Configura e inicializa o Chrome WebDriver com as opções necessárias.
        """
        try:
            # Configurações do Chrome
            chrome_options = Options()
            
            # Modo headless (sem interface gráfica)
            if self.headless:
                chrome_options.add_argument('--headless')
            
            # Argumentos para melhor performance e estabilidade
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            # Desabilita notificações e popups
            chrome_options.add_experimental_option('prefs', {
                'profile.default_content_setting_values.notifications': 2,
                'profile.default_content_settings.popups': 0
            })
            
            # Inicializa o driver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)
            
            logging.info("WebDriver configurado com sucesso")
            
        except WebDriverException as e:
            logging.error(f"Erro ao configurar WebDriver: {e}")
            raise
    
    def _aguardar_elemento(self, by: By, value: str, timeout: int = DEFAULT_TIMEOUT) -> Optional[object]:
        """
        Aguarda até que um elemento esteja presente e visível na página.
        
        Args:
            by: Tipo de seletor (By.ID, By.XPATH, etc.)
            value: Valor do seletor
            timeout: Tempo máximo de espera em segundos
            
        Returns:
            Elemento encontrado ou None se não encontrado
        """
        try:
            elemento = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return elemento
        except TimeoutException:
            logging.warning(f"Timeout ao aguardar elemento: {value}")
            return None
    
    def _extrair_texto_seguro(self, elemento, seletor: str, by: By = By.XPATH) -> str:
        """
        Extrai texto de um elemento de forma segura, tratando exceções.
        
        Args:
            elemento: Elemento pai onde buscar
            seletor: Seletor do elemento filho
            by: Tipo de seletor
            
        Returns:
            Texto extraído ou string vazia se não encontrado
        """
        try:
            sub_elemento = elemento.find_element(by, seletor)
            return sub_elemento.text.strip()
        except NoSuchElementException:
            return ""
        except Exception as e:
            logging.debug(f"Erro ao extrair texto: {e}")
            return ""
    
    def realizar_busca(self, nome: str) -> bool:
        """
        Realiza a busca por um nome no sistema eproc.
        
        Args:
            nome: Nome da parte a ser consultada
            
        Returns:
            True se a busca foi realizada com sucesso, False caso contrário
        """
        try:
            logging.info(f"Realizando busca para: {nome}")
            
            # Acessa a página de consulta
            self.driver.get(EPROC_URL)
            time.sleep(2)  # Aguarda carregamento inicial
            
            # Aguarda e preenche o campo de nome
            campo_nome = self._aguardar_elemento(By.XPATH, '//*[@id="txtStrParte"]')
            if not campo_nome:
                logging.error("Campo de nome não encontrado")
                return False
            
            campo_nome.clear()
            campo_nome.send_keys(nome)
            time.sleep(1)
            
            # Localiza e clica no botão de pesquisar
            botao_pesquisar = self._aguardar_elemento(By.XPATH, '//*[@id="sbmNovo"]')
            if not botao_pesquisar:
                logging.error("Botão de pesquisa não encontrado")
                return False
            
            botao_pesquisar.click()
            time.sleep(3)  # Aguarda processamento da busca
            
            logging.info(f"Busca realizada com sucesso para: {nome}")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao realizar busca para {nome}: {e}")
            return False
    
    def extrair_dados_processos(self, nome_consultado: str) -> List[Dict]:
        """
        Extrai os dados dos processos encontrados na página de resultados.
        
        Args:
            nome_consultado: Nome que foi consultado
            
        Returns:
            Lista de dicionários com os dados dos processos
        """
        processos = []
        
        try:
            # Aguarda a tabela de resultados
            time.sleep(2)
            
            # Verifica se há mensagem de "nenhum processo encontrado"
            try:
                mensagem_vazia = self.driver.find_element(By.XPATH, '//*[@id="divInfraAreaTabela"]/label')
                if mensagem_vazia:
                    logging.info(f"Nenhum processo encontrado para: {nome_consultado}")
                    return []
            except NoSuchElementException:
                pass  # Não há mensagem de vazio, continua a extração
            
            # Localiza a tabela de processos
            try:
                tabela = self.driver.find_element(By.XPATH, '//*[@id="divInfraAreaTabela"]/table')
            except NoSuchElementException:
                logging.warning(f"Tabela de nomes não encontrada para: {nome_consultado}")
                return []
            
            # Extrai todas as linhas da tabela
            linhas = tabela.find_elements(By.TAG_NAME, "tr")
            logging.info(f"Encontradas {len(linhas)} linhas na tabela")
            links: List[str] = []
            for idx, linha in enumerate(linhas, 1):
                try:
                    try:
                        # Extrai as células da linha
                        celulas = linha.find_element(By.TAG_NAME, "td")
                    except:
                        logging.info("Pulando cabeçario")
                        continue
                    # Verifica se o nome procurado esta na tabela
                    nome = celulas.find_element(By.TAG_NAME, "a")
                    if nome.text != nome_consultado:
                        continue
                    
                    links.append(nome.get_attribute("href"))
                    
                except Exception as e:
                    logging.warning(f"Erro ao extrair dados da linha {idx}: {e}")
                    continue

            for i, link in enumerate(links, 1):
                processo_info = {}
                logging.info(f"Entrando no link {i}/{len(links)}")
                # Acessa a página de consulta
                self.driver.get(link)
                time.sleep(2)  # Aguarda carregamento inicial
                try:
                    tabela = self.driver.find_element(By.XPATH, '//*[@id="divInfraAreaTabela"]/table')
                except NoSuchElementException:
                    logging.warning(f"Tabela de processos não encontrada para: {nome_consultado}")

                # Extrai todas as linhas da tabela
                linhas = tabela.find_elements(By.TAG_NAME, "tr")
                for idx, linha in enumerate(linhas, 1): 
                    try:
                        # Extrai as células da linha
                        celulas = linha.find_element(By.TAG_NAME, "td")
                    except:
                        logging.info("Pulando cabeçario")
                        continue
                # Acessa o processo
                processo = celulas.find_element(By.TAG_NAME, "a")
                self.driver.get(processo.get_attribute("href"))
                time.sleep(2)
                capa = self.driver.find_element(By.XPATH, '//*[@id="fldAssuntos"]')
                divs = capa.find_elements(By.TAG_NAME, "div")
                for i, div in enumerate(divs, 1):
                    logging.info(f"Extraindo div {i}/{len(divs)}")
                    elements = div.find_elements(By.XPATH, ".//*")
                    chave:str = ""
                    valor:str = ""
                    for element in elements:
                        if element.tag_name == "label":
                            chave = element.text
                        elif element.tag_name == "span":
                            valor = element.text
                        else:
                            pass
                    processo_info[chave] = valor
                
                processos.append(processo_info)
            logging.info(f"Total de {len(processos)} processos extraídos para: {nome_consultado}")
            
        except Exception as e:
            logging.error(f"Erro ao extrair dados dos processos: {e}")
        
        return processos
    
    def processar_nome(self, nome: str) -> List[Dict]:
        """
        Processa a consulta completa para um nome específico.
        
        Args:
            nome: Nome a ser consultado
            
        Returns:
            Lista de processos encontrados
        """
        logging.info(f"Iniciando processamento para: {nome}")
        
        # Realiza a busca
        if not self.realizar_busca(nome):
            logging.error(f"Falha na busca para: {nome}")
            return []
        
        # Extrai os dados
        processos = self.extrair_dados_processos(nome)
        
        # Adiciona aos resultados gerais
        self.resultados[nome] = processos
        
        return processos
    
    def processar_todos_nomes(self, nomes: List[str]):
        """
        Processa a consulta para todos os nomes da lista.
        
        Args:
            nomes: Lista de nomes a serem consultados
        """
        total_nomes = len(nomes)
        logging.info(f"Iniciando processamento de {total_nomes} nomes")
        
        for idx, nome in enumerate(nomes, 1):
            logging.info(f"Processando {idx}/{total_nomes}: {nome}")
            
            try:
                self.processar_nome(nome)
                time.sleep(2)  # Pausa entre consultas para evitar sobrecarga
                
            except Exception as e:
                logging.error(f"Erro ao processar {nome}: {e}")
                continue
        
        logging.info(f"Processamento concluído. Total de processos: {len(self.resultados)}")
    
    def salvar_resultados(self, arquivo: str = None) -> str:
        """
        Salva os resultados capturados em arquivo JSON.
        
        Args:
            arquivo: Nome do arquivo de saída (opcional)
            
        Returns:
            Caminho do arquivo salvo
        """
        if arquivo is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            arquivo = OUTPUT_DIR / f"processos_eproc_{timestamp}.json"
        else:
            arquivo = OUTPUT_DIR / arquivo
        
        try:
            # Prepara os dados para salvamento
            dados_saida = {
                "metadata": {
                    "data_extracao": datetime.now().isoformat(),
                    "total_processos": len(self.resultados),
                    "nomes_consultados": NOMES_CONSULTA,
                    "url_fonte": EPROC_URL
                },
                "processos": self.resultados
            }
            
            # Salva em JSON com formatação legível
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados_saida, f, ensure_ascii=False, indent=2)
            
            logging.info(f"Resultados salvos em: {arquivo}")
            logging.info(f"Total de processos salvos: {len(self.resultados)}")
            
            return str(arquivo)
            
        except Exception as e:
            logging.error(f"Erro ao salvar resultados: {e}")
            raise
    
    def gerar_relatorio_resumido(self) -> Dict:
        """
        Gera um relatório resumido dos dados capturados.
        
        Returns:
            Dicionário com estatísticas dos dados
        """
        relatorio = {
            "total_processos": len(self.resultados),
            "processos_por_nome": {},
            "data_geracao": datetime.now().isoformat()
        }
        
        return relatorio
    
    def fechar(self):
        """
        Fecha o WebDriver e libera recursos.
        """
        if self.driver:
            try:
                self.driver.quit()
                logging.info("WebDriver fechado com sucesso")
            except Exception as e:
                logging.warning(f"Erro ao fechar WebDriver: {e}")

# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """
    Função principal que orquestra a execução do scraper.
    """
    # Configura o logging
    configurar_logging()
    
    # Inicializa o scraper
    scraper = None
    
    try:
        logging.info("Iniciando captura de dados do eproc TJMG")
        
        # Cria instância do scraper (headless=False para ver o navegador)
        # Altere para headless=True para execução sem interface gráfica
        scraper = EProcScraper(headless=True)
        
        # Processa todos os nomes
        scraper.processar_todos_nomes(NOMES_CONSULTA)
        
        # Salva os resultados
        arquivo_saida = scraper.salvar_resultados()
        
        # Gera e exibe relatório resumido
        relatorio = scraper.gerar_relatorio_resumido()
        logging.info("=" * 80)
        logging.info("RELATÓRIO RESUMIDO")
        logging.info("=" * 80)
        logging.info(f"Total de processos capturados: {relatorio['total_processos']}")
        logging.info("\nProcessos por nome:")
        for nome, quantidade in relatorio['processos_por_nome'].items():
            logging.info(f"  - {nome}: {quantidade} processo(s)")
        logging.info("=" * 80)
        
        logging.info(f"\n✓ Execução concluída com sucesso!")
        logging.info(f"✓ Arquivo de resultados: {arquivo_saida}")
        logging.info(f"✓ Arquivo de log: {LOG_FILE}")
        
    except KeyboardInterrupt:
        logging.warning("\nExecução interrompida pelo usuário")
        
    except Exception as e:
        logging.error(f"Erro durante a execução: {e}", exc_info=True)
        
    finally:
        # Garante que o driver seja fechado
        if scraper:
            scraper.fechar()
        
        logging.info("Scraper finalizado")

# =============================================================================
# PONTO DE ENTRADA DO SCRIPT
# =============================================================================

if __name__ == "__main__":
    main()
