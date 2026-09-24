# トレーニング動画 編集ツール（腕立て伏せ）

デザイン案A（ミニマル）で、左上のトレーニング名とフルテロップを動画に焼き込みます。

## ファイル

- `telops.json` — タイトルとテロップの文言・表示時間（秒）。`[ ]` で囲んだ語はライム色で強調
- `overlay.html` — タイトル／テロップのデザイン（1920x1080）
- `make_overlays.mjs` — `telops.json` から透過PNGを書き出す
- `render.py` — 色補正・ビネット・音量調整をして、PNGを動画に合成する

## 手順

```sh
npm install
pip install imageio-ffmpeg faster-whisper   # ffmpeg と文字起こし

node make_overlays.mjs OUT/overlays
python3 render.py SRC.MOV OUT/overlays OUT/edit.mp4
# 1コマだけ確認: python3 render.py SRC.MOV OUT/overlays still.png --still 秒 テロップ番号
```

文言や表示時間を直すときは `telops.json` を編集して、上の2コマンドをやり直すだけです。
