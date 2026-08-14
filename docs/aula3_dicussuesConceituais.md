## Discussão com o grupo - Etapa 1

**Pergunta:** Se você enviar somente o `app.py` para outro computador, o que precisa existir nesse computador para a aplicação funcionar? Liste pelo menos quatro dependências ou configurações.

Se enviarmos somente o arquivo `app.py` para outro computador, a aplicação não funcionará imediatamente. O computador precisará ter algumas dependências e configurações:

1. **Python instalado:** o computador precisa ter uma versão compatível do Python instalada e configurada no `PATH`.

2. **Flask instalado:** como o código utiliza o Flask, essa biblioteca precisa estar instalada no ambiente Python. Podemos instalá-la com `pip install flask` ou utilizando o `requirements.txt`.

3. **Dependências do projeto:** todas as bibliotecas utilizadas pela aplicação precisam estar instaladas. O arquivo `requirements.txt` facilita a instalação dessas dependências.

4. **Porta 5000 disponível:** a aplicação está configurada para utilizar a porta `5000`, portanto ela precisa estar disponível e não pode estar bloqueada para o acesso necessário.

5. **Variáveis de ambiente:** a aplicação utiliza a variável `AMBIENTE`. Ela possui um valor padrão (`desenvolvimento`), mas pode ser configurada caso seja necessário executar a aplicação em outro ambiente.

### Conclusão

Enviar apenas o código não é suficiente para garantir que a aplicação funcione em outro computador. É necessário que o ambiente também esteja preparado com o Python, as dependências e as configurações necessárias.

Isso ajuda a entender **por que o Docker é útil**: ele permite empacotar a aplicação junto com suas dependências e configurações, tornando sua execução mais padronizada em diferentes ambientes.



## Discussão com o grupo - Pergunta da Etapa 3

**Por que uma configuração como `AMBIENTE=producao` é melhor como variável de ambiente do que escrita diretamente no código?**

### Resposta

Porque a variável de ambiente permite **alterar a configuração da aplicação sem precisar modificar o código**.

No exemplo da atividade, podemos executar o mesmo container com diferentes ambientes:

```bash
docker run --rm -p 5000:5000 -e AMBIENTE=producao radar-enem:v1
```

O código continua exatamente o mesmo, mas o valor de `AMBIENTE` pode mudar conforme o ambiente de execução, como `desenvolvimento`, `teste` ou `producao`.

Isso torna a aplicação mais **flexível, reutilizável e fácil de configurar**, além de evitar que informações específicas do ambiente fiquem fixas no código.

**Em resumo:** o código define **como a aplicação funciona**, enquanto as variáveis de ambiente permitem definir **como ela deve ser configurada em cada ambiente**.

# Respostas conceituais da Parte Final — Aula 3 | Mini Radar ENEM

## 1. O que foi necessário instalar e configurar para executar a aplicação sem Docker?

Para executar a aplicação localmente, sem utilizar Docker, foi necessário preparar manualmente o ambiente Python no computador.

Os principais componentes configurados foram:

* **Python 3.13:** utilizado para executar o arquivo `app.py`.
* **Ambiente virtual (`venv`):** criado e ativado para isolar as dependências da aplicação.
* **Flask:** framework utilizado pela aplicação, instalado a partir do arquivo `requirements.txt` com o comando `pip install -r requirements.txt`.
* **Porta 5000:** utilizada pela aplicação e que precisava estar disponível para a execução do servidor.

Dessa forma, sem Docker, o ambiente de execução precisou ser configurado manualmente, incluindo o Python, as dependências e as configurações necessárias para iniciar a aplicação.

---

## 2. O que o Docker passou a empacotar ou padronizar?

O Docker passou a **empacotar e padronizar o ambiente necessário para executar a aplicação**, por meio da construção de uma imagem.

No `Dockerfile`, foram definidos os principais elementos necessários para a execução:

* **Imagem base:** `python:3.12-slim`, que fornece o ambiente Python utilizado pelo container.
* **Dependências:** instaladas a partir do arquivo `requirements.txt`.
* **Código da aplicação:** o arquivo `app.py` é copiado para dentro da imagem.
* **Diretório de trabalho:** definido como `/app`.
* **Porta da aplicação:** a porta `5000` é documentada por meio da instrução `EXPOSE`.
* **Comando de inicialização:** definido como `CMD ["python", "app.py"]`.

Assim, as configurações necessárias para executar a aplicação ficam registradas na imagem Docker. Isso reduz a necessidade de realizar manualmente a mesma configuração em diferentes computadores ou ambientes.

