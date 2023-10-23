# 第1节 Git命令

## 设置用户

```powershell
git config --global user.name <username>  #设置用户签名
git config --global user.email <email>    #设置用户邮箱
```



## 新建本地库

```powershell
git init  #初始化当前的文件为git本地库
```





## 对本地库进行操作

### 1.查看当前状态

```
git status
```



### 2.加入暂存区

**添加文件到暂存区：**`git add <filename>`

**从暂存区删除:**`git rm -cached <file>`



### 3.提交到本地库

```powershell
git commit -m "logname" <file>  #提交到本地库(以logname为日志信息)

git reflog  #本地库的简易信息
git log     #本地库的详细信息
```



### 4.版本穿梭

```
git reset --hard <version_number>  #回退到某个版本
```





## GIT分支

复制当前的主线到分支上,与主线相分离,独立开发

***好处:***

1. 并行开发,提高效率
2. 开发失误不会影响到其它分支



### 1.基本语法

```
git branch <branchname>   # 创建分支
git branch -v             # 查看分支
git switch(checkout) <branchname>   # 切换分支
git merge  <branchname>   # 合并分支到当前分支
```



### 2.代码冲突

两个文件对同一位置都有修改,则合并的时候会出现代码冲突

需要人为的来进行冲突的界定







# 第2节  远程仓库

## 创建别名

```
git remote add <othername> <repo-URL>   #创建远程库的别名
git remote -v   #查看远程库的别名
```





## 远程库与本地库的交互

```
git push <myrepo> <branch>   #推送本地库的某分支到远程库
git pull <myrepo> <branch>   #拉取远程库的某分支到本地库

git clone <repo-URL>         #克隆远程库
// 1.克隆代码  2.创建本地库  3.创建别名
```



## 团队协作

