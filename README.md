# Internal Rules Chatbot (RAG Practice)

RAG学習用に作成しました。
社内規定（テキストデータ）に基づき、従業員の質問に回答するAIチャットボットです。
RAG (Retrieval-Augmented Generation) 技術を使用し、正確な引用元を提示しながら回答します。

![Demo](./demo.png)

## ✨ 主な機能

### RAG機能
- **ハイブリッド検索**: Azure AI Search によるベクトル検索とキーワード検索の組み合わせ
- **セマンティック検索**: 意味的な類似性を考慮した高度な検索
- **Query Rewriting**: 会話履歴を考慮し、「それはどういう意味？」のような指示語を含む質問も正しく解釈
- **引用元の提示**: 回答に使用した情報の出典（ファイル名・ページ番号・カテゴリ）を明記

### 会話管理機能
- **会話履歴の保存**: PostgreSQL による永続化
- **自動タイトル生成**: LLMによる会話の自動要約（30文字以内）
- **リアルタイム更新**: SSE (Server-Sent Events) によるタイトルの即座反映
- **会話の作成・削除・一覧表示**: ChatGPTスタイルのUI

### その他
- **ストリーミング応答**: ChatGPTのように、回答を一文字ずつリアルタイムに表示
- **レスポンシブUI**: モバイル/デスクトップ対応

## 🏗 アーキテクチャ

### バックエンド: 3層アーキテクチャ

```
Client Request
     ↓
┌─────────────────────────────────────┐
│  Router Layer (routers/)            │  ← API エンドポイント定義
│  - chat.py                          │
│  - conversation.py                  │
└─────────────────────────────────────┘
     ↓
┌─────────────────────────────────────┐
│  Service Layer (services/)          │  ← ビジネスロジック
│  - chat_service.py                  │    - Query Rewriting
│                                     │    - RAG処理
│                                     │    - タイトル生成
└─────────────────────────────────────┘
     ↓
┌─────────────────────────────────────┐
│  Repository Layer (repositories/)   │  ← データアクセス
│  - conversation_repository.py       │    - PostgreSQL操作
│  - search_repository.py             │    - Azure AI Search操作
└─────────────────────────────────────┘
```

### データフロー (SSE による会話タイトル生成)

```
1. ユーザーが最初のメッセージ送信
   ↓
2. Backend: チャット応答生成（ストリーミング）
   → SSE: data: {"type":"message","content":"..."}\n\n
   ↓
3. Backend: タイトル生成（LLM使用）
   ↓
4. Backend: DBに保存 & SSE送信
   → SSE: data: {"type":"title","title":"要約されたタイトル"}\n\n
   ↓
5. Frontend: タイトルをリアルタイム更新
```

## 🛠 技術スタック

### Frontend
- **言語**: TypeScript
- **Framework**: Next.js 15 (App Router)
- **UI**: Tailwind CSS
- **通信**: Server-Sent Events (SSE)

### Backend
- **言語**: Python 3.11+
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Migration**: Alembic

### Database & Search
- **RDB**: PostgreSQL (会話履歴・メッセージ保存)
- **Vector DB**: Azure AI Search (ドキュメント検索)

### AI/LLM
- **LLM**: OpenAI GPT-4o-mini (チャット応答・タイトル生成)
- **Embedding**: text-embedding-3-small (ベクトル化)

## 📂 プロジェクト構成

