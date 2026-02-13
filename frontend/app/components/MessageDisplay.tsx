import { Message } from '@/types';

type MessagedisplayProps = {
  messages: Message[];
  loading: boolean;
  bottomRef: React.RefObject<HTMLDivElement | null>;
};

export default function MessageDisplay({ messages, loading, bottomRef }: MessagedisplayProps) {
  return (
    <section className="p-5 flex flex-col gap-4 max-w-4xl mx-auto pb-4">
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
  );
}
