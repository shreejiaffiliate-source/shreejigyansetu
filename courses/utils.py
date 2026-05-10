import firebase_admin
from firebase_admin import credentials, messaging
import os
from django.conf import settings

# ✅ Initialize Firebase ONLY ONCE (Global Scope)
path_to_json = os.path.join(settings.BASE_DIR, 'firebase-credentials.json')

if not firebase_admin._apps:
    if os.path.exists(path_to_json):
        cred = credentials.Certificate(path_to_json)
        firebase_admin.initialize_app(cred)
        print("Firebase Admin Initialized Successfully")
    else:
        print(f"❌ ERROR: {path_to_json} missing!")

def send_push_notification(fcm_token, title, body, lesson_id, data=None):
    try:
        # Check if token exists
        if not fcm_token:
            print("⚠️ FCM Token is empty, skipping...")
            return False

        # Prepare Data Payload (FCM requires values to be STRINGS)
        payload_data = data or {}
        payload_data.update({
            "click_action": "FLUTTER_NOTIFICATION_CLICK",
            "lesson_id": str(lesson_id),
            "status": "new_reply" 
        })
        
        # Clean data to strings
        final_data = {k: str(v) for k, v in payload_data.items()}

        message = messaging.Message(
            notification=messaging.Notification(
                title=str(title),
                body=str(body),
            ),
            data=final_data,
            token=str(fcm_token),
            android=messaging.AndroidConfig(
                priority='high', 
                notification=messaging.AndroidNotification(
                    channel_id='high_importance_channel',
                    click_action='FLUTTER_NOTIFICATION_CLICK',
                    default_sound=True,
                    # ✅ FIX: 'notification_priority' hata diya hai, 
                    # 'priority' upar 'high' set hai toh pop-up apne aap aayega.
                ),
            ),

            # iOS ke liye bhi support add kar dete hain safe side
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(badge=1, sound='default'),
                ),
            ),
        )

        response = messaging.send(message)
        print(f'✅ Firebase Success: {response}')
        return True

    except Exception as e:
        if "not-found" in str(e).lower() or "404" in str(e) or "requested entity was not found" in str(e).lower():
            print(f"⚠️ Invalid/Expired FCM token: {e}")

            # Optional: yaha DB se token null bhi kar sakte ho
            # FCMDevice.objects.filter(token=fcm_token).delete()

        else:
            print(f"❌ Firebase Error: {e}")

        return False