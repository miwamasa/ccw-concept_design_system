# Concept Design Support System (CDSS)

コンポーネントベースのアプローチによる概念設計支援システムのプロトタイプ実装

## 概要

このシステムは、論文 "Concept Design Visualization - A component-based approach" (Mikito Iwamasa, Toshiba Corp., 2000) に基づいて実装されたシステムレベルの概念設計支援ツールです。

### 主な機能

- **インタラクティブ設計探索**: ステップバイステップでDE/SIコンポーネントを使用しながら設計探索を体験
- **知識ベースシステム**: 車の衝突回避システムの例を含む、ドメイン知識の活用
- **設計探索 (DE: Design Exploration)**: 設計プロセスを6種類のコンポーネント(SI, PI, EI, DI, CB, SA)で記録
- **論理依存グラフ (LD: Logical Dependency)**: システム間の論理的な依存関係を表現
- **システム統合グラフ (SI: Systems Integration)**: 最終的なシステム階層構造を5種類のコンポーネント(CND, BUP, COL, ALT, EXO)で可視化
- **自動変換**: DE → LD → SI への自動グラフ変換
- **リアルタイムグラフ可視化**: ReactFlowによる美しいインタラクティブなグラフ表示

## システムアーキテクチャ

### バックエンド (Python + FastAPI)
- **コンポーネントモデル**: DEコンポーネント (SI, PI, EI, DI, CB, SA) とSIコンポーネント (CND, BUP, COL, ALT, EXO)
- **グラフ構造**: NetworkXベースのグラフ管理
- **設計探索エンジン**: 状態遷移システムによる設計プロセスのガイド
- **グラフ変換エンジン**: DE→LD→SIの自動変換アルゴリズム

### フロントエンド (React + TypeScript + ReactFlow)
- **ビジュアルエディタ**: ReactFlowによるインタラクティブなグラフ可視化
- **リアルタイム更新**: APIとの連携による動的なグラフ表示
- **マルチグラフ表示**: DE、LD、SIグラフの同時表示

## セットアップ

### 前提条件
- Python 3.9以上
- Node.js 18以上
- npm または yarn

### インストール

#### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd ccw-concept_design_system
```

#### 2. バックエンドのセットアップ
```bash
cd backend
pip install -r requirements.txt
```

#### 3. フロントエンドのセットアップ
```bash
cd frontend
npm install
```

## 起動方法

### 方法1: 個別に起動

#### バックエンドの起動
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

#### フロントエンドの起動
```bash
cd frontend
npm run dev
```

### 方法2: 同時起動（ルートディレクトリから）
```bash
npm install
npm run dev
```

## 使い方

1. ブラウザで http://localhost:5173 を開く

2. モードを選択:
   - **Interactive Mode**: ステップバイステップで設計探索を体験
   - **Auto Mode**: 自動的に設計探索を実行

### Interactive Mode（推奨）

インタラクティブモードでは、実際にDE/SIコンポーネントを使いながら設計探索を体験できます。

1. "Start Exploration" をクリック（例: "car_running"）

2. 各ステップで入力:
   - **SI (Situation Assessment)**: 状況を評価
   - **PI (Problem Identification)**: 問題を特定
   - **EI (Establish Intention)**: 意図を確立
   - **DI (Decompose Intention)** または **SA (Solution Assignment)**: 意図を分解 or 解決策を適用

3. 知識ベースからの提案を参考にしながら進める

4. DEグラフがリアルタイムで更新される

5. サブシステムがある場合は、順次探索を続ける

### Auto Mode

自動モードでは、定義済みのシナリオで一括して設計探索を実行します。

1. 初期システムを入力（例: "car_running"）

2. "Start Exploration" をクリックしてDEグラフを生成

3. "Convert to LD & SI" をクリックして全てのグラフを表示

## DEコンポーネント

| コンポーネント | 名称 | 役割 |
|--------------|------|------|
| SI | Situation Assessment | 状況評価 |
| PI | Problem Identification | 問題特定 |
| EI | Establish Intention | 意図確立 |
| DI | Decompose Intention | 意図分解 |
| CB | Conditional Branch | 条件分岐 |
| SA | Solution Assignment | 解決策割り当て |

## SIコンポーネント

| コンポーネント | 名称 | 役割 |
|--------------|------|------|
| CND | Condition | 条件による役割分担 |
| BUP | Backups | バックアップ関係 |
| COL | Collaboration | 協調関係 |
| ALT | Alternative | 代替関係 |
| EXO | Exclusive | 排他的選択 |

## API エンドポイント

### 基本エンドポイント
- `GET /` - APIルート情報
- `GET /health` - ヘルスチェック
- `GET /api/component-types` - 利用可能なコンポーネント型の一覧

### 自動探索エンドポイント
- `POST /api/explore` - 設計探索の実行
- `GET /api/graphs/de` - DEグラフの取得
- `GET /api/graphs/ld` - LDグラフの取得
- `GET /api/graphs/si` - SIグラフの取得
- `POST /api/convert` - 全グラフの変換と取得

### インタラクティブ探索エンドポイント
- `POST /api/interactive/start` - インタラクティブ探索の開始
- `POST /api/interactive/situation` - 状況評価ステップ
- `POST /api/interactive/problem` - 問題特定ステップ
- `POST /api/interactive/intention` - 意図確立ステップ
- `POST /api/interactive/decompose` - 意図分解ステップ
- `POST /api/interactive/solution` - 解決策適用ステップ
- `GET /api/interactive/state` - 現在の探索状態の取得

### 知識ベースエンドポイント
- `GET /api/knowledge-base` - 知識ベース全体の取得
- `GET /api/knowledge-base/systems` - 全システムの一覧

## プロジェクト構造

```
ccw-concept_design_system/
├── backend/                    # Python/FastAPI バックエンド
│   ├── app/
│   │   ├── models/            # データモデル
│   │   │   ├── component.py   # 基底コンポーネントクラス
│   │   │   ├── de_components.py # DEコンポーネント
│   │   │   ├── si_components.py # SIコンポーネント
│   │   │   └── graphs.py      # グラフ構造
│   │   ├── services/          # ビジネスロジック
│   │   │   ├── design_exploration.py # 設計探索エンジン
│   │   │   └── graph_conversion.py   # グラフ変換エンジン
│   │   └── main.py            # FastAPIアプリケーション
│   └── requirements.txt       # Python依存関係
├── frontend/                  # React/TypeScript フロントエンド
│   ├── src/
│   │   ├── components/        # Reactコンポーネント
│   │   │   └── GraphVisualization.tsx
│   │   ├── services/          # APIクライアント
│   │   │   └── api.ts
│   │   ├── types/             # TypeScript型定義
│   │   │   └── index.ts
│   │   ├── App.tsx            # メインアプリケーション
│   │   └── main.tsx           # エントリーポイント
│   └── package.json           # Node.js依存関係
├── spec/                      # 仕様書
│   └── specfication_from_paper.md
├── instructions.md            # 実装指示
└── README.md                  # このファイル
```

## 開発

### バックエンド開発
```bash
cd backend
# テストの実行
pytest

# コードフォーマット
black app/

# 型チェック
mypy app/
```

### フロントエンド開発
```bash
cd frontend
# ビルド
npm run build

# プレビュー
npm run preview
```

## 技術スタック

### バックエンド
- **FastAPI**: Webフレームワーク
- **Pydantic**: データバリデーション
- **NetworkX**: グラフデータ構造
- **Uvicorn**: ASGIサーバー

### フロントエンド
- **React 18**: UIライブラリ
- **TypeScript**: 型安全性
- **ReactFlow**: グラフ可視化
- **Vite**: ビルドツール
- **Axios**: HTTPクライアント

## ライセンス

MIT

## 参考文献

Mikito Iwamasa, "Concept Design Visualization - A component-based approach", Toshiba Corp., 2000
