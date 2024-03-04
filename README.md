# API de Processamento de Imagens com AWS API Gateway e Lambda

Este guia fornece instruções passo a passo sobre como criar e configurar uma API de processamento de imagens usando AWS API Gateway e Lambda com Python.

## Pré-requisitos

Antes de começar, certifique-se de que você tem tudo o que é necessário:

- **Pyenv** - Ferramenta para gerenciar múltiplas versões do Python. A versão recomendada do Python para este projeto é a `3.11.3`. Para instalar o Pyenv, siga as [Instruções oficiais de instalação do Pyenv](https://github.com/pyenv/pyenv#installation).

- **Poetry** - Ferramenta de gerenciamento de dependências em Python. Para instalar o Poetry, siga as [Instruções oficiais de instalação do Poetry](https://python-poetry.org/docs/#installation).

- **Docker** - É necessário para criar um ambiente isolado que simula uma função Lambda para testes locais. Para instalar o Docker, siga as instruções em [Install Docker](https://docs.docker.com/). Após a instalação, você pode verificar se o Docker está rodando com o comando `docker ps`.

## Instalação e Configuração

Aqui estão os passos que você precisa seguir para configurar o seu ambiente de desenvolvimento:

1. Clonar o [Repositório Github](https://github.com/carlosfab/image-processing-api) para a sua máquina local e acessar a pasta `image-processing-api`:

   ```bash
   git clone https://github.com/carlosfab/image-processing-api
   cd image-processing-api
   ```

2. Configurar o Poetry para criar ambientes virtuais dentro do diretório do projeto.

   ```bash
   poetry config virtualenvs.in-project true
   ```

3. Configurar a versão `3.11.3` do Python com Pyenv:

   ```bash
   pyenv install 3.11.3
   pyenv local 3.11.3
   ```

4. Instalar as dependências do projeto:

   ```bash
   poetry install
   ```

5. Ativar o ambiente virtual.

   ```bash
   poetry shell
   ```

## Configurar AWS

Se ainda não possui conta na AWS, crie uma conta na AWS para poder utilizar os serviços AWS API Gateway e Lambda. Instalar e Configurar AWS CLI, A AWS CLI é uma ferramenta de linha de comando para gerenciar os serviços da AWS. Siga as [instruções oficiais para instalar a AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

Após a instalação, [configure a AWS CLI com suas credenciais](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) executando:

```bash
aws configure
```

Depois de configurar a AWS CLI, você pode obter o ID da sua conta AWS executando o seguinte comando:

```bash
aws sts get-caller-identity --query Account --output text
```

Este comando retorna o ID da sua conta AWS, que é útil para várias operações na AWS

