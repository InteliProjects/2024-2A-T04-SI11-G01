# Introdução

Esse documento é um guia, relacionado a como executar a interface para o usuário de nossa solução.

Com a interface, é possível realizar tanto a predição de possíveis fraudadores quanto realizar uma análise do cenário de fraudes.

Segue abaixo o guia de como iniciar o Docker:

# Como Executar

Para facilitar a execução da nossa interface, foi criada uma estrutura de Docker que simplifica a instalação das dependências e a execução do projeto. Essa abordagem também possibilita um possível deploy da solução de forma rápida e eficiente, sem a necessidade de configurar o ambiente manualmente.

Lembrando que, para iniciar o Docker com esse guia, você precisará de um sistema Linux com Docker e Python instalados.

## Passo a Passo

### 1. Construir a Imagem Docker:

Navegue até o diretório raiz do projeto, onde está localizado o arquivo `Dockerfile`, e execute o comando abaixo para construir a imagem Docker:

```bash
docker build -t meu_projeto_python .
```

### 2. Executar o Container:

Após construir a imagem do Docker, execute o seguinte comando para iniciar o container:

```bash
docker run --name interface_ia -d -p 8501:8501 meu_projeto_python
```

### 3. Acessar a Interface:

Com o container em execução, você pode acessar a interface através do seu navegador, no endereço:

```bash
http://localhost:8501
```

Com esses passos simples, sua interface estará pronta para ser utilizada!


# Como Executar a API Flask

Para executar a API Flask, siga as etapas abaixo:

## Passo a Passo

### Instalar as Dependências:

Instale as dependências necessárias usando `pip`. No diretório do seu projeto, execute:

```bash
pip install -r requirements.txt
```

### Executar a Aplicação Flask:

Para iniciar a API Flask, você pode usar o seguinte comando:

```bash
python api_service.py
```

### Acessar a API:

Com a aplicação em execução, você pode acessar a API através do seu navegador ou de uma ferramenta como o Postman. O endereço padrão será:

```
http://localhost:5000
```
E assim o modelo está pronto para ser utilizado via api !, o input deve ser no formato do padrão da Aegea.
