```
export CR_PAT=YOUR_TOKEN  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
pass init
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin

docker push ghcr.io/NAMESPACE/IMAGE_NAME:latest
```

---
Trouble shutting

Error saving credentials: error storing credentials - err: exit status 1, out: `error storing credentials - err: exit status 1, out: `pass not initialized: exit status 1: Error: password store is
empty. Try "pass init".``

```
service docker stop
rm ~/.docker/config.json
echo $CR_PAT | docker login ghcr.io -u Ap3lsin4k --password-stdin
Login Succeeded
```

---

```
docker tag <imageId or imageName> <nexus-hostname>:<repository-port>/<image>:<tag>

cc7ac30e4c1d378057b59df03e051d988313c7d12bd4d9116b3bc2e642393fc8
sha256:7e0f6ec0d61e8b356ed4c1422c3263ce2743dbc67a9973af9dd417ad90a8be6c
docker tag sha256:7e0f6ec0d61e8b356ed4c1422c3263ce2743dbc67a9973af9dd417ad90a8be6c ghcr.io/itmolerningproject/odoo16:latest
docker push ghcr.io/itmolerningproject/odoo16:latest
```

Source:
https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry

[main.md](main.md)