Dataset **Tsinghua Tencent 2021** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzM1MDlfVHNpbmdodWEgVGVuY2VudCAyMDIxL3RzaW5naHVhLXRlbmNlbnQtMjAyMS1EYXRhc2V0TmluamEudGFyIiwgInNpZyI6ICJTN0tPVFI5czB1UzJBTVJkdHB2emd5b1V1c0orcitzSi9JNmt6MTJRS05nPSJ9)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Tsinghua Tencent 2021', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://cg.cs.tsinghua.edu.cn/traffic-sign/tt100k_2021.zip).