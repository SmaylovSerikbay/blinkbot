"""
O'zbek lokallashtirish
"""
translations = {
    "start": {
        "welcome": "Blink-ga xush kelibsiz! 👋\n\nTilni tanlang:",
        "language_selected": "Til o'rnatildi: O'zbekcha 🇺🇿",
        "choose_role": "Rolingizni tanlang:",
        "driver": "Men Haydovchiman 🚗",
        "passenger": "Men Yo'lovchiman 🙋‍♂️",
    },
    "common": {
        "back": "Orqaga",
        "cancel": "Bekor qilish",
        "next": "Keyingi",
        "contact": "Bog'lanish",
        "search": "Qidirish",
        "share_phone": "📱 Raqamni ulashish",
    },
    "driver": {
        "create_trip": "Sayohat yaratish",
        "need_phone": "Sayohat yaratish uchun telefon raqamingizni ko'rsatish kerak 📱\n\nKontaktingizni ulashing:",
        "phone_saved": "✅ Telefon raqami saqlandi!",
        "need_verification": "⚠️ Sayohat e'lon qilish uchun verifikatsiyadan o'tish kerak.\n\nVerifikatsiyani boshlash uchun /verify buyrug'ini ishlating.",
        "from_city": "Qayerdan ketyapsiz? 🚗",
        "to_city": "Qayerga ketyapsiz? 🎯",
        "trip_date": "Sayohat qachon? 📅\n(Sanani ko'rsating: КК.ОО.ЙЙЙЙ)",
        "price": "Sayohat qancha turadi? 💰\n(Summani so'mda ko'rsating)",
        "description": "Tavsif qo'shing (ixtiyoriy): 📝",
        "trip_created": "✅ Sayohat muvaffaqiyatli yaratildi!",
    },
    "verification": {
        "start": "🔐 Haydovchini verifikatsiya qilish\n\nSayohat e'lon qilish uchun verifikatsiyadan o'tish kerak.\n\nHaydovchilik guvohnomasining fotosini yuboring:",
        "license_received": "✅ Guvohnoma fotosi olindi!\n\nEndi avtomobilingiz fotosini yuboring:",
        "car_received": "✅ Avtomobil fotosi olindi!\n\nSizning arizangiz administratorga yuborildi. Tekshiruvdan keyin xabar olasiz.",
        "already_verified": "✅ Siz allaqachon verifikatsiya qilingansiz!",
        "approved": "✅ Verifikatsiya arizasi tasdiqlandi!\n\nEndi sayohat e'lon qila olasiz.",
        "rejected": "❌ Verifikatsiya arizasi rad etildi.\n\nSavollaringiz bo'lsa, administratorga murojaat qiling.",
    },
    "passenger": {
        "search_trips": "Sayohat qidirish 🔍",
        "no_trips": "Sayohat topilmadi 😔",
        "trip_card": "🚗 <b>{from_city}</b> → <b>{to_city}</b>\n"
                     "📅 Sana: {date}\n"
                     "💰 Narx: {price} so'm\n"
                     "👤 Haydovchi: {name} {verified}\n"
                     "⭐ Reyting: {rating}\n"
                     "🚙 Avtomobil: {car_info}\n"
                     "{description}",
        "car_model": "ko'rsatilmagan",
    },
    "admin": {
        "verification_request": "🔐 <b>Verifikatsiyaga yangi ariza</b>\n\n"
                                "👤 Haydovchi: {name} (@{username})\n"
                                "📱 Telefon: {phone}\n"
                                "🆔 ID: {user_id}\n\n"
                                "Guvohnomalar:",
        "approve": "✅ Tasdiqlash",
        "reject": "❌ Rad etish",
        "verification_approved": "✅ {user_id} foydalanuvchisi uchun verifikatsiya tasdiqlandi",
        "verification_rejected": "❌ {user_id} foydalanuvchisi uchun verifikatsiya rad etildi",
    },
    "errors": {
        "invalid_date": "❌ Sana formati noto'g'ri. Quyidagi formatni ishlating: КК.ОО.ЙЙЙЙ",
        "invalid_price": "❌ Narx formati noto'g'ri. Raqamni ko'rsating.",
        "unknown_error": "❌ Xatolik yuz berdi. Qayta urinib ko'ring.",
        "phone_required": "❌ Davom etish uchun telefon raqamingizni ulashish kerak.",
        "not_verified": "❌ Siz verifikatsiyadan o'tmadingiz. /verify ishlating",
    },
}

