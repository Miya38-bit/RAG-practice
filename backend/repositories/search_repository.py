from azure.search.documents.aio import SearchClient
from exceptions import SearchError

"""
Azure AI Searchリポジトリクラス

"""
class SearchRepository:
    def __init__(self, search_client: SearchClient):
        self.search_client = search_client

    # ハイブリッド検索
    async def hybrid_search(
        self,
        vector_query: list[float],
        top_k: int = 2,
        text_query: str | None = None,
        use_semantic_search: bool = True,
        filter: str | None = None,
    ) -> list[dict]:
        try:
            results = await self.search_client.search(
                search_text=text_query,
                vector_queries=[  # type: ignore
                    {
                        "vector": vector_query,
                        "k": top_k,
                        "fields": "embedding",
                        "kind": "vector",
                    }
                ],
                query_type="semantic" if use_semantic_search else "simple",
                semantic_configuration_name="my-semantic-config"
                if use_semantic_search
                else None,
                filter=filter,
            )
            return [result async for result in results]
        except Exception as e:
            raise SearchError(f"検索中にエラーが発生しました: {str(e)}")
