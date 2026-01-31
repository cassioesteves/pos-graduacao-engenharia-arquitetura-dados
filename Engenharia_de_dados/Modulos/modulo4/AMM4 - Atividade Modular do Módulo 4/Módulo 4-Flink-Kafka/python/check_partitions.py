from confluent_kafka.admin import AdminClient

def check_partitions():
    conf = {'bootstrap.servers': '127.0.0.1:9092'}
    admin_client = AdminClient(conf)
    
    topic_name = "sales-transactions"
    md = admin_client.list_topics(timeout=10)
    
    if topic_name in md.topics:
        partitions = md.topics[topic_name].partitions
        print(f"Topic '{topic_name}' has {len(partitions)} partitions.")
    else:
        print(f"Topic '{topic_name}' not found.")

if __name__ == "__main__":
    check_partitions()
