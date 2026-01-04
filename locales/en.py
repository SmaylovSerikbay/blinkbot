"""
English localization
"""
translations = {
    "start": {
        "welcome": "Welcome to Blink! 👋\n\nChoose your language:",
        "language_selected": "Language set: English 🇬🇧",
        "choose_role": "Choose your role:",
        "driver": "I'm a Driver 🚗",
        "passenger": "I'm a Passenger 🙋‍♂️",
    },
    "common": {
        "back": "Back",
        "cancel": "Cancel",
        "next": "Next",
        "contact": "Contact",
        "search": "Search",
        "share_phone": "📱 Share Phone",
    },
    "driver": {
        "create_trip": "Create Trip",
        "need_phone": "Phone number is required to create trips 📱\n\nPlease share your contact:",
        "phone_saved": "✅ Phone number saved!",
        "need_verification": "⚠️ Verification is required to publish trips.\n\nUse /verify command to start verification process.",
        "from_city": "Where are you leaving from? 🚗",
        "to_city": "Where are you going? 🎯",
        "trip_date": "When is the trip? 📅\n(Enter date in format: DD.MM.YYYY)",
        "price": "What's the price? 💰\n(Enter amount in Tenge)",
        "description": "Add description (optional): 📝",
        "trip_created": "✅ Trip created successfully!",
    },
    "verification": {
        "start": "🔐 Driver Verification\n\nVerification is required to publish trips.\n\nPlease send a photo of your driver's license:",
        "license_received": "✅ License photo received!\n\nNow send a photo of your car:",
        "car_received": "✅ Car photo received!\n\nYour application has been sent to the administrator. You will receive a notification after review.",
        "already_verified": "✅ You are already verified!",
        "approved": "✅ Your verification request has been approved!\n\nYou can now publish trips.",
        "rejected": "❌ Your verification request has been rejected.\n\nIf you have questions, contact the administrator.",
    },
    "passenger": {
        "search_trips": "Search Trips 🔍",
        "no_trips": "No trips found 😔",
        "trip_card": "🚗 <b>{from_city}</b> → <b>{to_city}</b>\n"
                     "📅 Date: {date}\n"
                     "💰 Price: {price} ₸\n"
                     "👤 Driver: {name} {verified}\n"
                     "⭐ Rating: {rating}\n"
                     "🚙 Car: {car_info}\n"
                     "{description}",
        "car_model": "not specified",
    },
    "admin": {
        "verification_request": "🔐 <b>New Verification Request</b>\n\n"
                                "👤 Driver: {name} (@{username})\n"
                                "📱 Phone: {phone}\n"
                                "🆔 ID: {user_id}\n\n"
                                "License:",
        "approve": "✅ Approve",
        "reject": "❌ Reject",
        "verification_approved": "✅ Verification approved for user {user_id}",
        "verification_rejected": "❌ Verification rejected for user {user_id}",
    },
    "errors": {
        "invalid_date": "❌ Invalid date format. Use: DD.MM.YYYY",
        "invalid_price": "❌ Invalid price format. Enter a number.",
        "unknown_error": "❌ An error occurred. Please try again.",
        "phone_required": "❌ Phone number is required to continue.",
        "not_verified": "❌ You haven't passed verification. Use /verify",
    },
}

