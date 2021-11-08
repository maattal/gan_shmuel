from datetime import datetime

date_string = "20190625091115"
t = datetime.strptime(date_string, '%Y%m%d%H%M%S')
t1 = "today at 000000"
t2 = "now"
my_list = ['in','out','none']
my_string = ','.join(my_list) 



print (my_string)
print (t1,t2)