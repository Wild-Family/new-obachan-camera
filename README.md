# new-obachan-camera

## /
### main.py
- main
- API call

### pic.py
- 写真撮影

### face.py
- 顔の状態

### dialogue.py
- AITALKへ音声ファイルをリクエスト
- dialogue.csvからstatusでセリフを検索

## /test
### face.py
- cloud vision apiのテスト
### sendMQ.py
- Azure Service Busのキューに追加
### clearMQ.py
- Azure Service Busのキューをすべて削除(時々できない)
### take.py
- raspiで写真撮影のテスト