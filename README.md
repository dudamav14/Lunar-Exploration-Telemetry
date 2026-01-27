#  Lunar Exploration Telemetry Infrastructure

Este projeto implementa uma **infraestrutura de telemetria resiliente** projetada para monitorar um *Rover* na superfície lunar. A arquitetura foca no desacoplamento entre a geração de dados e sua persistência, garantindo a integridade das informações em condições extremas de rede[cite: 30, 31, 33].

---

##  Arquitetura do Sistema

O pipeline de dados segue uma abordagem de *Systems-of-Systems*:

* **Producers (Sensores):** Três aplicações Python independentes que simulam o hardware do Rover e enviam dados em regime de *burst* (rajadas).
* **Message Broker (Kafka):** Configurado em modo **KRaft** (sem Zookeeper) para garantir a durabilidade e ordenação das mensagens no porto `9092`.
* **Ingestion Agent (Telegraf):** Atua como o único *link* entre a rede do Rover e o Controle de Missão, realizando o *batching* dos dados.
* **Time Series Database (InfluxDB):** Armazena os dados históricos e processa a lógica de alertas via scripts *Flux*.

---

##  Isolamento de Rede

O projeto implementa **segregação de rede rigorosa** para mimetizar o *air gap* espacial:

1.  **`deep-space-net`**: Rede isolada onde os produtores comunicam com o broker Kafka.
2.  **`ground-control-net`**: Rede segura para comunicação entre o Telegraf e a base de dados do Controle de Terra.
3.  **Gateway Bridge**: O serviço `telegraf-gateway` é o único componente conectado a **ambas** as redes, servindo de ponte controlada.

---

##  Como Executar

### 1. Pré-requisitos
* **Docker** e **Docker Compose** instalados.
* Arquivo `.env` configurado com as credenciais do InfluxDB.

### 2. Inicialização
Para construir e iniciar todos os serviços simultaneamente, execute:
```bash
docker compose up --build
```

### 3. Acesso ao Painel de Controle
URL: http://localhost:8086.

* **Organização**: esa-sic.
* **Bucket**: lunar-mission.
* **Token**: Configurado via variável `${DOCKER_INFLUXDB_INIT_ADMIN_TOKEN}` no .env.

---

##  Monitorização e Alertas
### Painel de Controle de Missão (Dashboard)
O sistema inclui visualizações customizadas conforme os requisitos de missão:

* **Gauges**: Monitorização da Pressão da Cabine (ECLSS).
* **Heatmaps**: Correlação entre RPM do Motor e Tração das Rodas.
* **Single Stats**: Exibição do valor máximo de Radiação.
* **Graphs**: Histórico da Voltagem da Bateria com linha de limite crítico em 20V.

### Lógica de Alertas (Flux Scripts)
Os scripts automatizam a resposta a incidentes críticos:

* **`alert_mobility.flux`**: Detecta descarga crítica da bateria (abaixo de 20V).
* **`alert_eclss.flux`**: Alerta sobre níveis de radiação (Normal, Voo Comercial ou Crítico).
* **`alert_hga.flux`**: Monitora a qualidade do sinal (SNR) e latência da antena.

---

 ## Estrutura do Repositório
* `producers/`: Código-fonte dos simuladores e Dockerfile único.
* `telegraf/`: Configuração do agente (telegraf.conf) com hostname lunar-gateway.
* `flux/`: Scripts de processamento e alertas em linguagem Flux.
* `dashboard/`: Arquivo dashboard.json para importação no InfluxDB.
* `compose.yaml`: Definição de todos os serviços e volumes persistentes para Kafka e InfluxDB.

---
Nota: O sistema utiliza um limite de buffer de 10.000 métricas no Telegraf para suportar interrupções na conexão com o banco de dados sem perda de dados.

## Desenvolvido por: Maria Eduarda Teixeira Mendes e Francisco Gil Valverde \ Unidade Curricular: Computing Systems and Infrastructure (LIACD 2025-2026)
