export type Conversation = {
  id: string;
  title: string;
  created_at: string;
};

export type Message = {
  role: 'user' | 'assistant';
  content: string;
};

export type ChatRequest = {
  conversation_id: string | null;
  messages: Message[];
};