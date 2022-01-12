from consumer import KafkaConsumer_
#cg=consumer_group이라는 뜻

basic_cg = KafkaConsumer_()
basic_cg.set_group_id('220112')
basic_cg.set_topic_name('boaz_youtube_2')
print(basic_cg.get_group_id())
print(basic_cg.get_topic_name())
# basic_cg._consume()