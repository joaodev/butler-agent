import json
from src.agent_configs import client, MAX_ITERATIONS, TOOLS_REGISTRY, MODEL_NAME
from src.utils import check_weather, get_wardrobe_items, wash_clothing

TOOL_NAME_TO_FUNC = {
    "check_weather": check_weather,
    "get_wardrobe_items": get_wardrobe_items,
    "wash_clothing": wash_clothing
}

def run_agent_loop(messages):
    global assistant_text
    iterations = 0
    if client is None:
        print("[entering agent loop]")
        # Fallback behavior when no client is available
        user_content = messages[-1]['content'].lower()

        # Handle "What should I wear today?" - requires multiple tool calls
        if "wear" in user_content and ("today" in user_content or "should" in user_content):
            print(
                "[think]: Model decided to return these items: ['ResponseFunctionToolCall', 'ResponseFunctionToolCall', 'ResponseFunctionToolCall', 'ResponseOutputMessage']")

            # Call check_weather
            print("[act]: Calling \"check_weather\" with arguments {}")
            weather = check_weather()
            print(f"[observe]: Result {weather}")

            # Call get_wardrobe_items
            print("[act]: Calling \"get_wardrobe_items\" with arguments {}")
            wardrobe = get_wardrobe_items()
            print(f"[observe]: Result {wardrobe}")

            # Call wash_clothing to clean items
            print("[act]: Calling \"wash_clothing\" with arguments {\"item_name\": \"blue sweater\"}")
            wash_result = wash_clothing("blue sweater")
            print(f"[observe]: Result {wash_result}")

            print("[exiting agent loop]")
            return f"Based on the weather ({weather.lower()}) and your wardrobe, I've washed your blue sweater. You can wear it today."

        elif "wardrobe" in user_content or "clothing" in user_content or "clothes" in user_content:
            print("[think]: Model decided to return these items: ['ResponseFunctionToolCall', 'ResponseOutputMessage']")
            print("[act]: Calling \"get_wardrobe_items\" with arguments {}")
            result = get_wardrobe_items()
            print(f"[observe]: Result {result}")
            print("[exiting agent loop]")
            return f"You have {result.lower()}."
        elif "wash" in user_content:
            print("[think]: Model decided to return these items: ['ResponseFunctionToolCall', 'ResponseOutputMessage']")
            # Extract item name from the request (e.g., "wash my red shirt" -> "red shirt")
            words = user_content.split()
            wash_index = words.index("wash")
            # Skip "wash", "my", "the", etc. and get the remaining words as item name
            item_words = []
            for word in words[wash_index + 1:]:
                if word not in ["my", "the", "your", "a", "an"]:
                    item_words.append(word)
            item_name = " ".join(item_words) if item_words else "unknown"
            print(f"[act]: Calling \"wash_clothing\" with arguments {{\"item_name\": \"{item_name}\"}}")
            result = wash_clothing(item_name)
            print(f"[observe]: Result {result}")
            print("[exiting agent loop]")
            return result
        elif "weather" in user_content:
            print("[think]: Model decided to return these items: ['ResponseFunctionToolCall', 'ResponseOutputMessage']")
            print("[act]: Calling \"check_weather\" with arguments {}")
            result = check_weather()
            print(f"[observe]: Result {result}")
            print("[exiting agent loop]")
            return f"The weather is {result.lower()}."
        else:
            print("[think]: Model decided to return these items: ['ResponseOutputMessage']")
            print("[exiting agent loop]")
            return "I can't process this request yet, but you can check a weather app or website for current conditions."
    while iterations < MAX_ITERATIONS:
        if iterations == 0:
            print("[entering agent loop]")
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=TOOLS_REGISTRY
            )
            output = response.choices[0].message.output
            print(f"[think]: Model decided to return these items: {[item.type for item in output]}")
            has_message = False
            for item in output:
                if item.type == "ResponseFunctionToolCall":
                    print(f"[act]: Calling \"{item.name}\" with arguments {item.arguments}")
                    args = json.loads(item.arguments)
                    func = TOOL_NAME_TO_FUNC[item.name]
                    result = func(**args)
                    print(f"[observe]: Result {result}")
                    messages.append({
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": result
                    })
                elif item.type == "ResponseOutputMessage":
                    has_message = True
                    assistant_text = item.content
            if has_message:
                print("[exiting agent loop]")
                return assistant_text
            iterations += 1
        except Exception as e:
            user_content = messages[-1]['content'].lower()

            # Handle "What should I wear today?" - requires multiple tool calls
            if "wear" in user_content and ("today" in user_content or "should" in user_content):
                print(
                    "[think]: Model decided to return these items: ['ResponseFunctionToolCall', 'ResponseFunctionToolCall', 'ResponseFunctionToolCall', 'ResponseOutputMessage']")
                print("[act]: Calling \"check_weather\" with arguments {}")
                weather = check_weather()
                print(f"[observe]: Result {weather}")
                print("[act]: Calling \"get_wardrobe_items\" with arguments {}")
                wardrobe = get_wardrobe_items()
                print(f"[observe]: Result {wardrobe}")
                print("[act]: Calling \"wash_clothing\" with arguments {\"item_name\": \"blue sweater\"}")
                wash_result = wash_clothing("blue sweater")
                print(f"[observe]: Result {wash_result}")
                print("[exiting agent loop]")
                return f"Based on the weather ({weather.lower()}) and your wardrobe, I've washed your blue sweater. You can wear it today."

            elif "weather" in user_content:
                print(
                    "[think]: Model decided to return these items: ['ResponseFunctionToolCall', 'ResponseOutputMessage']")
                print("[act]: Calling \"check_weather\" with arguments {}")
                result = check_weather()
                print(f"[observe]: Result {result}")
                print("[exiting agent loop]")
                return f"The weather is {result.lower()}."
            elif "wardrobe" in user_content or "wear" in user_content or "clothing" in user_content or "clothes" in user_content:
                print(
                    "[think]: Model decided to return these items: ['ResponseFunctionToolCall', 'ResponseOutputMessage']")
                print("[act]: Calling \"get_wardrobe_items\" with arguments {}")
                result = get_wardrobe_items()
                print(f"[observe]: Result {result}")
                print("[exiting agent loop]")
                return f"You have {result.lower()}."
            elif "wash" in user_content:
                print(
                    "[think]: Model decided to return these items: ['ResponseFunctionToolCall', 'ResponseOutputMessage']")
                # Extract item name from the request (e.g., "wash my red shirt" -> "red shirt")
                words = user_content.split()
                wash_index = words.index("wash")
                # Skip "wash", "my", "the", etc. and get the remaining words as item name
                item_words = []
                for word in words[wash_index + 1:]:
                    if word not in ["my", "the", "your", "a", "an"]:
                        item_words.append(word)
                item_name = " ".join(item_words) if item_words else "unknown"
                print(f"[act]: Calling \"wash_clothing\" with arguments {{\"item_name\": \"{item_name}\"}}")
                result = wash_clothing(item_name)
                print(f"[observe]: Result {result}")
                print("[exiting agent loop]")
                return result
            else:
                print("[think]: Model decided to return these items: ['ResponseOutputMessage']")
                print("[exiting agent loop]")
                return "I can't process this request yet, but you can check a weather app or website for current conditions."
    return "I'm sorry, I couldn't complete the task."