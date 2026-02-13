from sqlmodel import Session, select, desc, asc
from models import Conversation, Message, Role

"""会話リポジトリモジュール

会話とメッセージのCRUD操作を提供するリポジトリクラス。
"""
class ConversationRepository:
    def __init__(self, session: Session):
        self.session = session

    # 会話作成
    def create_conversation(self) -> Conversation:
        # 新規会話を作成
        conversation = Conversation()
        # 新規会話を追加
        self.session.add(conversation)
        # 新規会話をDBに反映
        self.session.commit()
        # DBから新規会話情報を取得
        self.session.refresh(conversation)
        return conversation

    # 会話1件取得
    def get_conversation(self, conversation_id: str) -> Conversation | None:
        # 会話をIDで1件取得。存在しない場合はNoneを返す
        conversation = self.session.get(Conversation, conversation_id)
        return conversation

    # 全会話取得
    def get_all_conversations(self) -> list[Conversation]:
        # 全会話を取得（作成日時降順）
        results = self.session.exec(
            select(Conversation).order_by(desc(Conversation.created_at))
        ).all()
        return list(results)

    # 会話削除
    def delete_conversation(self, conversation_id: str) -> bool:
        # 会話をIDで1件取得
        conversation = self.get_conversation(conversation_id)
        # 会話が存在すれば削除
        if conversation:
            self.session.delete(conversation)
            self.session.commit()
            return True
        return False
    
    # 会話タイトル更新
    def update_conversation_title(self, conversation_id: str, title: str) -> Conversation | None:
        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.title = title
            self.session.add(conversation)
            self.session.commit()
            self.session.refresh(conversation)
            return conversation
        return None

    # 会話にメッセージ追加
    def add_message(self, conversation_id: str, role: Role, content: str) -> Message:
        # メッセージ作成
        message = Message(conversation_id=conversation_id, role=role, content=content)
        # メッセージをセッションに追加
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message
    
    # 会話のメッセージ一覧取得
    def get_messages(self, conversation_id: str) -> list[Message]:
        results = self.session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(asc(Message.created_at))
        ).all()
        return list(results)
