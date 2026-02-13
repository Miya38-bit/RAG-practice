import {
  createConversation,
  deleteConversation,
  fetchConversations,
  fetchMessages,
} from '@/lib/api';
import { Conversation, Message } from '@/types';
import { Dispatch, SetStateAction, useEffect, useState } from 'react';

type SidebarProps = {
  isOpen: boolean;
  onClose: () => void;
  conversationId: string | null;
  setConversationId: (id: string | null) => void;
  conversations: Conversation[];
  setConversations: Dispatch<SetStateAction<Conversation[]>>;
  setMessages: (messages: Message[]) => void;
};

export default function Sidebar({
  isOpen,
  onClose,
  conversationId,
  setConversationId,
  conversations,
  setConversations,
  setMessages,
}: SidebarProps) {

  const [loading, setLoading] = useState(true);

  // 会話一覧の初期読み込み
  useEffect(() => {
    fetchConversations()
      .then(setConversations)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [setConversations]);

  // 新規会話を作成
  const handleNewConversation = async () => {
    try {
      const newConv = await createConversation();
      setConversations([newConv, ...conversations]);
      setConversationId(newConv.id);
      setMessages([]);
      onClose(); // モバイルではサイドバーを閉じる
    } catch (error) {
      console.error('Failed to create conversation:', error);
    }
  };

  // 会話を選択
  const handleSelectConversation = async (id: string) => {
    setConversationId(id);
    try {
      const messages = await fetchMessages(id);
      setMessages(messages);
    } catch (error) {
      console.error('Failed to fetch messages for conversation:', error);
    }
    onClose(); // モバイルではサイドバーを閉じる
  };

  // 会話を削除
  const handleDeleteConversation = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation(); // 親のクリックイベントを発火させない
    if (!confirm('この会話を削除しますか？')) return;

    try {
      await deleteConversation(id);
      setConversations(conversations.filter((c) => c.id !== id));
      if (conversationId === id) {
        setConversationId(null);
        setMessages([]);
      }
    } catch (error) {
      console.error('Failed to delete conversation:', error);
    }
  };

  return (
    <>
      {/* サイドバー本体 */}
      <aside
        className={`
          fixed lg:static inset-y-0 left-0 z-20
          w-64 bg-stone-900 border-r border-stone-700
          transform transition-transform duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
          flex flex-col
        `}
      >
        {/* ヘッダー部分 */}
        <div className="p-4 border-b border-stone-700 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-orange-100">会話履歴</h2>
          {/* モバイル用の閉じるボタン */}
          <button
            type="button"
            onClick={onClose}
            className="lg:hidden p-1 hover:bg-stone-800 rounded"
            aria-label="サイドバーを閉じる"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* 新規会話ボタン */}
        <div className="p-3">
          <button
            type="button"
            onClick={handleNewConversation}
            className="w-full flex items-center gap-2 px-4 py-3 bg-orange-700 hover:bg-orange-600 text-white rounded-lg transition-colors shadow-md duration-300 active:scale-95 cursor-pointer"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4v16m8-8H4"
              />
            </svg>
            <span className="font-medium">新しい会話</span>
          </button>
        </div>

        {/* 会話一覧 */}
        <div className="flex-1 overflow-y-auto px-3 pb-3">
          {loading ? (
            <div className="text-center text-stone-400 py-8">読み込み中...</div>
          ) : conversations.length === 0 ? (
            <div className="text-center text-stone-500 py-8 text-sm">
              まだ会話がありません
            </div>
          ) : (
            <div className="space-y-2">
              {conversations.map((conv) => (
                <div
                  key={conv.id}
                  className={`
                    group relative rounded-lg transition-all
                    ${
                      conversationId === conv.id
                        ? 'bg-stone-700 shadow-md'
                        : 'hover:bg-stone-800'
                    }
                  `}
                >
                  <div className="flex items-start gap-2 px-3 py-3">
                    {/* 会話選択ボタン（クリック可能エリアを広く） */}
                    <button
                      type="button"
                      onClick={() => handleSelectConversation(conv.id)}
                      className="flex-1 text-left min-w-0 cursor-pointer"
                    >
                      <div className="flex-1 min-w-0">
                        {/* 会話のタイトル（最初のメッセージまたは日時） */}
                        <div className="text-sm font-medium text-stone-200 truncate">
                          {conv.title || '新しい会話'}
                        </div>
                        {/* 作成日時 */}
                        <div className="text-xs text-stone-400 mt-1">
                          {new Date(conv.created_at).toLocaleDateString(
                            'ja-JP',
                            {
                              month: 'short',
                              day: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit',
                            }
                          )}
                        </div>
                      </div>
                    </button>
                    {/* 削除ボタン（独立） */}
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeleteConversation(conv.id, e);
                      }}
                      className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-600/20 rounded transition-opacity shrink-0 cursor-pointer"
                      aria-label="削除"
                    >
                      <svg
                        className="w-4 h-4 text-red-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                        />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </aside>
    </>
  );
}
