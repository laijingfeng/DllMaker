��Ŀ | ����
---|---
���� | DllMaker
Ŀ¼ | Github
��ǩ | Github��dll-maker��DllMaker
��ע | [GitHub](https://github.com/laijingfeng/DllMaker)
���� | 2016-12-25
���� | 2017-04-02 12:06:58

[TOC]

# ʹ��

���������ļ������ð汾�ţ�һ������Dll�ļ�

## ����

- ����ŵ�codeĿ¼��ֻ������ߵ�`.cs`�ļ�
- ������dll�ŵ�dllĿ¼��ֻ����`.dll`��`.DLL`�ļ�
- ִ��`run_������_�汾��_�Ƿ�༭����.py`
    - ʾ����`run_JerryDebug_2016-12-26-00_0.py`

> ��ע��`�Ƿ�༭����`�����Unity���༭���û����`UNITY_EDITOR`�ĺ꣬����ļ�����`XXX_Editor`���������ø�`Editor`��
> 
> Unity��Dll�ļ�����������������ʽ��
> 
> 1. XXX��Android��IOSƽ̨����XXX_Editor��Editorƽ̨��
>
> 2. XXX��Anyƽ̨��

# ˵��

## ����

- code Ҫ�����Dll�Ĵ���ŵ���Ŀ¼��
- dll Ҫ�����Dll�Ĵ�������������Dll�ŵ���Ŀ¼��
- project ����������γɵĹ����ڸ�Ŀ¼��
    - build_log.log ������־
    - `bin/Release` ���ձ���õ�Dll��������
- template �������빤���õ���ģ��
- `dll_maker.log/dll_maker-prev.log` ������־
- `run_xx_xx_x.py` �����ű�
- `logger.py` log�����ű�

## ����

һ���⹤�����������¼����ļ���
- `xx.sln`
    - �������� 
- `xx.csproj`
    - Dll������
    - �����ļ�ע��
- `AssemblyInfo.cs`
    - �汾��
    - Dll�������

�趨���滻������
- `PROJECT_NAME` ������
- `BUILD_DATE` �汾��