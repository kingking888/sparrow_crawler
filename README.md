# sparrow-crawler
## 安装

## 接口说明

## 异步任务
|------------|------|
celery broker| redis|
|------------|------|
celery result| mysql|
|------------|------|
### 启动worker
celery -A sparrow_crawler  worker -l info
