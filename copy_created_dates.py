import os
from notion_client import Client

# Check if API key is set
api_key = os.environ.get("NOTION_API_KEY")
if not api_key:
    print("Error: NOTION_API_KEY environment variable is not set.")
    exit(1)

# Initialize Notion client
notion = Client(auth=api_key)

# Use the data source ID directly
DATA_SOURCE_ID = "45d16c99-346a-403a-b421-06c263064850"

print("📄 Querying data source directly (fast method)...")
print("=" * 60)

# Query the data source directly - fetch ALL pages with pagination
try:
    pages = []
    start_cursor = None
    
    while True:
        query_params = {
            "data_source_id": DATA_SOURCE_ID,
            "page_size": 100
        }
        if start_cursor:
            query_params["start_cursor"] = start_cursor
        
        response = notion.data_sources.query(**query_params)
        pages.extend(response["results"])
        
        print(f"   Fetched {len(response['results'])} pages... (total: {len(pages)})")
        
        if not response.get("has_more"):
            break
        start_cursor = response.get("next_cursor")
    
    print(f"✅ Found {len(pages)} total pages")
    
    if len(pages) == 0:
        print("⚠️  No pages found")
        exit(0)
    
    print("\n" + "=" * 60)
    print("📝 Updating Publication Dates...")
    print("=" * 60)
    
    success_count = 0
    for i, page in enumerate(pages, 1):
        page_id = page["id"]
        created_time = page["created_time"]
        
        try:
            notion.pages.update(
                page_id=page_id,
                properties={
                    "Publication Date": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": created_time
                                }
                            }
                        ]
                    }
                }
            )
            success_count += 1
            print(f"[{i}/{len(pages)}] ✅ {created_time}")
        except Exception as e:
            print(f"[{i}/{len(pages)}] ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"✅ Complete! Updated {success_count}/{len(pages)} pages")

except Exception as e:
    print(f"❌ Error querying data source: {e}")
    print("\nTrying alternative method...")
    exit(1)

