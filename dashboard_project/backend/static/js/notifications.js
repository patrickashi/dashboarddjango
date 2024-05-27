document.addEventListener("DOMContentLoaded", function () {
    function fetchUnreadNotifications() {
        fetch('{% url "unread_notification_count" %}')
            .then(response => response.json())
            .then(data => {
                const badge = document.getElementById('notification-badge');
                if (data.unread_count > 0) {
                    badge.style.display = 'inline';
                    badge.textContent = data.unread_count;
                } else {
                    badge.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error fetching unread notifications:', error);
            });
    }

    setInterval(fetchUnreadNotifications, 5000); // Check every 5 seconds
    fetchUnreadNotifications(); // Initial check
});