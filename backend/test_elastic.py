#!/usr/bin/env python3
"""
Elastic Connection Tester for Klein AI Dual Framework
Tests connection and sets up sample data for demo
"""

import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import json

# Load environment variables
load_dotenv()

def test_elastic_connection():
    """Test Elastic Cloud connection with credentials from .env"""

    print("🔍 Testing Elastic Connection...")

    cloud_id = os.getenv('ELASTIC_CLOUD_ID')
    username = os.getenv('ELASTIC_USER')
    password = os.getenv('ELASTIC_PASS')

    if not all([cloud_id, username, password]):
        print("❌ Missing Elastic credentials in .env file")
        print("Required: ELASTIC_CLOUD_ID, ELASTIC_USER, ELASTIC_PASS")
        return False

    try:
        # Create Elasticsearch client for Serverless
        endpoint = os.getenv('ELASTIC_ENDPOINT')
        api_key = os.getenv('ELASTIC_API_KEY')

        if endpoint and api_key:
            es = Elasticsearch(
                hosts=[endpoint],
                api_key=api_key
            )
        elif cloud_id and username and password:
            es = Elasticsearch(
                cloud_id=cloud_id,
                basic_auth=(username, password)
            )
        else:
            print("❌ Missing credentials")
            return False

        # Test connection
        info = es.info()
        print(f"✅ Connected to Elastic Cloud!")
        print(f"   Cluster: {info['cluster_name']}")
        print(f"   Version: {info['version']['number']}")

        # Test index creation
        index_name = "klein-ai-docs"

        # Create sample documents for demo
        sample_docs = [
            {
                "id": "haiti-weather",
                "title": "Haiti Weather Information",
                "content": "Port-au-Prince has a tropical climate with temperatures ranging from 24-32°C year-round. The city experiences a wet season from April to October and a dry season from November to March.",
                "category": "weather",
                "country": "Haiti"
            },
            {
                "id": "klein-ai-overview",
                "title": "Klein AI System Overview",
                "content": "Klein AI is designed to provide helpful, empathetic responses while maintaining safety through Ophir oversight. The system uses hybrid search to ground responses in verified information.",
                "category": "technical",
                "country": "global"
            },
            {
                "id": "safety-protocols",
                "title": "AI Safety Protocols",
                "content": "All AI responses are monitored by Ophir for safety, bias, and appropriateness. Restricted content is automatically flagged and blocked from reaching users.",
                "category": "safety",
                "country": "global"
            }
        ]

        # Index sample documents
        print(f"📄 Creating index '{index_name}' with sample documents...")

        for doc in sample_docs:
            result = es.index(
                index=index_name,
                id=doc["id"],
                document=doc
            )
            print(f"   ✅ Indexed: {doc['title']}")

        # Refresh index to make documents searchable
        es.indices.refresh(index=index_name)

        # Test search
        print("🔍 Testing search functionality...")
        search_query = {
            "query": {
                "multi_match": {
                    "query": "Port-au-Prince weather",
                    "fields": ["title^2", "content"]
                }
            }
        }

        search_result = es.search(index=index_name, body=search_query)
        hits = search_result['hits']['hits']

        if hits:
            print(f"✅ Search test successful! Found {len(hits)} results")
            for hit in hits:
                print(f"   📄 {hit['_source']['title']} (score: {hit['_score']})")
        else:
            print("⚠️  Search returned no results")

        print("\n🎉 Elastic setup complete and ready for Klein AI!")
        return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Verify Cloud ID is correct")
        print("2. Check username/password")
        print("3. Ensure deployment is running in Elastic Cloud")
        return False

if __name__ == "__main__":
    print("🚀 Klein AI Dual Framework - Elastic Setup")
    print("=" * 50)

    success = test_elastic_connection()

    if success:
        print("\n✅ SUCCESS: Your Klein AI system is ready with real Elastic power!")
        print("🎯 Next: Restart your backend to use real search")
    else:
        print("\n❌ Setup incomplete. Please check your Elastic Cloud configuration.")
