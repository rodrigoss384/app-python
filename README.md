# Desafio Técnico SRE/DevSecOps

## Visão Geral do Projeto

<br>
Demonstrar a habilidade de orquestrar uma aplicação web simples e seu banco de dados usando Docker Compose para um ambiente de desenvolvimento local.


## Tecnologias Utilizadas


* Docker & Docker Compose
* Kubernetes (Minikube)
* GitHub Actions (CI/CD)
* Prometheus (Métricas)
* Grafana (Dashboards)


<br>


## Como Executar este Projeto
<br>
Neste cenário, o foco é construir um ambiente com dois containeres: Um para uma 

aplicação web Python e outro para um banco de dados PostgreSQL. A aplicação Python deve ser capaz de se conectar e interagir com o banco de dados. 

As tarefas envolvem:
<br>
1. Criar um Dockerfile para a aplicação Python, definindo seu ambiente e dependências.

2. Desenvolver um arquivo docker-compose.yml para definir, configurar e interligar os serviços da aplicação e do banco de dados.

3. Garantir que a aplicação seja executável e testável localmente, validando a configuração do Docker Compose e a conectividade entre os contêineres.


<br>

---



## Cenário 1: Aplicação Multi-Container com Docker Compose


### Objetivo

<br>

Containerizar uma aplicação Python e um banco de dados PostgreSQL, orquestrando-os com Docker Compose.

<br>

### Como Executar

<br>

1. Faça um clone deste repositório na sua máquina local.
2. Navegue até a raiz do projeto.
3. Crie um Dockerfile como o demonstrado neste repositório, contendo as dependências para a imagem funcionar.
4. Crie um arquivo `.env` para guardar as credenciais de conexão com o banco de dados, como prática de segurança.
5. Crie o arquivo `docker-compose.yml`
6. Após isso execute o comando: `docker-compose up --build`

<br>

### Verificação

<br>

Acesse `http://localhost:5000` para verificar se o Servidor Web está respondendo, e `http://localhost:5000/health` para verificar se o banco de dados está respondendo. 
A resposta esperada é `{"status": "ok"}`.

<br>

##### Banco de Dados:

![Banco](https://drive.google.com/uc?export=view&id=1GZ6DX7zgTHYjETAVUHXOTTqdo-UHB11I)

<br>


#### OBS: No meu navegador não apareceu o localhost porque eu fiz todo processo usando uma máquina virtual ao invés da minha própria máquina.


<br>


##### Servidor Web:


![Servidor](https://drive.google.com/uc?export=view&id=1zW9WisTL2ZfJSWtqPmqOVloabHTBn8yO)

---

<br>

## Cenário 2: Deploy no Kubernetes com ConfigMap e Secret


### Objetivo

<br>

Implantar a aplicação em um cluster Kubernetes local (Minikube), gerenciando configurações com ConfigMaps e Secrets.

### Passos para o Deploy
1. Consulte a documentação oficial do Minikube para realizar a instalação correta: [Minikube](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download)
1. Inicie o Minikube: `minikube start`
2. Por padrão o Minikube executa seu próprio ambiente isolado do Docker na sua máquina, por isso ele não vai conseguir ver
a imagem construída com o Docker Compose, para resolver isso conecte-se no terminal do docker e execute o comando:
`eval $(minikube -p minikube docker-env)`
3. Construa a imagem local: `docker build -t app-python:v1 .`
4. Carregue a imagem para o cluster Minikube: `minikube image load app-python:v1`
5. Crie o Secret (Usado pra codificar credenciais) e o ConfigMap (Usado para dados sensíveis).
6. Crie os arquivos YAML com as configurações desejadas.
7. Aplique todos os manifestos: `kubectl apply -f diretorio-dos-arquivos-yaml/`

### Verificação
1. Obtenha a URL do serviço: `minikube service nome-do-service --url`
2. Com esse comando você reberá na tela um caminho para verificar a integridade do servidor web e do banco de dados `/health` no navegador. A resposta esperada é `{"status": "ok"}`.

<br>

![Minikube](https://drive.google.com/uc?export=view&id=1v5IkRmWsSOC-dr0ldHdf175Doi6CkVIt)


---

<br>

### Atualização do ConfigMap

##### Objetivo

Demonstrar como atualizar o ConfigMap sem reiniciar os pods, por isso vou alterar o valor da variável de ambiente que criei.

1. Abra o arquivo `configmap-app.yml`
2. Mude o valor da variável `APP_MODE` de `development` para `production`
3. Aplique nome o arquivo `configmap-app.yml` com o comando `kubectl apply -f configmap-app.yml`

<br>

Neste momento, os pods ainda estão rodando com o valor `development`

Para mudar o valor de uma variável de ambiente do ConfigMap sem problemas basta usar o `rollout` com o comando `kubectl rollout restart deployment deploy-app`

Este comando faz o controle dessa atualização dos pods de forma controlada, porque quando a gente usa o ConfigMap com variáveis de ambiente, não
é possível atualizar os valores no Pod sem reiniciá-lo elas são carregaddas somente na inicialização do container.

<br>

##### Você pode observar que os pods antigos vão sendo trocados por novos substituindo o valor da variável APP_MODE.

<br>

![ConfigMap](https://drive.google.com/uc?export=view&id=1s8qALC_lsqNb1f7qVqat3_y3d7Puix-I)

<br>

---

## Cenário 3: Pipeline CI/CD com GitHub Actions

### Objetivo
Automatizar o build, teste e publicação da imagem Docker usando GitHub Actions.

### Funcionamento
O pipeline é definido em `.github/workflows/main-pipeline.yml` e é acionado automaticamente a cada `push` na branch `main`.

### Verificação

<br>

![Pipeline](https://drive.google.com/uc?export=view&id=1OSYs--yqNkl8gfj8BDMcvqYSUiwpxW8r)

<br>

---

## Cenário 4: Logs e Monitoramento

### Objetivo
Propor e implementar uma solução de monitoramento de métricas e logs para a aplicação.

### Arquitetura
A solução implementada utiliza o stack PG (Prometheus e Grafana) rodando em uma VM totalmente independente da aplicação.
* **Métricas:** O `Node Exporter` expõe as métricas da VM da aplicação, que são coletadas pelo `Prometheus`
* Configurei um `docker-compose.yml` totalmente separado do que foi utilizado para a aplicação para sustentar também o `Grafana`
  que é o responsável pelo Dashboard.
* Os arquivos da stack de monitoramento estão definidos em `stack-monitoramento` onde também está o diretório para armazenamento
  persistente do `Grafana` e o arquivo de configuração do `Prometheus`

<br>

### Verificação
Os resultados podem ser visualizados no Grafana:
* **Métricas:** Dashboard "Node Exporter Full" (ID `1860`).

<br>

![Grafana](https://drive.google.com/uc?export=view&id=1925cXwdm0zBmB0T0HeYiWr0jVj04wB_C)

<br>

### Identificação de Situações Críticas

#### O cenário ideal seria configurando alertas no Prometheus com base em condições como:

* **Consumo de CPU acima de 80% por mais de 5 minutos.**
* **Uso de memória maior que 85%.**
* **Erro no HTTP request maior que 5$ nos últimos 10 minutos.**
* **Aplicação offline ou endpoint sem resposta.**

<br>

---

### Validação

Para validação que o monitoramento funciona corretamente:

* **Simular testes de carga e stress para verificar se os alertas serão disparados corretamente.**
* **Verificar os logs do Prometheus e trabalhar com a possibilidade de implementar futuramente o Alertmanager nesta solução.**
* **Utilizar o Grafana para checar se os gráficos refletem os testes em tempo real.**
