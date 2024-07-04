def notifications_count(request):
    if request.user.is_authenticated:
        notifications = request.user.notifications.filter(is_read=False)
        total_notifications = len(notifications)
    else:
        total_notifications = 0
        
    return {'total_notifications': total_notifications}