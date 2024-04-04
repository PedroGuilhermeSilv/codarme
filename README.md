<h1 align="center" style="font-weight: bold;">API de Agendamento💻</h1>

<p align="center">
 <a href="#tech">Technologies</a> • 
 <a href="#started">Getting Started</a> • 
  <a href="#routes">API Endpoints</a> •
 <a href="#colab">Collaborators</a> •
 <a href="#contribute">Contribute</a>
</p>

<p align="center">
    <b>API de Agendamento.</b>
</p>

<h2 id="technologies">💻 Technologies</h2>


- Django


<h2 id="started">🚀 Getting started</h2>

Here you describe how to run your project locally

<h3>Prerequisites</h3>

Here you list all prerequisites necessary for running your project. For example:

- [Python](https://github.com/)
- [Docker](https://github.com)
- [Poetry]()

<h3>Cloning</h3>

How to clone my project branch docker

```bash
git clone  https://github.com/PedroGuilhermeSilv/codarme
```

<h3>Config .env variables</h2>

Use the `.env-example` as reference to create your configuration file `.env` with your AWS Credentials

```yaml

```

<h3>Starting</h3>

How to start your project

```bash
cd codarme
docker compose up
```

<h2 id="routes">📍 API Endpoints</h2>

Here you can list the main routes of your API, and what are their expected request bodies.
​
| route               | description                                          
|----------------------|-----------------------------------------------------
| <kbd>GET /horarios</kbd>     | return all horarios [response details](#get-auth-detail)
| <kbd>GET /agendamentos</kbd>     | return all schedules [response details](#get-agend)
| <kbd>GET /agendamentos/id/</kbd>     | detalhar schedules [response details](#get-agend-datail)
| <kbd>POST /agendamentos</kbd>     | create schedules [response details](#post-agend)
| <kbd>DELETE /agendamentos/id/</kbd>     | detail schedules [response details](#get-auth-detail)

<h3 id="get-agend">GET /agendamentos/</h3>

**RESPONSE**
```json
[
{
"data_horario": "2024-04-04T16:40:30.190197Z",
"nome_cliente": "pedro",
"email_cliente": "pedro@hotmail.com",
"telefone_cliente": "989999"
},
{
"data_horario": "2024-04-04T16:41:22.023563Z",
"nome_cliente": "pedro",
"email_cliente": "pedro@hotmail.com",
"telefone_cliente": "989999"
},
{
"data_horario": "2024-04-04T16:44:48.183389Z",
"nome_cliente": "pedro2",
"email_cliente": "pedro@hotmail.com",
"telefone_cliente": "989999"
}
]
```

<h3 id="get-agend-datail">GET /agendamentos/id</h3>

**RESPONSE**
```json
{
"data_horario": "2024-04-04T16:44:48.183389Z",
"nome_cliente": "pedro2",
"email_cliente": "pedro@hotmail.com",
"telefone_cliente": "989999"
}

```

<h3 id="create-agend">GET /agendamentos</h3>

**REQUEST** 
```json
{
"data_horario": "2024-04-04T16:44:48.183389Z",
"nome_cliente": "pedro2",
"email_cliente": "pedro@hotmail.com",
"telefone_cliente": "989999"
}

```

<h2 id="contribute">📫 Contribute</h2>


