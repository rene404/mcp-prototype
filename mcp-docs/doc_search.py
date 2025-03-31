from server.base import MCPServer, tool
import PyPDF2
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)
CACHE_EXPIRATION = 300  # 5 minutes

class DocumentSearchServer(MCPServer):

    @tool
    def search_research_papers(self, keyword: str):
        """Search PDFs for relevant content."""
        cache_key = f"pdf:{keyword}"

        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        with open("financial_report.pdf", "rb") as file:
            reader = PyPDF2.PdfReader(file)
            pages = [page.extract_text() for page in reader.pages]

        matching_text = [p for p in pages if keyword.lower() in p.lower()]
        response = {"matches": matching_text[:3]}

        redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps(response))

        return response

if __name__ == "__main__":
    server = DocumentSearchServer()
    server.run()
