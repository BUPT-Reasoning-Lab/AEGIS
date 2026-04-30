import json
import sqlite3
from pathlib import Path


def create_database(db_path="dataset.db"):
    """创建数据库和表结构"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建表，包含所有可能的字段
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name TEXT NOT NULL,
            category TEXT,
            sub_type TEXT,
            with_text INTEGER,
            image_path TEXT,
            generated_model TEXT,
            original_caption TEXT,
            mask_path TEXT,
            vector_index TEXT,
            dataset_category TEXT NOT NULL
        )
    """
    )

    conn.commit()
    return conn


def import_json_to_db(json_file_path, dataset_category, conn):
    """将单个JSON文件导入数据库"""
    cursor = conn.cursor()

    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        cursor.execute(
            """
            INSERT INTO papers (
                image_name, category, sub_type, with_text, image_path,
                generated_model, original_caption, mask_path,
                vector_index, dataset_category
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                item.get("image_name"),
                item.get("category"),
                item.get("sub_type"),
                1 if item.get("with_text") else 0,  # 将布尔值转换为整数
                item.get("image_path"),
                item.get("generated_model"),
                item.get("original_caption"),
                item.get("mask_path"),
                None,  # vector_index 初始为空
                dataset_category,
            ),
        )

    conn.commit()
    print(f"成功导入 {len(data)} 条数据从 {dataset_category}.json")


def main():
    # 设置路径
    dataset_dir = Path(__file__).parent.parent / "assets" / "dataset"
    db_path = (
        Path(__file__).parent.parent / "assets" / "dataset_without_vector_index.db"
    )
    print("Database path:", db_path)

    # JSON文件列表
    json_files = [
        "image_inference_forgery.json",
        "real.json",
        "targeted_region_editing.json",
        "targeted_region_restoration.json",
        "text_constraint_fabrication.json",
    ]

    # 创建数据库
    print("正在创建数据库...")
    conn = create_database(str(db_path))

    # 导入每个JSON文件
    for json_file in json_files:
        json_path = dataset_dir / json_file
        dataset_category = json_file.replace(".json", "")

        if json_path.exists():
            print(f"正在导入 {json_file}...")
            import_json_to_db(json_path, dataset_category, conn)
        else:
            print(f"警告: 文件不存在 - {json_path}")

    # 关闭数据库连接
    conn.close()
    print(f"\n数据库创建完成: {db_path}")
    print("所有数据已成功导入!")

    # 打印统计信息
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT dataset_category, COUNT(*) FROM papers GROUP BY dataset_category"
    )
    results = cursor.fetchall()
    print("\n各数据集统计:")
    for category, count in results:
        print(f"  {category}: {count} 条记录")

    cursor.execute("SELECT COUNT(*) FROM papers")
    total = cursor.fetchone()[0]
    print(f"\n总计: {total} 条记录")

    conn.close()


if __name__ == "__main__":
    main()
