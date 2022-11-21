#FROM python:3.9
FROM public.ecr.aws/lambda/python
RUN yum install \
    atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel \
    ipa-gothic-fonts ipa-mincho-fonts unzip -y

RUN pip install selenium

RUN curl -OL https://chromedriver.storage.googleapis.com/107.0.5304.62/chromedriver_linux64.zip \
    && curl -Lo "./chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1047731%2Fchrome-linux.zip?alt=media"\
    && unzip chrome-linux.zip && rm chrome-linux.zip && \
    unzip chromedriver_linux64.zip && rm chromedriver_linux64.zip

COPY aws_tools_class.py ./

COPY main.py ./

RUN ls

CMD [ "main.handler" ]