```
rag-practice/
├── backend/
│   ├── main.py                    # FastAPI アプリケーション
│   ├── dependencies.py            # 依存性注入
│   ├── logger.py                  # 構造化ログ
│   ├── exceptions.py              # カスタム例外
│   ├── middleware.py              # リクエストログ
│   ├── exception_handlers.py      # 例外ハンドラー
│   ├── models.py                  # SQLModel データモデル
│   ├── upload_handbook.py         # データ登録スクリプト
│   ├── utils.py                   # ユーティリティ関数
│   │
│   ├── routers/                   # API層
│   │   ├── chat.py                # チャット API
│   │   └── conversation.py        # 会話管理 API
│   │
│   ├── services/                  # ビジネスロジック層
│   │   └── chat_service.py        # RAG処理・タイトル生成
│   │
│   ├── repositories/              # データアクセス層
│   │   ├── conversation_repository.py   # 会話CRUD
│   │   └── search_repository.py         # Azure AI Search操作
│   │
│   ├── alembic/                   # DBマイグレーション
│   │   └── versions/              # マイグレーションファイル
│   │
│   └── .env                       # 環境変数（未コミット）
│
└── frontend/
    ├── app/
    │   ├── page.tsx               # メインページ
    │   └── components/            # React コンポーネント
    │       ├── Header.tsx
    │       ├── Sidebar.tsx        # 会話一覧
    │       ├── MessageDisplay.tsx
    │       └── SendMessage.tsx    # SSE対応チャット送信
    │
    ├── lib/
    │   └── api.ts                 # API クライアント
    │
    └── types/
        └── index.ts               # TypeScript 型定義
```

## 🚀 環境構築 (Setup)

### 前提条件

- Node.js 18+
- Python 3.11+
- PostgreSQL 14+
- pnpm (推奨) または npm

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd rag-practice
```

### 2. PostgreSQL のセットアップ

#### Docker を使用する場合（推奨）

```bash
# docker-compose.yml があれば
docker-compose up -d db

# または手動で
docker run -d \
  --name rag-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=rag_practice \
  -p 5432:5432 \
  postgres:14
```

#### ローカルにインストールする場合

PostgreSQL をインストール後、データベースを作成：

```sql
CREATE DATABASE rag_practice;
```

### 3. 環境変数の設定

`backend/.env` ファイルを作成：

```ini
# OpenAI API
OPENAI_API_KEY=sk-...

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://...
AZURE_SEARCH_ADMIN_KEY=...

# PostgreSQL
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag_practice
```

### 4. 依存関係のインストール

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend

```bash
cd frontend
pnpm install  # または npm install
```

### 5. データベースマイグレーション

```bash
cd backend
alembic upgrade head
```

### 6. テストデータの投入

Azure AI Search に社内規定データを登録：

```bash
cd backend
python upload_handbook.py
```

## ▶️ 実行方法 (Usage)

### Backend の起動

```bash
cd backend
uvicorn main:app --reload
```

- **API Docs**: http://localhost:8000/docs

### Frontend の起動

```bash
cd frontend
pnpm dev  # または npm run dev
```

- **Chat UI**: http://localhost:3000

## 🗄 データベース操作

### マイグレーションの作成

モデルを変更した後：

```bash
cd backend
alembic revision --autogenerate -m "変更内容の説明"
alembic upgrade head
```

### マイグレーション履歴の確認

```bash
alembic history
alembic current
```

### ロールバック

```bash
alembic downgrade -1  # 1つ前に戻る
alembic downgrade <revision_id>  # 特定のバージョンに戻る
```

## 🧪 開発時のヒント

### バックエンドのログ確認

構造化ログが出力されます：

```bash
tail -f backend/logs/app.log
```

### 型チェック（推奨設定）

`.vscode/settings.json`:

```json
{
  "python.analysis.typeCheckingMode": "standard"
}
```

### SSE デバッグ

ブラウザの Developer Tools → Network タブで：
- `EventStream` タイプのリクエストを確認
- `data: {...}\n\n` 形式のレスポンスを確認

## 🐛 トラブルシューティング

### PostgreSQL 接続エラー

```bash
# PostgreSQL が起動しているか確認
docker ps  # Docker使用の場合
pg_isready  # ローカルインストールの場合

# DATABASE_URL が正しいか確認
echo $DATABASE_URL
```

### Alembic マイグレーションエラー

```bash
# 現在のステータス確認
alembic current

# マイグレーション履歴確認
alembic history

# 最新に更新
alembic upgrade head
```

### フロントエンド型エラー

```bash
# node_modules を削除して再インストール
rm -rf node_modules
pnpm install
```

## 📝 ライセンス

学習用プロジェクトのため、ライセンスは指定していません。
