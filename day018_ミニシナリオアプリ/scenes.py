# scenes.py

scenes = {
    "intro": {
        "text": "あなたは森の中にいます。どうしますか？",
        "image": "forest.png",
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

    "look":{
        "text": "水面には自分の顔が映っている。特に変わったところはなさそうだ。",
        "choices": [
            {"label": "帰るとしよう", "next": "end"}
        ]
    },

    "throw":{
        "text": "小石を投げ入れると、水面が波打った。それ以外に変わったところはなさそうだ。",
        "choices": [
            {"label": "帰るとしよう", "next": "end"}
        ]
    },

    "left":{
        "text": "見慣れた町並みが見えてきた。",
        "choices": [
            {"label": "まっすぐ帰って休むとしよう", "next": "end"}
        ]
    },

    "right":{
        "text": "ゴールドジムが見えてきた。",
        "choices": [
            {"label": "一汗かいていくとしよう。よりマッチョの高みを目指して──", "next": "end"}
        ]
    },

    "end":{
        "text": "物語はここで幕を閉じる。ESCを押して終了してください。",
        "choices": []
    },
}