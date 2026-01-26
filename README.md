# Python RAG Practice

Python × FastAPI × Azure AI Search × OpenAI を使用した、RAG (Retrieval-Augmented Generation) システム構築の学習用リポジトリです。

## 技術スタック

- **言語**: Python 3.14.2
- **Webフレームワーク**: FastAPI (ASGI)
- **検索エンジン (Vector DB)**: Azure AI Search
- **LLM / Embedding**: OpenAI API (`gpt-4o-mini`, `text-embedding-3-small`)
- **ライブラリ管理**: pip

## プロジェクト構成 (Structure)

```
rag-practice/
├── backend/          # Python FastAPI (API Server)
│   ├── .venv/        # Virtual Environment
│   └── main.py       # Server Entrypoint
└── frontend/         # Next.js (Chat UI)
    └── app/          # React Components
```

## 環境構築 (Setup)

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd rag-practice
```

### 2. バックエンドの準備 (Python)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd ..
```

※ `backend/.env` ファイルを作成し、APIキー等を設定してください。

### 3. フロントエンドの準備 (Node.js)

```bash
# ルートディレクトリで実行
pnpm install
cd frontend
pnpm install
cd ..
```

## 実行方法 (Usage)

プロジェクトルートから、以下のコマンド1つで**FrontendとBackendを同時起動**できます。

```bash
pnpm dev
```

- **Frontend**: http://localhost:3000 (チャット画面)
- **Backend**: http://localhost:8000 (APIサーバー)
