# RAGシステム開発 学習カリキュラム (9日間 + エクストラ)

9日間 + 週末でPython/FastAPI/Azure AI Search/RAGの技術力を最大化するための学習プランです。

## 🎯 このカリキュラムのゴール

**このプロジェクト（rag-practice）を段階的に改善しながら、実践的な技術を習得します。**

最終的に以下の状態を目指します:

- ✅ 本番運用可能なコード品質（型安全、テスト、ログ）
- ✅ ハイブリッド検索による高精度なRAG
- ✅ 会話履歴のDB永続化
- ✅ Dockerコンテナとしてデプロイ可能

```
【学習の流れ】
Day 1-3: コード品質の向上（ロギング、エラーハンドリング、テスト）
    ↓
Day 4-5: 検索精度の向上（ハイブリッド検索、セマンティック検索）
    ↓
Day 6-8: DB永続化とRAG精度向上（SQLModel + PostgreSQL、クエリ改善）
    ↓
Day 9: アーキテクチャとデプロイ準備（レイヤー分離、Docker化）
```

---

## � 日程別: プロジェクトに追加される機能・改善

各日程のカリキュラムを完了すると、このRAGチャットボットに以下の機能・改善が追加されます。

### 現在の状態（Before）

```
rag-practice/
├── backend/
│   ├── main.py          # 基本的なチャットAPI
│   ├── clients.py       # OpenAI/Azure接続
│   ├── utils.py         # Embedding取得
│   └── upload_handbook.py
└── frontend/            # Next.js チャットUI
```

**現在の機能:**

- ✅ 基本的なRAGチャット
- ✅ ベクトル検索
- ✅ Query Rewriting（簡易版）
- ✅ ストリーミング応答
- ❌ 型安全性なし
- ❌ ログ出力なし
- ❌ テストなし
- ❌ 会話履歴の永続化なし
- ❌ ハイブリッド検索なし

---

### Day 1 完了後: コード品質の基盤

| 追加されるファイル      | 内容               |
| :---------------------- | :----------------- |
| `backend/logger.py`     | 統一ログ出力機能   |
| `backend/exceptions.py` | カスタム例外クラス |

**チャットボットの変化:**

- 🆕 **全ファイルに型ヒント追加** → IDEの補完が効き、バグを事前に発見
- 🆕 **構造化ログ出力** → 本番障害時に原因特定が可能
- 🆕 **カスタム例外** → エラー種別ごとに適切な処理が可能

```python
# Before
async def get_embedding(text):
    response = await openai_client.embeddings.create(...)
    return response.data[0].embedding

# After
async def get_embedding(text: str) -> list[float]:
    try:
        response = await openai_client.embeddings.create(...)
        logger.info(f"Embedding created: {len(response.data[0].embedding)} dims")
        return response.data[0].embedding
    except OpenAIError as e:
        logger.error(f"Embedding error: {e}")
        raise EmbeddingError(str(e))
```

---

### Day 2 完了後: 設計の改善

| 追加されるファイル        | 内容             |
| :------------------------ | :--------------- |
| `backend/dependencies.py` | 依存性注入の定義 |
| `backend/schemas.py`      | Pydanticスキーマ |
| `backend/routers/chat.py` | APIルーター      |

**チャットボットの変化:**

- 🆕 **依存性注入** → クライアントの差し替えが容易（テスト時にモック可能）
- 🆕 **入力バリデーション強化** → 不正なリクエストを自動拒否
- 🆕 **APIバージョニング** → `/api/v1/chat` のようなURL設計

```python
# Before: グローバル変数を直接使用
@app.post("/chat")
async def create_chat(request: ChatRequest):
    results = search_client.search(...)

# After: 依存性注入でテスト可能に
@router.post("/chat")
async def create_chat(
    request: ChatRequest,
    search: SearchClient = Depends(get_search_client)
):
    results = search.search(...)
```

---

### Day 3 完了後: 品質保証

| 追加されるファイル              | 内容                       |
| :------------------------------ | :------------------------- |
| `backend/middleware.py`         | リクエストログミドルウェア |
| `backend/exception_handlers.py` | 例外ハンドラー             |
| `backend/tests/test_chat.py`    | APIテスト                  |

**チャットボットの変化:**

- 🆕 **リクエストログ** → 全APIリクエストの処理時間を自動記録
- 🆕 **統一エラーレスポンス** → クライアントに分かりやすいエラー形式
- 🆕 **自動テスト** → `pytest` でAPIの動作を保証

```json
// 統一されたエラーレスポンス
{
  "error": "Embedding generation failed",
  "type": "EmbeddingError",
  "request_id": "abc-123"
}
```

---

### Day 4-5 完了後: 検索精度の大幅向上

| 追加されるファイル         | 内容                             |
| :------------------------- | :------------------------------- |
| `backend/index_manager.py` | インデックス管理                 |
| `backend/search.py`        | 検索ロジック（リファクタリング） |

**チャットボットの変化:**

- 🆕 **ハイブリッド検索** → ベクトル検索 + キーワード検索の組み合わせ
- 🆕 **セマンティックランカー** → AIによる検索結果のリランキング
- 🆕 **フィルタリング** → カテゴリや日付で検索結果を絞り込み

```python
# Before: ベクトル検索のみ
results = search_client.search(
    search_text=None,
    vector_queries=[{"vector": vector_query, "k": 2, ...}]
)

# After: ハイブリッド検索
results = search_client.search(
    search_text=query,           # キーワード検索
    vector_queries=[vector_query],  # ベクトル検索
    query_type="semantic",        # セマンティックランカー
    filter="category eq '人事規定'"  # フィルタリング
)
```

**期待される効果:**

- 検索精度が 20-30% 向上（一般的なケース）
- 「育児休暇」で検索 → 関連ワード「産休」「育休」「子育て支援」もヒット

---

### Day 6 完了後: SQLModel + PostgreSQL によるDB永続化 ⭐

| 追加されるファイル                                | 内容                         |
| :------------------------------------------------ | :--------------------------- |
| `backend/models.py`                               | SQLModel モデル定義          |
| `backend/repositories/conversation_repository.py` | リポジトリパターンによるCRUD |
| `backend/database.py`                             | DB接続設定                   |
| `docker-compose.yml`                              | PostgreSQL 環境              |
| `alembic/`                                        | マイグレーション             |

