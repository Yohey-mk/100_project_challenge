# scenes.py

scenes = {
    "intro": {
        "text": "あなたは森の中にいます。どうしますか？",
        "choices": [
            {"label": "進む", "next": "forward"},
            {"label": "引き返す", "next": "back"}
        ]
    },
    "forward":{
        "text": "森の奥へ進むと、湖が現れた。",
        "choices": [
            {"label": "湖を覗く", "next": "look"},
            {"label": "近くにあった小石を湖に投げ入れる", "next": "throw"}
        ]
    },

    "back":{
        "text": "怪しい気配を感じたので立ち去ることにした。来た道は確か……",
        "choices": [
            {"label": "右側の道", "next": "right"},
            {"label": "左側の道", "next": "left"}
        ]
    },
}