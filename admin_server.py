import os
import re
import json
import base64
import subprocess
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

BASE_DIR = "/data/data/com.termux/files/usr/share/nginx/html"
PRODUCTS_FILE = os.path.join(BASE_DIR, "products.js")
IMAGES_DIR = os.path.join(BASE_DIR, "images", "products")

app = Flask(__name__)
CORS(app)

def slugify(name):
    s = re.sub(r'[^\w\u0600-\u06FF]+', '-', name.strip())
    return s.strip('-')[:40] or "product"

@app.route('/add-product', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        price = int(data.get('price', 0))
        category = data.get('category', '')
        color = data.get('color', '')
        style = data.get('style', '')
        desc = data.get('description', '')
        images_b64 = data.get('images', [])

        if not name or not price or not images_b64:
            return jsonify({"error": "بيانات ناقصة"}), 400

        product_id = int(datetime.now().timestamp() * 1000)
        folder_name = f"{slugify(name)}-{product_id}"
        folder_path = os.path.join(IMAGES_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        image_paths = []
        for i, img_data in enumerate(images_b64, start=1):
            header, encoded = img_data.split(',', 1) if ',' in img_data else ('', img_data)
            ext = 'jpg'
            if 'png' in header:
                ext = 'png'
            elif 'webp' in header:
                ext = 'webp'
            file_path = os.path.join(folder_path, f"{i}.{ext}")
            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(encoded))
            rel_path = f"images/products/{folder_name}/{i}.{ext}"
            image_paths.append(rel_path)

        product_js = f'''
  ,{{
    id: {product_id}, category: "{category}",
    brand: "Boutique Bon Plan",
    name: "{name}",
    price: {price},
    images: [
      {", ".join(chr(34) + p + chr(34) for p in image_paths)}
    ],
    rating: 5.0,
    color: "{color}",
    style: "{style}"{f", description: {chr(34)}{desc}{chr(34)}" if desc else ""}
  }}
'''

        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        marker = "\n  /* باش تزيد منتج جديد"
        if marker in content:
            content = content.replace(marker, product_js + marker)
        else:
            content = content.replace("];", product_js + "];")

        with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
            f.write(content)

        subprocess.run(['git', 'add', '.'], cwd=BASE_DIR, check=True)
        subprocess.run(['git', 'commit', '-m', f'اضافة منتج: {name}'], cwd=BASE_DIR, check=True)
        subprocess.run(['git', 'push'], cwd=BASE_DIR, check=True)

        return jsonify({"success": True, "message": "تم اضافة المنتج ونشره بنجاح"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
