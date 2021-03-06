# Test for Python + OpenCV developers


**Problem:**

Detect circles with diameter greater than 10 pixels.

**Comments on the environment and project decisions:**

- I pulled this to github [here](https://github.com/afgranero/py-cv-proj) ;
- I have other repos, but they are private because they are not finished, tell me if you want access to them;
- as this is a test and I am doing it alone, I did not use topic branches or issues;
- I interpreted "detect circles" in two ways:
    -  find circles centers;
    - highlight the circles on the original image and save it
- I took the following liberties:
    - I used tab as 4 spaces (the default in my environment and as PEP 8 recommends);
    - I used virtualenv to isolate libraries;
    - I did not committed the virtual environment to git though, I used `pip freeze` to create a `requirements.txt`;
    - refer to `requirements.txt` for the libraries versions needed;
    - I created the switch `-nodebug` on the command line, without this switch it will do this:
        - show windows with the intermediate states of processing on screen;
        - you can use left and right arrow keys to navigate intermediate steps;
        - save the intermediate images with same name as the original as prefix and with suffix `_1`, `_2`, etc;
        - on a production environment I would separate this on another class using python decorators to call it;
        - on a production environment I would do the opposite: to create a `-debug` switch instead
        - if there were much more test cases I would not print them individually, I would just save the steps.

**Thoughts about developing this solution**

<p align="justify">
Most programmers use OpenCV as a black box, without really understanding its algorithms, this is stimulated by the
creators of the library, to simplify and stimulate its use, the proof of that is that the documentation uses an example
directed approach, without many details of its internal workings.
</p>

<p align="justify">
This is the greatest reason to OpenCV popularity, its power and at the same time its greatest weakness. The Hough
transform used here is a good example of that, few users know that the Hough transform is a clever change of
coordinates that transform circles in cones on a 3D parameter space.
</p>

<p align="justify">
In fact this is a generalized Hough transform, as the original Hough transform was created to detect straight lines on
bubble chambers (I am a physicist so excuse me the digression).
</p>

<p align="justify">
Hough transform and its descendants are powerful and fast, but as everything the trouble is on the implementation.
The implementation used by OpenCV integrate several things on a monolithic method, it is made to be used on images with
little treatment, for that it uses internally a Sobel filter and a Canny filter. The parameter names also do not
stimulate the understanding: <code>param1</code> for instance is the upper threshold used on the Canny edge detection
previous to the Hought transform itself (the lower threshold is not under our control being half this value)
and <code>param2</code> is the threshold of the acumulator used by the Hough transform itself.</p>

<p align="justify">
This monolithic approach leads to being complex to tune the parameters. As we don't have access to the intermediate
values of the filter results (what would make simple to understand what had gone wrong) the way of adjusting those
parameters is by feeling and by trial and error. This generate programs like mine where the parameters are adjusted
recursively or in a loop until the desired result is reached.
</p>

<p align="justify">
Another side effect of that is to make it work better on balls (filled circles) than on circles, as Sobel and Canny
filters detects borders.
</p>

<p align="justify">
It is when knowledge of the algorithms becomes a diferential, and even knowledge of C and C++ to look on the source
code of the library and understand what is happening. It is in this case that I consider myself fit.
</p>

<p align="justify">
<b><i>If</i></b> I was to implement it I would use the intermediate steps of the circle Hough transform as callbacks
with defaults so better control and visualization of this steps could be achieved, making much easier to adjust
parameters.
</p>

**Usage:**
```
python pycv-proj-test.py images/image_filename
python3 pycv-proj-test.py images/image_filename
python pycv-proj-test.py images/image_filename -nodebug
python3 pycv-proj-test.py images/image_filename -nodebug
python pycv-proj-test.py -nodebug images/image_filename
python3 pycv-proj-test.py -nodebug images/image_filename
```

# Teste para desenvolvedores Python + OpenCV


**Problema:**

Detetar circunferências maiores que 10 pixels.

**Commentários sobre meu ambiente e decisões de projeto:**

- Fiz _pull_ para o _github_ [aqui](https://github.com/afgranero/py-cv-proj)
- tenho outros repositórios, mas eles são privados pois ainda estão incompletos;
- como isso é um teste e eu estou trabalhando sozinho, não usei _branches_ de tópico ou _issues_;
- interpretei "detetar circunferências" de duas maneiras:

    - encontra os centos das circunferências;
    - marcar as circunferências encontradas e seus centros na imagem original
- tomei as seguintes liberdades:
    - usei um tab como 4 espaços (o _default_ em meu ambiente e a recomendação da PEP 8);
    - usei o _virtualenv_ para isolar as bibliotecas;
    - entretanto não fiz _commit_ do ambiente virtual para o _git_, usei `pip freeze` para criar o `requirements.txt`;
    - recorra ao `requirements.txt` para as versões das bibliotecas necessárias;
    - criei  _switch_ `-nodebug` na linha de comando, sem este _switch_ o _script_ fará o seguinte:
        - abrir janelas para mostrar os estados intermediários do processamento na tela;
        - você pode usar setas para esquerda e direita para navegar nos passos intermediários
        - salvar as imagens intermediárias com o mesmo nome da original como prefixo e com sufixo `_1`, `_2`, etc;
        - em um ambiente de produção eu separaria isso em outra classe usando _decorators_ do Python para chamar;
        - em um ambiente de produção eu faria o inverso: criaria um _switch_ `-debug`;
        - seu houvesse muitos casos de teste eu não os mostraria individualmente, eu apenas salvaria os passos.

**Pensamentos sobre a solução**

<p align="justify">
A maioria dos usuários usam o OpenCV como uma caixa preta, sem entender realmente seus algoritmos, isso é estimulado
pelos criadores da biblioteca, para simplificar e estimular seu uso, a prova disso é que a documentação usa a abordagem
de exemplos sem muitos detalhes sobre o funcionamento interno.
</p>

<p align="justify">
Esse é o maior motivo da popularidade do OpenCV, de seu poder e ao mesmo tempo sua maior fraqueza. A transformada de
Hough usada aqui é um bom exemplo disso, poucos usuários sabem que a transformada de Hough é uma inteligente mudança
de coordenadas que transforma circunferências em cones em um espaço de parâmetros tridimensional.
</p>

<p align="justify">
Na verdade essa é uma transformada de Hough generalizada, já que a transformada de Hough original foi criada para
detetar linhas retas para achar traços em imagens em câmaras de bolha para uso em física (eu sou físico, assim me perdoe
a digressão).
</p>

<p align="justify">
A transformada de Hough e seus descendentes são poderosas e rápidas, mas como tudo o problema está na implementação.
A implementação usada pelo OpenCV integra muitas coisas em um método monolítico, ela é feita para ser usada em imagens
com pouco tratamente, para isso internamente ela utiliza um filtro Sobel e um filtro Canny. Os nomes dos
parâmetros também não estimulam muito a compreensão: <code>param1</code> por exemplo é o limiar superior usado na
deteção de borda Canny (sendo que o limiar inferior não está sob nosso controle sendo metade deste valor) e
<code>param2</code> que é o limiar do acumulador do algoritmo implementado para a transformada de Hough.
</p>

<p align="justify">
Essa abordagem monolítica tende a fazer ser complexo ajustar os parâmetros. Como não temos acesso aos valores
intermediários dos resultados dos filtros (o que tornaria simples entender o que deu errado) a maneira de ajustar os
parâmetros é por intuição e por tentativa e erro. Isso gera comenmente programas como o meu onde os parâmetros são
ajustados recursivamente ou em <i>loop</i> até se atingir um resultado desejado.
</p>

<p align="justify">
Outro efeito colateral disso é ela funcionar melhor em círculos do que circunferências, pois os filtros Sobel e
Canny extraem uma borda.
</p>

<p align="justify">
É nessa hora que o conhecimento dos algortimos se torna um diferencial, e mesmo o conhecimento de C e C++ para olhar o
código fonte e entender o que acontece. É nesse ponto eu me considero adequado.
</p>

<p align="justify">
<b><i>Se</i></b> eu fosse implementar-lo, eu faria com que os passos intermediários da transformada de Hough para
circunferências fossem <i>calbacks</i> com <i>defaults</i> permitindo melhor controle e visualização destes passos,
facilitando muito o ajuste dos parâmetros.
 </p>

**Uso:**
```
python pycv-proj-test.py images/image_filename
python3 pycv-proj-test.py images/image_filename
python pycv-proj-test.py images/image_filename -nodebug
python3 pycv-proj-test.py images/image_filename -nodebug
python pycv-proj-test.py -nodebug images/image_filename
python3 pycv-proj-test.py -nodebug images/image_filename
```

