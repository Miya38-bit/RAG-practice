import { Conversation, Message } from '@/types';
import { fetchChat } from '@/lib/api';
import { Dispatch, SetStateAction } from 'react';

type MessageProps = {
  input: string;
  setInput: (input: string) => void;
  messages: Message[];
  setMessages: Dispatch<SetStateAction<Message[]>>;
  loading: boolean;
  setLoading: (loading: boolean) => void;
  conversationId: string | null;
  setConversations: Dispatch<SetStateAction<Conversation[]>>;
};

export default function SendMessage({
  input,
  setInput,
  messages,
  setMessages,
  loading,
  setLoading,
  conversationId,
  setConversations,
}: MessageProps) {
  return (
    <div className="sticky bottom-0 bg-stone-900/95 backdrop-blur-md border-t border-stone-700 p-4">
      <form
        className="flex gap-3 max-w-4xl mx-auto"
        onSubmit={async (e) => {
          e.preventDefault();
          if (!input) return;

          // 過去の会話とユーザーメッセージを新規配列に追加
          const newHistoryMessages: Message[] = [
            ...messages,
            { role: 'user', content: input },
          ];

          // ユーザーの入力を含めた会話履歴でstateを更新
          setMessages(newHistoryMessages);
          // 入力欄を空にする
          setInput('');

          // バックエンドにリクエストを送信
          setLoading(true);

          const reader = await fetchChat({
            conversation_id: conversationId,
            messages: newHistoryMessages.slice(-100),
          });

          if (!reader) {
            setLoading(false);
            return;
          }

          // AIの回答用の空メッセージをstateに追加
          let aiMessage = '';
          setMessages((prev: Message[]) => [
            ...prev,
            { role: 'assistant', content: '' },
          ]);

          // AIの回答をstateに追加
          const decoder = new TextDecoder();
          try {
            while (true) {
              const { done, value } = await reader.read();
              if (done) break;

              // バイナリからテキスト変換
              const text = decoder.decode(value, { stream: true });
              const lines = text
                .split('\n\n')
                .filter((line) => line.trim() !== '');

              for (const line of lines) {
                if (line.startsWith('data: ')) {
                  const eventData = JSON.parse(line.slice(6));
                  if (eventData.type === 'message') {
                    aiMessage += eventData.content;
                    // 部分的に受信したAIメッセージでstateを更新
                    setMessages((prev: Message[]) => {
                      const newMessages = [...prev];
                      newMessages[newMessages.length - 1].content = aiMessage;
                      return newMessages;
                    });
                  } else if (eventData.type === 'title') {
                    setConversations((prev: Conversation[]) => {
                      const newConversations = [...prev].map((conv) => {
                        if (conv.id === conversationId) {
                          return { ...conv, title: eventData.title };
                        }
                        return conv;
                      });
                      return newConversations;
                    });
                  }
                }
              }
            }
          } catch (e) {
            console.error(e);
          } finally {
            setLoading(false);
          }
        }}
      >
        <input
          type="text"
          className="flex-1 p-3 rounded-full bg-stone-800 text-stone-100 border border-stone-700 focus:shadow-[0_0_12px_rgba(249,115,22,0.5)] outline-none transition-all placeholder-stone-500 duration-300"
          placeholder="質問を入力してください..."
          onChange={(e) => setInput(e.target.value)}
          value={input}
        />
        <button
          type="submit"
          className="py-3 px-6 bg-linear-to-r from-orange-700 to-amber-700 hover:from-orange-600 hover:to-amber-600 text-white font-medium rounded-full shadow-lg transition-all duration-300 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={loading || !input}
        >
          送信
        </button>
      </form>
    </div>
  );
}
