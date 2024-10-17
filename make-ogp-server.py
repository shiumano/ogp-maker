from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

import uvicorn

import sqlite3
import uuid
import json


app = FastAPI()

# SQLite接続設定
conn = sqlite3.connect('ogp.db')
cursor = conn.cursor()

# テーブル作成 (初回のみ実行)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ogp_data (
        id TEXT PRIMARY KEY,
        html TEXT
    )
''')
conn.commit()

def generate_html(data):
    """
    JSONデータからHTMLを生成する関数

    Args:
        data (dict): JSONデータ

    Returns:
        str: 生成されたHTMLの文字列
    """

    og_data = data['og']
    meta_tags_list = []
    for key, value in og_data.items():
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                meta_tags_list.append(f'<meta property="og:{key}:{subkey}" content="{subvalue}">')
        else:
            meta_tags_list.append(f'<meta property="og:{key}" content="{value}">')
    meta_tags_str = '\n'.join(meta_tags_list)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        {meta_tags_str}
    </head>
    <body>
    </body>
    </html>
    """

    return html

@app.post("/generate_ogp")
async def generate_ogp(request: Request):
    data = await request.json()
    html = generate_html(data)

    # UUIDを生成してIDとする
    ogp_id = str(uuid.uuid4())

    # SQLiteに保存
    cursor.execute("INSERT INTO ogp_data VALUES (?, ?)", (ogp_id, html))
    conn.commit()

    # 生成したHTMLへのリンクを返す
    return JSONResponse({"link": f"/ogp/{ogp_id}"})

@app.get("/ogp/{ogp_id}")
async def get_ogp(ogp_id: str):
    cursor.execute("SELECT html FROM ogp_data WHERE id=?", (ogp_id,))
    result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="OGP not found")
    
    return HTMLResponse(result[0])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")