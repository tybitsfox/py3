#!/usr/bin/python3
#_*_decoding:utf-8_*_
#感觉需要备份的东西越来越多，写个全面完整的备份脚本吧 ；）
"""allbak.py是一个用来备份我个人资料的脚本文件，通过这个脚本，我可以定期备份，轻松管理我的一些个人资料。
本脚本在备份前会自动将数据库的最新数据导出并备份。而且对每次的备份操作都生成信息文件方便比较和查阅
		Author:	tybitsfox	2022-11-24"""
import os
import time
import subprocess
#{{{配置文件的备份：定义一些固定需要备份的目录或文件
#1、用户目录下配置的备份
istr=['.vimrc','.vim/','.gitconfig','.bashrc','.bochsrc','.fluxbox/','.local/share/zathura/','.local/share/applications/','.config/conky/']
#2、/etc目录下的备份
estr=['apt/sources.list','apt/preferences.d/']
#3、/usr目录下
ustr=['local/bin/','share/fonts/truetype/winfonts/','local/v2ray/']
#个人网站的素材文件备份，依赖于/var/www/.gitignore,也就是没有纳入git管理的全部资料都在这里进行备份
wws='/var/www/.gitignore'
#数据库的备份
dstr=['ty001','env2016','env2017','env2018','gis_hb','web_data','gis_hb2018','gis_hb2019','gis_hb2020','hlgj_2018']
#邮件备份，备份的邮箱为：tyyyyt@163.com,tybitsfox@126.com,tybitsfox@21cn.com;使用的邮件客户端为thunderbird
emstr='/home/tian/.thunderbird/'
#游戏配置及部分模拟器的备份：epsxe,pcsx2,retroarch,mednafen,citra,yuzu,ryujinx,wine,dosbox
gappstr=['Ryujinx/','citra-linux-20221119-bccef5e/','ppsspp/','epsxe32/','retroarch/','yuzu/','duckstation/','citra-linux-20220702-546a8da/','epsxe/']
ginistr=['.config/citra-emu/','.config/ppsspp/','.config/PCSX2/','.config/retroarch/','.config/Ryujinx/','.config/yuzu/','.epsxe/','.local/share/duckstation/','.local/share/ePSXe/','.local/share/citra-emu/','.local/share/yuzu/','.wine/','.zsnes/']
#游戏配置的精简函数，下列目录将被精简
gdelstr=['.config/Ryujinx/games/','.config/retroarch/cheats/','.config/retroarch/downloads/','.config/retroarch/logs/','.config/retroarch/database/','.config/retroarch/shaders/','.config/PCSX2/sstates/','.config/ppsspp/PSP/PPSSPP_STATE/','.local/share/citra-emu/states/']
#生成的压缩备份文件
dststr=['sysini.tar.bz2','webpic.tar.bz2','mysqlbak.tar.bz2','email.tar.bz2','game.tar.bz2','gameini.tar.bz2','']
#}}}
fin_str=[]	#用于保存检测并存在的文件目录，全路径
cur_dir=''
#{{{check_exist(1)	测试配置文件或目录是否存在
def check_exist(x):
	"""para=1：用户配置的测试;=2：个人网站资料备份；=3：数据库备份；=4：邮件目录的测试；=5：游戏程序目录的测试；=6：游戏配置的测试"""
	if x == 1:
		print('用户配置文件或目录检测中...')
		for i in istr:
			j="home/tian/"+i
			if os.access(j,0):
				fin_str.append(j)
				s=j.ljust(80)+"存在"
			else:
				s=j.ljust(80)+"不存在"
			print(s)
		for i in estr:
			j="etc/"+i
			if os.access(j,0):
				fin_str.append(j)
				s=j.ljust(80)+"存在"
			else:
				s=j.ljust(80)+"不存在"
			print(s)
		for i in ustr:
			j="usr/"+i
			if os.access(j,0):
				fin_str.append(j)
				s=j.ljust(80)+"存在"
			else:
				s=j.ljust(80)+"不存在"
			print(s)
	elif x == 2:
		print('个人网站资料备份...')
		if os.access(wws,0):
			f1=open(wws,'r')
			for i in f1.readlines():
				j=i.rstrip()
				if len(j) > 0:
					fin_str.append('var/www/'+j)
			f1.close()
		else:
			print("缺失必要的目录文件，网站资料备份失败！")
			exit(0)
	elif x == 3:
		print('数据库资料更新...')
		s1="home/tian/sql/"
		if os.access(s1,0):
			os.system('rm -rf '+s1+'*')
		else:
			os.system('mkdir '+s1)
		for i in dstr:
			j='sudo mysqldump '+i+' > '+s1+i+'.sql'
