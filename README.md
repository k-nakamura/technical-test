# Face Predictor
## セットアップ方法
### 前提
- gcloudコマンドがインストール済  
- Google Cloud Platform上にプロジェクトを設定していてgcloudコマンドに設定済
- kubectlコマンドがインストール済

### 手順
1. Google Kubernetes EngineからKubernetes クラスタを作成する  
GPUを使用しないクラスタを作成した場合は/requirements.txtの以下の箇所を置換
```
tensorflow-gpu==1.14.0 -> tensorflow==1.14.0
```

※ GPUを使用したクラスタはGCPのコンソールから[IAMと管理 > 割り当て]からGPUの上限を引き上げるよう申請が必要なので注意  

3. デプロイ先のクラスタを設定
作成したクラスタをgcloudコマンドで扱えるよう設定
```
gcloud container clusters get-credentials <クラスタ名>
```

4. コンテナイメージの作成からデプロイ、サービスの作成  
/Makefileが配置されているディレクトリで以下のコマンドを実行  
(すでに同名のデプロイ、サービスがある場合は事前に削除しておく)
```
make all
```
