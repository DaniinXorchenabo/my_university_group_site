FROM python:3.8
LABEL maintainer="rkbcu@mail.ru"
RUN pip install --upgrade pip && pip install pymorphy2 && pip install vk_api && pip install regex && pip install nltk && pip install pony
ADD https://github.com/DaniinXorchenabo/vk_bot_for_group_chats_2.git / ./
EXPOSE 80
CMD ["python", "./main.py"]