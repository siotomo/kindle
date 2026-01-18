# Kindle本テキスト抽出システム

Kindleアプリから書籍をテキスト化し、マークダウンに変換する自動化パイプライン

## 全体パイプライン

```mermaid
flowchart LR
    subgraph Input
        K[📚 Kindle App]
    end

    subgraph Phase1["Phase 1 ✅"]
        SC[スクリーンショット取得]
    end

    subgraph Phase2["Phase 2 📋"]
        OCR[OCR処理]
    end

    subgraph Phase3["Phase 3 ❌"]
        TXT[テキスト結合・整形]
    end

    subgraph Phase4["Phase 4 ❌"]
        MD[マークダウン変換]
    end

    subgraph Phase5["Phase 5 ❌"]
        PIPE[パイプライン統合]
    end

    K --> SC
    SC -->|page_001.png...| OCR
    OCR -->|page_001.txt...| TXT
    TXT -->|book.txt| MD
    MD -->|book.md| PIPE

    style Phase1 fill:#90EE90
    style Phase2 fill:#FFE4B5
    style Phase3 fill:#FFB6C1
    style Phase4 fill:#FFB6C1
    style Phase5 fill:#FFB6C1
```

## 技術スタック

```mermaid
flowchart TB
    subgraph OS["対象OS"]
        MAC[macOS 10.14+]
    end

    subgraph Lang["言語"]
        PY[Python 3.7+]
    end

    subgraph Phase1Lib["Phase 1: スクリーンショット"]
        direction TB
        PAG[pyautogui<br/>画面操作・キャプチャ]
        PIL[Pillow<br/>画像保存]
        AS[AppleScript<br/>アプリ制御]
    end

    subgraph Phase2Lib["Phase 2: OCR（計画）"]
        direction TB
        TES[Tesseract OCR<br/>文字認識エンジン]
        OCV[OpenCV<br/>画像前処理]
        NP[NumPy<br/>数値計算]
    end

    subgraph Config["設定"]
        JSON[JSON<br/>config.json]
        CLI[argparse<br/>CLI]
    end

    MAC --> PY
    PY --> Phase1Lib
    PY --> Phase2Lib
    PY --> Config
```

## ディレクトリ構成

```
kindle/
├── CLAUDE.md                    # プロジェクト計画書
├── README.md                    # このファイル
├── phase1_screenshot/           # ✅ 実装完了
│   ├── capture.py              # メインスクリプト
│   ├── config.json             # 設定ファイル
│   └── README.md
└── phase2_ocr/                  # 📋 計画完了
    ├── README.md
    └── phase2_implementation_plan.md
```

## 実装状況

| Phase | 内容 | 状態 | 出力物 |
|-------|------|------|--------|
| 1 | スクリーンショット取得 | ✅ 完了 | `page_XXX.png` |
| 2 | OCR処理 | 📋 計画済 | `page_XXX.txt` |
| 3 | テキスト結合・整形 | ❌ 未着手 | `book.txt` |
| 4 | マークダウン変換 | ❌ 未着手 | `book.md` |
| 5 | パイプライン統合 | ❌ 未着手 | 統合CLI |

## Phase 2 OCR の技術選定

```mermaid
flowchart TD
    IMG[入力画像<br/>page_XXX.png]

    subgraph Preprocess["前処理 (OpenCV)"]
        GS[グレースケール化]
        DN[ノイズ除去]
        TH[二値化]
        DS[傾き補正]
    end

    subgraph OCR["OCR処理"]
        T1[Tesseract<br/>第1選択]
        T2[macOS Vision API<br/>代替]
    end

    subgraph Post["後処理"]
        CL[文字クリーニング]
        LY[レイアウト復元]
    end

    OUT[出力テキスト<br/>page_XXX.txt]

    IMG --> GS --> DN --> TH --> DS
    DS --> T1 & T2
    T1 & T2 --> CL --> LY --> OUT
```

**品質目標**: 認識率95%以上、処理速度2-5秒/ページ

## クイックスタート

### Phase 1: スクリーンショット取得

```bash
# 依存関係のインストール
pip install pyautogui pillow

# 実行
cd phase1_screenshot
python capture.py --book "書籍名" --pages 100
```

詳細は [phase1_screenshot/README.md](./phase1_screenshot/README.md) を参照
