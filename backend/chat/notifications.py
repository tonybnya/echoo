from notifications.channels import BaseNotificationChannel

class RabbitMQNotificationChannel(BaseNotificationChannel):
    name = 'rabbitmq'
    providers = ['console'] # For now, use console provider

    def build_payload(self, provider):
        # This payload is what will be sent to the provider
        return {
            'message': self.notification.short_description,
            'source': self.notification.source.username if self.notification.source else 'System',
            'action': self.notification.action,
            'url': self.notification.url,
        }

class ConsoleNotificationChannel(BaseNotificationChannel):
    name = 'console'
    providers = ['console']

    def build_payload(self, provider):
        return {
            'message': self.notification.short_description,
            'source': self.notification.source.username if self.notification.source else 'System',
            'action': self.notification.action,
        }