**チャットボットの変化:**

- 🆕 **SQLModel による型安全なDB操作** → Pydantic統合で開発体験向上
- 🆕 **PostgreSQL をDocker環境で使用** → 本番環境に近い構成
- 🆕 **リポジトリパターンでデータアクセス層を分離** → テスト可能で保守しやすい設計
- 🆕 **会話履歴のDB保存** → ブラウザを閉じても会話を再開可能
- 🆕 **会話セッション管理** → 複数の会話を切り替え可能

```python
# リポジトリパターンによる抽象化
class ConversationRepository:
    def create_conversation(self) -> Conversation: ...
    def add_message(self, conv_id: str, role: str, content: str) -> Message: ...
    def get_conversation_history(self, conv_id: str) -> list[Message]: ...
```

**新規API:**

```
POST /api/v1/conversations     → 新規会話作成
GET  /api/v1/conversations     → 会話一覧取得
GET  /api/v1/conversations/:id → 会話詳細取得
DELETE /api/v1/conversations/:id → 会話削除
```

**DBスキーマ (SQLModel):**

```
conversations (会話セッション)
├── id: str
├── created_at: datetime
└── messages: list[Message] (Relationship)
    ├── id: str
    ├── conversation_id: str (ForeignKey)
    ├── role: str (user/assistant)
    ├── content: str
    └── created_at: datetime
```

---

### Day 7 完了後: Query Rewritingの精度向上

| 追加/修正されるファイル     | 内容                    |
| :-------------------------- | :---------------------- |
| `backend/prompts.py`        | プロンプトテンプレート  |
| `backend/query_rewriter.py` | Query Rewritingロジック |

**チャットボットの変化:**

- 🆕 **改善されたQuery Rewriting** → 代名詞解決の精度向上
- 🆕 **プロンプトの外部化** → プロンプトの管理・調整が容易
- 🆕 **A/Bテスト基盤** → プロンプト比較が可能

```
会話例（改善前）:
User: 育児休暇について教えて
Bot: 育児休暇は...
User: それは男性も取れますか？
→ 検索クエリ: 「それは男性も取れますか？」（曖昧）

会話例（改善後）:
User: 育児休暇について教えて
Bot: 育児休暇は...
User: それは男性も取れますか？
→ 検索クエリ: 「育児休暇は男性も取得できるか」（明確）
```

---

### Day 8 完了後: 回答品質の向上

| 追加/修正されるファイル       | 内容             |
| :---------------------------- | :--------------- |
| `backend/response_builder.py` | 回答生成ロジック |

**チャットボットの変化:**

- 🆕 **スコア閾値フィルタ** → 低品質な検索結果を除外
- 🆕 **回答なしハンドリング** → 関連情報がない場合の適切な応答
- 🆕 **引用元の改善表示** → ソースの信頼性を明示

```
改善前の応答:
「育児休暇は取得できます。」
【出典: handbook.pdf (P.12)】

改善後の応答:
「育児休暇は取得できます。」

📚 参考情報:
[1] 人事規定書 - 第5章 休暇制度 (P.12-15) [関連度: 高]
[2] 育児支援ガイド - Q&A集 (P.3) [関連度: 中]

※ 2件の規定を参照して回答しました。
```

---

### Day 9 完了後: レイヤー分離 + 本番デプロイ可能 ⭐

| 追加されるファイル                          | 内容                           |
| :------------------------------------------ | :----------------------------- |
| `backend/routers/chat.py`                   | プレゼンテーション層（Router） |
| `backend/services/chat_service.py`          | ビジネスロジック層（Service）  |
| `backend/repositories/search_repository.py` | データアクセス層（Repository） |
| `backend/Dockerfile`                        | コンテナ定義                   |
| `backend/config.py`                         | 設定管理                       |
| `docker-compose.yml`                        | 開発環境定義                   |

**チャットボットの変化:**

- 🆕 **3層アーキテクチャへのリファクタリング** → 責務が明確になり保守性が大幅向上
- 🆕 **routers/ (プレゼンテーション層)** → HTTPリクエスト処理のみに専念
- 🆕 **services/ (ビジネスロジック層)** → RAGパイプライン、Query Rewriting
- 🆕 **repositories/ (データアクセス層)** → DB、Azure AI Searchへのアクセス抽象化
- 🆕 **Dockerコンテナ化** → どの環境でも同じ動作を保証
- 🆕 **型安全な設定管理** → 環境変数の検証付き読み込み

```python
# Before: main.py に全てが集中
main.py (500行)

# After: レイヤー分離
routers/chat.py         # HTTPリクエスト処理
services/chat_service.py # ビジネスロジック
repositories/
  ├── search_repository.py      # Azure AI Search
  └── conversation_repository.py # DB操作
```

```bash
# デプロイコマンド
docker-compose up -d  # DB + Backend を一括起動
```

---

### 完成後の状態（After）

```
rag-practice/
├── backend/
│   ├── main.py              # エントリーポイント
│   ├── config.py            # 設定管理 [NEW]
│   ├── logger.py            # ログ設定 [NEW]
│   ├── exceptions.py        # カスタム例外 [NEW]
│   ├── dependencies.py      # 依存性注入 [NEW]
│   ├── schemas.py           # Pydanticスキーマ [NEW]
│   ├── middleware.py        # ミドルウェア [NEW]
│   ├── exception_handlers.py # 例外ハンドラー [NEW]
│   ├── models.py            # SQLAlchemyモデル [NEW]
│   ├── crud.py              # CRUD操作 [NEW]
│   ├── database.py          # DB接続 [NEW]
│   ├── prompts.py           # プロンプト [NEW]
│   ├── query_rewriter.py    # Query Rewriting [NEW]
│   ├── search.py            # 検索ロジック [NEW]
│   ├── response_builder.py  # 回答生成 [NEW]
│   ├── index_manager.py     # インデックス管理 [NEW]
│   ├── routers/
│   │   └── chat.py          # チャットAPI [NEW]
│   ├── tests/
│   │   └── test_chat.py     # テスト [NEW]
│   ├── Dockerfile           # コンテナ定義 [NEW]
│   └── ...
├── alembic/                  # マイグレーション [NEW]
├── docker-compose.yml        # 開発環境 [NEW]
└── frontend/
```

