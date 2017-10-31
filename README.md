# Test for Python + OpenCV developers


**Problem:**

Detect circles with diameter greater than 10 pixels.

**Comments on my solution:**

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


**Usage:**
```
python pycv-proj-test.py images/image_filename
python3 pycv-proj-test.py images/image_filename
python pycv-proj-test.py images/image_filename -nodebug
```

# Teste para desenvolvedores Python + OpenCV


**Problema:**

Detetar circunferências maiores que 10 pixels.

**Commentários à minha solução:**

- Fiz _pull_ para o _github_ [here](https://github.com/afgranero/py-cv-proj)
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
    - criei  _switch_ `-nodebug` na linha de comando, sem este switch o _script_ fará o seguinte:
        - abrir janelas para mostrar os estados intermediários do processamento na tela;
        - você pode usar setas para esquerda e direita para navegar nos passos intermediários
        - salvar as imagens intermediárias com o mesmo nome da original como prefixo e com sufixo `_1`, `_2`, etc;
        - em um ambiente de produção eu separaria isso em outra classe usando __decorators_ do Python para chamar;
        - em um ambiente de produção eu faria o inverso: criaria um _switch_ `-debug`;
        - seu houvesse muitos casos de teste eu não os mostraria individualmente, eu apenas salvaria os passos.


**Uso:**
```
python pycv-proj-test.py images/image_filename
python3 pycv-proj-test.py images/image_filename
python pycv-proj-test.py images/image_filename -nodebug
```

