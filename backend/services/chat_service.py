from repositories.search_repository import SearchRepository
from repositories.conversation_repository import ConversationRepository
from openai import AsyncOpenAI
from exceptions import EmbeddingError, LLMError
from models import ChatRequest, MessageBase, Role
from typing import AsyncGenerator
import json
import config


class ChatService:
    def __init__(
        self,
        openai_client: AsyncOpenAI,
        search_repository: SearchRepository,
        conversation_repository: ConversationRepository,
    ):
        self.openai_client = openai_client
        self.search_repository = search_repository
        self.conversation_repository = conversation_repository

    # チャット処理
    async def process_chat(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        # 会話IDがなければ新規会話作成
        if request.conversation_id is None:
            conversation = self.conversation_repository.create_conversation()
            conversation_id = conversation.id
        else:
            conversation_id = request.conversation_id

        # ユーザーメッセージをDBに保存
        self.conversation_repository.add_message(
            conversation_id, "user", request.messages[-1].content
        )

        # Query Rewriting
        rewrited_query = await self._rewrite_query(request.messages)

        # ベクトル生成
        vector_query_for_reference = await self._generate_embedding(rewrited_query)

        # 参考情報のベクトル検索
        search_results = await self.search_repository.hybrid_search(
            vector_query=vector_query_for_reference,
            top_k=2,
            text_query=rewrited_query,
            use_semantic_search=True,
            filter=None,
        )

        # 参考情報の組み立て
        reference_messages = self._build_reference(search_results)

        # ストリーミング応答の取得とクライアントへのSSE送信
        full_response = ""
        async for chunk in self._stream_response(
            messages=[reference_messages] + request.messages,
        ):
            full_response += chunk
            yield f"data: {json.dumps({'type': 'message', 'content': chunk})}\n\n"

        # 会話タイトル更新（最初のメッセージをタイトルに変換）
        if len(request.messages) == 1:
            title = await self._create_conversation_title(request.messages[0].content)
            self.conversation_repository.update_conversation_title(
                conversation_id, title
            )
            yield f"data: {json.dumps({'type': 'title', 'title': title})}\n\n"

        # アシスタントメッセージをDBに保存
        self.conversation_repository.add_message(
            conversation_id, "assistant", full_response
        )

    # 会話タイトル要約
    async def _create_conversation_title(self, message: str) -> str:
        try:
            response = await self.openai_client.chat.completions.create(
                model=config.LLM_MODEL,
                messages=[  # type: ignore
                    self._create_system_message(
                        "system",
                        "以下の文章を30文字以内で要約し、会話のタイトルとして適切な名前を付けてください。",
                    ),
                    self._create_system_message("user", message),
                ],
            )
            result = response.choices[0].message.content
            if result is None:
                raise LLMError("LLMからの応答が空です")
            return result
        except Exception as e:
            raise LLMError(f"LLM応答中にエラーが発生しました: {str(e)}")

    # テキストからEmbedding生成
    async def _generate_embedding(self, text: str) -> list[float]:
        try:
            response = await self.openai_client.embeddings.create(
                model=config.EMBEDDING_MODEL, input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise EmbeddingError(f"Embedding作成中にエラーが発生しました: {str(e)}")

    # 質問の意図を検索ワードに書き直す
    async def _rewrite_query(self, messages: list[MessageBase]) -> str:
        # システムメッセージ（指示）を追加
        system_message = self._create_system_message(
            "system",
            "これまでの会話履歴から質問の意図を誰が見ても意味がわかる検索ワードに書き直してください",
        )

        # 指示文とすべての会話履歴を結合
        all_messages = [system_message] + messages

        # 質問の意図を検索ワードに書き直してもらう
        try:
            response = await self.openai_client.chat.completions.create(
                model=config.LLM_MODEL,
                messages=all_messages,  # type: ignore
            )
            result = response.choices[0].message.content
            if result is None:
                raise LLMError("LLMからの応答が空です")
            return result
        except Exception as e:
            raise LLMError(f"LLM応答中にエラーが発生しました: {str(e)}")

    # 参考情報の組み立て
    def _build_reference(self, search_results: list[dict]) -> MessageBase:
        context = ""
        for result in search_results:
            context += f"【出典: {result['source']} (P.{result['page']}) / カテゴリ: {result['category']}】\n"
            context += f"{result['content']}\n\n"

        system_messages = self._create_system_message(
            "system",
            f"以下の情報を元に質問に答えてください。\n\n【参考情報】\n{context}",
        )
        return system_messages

    # ストリーミング応答取得
    async def _stream_response(
        self,
        messages: list[MessageBase],
    ) -> AsyncGenerator[str, None]:
        try:
            response = await self.openai_client.chat.completions.create(
                model=config.LLM_MODEL,
                messages=messages,  # type: ignore
                stream=True,
            )
            async for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            raise LLMError(f"LLM応答中にエラーが発生しました: {str(e)}")

    # ユーザーのメッセージを作成
    def _create_system_message(self, role: Role, content: str) -> MessageBase:
        return MessageBase(role=role, content=content)
