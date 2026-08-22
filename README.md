# Python Project Template

<div align="center">

[![CI](https://github.com/yama0308/python-project-template/actions/workflows/ci.yml/badge.svg)](https://github.com/yama0308/python-project-template/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.14%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/package%20manager-uv-DE5FE9?logo=astral&logoColor=white)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## Overview

本リポジトリは、**uv**、**Ruff**、**ty** などの最新ツールチェーンを中心に構成された Python プロジェクト用テンプレートです。
環境構築の高速化、厳格な静的解析、整備されたテスト環境、およびコミット/プッシュ時の品質保証フロー（pre-commit / GitHub Actions）を初期状態で完備しています。

---

## Tech Stack & Features

| ツール / ライブラリ | 用途 | 特徴・採用理由 |
|:---|:---|:---|
| **[uv](https://docs.astral.sh/uv/)** | パッケージ・環境管理 | Rust 製の超高速パッケージマネージャー。`uv.lock` による決定論的依存解決 |
| **[Ruff](https://docs.astral.sh/ruff/)** | Linter & Formatter | Rust 製の高速解析ツール。Black, isort, Flake8 等のルールを統合 |
| **[ty](https://github.com/astral-sh/ty)** | 型チェッカー / Language Server | Astral 製の高速な型チェッカー。型安全性の向上 |
| **[pytest](https://docs.pytest.org/)** | テストフレームワーク | カバレッジ計測 (`pytest-cov`)、環境変数制御 (`pytest-env`)、モック (`pytest-mock`) を標準統合 |
| **[poethepoet](https://poethepoet.natn.io/)** | タスクランナー | `pyproject.toml` 内でフォーマット・リント・テストタスクを一元管理 |
| **[pre-commit](https://pre-commit.com/)** | Git コミットフック | コミット前の自動フォーマット・リントチェック（`pre-commit-uv` 連携で高速化） |
| **[GitHub Actions](https://github.com/features/actions)** | CI パイプライン | 全ブランチの Push / PR に対して Lint と Test を並列実行 |

---

## Configuration Details

### 1. `pyproject.toml`
プロジェクト設定の Single Source of Truth として各種ツール設定を集約しています。

- **`[project]` / `[dependency-groups]` (PEP 735)**:
  - 開発用モジュールは `[dependency-groups.dev]` に明記。
- **`[tool.poe.tasks]`**:
  - `fmt`: Ruff による自動フォーマット & import 整列・自動修正。
  - `lint`: Ruff (Lint) + ty (型チェック) を統合実行。
  - `check`: `lint` + `test` を一括実行。
- **`[tool.ruff]` & `[tool.ruff.lint]`**:
  - `select = ["ALL"]` をベースに、競合やノイズとなるルール（`TD`, `FIX`, `FBT`, `COM`, `PL`, `FLY`, `ISC001`, `CPY001`）を明示的に除外。
  - `[tool.ruff.lint.per-file-ignores]`:
    - `__init__.py`: re-export 用の未使用 import (`F401`) や docstring を許容。
    - `tests/**/*.py`: `assert` の使用 (`S101`) や docstring (`D10x`)、未使用引数 (`ARG`) を許容しつつ、型アノテーション (`ANN`) は維持。
- **`[tool.coverage]` & `[tool.pytest.ini_options]`**:
  - `branch = true` による分岐カバレッジ計測。
  - `relative_files = true` により CI 環境でのカバレッジパス不整合を防止。
  - `exclude_lines` で `if TYPE_CHECKING:` などの型・デバッグ用コードを計測対象外に設定。

### 2. `.pre-commit-config.yaml`
- 改行コード (`mixed-line-ending` -> LF)、末尾空白、YAML/TOML 構文チェックを実施。
- `repo: local` により、仮想環境内の `poe fmt`（フォーマット）および `poe lint`（リント・型チェック）を直接呼び出し、バージョン差異を排除。
- `.json` ファイルは末尾改行チェック (`end-of-file-fixer`) から除外設定済み。

### 3. `.vscode/settings.json`
- 保存時アクション（`editor.codeActionsOnSave`）で Ruff の自動修正と import 整理を適用。
- VS Code 標準のテストエクスプローラーで `pytest` を即座に認識・実行可能。
- `files.exclude` で `__pycache__` や `.pytest_cache`, `.ruff_cache` などの不要なフォルダーをサイドバーから非表示化。

### 4. `.github/workflows/ci.yml`
- `astral-sh/setup-uv` を利用し、キャッシュを活用した高速な CI を実現。
- `lint`（Ruff チェック、フォーマットチェック、ty 型チェック）と `test`（pytest & coverage）を並列ジョブで実行。

---

## Getting Started

### 前提条件
- [uv](https://docs.astral.sh/uv/) がインストールされていること

### 1. 依存関係のインストール
```sh
# 仮想環境の作成とパッケージ同期
uv sync
```

### 2. pre-commit のセットアップ
```sh
# pre-commit を uv ツールとしてインストール（未導入の場合）
uv tool install pre-commit --with pre-commit-uv

# Git フックの登録
pre-commit install
```

---

## Available Commands (Task Runner)

`poethepoet` を利用したコマンド一覧です：

```sh
# フォーマット実行 (Ruff format + check --fix)
uv run poe fmt

# リント・型チェック実行 (Ruff check + ty check)
uv run poe lint

# テスト実行 (pytest + coverage)
uv run poe test

# テスト実行 + HTMLカバレッジレポート生成 (htmlcov/ に出力)
uv run poe test-cov

# リント・テストを一括実行
uv run poe check
```

---

## Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI 定義
├── .vscode/
│   ├── extensions.json          # 推奨 VS Code 拡張機能
│   └── settings.json            # 開発用エディタ設定
├── src/
│   └── calc.py                  # ソースコード (サンプル)
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # 共通 fixture 定義用
│   └── test_calc.py             # 単体テスト (サンプル)
├── .gitignore
├── .pre-commit-config.yaml      # pre-commit フック設定
├── .python-version              # Python バージョン指定 (3.14)
├── pyproject.toml               # プロジェクト構成・各種ツール設定
├── README.md                    # ドキュメント
└── uv.lock                      # 依存関係ロックファイル
```

---

## License

このプロジェクトは [MIT License](LICENSE) のもとで公開されています。
