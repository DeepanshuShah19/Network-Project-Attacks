FROM adorigi/victim_image

COPY resolv.conf /etc/resolv.conf.override

COPY start.sh /
RUN  chmod +x /start.sh 

CMD [ "/start.sh"]

RUN apt update && apt install wget
