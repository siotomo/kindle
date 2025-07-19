# フェーズ2: OCR基本実装

## 概要
フェーズ1で取得したスクリーンショット画像からOCR（光学文字認識）を使用してテキストを抽出し、各ページごとのテキストファイルとして保存するシステム。

## 前提条件
### 必須要件
1. **フェーズ1の完了**
   - スクリーンショット画像が `output/[book_name]/` に保存済み
   - 画像形式: PNG または JPG
   - ファイル命名規則: `page_001.png`, `page_002.png`...

2. **Tesseract OCRのインストール**
   ```bash
   # Homebrewを使用
   brew install tesseract
   
   # 日本語データのインストール
   brew install tesseract-lang
   ```

3. **Python環境**
   - Python 3.8以上
   - 仮想環境の使用を推奨

### 動作環境
- macOS 10.14以降
- メモリ: 4GB以上推奨
- ストレージ: 画像サイズの2倍以上の空き容量

## セットアップ
```bash
# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate

# 必要なライブラリのインストール
pip install -r requirements.txt

# Tesseractのインストール確認
tesseract --version
```

## 使用方法
### 必須引数
- `--book`: 本の名前（フェーズ1で使用したものと同じ）

### オプション引数
- `--input`: 入力画像ディレクトリ（デフォルト: `../output/[book_name]/`）
- `--output`: 出力テキストディレクトリ（デフォルト: `./output/[book_name]/`）
- `--start`: 開始ページ番号（デフォルト: 1）
- `--end`: 終了ページ番号（デフォルト: 全ページ）
- `--workers`: 並列処理のワーカー数（デフォルト: 4）
- `--debug`: デバッグモード（詳細ログ出力）

### 実行例
```bash
# 基本実行（フェーズ1の出力を自動検出）
python ocr_extract.py --book "Python入門"

# カスタム入力ディレクトリ指定
python ocr_extract.py --input "./screenshots" --output "./texts"

# 特定ページ範囲のみ処理
python ocr_extract.py --book "Python入門" --start 1 --end 50

# 高速処理（8並列）
python ocr_extract.py --book "Python入門" --workers 8
```

## 設定
`config.json`で以下の項目を設定できます：
- `ocr_engine`: 使用するOCRエンジン（tesseract/vision）
- `language`: 認識言語（jpn+eng）
- `preprocessing`: 画像前処理の設定
  - `grayscale`: グレースケール変換
  - `denoise`: ノイズ除去
  - `threshold`: 二値化処理
  - `deskew`: 傾き補正
- `output`: 出力設定
  - `format`: 出力形式（txt/json）
  - `encoding`: 文字エンコーディング（utf-8）
- `batch`: バッチ処理設定
  - `parallel_workers`: 並列ワーカー数
  - `retry_failed`: 失敗時の再試行

## 出力
- テキストファイルは `output/[book_name]/` フォルダに保存
- ファイル名: `page_001.txt`, `page_002.txt`, ...
- エンコーディング: UTF-8
- 処理ログ: `output/[book_name]/ocr_log.json`

## トラブルシューティング
### よくある問題
1. **「Tesseractが見つかりません」エラー**
   ```bash
   # Tesseractのパスを確認
   which tesseract
   
   # パスを環境変数に設定
   export PATH="/opt/homebrew/bin:$PATH"
   ```

2. **日本語が文字化けする**
   - 日本語データがインストールされているか確認
   ```bash
   tesseract --list-langs | grep jpn
   ```

3. **処理が遅い**
   - ワーカー数を増やす: `--workers 8`
   - 画像サイズを確認（大きすぎる場合は前処理で縮小）

4. **メモリ不足エラー**
   - ワーカー数を減らす: `--workers 2`
   - バッチサイズを調整（config.json）

## 品質向上のヒント
1. **画像の品質**
   - 解像度: 300DPI以上推奨
   - コントラスト: はっきりとした白黒

2. **前処理の調整**
   - フォントが薄い場合: `threshold`を調整
   - ノイズが多い場合: `denoise`を有効化

3. **後処理**
   - 次のフェーズで文章の整形を行います
   - 現段階では生のOCR結果を保存

## 注意事項
- OCR処理には時間がかかります（1ページあたり2-5秒）
- 大量のページを処理する場合は、分割実行を推奨
- 処理済みファイルは自動的にスキップされます
- 著作権法を遵守し、個人利用の範囲でご使用ください

## 次のステップ
フェーズ3では、抽出されたテキストファイルを結合・整形します。