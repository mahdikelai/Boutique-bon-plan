const products = [
  {
    id: 100, category: "robes",
    brand: "Boutique Bon Plan",
    name: "فوندغوب",
    price: 850,
    images: [
      "images/products/product1/1.jpg",
      "images/products/product1/2.jpg",
      "images/products/product1/3.jpg"
    ],
    rating: 4.5,
    color: "nude",
    style: "elegant"
  },
  {
    id: 101, category: "robes",
    brand: "Boutique Bon Plan",
    name: "فوندغوب قلب ❤️",
    price: 1200,
    images: [
      "images/products/product2/1.jpg",
      "images/products/product2/2.jpg",
      "images/products/product2/3.jpg",
      "images/products/product2/4.jpg",
      "images/products/product2/5.jpg",
      "images/products/product2/6.jpg"
    ],
    rating: 4.9,
    color: "red",
    style: "sexy",
    description: "👗 أناقة وتميّز لكل امرأة تحب تكون أنيقة 💕"
  }
  

  ,{
    id: 1786700001, category: "lingerie",
    brand: "Boutique Bon Plan",
    name: "3 بياس ريال مدريد 🖤🤍",
    price: 1200,
    images: [
      "images/products/pack-real-madrid/1.jpg",
      "images/products/pack-real-madrid/2.jpg",
      "images/products/pack-real-madrid/3.jpg"
    ],
    rating: 5.0,
    color: "أبيض",
    style: ""
  }

  ,{
    id: 1786799551101, category: "sleepwear",
    brand: "Boutique Bon Plan",
    name: "بيستي شورت كيتي ❤️",
    price: 800,
    images: [
      "images/products/بيستي-شورت-كيتي-1786799551101/1.jpg", "images/products/بيستي-شورت-كيتي-1786799551101/2.jpg", "images/products/بيستي-شورت-كيتي-1786799551101/3.jpg", "images/products/بيستي-شورت-كيتي-1786799551101/4.jpg"
    ],
    rating: 5.0,
    color: "اسود ، أحمر ، ابيض ، أزرق",
    style: ""
  }

  ,{
    id: 1786831633792, category: "robes",
    brand: "Boutique Bon Plan",
    name: "روب ديكوتي إيفازي",
    price: 1000,
    images: [
      "images/products/روب-ديكوتي-إيفازي-1786831633792/1.jpg", "images/products/روب-ديكوتي-إيفازي-1786831633792/2.jpg", "images/products/روب-ديكوتي-إيفازي-1786831633792/3.jpg", "images/products/روب-ديكوتي-إيفازي-1786831633792/4.jpg"
    ],
    rating: 5.0,
    color: "",
    style: "", description: "روب ديكوتي Évasé ✨🌸\nأناقة بسيطة، راحة وذوق في قطعة وحدة 😍\nروب ديكوتي Évasé بقصّة أنيقة وواسعة 💕\n🇩🇿 صناعة محلية 100%\n🧵 مخدومة بعناية في الورشة، من الورشة مباشرة للزبون\n✨ موديل أنيق ومريح\n💰 السعر: 1000 دج فقط\n🚚 التوصيل متوفر لجميع الولايات\n💵 الدفع عند الاستلام"
  }

  ,{
    id: 1786832986316, category: "bodysuits",
    brand: "Boutique Bon Plan",
    name: "كومبي شورت تيغر دونتال",
    price: 1000,
    images: [
      "images/products/كومبي-شورت-تيغر-دونتال-1786832986316/1.jpg", "images/products/كومبي-شورت-تيغر-دونتال-1786832986316/2.jpg", "images/products/كومبي-شورت-تيغر-دونتال-1786832986316/3.jpg"
    ],
    rating: 5.0,
    color: "",
    style: "", description: "🐆 كومبي شورت تيغر دونتال ✨\nأناقة وجاذبية في قطعة وحدة ❤️‍🔥\nكومبي شورت تيغر دونتال بتصميم أنثوي مميز، يجمع بين نقشة الـTiger الجريئة ولمسات الدونتال السوداء الأنيقة، مع ربطات على الكتفين تزيده جمالاً وتميزاً. 😍\n✨ تصميم أنثوي وجذاب\n🖤 تفاصيل دانتيل أنيقة\n🐆 نقشة Tiger مميزة\n🎀 ربطات كتف قابلة للتعديل\n👗 المقاس: Standard\n💰 السعر: 1000 دج فقط\n🚚 التوصيل متوفر لجميع الولايات\n💵 الدفع عند الاستلام\n📩 أطلبه الآن 💕", stock: 3
  }

  

  

  ,{
    id: 1786836428497, category: "robes",
    brand: "Boutique Bon Plan",
    name: "فوندغوب مشرشفة موتيف بابيو",
    price: 1200,
    images: [
      "images/products/فوندغوب-مشرشفة-موتيف-بابيو-1786836428497/1.jpg", "images/products/فوندغوب-مشرشفة-موتيف-بابيو-1786836428497/2.jpg", "images/products/فوندغوب-مشرشفة-موتيف-بابيو-1786836428497/3.jpg", "images/products/فوندغوب-مشرشفة-موتيف-بابيو-1786836428497/4.jpg", "images/products/فوندغوب-مشرشفة-موتيف-بابيو-1786836428497/5.jpg", "images/products/فوندغوب-مشرشفة-موتيف-بابيو-1786836428497/6.jpg", "images/products/فوندغوب-مشرشفة-موتيف-بابيو-1786836428497/7.jpg"
    ],
    rating: 5.0,
    color: "",
    style: ""
  }

  ,{
    id: 1786877444840, category: "robes",
    brand: "Boutique Bon Plan",
    name: "براسيار جيب ❤️",
    price: 1000,
    images: [
      "images/products/براسيار-جيب-1786877444840/1.jpg", "images/products/براسيار-جيب-1786877444840/2.jpg", "images/products/براسيار-جيب-1786877444840/3.jpg", "images/products/براسيار-جيب-1786877444840/4.jpg", "images/products/براسيار-جيب-1786877444840/5.jpg", "images/products/براسيار-جيب-1786877444840/6.jpg", "images/products/براسيار-جيب-1786877444840/7.jpg", "images/products/براسيار-جيب-1786877444840/8.jpg", "images/products/براسيار-جيب-1786877444840/9.jpg", "images/products/براسيار-جيب-1786877444840/10.jpg"
    ],
    rating: 5.0,
    color: "",
    style: "", description: "🌸 بسم الله ما شاء الله ❤️\n✨ براسيار جيب ✨\n👗 لاطاي ستوندارد 🥰 \n👗 أناقة وتميّز لكل امرأة تحب تكون أنيقة 💕\n🚚 التوصيل متوفر لـ 58 ولاية\n💰 السعر: 1000 دج فقط 🤐\n📦 الدفع عند الاستلام\n😍 مرحباً بكم، أطلبي الآن 📝", stock: 5
  }

  ,{
    id: 1786889651477, category: "sleepwear",
    brand: "Boutique Bon Plan",
    name: "بيجامة كيتي",
    price: 1100,
    images: [
      "images/products/بيجامة-كيتي-1786889651477/1.jpg", "images/products/بيجامة-كيتي-1786889651477/2.jpg", "images/products/بيجامة-كيتي-1786889651477/3.jpg", "images/products/بيجامة-كيتي-1786889651477/4.jpg"
    ],
    rating: 5.0,
    color: "",
    style: "", description: "🌸 بسم الله ما شاء الله ❤️\n✨ براسيار جيب ✨\n👗 لاطاي ستوندارد 🥰 \n👗 أناقة وتميّز لكل امرأة تحب تكون أنيقة 💕\n🚚 التوصيل متوفر لـ 58 ولاية\n💰 السعر: 1000 دج فقط 🤐\n📦 الدفع عند الاستلام\n😍 مرحباً بكم، اطلبيه الآن 📝 💌", stock: 5
  }

  ,{
    id: 1786945525033, category: "bridal",
    brand: "Boutique Bon Plan",
    name: "امبورطاسيو",
    price: 2500,
    images: [
      "images/products/امبورطاسيو-1786945525033/1.jpg", "images/products/امبورطاسيو-1786945525033/2.jpg", "images/products/امبورطاسيو-1786945525033/3.jpg", "images/products/امبورطاسيو-1786945525033/4.jpg"
    ],
    rating: 5.0,
    color: "ابيض، احمر، أسود، عنابي",
    style: "", stock: 5
  }

  ,{
    id: 1787009630258, category: "robes",
    brand: "Boutique Bon Plan",
    name: "فوندروب مشرشفة بالخيوط",
    price: 800,
    images: [
      "images/products/فوندروب-مشرشفة-بالخيوط-1787009630258/1.jpg", "images/products/فوندروب-مشرشفة-بالخيوط-1787009630258/2.jpg", "images/products/فوندروب-مشرشفة-بالخيوط-1787009630258/3.jpg", "images/products/فوندروب-مشرشفة-بالخيوط-1787009630258/4.jpg", "images/products/فوندروب-مشرشفة-بالخيوط-1787009630258/5.jpg", "images/products/فوندروب-مشرشفة-بالخيوط-1787009630258/6.jpg", "images/products/فوندروب-مشرشفة-بالخيوط-1787009630258/7.jpg", "images/products/فوندروب-مشرشفة-بالخيوط-1787009630258/8.jpg"
    ],
    rating: 5.0,
    color: "",
    style: "", description: "🌸 بسم الله ما شاء الله ❤️\n✨ براسيار جيب ✨\n👗 لاطاي s m l xl 🥰 \n👗 أناقة وتميّز لكل امرأة تحب تكون أنيقة 💕\n🚚 التوصيل متوفر لـ 58 ولاية\n💰 السعر: 800 دج فقط 🤐\n📦 الدفع عند الاستلام\n😍 مرحباً بكم، اطلبيها الآن 📝 💌", stock: 5, sizes: ["S", "M", "L", "XL"]
  }

  /* باش تزيد منتج جديد، انسخ هذا القالب وبدل القيم:
  ,{
    id: 102, category: "lingerie",
    brand: "Boutique Bon Plan",
    name: "اسم المنتج",
    price: 0,
    images: [
      "images/products/product3/1.jpg"
    ],
    rating: 5.0,
    color: "",
    style: ""
  }
  */
];
