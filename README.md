# LangGraph-Agent-UI

LangGraph-Agent-UI is a **Streamlit-powered application** that provides an interactive user interface to communicate with an AI agent service. The application uses **FastAPI** for backend services and integrates **LangGraph** to build AI-driven agents for natural language interaction.

---

## 🌟 Features

- **💬 Interactive Chat Interface**: Communicate seamlessly with the AI agent.
- **🔄 Multi-Agent and Model Support**: Easily switch between different agents and large language models (LLMs).
- **📈 Real-Time Feedback**: Users can provide feedback on responses to improve the system.
- **🛠️ Tool Call Handling**: Supports integration with external tools and APIs for advanced functionalities.
- **🔖 Session Management**: Resume previous chats using thread IDs.
- **⚙️ Customizable Settings**: Configure agents, models, and streaming options from the sidebar.
- **📊 Analytics Dashboard**: Monitor agent performance and user interactions in real-time (upcoming feature).
- **🔐 Secure Connections**: Built-in support for HTTPS and API key authentication to protect your data.

---

## 🏗️ Architecture

The project employs the following architecture:

- **Frontend**: Built with [Streamlit](https://streamlit.io/).
- **Backend**: Powered by [FastAPI](https://fastapi.tiangolo.com/).
- **Agent Framework**: Utilizes [LangGraph](https://langchain-ai.github.io/langgraph/) to construct and manage AI agents.
- **Hosting**: Frontend is hosted on Streamlit Cloud, while the backend runs on Azure.

![Agent Service Architecture](https://github.com/HabtamuFeyera/langgraph-agent-ui/blob/main/media/agent_architecture.png?raw=true)

---

## 📖 About LangGraph

LangGraph is an **open-source framework** designed for creating and managing AI agents and multi-agent applications. It provides the tools necessary to handle the complexities associated with state management, agent interactions, and error handling. By using LangGraph, developers can build robust applications that utilize Large Language Models (LLMs) effectively.

---

## 🚀 Getting Started

### 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HabtamuFeyera/langgraph-agent-ui.git
   cd langgraph-agent-ui
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the root directory.
   - Add the following variables:
     ```env
     AGENT_URL=<your-agent-url>
     HOST=0.0.0.0
     PORT=8000
     ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Access the application**:
   Open your browser and navigate to [http://localhost:8501](http://localhost:8501).

---

## 🎯 Usage

1. **Interact with the AI Assistant**:
   - Type your queries into the chat input.

2. **Customize your experience**:
   - Use the sidebar to switch between agents, models, and configure streaming options.

3. **Share or resume chats**:
   - Use the **Share/Resume Chat** button to generate a unique URL for sharing or resuming conversations.

4. **Monitor performance**:
   - Check the analytics dashboard (upcoming feature) to analyze user interactions and agent performance.

5. **Provide feedback**:
   - Help improve the system by submitting feedback on the AI responses.

---

## 🤝 Contributing

We welcome contributions! To contribute:

1. **Fork the repository**.
2. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature-name
   ```
3. **Commit your changes** and push them to your fork.
4. **Submit a pull request**:
   - Include details of your changes.

---

## 📚 Acknowledgments

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for more details.

---

## 💡 Pro Tips

- **Enable SSL**: For a production-ready deployment, configure HTTPS with your domain.
- **Scale Your Backend**: Use containers (e.g., Docker) and cloud platforms like Azure or AWS for scalable deployments.
- **Use Caching**: Implement caching mechanisms to improve response times and reduce server load.

---

## 💖 Made with Love

Created with ❤️ by [Habtamu Feyera](https://www.linkedin.com/in/habtamu-feyera-2447a917b/) in Addis Ababa.

---

## 🌍 Stay Connected

- **LinkedIn**: [Habtamu Feyera](https://www.linkedin.com/in/habtamu-feyera-2447a917b/)
- **GitHub**: [Habtamu Feyera](https://github.com/HabtamuFeyera)
- **YouTube**: [Decode AI with Habtamu](http://www.youtube.com/@DecodeAI_HF)

