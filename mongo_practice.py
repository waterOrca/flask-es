# 載入 pymongo 套件
import pymongo

# 連線到 MongoDB 雲端資料庫
client = pymongo.MongoClient("mongodb+srv://root:1FMpJvtF36HFIOa9@mycluster.6srbj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# 把資料放進資料庫中
db = client.test # 選擇操作 test 資料庫
collection = db.users # 選擇操作 users 集合
collection.insert_one({
    "name":"timmy",
    "gender":"男"
})
print("新增資料成功")



