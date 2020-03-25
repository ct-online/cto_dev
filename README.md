# Work with the docker dev environment:
Stay in this directory and execute these commands as administrator/root user.

1. Create image and run container:
docker-compose up -d

2. Stop / Start container:
docker-compose stop
docker-compose start

3. Get an interactive shell on the dev container:
docker-compose exec cto_dev /bin/bash

4. Delete the dev environment:
If you want to delete the docker container use `docker-compose down`.
This command will remove the container and delete all files. 
To save the data permanently you can use the /root/share folder.

# Create a plugin skeleton:
1. Get an interactive shell on the dev container:
docker-compose exec cto_dev /bin/bash
2. cd share/cto_skeleton
3. python3 cto_gulp_skeleton.py 'module_name' 'plugin_name' '1.0.0' 'module description'
4. Go into your module created in step 3.
cd cto_skeleton/module_name
5. Install project dependencies:
npm install
6. Build project:
gulp
7. See your result in the "dist" folder.
