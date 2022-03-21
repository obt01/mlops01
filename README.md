# mlops01

```
$ curl "http://localhost:8010/predict/test"
$ curl "http://localhost:8010/predict" -F "file=@data/bobby.jpg"
```


## TorchServe

```
$ curl http://host.docker.internal:8080/ping
$ curl http://host.docker.internal:8081/models
$ curl -X POST http://host.docker.internal:8080/predictions/resnet101 -F "file=@data/bobby.jpg"
```