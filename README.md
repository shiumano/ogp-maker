# ogp-maker
JsonリクエストからOGPを動的に生成するAPI

# 動かし方
```
pip install -r requirements.txt  # fastapi[all] だけだけど一応ね
python make-ogp-server.py
```

# 使い方
## OGPの作成
OGPの仕様を頼りにJsonデータを作ってPOSTします
↓こんな感じ
```
curl -X POST -H "Content-Type: application/json" -d '{
  "og": {
    "url": "https://google.co.jp/",
    "title": "Google検索",
    "image": {
      "url": "https://www.google.co.jp/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
      "width": 272,
      "height": 92
    },
    "description": "ウェブページに関する説明",
    "type": "website",
    "site_name": "Google"
  }
}' http://localhost:8080/generate_ogp
```
うまくいけば、生成されたHTMLのリンクが出てきます
```
{"link":"/ogp/09b0aba3-4373-4f61-83a9-77d6f1b03dbd"}
```

## アクセス
出てきたリンクにアクセスします
```
curl http://localhost:8080/ogp/09b0aba3-4373-4f61-83a9-77d6f1b03dbd
```
生成されたHTMLが出てきます
```
    <!DOCTYPE html>
    <html>
    <head>
        <meta property="og:url" content="https://google.co.jp/">
<meta property="og:title" content="Google検索">
<meta property="og:image:url" content="https://www.google.co.jp/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png">
<meta property="og:image:width" content="272">
<meta property="og:image:height" content="92">
<meta property="og:description" content="ウェブページに関する説明">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Google">
    </head>
    <body>
    </body>
    </html>

```
Discordでの表示

![image](https://github.com/user-attachments/assets/94d4d89f-9447-4447-9c7c-eadc85cb6452)

# ・・・・・・・・
このコードはGeminiに書いてもらいました

↓チャットログ

https://g.co/gemini/share/88c723750ca5
