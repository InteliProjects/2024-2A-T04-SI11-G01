# Análise Financeira

Uma análise financeira é um estudo seguindo algumas metodologias/frameworks que auxiliam na visualização de quanto custaria uma certa operação, e assim entender se é:

I - Viável;  
II - Compensação entre investimento e retorno. 

Dessa forma, quem executa o projeto tem mais informações para pensar em escopo e timing para desenvolvimento.

No caso do modelo de deep learning com a Aegea, estaremos desenvolvendo uma tecnologia pontual que, se funcionar com o desempenho do nosso modelo, gerará vários argumentos a favor, pois é um número expressivo. No entanto, para termos argumentos mais conclusivos, sugerimos à Aegea que:

1. Crie um KPI de: **Aproveitamento**, visita na casa de um cliente/encontro de fraude.
2. **Média do valor ganho em fraudes encontradas**.

Dessa forma, conseguiríamos enxergar o verdadeiro valor da solução. Por exemplo, poderíamos fazer um teste A/B onde verificaríamos se, de fato, com o modelo rodando, aumentamos o aproveitamento (1º KPI). Multiplicado pelo valor gasto, podemos determinar até que ponto vale a pena um investimento intensivo nessa solução.

## Custos e Estrutura

Por sorte, a solução que propomos não envolve muitos custos, mas, se mostrar uma ferramenta valiosa (sendo esse valor mostrado com a lógica acima), pode ser incrementado com o aumento de recursos. Sendo assim, nosso custo é separado em 3 partes:

1. **Pessoas**
2. **Tempo**
3. **Infraestrutura**

(Sendo 1 e 2 quase que integrados)

### Pessoas e Tempo

Para melhorar nosso modelo a fim de ficar pronto para entrar em produção, teríamos que contar com:

- **I - Cientista de dados**
- **II - Engenheiro de dados**

Poderíamos utilizar colaboradores que já estão na Aegea. 

#### Estimativa de Tempo:

Usando um guesstimation, estimamos que em **3 semanas** teríamos o modelo pronto para entrar em produção. 

#### Custo com Pessoas:

Considerando um salário de **R$ 10.000** para ambos os cargos (conforme [salário de cientista de dados](https://www.salario.com.br/profissao/cientista-de-dados-data-scientist/)), teríamos um custo de **R$ 15.000** com pessoas.

### Infraestrutura

A parte de infraestrutura necessária para rodar o modelo de deep learning envolveria:

- **Servidores/Cloud Computing:** Provavelmente será necessário utilizar serviços de cloud computing para garantir o processamento dos dados de forma escalável. Pode ser usada uma plataforma como AWS, Google Cloud ou Azure. Para deep learning, são comuns máquinas com GPUs dedicadas, essenciais para o treinamento e inferência de modelos de machine learning. Custos podem variar de acordo com a intensidade do uso, mas podemos estimar entre **R$ 2.000 a R$ 5.000 por mês** para rodar os modelos de forma eficiente, dependendo da carga.

- **Armazenamento de Dados:** O armazenamento de dados sobre fraudes encontradas, clientes e outros registros pode ser feito em um serviço de banco de dados na nuvem. Utilizar serviços como AWS S3 ou Google Cloud Storage pode ser uma opção mais econômica para o volume de dados. Podemos estimar um custo de **R$ 500 a R$ 1.500 por mês**.

- **Ferramentas de Monitoramento e Gerenciamento:** Para acompanhar a performance dos modelos em produção, é necessário utilizar ferramentas de monitoramento e análise de logs. Isso poderia incluir soluções como **Datadog** ou **Prometheus**. Estimativa de custo: **R$ 300 a R$ 1.000 por mês**, dependendo da escala.

### Total estimado para Infraestrutura:

Entre **R$ 2.800 a R$ 7.500 por mês**, com possibilidade de aumentar conforme a necessidade de escala.

## Resumo dos Custos Totais:

- **Pessoas:** R$ 15.000 (cientista e engenheiro de dados por 3 semanas)
- **Infraestrutura:** R$ 2.800 a R$ 7.500 por mês

Assim, o custo inicial para desenvolver e rodar o modelo de deep learning por 1 mês ficaria em torno de **R$ 17.800 a R$ 22.500**, considerando as três semanas estimadas para o desenvolvimento e a infraestrutura para suportar o modelo.

## Conclusão

Com essa estrutura de custos, e utilizando os KPIs sugeridos (aproveitamento das visitas e valor médio de fraudes encontradas), a Aegea pode calcular o **ROI** (Retorno sobre o Investimento) e validar se o projeto de deep learning justifica o investimento, observando se o aumento no aproveitamento compensa os custos.
