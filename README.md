# Stack-chan Color Simulator 🎨

M5Stack の **Stack-chan（SKU: K151, CoreS3版）** を 3D プリントで組むときの **配色を、ブラウザ上でパーツごとに試せる**シミュレーターです。フィラメント色のプリセット（約65色）や自由配色、作例スキーム、配色の共有URL・レシピ表示、PNG 書き出しなどに対応しています。

A browser-based **color simulator** for the 3D-printed **M5Stack Stack-chan (SKU: K151, CoreS3)** — try filament colors per part, in 3D, before you print.

## ▶ 使う / Use it

- **オンライン（おすすめ）**: 👉 https://kaburimen3.github.io/stackchan-color-simulator/
  クリックするだけ、インストール不要。スマホでも動きます。
- **オフライン**: 上のページを「名前を付けて保存」するか、[Releases](https://github.com/kaburimen3/stackchan-color-simulator/releases) の HTML を 1 つダウンロード → **ダブルクリックで起動**（ネット不要・全部 1 ファイルに同梱）。

操作: ドラッグ=回転 / ホイール=ズーム / パーツをクリックで選択 → 色を選ぶ。🔧調整モードで位置・大きさの微調整も可。

## ⚠️ 注意 / Disclaimer

> **これは個人が趣味で作った非公式ツールです。M5Stack 社・Stack-chan プロジェクトとは一切関係ありません。**
> 表示される色は、実際のフィラメント色・実機の見た目とは異なります（あくまで**配色イメージの参考用**です）。
> **現状有姿（AS-IS）で提供します。動作保証・サポート・不具合修正・今後の更新は行いません。自己責任でご利用ください。**
> Issue / Pull Request は基本的に確認しません（無効化している場合があります）。改造して使いたい方は自由に fork してください（MIT）。

> Unofficial, fan-made tool. Not affiliated with / endorsed by M5Stack or the Stack-chan project.
> Colors are approximate and will differ from real filament and the real device — **for reference only**.
> Provided **AS-IS, with no warranty, no support, and no bug fixes or future updates.** Use at your own risk.
> Issues/PRs are not monitored. Feel free to fork (MIT).

## 🔒 プライバシー / セキュリティ

完全な**クライアントサイドの静的ページ**です。サーバーへの送信・データ収集・トラッキング・外部 API 呼び出しはありません。オンライン版・オフライン版とも **three.js を同梱**しており、実行時に外部 CDN へ取りに行きません。

Fully client-side & static. No data is sent anywhere, no tracking, no external calls. three.js is bundled (no runtime CDN dependency).

## 🛠 ソースから再生成 / Build

```bash
# 顔テクスチャを変えたいとき（色や要素位置は make_face_tex.py 上部の定数で調整）
python make_face_tex.py
# 自己完結 HTML（docs/index.html = 公開サイト & オフライン版）を再生成
python build.py
```

`index.html` が開発用ソース（three.js は CDN、`./*.glb` を fetch）。ローカル確認は任意の静的サーバで（例: `python -m http.server 8765`）。

## 📦 内容物 / Repo layout

| | |
|---|---|
| `docs/index.html` | 公開サイト本体（自己完結・GitHub Pages が配信。オフライン版もこれ） |
| `index.html` | 開発用ソース |
| `assembled.glb` / `coreS3_face.glb` | 本体10パーツ / CoreS3-Lite ケース（M5Stack STL 由来の派生物） |
| `coreS3_face_tex.png` | 前面の顔テクスチャ（`make_face_tex.py` 生成の自作画像） |
| `make_face_tex.py` / `build.py` | テクスチャ生成 / 自己完結 HTML ビルド |
| `vendor/` | three.js r0.160（MIT, 同梱） |

## 🙏 謝辞 / Acknowledgments

- **Stack-chan** — 原作: ししかわ氏（Shinya Ishikawa, [@meganetaaan](https://github.com/meganetaaan)）による、オープンソースの超かわいいロボット。プロジェクト: [stack-chan/stack-chan](https://github.com/stack-chan/stack-chan)
- **M5Stack** — K151 Stack-chan / CoreS3-Lite の製品化と、3D モデルのオープンソース公開（[m5stack/M5_Hardware](https://github.com/m5stack/M5_Hardware)）。
- **three.js** — WebGL 3D 描画ライブラリ。

すばらしいハードウェアとオープンな素材に感謝します。本ツールはそれらに着想を得た、非公式のファン制作物です。
Thanks to Shinya Ishikawa (the Stack-chan creator), M5Stack, and the three.js authors. This is an unofficial, fan-made tool inspired by their work.

## 📝 ライセンス / License

- 本プロジェクトのコード: **MIT**（© 2026 Stack-chan Color Simulator contributors） — [LICENSE](LICENSE)
- 3D モデル: **M5Stack K151 / CoreS3-Lite（MIT, © 2021 M5Stack）** 由来 — 描画: **three.js（MIT）**
- 詳細・帰属表示: [CREDITS.md](CREDITS.md)
