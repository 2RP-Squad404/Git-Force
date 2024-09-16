# Git-Force
# O que cada um está fazendo

**David:** Estou vendo no Gemini a criação de um dataset em formato JSON para poder analisar as colunas e, depois, peço para ele gerar views para, posteriormente, trabalhar com queries dentro do Dataform.

**Gabriel Brizola:** No início da demanda, busquei estudar sobre a automatização do processo. Após enfrentar várias dúvidas sobre como seria a implementação, foquei em gerar scripts SQLX utilizando o Vertex AI e em verificar se as respostas fornecidas pela IA eram adequadas.

**Giovani:** Criei um arquivo inicial em Terraform para definir a infraestrutura como código. Além disso, escrevi uma função no Cloud Functions que imprime uma mensagem sempre que um arquivo é carregado no nosso bucket, como um teste para verificar se o gatilho funcionava corretamente.

**Matheus:** Estou realizando estudos aplicados ao projeto da Squad de backend. Estou focando em aprender novas funções e ferramentas como Docker, APIs, Pub/Sub, Kafka e RabbitMQ. Também estou me dedicando ao estudo de APIs, especialmente porque é onde estou encontrando mais dificuldades.

**Melina:** Nos dias 11 e 12, comecei a explorar as ferramentas que usaríamos no projeto. Primeiro, criei um arquivo JSON para teste e tópicos no Pub/Sub, incluindo uma assinatura pull para o tópico JSON. Depois, criei um bucket para armazenar o JSON e uma função para que o Pub/Sub recebesse esse arquivo. No dia 13, com a ajuda de uma colega e o uso do Gemini, converti uma tabela de simulação para JSON e depois para SQLX, garantindo que a transformação estivesse correta. Fiz o mesmo processo com as tabelas reais purchases e campaign, criando duas views para elas.

**João:** Passei grande parte do tempo estudando alguns funcionamentos para criar uma consulta em SQL utilizando o GenIa e o ChatGPT pra depois fazer um script em SQLX, tive certa dificuldade de entender e não consegui fazer tanta coisa na prática.

**José:** Estou estudando a plataforma do GCP, fazendo testes utilizando o Vertex IA para gerar códigos em SQLX recendo JSON, estou fazendo ajustes utilizando o gemini-flash 1.15 por ser gratuito e satisfazer o intuito de testes. 

# Resultados(propostas, o que foi entendido)

**David:** Tive algumas dificuldades, porém, conseguir compreender o que é um JSON e entendi o que é uma view gerada dentro do Dataform.

**Gabriel Brizola:** Até o momento, os resultados não foram satisfatórios. A IA gerou scripts com sintaxe incorreta e não apresentou as respostas esperadas. Além disso, não tenho certeza se o nível de complexidade do JSON enviado à IA foi adequado.

**Giovani:** Continuando com o trabalho, meu objetivo é criar um fluxo que permitirá transformar o conteúdo dos JSONs que estiverem no bucket em views que serão postadas num tópico PubSub que será consumido pelo Dataform.

**Matheus:** Como parte do treinamento para o projeto, desenvolvi algumas aplicações utilizando FastAPI e banco de dados. Isso me ajudou a compreender melhor as funções básicas de uma API, como os endpoints (POST, GET, PUT e DELETE), que são parte do CRUD, algo que já havia sido mencionado antes. Percebi uma evolução no meu entendimento das ferramentas e como utilizá-las. Além disso, estou aprimorando meus conhecimentos na linguagem Python, bem como em comandos Shell e Linux, áreas nas quais eu tinha pouca experiência prévia.

**Melina:** 
- Tive um pouco de dificuldade para trabalhar com o Gemini e conseguir criar a primeira view, porém logo após entender como era feito, eu realizei as tarefas sem dificuldade;
- Pretendo criar outras views, selecionando apenas algumas colunas, ou até mesmo com outras tabelas.

**João:** Não teve tantos resultados devido a pouca utilização do GCP, mas consegui gerar alguns JSON's com as IA's mas não tive tanto sucesso assim em gerar os scripts

**José:** Pude avançar positivamente no aprendizado com treinamento da IA conseguindo fazer um pedido e ela estar conseguindo responder aproximadamente com poucos erros. O que foi possível entender, foi que é necessário criar uma IA para gerar códigos em SQLX para automatizar processos na criação de views. 

# Dúvidas

**David:**
- Seriam sobre como usar a IA do Cloud, pelo fato de eu ainda não ter analisado a ferramenta para saber como trabalhar com ela, e, às vezes, tenho dúvidas sobre alguns nomes.

**Gabriel Brizola:** 
- De onde virão os JSONs?
- Qual é a complexidade de um JSON real vindo de uma demanda real?
- O que os JSONs irão conter?
- Qual é a melhor forma de formular perguntas para uma IA, de modo a obter respostas mais precisas?
- As tabelas já estarão formadas? Utilizaremos o JSON apenas para a criação da view?

**Giovani:** 
- De onde virão os JSONs?

**Matheus:**
- Sem dúvidas.

**Melina:**
- Ainda tenho dúvidas sobre o funcionamento do Gemini, por exemplo o comportamento dele e as suas respostas referentes a tabelas com esquemas diferentes.

**João:**
- Tenho dúvidas em como gerar as coisas com as IA's e em utilizar o Dataform

**José:** Ainda estou meio perdido na plataforma e não sei exatamente o quais ferramentas e APIs serão utilizadas para fazer esse projeto, tenho dificuldades para criar uma rotina no Dataform no momento.
