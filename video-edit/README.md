# トレーニング動画 編集ツール

デザイン案A（ミニマル）で、左上のトレーニング名とフルテロップを動画に焼き込みます。

## ファイル

- `projects/*.json` — 動画ごとの設定。`titles`（左上のトレーニング名。途中で切り替え可、`\n` で改行、`size` で文字サイズ）と `telops`（文言・表示時間（秒））。`[ ]` で囲んだ語はライム色で強調
- `overlay.html` — タイトル／テロップのデザイン（1920x1080）
- `make_overlays.mjs` — 設定から透過PNGを書き出す
- `render.py` — 色補正・ビネット・音量調整をして、PNGを動画に合成する

## 手順

```sh
npm install
pip install imageio-ffmpeg faster-whisper   # ffmpeg と文字起こし

node make_overlays.mjs projects/02_dragon_flag.json OUT/overlays
python3 render.py projects/02_dragon_flag.json SRC.MOV OUT/overlays OUT/edit.mp4
# 1コマだけ確認: python3 render.py projects/02_dragon_flag.json SRC.MOV OUT/overlays still.png --still 秒
```

文言や表示時間を直すときは `projects/*.json` を編集して、上の2コマンドをやり直すだけです。
