from elasticsearch import Elasticsearch
from core.config import settings
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Local fallback documents for when Elastic is not configured
LOCAL_DOCS = [
    {
        "title": "Haiti Disaster Response Guidelines",
        "content": "Port-au-Prince weather patterns show frequent afternoon thunderstorms during hurricane season (June-November). Emergency responders should monitor local conditions and prepare for rapid weather changes.",
        "source": "Haiti Emergency Management"
    },
    {
        "title": "Naval Training Protocol - Basic Navigation",
        "content": "Standard maritime navigation requires continuous monitoring of weather conditions, especially in Caribbean waters where conditions can change rapidly.",
        "source": "Naval Training Manual (Unclassified)"
    },
    {
        "title": "Multilingual Support Guidelines",
        "content": "When providing assistance in Haiti, responders should be prepared to communicate in French, Haitian Creole, and English to ensure effective community engagement.",
        "source": "International Response Guidelines"
    }
]

class RetrievalService:
    def __init__(self):
        self.es_client = None
        self.index_name = "klein-knowledge-base"

        # Try to initialize Elasticsearch if credentials are provided
        if settings.elastic_cloud_id and settings.elastic_user and settings.elastic_pass:
            try:
                self.es_client = Elasticsearch(
                    cloud_id=settings.elastic_cloud_id,
                    basic_auth=(settings.elastic_user, settings.elastic_pass)
                )
                logger.info("Elasticsearch client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Elasticsearch: {e}")
                self.es_client = None
        else:
            logger.info("Elasticsearch credentials not provided, using local fallback")

    def search_context(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """
        Search for relevant context documents.
        Falls back to local documents if Elastic is not available.
        """
        if self.es_client:
            return self._elastic_search(query, max_results)
        else:
            return self._local_search(query, max_results)

    def _elastic_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search using Elasticsearch hybrid search"""
        try:
            search_body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^2", "content", "source"],
                        "type": "best_fields"
                    }
                },
                "size": max_results,
                "_source": ["title", "content", "source"]
            }

            response = self.es_client.search(
                index=self.index_name,
                body=search_body
            )

            results = []
            for hit in response['hits']['hits']:
                results.append({
                    "title": hit['_source'].get('title', ''),
                    "content": hit['_source'].get('content', ''),
                    "source": hit['_source'].get('source', ''),
                    "score": hit['_score']
                })

            return results

        except Exception as e:
            logger.error(f"Elasticsearch search failed: {e}")
            # Fallback to local search
            return self._local_search(query, max_results)

    def _local_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Simple local search through predefined documents"""
        query_lower = query.lower()
        scored_docs = []

        for doc in LOCAL_DOCS:
            score = 0
            # Simple scoring based on keyword matches
            for word in query_lower.split():
                if word in doc['title'].lower():
                    score += 2
                if word in doc['content'].lower():
                    score += 1

            if score > 0:
                scored_docs.append({**doc, "score": score})

        # Sort by score and return top results
        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        return scored_docs[:max_results]

    def index_document(self, doc: Dict[str, Any]) -> bool:
        """Index a new document (only works with Elastic)"""
        if not self.es_client:
            logger.warning("Cannot index document: Elasticsearch not available")
            return False

        try:
            response = self.es_client.index(
                index=self.index_name,
                body=doc
            )
            return response['result'] in ['created', 'updated']
        except Exception as e:
            logger.error(f"Failed to index document: {e}")
            return False

# Global instance
retrieval_service = RetrievalService()
