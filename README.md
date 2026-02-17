# Butler Agent 🤖

A helpful AI-powered butler assistant that can check the weather, manage your wardrobe, and wash your clothes. This project demonstrates an agentic AI system using OpenAI's function calling capabilities.

## 📋 Overview

The Butler Agent is an interactive assistant that understands natural language requests and performs tasks by:
- Checking current weather conditions
- Viewing your wardrobe inventory with item status
- Washing dirty clothing items to make them clean

The agent uses OpenAI's API with function calling to intelligently decide which tools to use based on your requests.

## 🚀 Features

- **Weather Check**: Ask about the current weather conditions
- **Wardrobe Management**: View all items in your wardrobe with their status (clean/dirty)
- **Clothing Care**: Wash dirty items to make them clean
- **Multi-step Reasoning**: The agent can combine multiple tool calls to answer complex requests
- **Agentic Loop**: Implements a reasoning loop that continues until it generates a final response

## 📦 Requirements

- Python 3.8+
- OpenAI API key (or use local fallback mode)

## 🔧 Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /home/joao/Projects/Python/butler-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root directory:
   ```bash
   cp .env.example .env  # if available, or create manually
   ```

   Add your OpenAI credentials to `.env`:
   ```
   API_KEY=your_openai_api_key_here
   BASE_URL=https://api.openai.com/v1
   ```

   > **Note**: If you don't have an API key, the agent will fall back to a local demo mode with pre-configured responses.

## 💬 Usage

### Running the Agent

Start the interactive agent:
```bash
python -m src.main
```

You'll see a prompt where you can type your requests:
```
[user]: What should I wear today?
```

### Example Interactions

Here are some ways to interact with the Butler Agent:

#### 1. **Check the Weather**
```
[user]: What's the weather like?
[assistant]: The weather is cold, rainy.
```

#### 2. **View Your Wardrobe**
```
[user]: Show me my wardrobe
[assistant]: You have Item blue weather is dirty; Item brown jacket is dirty.
```

#### 3. **Wash a Specific Item**
```
[user]: Please wash my blue weather
[assistant]: blue weather is washed
```

#### 4. **Get Outfit Recommendations** (Multi-step)
```
[user]: What should I wear today?
[assistant]: Based on the weather (cold, rainy) and your wardrobe, I've washed your blue sweater. You can wear it today.
```

#### 5. **Ask About Your Clothes**
```
[user]: What clothing do I have?
[assistant]: You have Item blue weather is dirty; Item brown jacket is dirty.
```

#### 6. **Multiple Action Request**
```
[user]: Wash my brown jacket and tell me the weather
[assistant]: [Performs multiple function calls and provides a summary]
```

### Exit Commands

To exit the agent, type any of these commands:
- `q`
- `quit`
- `exit`

## 🏗️ Project Structure

```
butler-agent/
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .env                      # Environment variables (not in repo)
└── src/
    ├── main.py              # Entry point with interactive loop
    ├── agent.py             # Main agent logic and agentic loop
    ├── agent_configs.py     # Configuration, prompts, and tool registry
    └── utils.py             # Tool implementations (weather, wardrobe, washing)
```

## 🛠️ Technical Details

### Agent Loop Flow

1. **User Input**: Accept a natural language request
2. **LLM Processing**: Send request to OpenAI with available tools
3. **Tool Selection**: Model decides which tools to call (if any)
4. **Tool Execution**: Execute the selected functions
5. **Response Generation**: Model generates a natural language response
6. **Loop Until Done**: Repeat steps 2-5 until model outputs a final message

### Available Tools

The agent has access to the following tools:

| Tool | Description | Parameters |
|------|-------------|-----------|
| `check_weather` | Get current weather conditions | None |
| `get_wardrobe_items` | List all wardrobe items with status | None |
| `wash_clothing` | Clean a dirty clothing item | `item_name` (string) |

### Fallback Mode

If no OpenAI API key is available, the agent runs in **local fallback mode** with:
- Pre-configured responses for common requests
- Pattern matching based on keywords
- Full functionality without external API calls

## 🎮 Try These Prompts

Test the agent with these example requests:

```
1. "What's the weather?"
2. "Show me my wardrobe"
3. "Wash my blue weather"
4. "What should I wear today?"
5. "Do I have a brown jacket?"
6. "Clean my clothes"
7. "Tell me the weather and my wardrobe"
```

## 🔐 Security

- Keep your `.env` file secure and never commit it to version control
- API keys should only be stored locally or in secure secret management systems
- The `.env` file is already in `.gitignore` for safety

## 🤝 Extending the Agent

To add new capabilities:

1. **Add a new tool function** in `src/utils.py`:
   ```python
   def new_tool(param1, param2):
       # Implementation
       return "Result"
   ```

2. **Register the tool** in `src/agent_configs.py`:
   - Add to `TOOLS_REGISTRY`
   - Add to `TOOL_NAME_TO_FUNC` in `src/agent.py`

3. **Update the system prompt** if needed to guide the agent's behavior

## 📝 License

This project is open for educational and personal use.

## 🐛 Troubleshooting

### "API key not found" Error
- Ensure your `.env` file exists in the project root
- Verify `API_KEY` and `BASE_URL` are correctly set
- The agent will use fallback mode if these are missing

### Tool calls not working
- Check that the tool name in `TOOLS_REGISTRY` matches the function name in `TOOL_NAME_TO_FUNC`
- Verify function parameters match the tool definition

### Empty wardrobe
- Edit the `WARDROBE` dictionary in `src/agent_configs.py` to add items
- Items should have a status of either "clean" or "dirty"

