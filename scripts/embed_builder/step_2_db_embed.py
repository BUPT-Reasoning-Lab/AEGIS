import sqlite3
import json
import os
import shutil
from pathlib import Path

from query_engine import Embedder

DATABASE_DIR = Path(__file__).parent.parent / "assets"


def main():
    # 配置参数
    origin_db_path = (
        Path(__file__).parent.parent / "assets" / "dataset_without_vector_index.db"
    )

    db_path = Path(__file__).parent.parent / "assets" / "dataset_with_vector_index.db"

    shutil.copyfile(origin_db_path, db_path)

    model_name_or_path = (
        "./assets/facebook/dinov3-vits16-pretrain-lvd1689m"  # 根据实际使用的模型修改
    )

    # 检查数据库文件是否存在
    if not os.path.exists(db_path):
        print(f"错误: 数据库文件 {db_path} 不存在")
        return

    # 初始化 Embedder
    print("正在加载模型...")
    embedder = Embedder(model_name_or_path)
    print("模型加载完成")

    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查询所有记录
    cursor.execute("SELECT id, image_path FROM papers WHERE image_path IS NOT NULL")
    records = cursor.fetchall()

    total_records = len(records)
    print(f"找到 {total_records} 条记录需要处理")

    # 处理每条记录
    success_count = 0
    error_count = 0

    for idx, (record_id, image_path) in enumerate(records, 1):
        try:
            # 检查图片文件是否存在
            if not os.path.exists(os.path.join(DATABASE_DIR, image_path)):
                print(f"[{idx}/{total_records}] 警告: 图片文件不存在: {image_path}")
                error_count += 1
                continue

            # 生成嵌入向量
            # print(f"[{idx}/{total_records}] 正在处理: {image_path}")
            embedding = embedder.embed(os.path.join(DATABASE_DIR, image_path))

            # 将 tensor 转换为 list 以便存储
            # 如果在 GPU 上，需要先移到 CPU
            embedding_list = embedding.cpu().numpy().tolist()

            # 将向量转换为 JSON 字符串存储
            vector_json = json.dumps(embedding_list)

            # 更新数据库
            cursor.execute(
                "UPDATE papers SET vector_index = ? WHERE id = ?",
                (vector_json, record_id),
            )

            success_count += 1
            # print(
            #     f"[{idx}/{total_records}] 成功处理，向量维度: {len(embedding_list[0])}"
            # )

        except Exception as e:
            print(
                f"[{idx}/{total_records}] 错误: 处理记录 ID {record_id} 时出错: {str(e)}"
            )
            error_count += 1
            continue

    # 提交更改
    conn.commit()
    print("\n处理完成!")
    print(f"成功: {success_count} 条")
    print(f"失败: {error_count} 条")

    # 关闭数据库连接
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
