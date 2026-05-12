from duckduckgo_search import DDGS
try:
    import brain
    from memory import memory_manager
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    import brain
    from memory import memory_manager

from skills.registry import register_skill

@register_skill(["search", "google", "find out", "check online"])
def web_search_skill(command):
    """
    Performs a real-time web search and synthesizes an answer using the AI.
    """
    # Extract the actual query from the command
    query = command.lower()
    for trigger in ["search", "google", "find out", "check online"]:
        query = query.replace(trigger, "")
    query = query.strip()
    
    if not query:
        return "Sir, what would you like me to search for?"

    print(f"[WEB_SEARCH] Looking up: {query}...")
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=4))
        
        if not results:
            return f"Sir, I couldn't find any relevant data online for '{query}'."

        # Format context for the AI
        context = "\n".join(f"- {r['title']}: {r['body']}" for r in results)
        
        # Get history for context
        history = memory_manager.get_memory(limit=5)
        
        print(f"[WEB_SEARCH] Synthesizing answer with AI...")
        prompt = f"Using these real-time search results, please answer the user's query: '{query}'\n\nSearch Results:\n{context}"
        
        return brain.ask_ai(prompt, history)
        
    except Exception as e:
        print(f"Search Error: {e}")
        return "Sir, I encountered a connectivity issue with the search satellites."
