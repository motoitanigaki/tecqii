# Qiita エンジニア検索・ランキング

## 概要
Qiita エンジニア検索・ランキングはQiita上のユーザーをcontribution数でランキング表示・検索ができるサイトです。

http://tecqii.com/

## 構成
- 基本的な技術要素
  - Python3
  - Django
  - Django-rest-framework
  - Bootstrap
  - Qiita API
- 本番環境
  - CentOS
  - Apache
  - PostgreSQL
 
## 仕様
- Qiita APIのコールなどは各種バッチ化しcronでスケジューリング
- 一部キーワード抽出などでMecabなどの言語処理ツールを利用
- memcachedにてキャッシュを利用


