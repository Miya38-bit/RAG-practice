from dataclasses import dataclass

def test_chat_success(client, mock_openai_client, mock_search_client):
    # 1. 検索用モック: SearchClient.search の戻り値を設定
    mock_search_client.search.return_value = [
        {
            "source": "test.pdf",
            "page": 1,
            "category": "test",
            "content": "これはテスト用の検索結果です。",
        }
    ]

    @dataclass
    class MockContent:
        content: str

    @dataclass
    class MockChoice:
        delta: MockContent = None  # ストリーミング用
        message: MockContent = None  # 通常用

    @dataclass
    class MockResponse:
        choices: list[MockChoice]

    # 2. OpenAIモック: 呼び出し方(streamの有無)で振る舞いを変える
    async def mock_openai_side_effect(model, messages, stream=False, **kwargs):

        # パターンA: ストリーミング応答 (Webへの回答)
        if stream:

            async def stream_generator():
                # "これは" "テストです。" と少しずつ返す
                yield MockResponse(choices=[MockChoice(delta=MockContent("これは"))])
                yield MockResponse(
                    choices=[MockChoice(delta=MockContent("テストです。"))]
                )

            return stream_generator()

        # パターンB: 通常応答 (クエリ書き換え)
        else:
            return MockResponse(
                choices=[MockChoice(message=MockContent("書き換えられたクエリ"))]
            )

    mock_openai_client.chat.completions.create.side_effect = mock_openai_side_effect

    # 3. テスト実行
    response = client.post(
        "/api/v1/chat", json={"messages": [{"role": "user", "content": "こんにちは"}]}
    )

    # 4. 検証
    assert response.status_code == 200
    assert "これはテストです。" in response.text
