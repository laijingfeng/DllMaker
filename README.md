项目 | 内容
---|---
标题 | DllMaker
目录 | Github
标签 | Github、dll-maker、DllMaker
备注 | [GitHub](https://github.com/laijingfeng/DllMaker)
创建 | 2016-12-25
更新 | 2017-04-02 12:06:58

[TOC]

# 使用

给定代码文件，设置版本号，一键生成Dll文件

## 步骤

- 代码放到code目录，只会拿里边的`.cs`文件
- 依赖的dll放到dll目录，只会拿`.dll`和`.DLL`文件
- 执行`run_工程名_版本号_是否编辑器用.py`
    - 示例：`run_JerryDebug_2016-12-26-00_0.py`

> 备注：`是否编辑器用`是针对Unity，编辑器用会打上`UNITY_EDITOR`的宏，输出文件会是`XXX_Editor`，将来配置给`Editor`用
> 
> Unity的Dll文件可以是以下两种形式：
> 
> 1. XXX（Android和IOS平台）、XXX_Editor（Editor平台）
>
> 2. XXX（Any平台）

# 说明

## 介绍

- code 要编译成Dll的代码放到该目录下
- dll 要编译成Dll的代码依赖的其他Dll放到该目录下
- project 编译过程中形成的工程在该目录下
    - build_log.log 编译日志
    - `bin/Release` 最终编译好的Dll会在这里
- template 构建编译工程用到的模板
- `dll_maker.log/dll_maker-prev.log` 操作日志
- `run_xx_xx_x.py` 启动脚本
- `logger.py` log辅助脚本

## 背景

一个库工程主体是以下几个文件：
- `xx.sln`
    - 启动工程 
- `xx.csproj`
    - Dll依赖项
    - 代码文件注册
- `AssemblyInfo.cs`
    - 版本号
    - Dll输出名字

设定的替换变量：
- `PROJECT_NAME` 工程名
- `BUILD_DATE` 版本号