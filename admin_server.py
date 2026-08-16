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

def js_escape(text):
    if text is None:
        return ""
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    text = text.replace('\n', '\\n').replace('\r', '')
    return text

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
        stock = data.get('stock')
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

        safe_category = js_escape(category)
        safe_name = js_escape(name)
        safe_color = js_escape(color)
        safe_style = js_escape(style)
        safe_desc = js_escape(desc)

        product_js = f'''
  ,{{
    id: {product_id}, category: "{safe_category}",
    brand: "Boutique Bon Plan",
    name: "{safe_name}",
    price: {price},
    images: [
      {", ".join(chr(34) + p + chr(34) for p in image_paths)}
    ],
    rating: 5.0,
    color: "{safe_color}",
    style: "{safe_style}"{f", description: {chr(34)}{safe_desc}{chr(34)}" if desc else ""}{f", stock: {stock}" if stock else ""}
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

        return jsonify({"success": True, "message": "تم اضافة المنتج ونشره بنجاح"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete-product', methods=['POST'])
def delete_product():
    try:
        data = request.get_json()
        product_id = data.get('id')
        if not product_id:
            return jsonify({"error": "معرف المنتج ناقص"}), 400

        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        pattern = re.compile(
            r',?\s*\{\s*id:\s*' + str(product_id) + r',.*?\n\s*\}',
            re.DOTALL
        )
        new_content, count = pattern.subn('', content, count=1)

        if count == 0:
            return jsonify({"error": "ماتلقاش المنتج"}), 404

        with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)

        subprocess.run(['git', 'add', '.'], cwd=BASE_DIR, check=True)
        subprocess.run(['git', 'commit', '-m', f'حذف منتج: {product_id}'], cwd=BASE_DIR, check=True)

        return jsonify({"success": True, "message": "تم حذف المنتج ونشر التحديث"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-products', methods=['GET'])
def get_products():
    try:
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'const products = (\[[\s\S]*?\]);', content)
        if not match:
            return jsonify([])
        products_str = match.group(1)
        products_str = re.sub(r'/\*[\s\S]*?\*/', '', products_str)
        products_str = re.sub(r',(\s*[\]\}])', r'\1', products_str)
        products_str = re.sub(r'([{,]\s*)(\w+):', r'\1"\2":', products_str)
        products = json.loads(products_str)
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

DELIVERY_FILE = os.path.join(BASE_DIR, "delivery-prices.json")

@app.route('/get-delivery-prices', methods=['GET'])
def get_delivery_prices():
    try:
        with open(DELIVERY_FILE, encoding='utf-8') as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update-delivery-price', methods=['POST'])
def update_delivery_price():
    try:
        data = request.get_json()
        wilaya_name = data.get('name')
        office = data.get('office')
        home = data.get('home')

        with open(DELIVERY_FILE, encoding='utf-8') as f:
            wilayas = json.load(f)

        found = False
        for w in wilayas:
            if w['name'] == wilaya_name:
                w['office'] = office
                w['home'] = home
                found = True
                break

        if not found:
            if data.get('isNew'):
                wilayas.append({"name": wilaya_name, "office": office, "home": home})
            else:
                return jsonify({"error": "ماتلقاتش الولاية"}), 404

        with open(DELIVERY_FILE, 'w', encoding='utf-8') as f:
            json.dump(wilayas, f, ensure_ascii=False, indent=2)

        subprocess.run(['git', 'add', '.'], cwd=BASE_DIR, check=True)
        subprocess.run(['git', 'commit', '-m', f'تحديث سعر التوصيل: {wilaya_name}'], cwd=BASE_DIR, check=True)

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete-delivery-price', methods=['POST'])
def delete_delivery_price():
    try:
        data = request.get_json()
        wilaya_name = data.get('name')

        with open(DELIVERY_FILE, encoding='utf-8') as f:
            wilayas = json.load(f)

        new_wilayas = [w for w in wilayas if w['name'] != wilaya_name]
        if len(new_wilayas) == len(wilayas):
            return jsonify({"error": "ماتلقاتش الولاية"}), 404

        with open(DELIVERY_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_wilayas, f, ensure_ascii=False, indent=2)

        subprocess.run(['git', 'add', '.'], cwd=BASE_DIR, check=True)
        subprocess.run(['git', 'commit', '-m', f'حذف: {wilaya_name}'], cwd=BASE_DIR, check=True)

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

CATEGORIES_FILE = os.path.join(BASE_DIR, "categories.json")

@app.route('/get-categories', methods=['GET'])
def get_categories():
    try:
        with open(CATEGORIES_FILE, encoding='utf-8') as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/save-category', methods=['POST'])
def save_category():
    try:
        data = request.get_json()
        cat_id = data.get('id', '').strip()
        label = data.get('label', '').strip()
        image_b64 = data.get('image')

        if not cat_id or not label:
            return jsonify({"error": "بيانات ناقصة"}), 400

        with open(CATEGORIES_FILE, encoding='utf-8') as f:
            categories = json.load(f)

        image_path = None
        if image_b64:
            header, encoded = image_b64.split(',', 1) if ',' in image_b64 else ('', image_b64)
            ext = 'png'
            if 'jpeg' in header or 'jpg' in header:
                ext = 'jpg'
            elif 'webp' in header:
                ext = 'webp'
            image_path = f"images/categories/{cat_id}.{ext}"
            full_path = os.path.join(BASE_DIR, image_path)
            with open(full_path, 'wb') as f:
                f.write(base64.b64decode(encoded))

        existing = next((c for c in categories if c['id'] == cat_id), None)
        if existing:
            existing['label'] = label
            if image_path:
                existing['image'] = image_path
        else:
            categories.append({
                "id": cat_id,
                "label": label,
                "image": image_path or f"images/categories/{cat_id}.png"
            })

        with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)

        subprocess.run(['git', 'add', '.'], cwd=BASE_DIR, check=True)
        subprocess.run(['git', 'commit', '-m', f'تحديث قسم: {label}'], cwd=BASE_DIR, check=True)

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete-category', methods=['POST'])
def delete_category():
    try:
        data = request.get_json()
        cat_id = data.get('id')

        with open(CATEGORIES_FILE, encoding='utf-8') as f:
            categories = json.load(f)

        new_categories = [c for c in categories if c['id'] != cat_id]
        if len(new_categories) == len(categories):
            return jsonify({"error": "ماتلقاش القسم"}), 404

        with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_categories, f, ensure_ascii=False, indent=2)

        subprocess.run(['git', 'add', '.'], cwd=BASE_DIR, check=True)
        subprocess.run(['git', 'commit', '-m', f'حذف قسم: {cat_id}'], cwd=BASE_DIR, check=True)

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

BANNERS_FILE = os.path.join(BASE_DIR, "banners.json")

@app.route('/get-banners', methods=['GET'])
def get_banners():
    try:
        with open(BANNERS_FILE, encoding='utf-8') as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/save-banner', methods=['POST'])
def save_banner():
    try:
        data = request.get_json()
        banner_id = data.get('id') or f"b{int(datetime.now().timestamp())}"
        link = data.get('link') or None
        caption = data.get('caption') or None
        image_b64 = data.get('image')

        with open(BANNERS_FILE, encoding='utf-8') as f:
            banners = json.load(f)

        image_path = None
        if image_b64:
            header, encoded = image_b64.split(',', 1) if ',' in image_b64 else ('', image_b64)
            ext = 'jpg'
            if 'png' in header:
                ext = 'png'
            elif 'webp' in header:
                ext = 'webp'
            image_path = f"images/banners/{banner_id}.{ext}"
            full_path = os.path.join(BASE_DIR, image_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'wb') as f:
                f.write(base64.b64decode(encoded))

        existing = next((b for b in banners if b['id'] == banner_id), None)
        if existing:
            existing['link'] = link
            existing['caption'] = caption
            if image_path:
                existing['image'] = image_path
                existing['gradient'] = None
        else:
            banners.append({
                "id": banner_id,
                "image": image_path,
                "gradient": None if image_path else "linear-gradient(135deg, #e6007e, #d4af37)",
                "link": link,
                "caption": caption
            })

        with open(BANNERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(banners, f, ensure_ascii=False, indent=2)

        subprocess.run(['git', 'add', '.'], cwd=BASE_DIR, check=True)
        subprocess.run(['git', 'commit', '-m', f'تحديث بانر: {banner_id}'], cwd=BASE_DIR, check=True)

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete-banner', methods=['POST'])
def delete_banner():
    try:
        data = request.get_json()
        banner_id = data.get('id')

        with open(BANNERS_FILE, encoding='utf-8') as f:
            banners = json.load(f)

        new_banners = [b for b in banners if b['id'] != banner_id]
        if len(new_banners) == len(banners):
            return jsonify({"error": "ماتلقاش البانر"}), 404

        with open(BANNERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_banners, f, ensure_ascii=False, indent=2)

        subprocess.run(['git', 'add', '.'], cwd=BASE_DIR, check=True)
        subprocess.run(['git', 'commit', '-m', f'حذف بانر: {banner_id}'], cwd=BASE_DIR, check=True)

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update-product-category', methods=['POST'])
def update_product_category():
    try:
        data = request.get_json()
        product_id = data.get('id')
        new_category = data.get('category', '').strip()

        if not product_id or not new_category:
            return jsonify({"error": "بيانات ناقصة"}), 400

        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        pattern = re.compile(
            r'(id:\s*' + str(product_id) + r',\s*category:\s*")[^"]*(")'
        )
        new_content, count = pattern.subn(r'\g<1>' + new_category + r'\g<2>', content, count=1)

        if count == 0:
            return jsonify({"error": "ماتلقاش المنتج"}), 404

        with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)

        subprocess.run(['git', 'add', '.'], cwd=BASE_DIR, check=True)
        subprocess.run(['git', 'commit', '-m', f'تغيير فئة منتج: {product_id}'], cwd=BASE_DIR, check=True)

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

COLORS_FILE = os.path.join(BASE_DIR, "colors.json")

@app.route('/get-colors', methods=['GET'])
def get_colors():
    try:
        with open(COLORS_FILE, encoding='utf-8') as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/save-colors', methods=['POST'])
def save_colors():
    try:
        data = request.get_json()

        with open(COLORS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        subprocess.run(['git', 'add', '.'], cwd=BASE_DIR, check=True)
        subprocess.run(['git', 'commit', '-m', 'تحديث ألوان الموقع'], cwd=BASE_DIR, check=True)

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

REVIEWS_FILE = os.path.join(BASE_DIR, "reviews.json")

@app.route('/get-reviews', methods=['GET'])
def get_reviews():
    try:
        product_id = request.args.get('product_id')
        with open(REVIEWS_FILE, encoding='utf-8') as f:
            reviews = json.load(f)
        if product_id:
            reviews = [r for r in reviews if str(r.get('product_id')) == str(product_id)]
        return jsonify(reviews)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add-review', methods=['POST'])
def add_review():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        name = data.get('name', '').strip()
        rating = int(data.get('rating', 5))
        text = data.get('text', '').strip()

        if not product_id or not name or not text:
            return jsonify({"error": "بيانات ناقصة"}), 400

        with open(REVIEWS_FILE, encoding='utf-8') as f:
            reviews = json.load(f)

        reviews.append({
            "id": int(datetime.now().timestamp() * 1000),
            "product_id": product_id,
            "name": name,
            "rating": rating,
            "text": text
        })

        with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
            json.dump(reviews, f, ensure_ascii=False, indent=2)

        subprocess.run(['git', 'add', '.'], cwd=BASE_DIR, check=True)
        subprocess.run(['git', 'commit', '-m', f'تقييم جديد: {name}'], cwd=BASE_DIR, check=True)

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete-review', methods=['POST'])
def delete_review():
    try:
        data = request.get_json()
        review_id = data.get('id')

        with open(REVIEWS_FILE, encoding='utf-8') as f:
            reviews = json.load(f)

        new_reviews = [r for r in reviews if r['id'] != review_id]
        if len(new_reviews) == len(reviews):
            return jsonify({"error": "ماتلقاش التقييم"}), 404

        with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_reviews, f, ensure_ascii=False, indent=2)

        subprocess.run(['git', 'add', '.'], cwd=BASE_DIR, check=True)
        subprocess.run(['git', 'commit', '-m', 'حذف تقييم'], cwd=BASE_DIR, check=True)

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pending-changes', methods=['GET'])
def pending_changes():
    try:
        result = subprocess.run(
            ['git', 'log', 'origin/main..HEAD', '--oneline'],
            cwd=BASE_DIR, capture_output=True, text=True
        )
        commits = [l for l in result.stdout.strip().split('\n') if l]
        return jsonify({"count": len(commits), "commits": commits})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/publish', methods=['POST'])
def publish():
    try:
        result = subprocess.run(
            ['git', 'push'], cwd=BASE_DIR, capture_output=True, text=True
        )
        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