> **Observação:** no computador, foi utilizado o Python 3.13. Entretanto, o `Dockerfile` fornecido na atividade utiliza a imagem `python:3.12-slim`. Portanto, o Python utilizado dentro do container é o **Python 3.12**, conforme definido pela imagem base do Dockerfile.

---

## 3. Se o container for executado em uma VM IaaS, quais responsabilidades ainda ficam com a equipe?

Em um modelo **IaaS (Infrastructure as a Service)**, o provedor de nuvem disponibiliza a infraestrutura necessária, como servidores, armazenamento e recursos de rede. Porém, a equipe ainda precisa administrar diversas partes do ambiente.

De acordo com a atividade, algumas das principais responsabilidades são:

* **Máquina virtual:** configurar e administrar a VM.
* **Sistema operacional:** instalar, atualizar e aplicar patches de segurança.
* **Docker:** instalar, configurar e manter o Docker na máquina virtual.
* **Containers:** executar, configurar e administrar os containers da aplicação.
* **Aplicação:** manter o código, as dependências e as configurações.
* **Rede e segurança:** configurar regras de acesso, portas e controles de segurança.
* **Monitoramento e disponibilidade:** acompanhar o funcionamento da aplicação e atuar em caso de falhas.

Portanto, o Docker facilita o **empacotamento e a execução da aplicação**, mas não elimina as responsabilidades relacionadas à administração da infraestrutura em um ambiente IaaS.

---

## 4. O que um PaaS poderia assumir automaticamente?

Em um modelo **PaaS (Platform as a Service)**, o provedor assume uma parte maior das responsabilidades de infraestrutura e operação da aplicação.

Entre as tarefas que podem ser automatizadas ou gerenciadas pelo PaaS estão:

* **Infraestrutura e sistema operacional:** gerenciamento e manutenção da infraestrutura subjacente.
* **Runtime:** disponibilização e gerenciamento do ambiente necessário para executar a aplicação.
* **Provisionamento:** criação e configuração dos recursos necessários para a aplicação.
* **Recuperação de falhas:** reinicialização ou substituição de instâncias em determinadas situações.
* **Escalabilidade:** aumento ou redução dos recursos conforme a demanda, dependendo da plataforma.
* **Monitoramento e disponibilidade:** recursos para acompanhar a aplicação e manter sua disponibilidade.

Com isso, a equipe pode se concentrar principalmente no **desenvolvimento e manutenção da aplicação**, enquanto o provedor gerencia grande parte da infraestrutura e das tarefas operacionais.

---

## 5. Por que Docker não pode ser classificado, sozinho, como IaaS, PaaS ou SaaS?

O Docker é uma **tecnologia de conteinerização** utilizada para empacotar, distribuir e executar aplicações de maneira padronizada. Ele não representa, por si só, um modelo de serviço em nuvem.

### Não é IaaS

O Docker não fornece, sozinho, máquinas virtuais, servidores físicos, armazenamento ou toda a infraestrutura necessária para executar uma aplicação.

### Não é PaaS

O Docker, por si só, não fornece uma plataforma totalmente gerenciada que assuma automaticamente responsabilidades como infraestrutura, disponibilidade, monitoramento e escalabilidade.

### Não é SaaS

O Docker também não é uma aplicação pronta disponibilizada ao usuário final como um serviço de software.

Portanto, o Docker pode ser **utilizado em ambientes IaaS, PaaS e em diferentes arquiteturas de computação em nuvem**, mas ele próprio é uma tecnologia de conteinerização e não um modelo de serviço.

---

# Conclusão

A atividade demonstrou que o Docker resolve principalmente o problema de **empacotamento, portabilidade e padronização do ambiente de execução da aplicação**.

Sem Docker, é necessário configurar manualmente o ambiente, instalar as dependências e garantir que as versões utilizadas sejam compatíveis. Com Docker, essas configurações podem ser definidas no `Dockerfile` e reproduzidas por meio de uma imagem.

Entretanto, o uso do Docker não elimina todas as responsabilidades relacionadas à aplicação. Dependendo do modelo de serviço utilizado, ainda podem existir responsabilidades relacionadas à **infraestrutura, segurança, disponibilidade, monitoramento e escalabilidade**.

A principal diferença entre IaaS e PaaS está justamente na distribuição dessas responsabilidades:

* **IaaS:** oferece maior controle sobre a infraestrutura, mas exige mais responsabilidades da equipe.
* **PaaS:** oferece maior abstração e automação, reduzindo o trabalho operacional da equipe.

Assim, a escolha entre IaaS e PaaS depende do equilíbrio desejado entre **controle, simplicidade, escalabilidade e responsabilidades operacionais**.
