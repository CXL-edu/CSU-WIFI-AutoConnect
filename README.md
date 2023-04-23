# CSU-WIFI AutoConnect

在通过向日葵远控软件使用实验室服务器时，由于服务器连接校园网不稳定，导致服务器下线

该脚本通过检查服务器是否联网，若未连网，连接到校园网，并自动输入存储的校园网账号和密码进行登录。

exe文件可能由于编译时受限于路径，导致无法直接运行，可在本地使用pyinstaller库进行重新编译
```python
pip install pyinstaller
pyinstaller CSU-WIFI-AutoConnect.py
```


git操作：
>git add . 							||将本地的更改添加到缓冲区，.是添加所有更改文件，也可以指定文件，如README.md 
>
>git commit -m "备注"	   ||输入提交信息并压缩文件
>
>git push							 ||将文件上传至云端

>
>git ls-files						   ||查看本地缓冲区的文件
>
>git remote -v					 ||查看连接的远程版本信息
>



更新github

>git remote remove origin	||git取消与远程仓库的连接
>
>git remote add origin https://github.com/...（这里填写GitHub上的地址）//先进行远程连接
>
>git pull	||如果github上的文件发生了更改，需要先将github和本地merge，再将本地修改上传
>
>git add . 							||将本地的更改添加到缓冲区
>
>git commit -m "备注"	   ||输入提交信息并压缩文件
>
>git push							 ||将文件上传至云端





在进行版本控制时，如果有多个分支，需要在命令后面指定分支

>git revert -n <分支名>   ||撤销本地commit
>
>git revert -m <分支名>    ||撤销merge commit
>
>`git revert` 的作用是撤销某个 commit，但是保留该 commit 之前和之后的所有 commit。`git revert` 的操作会将撤销的操作记录下来，以便以后可以恢复。与 `git reset` 不同，`git revert` 不会删除 commit记录。
>
>
>
>git reset <branch-name>         ||默认为mixed方式，撤销本地 commit 并保留工作区更改，但是不将更改放回暂存区
>
>git branch <branch-name>        ||创建分支
>
>git branch -d <branch-name>        ||删除分支
>
>git checkout <branch-name>        ||切换分支
>
>git checkout -b <branch-name>        ||创建并切换到分支
>
>git merge <branch-name>              ||合并<branch-name>分支到当前分支



.gitignore文件，用于提示哪些文件不需要放入git中操作

>#为注释
>
>*txt			# 忽略所有.txt结尾的文件
>
>!lib.txt		# 忽略lib.txt以外的所有文件
>
>/temp		# 忽略根目录下的temp文件，不包含其它目录下的temp文件
>
>build/		# 忽略build/目录下的所有文件
>
>doc/*.txt	# 忽略doc下第一级目录的所有.txt文件，比如忽略doc/note.txt但是不忽略doc/test/note.txt





```python
# 在命令中加入用户名和密码，即可克隆私有仓库，命令如下
# git clone https://username:password@github.com/username/repo_name.git

# !git clone https://CXL:mima123@github.com/CXL-edu/test1.git
# remote: Support for password authentication was removed on August 13, 2021. 
# Please use a personal access token instead.

!git clone https://密钥@github.com/CXL-edu/test1.git
# 改为私有秘钥，https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
```







