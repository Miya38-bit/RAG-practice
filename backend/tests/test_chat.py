from dataclasses import dataclass
from unittest.mock import MagicMock
import pytest


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


def test_chat_search_error(client, mock_openai_client, mock_search_client):
    # 検索機能が「原因不明のエラー」で失敗するように設定
    mock_search_client.search.side_effect = Exception(
        "検索データベースに接続できません"
    )

    # OpenAIのモック設定 (クエリ書き換えまでは成功させる必要があるため)
    # stream=False の場合だけ返せばOK（そこまでしか進まないので）
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "書き換えられたクエリ"
    mock_openai_client.chat.completions.create.return_value = mock_response

    # テスト実行
    response = client.post(
        "/api/v1/chat", json={"messages": [{"role": "user", "content": "失敗するはず"}]}
    )

    # 検証
    # Exception は utils.py で catch され、SearchError に変換されて再送出されます。
    # そのため、rag_exception_handler が動き、503エラーになります。
    # 検証
    # Exception は utils.py で catch され、SearchError に変換されて再送出されます。
    # そのため、rag_exception_handler が動き、503エラーになります。
    assert response.status_code == 503
    assert "SearchError" in response.text


def test_chat_openai_error(client, mock_openai_client, mock_search_client):
    # 1. 検索機能は成功させる
    mock_search_client.search.return_value = []

    # 2. OpenAIの設定 (1回目は成功、2回目は失敗)
    mock_openai_client.chat.completions.create.side_effect = [
        # 1回目 (書き換え): 成功
        MockResponse(choices=[MockChoice(message=MockContent("rewrite"))]),
        # 2回目 (生成): 失敗
        Exception("ストリーミング中のエラー"),
    ]

    # 3. テスト実行と検証
    # 「RuntimeError が起きるはずだ」ということをテストします
    with pytest.raises(RuntimeError):
        client.post(
            "/api/v1/chat", json={"messages": [{"role": "user", "content": "こんにちは"}]}
        )
