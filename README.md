��Ŀ | ����
---|---
���� | DllMaker
Ŀ¼ | Github
��ǩ | Github��dll-maker��DllMaker
��ע | [GitHub](https://github.com/laijingfeng/DllMaker)
���� | 2016-12-25
���� | 2017-04-15 14:41:05

[TOC]

# ʹ��

���������ļ������ð汾�ţ�һ������Dll�ļ�

## ����

- ����ŵ�codeĿ¼��ֻ������ߵ�`.cs`�ļ�
- ������dll�ŵ�dllĿ¼��ֻ����`.dll`��`.DLL`�ļ�
- ִ��`run_������_�汾��_�Ƿ�༭����.py`
    - ʾ����
        - `run_JerryDebug_2016-12-26-00_none.py`
        - `run_JerryDebug_2016-12-26-00_UNITY_EDITOR-UNITY_IOS.py`

������ĺ�Ҫ������ģ����磺

```
#if UNITY_EDITOR
    a;
#elif UNITY_ANDROID
    b;
#else
    a;
#endif

#if UNITY_ANDROID && !UNITY_EDITOR
    b;
#else
    a;
#endif

�༭��Androidƽ̨��Ӧ����a������dll�еڶ���д������Ϊb
```

# ˵��

## ����

- code Ҫ�����Dll�Ĵ���ŵ���Ŀ¼��
- dll Ҫ�����Dll�Ĵ�������������Dll�ŵ���Ŀ¼��
- project ����������γɵĹ����ڸ�Ŀ¼��
    - build_log.log ������־
    - `bin/Release` ���ձ���õ�Dll��������
- template �������빤���õ���ģ��
- `dll_maker.log/dll_maker-prev.log` ������־
- `run_xx_xx_xx.py` �����ű�
- `logger.py` log�����ű�

## ����

һ���⹤�����������¼����ļ���
- `xx.sln`
    - �������� 
- `xx.csproj`
    - Dll������
    - �����ļ�ע��
    - �����������
- `AssemblyInfo.cs`
    - �汾��
    - Dll�������

�趨���滻������
- `PROJECT_NAME` ������
- `BUILD_DATE` �汾��