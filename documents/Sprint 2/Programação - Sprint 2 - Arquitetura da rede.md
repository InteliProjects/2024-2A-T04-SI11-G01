### Documentação da Arquitetura da Rede Neural

#### 1. **Introdução**

Esta documentação descreve a arquitetura de uma Rede Neural Artificial (RNA) projetada para a detecção de fraudes. A rede é do tipo Feedforward Neural Network (FNN) e consiste em uma sequência de camadas densas, cada uma conectada totalmente à próxima, com o objetivo de capturar padrões complexos e não lineares presentes nos dados. Porém, é importante lembrar que a alteração dessa arquitetura pode ser necessária para otimizar o desempenho do modelo, de acordo com a natureza específica do problema e dos dados.

#### 2. **Descrição da Arquitetura**

![Arquitetura da Rede Neural](https://github.com/Inteli-College/2024-2A-T04-SI11-G01/blob/main/assets/arquitetura.png)

A rede neural apresentada é composta por:

- **Camada de Entrada**: Recebe o vetor de características `x` do dataset. Este vetor contém todos os atributos relevantes para a detecção de fraudes. Não há função de ativação aplicada nesta camada, pois seu papel é simplesmente fornecer os dados para a primeira camada oculta.

- **Camadas Densas (Hidden Layers)**: A rede possui cinco camadas densas (ocultas) com tamanhos decrescentes:
  - Primeira camada densa: 256 neurônios
  - Segunda camada densa: 128 neurônios
  - Terceira camada densa: 64 neurônios
  - Quarta camada densa: 32 neurônios
  - Quinta camada densa: 16 neurônios
  
  Cada uma dessas camadas utiliza uma função de ativação, comumente a ReLU (Rectified Linear Unit), para introduzir não-linearidades no modelo, permitindo que a rede capture relações complexas nos dados.

- **Camada de Saída**: Contém um único neurônio que aplica a função de ativação sigmoide (`σ`). O resultado dessa camada é uma probabilidade entre 0 e 1, que indica a probabilidade de uma transação ser fraudulenta ou não. Um limiar de decisão pode ser aplicado para classificar as transações com base nessa probabilidade. Se a probabilidade for maior que o limiar, a transação é classificada como fraudulenta; caso contrário, é considerada legítima.

#### 3. **Justificativa da Arquitetura**

A escolha desta arquitetura baseia-se em várias considerações fundamentais:

- **Camadas Densas**: As camadas densas são essenciais para a modelagem de dados tabulares, onde as interações entre variáveis não são necessariamente lineares. A escolha por múltiplas camadas oculta reflete a necessidade de extrair e combinar padrões em diferentes níveis de abstração.

- **Tamanho Decrescente das Camadas**: A redução gradual do número de neurônios em cada camada oculta (256, 128, 64, 32, 16) segue uma prática comum em redes neurais, onde a arquitetura piramidal ajuda na compressão dos dados, eliminando informações redundantes e concentrando-se nas características mais relevantes para a tomada de decisão na camada final.

- **Função de Ativação Sigmoide na Saída**: A função sigmoide é apropriada para problemas de classificação binária, como a detecção de fraudes, porque mapeia qualquer entrada para um valor entre 0 e 1, interpretável como uma probabilidade.

#### 4. **Justificativa com Base na Literatura**

De acordo com a literatura existente, a arquitetura de uma rede neural para tarefas de classificação geralmente segue as seguintes diretrizes:

- **Número de Camadas e Neurônios**: A escolha do número de camadas e neurônios em cada camada é crítica para o desempenho da rede. Pesquisas mostram que redes mais profundas (com mais camadas) são capazes de aprender representações mais complexas, embora possam sofrer de sobreajuste se não forem bem reguladas. A estrutura piramidal (decrescente) ajuda na diminuição gradual da dimensionalidade, evitando a retenção de ruídos nos dados.

- **Funções de Ativação**: A ReLU é amplamente adotada devido à sua simplicidade e eficiência computacional, além de mitigar o problema do gradiente desaparecido, o que é comum em funções de ativação sigmoides em camadas intermediárias. A função sigmoide na camada de saída é apropriada para problemas de classificação binária, onde a saída deve ser interpretada como uma probabilidade.

- **Detecção de Fraudes**: Problemas de detecção de fraudes, por serem altamente desbalanceados e complexos, beneficiam-se de arquiteturas profundas com múltiplas camadas densas, onde cada camada sucessiva aprende características mais abstratas e informativas. A função sigmoide na camada de saída é apropriada para produzir uma probabilidade de fraude, que pode ser usada para definir um limiar de decisão.

#### 5. **Conclusão**

A arquitetura proposta é adequada para a detecção de fraudes devido à sua capacidade de capturar padrões complexos em dados tabulares, através de uma combinação de camadas densas, ativação não linear, e uma estrutura que promove a compactação e abstração progressiva dos dados. Esta rede, uma vez treinada adequadamente, deve ser capaz de distinguir entre transações legítimas e fraudulentas com alta precisão. No entanto, é importante ressaltar que o desempenho final do modelo depende de vários fatores, como a qualidade dos dados, o processo de treinamento, a regularização e a validação adequada. Portanto, é sempre recomendável realizar experimentos e ajustes adicionais para otimizar a arquitetura e maximizar o desempenho do modelo.