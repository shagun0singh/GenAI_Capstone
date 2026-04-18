import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_FILE = os.path.join(BASE_DIR, "knowledge", "market_trends.txt")

def get_market_insights(query):
    # A simple, lightweight textbook "search" approach instead of heavy ML models
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    query_words = [w.lower() for w in query.split() if len(w) > 3]
    
    results = []
    for line in lines:
        # If any significant query word is in the line, consider it a match
        if any(word in line.lower() for word in query_words) and line.strip():
            results.append(line.strip())
            
    # Fallback to the first few lines if no matches are found
    if not results:
        results = lines[:3]
        
    return "\n\n".join(results[:3])

if __name__ == "__main__":
    print(get_market_insights("What are the risks of leasehold properties?"))
