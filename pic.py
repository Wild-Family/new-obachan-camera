from azure.servicebus import ServiceBusService, Message, Queue
import settings

bus_service = ServiceBusService(
    #service_namespace='mynamespace',
    shared_access_key_name=settings.SHARED_ACCESS_KEY_NAME,
    shared_access_key_value=settings.SHARED_ACCESS_KEY
    )

if __name__ == "__main__":
    print(settings.SHARED_ACCESS_KEY)
    #msg = bus_service.receive_queue_message('taskqueue', peek_lock=False)
    #print(msg.body)