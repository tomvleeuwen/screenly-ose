FROM debian:jessie
MAINTAINER Sebastian Schildt <sebastian@frozenlight.de>

#Build from main directore with  docker build -f mothership/Dockerfile -t mothership .

RUN apt-get update && \
    apt-get -y install git-core net-tools python-pip python-requests python-netifaces python-simplejson python-imaging python-dev sqlite3 libffi-dev libssl-dev screen vim openssh-server && \
    apt-get clean

# Install Python requirements
RUN pip install web.py
ADD requirements.txt /tmp/requirements.txt
RUN pip install --upgrade cffi
RUN pip install -r /tmp/requirements.txt


# Create runtime user
RUN useradd pi

# Install config file and file structure
RUN mkdir -p /home/pi/.screenly /home/pi/screenly /home/pi/screenly_assets
COPY ansible/roles/screenly/files/screenly.conf /home/pi/.screenly/screenly.conf
RUN chown -R pi:pi /home/pi



# Copy in code base
COPY . /home/pi/screenly

RUN ls /home
RUN ls /home/pi/screenly
RUN ls /home/pi/screenly/bin
RUN chown -R pi:pi /home/pi/screenly/

RUN python /home/pi/screenly/bin/createAuth.py
RUN echo "admin:admin" > /home/pi/screenly/mothership/secret

#local server instance should talk to local mothership
RUN echo "[beacon]" >> /home/pi/.screenly/screenly.conf 
RUN echo "mothership = 127.0.0.1:9000" >> /home/pi/.screenly/screenly.conf 

USER pi
WORKDIR /home/pi/screenly

EXPOSE 8080
EXPOSE 9000

CMD mothership/dockerrun.sh
