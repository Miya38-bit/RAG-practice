'use client';

import { useEffect, useRef, useState } from 'react';

type Message = {
  role: 'user' | 'assistant';
  content: string;
};

/**
 * コンテナーコンポーネント
 * @param children 子要素
 * @param className クラス名
 */
function Container({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return <div className={`max-w-7xl mx-auto ${className}`}>{children}</div>;
}

/**
 * バックエンドにリクエストを送信して応答を取得
 * @param url バックエンドのURL
 * @param message ユーザーの入力
 * @returns バックエンドからの応答
 */
async function fetchChat(url: string, messages: Message[]) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ messages }),
    });
    const reader = response.body?.getReader();

    return reader;
  } catch (error) {
    console.error('Error fetching chat:', error);
    return null;
  }
}

/**
 * メインコンポーネント
 */
export default function Home() {
  // 入力欄のステート
  const [input, setInput] = useState('');
  // メッセージのステート
  const [messages, setMessages] = useState<Message[]>([]);
  // 読み込み中のステート
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <main className="min-h-screen bg-stone-800 text-stone-200">
      <header className="sticky top-0 p-5 bg-stone-900/80 backdrop-blur-md border-b border-orange-800/50 shadow-lg shadow-orange-500/50">
        <Container>
          <h1 className="text-2xl font-bold">Internal Rules Chatbot</h1>
        </Container>
      </header>
      <section className="p-5 flex flex-col gap-4 max-w-4xl mx-auto pb-24">
        {messages.map((message, index) => {
          const isUser = message.role === 'user';
          // メッセージの表示位置を決める
          return (
            <div
              key={index}
              className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`p-4 max-w-[80%] shadow-md rounded-2xl
          ${
            isUser
              ? 'bg-orange-700 text-orange-50 rounded-br-none'
              : 'bg-stone-700 text-stone-100 rounded-bl-none'
          }`}
              >
                {message.content}
              </div>
            </div>
          );
        })}
        {loading && (
          <div className="flex justify-start">
            <div className="text-stone-100/90 text-sm">返答中...</div>
          </div>
        )}
        <div ref={bottomRef} />
      </section>
      <div className="fixed bottom-0 w-full bg-stone-900/90 backdrop-blur-md border-t border-stone-800 p-4">
        <Container>
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
              const reader = await fetchChat(
                'http://127.0.0.1:8000/chat',
                newHistoryMessages.slice(-10)
              );

              console.log(reader);
              if (!reader) {
                setLoading(false);
                return;
              }

              // AIの回答用の空メッセージをstateに追加
              let aiMessage = '';
              setMessages((prev) => [
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
                  aiMessage += text;
                  // stateを更新
                  setMessages((prev) => {
                    const newMessages = [...prev];
                    newMessages[newMessages.length - 1].content = aiMessage;
                    return newMessages;
                  });
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
        </Container>
      </div>
    </main>
  );
}