**完成後の機能:**

- ✅ 基本的なRAGチャット
- ✅ **ハイブリッド検索**（ベクトル + キーワード）
- ✅ **セマンティックランカー**
- ✅ **改善されたQuery Rewriting**
- ✅ ストリーミング応答
- ✅ **型安全なコード**
- ✅ **構造化ログ**
- ✅ **自動テスト**
- ✅ **会話履歴のDB永続化**
- ✅ **Dockerデプロイ可能**

---

## 📅 スケジュール概要

| Day       | テーマ                   | 学ぶ理由                                 | ゴール                             |
| :-------- | :----------------------- | :--------------------------------------- | :--------------------------------- |
| **Day 1** | Python深化               | 実務コードは型安全・ログ・例外処理が必須 | 保守しやすいコードが書ける         |
| **Day 2** | FastAPI実践 (1)          | DIやバリデーションは大規模開発の基本     | テストしやすい設計ができる         |
| **Day 3** | FastAPI実践 (2)          | 一貫したエラー処理とテストで品質担保     | APIの品質を保証できる              |
| **Day 4** | Azure AI Search (1)      | インデックス設計が検索精度を左右する     | 適切なインデックスを設計できる     |
| **Day 5** | Azure AI Search (2)      | ハイブリッド検索で精度が大幅向上         | 実務レベルの検索を実装できる       |
| **休日**  | 週末                     | 復習と発展学習                           | Week 1の定着                       |
| **Day 6** | SQLModel + PostgreSQL ⭐ | SQLModelとリポジトリパターンで保守性向上 | 型安全なDB操作ができる             |
| **Day 7** | RAG実装深化 (1)          | Query Rewritingの精度が回答品質を決める  | 文脈を理解した検索ができる         |
| **Day 8** | RAG実装深化 (2)          | 検索結果の処理で最終的な回答品質が決まる | 信頼性の高い回答を生成できる       |
| **Day 9** | レイヤー分離 + Docker ⭐ | 保守性向上とデプロイ準備は必須           | 実務レベルのアーキテクチャが組める |
| **休日**  | バッファ                 | 遅れの調整、総復習                       | 知識の定着と総仕上げ               |
| **休日**  | Extra                    | CI/CD、最終確認                          | 発展的なスキル習得                 |

---

## 👤 前提条件

- **学習時間**: 8時間/日 × 9日 = 72時間（目安）
- **休日**: エクストラ学習（任意）
- **想定スキルレベル**:
  - プログラミング基礎知識（いずれかの言語での開発経験）
  - Web開発の基礎知識（API、HTTP、JSONなど）
  - SQLの基本的な知識

---

## 📚 詳細カリキュラム

---

### Day 1: Python Deep Dive

#### 💡 なぜこれを学ぶのか

| 学習内容       | なぜ必要か                               | できるようになること                |
| :------------- | :--------------------------------------- | :---------------------------------- |
| 型ヒント       | 大規模開発ではバグ防止・コード理解に必須 | IDEの補完が効き、バグを事前に防げる |
| 非同期処理     | API開発で並列処理は必須スキル            | 効率的なI/O処理が書ける             |
| ログ・例外処理 | 本番障害時の調査に必須                   | 問題発生時に原因特定ができる        |

**目標**: 堅牢で保守性の高いPythonコードが書けるようになる。

#### ⏰ 時間配分

| 時間             | 内容                                |
| :--------------- | :---------------------------------- |
| 9:00-11:00 (2h)  | 型ヒント (Type Hints) の学習        |
| 11:00-13:00 (2h) | 非同期処理 (AsyncIO) の学習         |
| 14:00-16:00 (2h) | エラーハンドリング & ロギングの学習 |
| 16:00-18:00 (2h) | 🛠️ 実践課題: プロジェクトに適用     |

#### 📖 学習内容

**型ヒント (Type Hints)**

- `list[str]`, `dict[str, Any]` などの基本
- `Optional`, `Union` の使い分け
- `TypedDict`, `Literal` の活用
- `mypy` を使った静的解析の導入

**非同期処理 (AsyncIO)**

- `async` / `await` の仕組み理解
- `asyncio.gather` による並列処理
- 同期コードと非同期コードの混在時の注意点
- `asyncio.create_task` によるバックグラウンド処理

**エラーハンドリング & ロギング**

- `try-except` のベストプラクティス
- カスタム例外クラスの作成
- `logging` モジュールによる適切なログレベル設計
- **構造化ログ（JSON形式）の導入** ⭐
- **リクエスト/レスポンスの全量ログ** ⭐
- **本番運用を想定したログレベル設計** ⭐

#### 🛠️ 実践課題: rag-practiceに適用

1. **型ヒントの厳格化**
   - `main.py`, `utils.py`, `clients.py` の全関数に型ヒントを追加
   - `mypy --strict` でエラーがないか確認

2. **構造化ロガーの実装**

   ```python
   # backend/logger.py を新規作成
   import logging
   import json
   from datetime import datetime

   class JSONFormatter(logging.Formatter):
       def format(self, record):
           log_data = {
               "timestamp": datetime.utcnow().isoformat(),
               "level": record.levelname,
               "message": record.getMessage(),
               "module": record.module,
           }
           if record.exc_info:
               log_data["exception"] = self.formatException(record.exc_info)
           return json.dumps(log_data, ensure_ascii=False)

   def get_logger(name: str) -> logging.Logger:
       logger = logging.getLogger(name)
       handler = logging.StreamHandler()
       handler.setFormatter(JSONFormatter())
       logger.addHandler(handler)
       logger.setLevel(logging.INFO)
       return logger
   ```

3. **リクエスト/レスポンスログミドルウェア**

   ```python
   # backend/middleware.py を新規作成
   import time
   from starlette.middleware.base import BaseHTTPMiddleware
   from logger import get_logger

   logger = get_logger(__name__)

   class LoggingMiddleware(BaseHTTPMiddleware):
       async def dispatch(self, request, call_next):
           start_time = time.time()

           # リクエストログ
           logger.info(f"Request: {request.method} {request.url.path}")

           response = await call_next(request)

           # レスポンスログ
           duration = time.time() - start_time
           logger.info(f"Response: {response.status_code} - {duration:.3f}s")

           return response
   ```

