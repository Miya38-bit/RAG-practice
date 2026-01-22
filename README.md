# Python RAG Practice

Python × FastAPI × Azure AI Search × OpenAI を使用した、RAG (Retrieval-Augmented Generation) システム構築の学習用リポジトリです。

## 技術スタック

- **言語**: Python 3.14.2
- **Webフレームワーク**: FastAPI (ASGI)
- **検索エンジン (Vector DB)**: Azure AI Search
- **LLM / Embedding**: OpenAI API (`gpt-4o-mini`, `text-embedding-3-small`)
- **ライブラリ管理**: pip

## 環境構築 (Setup)

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd rag-practice
```

### 2. 仮想環境の作成と有効化 (Windows)

```powershell
# 仮想環境の作成
python -m venv .venv

# 有効化
.\.venv\Scripts\Activate.ps1
```

※ Mac/Linuxの場合: `source .venv/bin/activate`

### 3. ライブラリのインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

プロジェクトルートに `.env` ファイルを作成し、以下の情報を記述してください。

```env
# OpenAI
OPENAI_API_KEY="sk-..."

# Azure AI Search
AZURE_SEARCH_ENDPOINT="https://<your-service-name>.search.windows.net"
AZURE_SEARCH_API_KEY="<your-admin-key>"
AZURE_SEARCH_INDEX_NAME="<your-index-name>"
```

---

## 実行方法 (Usage)

### 単体機能の動作確認

以下のスクリプトで各機能単体のテストが可能です。

- `test_openai.py`: OpenAI API (Chat) の接続テスト
- `test_embedding.py`: Embedding (ベクトル化) のテスト
- `test_azure_search.py`: Azure AI Search へのデータ登録 & ベクトル検索テスト

```bash
python test_azure_search.py
```

### APIサーバーの起動

FastAPIサーバーを起動し、ブラウザからRAGチャットを利用します。

```bash
uvicorn main:app --reload
```

起動後、以下のURLにアクセスしてください。

- **Swagger UI (APIテスト画面)**: http://127.0.0.1:8000/docs

### チャットAPIのテスト

Swagger UIの `POST /chat` エンドポイントから以下のようなJSONを送信してテストできます。

```json
{
  "message": "美味しいご飯の話をして"
}
```

Azure AI Searchに登録されたデータ（例: "最近、美味しいコーヒーを淹れることにハマっています" 等）を元に、AIが回答を生成します。
