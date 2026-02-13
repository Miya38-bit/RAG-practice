import { ChatRequest, Conversation } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

// 会話作成
export async function createConversation(): Promise<Conversation> {
  const response = await fetch(`${API_BASE_URL}/conversations`, {
    method: 'POST',
  });
  if (!response.ok) throw new Error('Failed to create conversation');
  
  const data = await response.json();
  return data;
}

// 会話一覧取得
export async function fetchConversations(): Promise<Conversation[]> {
  const response = await fetch(`${API_BASE_URL}/conversations`);
  if (!response.ok) throw new Error('Failed to fetch conversations');

  const data = await response.json();
  return data;
}

// 会話削除
export async function deleteConversation(
  conversationId: string
): Promise<Response> {
  const response = await fetch(
    `${API_BASE_URL}/conversations/${conversationId}`,
    {
      method: 'DELETE',
    }
  );
  if (!response.ok) throw new Error('Failed to delete conversation');

  return response;
}

// 会話に紐づくメッセージ履歴取得
export async function fetchMessages(conversationId: string) {
  const response = await fetch(
    `${API_BASE_URL}/conversations/${conversationId}/messages`
  );
  if (!response.ok) throw new Error('Failed to fetch messages');

  const data = await response.json();
  return data;
}

// チャットリクエスト送信
export async function fetchChat(chatRequest: ChatRequest) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(chatRequest),
  });
  if (!response.ok) throw new Error('Failed to fetch chat');

  const render = response.body?.getReader();
  return render;
}
