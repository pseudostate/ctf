FROM httpd:2.4-alpine

RUN sed -i 's/^Listen 80$/Listen 3000/' /usr/local/apache2/conf/httpd.conf \
    && sed -i 's/^#\(LoadModule proxy_module modules\/mod_proxy.so\)$/\1/' /usr/local/apache2/conf/httpd.conf \
    && sed -i 's/^#\(LoadModule proxy_http_module modules\/mod_proxy_http.so\)$/\1/' /usr/local/apache2/conf/httpd.conf \
    && sed -i 's/^#\(LoadModule headers_module modules\/mod_headers.so\)$/\1/' /usr/local/apache2/conf/httpd.conf \
    && printf '\nServerName localhost\nInclude conf/extra/chall.conf\n' >> /usr/local/apache2/conf/httpd.conf

COPY chall.conf /usr/local/apache2/conf/extra/chall.conf
