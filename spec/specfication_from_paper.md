# コンセプト設計支援システム（CDSS）仕様書

**バージョン**: 1.0  
**作成日**: 2025年11月17日  
**基づく論文**: "Concept Design Visualization - A component-based approach" (Mikito Iwamasa, Toshiba Corp., 2000)

---

## 目次

1. [システム概要](#1-システム概要)
2. [システムアーキテクチャ](#2-システムアーキテクチャ)
3. [DEコンポーネント仕様](#3-deコンポーネント仕様)
4. [SIコンポーネント仕様](#4-siコンポーネント仕様)
5. [グラフ構造仕様](#5-グラフ構造仕様)
6. [設計自動化アルゴリズム](#6-設計自動化アルゴリズム)
7. [データ構造](#7-データ構造)
8. [API仕様](#8-api仕様)
9. [ユースケース](#9-ユースケース)
10. [テストケース](#10-テストケース)

---

## 1. システム概要

### 1.1 目的

コンセプト設計支援システム（CDSS: Concept Design Support System）は、大規模ITシステムの概念設計段階において、設計者の探索活動を支援し、設計履歴を可視化・記録し、最終的なシステム統合構造を半自動的に生成するシステムである。

### 1.2 主要機能

- **設計探索支援**: 状態遷移システムによる設計プロセスのガイド
- **設計履歴記録**: DEグラフによる設計探索履歴の可視化
- **システム統合支援**: SIグラフによるシステム階層構造の設計
- **自動変換**: DEグラフからSIグラフへの自動変換
- **知識ベース統合**: ドメイン知識の活用と参照

### 1.3 システム全体図

```
┌─────────────────────────────────────────────────────────┐
│        コンセプト設計支援システム（CDSS）                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐              ┌──────────────┐        │
│  │   設計者     │              │  知識ベース   │        │
│  │  (Designer)  │◄────────────►│    (KB)      │        │
│  └──────┬───────┘              └──────────────┘        │
│         │                                               │
│         ▼                                               │
│  ┌─────────────────────────┐                           │
│  │   設計探索モジュール      │                           │
│  │  (Design Exploration)   │                           │
│  │   ・状態遷移制御         │                           │
│  │   ・DEコンポーネント     │                           │
│  │   ・DEグラフ生成         │────────────┐              │
│  └─────────────────────────┘            │              │
│                                         ▼              │
│                              ┌─────────────────────┐   │
│                              │   グラフ変換エンジン  │   │
│                              │  (Conversion Engine) │   │
│                              │   ・LD グラフ生成    │   │
│                              │   ・意味論解釈       │   │
│                              │   ・階層抽出         │   │
│                              └──────────┬──────────┘   │
│                                         │              │
│                                         ▼              │
│  ┌─────────────────────────┐                           │
│  │   システム統合モジュール   │                           │
│  │  (Systems Integration)  │                           │
│  │   ・SIコンポーネント     │                           │
│  │   ・SIグラフ生成         │                           │
│  │   ・階層構造設計         │                           │
│  └─────────────────────────┘                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 2. システムアーキテクチャ

### 2.1 レイヤ構造

システムは以下の4層で構成される：

```
┌───────────────────────────────────────────┐
│      プレゼンテーション層                    │
│  ・GUI（グラフ可視化、インタラクション）      │
└──────────────┬────────────────────────────┘
               │
┌──────────────▼────────────────────────────┐
│         ビジネスロジック層                   │
│  ・設計探索エンジン                         │
│  ・システム統合エンジン                      │
│  ・グラフ変換エンジン                       │
└──────────────┬────────────────────────────┘
               │
┌──────────────▼────────────────────────────┐
│          データ管理層                       │
│  ・DEグラフ管理                            │
│  ・SIグラフ管理                            │
│  ・知識ベース管理                          │
└──────────────┬────────────────────────────┘
               │
┌──────────────▼────────────────────────────┐
│         データストレージ層                   │
│  ・グラフデータベース                       │
│  ・知識ベースDB                            │
│  ・設計履歴DB                              │
└───────────────────────────────────────────┘
```

### 2.2 主要モジュール

#### 2.2.1 設計探索モジュール (Design Exploration Module)

**責務**:
- 設計者との対話的なインタラクション
- 状態遷移に基づく設計プロセスのガイド
- DEグラフの構築と管理

**主要コンポーネント**:
- 状態遷移エンジン
- DEコンポーネントファクトリ
- 知識ベースインターフェース

#### 2.2.2 システム統合モジュール (Systems Integration Module)

**責務**:
- SIグラフの構築と管理
- システム階層構造の設計
- サブシステム間関係の定義

**主要コンポーネント**:
- SIコンポーネントファクトリ
- 階層構造マネージャ
- 関係性検証エンジン

#### 2.2.3 グラフ変換モジュール (Graph Conversion Module)

**責務**:
- DEグラフからLDグラフへの変換
- LDグラフからSIグラフへの変換
- 意味論に基づく解釈

**主要コンポーネント**:
- セマンティクスエンジン
- グラフ変換エンジン
- 階層抽出エンジン

---

## 3. DEコンポーネント仕様

### 3.1 概要

設計探索（DE: Design Exploration）コンポーネントは、人間の問題解決活動を抽象化した6種類のコンポーネントで構成される。

### 3.2 コンポーネント一覧

#### 3.2.1 SI: Situation Assessment（状況評価）

**目的**: 与えられたシステムに対する状況の評価を記録

**入力ポート**:
- `System`: 評価対象のシステム (Sy)

**出力ポート**:
- `EvaluatedSystem`: 状況評価後のシステム (Sy, Si)

**図示**:
```
    Sy ──┐
         │
    ┌────▼────┐
    │   SI    │
    │ (状況評価) │
    └────┬────┘
         │
         ▼
    (Sy, Si)
```

**意味論**:
```
Input: System(Sy)
Process: Assess situation Si for System Sy
Output: System(Sy) with Situation(Si)
```

**例**:
- システム: 「車が走行中」
- 状況評価: 「障害物が道路上に存在」

#### 3.2.2 PI: Problem Identification（問題特定）

**目的**: システムに対する問題を特定・記録

**入力ポート**:
- `System`: 問題を持つシステム (Sy)

**出力ポート**:
- `Problem`: 特定された問題 (P)

**図示**:
```
    Sy ──┐
         │
    ┌────▼────┐
    │   PI    │
    │ (問題特定) │
    └────┬────┘
         │
         ▼
        P
```

**意味論**:
```
Input: System(Sy)
Process: Identify problem P in System Sy
Output: Problem(P)
```

**例**:
- システム: 「車が走行中 + 障害物存在」
- 問題: 「衝突の可能性」

#### 3.2.3 EI: Establish Intention（意図確立）

**目的**: 問題を解決するための意図を確立

**入力ポート**:
- `System`: 現在のシステム (Sy)
- `Problem`: 解決すべき問題 (P)

**出力ポート**:
- `Intention`: 確立された意図 (I)

**図示**:
```
    Sy ──┐    P ──┐
         │        │
    ┌────▼────────▼┐
    │      EI      │
    │   (意図確立)   │
    └───────┬───────┘
            │
            ▼
            I
```

**意味論**:
```
Input: System(Sy), Problem(P)
Process: Establish intention I to solve P
Output: Intention(I)
```

**例**:
- システム: 「車が走行中 + 障害物存在」
- 問題: 「衝突の可能性」
- 意図: 「衝突を回避するシステム」

#### 3.2.4 DI: Decompose Intention（意図分解）

**目的**: 意図とシステムをサブ意図とサブシステムに分解

**入力ポート**:
- `System`: 分解対象のシステム (Sy)
- `Intention`: 分解する意図 (I)

**出力ポート**:
- `SubIntentions`: サブ意図のリスト ({I1, I2, ...})
- `SubSystems`: サブシステムのリスト ({Sy1, Sy2, ...})

**図示**:
```
   Sy ──┐   I ──┐
        │       │
   ┌────▼───────▼──┐
   │      DI       │
   │   (意図分解)    │
   └────┬──────┬───┘
        │      │
   ┌────▼──┐ ┌─▼────┐
   │{I1,I2}│ │{Sy1, │
   │  ...  │ │Sy2,..}│
   └───────┘ └──────┘
```

**意味論**:
```
Input: System(Sy), Intention(I)
Process: Decompose (I, Sy) into {(I1, Sy1), (I2, Sy2), ...}
Output: SubIntentions({I1, I2, ...}), SubSystems({Sy1, Sy2, ...})
```

**例**:
- 意図: 「衝突を回避するシステム」
- 分解結果:
  - サブ意図1: 「車による回避」→ サブシステム1: 「自動操縦システム」
  - サブ意図2: 「運転者による回避」→ サブシステム2: 「人間操縦システム」

#### 3.2.5 CB: Conditional Branch（条件分岐）

**目的**: 特定の状況下で意図を選択的にフォーカス

**入力ポート**:
- `System`: 現在のシステム (Sy)
- `Intention`: フォーカスする意図 (I)
- `Situation`: 条件となる状況 (Si)

**出力ポート**:
- `FocusedIntention`: 状況に基づく意図 (I, Si)

**図示**:
```
  Sy─┐  I─┐  Si─┐
     │    │     │
  ┌──▼────▼─────▼┐
  │      CB      │
  │  (条件分岐)    │
  └───────┬───────┘
          │
          ▼
      (I, Si)
```

**意味論**:
```
Input: System(Sy), Intention(I), Situation(Si)
Process: Focus intention I for situation Si
Output: Intention(I) under Situation(Si)
```

**例**:
- 意図: 「運転者による回避」
- 状況: 「視界不良（霧、嵐）」
- 結果: 「視界不良時の運転者支援」

#### 3.2.6 SA: Solution Assignment（解決策割り当て）

**目的**: システムに解決策を適用してサブシステムを生成

**入力ポート**:
- `System`: 現在のシステム (Sy)
- `Solution`: 適用する解決策 (So)

**出力ポート**:
- `SubSystem`: 解決策適用後のサブシステム (Sy')

**図示**:
```
   Sy ──┐  So ──┐
        │       │
   ┌────▼───────▼┐
   │     SA      │
   │ (解決策割当)  │
   └──────┬──────┘
          │
          ▼
         Sy'
```

**意味論**:
```
Input: System(Sy), Solution(So)
Process: Apply solution So to system Sy
Output: SubSystem(Sy')
```

**例**:
- システム: 「視界不良時の運転者支援」
- 解決策: 「障害物警報」
- サブシステム: 「障害物警報システム」

### 3.3 DEコンポーネントの相互関係図

```
      ┌──────┐
      │ Fact │  (初期システム)
      └───┬──┘
          │
          ▼
      ┌───────────┐
      │    SI     │  状況評価
      │(Situation │
      │Assessment)│
      └─────┬─────┘
            │
            ▼
      ┌───────────┐
      │    PI     │  問題特定
      │ (Problem  │
      │Identifi.) │
      └─────┬─────┘
            │
            ▼
      ┌───────────┐
      │    EI     │  意図確立
      │(Establish │
      │Intention) │
      └─────┬─────┘
            │
       ┌────┴────┐
       │         │
       ▼         ▼
  ┌────────┐  ┌────────┐
  │   DI   │  │   SA   │  意図分解 or 解決策適用
  │(Decom- │  │(Solut. │
  │ pose)  │  │Assign) │
  └───┬────┘  └────┬───┘
      │            │
      │            ▼
      │        ┌──────┐
      │        │ End  │  (最終サブシステム)
      │        └──────┘
      │
      ▼
  ┌────────┐
  │   CB   │  条件分岐（必要に応じて）
  │(Condi- │
  │tional) │
  └───┬────┘
      │
      ▼
   (再帰的に SI へ)
```

### 3.4 コンポーネント接続ルール

1. **SI → PI**: 状況評価の後に問題特定
2. **PI → EI**: 問題特定の後に意図確立
3. **EI → DI or SA**: 意図確立後、分解または解決策適用
4. **DI → SI**: 分解されたサブシステムに対して再度状況評価
5. **CB → SI**: 条件分岐後、特定状況下での状況評価
6. **SA → End**: 解決策適用で終端ノード

---

## 4. SIコンポーネント仕様

### 4.1 概要

システム統合（SI: Systems Integration）コンポーネントは、サブシステム間の協調関係を表現する5種類のコンポーネントで構成される。

### 4.2 コンポーネント一覧

#### 4.2.1 CND: Condition（条件）

**目的**: 状況に応じてサブシステムが役割を分担

**関係性**: Sys1とSys2が状況Si1、Si2に応じて役割を分担

**図示**:
```
         Si1    Si2
          │      │
          ▼      ▼
    Sys1 ─┬─ CND ─┬─ Sys2
          └───┬───┘
              │
            SysO
```

**意味論**:
```
Under Situation Si1: Sys1 performs role
Under Situation Si2: Sys2 performs role
Integration: SysO = CND(Sys1, Sys2, Si1, Si2)
```

**論理依存グラフ表現**:
```
     Si1          Si2
      │            │
      ▼            ▼
    Sys1         Sys2
      └────┬──────┘
           │ OR
           ▼
         SysO
```

**例**:
- Sys1: 「自動操縦システム」
- Sys2: 「人間操縦システム」
- Si1: 「通常走行時」
- Si2: 「特殊状況時」

#### 4.2.2 BUP: Backups（バックアップ）

**目的**: あるサブシステムが失敗した際に別のサブシステムがバックアップ

**関係性**: Sys2がSys1の失敗時にバックアップ

**図示**:
```
         Sys1
          │
          │ (primary)
    Sys1 ─┼─ BUP ──── Sys2
          │           (backup)
          └─────┬─────┘
                │
              SysO
```

**意味論**:
```
Primary: Sys1 operates normally
Backup: If Sys1 fails, Sys2 takes over
Integration: SysO = BUP(Sys1, Sys2)
```

**論理依存グラフ表現**:
```
        Sys1
         │
         │ (if fails)
         ▼
       Sys2
         │
         ▼
       SysO
```

**例**:
- Sys1: 「障害物警報システム」
- Sys2: 「操縦誘導システム」
- 関係: 「警報が機能しない場合、誘導システムが作動」

#### 4.2.3 COL: Collaboration（協調）

**目的**: 複数のサブシステムが協力して高次の目的を達成

**関係性**: Sys1とSys2が協調して動作

**図示**:
```
    Sys1 ────┐
             │
         ┌───▼───┐
         │  COL  │
         └───┬───┘
             │
    Sys2 ────┘
             │
             ▼
           SysO
```

**意味論**:
```
Collaboration: Sys1 AND Sys2 work together
Integration: SysO = COL(Sys1, Sys2)
```

**論理依存グラフ表現**:
```
    Sys1    Sys2
      │      │
      └──┬───┘
         │ AND
         ▼
       SysO
```

**例**:
- Sys1: 「障害物警報システム」
- Sys2: 「操縦誘導システム」
- 関係: 「両方が協力して視界不良時の運転を支援」

#### 4.2.4 ALT: Alternative（代替）

**目的**: 目的達成のために複数の選択肢が存在

**関係性**: Sys1またはSys2、または両方が必要

**図示**:
```
    Sys1 ────┐
             │
         ┌───▼───┐
         │  ALT  │
         └───┬───┘
             │
    Sys2 ────┘
             │
             ▼
           SysO
```

**意味論**:
```
Alternative: Sys1 OR Sys2 OR (Sys1 AND Sys2)
Integration: SysO = ALT(Sys1, Sys2)
```

**論理依存グラフ表現**:
```
    Sys1    Sys2
      │      │
      └──┬───┘
         │ OR (inclusive)
         ▼
       SysO
```

**例**:
- Sys1: 「自動操縦システム」
- Sys2: 「人間操縦システム + 支援システム」
- 関係: 「いずれか、または両方で衝突回避」

#### 4.2.5 EXO: Exclusive（排他）

**目的**: 複数の選択肢のうち1つのみを選択

**関係性**: Sys1またはSys2のいずれか一方のみ

**図示**:
```
    Sys1 ────┐
             │
         ┌───▼───┐
         │  EXO  │
         └───┬───┘
             │
    Sys2 ────┘
             │
             ▼
           SysO
```

**意味論**:
```
Exclusive: Sys1 XOR Sys2 (exactly one)
Integration: SysO = EXO(Sys1, Sys2)
```

**論理依存グラフ表現**:
```
    Sys1    Sys2
      │      │
      └──┬───┘
         │ XOR
         ▼
       SysO
```

**例**:
- Sys1: 「システム構成案A」
- Sys2: 「システム構成案B」
- 関係: 「どちらか一方を最終的に選択」

### 4.3 SIコンポーネント関係図

```
システム階層の例：

         ┌─────────────────────┐
         │      SysLvl1        │
         │  (衝突回避システム)    │
         └──────────┬──────────┘
                    │
         ┌──────────▼──────────┐
         │        CND          │  条件分岐
         └──┬─────────────┬────┘
            │             │
   ┌────────▼──┐    ┌────▼─────────┐
   │ SysLvl2-1 │    │  SysLvl2-2   │
   │(自動操縦)  │    │(人間操縦)     │
   └───────────┘    └──────┬───────┘
                           │
                    ┌──────▼──────┐
                    │     COL     │  協調
                    └──┬───────┬──┘
                       │       │
              ┌────────▼──┐ ┌──▼────────┐
              │SysLvl3-1  │ │ SysLvl3-2 │
              │(警報)     │ │(誘導)     │
              └───────────┘ └───────────┘
```

---

## 5. グラフ構造仕様

### 5.1 DEグラフ（Design Exploration Graph）

#### 5.1.1 定義

DEグラフは、設計探索の履歴を記録する有向グラフである。

**形式定義**:
```
DE_Graph = (V, E)
where:
  V = {v_i | v_i ∈ DE_Components ∪ {System, Problem, Intention, Situation, Solution}}
  E = {(v_i, v_j) | v_i, v_j ∈ V, ∃ port connection}
```

#### 5.1.2 ノード種別

| ノード種別 | 表現 | 説明 |
|-----------|------|------|
| DEコンポーネント | SI, PI, EI, DI, CB, SA | 設計探索活動 |
| システム | Sy | 設計対象システム |
| 問題 | P | 特定された問題 |
| 意図 | I | 確立された意図 |
| 状況 | Si | 評価された状況 |
| 解決策 | So | 適用された解決策 |

#### 5.1.3 エッジ種別

| エッジ種別 | 表現 | 説明 |
|-----------|------|------|
| データフロー | → | コンポーネント間のデータの流れ |
| 制御フロー | ⇒ | 設計プロセスの遷移 |

#### 5.1.4 DEグラフの例

```
                  ┌─────────┐
                  │  Fact   │
                  │  (Sy1)  │
                  └────┬────┘
                       │
                       ▼
                  ┌─────────┐
                  │   SI    │
                  └────┬────┘
                       │
                   ┌───▼────┐
                   │ (Sy2,S)│
                   └───┬────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
         ┌────────┐        ┌────────┐
         │   PI   │        │   KB   │ (Knowledge Base)
         └───┬────┘        └────────┘
             │
             ▼
          ┌──────┐
          │  P   │
          └──┬───┘
             │
             ▼
         ┌────────┐
         │   EI   │
         └───┬────┘
             │
             ▼
          ┌──────┐
          │ Int  │
          └──┬───┘
             │
             ▼
         ┌────────┐
         │   SA   │
         └───┬────┘
             │
             ▼
        ┌─────────┐
        │  (Sy3,  │
        │  Sol)   │
        └─────────┘
```

### 5.2 LDグラフ（Logical Dependency Graph）

#### 5.2.1 定義

LDグラフは、DEグラフとSIグラフの共通基盤となる論理依存関係を表すグラフである。

**形式定義**:
```
LD_Graph = (V, E, L)
where:
  V = {v_i | v_i ∈ {System, Situation}}
  E = {(v_i, v_j) | v_i, v_j ∈ V}
  L = {AND, OR, XOR} (論理演算子)
```

#### 5.2.2 論理演算子

| 演算子 | 記号 | 意味 |
|-------|------|------|
| AND | ∧ | 全ての入力が必要 |
| OR | ∨ | いずれかの入力が必要 |
| XOR | ⊕ | 1つの入力のみが必要 |

#### 5.2.3 LDグラフの例

```
     car_running
          │
          ▼
      ┌───────┐
      │obstacle│
      └───┬───┘
          │
          ▼
     car_crashing
          │
     ┌────┴────┐
     │         │
     ▼         ▼
  by_car   by_driver
     │         │
     ▼         ▼
 SubSys1  ┌────────┐
          │low_vis.│
          └───┬────┘
              │
         ┌────┴────┐
         │         │
         ▼         ▼
    by_alarm  by_guide
         │         │
         ▼         ▼
     SubSys3   SubSys4
```

### 5.3 SIグラフ（Systems Integration Graph）

#### 5.3.1 定義

SIグラフは、システム階層構造とサブシステム間の関係を表すグラフである。

**形式定義**:
```
SI_Graph = (V, E, H)
where:
  V = {v_i | v_i ∈ Systems}
  E = {(v_i, v_j, rel) | v_i, v_j ∈ V, rel ∈ SI_Components}
  H = {level_i} (階層レベル)
```

#### 5.3.2 階層構造

```
Level 0: SysLvl0 (最上位システム)
           │
Level 1:   ├── SysLvl1-1
           │     │
Level 2:   │     ├── SysLvl2-1
           │     └── SysLvl2-2
           │
           └── SysLvl1-2
                 │
Level 2:         └── SysLvl2-3
```

#### 5.3.3 SIグラフの例（車両制御システム）

```
                    ┌────────────────────────┐
                    │      SysLvl1           │
                    │ (Collision Avoidance)  │
                    └───────────┬────────────┘
                                │
                    ┌───────────▼───────────┐
                    │         CND           │
                    │   (obstacle/normal)   │
                    └─────┬──────────┬──────┘
                          │          │
              ┌───────────▼─┐    ┌──▼──────────────┐
              │  SysLvl2-1  │    │   SysLvl2-2     │
              │ (Auto       │    │ (Human          │
              │ Maneuvering)│    │ Maneuvering)    │
              └─────────────┘    └─────────┬───────┘
                                            │
                                ┌───────────▼──────────┐
                                │         CND          │
                                │   (low_visibility)   │
                                └────┬───────────┬─────┘
                                     │           │
                          ┌──────────▼──┐  ┌────▼─────────┐
                          │ SysLvl3-1   │  │  SysLvl3-2   │
                          │ (Obstacle   │  │ (Maneuvering │
                          │  Alarming)  │  │  Guiding)    │
                          └──────┬──────┘  └──────┬───────┘
                                 │                │
                                 └────────┬───────┘
                                          │
                                      ┌───▼────┐
                                      │  BUP   │
                                      └────────┘
```

---

## 6. 設計自動化アルゴリズム

### 6.1 設計探索アルゴリズム

#### 6.1.1 状態遷移システム

**状態定義**:
```
States = {
  Start,
  Fact,
  SituationAssessment,
  ProblemIdentification,
  EstablishIntention,
  Searching,
  DecomposeIntention,
  ApplyingSolution,
  SubSystemFound,
  End,
  AssessSideEffect,
  SideEffectIdentified,
  IdentifyingProblem
}
```

**遷移ルール**:
```
Transition_Rules = {
  (Start, -, Fact),
  (Fact, -, SituationAssessment),
  (SituationAssessment, -, AssessSideEffect),
  (AssessSideEffect, side_effect_found, SideEffectIdentified),
  (AssessSideEffect, no_side_effect, Searching),
  (SideEffectIdentified, -, ProblemIdentification),
  (ProblemIdentification, -, EstablishIntention),
  (EstablishIntention, -, Searching),
  (Searching, decompose, DecomposeIntention),
  (Searching, solution_found, ApplyingSolution),
  (DecomposeIntention, -, Fact),
  (ApplyingSolution, -, SubSystemFound),
  (SubSystemFound, more_to_explore, Fact),
  (SubSystemFound, complete, End)
}
```

#### 6.1.2 状態遷移図

```
                        ┌───────┐
                        │ Start │
                        └───┬───┘
                            │
                            ▼
                        ┌───────┐
                    ┌───┤ Fact  │◄────┐
                    │   └───┬───┘     │
                    │       │         │
                    │       ▼         │
                    │  ┌─────────────────┐
                    │  │   Situation     │
                    │  │   Assessment    │
                    │  └────────┬────────┘
                    │           │
                    │           ▼
                    │  ┌─────────────────┐
                    │  │  Assess Side    │
                    │  │     Effect      │
                    │  └──┬──────────┬───┘
                    │     │          │
                    │  [SE]        [No SE]
                    │     │          │
                    │     ▼          │
                    │  ┌──────────┐  │
                    │  │ Problem  │  │
                    │  │   Ident. │  │
                    │  └────┬─────┘  │
                    │       │        │
                    │       ▼        │
                    │  ┌──────────┐  │
                    │  │ Establish│  │
                    │  │ Intention│  │
                    │  └────┬─────┘  │
                    │       │        │
                    │       └────┬───┘
                    │            │
                    │            ▼
                    │       ┌──────────┐
                    │       │Searching │
                    │       └─┬──────┬─┘
                    │         │      │
                    │    [decomp]  [solution]
                    │         │      │
                    │         ▼      ▼
                    │    ┌────────┐ ┌──────────┐
                    │    │Decom-  │ │ Applying │
                    │    │pose    │ │ Solution │
                    │    └───┬────┘ └────┬─────┘
                    │        │           │
                    └────────┘           ▼
                                    ┌──────────┐
                                    │SubSystem │
                                    │  Found   │
                                    └─┬──────┬─┘
                                      │      │
                                  [more]  [done]
                                      │      │
                                      └──────┤
                                             ▼
                                         ┌─────┐
                                         │ End │
                                         └─────┘
```

#### 6.1.3 探索アルゴリズム（疑似コード）

```python
class DesignExplorationEngine:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.current_state = State.START
        self.de_graph = DEGraph()
        
    def explore(self, initial_system):
        """設計探索のメインループ"""
        self.current_system = initial_system
        self.current_state = State.FACT
        
        while self.current_state != State.END:
            action = self.get_action(self.current_state)
            result = self.execute_action(action)
            self.record_to_graph(action, result)
            self.current_state = self.transition(self.current_state, result)
            
        return self.de_graph
    
    def get_action(self, state):
        """状態に応じたアクションの決定"""
        actions = {
            State.FACT: self.initiate_system,
            State.SITUATION_ASSESSMENT: self.assess_situation,
            State.PROBLEM_IDENTIFICATION: self.identify_problem,
            State.ESTABLISH_INTENTION: self.establish_intention,
            State.SEARCHING: self.search_solution,
            State.DECOMPOSE_INTENTION: self.decompose,
            State.APPLYING_SOLUTION: self.apply_solution
        }
        return actions.get(state)
    
    def assess_situation(self):
        """状況評価の実行"""
        # 設計者とインタラクション
        situation = self.interact_with_designer(
            "What is the current situation for system {}?".format(
                self.current_system
            )
        )
        
        # 知識ベースへの問い合わせ
        kb_situation = self.kb.query_situation(self.current_system)
        
        # SI コンポーネントの生成
        si_component = SIComponent(
            system=self.current_system,
            situation=situation or kb_situation
        )
        
        return si_component
    
    def identify_problem(self):
        """問題特定の実行"""
        # 副作用の評価
        side_effects = self.assess_side_effects(
            self.current_system, 
            self.current_situation
        )
        
        if side_effects:
            # 知識ベースから問題を検索
            problem = self.kb.query_problem(
                self.current_system,
                self.current_situation
            )
            
            # PI コンポーネントの生成
            pi_component = PIComponent(
                system=self.current_system,
                problem=problem
            )
            
            return pi_component
        
        return None
    
    def establish_intention(self):
        """意図確立の実行"""
        intention = self.kb.query_intention(
            self.current_problem
        )
        
        # 設計者の確認
        confirmed_intention = self.interact_with_designer(
            "Proposed intention: {}. Confirm or modify?".format(
                intention
            )
        )
        
        # EI コンポーネントの生成
        ei_component = EIComponent(
            system=self.current_system,
            problem=self.current_problem,
            intention=confirmed_intention or intention
        )
        
        return ei_component
    
    def search_solution(self):
        """解決策の探索"""
        # 知識ベースから解決策候補を取得
        solutions = self.kb.query_solutions(
            self.current_intention
        )
        
        # 分解が必要か解決策適用が可能か判断
        if self.should_decompose(solutions):
            return {"action": "decompose", "data": None}
        else:
            return {"action": "solution", "data": solutions}
    
    def decompose(self):
        """意図とシステムの分解"""
        # 分解方法の決定
        decomposition = self.kb.query_decomposition(
            self.current_intention,
            self.current_system
        )
        
        # DI コンポーネントの生成
        di_component = DIComponent(
            system=self.current_system,
            intention=self.current_intention,
            sub_intentions=decomposition["intentions"],
            sub_systems=decomposition["systems"]
        )
        
        return di_component
    
    def apply_solution(self):
        """解決策の適用"""
        # 解決策の選択
        selected_solution = self.interact_with_designer(
            "Select solution from: {}".format(self.candidate_solutions)
        )
        
        # SA コンポーネントの生成
        sa_component = SAComponent(
            system=self.current_system,
            solution=selected_solution,
            subsystem=self.generate_subsystem(
                self.current_system, 
                selected_solution
            )
        )
        
        return sa_component
    
    def record_to_graph(self, action, result):
        """DEグラフへの記録"""
        self.de_graph.add_component(result)
        self.de_graph.add_edges(self.get_connections(result))
    
    def transition(self, current_state, result):
        """次の状態への遷移"""
        return self.state_machine.next_state(current_state, result)
```

### 6.2 グラフ変換アルゴリズム

#### 6.2.1 DEグラフからSIグラフへの変換手順

**全体フロー**:
```
DE Graph
    │
    ▼
Step 1: Convert to LD Graph
    │
    ▼
LD Graph
    │
    ▼
Step 2: Simplify LD Graph
    │
    ▼
Simplified LD Graph
    │
    ▼
Step 3: Extract Hierarchies
    │
    ▼
Hierarchical Structure
    │
    ▼
Step 4: Extract SI Components
    │
    ▼
SI Graph
    │
    ▼
Step 5: Resolve Alternatives
    │
    ▼
Final SI Graph
```

#### 6.2.2 Step 1: DEグラフからLDグラフへの変換

**変換ルール**:

| DEコンポーネント | LDグラフ表現 |
|-----------------|-------------|
| SI(Sy) → (Sy, Si) | Sy → (Sy, Si) |
| PI(Sy) → P | Sy → P |
| EI(Sy, P) → I | (Sy, P) → I |
| DI(Sy, I) → {(Ik, Syk)} | (Sy, I) → {(Ik, Syk)} (AND) |
| CB(Sy, I, Si) → (I, Si) | (Sy, I, Si) → (I, Si) |
| SA(Sy, So) → Sy' | (Sy, So) → Sy' |

**疑似コード**:
```python
def convert_de_to_ld(de_graph):
    """DEグラフをLDグラフに変換"""
    ld_graph = LDGraph()
    
    for component in de_graph.get_components():
        if isinstance(component, SIComponent):
            # SI: System → (System, Situation)
            ld_graph.add_node(component.system)
            ld_graph.add_node((component.system, component.situation))
            ld_graph.add_edge(
                component.system, 
                (component.system, component.situation)
            )
            
        elif isinstance(component, PIComponent):
            # PI: System → Problem
            ld_graph.add_node(component.system)
            ld_graph.add_node(component.problem)
            ld_graph.add_edge(component.system, component.problem)
            
        elif isinstance(component, EIComponent):
            # EI: (System, Problem) → Intention
            ld_graph.add_node((component.system, component.problem))
            ld_graph.add_node(component.intention)
            ld_graph.add_edge(
                (component.system, component.problem),
                component.intention,
                logic="AND"
            )
            
        elif isinstance(component, DIComponent):
            # DI: (System, Intention) → {(Intentionk, Systemk)}
            source = (component.system, component.intention)
            ld_graph.add_node(source)
            
            for sub_int, sub_sys in zip(
                component.sub_intentions, 
                component.sub_systems
            ):
                target = (sub_int, sub_sys)
                ld_graph.add_node(target)
                ld_graph.add_edge(source, target, logic="AND")
                
        elif isinstance(component, CBComponent):
            # CB: (System, Intention, Situation) → (Intention, Situation)
            source = (
                component.system, 
                component.intention, 
                component.situation
            )
            target = (component.intention, component.situation)
            ld_graph.add_node(source)
            ld_graph.add_node(target)
            ld_graph.add_edge(source, target)
            
        elif isinstance(component, SAComponent):
            # SA: (System, Solution) → SubSystem
            source = (component.system, component.solution)
            ld_graph.add_node(source)
            ld_graph.add_node(component.subsystem)
            ld_graph.add_edge(source, component.subsystem)
    
    return ld_graph
```

#### 6.2.3 Step 2: LDグラフの簡略化

**簡略化ルール**:
1. System、Situation、論理依存のみを残す
2. Problem、Intention、Solutionノードを削除
3. エッジの論理関係を保持

**疑似コード**:
```python
def simplify_ld_graph(ld_graph):
    """LDグラフを簡略化"""
    simplified = LDGraph()
    
    # System と Situation ノードのみを抽出
    for node in ld_graph.get_nodes():
        if is_system(node) or is_situation(node):
            simplified.add_node(node)
    
    # 論理依存関係を保持してエッジを再構築
    for edge in ld_graph.get_edges():
        source_sys = extract_system(edge.source)
        target_sys = extract_system(edge.target)
        
        if source_sys and target_sys:
            simplified.add_edge(
                source_sys, 
                target_sys, 
                logic=edge.logic
            )
    
    return simplified
```

#### 6.2.4 Step 3: 階層構造の抽出

**アルゴリズム**:
1. 連結成分を計算
2. 関節点でグラフを分割
3. 各サブグラフを階層レベルに割り当て

**疑似コード**:
```python
def extract_hierarchies(simplified_ld_graph):
    """階層構造を抽出"""
    # 連結成分を計算
    connected_components = find_connected_components(
        simplified_ld_graph
    )
    
    # 関節点を検出
    articulation_points = find_articulation_points(
        simplified_ld_graph
    )
    
    # 関節点で分割
    subgraphs = split_at_articulation_points(
        simplified_ld_graph,
        articulation_points
    )
    
    # 階層レベルを割り当て
    hierarchies = {}
    for level, subgraph in enumerate(subgraphs):
        hierarchies[f"Level_{level}"] = subgraph
    
    return hierarchies

def find_connected_components(graph):
    """連結成分を発見（深さ優先探索）"""
    visited = set()
    components = []
    
    for node in graph.get_nodes():
        if node not in visited:
            component = []
            dfs(graph, node, visited, component)
            components.append(component)
    
    return components

def dfs(graph, node, visited, component):
    """深さ優先探索"""
    visited.add(node)
    component.append(node)
    
    for neighbor in graph.get_neighbors(node):
        if neighbor not in visited:
            dfs(graph, neighbor, visited, component)

def find_articulation_points(graph):
    """関節点を発見（Tarjanのアルゴリズム）"""
    visited = set()
    disc = {}  # 発見時刻
    low = {}   # 最小到達時刻
    parent = {}
    ap = set() # 関節点集合
    time = [0]
    
    for node in graph.get_nodes():
        if node not in visited:
            dfs_ap(graph, node, visited, disc, low, parent, ap, time)
    
    return ap

def dfs_ap(graph, u, visited, disc, low, parent, ap, time):
    """関節点発見のための深さ優先探索"""
    children = 0
    visited.add(u)
    disc[u] = low[u] = time[0]
    time[0] += 1
    
    for v in graph.get_neighbors(u):
        if v not in visited:
            children += 1
            parent[v] = u
            dfs_ap(graph, v, visited, disc, low, parent, ap, time)
            
            low[u] = min(low[u], low[v])
            
            # 根ノードかつ複数の子を持つ
            if parent.get(u) is None and children > 1:
                ap.add(u)
            
            # 根ノード以外で low[v] >= disc[u]
            if parent.get(u) is not None and low[v] >= disc[u]:
                ap.add(u)
                
        elif v != parent.get(u):
            low[u] = min(low[u], disc[v])
```

#### 6.2.5 Step 4: SIコンポーネントの抽出

**抽出ルール**:

| LDグラフパターン | SIコンポーネント |
|-----------------|-----------------|
| Sy1 → Sy2 (Si1/Si2) | CND(Sy1, Sy2, Si1, Si2) |
| Sy1 ∧ Sy2 → SyO | COL(Sy1, Sy2) |
| Sy1 ∨ Sy2 → SyO | ALT(Sy1, Sy2) |
| Sy1 ⊕ Sy2 → SyO | EXO(Sy1, Sy2) |
| Sy1 → Sy2 (backup) | BUP(Sy1, Sy2) |

**疑似コード**:
```python
def extract_si_components(hierarchies):
    """LDグラフからSIコンポーネントを抽出"""
    si_graph = SIGraph()
    
    for level, subgraph in hierarchies.items():
        # 各階層レベルでSIコンポーネントを抽出
        for node in subgraph.get_nodes():
            # ノードの入力エッジを解析
            in_edges = subgraph.get_in_edges(node)
            
            if len(in_edges) == 0:
                # ルートノード
                si_graph.add_root(node, level)
                
            elif len(in_edges) == 1:
                edge = in_edges[0]
                # 単純な依存関係
                si_graph.add_dependency(edge.source, node, level)
                
            else:
                # 複数の入力 → 論理関係を判定
                logic = determine_logic(in_edges)
                
                if logic == "AND":
                    # Collaboration
                    si_component = COLComponent(
                        subsystems=[e.source for e in in_edges],
                        parent=node
                    )
                    si_graph.add_component(si_component, level)
                    
                elif logic == "OR":
                    # Alternative
                    si_component = ALTComponent(
                        subsystems=[e.source for e in in_edges],
                        parent=node
                    )
                    si_graph.add_component(si_component, level)
                    
                elif logic == "XOR":
                    # Exclusive
                    si_component = EXOComponent(
                        subsystems=[e.source for e in in_edges],
                        parent=node
                    )
                    si_graph.add_component(si_component, level)
            
            # 条件分岐のチェック
            if has_conditional_branch(subgraph, node):
                situations = extract_situations(subgraph, node)
                si_component = CNDComponent(
                    subsystems=get_subsystems(subgraph, node),
                    situations=situations,
                    parent=node
                )
                si_graph.add_component(si_component, level)
    
    return si_graph

def determine_logic(edges):
    """エッジの論理関係を判定"""
    logics = [e.logic for e in edges]
    
    if all(l == "AND" for l in logics):
        return "AND"
    elif all(l == "OR" for l in logics):
        return "OR"
    elif all(l == "XOR" for l in logics):
        return "XOR"
    else:
        # 混合の場合はデフォルトでOR
        return "OR"
```

#### 6.2.6 Step 5: 代替関係の解決

**解決ルール**:
1. ALTコンポーネントを特定
2. 設計者に選択を依頼
3. 未選択の選択肢をBUPに変換

**疑似コード**:
```python
def resolve_alternatives(si_graph, designer_input=None):
    """代替関係を解決"""
    alt_components = si_graph.find_components_by_type(ALTComponent)
    
    for alt in alt_components:
        if designer_input:
            # 設計者の選択を取得
            selected = designer_input.get_selection(alt)
        else:
            # インタラクティブに選択
            selected = interact_with_designer(
                "Select primary system from: {}".format(
                    alt.subsystems
                )
            )
        
        # 未選択をバックアップに変換
        remaining = [s for s in alt.subsystems if s != selected]
        
        if remaining:
            bup_component = BUPComponent(
                primary=selected,
                backups=remaining,
                parent=alt.parent
            )
            si_graph.replace_component(alt, bup_component)
    
    return si_graph
```

### 6.3 アルゴリズムの複雑性

| アルゴリズム | 時間複雑度 | 空間複雑度 |
|-------------|-----------|-----------|
| 設計探索 | O(n × m) | O(n) |
| DE→LD変換 | O(n) | O(n) |
| LDグラフ簡略化 | O(n + e) | O(n) |
| 連結成分計算 | O(n + e) | O(n) |
| 関節点発見 | O(n + e) | O(n) |
| SIコンポーネント抽出 | O(n × e) | O(n) |

**記号**:
- n: ノード数
- m: 設計探索のステップ数
- e: エッジ数

---

## 7. データ構造

### 7.1 コンポーネントクラス

#### 7.1.1 基底クラス

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from enum import Enum

class ComponentType(Enum):
    """コンポーネントタイプの列挙"""
    # DEコンポーネント
    SI = "SituationAssessment"
    PI = "ProblemIdentification"
    EI = "EstablishIntention"
    DI = "DecomposeIntention"
    CB = "ConditionalBranch"
    SA = "SolutionAssignment"
    
    # SIコンポーネント
    CND = "Condition"
    BUP = "Backups"
    COL = "Collaboration"
    ALT = "Alternative"
    EXO = "Exclusive"

class Port:
    """ポートクラス"""
    def __init__(self, name: str, data_type: type, direction: str):
        """
        Parameters:
            name: ポート名
            data_type: データ型
            direction: "input" or "output"
        """
        self.name = name
        self.data_type = data_type
        self.direction = direction
        self.connection = None  # 接続先
    
    def connect(self, other_port: 'Port'):
        """ポート接続"""
        self.connection = other_port
        other_port.connection = self

class Component(ABC):
    """コンポーネント基底クラス"""
    def __init__(self, component_id: str, component_type: ComponentType):
        self.id = component_id
        self.type = component_type
        self.input_ports: Dict[str, Port] = {}
        self.output_ports: Dict[str, Port] = {}
        self.metadata: Dict[str, Any] = {}
    
    def add_input_port(self, port: Port):
        """入力ポート追加"""
        self.input_ports[port.name] = port
    
    def add_output_port(self, port: Port):
        """出力ポート追加"""
        self.output_ports[port.name] = port
    
    @abstractmethod
    def execute(self) -> Any:
        """コンポーネントの実行（サブクラスで実装）"""
        pass
    
    @abstractmethod
    def to_ld_graph(self) -> 'LDNode':
        """LDグラフノードへの変換（サブクラスで実装）"""
        pass
    
    def __repr__(self):
        return f"{self.type.value}(id={self.id})"
```

#### 7.1.2 DEコンポーネントクラス

```python
class SIComponent(Component):
    """状況評価コンポーネント"""
    def __init__(self, component_id: str, system: Any, situation: Any = None):
        super().__init__(component_id, ComponentType.SI)
        self.system = system
        self.situation = situation
        
        # ポート定義
        self.add_input_port(Port("system", Any, "input"))
        self.add_output_port(Port("evaluated_system", tuple, "output"))
    
    def execute(self):
        """状況評価の実行"""
        return (self.system, self.situation)
    
    def to_ld_graph(self):
        """LDグラフノードへ変換"""
        return LDNode(
            node_id=f"{self.id}_ld",
            data=self.system,
            dependencies=[],
            logic=None
        )

class PIComponent(Component):
    """問題特定コンポーネント"""
    def __init__(self, component_id: str, system: Any, problem: Any = None):
        super().__init__(component_id, ComponentType.PI)
        self.system = system
        self.problem = problem
        
        self.add_input_port(Port("system", Any, "input"))
        self.add_output_port(Port("problem", Any, "output"))
    
    def execute(self):
        return self.problem
    
    def to_ld_graph(self):
        return LDNode(
            node_id=f"{self.id}_ld",
            data=self.system,
            dependencies=[],
            logic=None
        )

class EIComponent(Component):
    """意図確立コンポーネント"""
    def __init__(
        self, 
        component_id: str, 
        system: Any, 
        problem: Any, 
        intention: Any = None
    ):
        super().__init__(component_id, ComponentType.EI)
        self.system = system
        self.problem = problem
        self.intention = intention
        
        self.add_input_port(Port("system", Any, "input"))
        self.add_input_port(Port("problem", Any, "input"))
        self.add_output_port(Port("intention", Any, "output"))
    
    def execute(self):
        return self.intention
    
    def to_ld_graph(self):
        return LDNode(
            node_id=f"{self.id}_ld",
            data=(self.system, self.problem),
            dependencies=[],
            logic="AND"
        )

class DIComponent(Component):
    """意図分解コンポーネント"""
    def __init__(
        self, 
        component_id: str, 
        system: Any, 
        intention: Any,
        sub_intentions: List[Any] = None,
        sub_systems: List[Any] = None
    ):
        super().__init__(component_id, ComponentType.DI)
        self.system = system
        self.intention = intention
        self.sub_intentions = sub_intentions or []
        self.sub_systems = sub_systems or []
        
        self.add_input_port(Port("system", Any, "input"))
        self.add_input_port(Port("intention", Any, "input"))
        self.add_output_port(Port("sub_intentions", List, "output"))
        self.add_output_port(Port("sub_systems", List, "output"))
    
    def execute(self):
        return (self.sub_intentions, self.sub_systems)
    
    def to_ld_graph(self):
        source = (self.system, self.intention)
        targets = list(zip(self.sub_intentions, self.sub_systems))
        
        return LDNode(
            node_id=f"{self.id}_ld",
            data=source,
            dependencies=targets,
            logic="AND"
        )

class CBComponent(Component):
    """条件分岐コンポーネント"""
    def __init__(
        self, 
        component_id: str, 
        system: Any, 
        intention: Any,
        situation: Any
    ):
        super().__init__(component_id, ComponentType.CB)
        self.system = system
        self.intention = intention
        self.situation = situation
        
        self.add_input_port(Port("system", Any, "input"))
        self.add_input_port(Port("intention", Any, "input"))
        self.add_input_port(Port("situation", Any, "input"))
        self.add_output_port(Port("focused_intention", tuple, "output"))
    
    def execute(self):
        return (self.intention, self.situation)
    
    def to_ld_graph(self):
        return LDNode(
            node_id=f"{self.id}_ld",
            data=(self.intention, self.situation),
            dependencies=[(self.system, self.intention, self.situation)],
            logic=None
        )

class SAComponent(Component):
    """解決策割り当てコンポーネント"""
    def __init__(
        self, 
        component_id: str, 
        system: Any, 
        solution: Any,
        subsystem: Any = None
    ):
        super().__init__(component_id, ComponentType.SA)
        self.system = system
        self.solution = solution
        self.subsystem = subsystem
        
        self.add_input_port(Port("system", Any, "input"))
        self.add_input_port(Port("solution", Any, "input"))
        self.add_output_port(Port("subsystem", Any, "output"))
    
    def execute(self):
        return self.subsystem
    
    def to_ld_graph(self):
        return LDNode(
            node_id=f"{self.id}_ld",
            data=self.subsystem,
            dependencies=[(self.system, self.solution)],
            logic=None
        )
```

#### 7.1.3 SIコンポーネントクラス

```python
class SIComponent(Component):
    """SIコンポーネント基底クラス"""
    def __init__(self, component_id: str, component_type: ComponentType):
        super().__init__(component_id, component_type)
        self.subsystems: List[Any] = []
        self.parent: Any = None

class CNDComponent(SIComponent):
    """条件コンポーネント"""
    def __init__(
        self, 
        component_id: str,
        subsystems: List[Any],
        situations: List[Any],
        parent: Any
    ):
        super().__init__(component_id, ComponentType.CND)
        self.subsystems = subsystems
        self.situations = situations
        self.parent = parent
    
    def execute(self):
        """状況に応じたサブシステムの選択"""
        # 実際の実装では、現在の状況に基づいて選択
        pass
    
    def to_diagram(self):
        """ダイアグラム表現"""
        return {
            "type": "CND",
            "subsystems": self.subsystems,
            "situations": self.situations,
            "parent": self.parent
        }

class BUPComponent(SIComponent):
    """バックアップコンポーネント"""
    def __init__(
        self, 
        component_id: str,
        primary: Any,
        backups: List[Any],
        parent: Any
    ):
        super().__init__(component_id, ComponentType.BUP)
        self.primary = primary
        self.backups = backups
        self.parent = parent
    
    def execute(self):
        """プライマリまたはバックアップの選択"""
        # プライマリが利用可能ならそれを使用、そうでなければバックアップ
        pass
    
    def to_diagram(self):
        return {
            "type": "BUP",
            "primary": self.primary,
            "backups": self.backups,
            "parent": self.parent
        }

class COLComponent(SIComponent):
    """協調コンポーネント"""
    def __init__(
        self, 
        component_id: str,
        subsystems: List[Any],
        parent: Any
    ):
        super().__init__(component_id, ComponentType.COL)
        self.subsystems = subsystems
        self.parent = parent
    
    def execute(self):
        """全サブシステムの協調動作"""
        # 全サブシステムが協調して動作
        pass
    
    def to_diagram(self):
        return {
            "type": "COL",
            "subsystems": self.subsystems,
            "parent": self.parent
        }

class ALTComponent(SIComponent):
    """代替コンポーネント"""
    def __init__(
        self, 
        component_id: str,
        subsystems: List[Any],
        parent: Any
    ):
        super().__init__(component_id, ComponentType.ALT)
        self.subsystems = subsystems
        self.parent = parent
    
    def execute(self):
        """代替可能なサブシステムの選択"""
        # いずれか、または複数のサブシステムを選択
        pass
    
    def to_diagram(self):
        return {
            "type": "ALT",
            "subsystems": self.subsystems,
            "parent": self.parent
        }

class EXOComponent(SIComponent):
    """排他コンポーネント"""
    def __init__(
        self, 
        component_id: str,
        subsystems: List[Any],
        parent: Any
    ):
        super().__init__(component_id, ComponentType.EXO)
        self.subsystems = subsystems
        self.parent = parent
    
    def execute(self):
        """排他的なサブシステムの選択"""
        # いずれか1つのサブシステムのみを選択
        pass
    
    def to_diagram(self):
        return {
            "type": "EXO",
            "subsystems": self.subsystems,
            "parent": self.parent
        }
```

### 7.2 グラフクラス

#### 7.2.1 DEグラフクラス

```python
from typing import Dict, List, Set
import networkx as nx

class DEGraph:
    """設計探索グラフ"""
    def __init__(self):
        self.graph = nx.DiGraph()
        self.components: Dict[str, Component] = {}
        self.root_node = None
    
    def add_component(self, component: Component):
        """コンポーネント追加"""
        self.components[component.id] = component
        self.graph.add_node(component.id, component=component)
    
    def add_edge(self, source_id: str, target_id: str, **attributes):
        """エッジ追加"""
        self.graph.add_edge(source_id, target_id, **attributes)
    
    def get_component(self, component_id: str) -> Component:
        """コンポーネント取得"""
        return self.components.get(component_id)
    
    def get_successors(self, component_id: str) -> List[str]:
        """後続ノード取得"""
        return list(self.graph.successors(component_id))
    
    def get_predecessors(self, component_id: str) -> List[str]:
        """先行ノード取得"""
        return list(self.graph.predecessors(component_id))
    
    def traverse_dfs(self, start_id: str = None) -> List[Component]:
        """深さ優先探索"""
        if start_id is None:
            start_id = self.root_node
        
        visited = []
        stack = [start_id]
        seen = set()
        
        while stack:
            node_id = stack.pop()
            if node_id in seen:
                continue
            
            seen.add(node_id)
            visited.append(self.components[node_id])
            
            # 後続ノードをスタックに追加
            for successor in self.get_successors(node_id):
                if successor not in seen:
                    stack.append(successor)
        
        return visited
    
    def to_dict(self) -> Dict:
        """辞書形式に変換"""
        return {
            "nodes": [
                {
                    "id": comp.id,
                    "type": comp.type.value,
                    "data": comp.metadata
                }
                for comp in self.components.values()
            ],
            "edges": [
                {
                    "source": u,
                    "target": v,
                    "attributes": data
                }
                for u, v, data in self.graph.edges(data=True)
            ]
        }
    
    def visualize(self, output_path: str = None):
        """グラフ可視化"""
        import matplotlib.pyplot as plt
        
        pos = nx.spring_layout(self.graph)
        
        # ノードの描画
        nx.draw_networkx_nodes(
            self.graph, 
            pos, 
            node_color='lightblue',
            node_size=1000
        )
        
        # エッジの描画
        nx.draw_networkx_edges(
            self.graph, 
            pos, 
            arrows=True,
            arrowsize=20
        )
        
        # ラベルの描画
        labels = {
            node: self.components[node].type.value[:3]
            for node in self.graph.nodes()
        }
        nx.draw_networkx_labels(self.graph, pos, labels)
        
        if output_path:
            plt.savefig(output_path)
        else:
            plt.show()
```

#### 7.2.2 LDグラフクラス

```python
class LDNode:
    """LDグラフノード"""
    def __init__(
        self, 
        node_id: str, 
        data: Any, 
        dependencies: List[Any] = None,
        logic: str = None
    ):
        self.id = node_id
        self.data = data
        self.dependencies = dependencies or []
        self.logic = logic  # "AND", "OR", "XOR", None
    
    def __repr__(self):
        return f"LDNode(id={self.id}, data={self.data}, logic={self.logic})"

class LDGraph:
    """論理依存グラフ"""
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes: Dict[str, LDNode] = {}
    
    def add_node(self, node: LDNode):
        """ノード追加"""
        self.nodes[node.id] = node
        self.graph.add_node(node.id, node=node)
    
    def add_edge(
        self, 
        source_id: str, 
        target_id: str, 
        logic: str = None
    ):
        """エッジ追加"""
        self.graph.add_edge(source_id, target_id, logic=logic)
    
    def simplify(self) -> 'LDGraph':
        """グラフ簡略化"""
        simplified = LDGraph()
        
        # System と Situation ノードのみを抽出
        for node_id, node in self.nodes.items():
            if self._is_system_or_situation(node):
                simplified.add_node(node)
        
        # エッジを再構築
        for u, v, data in self.graph.edges(data=True):
            if u in simplified.nodes and v in simplified.nodes:
                simplified.add_edge(u, v, data.get('logic'))
        
        return simplified
    
    def _is_system_or_situation(self, node: LDNode) -> bool:
        """System または Situation ノードか判定"""
        # 実装では、ノードのデータ型をチェック
        return True  # 簡略化のため、常に True
    
    def find_connected_components(self) -> List[Set[str]]:
        """連結成分を発見"""
        return list(nx.weakly_connected_components(self.graph))
    
    def find_articulation_points(self) -> Set[str]:
        """関節点を発見"""
        # 無向グラフに変換
        undirected = self.graph.to_undirected()
        return set(nx.articulation_points(undirected))
    
    def split_at_articulation_points(
        self, 
        articulation_points: Set[str]
    ) -> List['LDGraph']:
        """関節点で分割"""
        # 関節点を削除したグラフを作成
        temp_graph = self.graph.copy()
        temp_graph.remove_nodes_from(articulation_points)
        
        # 連結成分ごとにサブグラフを作成
        components = list(nx.weakly_connected_components(temp_graph))
        subgraphs = []
        
        for component in components:
            subgraph = LDGraph()
            for node_id in component:
                subgraph.add_node(self.nodes[node_id])
            
            for u, v, data in self.graph.edges(data=True):
                if u in component and v in component:
                    subgraph.add_edge(u, v, data.get('logic'))
            
            subgraphs.append(subgraph)
        
        return subgraphs
    
    def to_dict(self) -> Dict:
        """辞書形式に変換"""
        return {
            "nodes": [
                {"id": node.id, "data": str(node.data), "logic": node.logic}
                for node in self.nodes.values()
            ],
            "edges": [
                {"source": u, "target": v, "logic": data.get('logic')}
                for u, v, data in self.graph.edges(data=True)
            ]
        }
```

#### 7.2.3 SIグラフクラス

```python
class SIGraph:
    """システム統合グラフ"""
    def __init__(self):
        self.graph = nx.DiGraph()
        self.components: Dict[str, SIComponent] = {}
        self.hierarchies: Dict[str, List[str]] = {}  # レベル → ノードリスト
    
    def add_component(self, component: SIComponent, level: str):
        """SIコンポーネント追加"""
        self.components[component.id] = component
        self.graph.add_node(component.id, component=component, level=level)
        
        if level not in self.hierarchies:
            self.hierarchies[level] = []
        self.hierarchies[level].append(component.id)
    
    def add_edge(
        self, 
        source_id: str, 
        target_id: str, 
        relationship: str = None
    ):
        """エッジ追加"""
        self.graph.add_edge(source_id, target_id, relationship=relationship)
    
    def get_level(self, component_id: str) -> str:
        """コンポーネントの階層レベルを取得"""
        return self.graph.nodes[component_id]['level']
    
    def get_components_at_level(self, level: str) -> List[SIComponent]:
        """特定レベルのコンポーネント取得"""
        component_ids = self.hierarchies.get(level, [])
        return [self.components[cid] for cid in component_ids]
    
    def find_components_by_type(
        self, 
        component_type: type
    ) -> List[SIComponent]:
        """タイプでコンポーネントを検索"""
        return [
            comp for comp in self.components.values()
            if isinstance(comp, component_type)
        ]
    
    def replace_component(
        self, 
        old_component: SIComponent, 
        new_component: SIComponent
    ):
        """コンポーネント置換"""
        old_id = old_component.id
        level = self.get_level(old_id)
        
        # 古いコンポーネントを削除
        self.graph.remove_node(old_id)
        del self.components[old_id]
        self.hierarchies[level].remove(old_id)
        
        # 新しいコンポーネントを追加
        self.add_component(new_component, level)
        
        # エッジを再接続（必要に応じて）
        # ...
    
    def to_hierarchical_dict(self) -> Dict:
        """階層構造を辞書形式に変換"""
        result = {}
        
        for level in sorted(self.hierarchies.keys()):
            result[level] = [
                {
                    "id": comp.id,
                    "type": comp.type.value,
                    "subsystems": [
                        str(s) for s in comp.subsystems
                    ],
                    "parent": str(comp.parent)
                }
                for comp in self.get_components_at_level(level)
            ]
        
        return result
    
    def visualize_hierarchy(self, output_path: str = None):
        """階層構造を可視化"""
        import matplotlib.pyplot as plt
        
        # 階層レイアウトの計算
        pos = nx.multipartite_layout(
            self.graph, 
            subset_key='level'
        )
        
        # レベルごとに色分け
        colors = []
        for node in self.graph.nodes():
            level = self.get_level(node)
            level_num = int(level.split('_')[1])
            colors.append(plt.cm.viridis(level_num / len(self.hierarchies)))
        
        nx.draw_networkx_nodes(
            self.graph, 
            pos, 
            node_color=colors,
            node_size=1000
        )
        
        nx.draw_networkx_edges(
            self.graph, 
            pos, 
            arrows=True,
            arrowsize=20
        )
        
        labels = {
            node: self.components[node].type.value[:3]
            for node in self.graph.nodes()
        }
        nx.draw_networkx_labels(self.graph, pos, labels)
        
        if output_path:
            plt.savefig(output_path)
        else:
            plt.show()
```

### 7.3 知識ベースクラス

```python
class KnowledgeBase:
    """知識ベース"""
    def __init__(self, domain: str):
        self.domain = domain
        self.situations: Dict[str, List[str]] = {}
        self.problems: Dict[str, List[str]] = {}
        self.intentions: Dict[str, str] = {}
        self.solutions: Dict[str, List[str]] = {}
        self.decompositions: Dict[str, Dict] = {}
    
    def register_situation(self, system: str, situation: str):
        """状況の登録"""
        if system not in self.situations:
            self.situations[system] = []
        self.situations[system].append(situation)
    
    def register_problem(self, system_situation: str, problem: str):
        """問題の登録"""
        if system_situation not in self.problems:
            self.problems[system_situation] = []
        self.problems[system_situation].append(problem)
    
    def register_intention(self, problem: str, intention: str):
        """意図の登録"""
        self.intentions[problem] = intention
    
    def register_solution(self, intention: str, solution: str):
        """解決策の登録"""
        if intention not in self.solutions:
            self.solutions[intention] = []
        self.solutions[intention].append(solution)
    
    def register_decomposition(
        self, 
        intention: str, 
        sub_intentions: List[str],
        sub_systems: List[str]
    ):
        """分解方法の登録"""
        self.decompositions[intention] = {
            "sub_intentions": sub_intentions,
            "sub_systems": sub_systems
        }
    
    def query_situation(self, system: str) -> List[str]:
        """状況の問い合わせ"""
        return self.situations.get(system, [])
    
    def query_problem(self, system_situation: str) -> List[str]:
        """問題の問い合わせ"""
        return self.problems.get(system_situation, [])
    
    def query_intention(self, problem: str) -> str:
        """意図の問い合わせ"""
        return self.intentions.get(problem)
    
    def query_solutions(self, intention: str) -> List[str]:
        """解決策の問い合わせ"""
        return self.solutions.get(intention, [])
    
    def query_decomposition(self, intention: str) -> Dict:
        """分解方法の問い合わせ"""
        return self.decompositions.get(intention, {})
    
    def to_dict(self) -> Dict:
        """辞書形式に変換"""
        return {
            "domain": self.domain,
            "situations": self.situations,
            "problems": self.problems,
            "intentions": self.intentions,
            "solutions": self.solutions,
            "decompositions": self.decompositions
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'KnowledgeBase':
        """辞書から知識ベースを生成"""
        kb = cls(data["domain"])
        kb.situations = data["situations"]
        kb.problems = data["problems"]
        kb.intentions = data["intentions"]
        kb.solutions = data["solutions"]
        kb.decompositions = data["decompositions"]
        return kb
```

---

## 8. API仕様

### 8.1 REST API

#### 8.1.1 エンドポイント一覧

| エンドポイント | メソッド | 説明 |
|--------------|---------|------|
| `/api/design/sessions` | POST | 設計セッション開始 |
| `/api/design/sessions/{id}` | GET | セッション情報取得 |
| `/api/design/sessions/{id}` | DELETE | セッション終了 |
| `/api/design/explore` | POST | 設計探索実行 |
| `/api/design/de-graph` | GET | DEグラフ取得 |
| `/api/design/convert` | POST | グラフ変換実行 |
| `/api/design/si-graph` | GET | SIグラフ取得 |
| `/api/kb/query` | POST | 知識ベース問い合わせ |
| `/api/kb/register` | POST | 知識ベース登録 |

#### 8.1.2 API詳細

**1. 設計セッション開始**

```http
POST /api/design/sessions
Content-Type: application/json

Request:
{
  "domain": "vehicle_control",
  "initial_system": "car_running",
  "designer_id": "user123"
}

Response: 200 OK
{
  "session_id": "sess_abc123",
  "status": "initialized",
  "created_at": "2025-11-17T10:00:00Z"
}
```

**2. 設計探索実行**

```http
POST /api/design/explore
Content-Type: application/json

Request:
{
  "session_id": "sess_abc123",
  "action": "assess_situation",
  "parameters": {
    "system": "car_running",
    "situation": "obstacle_on_road"
  }
}

Response: 200 OK
{
  "component_id": "si_001",
  "component_type": "SituationAssessment",
  "result": {
    "system": "car_running",
    "situation": "obstacle_on_road"
  },
  "next_actions": [
    "identify_problem",
    "assess_side_effect"
  ]
}
```

**3. DEグラフ取得**

```http
GET /api/design/de-graph?session_id=sess_abc123
Accept: application/json

Response: 200 OK
{
  "session_id": "sess_abc123",
  "graph": {
    "nodes": [
      {
        "id": "si_001",
        "type": "SituationAssessment",
        "data": {
          "system": "car_running",
          "situation": "obstacle_on_road"
        }
      },
      {
        "id": "pi_001",
        "type": "ProblemIdentification",
        "data": {
          "problem": "collision_risk"
        }
      }
    ],
    "edges": [
      {
        "source": "si_001",
        "target": "pi_001"
      }
    ]
  }
}
```

**4. グラフ変換実行**

```http
POST /api/design/convert
Content-Type: application/json

Request:
{
  "session_id": "sess_abc123",
  "source_graph_type": "de_graph",
  "target_graph_type": "si_graph"
}

Response: 200 OK
{
  "conversion_id": "conv_xyz789",
  "status": "completed",
  "si_graph_id": "sig_def456"
}
```

**5. SIグラフ取得**

```http
GET /api/design/si-graph?graph_id=sig_def456
Accept: application/json

Response: 200 OK
{
  "graph_id": "sig_def456",
  "hierarchies": {
    "Level_0": [
      {
        "id": "sys_lvl1",
        "type": "Condition",
        "subsystems": ["sys_auto", "sys_human"],
        "situations": ["normal", "low_visibility"]
      }
    ],
    "Level_1": [
      {
        "id": "sys_auto",
        "type": "System",
        "description": "Auto maneuvering system"
      },
      {
        "id": "sys_human",
        "type": "Condition",
        "subsystems": ["sys_alarm", "sys_guide"],
        "situations": ["low_visibility"]
      }
    ]
  }
}
```

**6. 知識ベース問い合わせ**

```http
POST /api/kb/query
Content-Type: application/json

Request:
{
  "query_type": "problem",
  "parameters": {
    "system": "car_running",
    "situation": "obstacle_on_road"
  }
}

Response: 200 OK
{
  "results": [
    {
      "problem": "collision_risk",
      "confidence": 0.95
    }
  ]
}
```

### 8.2 Python SDK

```python
from cdss import DesignSession, KnowledgeBase, Visualizer

# セッション初期化
session = DesignSession(
    domain="vehicle_control",
    initial_system="car_running"
)

# 知識ベース設定
kb = KnowledgeBase.load("vehicle_control_kb.json")
session.set_knowledge_base(kb)

# 設計探索
result = session.assess_situation("obstacle_on_road")
problem = session.identify_problem()
intention = session.establish_intention(problem)

# DEグラフ取得
de_graph = session.get_de_graph()

# グラフ変換
si_graph = session.convert_to_si_graph()

# 可視化
visualizer = Visualizer()
visualizer.plot_de_graph(de_graph, "de_graph.png")
visualizer.plot_si_graph(si_graph, "si_graph.png")
```

---

## 9. ユースケース

### 9.1 車両衝突回避システムの設計

**目的**: 車両が走行中に障害物に衝突することを回避するシステムの概念設計

**設計探索プロセス**:

```
1. 初期システム: 「車が走行中」(Fact)

2. 状況評価 (SI)
   入力: 「車が走行中」
   出力: 「道路上に障害物」

3. 副作用評価
   入力: 「車が走行中」+ 「道路上に障害物」
   出力: 「衝突の可能性」

4. 問題特定 (PI)
   入力: 「衝突の可能性」
   出力: 問題「衝突」

5. 意図確立 (EI)
   入力: 「衝突」
   出力: 意図「衝突を回避するシステム」

6. 解決策探索 (Searching)
   入力: 「衝突を回避するシステム」
   出力: 2つの代替案
     - 「車による操縦」
     - 「運転者による操縦」

7. 意図分解 (DI)
   入力: 「衝突を回避するシステム」
   出力:
     - サブ意図1: 「車による回避」→ サブシステム1: 「自動操縦システム」
     - サブ意図2: 「運転者による回避」→ サブシステム2: 「人間操縦システム」

8. サブシステム2のさらなる探索
   8.1 状況評価 (SI)
       入力: 「人間操縦システム」
       出力: 「視界不良（霧、嵐）」

   8.2 副作用評価
       入力: 「人間操縦システム」+ 「視界不良」
       出力: 「衝突の可能性」

   8.3 問題特定 (PI)
       入力: 「衝突の可能性」
       出力: 問題「衝突」

   8.4 意図確立 (EI)
       入力: 「衝突」
       出力: 意図「視界不良時でも運転者が操縦できるシステム」

   8.5 解決策探索 (Searching)
       入力: 「視界不良時でも運転者が操縦できるシステム」
       出力: 2つの代替案
         - 「障害物警報」
         - 「操縦誘導」

   8.6 解決策適用 (SA)
       入力: 「障害物警報」
       出力: サブシステム3: 「障害物警報システム」

   8.7 解決策適用 (SA)
       入力: 「操縦誘導」
       出力: サブシステム4: 「操縦誘導システム」

最終結果: 4つのサブシステム
  - SubSystem1: 自動操縦システム
  - SubSystem2: 人間操縦システム
  - SubSystem3: 障害物警報システム
  - SubSystem4: 操縦誘導システム
```

**DEグラフ**:

```
car_running (Fact)
      │
      ▼
    (SI) ─── obstacle
      │
      ▼
car_running + crash (副作用)
      │
      ▼
    (PI) ─── crash
      │
      ▼
    (EI) ─── prevent_crash
      │
      ▼
    (DI)
    ┌─┴─┐
    │   │
  by_car  by_driver
    │        │
    ▼        ▼
(SA)    ┌────────┐
 │      │  (SI)  │── low_visibility
 │      └───┬────┘
 │          │
 │          ▼
 │      car_running + crash
 │          │
 │          ▼
 │        (PI) ─── crash
 │          │
 │          ▼
 │        (EI) ─── maneuver_under_low_vis
 │          │
 │          ▼
 │     ┌────┴────┐
 │     │         │
 │   by_alarm  by_guide
 │     │         │
 │     ▼         ▼
 │   (SA)      (SA)
 │     │         │
 ▼     ▼         ▼
SubSys1 SubSys3  SubSys4
(auto)  (alarm)  (guide)
```

**グラフ変換プロセス**:

1. **DEグラフ → LDグラフ**:
```
car_running
     │
     ▼
  obstacle
     │
     ▼
car_crashing
     │
  ┌──┴──┐
  │     │
by_car  by_driver
  │       │
  │    ┌──▼─────┐
  │    │low_vis.│
  │    └───┬────┘
  │        │
  │    ┌───▼──┐
  │    │crash │
  │    └───┬──┘
  │     ┌──┴───┐
  │     │      │
  │  by_alarm by_guide
  │     │      │
  ▼     ▼      ▼
SubSys1 SubSys3 SubSys4
```

2. **階層抽出**:
```
Level 0: car_crashing
           │
Level 1:   ├── by_car → SubSys1
           └── by_driver
                 │
Level 2:         ├── SubSys3
                 └── SubSys4
```

3. **SIコンポーネント抽出**:
```
Level 0: SysLvl1 (Collision Avoidance)
           │
         [CND] (obstacle / normal)
           │
      ┌────┴────┐
Level 1: SubSys1  SysLvl2
        (Auto)    (Human)
                    │
                  [CND] (low_visibility)
                    │
               ┌────┴────┐
Level 2:    SubSys3    SubSys4
           (Alarm)    (Guide)
                  │
                 [BUP]
```

**最終SIグラフ**:

```
                 ┌──────────────────┐
                 │    SysLvl1       │
                 │ (Collision       │
                 │  Avoidance)      │
                 └─────────┬────────┘
                           │
                   ┌───────▼───────┐
                   │      CND      │
                   │ (obstacle/    │
                   │  normal)      │
                   └───┬───────┬───┘
                       │       │
          ┌────────────▼┐   ┌─▼──────────┐
          │   SubSys1   │   │  SysLvl2   │
          │   (Auto     │   │  (Human    │
          │  Maneuver)  │   │  Maneuver) │
          └─────────────┘   └─────┬──────┘
                                  │
                        ┌─────────▼─────────┐
                        │       CND         │
                        │  (low_visibility) │
                        └────┬─────────┬────┘
                             │         │
                    ┌────────▼──┐  ┌──▼────────┐
                    │ SubSys3   │  │ SubSys4   │
                    │ (Obstacle │  │ (Maneuver │
                    │  Alarm)   │  │  Guide)   │
                    └─────┬─────┘  └─────┬─────┘
                          │              │
                          └──────┬───────┘
                                 │
                             ┌───▼───┐
                             │  BUP  │
                             └───────┘
```

### 9.2 実装例（Python）

```python
# 設計セッション開始
session = DesignSession(
    domain="vehicle_control",
    initial_system="car_running"
)

# 知識ベース読み込み
kb = KnowledgeBase.load("vehicle_kb.json")
session.set_knowledge_base(kb)

# 設計探索
# Step 1: 状況評価
si_comp = session.assess_situation("obstacle_on_road")
print(f"Situation: {si_comp.situation}")

# Step 2: 問題特定
pi_comp = session.identify_problem()
print(f"Problem: {pi_comp.problem}")

# Step 3: 意図確立
ei_comp = session.establish_intention(pi_comp.problem)
print(f"Intention: {ei_comp.intention}")

# Step 4: 意図分解
di_comp = session.decompose_intention(ei_comp.intention)
print(f"Sub-intentions: {di_comp.sub_intentions}")
print(f"Sub-systems: {di_comp.sub_systems}")

# サブシステムごとの探索（再帰的）
for sub_sys in di_comp.sub_systems:
    if sub_sys == "human_maneuvering":
        # 人間操縦システムをさらに探索
        sub_session = session.create_sub_session(sub_sys)
        
        si_comp2 = sub_session.assess_situation("low_visibility")
        pi_comp2 = sub_session.identify_problem()
        ei_comp2 = sub_session.establish_intention(pi_comp2.problem)
        
        solutions = sub_session.search_solutions(ei_comp2.intention)
        for sol in solutions:
            sa_comp = sub_session.apply_solution(sol)
            print(f"Sub-system created: {sa_comp.subsystem}")

# DEグラフ取得
de_graph = session.get_de_graph()
de_graph.visualize("vehicle_de_graph.png")

# グラフ変換
converter = GraphConverter()
ld_graph = converter.de_to_ld(de_graph)
simplified = ld_graph.simplify()
hierarchies = converter.extract_hierarchies(simplified)
si_graph = converter.ld_to_si(hierarchies)

# 代替関係の解決
si_graph = converter.resolve_alternatives(si_graph)

# 可視化
si_graph.visualize_hierarchy("vehicle_si_graph.png")

# 結果保存
session.save_results("vehicle_design.json")
```

---

## 10. テストケース

### 10.1 単体テスト

#### 10.1.1 DEコンポーネントのテスト

**テストケース: SIComponent（状況評価）**

```python
import unittest
from cdss.components import SIComponent

class TestSIComponent(unittest.TestCase):
    """SIコンポーネントの単体テスト"""
    
    def setUp(self):
        """テストの初期化"""
        self.system = "car_running"
        self.situation = "obstacle_on_road"
    
    def test_si_component_creation(self):
        """SIコンポーネントの生成テスト"""
        si_comp = SIComponent(
            component_id="si_test_001",
            system=self.system,
            situation=self.situation
        )
        
        self.assertEqual(si_comp.system, self.system)
        self.assertEqual(si_comp.situation, self.situation)
        self.assertEqual(si_comp.type, ComponentType.SI)
    
    def test_si_component_execution(self):
        """SIコンポーネントの実行テスト"""
        si_comp = SIComponent(
            component_id="si_test_002",
            system=self.system,
            situation=self.situation
        )
        
        result = si_comp.execute()
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, (self.system, self.situation))
    
    def test_si_component_ld_conversion(self):
        """LDグラフへの変換テスト"""
        si_comp = SIComponent(
            component_id="si_test_003",
            system=self.system,
            situation=self.situation
        )
        
        ld_node = si_comp.to_ld_graph()
        self.assertIsInstance(ld_node, LDNode)
        self.assertEqual(ld_node.data, self.system)
    
    def test_si_component_ports(self):
        """ポートの接続テスト"""
        si_comp = SIComponent(
            component_id="si_test_004",
            system=self.system,
            situation=self.situation
        )
        
        # 入力ポートの確認
        self.assertIn("system", si_comp.input_ports)
        
        # 出力ポートの確認
        self.assertIn("evaluated_system", si_comp.output_ports)
```

**テストケース: DIComponent（意図分解）**

```python
class TestDIComponent(unittest.TestCase):
    """DIコンポーネントの単体テスト"""
    
    def setUp(self):
        """テストの初期化"""
        self.system = "collision_avoidance"
        self.intention = "prevent_crash"
        self.sub_intentions = ["by_car", "by_driver"]
        self.sub_systems = ["auto_maneuver", "human_maneuver"]
    
    def test_di_component_creation(self):
        """DIコンポーネントの生成テスト"""
        di_comp = DIComponent(
            component_id="di_test_001",
            system=self.system,
            intention=self.intention,
            sub_intentions=self.sub_intentions,
            sub_systems=self.sub_systems
        )
        
        self.assertEqual(di_comp.system, self.system)
        self.assertEqual(di_comp.intention, self.intention)
        self.assertEqual(len(di_comp.sub_intentions), 2)
        self.assertEqual(len(di_comp.sub_systems), 2)
    
    def test_di_component_execution(self):
        """DIコンポーネントの実行テスト"""
        di_comp = DIComponent(
            component_id="di_test_002",
            system=self.system,
            intention=self.intention,
            sub_intentions=self.sub_intentions,
            sub_systems=self.sub_systems
        )
        
        result = di_comp.execute()
        self.assertIsInstance(result, tuple)
        self.assertEqual(result[0], self.sub_intentions)
        self.assertEqual(result[1], self.sub_systems)
    
    def test_di_component_ld_conversion(self):
        """LDグラフへの変換テスト"""
        di_comp = DIComponent(
            component_id="di_test_003",
            system=self.system,
            intention=self.intention,
            sub_intentions=self.sub_intentions,
            sub_systems=self.sub_systems
        )
        
        ld_node = di_comp.to_ld_graph()
        self.assertEqual(ld_node.logic, "AND")
        self.assertEqual(len(ld_node.dependencies), 2)
```

#### 10.1.2 SIコンポーネントのテスト

**テストケース: CNDComponent（条件）**

```python
class TestCNDComponent(unittest.TestCase):
    """CNDコンポーネントの単体テスト"""
    
    def setUp(self):
        """テストの初期化"""
        self.subsystems = ["auto_maneuver", "human_maneuver"]
        self.situations = ["normal", "special"]
        self.parent = "collision_avoidance"
    
    def test_cnd_component_creation(self):
        """CNDコンポーネントの生成テスト"""
        cnd_comp = CNDComponent(
            component_id="cnd_test_001",
            subsystems=self.subsystems,
            situations=self.situations,
            parent=self.parent
        )
        
        self.assertEqual(len(cnd_comp.subsystems), 2)
        self.assertEqual(len(cnd_comp.situations), 2)
        self.assertEqual(cnd_comp.parent, self.parent)
    
    def test_cnd_component_diagram(self):
        """ダイアグラム表現のテスト"""
        cnd_comp = CNDComponent(
            component_id="cnd_test_002",
            subsystems=self.subsystems,
            situations=self.situations,
            parent=self.parent
        )
        
        diagram = cnd_comp.to_diagram()
        self.assertEqual(diagram["type"], "CND")
        self.assertIn("subsystems", diagram)
        self.assertIn("situations", diagram)
```

#### 10.1.3 グラフ構造のテスト

**テストケース: DEGraph**

```python
class TestDEGraph(unittest.TestCase):
    """DEグラフの単体テスト"""
    
    def setUp(self):
        """テストの初期化"""
        self.de_graph = DEGraph()
    
    def test_add_component(self):
        """コンポーネント追加のテスト"""
        si_comp = SIComponent(
            component_id="si_001",
            system="test_system",
            situation="test_situation"
        )
        
        self.de_graph.add_component(si_comp)
        self.assertIn("si_001", self.de_graph.components)
    
    def test_add_edge(self):
        """エッジ追加のテスト"""
        si_comp = SIComponent("si_001", "sys1", "sit1")
        pi_comp = PIComponent("pi_001", "sys1", "prob1")
        
        self.de_graph.add_component(si_comp)
        self.de_graph.add_component(pi_comp)
        self.de_graph.add_edge("si_001", "pi_001")
        
        successors = self.de_graph.get_successors("si_001")
        self.assertIn("pi_001", successors)
    
    def test_traverse_dfs(self):
        """深さ優先探索のテスト"""
        # グラフ構築
        si_comp = SIComponent("si_001", "sys1", "sit1")
        pi_comp = PIComponent("pi_001", "sys1", "prob1")
        ei_comp = EIComponent("ei_001", "sys1", "prob1", "int1")
        
        self.de_graph.add_component(si_comp)
        self.de_graph.add_component(pi_comp)
        self.de_graph.add_component(ei_comp)
        
        self.de_graph.add_edge("si_001", "pi_001")
        self.de_graph.add_edge("pi_001", "ei_001")
        
        self.de_graph.root_node = "si_001"
        
        # DFS実行
        visited = self.de_graph.traverse_dfs()
        self.assertEqual(len(visited), 3)
    
    def test_to_dict(self):
        """辞書変換のテスト"""
        si_comp = SIComponent("si_001", "sys1", "sit1")
        self.de_graph.add_component(si_comp)
        
        graph_dict = self.de_graph.to_dict()
        self.assertIn("nodes", graph_dict)
        self.assertIn("edges", graph_dict)
        self.assertEqual(len(graph_dict["nodes"]), 1)
```

### 10.2 統合テスト

#### 10.2.1 設計探索フロー全体のテスト

```python
class TestDesignExplorationFlow(unittest.TestCase):
    """設計探索フロー全体の統合テスト"""
    
    def setUp(self):
        """テストの初期化"""
        # 知識ベースの準備
        self.kb = KnowledgeBase("test_domain")
        self.kb.register_situation("car_running", "obstacle_on_road")
        self.kb.register_problem("car_running+obstacle", "collision")
        self.kb.register_intention("collision", "prevent_crash")
        self.kb.register_solution("prevent_crash", "auto_maneuver")
        
        # セッション初期化
        self.session = DesignSession(
            domain="test_domain",
            initial_system="car_running"
        )
        self.session.set_knowledge_base(self.kb)
    
    def test_full_exploration_flow(self):
        """完全な設計探索フローのテスト"""
        # Step 1: 状況評価
        si_result = self.session.assess_situation()
        self.assertIsNotNone(si_result)
        self.assertEqual(si_result.situation, "obstacle_on_road")
        
        # Step 2: 問題特定
        pi_result = self.session.identify_problem()
        self.assertIsNotNone(pi_result)
        self.assertEqual(pi_result.problem, "collision")
        
        # Step 3: 意図確立
        ei_result = self.session.establish_intention(pi_result.problem)
        self.assertIsNotNone(ei_result)
        self.assertEqual(ei_result.intention, "prevent_crash")
        
        # Step 4: 解決策適用
        sa_result = self.session.apply_solution("auto_maneuver")
        self.assertIsNotNone(sa_result)
        
        # DEグラフの検証
        de_graph = self.session.get_de_graph()
        self.assertGreaterEqual(len(de_graph.components), 4)
    
    def test_de_graph_structure(self):
        """DEグラフ構造の検証"""
        # 設計探索実行
        self.session.assess_situation()
        self.session.identify_problem()
        self.session.establish_intention("collision")
        self.session.apply_solution("auto_maneuver")
        
        de_graph = self.session.get_de_graph()
        
        # ノード数の確認
        self.assertEqual(len(de_graph.components), 4)
        
        # エッジの確認
        edges = list(de_graph.graph.edges())
        self.assertGreater(len(edges), 0)
```

#### 10.2.2 グラフ変換プロセス全体のテスト

```python
class TestGraphConversionFlow(unittest.TestCase):
    """グラフ変換プロセス全体の統合テスト"""
    
    def setUp(self):
        """テストの初期化"""
        # サンプルDEグラフの構築
        self.de_graph = self._create_sample_de_graph()
        self.converter = GraphConverter()
    
    def _create_sample_de_graph(self):
        """サンプルDEグラフの作成"""
        de_graph = DEGraph()
        
        si_comp = SIComponent("si_001", "car_running", "obstacle")
        pi_comp = PIComponent("pi_001", "car_running", "collision")
        ei_comp = EIComponent("ei_001", "car_running", "collision", "prevent")
        sa_comp = SAComponent("sa_001", "car_running", "auto", "auto_sys")
        
        de_graph.add_component(si_comp)
        de_graph.add_component(pi_comp)
        de_graph.add_component(ei_comp)
        de_graph.add_component(sa_comp)
        
        de_graph.add_edge("si_001", "pi_001")
        de_graph.add_edge("pi_001", "ei_001")
        de_graph.add_edge("ei_001", "sa_001")
        
        return de_graph
    
    def test_de_to_ld_conversion(self):
        """DE→LD変換のテスト"""
        ld_graph = self.converter.de_to_ld(self.de_graph)
        
        self.assertIsInstance(ld_graph, LDGraph)
        self.assertGreater(len(ld_graph.nodes), 0)
    
    def test_ld_simplification(self):
        """LDグラフ簡略化のテスト"""
        ld_graph = self.converter.de_to_ld(self.de_graph)
        simplified = ld_graph.simplify()
        
        self.assertIsInstance(simplified, LDGraph)
        # 簡略化後のノード数は元より少ないか同じ
        self.assertLessEqual(len(simplified.nodes), len(ld_graph.nodes))
    
    def test_hierarchy_extraction(self):
        """階層抽出のテスト"""
        ld_graph = self.converter.de_to_ld(self.de_graph)
        simplified = ld_graph.simplify()
        hierarchies = self.converter.extract_hierarchies(simplified)
        
        self.assertIsInstance(hierarchies, dict)
        self.assertGreater(len(hierarchies), 0)
    
    def test_si_component_extraction(self):
        """SIコンポーネント抽出のテスト"""
        ld_graph = self.converter.de_to_ld(self.de_graph)
        simplified = ld_graph.simplify()
        hierarchies = self.converter.extract_hierarchies(simplified)
        si_graph = self.converter.ld_to_si(hierarchies)
        
        self.assertIsInstance(si_graph, SIGraph)
        self.assertGreater(len(si_graph.components), 0)
    
    def test_full_conversion_pipeline(self):
        """完全な変換パイプラインのテスト"""
        # Step 1: DE → LD
        ld_graph = self.converter.de_to_ld(self.de_graph)
        
        # Step 2: Simplify
        simplified = ld_graph.simplify()
        
        # Step 3: Extract Hierarchies
        hierarchies = self.converter.extract_hierarchies(simplified)
        
        # Step 4: LD → SI
        si_graph = self.converter.ld_to_si(hierarchies)
        
        # Step 5: Resolve Alternatives
        final_si_graph = self.converter.resolve_alternatives(si_graph)
        
        # 検証
        self.assertIsInstance(final_si_graph, SIGraph)
        self.assertGreater(len(final_si_graph.components), 0)
        self.assertGreater(len(final_si_graph.hierarchies), 0)
```

### 10.3 エンドツーエンドテスト

#### 10.3.1 車両制御システムの完全な設計プロセス

```python
class TestVehicleControlSystemE2E(unittest.TestCase):
    """車両制御システムのE2Eテスト"""
    
    def setUp(self):
        """テストの初期化"""
        # 知識ベースの準備
        self.kb = self._create_vehicle_kb()
        
        # セッション初期化
        self.session = DesignSession(
            domain="vehicle_control",
            initial_system="car_running"
        )
        self.session.set_knowledge_base(self.kb)
    
    def _create_vehicle_kb(self):
        """車両制御用知識ベースの作成"""
        kb = KnowledgeBase("vehicle_control")
        
        # 状況の登録
        kb.register_situation("car_running", "obstacle_on_road")
        kb.register_situation("human_maneuvering", "low_visibility")
        
        # 問題の登録
        kb.register_problem("car_running+obstacle", "collision_risk")
        kb.register_problem("human_maneuvering+low_visibility", "collision_risk")
        
        # 意図の登録
        kb.register_intention("collision_risk", "prevent_collision")
        kb.register_intention(
            "collision_risk_low_vis",
            "support_driver_in_low_visibility"
        )
        
        # 解決策の登録
        kb.register_solution("prevent_collision", "auto_maneuvering")
        kb.register_solution("prevent_collision", "human_maneuvering")
        kb.register_solution("support_driver_in_low_visibility", "alarm")
        kb.register_solution("support_driver_in_low_visibility", "guide")
        
        # 分解の登録
        kb.register_decomposition(
            "prevent_collision",
            ["by_car", "by_driver"],
            ["auto_maneuvering", "human_maneuvering"]
        )
        
        return kb
    
    def test_complete_vehicle_design(self):
        """完全な車両システム設計のテスト"""
        # ====== フェーズ1: 初期設計探索 ======
        
        # 状況評価
        si1 = self.session.assess_situation()
        self.assertEqual(si1.situation, "obstacle_on_road")
        
        # 問題特定
        pi1 = self.session.identify_problem()
        self.assertEqual(pi1.problem, "collision_risk")
        
        # 意図確立
        ei1 = self.session.establish_intention(pi1.problem)
        self.assertEqual(ei1.intention, "prevent_collision")
        
        # 意図分解
        di1 = self.session.decompose_intention(ei1.intention)
        self.assertEqual(len(di1.sub_systems), 2)
        self.assertIn("auto_maneuvering", di1.sub_systems)
        self.assertIn("human_maneuvering", di1.sub_systems)
        
        # ====== フェーズ2: サブシステムの探索 ======
        
        # auto_maneuvering は解決策として終了
        sa1 = self.session.apply_solution("auto_maneuvering")
        self.assertIsNotNone(sa1.subsystem)
        
        # human_maneuvering をさらに探索
        sub_session = self.session.create_sub_session("human_maneuvering")
        
        si2 = sub_session.assess_situation()
        self.assertEqual(si2.situation, "low_visibility")
        
        pi2 = sub_session.identify_problem()
        self.assertEqual(pi2.problem, "collision_risk")
        
        ei2 = sub_session.establish_intention(pi2.problem)
        self.assertEqual(ei2.intention, "support_driver_in_low_visibility")
        
        # 2つの解決策を適用
        sa2 = sub_session.apply_solution("alarm")
        sa3 = sub_session.apply_solution("guide")
        
        self.assertIsNotNone(sa2.subsystem)
        self.assertIsNotNone(sa3.subsystem)
        
        # ====== フェーズ3: DEグラフの検証 ======
        
        de_graph = self.session.get_de_graph()
        
        # 期待されるコンポーネント数
        # SI×2, PI×2, EI×2, DI×1, SA×3 = 10
        self.assertGreaterEqual(len(de_graph.components), 10)
        
        # ====== フェーズ4: グラフ変換 ======
        
        converter = GraphConverter()
        
        # DE → LD
        ld_graph = converter.de_to_ld(de_graph)
        self.assertGreater(len(ld_graph.nodes), 0)
        
        # Simplify
        simplified = ld_graph.simplify()
        
        # Extract Hierarchies
        hierarchies = converter.extract_hierarchies(simplified)
        self.assertIn("Level_0", hierarchies)
        self.assertIn("Level_1", hierarchies)
        
        # LD → SI
        si_graph = converter.ld_to_si(hierarchies)
        
        # Resolve Alternatives
        final_si_graph = converter.resolve_alternatives(si_graph)
        
        # ====== フェーズ5: SIグラフの検証 ======
        
        # 階層レベルの確認
        self.assertGreaterEqual(len(final_si_graph.hierarchies), 2)
        
        # CNDコンポーネントの存在確認
        cnd_components = final_si_graph.find_components_by_type(CNDComponent)
        self.assertGreater(len(cnd_components), 0)
        
        # BUPコンポーネントの存在確認（代替解決後）
        bup_components = final_si_graph.find_components_by_type(BUPComponent)
        # 少なくとも1つのBUP関係が存在すべき
        
        # ====== フェーズ6: 結果の可視化と保存 ======
        
        visualizer = Visualizer()
        
        # DEグラフの可視化
        de_graph.visualize("/tmp/test_vehicle_de_graph.png")
        self.assertTrue(os.path.exists("/tmp/test_vehicle_de_graph.png"))
        
        # SIグラフの可視化
        si_graph.visualize_hierarchy("/tmp/test_vehicle_si_graph.png")
        self.assertTrue(os.path.exists("/tmp/test_vehicle_si_graph.png"))
        
        # 結果の保存
        result = {
            "de_graph": de_graph.to_dict(),
            "si_graph": si_graph.to_hierarchical_dict()
        }
        
        with open("/tmp/test_vehicle_design.json", "w") as f:
            json.dump(result, f, indent=2)
        
        self.assertTrue(os.path.exists("/tmp/test_vehicle_design.json"))
```

### 10.4 テストカバレッジ目標

| モジュール | カバレッジ目標 | 説明 |
|-----------|--------------|------|
| コンポーネント | 95%以上 | DEおよびSIコンポーネント |
| グラフ構造 | 90%以上 | DE/LD/SIグラフ |
| アルゴリズム | 85%以上 | 変換、探索アルゴリズム |
| API | 80%以上 | REST API |
| 統合 | 90%以上 | E2Eテスト |

### 10.5 テスト実行方法

```bash
# 全テストの実行
pytest tests/ -v --cov=cdss --cov-report=html

# 単体テストのみ
pytest tests/unit/ -v

# 統合テストのみ
pytest tests/integration/ -v

# E2Eテストのみ
pytest tests/e2e/ -v

# 特定のテストクラス
pytest tests/unit/test_components.py::TestSIComponent -v

# カバレッジレポートの表示
open htmlcov/index.html
```

---

## 付録A: 用語集

| 用語 | 説明 |
|------|------|
| CDSS | Concept Design Support System（コンセプト設計支援システム） |
| DE | Design Exploration（設計探索） |
| SI | Systems Integration（システム統合） |
| LD | Logical Dependency（論理依存） |
| KB | Knowledge Base（知識ベース） |
| SI (component) | Situation Assessment（状況評価）コンポーネント |
| PI | Problem Identification（問題特定） |
| EI | Establish Intention（意図確立） |
| DI | Decompose Intention（意図分解） |
| CB | Conditional Branch（条件分岐） |
| SA | Solution Assignment（解決策割り当て） |
| CND | Condition（条件）SIコンポーネント |
| BUP | Backups（バックアップ） |
| COL | Collaboration（協調） |
| ALT | Alternative（代替） |
| EXO | Exclusive（排他） |
| RSID | Revision Save ID（リビジョン保存ID） |

---

## 付録B: 参考文献

1. Mikito Iwamasa, "Concept Design Visualization - A component-based approach", Toshiba Corp., 2000
2. Simon, H. A., "The Sciences of the Artificial" (3rd edition), MIT Press, Cambridge MA, 1996
3. S. Buckingham Shum, "Design Argumentation as Design Rationale", The Encyclopedia of Computer Science and Technology, Marcel Dekker, Inc., 1996
4. T. R. Gruber and D. M. Russell, "Generative design rationale: beyond the record and replay paradigm", Lawrence Erlbaum Associates, 1995

---

## 改訂履歴

| バージョン | 日付 | 変更内容 | 担当者 |
|-----------|------|---------|--------|
| 1.0 | 2025-11-17 | 初版作成 | - |

---

**End of Document**