// frida -U -f kr.co.eqst.aos -l gta.js
setImmediate(function() {
    Java.perform(function() {
        Java.use("com.android.org.conscrypt.TrustManagerImpl").checkTrustedRecursive.implementation = function (certs, authType, host, clientAuth, ocspData, tlsSctData) {
            return Java.use("java.util.ArrayList").$new();
        }; // (필요 시) SSL 인증 우회
    });
});