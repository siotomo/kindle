# フェーズ2: OCR基本実装 - 実装計画

## 概要
フェーズ1で取得したスクリーンショット画像群から、OCR技術を使用してテキストを抽出し、各ページごとのテキストファイルを生成するシステムの実装計画。

## 成果物
- **OCRテキスト抽出スクリプト** (`ocr_extract.py`)
- **設定ファイル** (`config.json`)
- **出力**: 各ページの生テキストファイル（`page_001.txt`, `page_002.txt`...）

## 技術選定
### OCRエンジン
1. **第1選択: Tesseract OCR + pytesseract**
   - オープンソース、無料
   - 日本語対応（jpn_vertデータ必要）
   - 縦書き・横書き両対応
   
2. **第2選択: Vision API (macOS内蔵)**
   - macOS専用だが高精度
   - 追加インストール不要
   - pyobjcライブラリ経由で利用

### 画像前処理ライブラリ
- OpenCV: 画像の前処理（ノイズ除去、二値化、傾き補正）
- Pillow: 基本的な画像操作

## 実装フェーズ

### Phase 2.1: 基本OCR実装（1日目）
**目標**: 単一画像からテキスト抽出できる最小実装
- Tesseractのインストールと設定
- 基本的なOCR関数の実装
- 1枚の画像でテスト

### Phase 2.2: 画像前処理の実装（2日目）
**目標**: OCR精度を向上させる前処理パイプライン
- グレースケール変換
- ノイズ除去（ガウシアンフィルタ）
- 二値化処理
- 傾き補正

### Phase 2.3: バッチ処理の実装（3日目）
**目標**: 複数画像を効率的に処理
- ディレクトリ内の全画像を自動処理
- プログレスバー表示
- エラーハンドリング
- 処理済みファイルのスキップ機能

### Phase 2.4: 日本語最適化（4日目）
**目標**: 日本語テキストの認識精度向上
- 縦書き・横書きの自動判定
- ルビ（ふりがな）の処理
- 句読点・記号の正確な認識
- フォント別の最適化パラメータ

### Phase 2.5: 後処理とクリーンアップ（5日目）
**目標**: 抽出されたテキストの品質改善
- 文字化けの修正
- 改行位置の最適化
- 重複文字の除去
- 基本的な誤字修正

## ディレクトリ構造
```
phase2_ocr/
├── README.md              # 使用方法と設定ガイド
├── requirements.txt       # 必要なPythonパッケージ
├── config.json           # OCR設定ファイル
├── ocr_extract.py        # メインスクリプト
├── preprocessing.py      # 画像前処理モジュール
├── postprocessing.py     # テキスト後処理モジュール
├── utils/
│   ├── __init__.py
│   ├── image_utils.py    # 画像処理ユーティリティ
│   └── text_utils.py     # テキスト処理ユーティリティ
├── tests/
│   ├── test_ocr.py       # OCR機能のテスト
│   └── sample_images/    # テスト用画像
└── output/               # 出力先ディレクトリ
```

## 設定項目（config.json）
```json
{
  "ocr_engine": "tesseract",
  "language": "jpn+eng",
  "preprocessing": {
    "grayscale": true,
    "denoise": true,
    "threshold": "adaptive",
    "deskew": true
  },
  "output": {
    "format": "txt",
    "encoding": "utf-8",
    "preserve_layout": false
  },
  "batch": {
    "parallel_workers": 4,
    "chunk_size": 10,
    "retry_failed": true
  }
}
```

## コマンドラインインターフェース
```bash
# 基本実行（フェーズ1の出力を自動検出）
python ocr_extract.py --book "Python入門"

# カスタム入力ディレクトリ指定
python ocr_extract.py --input "./screenshots" --output "./texts"

# 特定ページ範囲のみ処理
python ocr_extract.py --book "Python入門" --start 1 --end 50

# 並列処理のワーカー数指定
python ocr_extract.py --book "Python入門" --workers 8

# デバッグモード（詳細ログ出力）
python ocr_extract.py --book "Python入門" --debug
```

## 品質メトリクス
- **文字認識率**: 95%以上を目標
- **処理速度**: 1ページあたり2-5秒
- **メモリ使用量**: 最大2GB以内
- **エラー率**: 1%未満

## 依存関係
- Python 3.8以上
- Tesseract 4.0以上
- OpenCV 4.5以上
- NumPy, Pillow, pytesseract

## リスクと対策
1. **OCR精度が低い場合**
   - 複数のOCRエンジンを組み合わせる
   - 機械学習モデルでの後処理

2. **処理速度が遅い場合**
   - GPU活用（CUDA対応）
   - 分散処理の実装

3. **メモリ不足**
   - 画像の分割処理
   - ストリーミング処理の実装

## 次フェーズへの引き継ぎ
- 出力形式: UTF-8エンコードのプレーンテキスト
- ファイル命名規則: `page_XXX.txt`（XXXは3桁のゼロパディング）
- メタデータ: 各ファイルに処理日時、使用設定を記録

## 成功基準
- [ ] 100ページの画像を自動処理できる
- [ ] 日本語テキストを95%以上の精度で認識
- [ ] エラー発生時も処理を継続できる
- [ ] 処理済みファイルをスキップできる
- [ ] 進捗状況をリアルタイムで確認できる