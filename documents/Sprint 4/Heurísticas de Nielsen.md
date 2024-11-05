# Introdução

As **Heurísticas de Usabilidade de Nielsen** são princípios amplamente aceitos que auxiliam no desenvolvimento de interfaces de usuário intuitivas e eficientes. Elas fornecem diretrizes claras para avaliar e melhorar a usabilidade de sistemas digitais, garantindo que a interação com o usuário seja fluida e livre de frustrações. Aplicar essas heurísticas ajuda a reduzir erros, melhorar a navegação e assegurar que o sistema atenda às expectativas e necessidades do usuário.

Neste documento, analisamos como as heurísticas de Nielsen foram implementadas em nosso projeto, destacando exemplos práticos e identificando áreas que ainda podem ser otimizadas.

## 1. Visibilidade do Status do Sistema
O sistema deve sempre manter os usuários informados sobre o que está acontecendo, fornecendo feedback apropriado dentro de um tempo razoável.

- **Exemplo:** Uma playlist no YouTube, onde sabemos o status do vídeo (assistido, carregando, etc.).
- **No caso do projeto:** Sinalizamos o status do usuário, ou onde ele está, com uma marcação em vermelho na barra principal da aplicação.

## 2. Compatibilidade entre o Sistema e o Mundo Real
O sistema deve falar a linguagem dos usuários, com palavras e conceitos familiares, ao invés de termos técnicos. Ele deve seguir convenções do mundo real, apresentando informações de forma natural e lógica.

- **Exemplo:** Ícones universais, como os de "lixeira" ou "envelope" para email.
- **No caso do projeto:** Usamos ícones gerais, como o de upload, que são facilmente compreendidos por qualquer usuário.

## 3. Controle e Liberdade para o Usuário
Os usuários devem ter "saídas de emergência" para desfazer ações ou abandonar estados indesejados sem complicação.

- **Exemplo:** Um botão "desfazer" ou a opção de cancelar uma ação.
- **No caso do projeto:** No caso de envio incorreto de arquivos CSV, investigamos uma maneira de o sistema ignorar dados inválidos.

## 4. Consistência e Padronização
O sistema deve seguir padrões para que os usuários não precisem adivinhar se diferentes ações significam a mesma coisa.

- **Exemplo:** O Google aplica padrões de design consistentes em suas plataformas.
- **No caso do projeto:** A consistência entre telas é um objetivo importante, especialmente considerando que o projeto ainda está em fase inicial.

## 5. Prevenção de Erros
O sistema deve evitar que os erros aconteçam antes que o usuário os cometa.

- **Exemplo:** Sistemas que pedem confirmação antes de deletar arquivos.
- **No caso do projeto:** Podemos adicionar um item que verifique o endereço de arquivos CSV para evitar erros futuros.

## 6. Reconhecimento em vez de Memorização
A interface deve minimizar a carga de memória do usuário, tornando objetos e ações visíveis.

- **Exemplo:** Sistemas que mostram atalhos já usados anteriormente.
- **No caso do projeto:** A função de upload de Excel implementa esse princípio ao simplificar o processo de reconhecimento.

## 7. Flexibilidade e Eficiência de Uso
O sistema deve permitir que usuários avançados utilizem atalhos e personalizem suas interações, mas sem comprometer a experiência dos iniciantes.

- **Exemplo:** Atalhos de teclado no Windows.
- **No caso do projeto:** A plataforma foi projetada com foco em usuários leigos, sem a adição de atalhos para usuários experientes.

## 8. Estética e Design Minimalista
Diálogos devem ser simples e não incluir informações irrelevantes.

- **Exemplo:** O design do Medium, que prioriza o conteúdo e minimiza distrações.
- **No caso do projeto:** Podemos ter falhado ao adicionar informações desnecessárias, e isso pode ser ajustado.

## 9. Ajude os Usuários a Reconhecer, Diagnosticar e Recuperar-se de Erros
Mensagens de erro devem ser claras, indicar o problema e sugerir soluções.

- **Exemplo:** Campos obrigatórios destacados em vermelho quando deixados em branco.
- **No caso do projeto:** Podemos melhorar ao informar o usuário sobre erros no upload de arquivos CSV incorretos, sugerindo a solução ao invés de apresentar apenas uma mensagem de erro.

## 10. Ajuda e Documentação
Mesmo que o sistema deva ser intuitivo, a ajuda e a documentação devem estar acessíveis quando necessário.

- **Exemplo:** Jogos que oferecem tutoriais rápidos ou dicas ao longo do jogo.
- **No caso do projeto:** A documentação é eficiente, mas a seção de ajuda pode ser aprimorada.

# Conclusão

A aplicação das **Heurísticas de Usabilidade de Nielsen** em nosso projeto garantiu que o sistema se tornasse mais intuitivo, eficiente e centrado no usuário. Embora tenhamos implementado várias diretrizes com sucesso, ainda há espaço para aprimoramentos em áreas como prevenção de erros e simplificação do design. A melhoria contínua, com base nas heurísticas, proporcionará uma experiência mais robusta e agradável, alinhada às expectativas dos usuários.
