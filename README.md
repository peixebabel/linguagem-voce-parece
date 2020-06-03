# Com que linguagem você parece?

Inspiradas numa pesquisa usando dados do GitHub, a Mila e a Vivi resolveram desenvolver um programa que a partir dos seus atributos faciais, diz as top 5 linguagens que você se parece/programa/codifica.
Claro, não tem nenhum valor real, mas serve para entender a tecnologia por trás e se divertir, não é mesmo?

O site do app é: https://face-linguagem.anvil.app.

Como usamos muitos serviços gratuitos, os servidores estão lentos.

O código foi feito em Python, rodando no [Heroku](https://www.heroku.com/), e a interface usando Python + [Anvil](http://anvil.works/). A base de dados foi feita com base nos trendings do GitHub paras as seguintes linguagens: C, C++, C#, Python, Ruby, R, Go, Swift, HTML (hehe), PHP, JavaScript e Java.

Os atributos são extraídos com a [API Microsoft Face](https://azure.microsoft.com/pt-br/services/cognitive-services/face/) e o modelo de predição é bayesiano.

Com que linguagem a Ada Lovelace se parece?

![A imagem diz no alto: Com que linguagem você se parece. Tem o rosto em pintura da Ada Lovelace na esquerda e suas top 5 linguagens na direita. São elas Java, C++, Html, JavaScript e Python. Em baixo o texto: Você aparenta 26 anos. Seu gênero aparente é Feminino. Seu coeficiente de barba [0-1] é 0 com coeficiente de bigode de 0 e de costeletas de 0. Seu coeficiente de sorriso [0-1] é 0.039. Sua emoção é Neutro.](https://github.com/peixebabel/linguagem-voce-parece/blob/master/ada.png)


E o Alan Turing?

![A imagem diz no alto: Com que linguagem você se parece. Tem o rosto do Alan Turing na esquerda e suas top 5 linguagens na direita. São elas C#, C, Go, Java e Html. Em baixo o texto: Você aparente 40 anos. Seu gênero aparente é Masculino. Seu coeficiente de barba é 0.1 com coeficiente de costeleda e de bigode de 0.1. Seu coeficiente de sorriso é 0.022. Sua emoção é neutro.](https://github.com/peixebabel/linguagem-voce-parece/blob/master/alanturing.png)

E o nosso querido Drauzio Varella?

![A imagem diz no alto: Com que linguagem você se parece. Tem o rosto do Drauzio Varella na esquerda e suas top 5 linguagens na direita. São elas R, C#, C++, Html e Python. Em baixo o texto: Você aparenta 65 anos. Seu gênero aparente é Masculino. Seu coeficiente de barba [0-1] é 0.1. Com coeficiente de bigode de 0.1 e de costeletas de 0.1. Seu coeficiente de sorriso [0-1] é 0.958. Sua emoção é Felicidade.](https://github.com/peixebabel/linguagem-voce-parece/blob/master/drauzio.jpeg)


Se não estiver acessível, por favor nos infome para que a gente arrume!
Ah! A API usada só retorna os gêneros Masculino e Feminino, por isso apenas eles são indicados.

> # Arquivos

- bayes_model.pkl	: Inferência bayesiana
- github_stereotype.py : Conexão com o Anvil (Interface)
- github_stereotype.ipynb : Análise dos dados
- linguagens.txt : Linguagens inclusas na análise
- requirements.txt : Bibliotecas necessárias
