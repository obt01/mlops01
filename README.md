# mlops01



## TorchServe

```
$ curl http://host.docker.internal:8080/ping
$ curl http://host.docker.internal:8081/models
$ curl -X POST http://host.docker.internal:8080/predictions/resnet101 -T ./data/bobby.jpg
```