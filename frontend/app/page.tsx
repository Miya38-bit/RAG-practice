'use client';

import { Conversation, Message } from '@/types';
import { useEffect, useRef, useState } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import MessageDisplay from './components/MessageDisplay';
import SendMessage from './components/SendMesage';

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
  // 会話IDのステート
  const [conversationId, setConversationId] = useState<string | null>(null);
  // サイドバー開閉のステート
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  // 会話一覧のステート
  const [conversations, setConversations] = useState<Conversation[]>([]);

  const bottomRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex h-screen bg-stone-800 text-stone-200 overflow-hidden">
      {/* サイドバー */}
      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        conversationId={conversationId}
        setConversationId={setConversationId}
        conversations={conversations}
        setConversations={setConversations}
        setMessages={setMessages}
      />

      {/* メインコンテンツエリア */}
      <div className="flex flex-col flex-1 relative">
        {/* ヘッダー */}
        <Header onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />

        {/* メッセージ表示エリア */}
        <div className="flex-1 overflow-y-auto">
          <MessageDisplay
            messages={messages}
            loading={loading}
            bottomRef={bottomRef}
          />
        </div>

        {/* メッセージ送信エリア */}
        <SendMessage
          input={input}
          setInput={setInput}
          messages={messages}
          setMessages={setMessages}
          loading={loading}
          setLoading={setLoading}
          conversationId={conversationId}
          setConversations={setConversations}
        />
      </div>

      {/* モバイル用オーバーレイ（サイドバーが開いている時に背景を暗くする） */}
      {isSidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 lg:hidden z-10"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}
    </div>
  );
}
