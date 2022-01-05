from crontab import CronTab

my_cron = CronTab(user='ubuntu')

job = my_cron.new(command='python3 /Linebot/test_01.py')
job.set_comment("test_01")
#每天早上6點
job.hour.on(6)
job.minute.on(00)

# job.minute.every(1)

# my_cron.remove_all()

my_cron.write()
# $crontab -l

# https://blog.csdn.net/fafadsj666/article/details/104360047?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_title~default-6&spm=1001.2101.3001.4242.3
# 重新開機或重啟容器記得跑下面 sudo service cron start
'''
00 06 * * *  sh /Linebot/run.sh >> /Linebot/logs/mylog.log 2>&1  #每天早上6点运行run.sh
启动
sudo service cron start

編輯
crontab -e

查看
crontab -l

crontab -e 後
00 06 * * *  sh /run.sh所在文件夹/run.sh >> /home/mylog.log 2>&1  #每天早上6点运行run.sh
# 运行脚本输出信息保存在/home/mylog.log

儲存完重啟
sudo service cron restart

参数：
-e　编辑该用户的计时器设置。
-l　列出该用户的计时器设置。
-r　删除该用户的计时器设置。
-u<用户名称> 　指定要设定计时器的用户名称。

 

格式:
*   *　 *　 *　 *　　command
分　时　日　月　周　 命令

第1列表示分钟1～59 每分钟用*或者 */1表示
第2列表示小时1～23（0表示0点）
第3列表示日期1～31
第4列表示月份1～12
第5列标识号星期0～6（0表示星期天）
第6列要运行的命令

'''