#			print(j)
			k=subprocess.run(j,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
			if k.returncode != 0:
				subprocess.run('rm '+s1+i+'.sql',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	elif x == 4:
		print('邮件目录测试...')
		if os.access(emstr,0):
			return 0
		else:
			print("目标目录: "+emstr+" 不存在，备份终止.")
			exit(0)
	elif x == 5:
		print('游戏程序目录测试...')
		for i in gappstr:
			j="usr/games/"+i
			if os.access(j,0):
				fin_str.append(j)
				s=j.ljust(80)+'存在'
			else:
				s=j.ljust(80)+'不存在'
			print(s)
	elif x == 6:
		print('游戏配置测试...')
		for i in ginistr:
			j='home/tian/'+i
			if os.access(j,0):
				fin_str.append(j)
				s=j.ljust(80)+'存在'
			else:
				s=j.ljust(80)+'不存在'
			print(s)
	else:
		return 0
#}}}
#{{{reduce_normal 普通精简
def	reduce_normal():
	print('开始对游戏配置进行精简...')
	for i in gdelstr:
		j='home/tian/'+i
		if os.access(j,0):
#			subprocess.run('rm -rf '+j,shell=True,stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
			print(i.ljust(80)+'已清空')
#}}}
#{{{sub_main()	二级选择，模拟器配置备份：完全备份，精简备份，极简备份
def sub_main():
	print('模拟器配置检测完成！备份有三种方式：1、完全备份\t2、精简备份\t3、极简备份')
	print('\033[31;5m 注意：精简备份会删除现有配置中的某些文件，完全备份和极简备份不会删除任何文件\033[0m')
	i=input('\n请选择：')
	if i == '1':
		print('完全备份...')
		exit(0)
	elif i == '2':
		reduce_normal()
	elif i == '3':
		print('极简备份...')
		exit(0)
	else:
		exit(0)
#}}}	
#{{{main()	主函数
def main():
	"""主函数，调度其他函数或变量完成程序功能"""	
	cur_dir=os.getcwd()		#当前目录路径
	if cur_dir[-1] != '/':
		cur_dir+='/'
	os.system("echo '当前备份设备：' > backup.info")
	os.system('sudo dmidecode -t 1|grep Product >> backup.info')
	t=time.ctime(time.time())
	os.system('echo 当前备份时间：'+t+' >> backup.info')
	os.chdir('/')
	dfile=cur_dir+'backup.info'
	os.system('clear')
	print('---------------------------------------')
	print('|                    	              |')
	print('| 1、系统配置配置备份	2、数据库备份 |')
	print('| 3、个人网站资料备份	4、邮件备份   |')
	print('| 5、模拟器配置备份	6、模拟器备份 |')
	print('|                    	              |')
	print('---------------------------------------')
	i=input('\n请输入你的选择：')
	if i == '1':
		check_exist(1)
		print('配置检测完成，开始备份....')
		os.system('echo 配置检测完成，开始备份.... >> '+dfile)
		cmd='tar cjvf '+cur_dir+dststr[0]+' '
		for j in fin_str:
			cmd+=j+' '
			os.system('echo '+j+' >> '+dfile)
	elif i == '2':		#注意：check_exist函数参数是3
		check_exist(3)
		print('数据库更新完成，开始备份....')
		os.system('echo 数据库更新完成，开始备份.... >> '+dfile)
		cmd='tar cjvf '+cur_dir+dststr[2]+' home/tian/sql/ '
		os.system('ls -latr home/tian/sql/ >> '+dfile)
	elif i == '3':		#check_exist函数参数为2
		check_exist(2)
		print('配置检测完成，开始备份....')
		os.system('echo 配置检测完成，开始备份.... >> '+dfile)
		cmd='tar cjvf '+cur_dir+dststr[1]+' '
		for j in fin_str:
			cmd+=j+' '
			os.system('echo '+j+' >> '+dfile)
	elif i == '4':				#邮件备份
		check_exist(4)
		print('配置检测完成，开始备份....')
		os.system('echo 配置检测完成，开始备份.... >> '+dfile)
		cmd='tar cjvf '+cur_dir+dststr[3]+' '+emstr+' '
	elif i == '5':				#游戏配置；参数为6
		check_exist(6)
#		print('配置检测完成，开始备份....')
		sub_main()
		exit(0)
#		os.system('echo 配置检测完成，开始备份.... >> '+dfile)
#		cmd='tar cjvf '+cur_dir+dststr[5]+' '
#		for j in fin_str:
#			cmd+=j+' '
#			os.system('echo '+j+' >> '+dfile)
	elif i == '6':				#游戏程序备份；参数为5
		check_exist(5)
		print('配置检测完成，开始备份....')
		os.system('echo 配置检测完成，开始备份.... >> '+dfile)
		cmd='tar cjvf '+cur_dir+dststr[4]+' '
		for j in fin_str:
			cmd+=j+' '
			os.system('echo '+j+' >> '+dfile)
	else:
		print('选择错误，备份终止')
		exit(0)
	cmd+=dfile[1:]
	subprocess.run(cmd,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	print('备份完成～～～～～')
#}}}
main()


