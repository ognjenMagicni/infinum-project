# Infinum Project

## Project Setup Guide  

This guide will help you set up the project locally on your machine. Follow the steps carefully to get everything running.

---

### **🛠️ Prerequisites**  
Before you begin, make sure you have the following installed:
- [PostreSQL](https://dev.mysql.com/downloads/mysql/) (database)  
- [pgAdmin4](https://www.mysql.com/products/workbench/) (for managing the database)  
- [Python](https://www.python.org/) (for backend and frontend)  

---

### **1. Cloning the Repository**  
To clone the project from GitHub, open a terminal and run:  

```sh
git clone --single-branch --branch new-master  git@github.com:ognjenMagicni/infinum-project.git
```

### **2. Setting database**

1. Open pgAdmin4.
2. Create a new databse named infinum.
3. Right click database infinum -> Restore.
4. Set absolute path to infinum-project/database/infinum_database.sql file in Filename
5. Click Restore and wait for the process to complete.

### **3. Setting Up The Virtual Environment**

For Linux:
```sh
cd infinum-project/backend
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

For Windows:
IMPORTANT! For Windows users you have to go in infinum-project/backend/requirements.txt and delete 'uvloop==0.21.0' line, since it is not support for Windows
```sh
cd infinum-project\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### **4. Setting Up Global Environemnts**

1. Open infinum-project/application.env and write following variables
2. Get Tavily key at [link](https://tavily.com/) for tavily variable
3. database: infinum
4. The rest should populate based on your configuration

### **5. Setting Up The Frontend and Backend**

1. Ensure that you are connected to venv
2. Run backend
```sh
cd infinum-project/backend
fastapi dev main.py
```
3. Run frontend
```sh
cd infinum-project/frontend
streamlit run main.py
```

### **6. Running the Application**
Once both backend and frontend are running, open your browser and go to:
🔗 http://localhost:8501

## Project Arhitecture

Project is a full stack application, which means it has database, which is connected to backend and has user interface, that is frontend. 
Chat bot uses **LangChain** framework. **LangGraph** is included for better orchestration. It uses two tools **Tavily** search, which searches web if necessary and **retriever**. Retriever has access to files in documents folder mostly about Montenegrin law and book about legal issues and analysis. First, chat bot if necessary uses retriever to gather necessary information. If that does not work he tries to get info using Tavily.

## Challanges I Have Faced

**1. Creating chat bot with retriever and Tavily tool**

My chat bot with retriever and Tavily tools did not work. So I had to break down problem in easier ones. To understand fully functionalities of LangGraph, how to add nodes, edges and conditional edges. Then build chat bot only with retriever, later chat bot only with Tavily. At the end I managed to combine them together and create chat bot with both tools. 

**2. Learning in Fly New Frameworks**

I had to quickly learn basic fundamentals of new technologies such as Streamlit and PostgreSQL. I had experience in learning new tools for short time, using LLM models and YouTube videos. I write my detailed documentation and sources of information later when come back to have my own tutorial to quickly revise this technology. 

## Future Upgrades

While building project I set the architecture to be upgraded in following
1. Adding **LangSmith** functionality to track messages between chat bot and users.
2. Adding **sessions** to enable users start a new conversation with chat bot, without interfering with previous messages


