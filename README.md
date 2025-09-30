# django-petcare-reservation-api

# 🐾 Django Contact + Reservation API

## 🚀 Django Project  
### 📬 Contatos + 📅 Reservas + 🐾 Categorias + 🌐 API REST + 🧪 Testes Automatizados

![Capa do Projeto](reserva_contato.png)

---

## 🏅 Badges

![GitHub repo size](https://img.shields.io/github/repo-size/Rogerio5/django-contact-reservation-api)
![GitHub license](https://img.shields.io/github/license/Rogerio5/django-contact-reservation-api)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Django](https://img.shields.io/badge/django-4.2-green)
![DRF](https://img.shields.io/badge/DRF-3.14-red)
![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)

---

## 📖 Descrição / Description

**PT:**  
Este projeto é a evolução de um mini projeto Django. Agora, além da página de contato, foi adicionado um **sistema de reservas**, um módulo de **categorias de animais**, uma **API REST completa** com **Django REST Framework**, autenticação via Token e **testes automatizados** com Pytest e Coverage.  

**EN:**  
This project is the evolution of a Django mini project. In addition to the contact page, it now includes a **reservation system**, an **animal categories module**, a **full REST API** with **Django REST Framework**, token-based authentication, and **automated tests** with Pytest and Coverage.  

---

## ⚙️ Funcionalidades / Features

| 🧩 Funcionalidade (PT)                          | 💡 Description (EN)                          |
|------------------------------------------------|----------------------------------------------|
| 📬 Página de contato em `/contato/`            | 📬 Contact page at `/contato/`               |
| 📅 Página de reservas em `/reserva/`           | 📅 Reservation page at `/reserva/`           |
| 🐾 Gestão de categorias de animais             | 🐾 Animal categories management              |
| 🔗 Relacionamento Categoria ↔ Reserva com endpoint `/api/categorias/<id>/reservas/` | 🔗 Category ↔ Reservation relationship with endpoint `/api/categorias/<id>/reservations/` |
| 💾 Salvamento no banco de dados                | 💾 Database persistence                      |
| 🔐 Gerenciamento via Django Admin              | 🔐 Management via Django Admin               |
| 🎨 Templates com Bootstrap + CSS customizado   | 🎨 Templates styled with Bootstrap + custom CSS |
| 🌐 API REST para Contatos, Reservas e Categorias | 🌐 REST API for Contacts, Reservations and Categories |
| 🔎 Filtros, busca e ordenação na API           | 🔎 Filters, search and ordering in API       |
| 🧪 Testes via Postman Collection e Pytest      | 🧪 Testing via Postman Collection and Pytest |

---

## 🚀 Execução / Execution

**PT-BR:**

1. Clone o repositório  
   ```bash
   git clone https://github.com/Rogerio5/django-contact-reservation-api.git
   cd django-contact-reservation-api
2. Crie um ambiente virtual e instale as dependências
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   pip install -r requirements-dev.txt   # dependências de desenvolvimento
   ```
3. Execute as migrações
   ```bash
   python manage.py migrate
   ```
4. Crie um superusuário
   ```bash
   python manage.py createsuperuser
   ```
5. Rode o servidor
   ```bash
   python manage.py runserver
   ```
6. Acesse no navegador

    Contato: http://127.0.0.1:8000/contato/
    
    Reservas: http://127.0.0.1:8000/reserva/
    
    Admin: http://127.0.0.1:8000/admin/
    
    API Contatos: http://127.0.0.1:8000/contato/api/contatos/
    
    API Reservas: http://127.0.0.1:8000/contato/api/reservas/

**EN**

1. Clone the repository

```bash
git clone https://github.com/Rogerio5/django-contact-reservation-api.git
cd django-contact-reservation-api
```
2. Create a virtual environment and install dependencies

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
pip install -r requirements-dev.txt   # development dependencies
```
3. Run migrations

```bash
python manage.py migrate
```
4. Create a superuser

```bash
python manage.py createsuperuser
```
5. Start the server

```bash
python manage.py runserver
```
6. Access in browser

  Contact: http://127.0.0.1:8000/contato/
  
  Reservations: http://127.0.0.1:8000/reserva/
  
  Admin: http://127.0.0.1:8000/admin/
  
  Contacts API: http://127.0.0.1:8000/contato/api/contatos/
  
  Reservations API: http://127.0.0.1:8000/contato/api/reservas/

---

## 🧪 Testes

🔹 **Testes Automatizados (Django + Pytest)**

1. **Rodar todos os testes**
   ```bash
   pytest
2. Rodar com cobertura
   
   ```bash
   pytest --cov
   ```
3. Gerar relatório em HTML

   ```bash
   coverage html
   ```
4. Abrir no navegador

   Código
   htmlcov/index.html
   
   ✅ Cobertura atual: 98%

---

## 🧪 Testes com Postman / Postman Tests

**PT:**  
Este projeto já inclui uma **coleção do Postman** (`postman_collection.json`) para facilitar os testes da API.  
A coleção cobre **CRUD completo** para **Contatos, Reservas e Categorias**, além de um **endpoint especial** que retorna todas as reservas de uma categoria específica.  

**EN:**  
This project already includes a **Postman collection** (`postman_collection.json`) to make API testing easier.  
The collection covers **full CRUD** for **Contacts, Reservations, and Categories**, plus a **special endpoint** that returns all reservations of a specific category.  

---

### ⚙️ Configuração do Ambiente / Environment Setup

| Variável / Variable | Valor (exemplo) / Example Value | Descrição / Description |
|---------------------|---------------------------------|--------------------------|
| `auth_token`        | `seu_token_gerado_no_django` / `your_token_generated_in_django` | Token de autenticação (obtido via login ou admin) / Authentication token (obtained via login or admin) |
| `url`               | `http://127.0.0.1:8000`         | Endereço base da API / Base URL of the API |

**PT:**  
1. Abra o **Postman** → **Environments** → **Add**.  
2. Crie um ambiente chamado **Django API**.  
3. Adicione as variáveis acima.  
4. Clique em **Save** e selecione o ambiente no canto superior direito.  

**EN:**  
1. Open **Postman** → **Environments** → **Add**.  
2. Create an environment named **Django API**.  
3. Add the variables above.  
4. Click **Save** and select the environment in the top right corner.  

---

### ▶️ Endpoints disponíveis / Available Endpoints

- **Contatos / Contacts** → CRUD completo em `/api/contatos/`  
- **Reservas / Reservations** → CRUD completo em `/api/reservas/`  
- **Categorias / Categories** → CRUD completo em `/api/categorias/`  
  - **GET `/api/categorias/<id>/reservas/`** → retorna todas as reservas (animais) de uma categoria específica / returns all reservations (animals) of a specific category  

---

### 🔎 Exemplos de uso / Usage Examples

- **Listar Contatos / List Contacts** → `GET {{url}}/contato/api/contatos/`  
- **Criar Contato / Create Contact** → `POST {{url}}/contato/api/contatos/`  
- **Listar Reservas / List Reservations** → `GET {{url}}/contato/api/reservas/`  
- **Criar Reserva / Create Reservation** → `POST {{url}}/contato/api/reservas/`  
- **Listar Categorias / List Categories** → `GET {{url}}/contato/api/categorias/`  
- **Reservas de uma Categoria / Reservations of a Category** → `GET {{url}}/contato/api/categorias/1/reservas/`  

---

### 🔑 Obtendo o Token / Getting the Token

**PT:**  
1. Crie um usuário no Django Admin ou via `createsuperuser`.  
2. Gere o token de autenticação:  
   ```bash
   python manage.py drf_create_token <seu_usuario>
   ou acesse pelo Django Admin → Tokens.

3. Copie o token e cole no campo auth_token do ambiente no Postman.

EN:

1. Create a user in Django Admin or via `createsuperuser`.

2. Generate the authentication token:

```bash
python manage.py drf_create_token <your_user>
or access it through Django Admin → Tokens.
```
3. Copy the token and paste it into the auth_token field of the Postman environment.

---
