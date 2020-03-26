
# nginx-webdav

A WebDAV server (wsgidav) behind an NGINX instance, secured by client-side certificates.
  
## User configuration

The nginx instance is configured to request SSL client certificates, and uses the certificate to identify the user and serve a separate directory for them.
The username is expected to be the Subject of the certificate. The WebDAV server expects a directory for each user to exist under the root data directory. For instance, if client certificates for "john" and "josh" have been issued, the following is how the data directory is expected to look:
* /data
  * john
    * jonh's files
  * josh
    * josh's files

## Volumes

* **/ssl**: the certificates to use by nginx. The following files are expected to be there:
  * **server.crt**: the server certificate
  * **server.key**: the server certificate private key
  * **client.crt**: the CA used to verify client certificates
* **/data**: the root directory for the WebDAV data. Subfolders are presumed to exist per user, as described above.

## Running in docker-compose

```yaml
version: "3"
services:
  nginx:
    image: alexta69/nginx-webdav
    container_name: nginx-webdav
     restart: unless-stopped
    ports:
      - "443:443"
    volumes:
      - /path/to/data:/data
      - /path/to/ssl:/ssl
```
