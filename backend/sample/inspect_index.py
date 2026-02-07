"""
Azure AI Search のインデックス定義を確認するスクリプト
"""
import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

load_dotenv()

# 環境変数から設定を取得
service_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
api_key = os.getenv("AZURE_SEARCH_API_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")

if not all([service_endpoint, api_key, index_name]):
    raise ValueError("環境変数が設定されていません")

# SearchIndexClient の作成
index_client = SearchIndexClient(
    endpoint=service_endpoint,
    credential=AzureKeyCredential(api_key)
)

# インデックス定義を取得
index = index_client.get_index(index_name)

print(f"=== インデックス名: {index.name} ===\n")

print("【フィールド一覧】")
for field in index.fields:
    print(f"\n- フィールド名: {field.name}")
    print(f"  型: {field.type}")
    print(f"  Key: {field.key}")
    print(f"  searchable: {field.searchable}")
    print(f"  filterable: {field.filterable}")
    print(f"  sortable: {field.sortable}")
    print(f"  facetable: {field.facetable}")
    if hasattr(field, 'vector_search_dimensions'):
        print(f"  ベクトル次元数: {field.vector_search_dimensions}")
        print(f"  ベクトルプロファイル: {field.vector_search_profile_name}")
    if hasattr(field, 'analyzer_name'):
        print(f"  analyzer_name: {field.analyzer_name}")

print("\n\n【ベクトル検索設定】")
if index.vector_search:
    print(f"プロファイル数: {len(index.vector_search.profiles) if index.vector_search.profiles else 0}")
    if index.vector_search.profiles:
        for profile in index.vector_search.profiles:
            print(f"\n- プロファイル名: {profile.name}")
            print(f"  アルゴリズム: {profile.algorithm_configuration_name}")

    if index.vector_search.algorithms:
        print("\n【アルゴリズム設定】")
        for algo in index.vector_search.algorithms:
            print(f"\n- アルゴリズム名: {algo.name}")
            print(f"  種類: {algo.kind}")

print("\n\n【セマンティック検索設定】")
if index.semantic_search:
    print(f"設定数: {len(index.semantic_search.configurations) if index.semantic_search.configurations else 0}")
    if index.semantic_search.configurations:
        for config in index.semantic_search.configurations:
            print(f"\n- 設定名: {config.name}")
else:
    print("セマンティック検索は設定されていません")