4. **カスタム例外クラス**

   ```python
   # backend/exceptions.py を新規作成
   class RAGException(Exception):
       """RAGシステムの基底例外"""
       pass

   class EmbeddingError(RAGException):
       """Embedding生成時のエラー"""
       pass

   class SearchError(RAGException):
       """検索実行時のエラー"""
       pass
   ```

#### 📚 参考リソース

- [Python 型ヒント公式ドキュメント](https://docs.python.org/ja/3/library/typing.html)
- [Real Python - Async IO](https://realpython.com/async-io-python/)
- [Python Logging HOWTO](https://docs.python.org/ja/3/howto/logging.html)
- [FastAPI - Request/Response Logging](https://medium.com/@joerosborne/how-to-log-every-request-and-response-in-fastapi-dcf8d2be2055) ⭐

---

### Day 2: FastAPI実践 (1)

#### 💡 なぜこれを学ぶのか

| 学習内容        | なぜ必要か                             | できるようになること                      |
| :-------------- | :------------------------------------- | :---------------------------------------- |
| 依存性注入 (DI) | テスト可能な設計、モジュール分離に必須 | DBやAPIクライアントを差し替え可能にできる |
| Pydantic        | 入力バリデーションで不正データを防ぐ   | 安全なAPI入力処理ができる                 |
| APIRouter       | 大規模APIの整理に必須                  | エンドポイントを整理して管理できる        |

**目標**: 依存性注入とPydanticによる堅牢なAPI設計パターンを習得する。

#### ⏰ 時間配分

| 時間             | 内容                              |
| :--------------- | :-------------------------------- |
| 9:00-11:00 (2h)  | 依存性注入 (Dependency Injection) |
| 11:00-13:00 (2h) | Pydantic バリデーション           |
| 14:00-16:00 (2h) | APIRouter によるモジュール分割    |
| 16:00-18:00 (2h) | 🛠️ 実践課題: プロジェクトに適用   |

#### 📖 学習内容

**Dependency Injection (DI)**

- `Depends` を使ったDBセッションやAPIクライアントの注入
- 依存関係のネスト（依存の依存）
- `yield` を使ったリソースのクリーンアップ
- テスト時のモック差し替えの容易さを体感する

**Pydantic バリデーション**

- `BaseModel` の `Field` 設定（制約、説明、例）
- バリデーター (`@field_validator`, `@model_validator`) の実装
- エイリアス、シリアライズ設定
- `pydantic-settings` による設定管理

**APIRouter**

- ルーターによるエンドポイントのグループ化
- プレフィックス、タグの設定
- ルーターのインクルード

#### 🛠️ 実践課題: rag-practiceに適用

1. **依存性注入でクライアント管理**

   ```python
   # backend/dependencies.py を新規作成
   from fastapi import Depends
   from clients import search_client, openai_client

   async def get_search_client():
       return search_client

   async def get_openai_client():
       return openai_client
   ```

2. **Pydanticモデルの強化**

   ```python
   # backend/schemas.py を新規作成
   from pydantic import BaseModel, Field

   class Message(BaseModel):
       role: str = Field(..., pattern="^(user|assistant|system)$")
       content: str = Field(..., min_length=1, max_length=10000)

   class ChatRequest(BaseModel):
       messages: list[Message] = Field(..., min_length=1)

   class ChatResponse(BaseModel):
       message: str
       sources: list[dict] = []
   ```

3. **APIルーターの導入**

   ```python
   # backend/routers/chat.py を新規作成
   from fastapi import APIRouter

   router = APIRouter(prefix="/api/v1", tags=["chat"])

   @router.post("/chat")
   async def create_chat(...):
       ...
   ```

#### 📚 参考リソース

- [FastAPI 公式: Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI 公式: Request Body - Nested Models](https://fastapi.tiangolo.com/tutorial/body-nested-models/)
- [Pydantic V2 ドキュメント](https://docs.pydantic.dev/latest/)

---

### Day 3: FastAPI実践 (2)

#### 💡 なぜこれを学ぶのか

| 学習内容     | なぜ必要か                               | できるようになること                     |
| :----------- | :--------------------------------------- | :--------------------------------------- |
| ミドルウェア | リクエストログ、認証など横断的処理に必須 | 全APIに共通処理を適用できる              |
| 例外処理統一 | 一貫したエラーレスポンスはAPI品質の基本  | クライアントに分かりやすいエラーを返せる |
| テスト       | 品質担保、リグレッション防止に必須       | コード変更時に安心してデプロイできる     |

**目標**: ミドルウェア、例外ハンドリング、テストの実装パターンを習得する。

#### ⏰ 時間配分

| 時間             | 内容                            |
| :--------------- | :------------------------------ |
| 9:00-11:00 (2h)  | ミドルウェアのカスタマイズ      |
| 11:00-13:00 (2h) | 例外処理の統一                  |
| 14:00-16:00 (2h) | pytest によるユニットテスト     |
| 16:00-18:00 (2h) | 🛠️ 実践課題: プロジェクトに適用 |

#### 📖 学習内容

**Middleware**

- リクエスト/レスポンスのログ出力
- 処理時間の計測
- 認証ミドルウェアの考え方

**例外処理の統一** ⭐

- `HTTPException` の使い方
- **カスタム例外ハンドラーの登録（グローバルハンドラー）**
- **エラーレスポンスの統一フォーマット**
- **本番環境でのエラー情報の適切な隠蔽**
- **例外発生時のログ記録とアラート設計**

**pytest 基礎**

- `TestClient` によるAPIテスト
- フィクスチャ (`@pytest.fixture`)
- `unittest.mock` によるモック

#### 🛠️ 実践課題: rag-practiceに適用

1. **リクエストログミドルウェア**

   ```python
   # backend/middleware.py
   import time
   from starlette.middleware.base import BaseHTTPMiddleware

   class LoggingMiddleware(BaseHTTPMiddleware):
       async def dispatch(self, request, call_next):
           start = time.time()
           response = await call_next(request)
           duration = time.time() - start
           logger.info(f"{request.method} {request.url.path} - {duration:.3f}s")
           return response
   ```

2. **グローバル例外ハンドラーの実装**

   ```python
   # backend/exception_handlers.py
   from fastapi import Request, status
   from fastapi.responses import JSONResponse
   from logger import get_logger
   import traceback

   logger = get_logger(__name__)

   async def rag_exception_handler(request: Request, exc: RAGException):
       # エラーログ記録
       logger.error(f"RAG Error: {str(exc)}", exc_info=True)

       return JSONResponse(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           content={
               "error": "システムエラーが発生しました",  # 本番では詳細を隠す
               "type": exc.__class__.__name__,
               "detail": str(exc) if app.debug else None  # デバッグ時のみ詳細表示
           }
       )

   async def general_exception_handler(request: Request, exc: Exception):
       # 予期しないエラーの記録
       logger.critical(f"Unexpected error: {str(exc)}", exc_info=True)

       return JSONResponse(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           content={"error": "予期しないエラーが発生しました"}
       )
   ```

3. **テストの作成**

   ```python
   # backend/tests/test_chat.py
   from fastapi.testclient import TestClient
   from main import app

   client = TestClient(app)

   def test_chat_endpoint_success():
       response = client.post("/chat", json={
           "messages": [{"role": "user", "content": "育児休暇について"}]
       })
       assert response.status_code == 200
   ```

#### 📚 参考リソース

- [FastAPI 公式: Middleware](https://fastapi.tiangolo.com/tutorial/middleware/)
- [FastAPI 公式: Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [FastAPI 公式: Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

### Day 4: Azure AI Search (1)

#### 💡 なぜこれを学ぶのか

| 学習内容         | なぜ必要か                     | できるようになること                   |
| :--------------- | :----------------------------- | :------------------------------------- |
| インデックス設計 | 検索精度・パフォーマンスの土台 | 要件に合ったインデックスを設計できる   |
| アナライザー     | 日本語検索の精度に直結         | 日本語を適切にトークナイズできる       |
| Python SDK       | 実装に必須                     | プログラムからインデックスを操作できる |

**目標**: インデックス設計と基本的な検索クエリを理解する。

#### ⏰ 時間配分

| 時間             | 内容                            |
| :--------------- | :------------------------------ |
| 9:00-11:00 (2h)  | インデックス設計の基礎          |
| 11:00-13:00 (2h) | フィールド属性とアナライザー    |
| 14:00-16:00 (2h) | Python SDK による操作           |
| 16:00-18:00 (2h) | 🛠️ 実践課題: プロジェクトに適用 |

#### 📖 学習内容

**インデックス設計**

- フィールドタイプ（`Edm.String`, `Collection(Edm.Single)` 等）
- フィールド属性 (`searchable`, `filterable`, `sortable`, `facetable`)
- ベクトルフィールドの設定（次元数、類似度アルゴリズム）

**アナライザー**

- 日本語アナライザー (`ja.microsoft`, `ja.lucene`) の違い
- カスタムアナライザーの概念

**Python SDK**

- `azure-search-documents` パッケージの使い方
- `SearchIndexClient` によるインデックス管理
- `SearchClient` によるドキュメント操作

#### 🛠️ 実践課題: rag-practiceに適用

1. **インデックス定義の確認・改善**

   ```python
   # backend/index_manager.py を新規作成
   from azure.search.documents.indexes import SearchIndexClient
   from azure.search.documents.indexes.models import (
       SearchIndex,
       SearchField,
       SearchFieldDataType,
       VectorSearch,
       HnswAlgorithmConfiguration,
   )

   def create_handbook_index(client: SearchIndexClient):
       fields = [
           SearchField(name="id", type=SearchFieldDataType.String, key=True),
           SearchField(name="content", type=SearchFieldDataType.String,
                      searchable=True, analyzer_name="ja.microsoft"),
           SearchField(name="category", type=SearchFieldDataType.String,
                      filterable=True, facetable=True),
           SearchField(name="embedding", type=SearchFieldDataType.Collection(
               SearchFieldDataType.Single),
               vector_search_dimensions=1536,
               vector_search_profile_name="myHnswProfile"),
       ]
       # インデックス作成...
   ```

2. **既存インデックスの分析**
   - Azure Portal でインデックス定義を確認
   - 改善点をドキュメント化

#### 📚 参考リソース

- [Azure AI Search インデックス設計](https://learn.microsoft.com/ja-jp/azure/search/search-what-is-an-index)
- [Azure AI Search Python SDK](https://learn.microsoft.com/ja-jp/python/api/overview/azure/search-documents-readme)
- [日本語アナライザー](https://learn.microsoft.com/ja-jp/azure/search/index-add-language-analyzers)

---

### Day 5: Azure AI Search (2)

#### 💡 なぜこれを学ぶのか

| 学習内容           | なぜ必要か                       | できるようになること               |
| :----------------- | :------------------------------- | :--------------------------------- |
| ハイブリッド検索   | ベクトル検索単体より精度が向上   | キーワード＋意味の両方で検索できる |
| セマンティック検索 | AIによるリランキングで精度向上   | より関連性の高い結果を上位に出せる |
| フィルタリング     | メタデータで絞り込みは実務で必須 | カテゴリや日付で検索結果を絞れる   |

**目標**: ハイブリッド検索とセマンティック検索を実装できるようになる。

#### ⏰ 時間配分

| 時間             | 内容                                       |
| :--------------- | :----------------------------------------- |
| 9:00-11:00 (2h)  | ハイブリッド検索の理論と実装               |
| 11:00-13:00 (2h) | セマンティック検索とセマンティックランカー |
| 14:00-16:00 (2h) | フィルタリングとファセット                 |
| 16:00-18:00 (2h) | 🛠️ 実践課題: プロジェクトに適用            |

#### 📖 学習内容

**ハイブリッド検索**

- キーワード検索とベクトル検索の組み合わせ
- RRF (Reciprocal Rank Fusion) によるスコア統合
- 各検索手法の重み付け

**セマンティック検索**

- セマンティック構成の設定
- セマンティックランカーによるリランキング
- キャプションとアンサーの抽出

**フィルタリング**

- OData フィルター構文
- 複合条件（AND, OR, NOT）
- 日付範囲、数値範囲

#### 🛠️ 実践課題: rag-practiceに適用

1. **ハイブリッド検索の実装**

   ```python
   # main.py の検索処理を改善
   from azure.search.documents.models import VectorizedQuery

   async def hybrid_search(query: str, vector: list[float], category: str = None):
       vector_query = VectorizedQuery(
           vector=vector,
           k_nearest_neighbors=3,
           fields="embedding"
       )

       filter_expr = f"category eq '{category}'" if category else None

       results = search_client.search(
           search_text=query,  # キーワード検索
           vector_queries=[vector_query],  # ベクトル検索
           filter=filter_expr,
           query_type="semantic",
           semantic_configuration_name="my-semantic-config",
           top=5
       )
       return list(results)
   ```

2. **検索結果の比較検証**
   - ベクトルのみ vs ハイブリッド の結果を比較
   - 検索クエリごとの精度をログに記録

#### 📚 参考リソース

- [Azure AI Search ハイブリッド検索](https://learn.microsoft.com/ja-jp/azure/search/hybrid-search-overview)
- [セマンティック検索の概要](https://learn.microsoft.com/ja-jp/azure/search/semantic-search-overview)
- [OData フィルター構文](https://learn.microsoft.com/ja-jp/azure/search/search-query-odata-filter)

---

### 🌟 Extra: Week 1 週末

#### 推奨タスク

1. **Week 1 の復習**
   - 作成したコードのリファクタリング
   - 理解が浅い部分の再学習

2. **RAG評価手法の調査**
   - `Ragas` フレームワークの概要把握
   - 評価指標（Faithfulness, Answer Relevance, Context Precision）の理解

3. **LangChain の概要把握**
   - LangChain の基本コンセプト
   - 実務で使用される可能性に備えて概要を把握

---

### Day 6: Database & SQL

#### 💡 なぜこれを学ぶのか

| 学習内容         | なぜ必要か                     | できるようになること           |
| :--------------- | :----------------------------- | :----------------------------- |
| SQLAlchemy       | PythonでのDB操作の標準的な方法 | 型安全にDBを操作できる         |
| Alembic          | スキーマ変更の履歴管理に必須   | DBの変更を安全にデプロイできる |
| データモデリング | 会話履歴は必須機能             | 会話を永続化して再開できる     |

**目標**: 会話履歴を永続化するデータ層を実装する。

#### ⏰ 時間配分

| 時間             | 内容                                |
| :--------------- | :---------------------------------- |
| 9:00-10:00 (1h)  | PostgreSQL (Docker) 環境構築        |
| 10:00-12:00 (2h) | SQLModel 基礎 + モデル定義          |
| 12:00-14:00 (2h) | Alembic マイグレーション            |
| 14:00-16:00 (2h) | リポジトリパターンによるCRUD実装    |
| 16:00-18:00 (2h) | 🛠️ 実践課題: 会話履歴機能の完全実装 |

#### 📖 学習内容

**PostgreSQL (Docker)**

- Docker Compose による PostgreSQL 環境構築
- データベース、ユーザー、パスワードの設定
- ローカル開発環境でのDB接続

**SQLModel** ⭐

- Pydantic + SQLAlchemy の統合
- モデル定義（テーブルとPydanticモデルの兼用）
- リレーションシップ（Relationship）
- 基本的なCRUD操作

**Alembic**

- Alembic初期化とマイグレーション設定
- オートマイグレーション（`alembic revision --autogenerate`）
- マイグレーション適用（`alembic upgrade head`）

**リポジトリパターン** ⭐

- データアクセスロジックの分離
- `repositories/` ディレクトリの作成
- テスト可能な設計

#### 🛠️ 実践課題: rag-practiceに適用

1. **Docker Composeで PostgreSQL 環境構築**

   ```yaml
   # docker-compose.yml（既存ファイルに追加）
   services:
     db:
       image: postgres:15
       environment:
         POSTGRES_USER: raguser
         POSTGRES_PASSWORD: ragpass
         POSTGRES_DB: rag_practice
       ports:
         - "5432:5432"
       volumes:
         - postgres_data:/var/lib/postgresql/data

   volumes:
     postgres_data:
   ```

2. **SQLModel モデル定義** ⭐

   ```python
   # backend/models.py を新規作成
   from sqlmodel import Field, Relationship, SQLModel
   from datetime import datetime
   from typing import Optional
   import uuid

   class Conversation(SQLModel, table=True):
       __tablename__ = "conversations"

       id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
       created_at: datetime = Field(default_factory=datetime.utcnow)

       # Relationship
       messages: list["Message"] = Relationship(back_populates="conversation")

   class Message(SQLModel, table=True):
       __tablename__ = "messages"

       id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
       conversation_id: str = Field(foreign_key="conversations.id")
       role: str
       content: str
       created_at: datetime = Field(default_factory=datetime.utcnow)

       # Relationship
       conversation: Optional[Conversation] = Relationship(back_populates="messages")
   ```

3. **リポジトリパターンでCRUD実装** ⭐

   ```python
   # backend/repositories/conversation_repository.py を新規作成
   from sqlmodel import Session, select
   from models import Conversation, Message

   class ConversationRepository:
       def __init__(self, session: Session):
           self.session = session

       def create_conversation(self) -> Conversation:
           conversation = Conversation()
           self.session.add(conversation)
           self.session.commit()
           self.session.refresh(conversation)
           return conversation

       def add_message(self, conv_id: str, role: str, content: str) -> Message:
           message = Message(conversation_id=conv_id, role=role, content=content)
           self.session.add(message)
           self.session.commit()
           return message

       def get_conversation_history(self, conv_id: str) -> list[Message]:
           statement = select(Message).where(Message.conversation_id == conv_id)
           return self.session.exec(statement).all()
   ```

#### 📚 参考リソース

- [SQLModel 公式ドキュメント](https://sqlmodel.tiangolo.com/) ⭐
- [FastAPI + SQLModel チュートリアル](https://sqlmodel.tiangolo.com/tutorial/fastapi/)
- [Docker Compose で PostgreSQL](https://hub.docker.com/_/postgres)
- [Alembic チュートリアル](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

---

### Day 7: RAG実装深化 (1)

#### 💡 なぜこれを学ぶのか

| 学習内容        | なぜ必要か                                   | できるようになること             |
| :-------------- | :------------------------------------------- | :------------------------------- |
| Query Rewriting | 「それ」「これ」を解決しないと検索精度が低下 | 文脈を考慮した正確な検索ができる |
| プロンプト設計  | LLMの出力品質はプロンプト次第                | 安定した高品質な出力を得られる   |
| 会話履歴活用    | 継続的な対話には必須                         | マルチターンの会話ができる       |

**目標**: クエリ書き換えの精度を向上させ、より正確な検索を実現する。

#### ⏰ 時間配分

| 時間             | 内容                            |
| :--------------- | :------------------------------ |
| 9:00-11:00 (2h)  | Query Rewriting パターンの学習  |
| 11:00-13:00 (2h) | プロンプトエンジニアリング      |
| 14:00-16:00 (2h) | 会話履歴を活用した文脈理解      |
| 16:00-18:00 (2h) | 🛠️ 実践課題: プロジェクトに適用 |

#### 📖 学習内容

**Query Rewriting パターン**

- Stand-alone Question（自立質問への変換）
- Multi-Query（複数クエリ生成）
- Step-back Prompting（抽象化質問）

**プロンプトエンジニアリング**

- システムプロンプトの設計
- Few-shot examples の効果
- 出力フォーマットの指定

**文脈理解**

- 会話履歴のサマリー生成
- 関連する過去発話の抽出
- コンテキストウィンドウの管理

#### 🛠️ 実践課題: rag-practiceに適用

1. **Query Rewriting の改善**

   ```python
   # 改善版のプロンプト
   REWRITE_PROMPT = """
   あなたは質問を検索用クエリに変換する専門家です。

   ## タスク
   会話履歴を参照し、最新の質問を「誰が読んでも意味がわかる検索クエリ」に書き換えてください。

   ## ルール
   - 代名詞（それ、これ、あれ）は具体的な名詞に置き換える
   - 会話の文脈から推測される意図を明確にする
   - 検索に適したキーワードを含める
   - 日本語で出力する

   ## 出力形式
   検索クエリのみを1行で出力してください。余計な説明は不要です。

   ## 会話履歴
   {history}

   ## 最新の質問
   {question}
   """
   ```

2. **A/Bテストの仕組み**
   - 旧プロンプト vs 新プロンプトの比較
   - 結果をログに記録

#### 📚 参考リソース

- [LangChain: Conversational RAG](https://python.langchain.com/docs/tutorials/qa_chat_history/)
- [OpenAI Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering)

---

### Day 8: RAG実装深化 (2)

#### 💡 なぜこれを学ぶのか

| 学習内容     | なぜ必要か                   | できるようになること             |
| :----------- | :--------------------------- | :------------------------------- |
| スコアリング | 低品質な検索結果を除外できる | 信頼性の高い情報のみ使える       |
| リランキング | 検索結果の順序を最適化       | 最も関連性の高い情報を優先できる |
| 引用元提示   | 回答の根拠を示すのは必須     | ユーザーが情報を検証できる       |

**目標**: 検索精度を向上させ、信頼性の高い回答を生成する。

#### ⏰ 時間配分

| 時間             | 内容                             |
| :--------------- | :------------------------------- |
| 9:00-11:00 (2h)  | 検索結果のスコアリングと閾値設定 |
| 11:00-13:00 (2h) | リランキングの実装               |
| 14:00-16:00 (2h) | 引用元の正確な提示               |
| 16:00-18:00 (2h) | 🛠️ 実践課題: プロジェクトに適用  |

#### 📖 学習内容

**スコアリングと閾値**

- 検索スコアの意味と解釈
- 低スコア結果の除外
- 結果が見つからない場合のハンドリング

**リランキング**

- Cross-encoder によるリランキング
- Azure Semantic Ranker の活用
- 計算コストと精度のトレードオフ

**引用元提示**

- ソースドキュメントの特定
- ページ番号、セクションの抽出
- 回答文と引用元の紐付け

#### 🛠️ 実践課題: rag-practiceに適用

1. **スコア閾値の実装**

   ```python
   MIN_SCORE_THRESHOLD = 0.7

   def filter_results(results: list[dict]) -> list[dict]:
       return [r for r in results if r.get("@search.score", 0) >= MIN_SCORE_THRESHOLD]
   ```

2. **引用元フォーマットの改善**

   ```python
   def format_sources(results: list[dict]) -> str:
       sources = []
       for i, r in enumerate(results, 1):
           source = f"[{i}] {r['source']} (P.{r['page']})"
           sources.append(source)
       return "\n".join(sources)
   ```

3. **回答なしケースの処理**
   ```python
   if not filtered_results:
       return {
           "message": "申し訳ありませんが、ご質問に関連する情報が見つかりませんでした。",
           "sources": []
       }
   ```

---

### Day 9: Architecture & Production Readiness

#### 💡 なぜこれを学ぶのか

| 学習内容                          | なぜ必要か                           | できるようになること             |
| :-------------------------------- | :----------------------------------- | :------------------------------- |
| **レイヤー分離** ⭐               | main.pyの肥大化を防ぎ保守性向上      | 移植性・テスト可能性が向上する   |
| **クリーンアーキテクチャ基礎** ⭐ | 実務プロジェクトで広く采用           | 保守しやすい設計ができる         |
| Docker                            | 環境を統一してデプロイするモダン標準 | どの環境でも同じ動作を保証できる |
| 設定管理                          | 機密情報の安全な管理は必須           | APIキーを安全に扱える            |

**目標**: レイヤー分離で保守性を向上させ、Docker化してデプロイ可能にする。

#### ⏰ 時間配分

| 時間             | 内容                                                             |
| :--------------- | :--------------------------------------------------------------- |
| 9:00-12:00 (3h)  | 🏗️ レイヤー分離リファクタリング（routers/services/repositories） |
| 12:00-14:00 (2h) | Docker化 + 環境変数管理                                          |
| 14:00-16:00 (2h) | セキュリティ強化                                                 |
| 16:00-18:00 (2h) | 🛠️ 結合テスト + デプロイ確認                                     |

#### 📖 学習内容

**レイヤー分離リファクタリング** ⭐

- **3層アーキテクチャの実装**
  - `routers/`: プレゼンテーション層（HTTPリクエストの処理）
  - `services/`: ビジネスロジック層（Query Rewriting, RAGパイプライン）
  - `repositories/`: データアクセス層（DB, Azure AI Search）
- **依存性の逆転（DIP）**
  - インターフェースを用いた結合度の低減
  - テスト時のモック差し替え
- **main.pyの簡素化**
  - エンドポイントはroutersに移動
  - ビジネスロジックはservicesへ

**Docker化**

- Dockerfile の作成（マルチステージビルド）
- docker-compose による開発環境
- ヘルスチェックの設定

**設定管理**

- pydantic-settings による型安全な設定
- 環境ごとの設定切り替え

**セキュリティ**

- 入力のサニタイズ
- CORS設定の本番向け調整

#### 🛠️ 実践課題: rag-practiceに適用

1. **3層アーキテクチャへのリファクタリング**

   ```python
   # backend/routers/chat.py
   from fastapi import APIRouter, Depends
   from services.chat_service import ChatService
   from schemas import ChatRequest, ChatResponse

   router = APIRouter(prefix="/api/v1", tags=["chat"])

   @router.post("/chat", response_model=ChatResponse)
   async def chat(
       request: ChatRequest,
       chat_service: ChatService = Depends()
   ):
       return await chat_service.process_chat(request)
   ```

   ```python
   # backend/services/chat_service.py
   class ChatService:
       def __init__(
           self,
           search_repo: SearchRepository,
           conversation_repo: ConversationRepository,
           query_rewriter: QueryRewriter
       ):
           self.search_repo = search_repo
           self.conversation_repo = conversation_repo
           self.query_rewriter = query_rewriter

       async def process_chat(self, request: ChatRequest):
           # ビジネスロジックを集約
           rewritten_query = await self.query_rewriter.rewrite(request)
           search_results = await self.search_repo.hybrid_search(rewritten_query)
           response = await self._generate_response(search_results)
           await self.conversation_repo.save_message(request, response)
           return response
   ```

   ```python
   # backend/repositories/search_repository.py
   class SearchRepository:
       def __init__(self, search_client: SearchClient):
           self.client = search_client

       async def hybrid_search(self, query: str) -> list[dict]:
           # Azure AI Search へのアクセスを抽象化
           ...
   ```

2. **Dockerfile 作成**

   ```dockerfile
   # backend/Dockerfile
   FROM python:3.11-slim as builder
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   FROM python:3.11-slim
   WORKDIR /app
   COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
   COPY . .
   EXPOSE 8000
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

3. **設定クラス**

   ```python
   # backend/config.py
   from pydantic_settings import BaseSettings

   class Settings(BaseSettings):
       openai_api_key: str
       azure_search_endpoint: str
       azure_search_api_key: str
       azure_search_index_name: str
       log_level: str = "INFO"

       class Config:
           env_file = ".env"

   settings = Settings()
   ```

4. **結合テストの実行**
   - 全エンドポイントの動作確認
   - エラーケースのテスト
   - レイヤー分離後の動作確認

---

### 休日: バッファ

この日は以下の用途に使用:

- 遅れている項目のキャッチアップ
- 理解が浅い領域の復習
- 作成したコードの総点検
- ドキュメント整理

---

### 🌟 Extra: Week 2 週末

#### 推奨タスク

1. **完璧なクリーンアーキテクチャ** ⭐

   Day 9で実装した3層アーキテクチャをさらに発展させます。

   **Use Case層の追加**

   ```python
   # backend/use_cases/chat_use_case.py
   from entities.conversation import ConversationEntity

   class ChatUseCase:
       """
       ビジネスルールを含むユースケース層
       サービス層とは異なり、エンティティを中心に設計
       """
       def __init__(self, search_repo, conversation_repo):
           self.search_repo = search_repo
           self.conversation_repo = conversation_repo

       async def execute(self, user_query: str, conversation_id: str) -> ConversationEntity:
           # エンティティでビジネスルールを表現
           conversation = await self.conversation_repo.find_by_id(conversation_id)
           conversation.add_user_message(user_query)

           search_results = await self.search_repo.search(user_query)
           response = conversation.generate_response(search_results)

           await self.conversation_repo.save(conversation)
           return conversation
   ```

   **Entity層の追加**

   ```python
   # backend/entities/conversation.py
   from dataclasses import dataclass

   @dataclass
   class ConversationEntity:
       """
       ビジネスロジックを持つエンティティ
       DBモデルとは独立した純粋なドメインオブジェクト
       """
       id: str
       messages: list[Message]

       def add_user_message(self, content: str):
           # ビジネスルール: メッセージの追加制約
           if len(self.messages) > 100:
               raise ValueError("会話が長すぎます")
           self.messages.append(Message(role="user", content=content))

       def generate_response(self, search_results: list) -> str:
           # ビジネスルール: 回答生成ロジック
           ...
   ```

   **参考リソース**:
   - [Clean Architecture (書籍)](https://www.amazon.co.jp/dp/B07FSBHS2V)
   - [Python Clean Architecture Example](https://github.com/Enforcer/clean-architecture)

2. **CI/CD パイプライン**
   - GitHub Actions による自動テスト
   - Azure へのデプロイフロー確認

3. **高度なプロンプト技術**
   - Chain-of-Thought プロンプティング
   - Function Calling (Tools) の実装

4. **最終確認**
   - 全機能の動作確認
   - 実践で想定される質問への回答準備

---

## ✅ 最終チェックリスト

- [ ] Python型ヒントを完璧に理解し、実装できる
- [ ] FastAPIの依存性注入パターンを実装できる
- [ ] Azure AI Searchでハイブリッド検索を実装できる
- [ ] SQLAlchemyで基本的なCRUD操作ができる
- [ ] Dockerでアプリをコンテナ化できる
- [ ] pytestで基本的なテストを作成できる
- [ ] エラーハンドリングとロギングが適切に実装されている
- [ ] 環境変数を安全に管理できる
- [ ] Query Rewriting の仕組みを説明できる
- [ ] 検索精度向上のための手法を3つ以上挙げられる

---

## 📈 進捗記録

| Day           | 完了項目 | 学習時間 | メモ |
| :------------ | :------- | :------- | :--- |
| Day 1         |          |          |      |
| Day 2         |          |          |      |
| Day 3         |          |          |      |
| Day 4         |          |          |      |
| Day 5         |          |          |      |
| 休日 (Week 1) |          |          |      |
| Day 6         |          |          |      |
| Day 7         |          |          |      |
| Day 8         |          |          |      |
| Day 9         |          |          |      |
| 休日 (Week 2) |          |          |      |
