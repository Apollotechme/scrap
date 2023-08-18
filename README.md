# Instruções para Executar o Script com Venv

Este guia fornece instruções passo a passo para configurar um ambiente virtual (venv) e executar o script Python para consultar o Simples Nacional, passando o CNPJ como argumento.

## Pré-requisitos

Certifique-se de ter o Python instalado em seu sistema.

## Configurar o Ambiente Virtual (Venv)

1. Abra um terminal.

2. Navegue até o diretório onde você tem os arquivos do seu projeto.

3. Crie um ambiente virtual:

```bash
python -m venv venv
```

## Ative o ambiente virtual:

### No Windows:

```bash
venv\Scripts\activate
```

### No Linux ou macOS:

```bash
source venv/bin/activate
```

## Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

# Executar o Script
Após configurar o ambiente virtual, você pode executar o script Python para consultar o Simples Nacional, passando o CNPJ como argumento.

## No Windows:

```bash
python main.py <cnpj>
```

## No Linux ou macOS:

```bash
python3 main.py <cnpj>
```

Substitua <cnpj> pelo número do CNPJ que você deseja consultar.

Certifique-se de que o ambiente virtual esteja ativado antes de executar o script.

### Exemplo:

```bash
python main.py 00201139000101
```

# Desativar o Ambiente Virtual

Quando você terminar de usar o ambiente virtual, você pode desativá-lo:

```bash
deactivate
```

Isso encerrará o ambiente virtual.

## Visualizar o JSON Resultante

Após executar o script com sucesso, um arquivo chamado `dados_consulta.json` será gerado no mesmo diretório do projeto. Esse arquivo contém os dados consultados do Simples Nacional, incluindo informações sobre a empresa, situação no Simples Nacional, períodos anteriores e o PDF em base64.

Você pode visualizar o conteúdo do arquivo JSON usando um editor de texto ou visualizador JSON. Se preferir uma formatação mais legível, você pode utilizar ferramentas online ou extensões para navegadores que exibem JSON de forma estruturada.

Lembre-se de que os dados do JSON podem ser processados e analisados de várias maneiras, de acordo com suas necessidades.





